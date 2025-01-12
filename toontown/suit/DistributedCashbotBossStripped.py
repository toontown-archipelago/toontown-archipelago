import functools
import random

from direct.directnotify import DirectNotifyGlobal
from direct.fsm import FSM
from direct.gui.OnscreenText import OnscreenText
from direct.interval.IntervalGlobal import *
from direct.task.Task import Task
from panda3d.core import *
from panda3d.direct import *

from libotp import *
from otp.otpbase import OTPGlobals
from toontown.building import ElevatorConstants
from toontown.coghq import CraneLeagueGlobals
from toontown.coghq.ActivityLog import ActivityLog
from toontown.coghq.BossSpeedrunTimer import BossSpeedrunTimedTimer, BossSpeedrunTimer
from toontown.distributed import DelayDelete
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals
from . import DistributedBossCog
from . import SuitDNA
from .DistributedBossCogStripped import DistributedBossCogStripped

TTL = TTLocalizer
from toontown.coghq import BossHealthBar
from toontown.coghq.CraneLeagueHeatDisplay import CraneLeagueHeatDisplay


class DistributedCashbotBossStripped(DistributedBossCogStripped):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedCashbotBoss')
    numFakeGoons = 3

    BASE_HEAT = 500

    def __init__(self, cr):
        super().__init__(cr)

        # hack for quick access while debugging
        base.boss = self

        self.wantCustomCraneSpawns = False
        self.customSpawnPositions = {}
        self.ruleset = CraneLeagueGlobals.CFORuleset()  # Setup a default ruleset as a fallback
        self.modifiers = []
        self.heatDisplay = CraneLeagueHeatDisplay()
        self.heatDisplay.hide()
        self.spectators = []
        self.localToonSpectating = False
        self.endVault = None
        self.warningSfx = None
        # By "heldObject", we mean the safe he's currently wearing as
        # a helmet, if any.  It's called a heldObject because this is
        # the way the cranes refer to the same thing, and we use the
        # same interface to manage this.
        self.heldObject = None

        self.latency = 0.5  # default latency for updating object posHpr

        self.activityLog = ActivityLog()

        self.toonSpawnpointOrder = [i for i in range(8)]
        self.stunEndTime = 0
        self.myHits = []
        self.tempHp = self.ruleset.CFO_MAX_HP
        self.processingHp = False
        return

    def setToonSpawnpoints(self, order):
        self.toonSpawnpointOrder = order

    def addToActivityLog(self, doId, content):
        doObj = base.cr.doId2do.get(doId)

        try:
            name = doObj.getName()
        except:
            name = doId

        msg = '[%s]' % name
        msg += ' %s' % content
        self.activityLog.addToLog(msg)

    def debug(self, doId='system', content='null'):
        if self.ruleset.GENERAL_DEBUG:
            self.addToActivityLog(doId, content)

    def goonStatesDebug(self, doId='system', content='null'):
        if self.ruleset.GOON_STATES_DEBUG:
            self.addToActivityLog(doId, content)

    def safeStatesDebug(self, doId='system', content='null'):
        if self.ruleset.SAFE_STATES_DEBUG:
            self.addToActivityLog(doId, content)

    def craneStatesDebug(self, doId='system', content='null'):
        if self.ruleset.CRANE_STATES_DEBUG:
            self.addToActivityLog(doId, content)

    def updateSpectators(self, specs):
        self.spectators = specs
        if not self.localToonSpectating and localAvatar.doId in self.spectators:
            self.setLocalToonSpectating()
        elif self.localToonSpectating and localAvatar.doId not in self.spectators:
            self.disableLocalToonSpectating()

        for toonId in self.involvedToons:
            t = base.cr.doId2do.get(toonId)
            if t:
                if toonId in self.spectators:
                    t.hide()
                elif toonId in self.getInvolvedToonsNotSpectating():
                    t.show()

    def setLocalToonSpectating(self):
        self.localToonSpectating = True
        self.localToonIsSafe = True

    def disableLocalToonSpectating(self):
        self.localToonSpectating = False
        self.localToonIsSafe = False

    def getInvolvedToonsNotSpectating(self):
        toons = list(self.involvedToons)
        for s in self.spectators:
            if s in toons:
                toons.remove(s)

        return toons

    def announceGenerate(self):
        super().announceGenerate()

        # at this point all our attribs have been filled in.
        self.setName(TTLocalizer.CashbotBossName)
        nameInfo = TTLocalizer.BossCogNameWithDept % {'name': self._name,
                                                      'dept': SuitDNA.getDeptFullname(self.style.dept)}
        self.setDisplayName(nameInfo)

        # Our goal in this battle is to drop stuff on the CFO's head.
        # For this, we need a target.
        target = CollisionSphere(2, 0, 0, 3)
        targetNode = CollisionNode('headTarget')
        targetNode.addSolid(target)
        targetNode.setCollideMask(ToontownGlobals.PieBitmask)
        self.headTarget = self.neck.attachNewNode(targetNode)
        # self.headTarget.show()

        # And he gets a big bubble around his torso, just to keep
        # things from falling through him.  It's a big sphere so
        # things will tend to roll off him instead of landing on him.
        shield = CollisionSphere(0, 0, 0.8, 7)
        shieldNode = CollisionNode('shield')
        shieldNode.addSolid(shield)
        shieldNode.setCollideMask(ToontownGlobals.PieBitmask)
        self.pelvis.attachNewNode(shieldNode)

        self.eyes = loader.loadModel('phase_10/models/cogHQ/CashBotBossEyes.bam')

        # Get the eyes ready for putting outside the helmet.
        self.eyes.setPosHprScale(4.5, 0, -2.5, 90, 90, 0, 0.4, 0.4, 0.4)
        self.eyes.reparentTo(self.neck)
        self.eyes.hide()

    def getBossMaxDamage(self):
        return self.ruleset.CFO_MAX_HP

    def calculateHeat(self):
        bonusHeat = 0
        # Loop through all modifiers present and calculate the bonus heat
        for modifier in self.modifiers:
            bonusHeat += modifier.getHeat()

        return self.BASE_HEAT + bonusHeat

    def setModifiers(self, mods):
        modsToSet = []  # A list of CFORulesetModifierBase subclass instances
        for modStruct in mods:
            modsToSet.append(CraneLeagueGlobals.CFORulesetModifierBase.fromStruct(modStruct))

        self.modifiers = modsToSet
        self.modifiers.sort(key=lambda m: m.MODIFIER_TYPE)

    def disable(self):
        """
        This method is called when the DistributedObject
        is removed from active duty and stored in a cache.
        """
        super().disable()
        del base.boss

    def makeBossFleeMovie(self):
        # Generate an interval which shows the boss giving up and
        # running out the door, only to be nailed by a passing train.

        hadEnough = TTLocalizer.CashbotBossHadEnough
        outtaHere = TTLocalizer.CashbotBossOuttaHere
        loco = loader.loadModel('phase_10/models/cogHQ/CashBotLocomotive')
        car1 = loader.loadModel('phase_10/models/cogHQ/CashBotBoxCar')
        car2 = loader.loadModel('phase_10/models/cogHQ/CashBotTankCar')
        trainPassingSfx = base.loader.loadSfx('phase_10/audio/sfx/CBHQ_TRAIN_pass.ogg')
        boomSfx = loader.loadSfx('phase_3.5/audio/sfx/ENC_cogfall_apart.ogg')
        rollThroughDoor = self.rollBossToPoint(fromPos=Point3(120, -280, 0), fromHpr=None, toPos=Point3(120, -250, 0),
                                               toHpr=None, reverse=0)
        rollTrack = Sequence(Func(self.getGeomNode().setH, 180), rollThroughDoor[0], Func(self.getGeomNode().setH, 0))

        # Generate a track that shows one long train running by (which
        # it achieves by running the same two cars repeatedly past
        # the door).

        # The trains move at 300 ft/s, so a gap of this much time puts
        # car2 80 ft behind car1.
        g = 80.0 / 300.0
        trainTrack = Track(
            (0 * g, loco.posInterval(0.5, Point3(0, -242, 0), startPos=Point3(150, -242, 0))),
            (1 * g, car2.posInterval(0.5, Point3(0, -242, 0), startPos=Point3(150, -242, 0))),
            (2 * g, car1.posInterval(0.5, Point3(0, -242, 0), startPos=Point3(150, -242, 0))),
            (3 * g, car2.posInterval(0.5, Point3(0, -242, 0), startPos=Point3(150, -242, 0))),
            (4 * g, car1.posInterval(0.5, Point3(0, -242, 0), startPos=Point3(150, -242, 0))),
            (5 * g, car2.posInterval(0.5, Point3(0, -242, 0), startPos=Point3(150, -242, 0))),
            (6 * g, car1.posInterval(0.5, Point3(0, -242, 0), startPos=Point3(150, -242, 0))),
            (7 * g, car2.posInterval(0.5, Point3(0, -242, 0), startPos=Point3(150, -242, 0))),
            (8 * g, car1.posInterval(0.5, Point3(0, -242, 0), startPos=Point3(150, -242, 0))),
            (9 * g, car2.posInterval(0.5, Point3(0, -242, 0), startPos=Point3(150, -242, 0))),
            (10 * g, car1.posInterval(0.5, Point3(0, -242, 0), startPos=Point3(150, -242, 0))),
            (11 * g, car2.posInterval(0.5, Point3(0, -242, 0), startPos=Point3(150, -242, 0))),
            (12 * g, car1.posInterval(0.5, Point3(0, -242, 0), startPos=Point3(150, -242, 0))),
            (13 * g, car2.posInterval(0.5, Point3(0, -242, 0), startPos=Point3(150, -242, 0))),
            (14 * g, car1.posInterval(0.5, Point3(0, -242, 0), startPos=Point3(150, -242, 0))))
        bossTrack = Track(
            (0.0, Sequence(
                Func(camera.reparentTo, render),
                Func(camera.setPosHpr, 105, -280, 20, -158, -3, 0),
                Func(self.reparentTo, render),
                Func(self.show),
                Func(self.clearChat),
                Func(self.setPosHpr, *ToontownGlobals.CashbotBossBattleThreePosHpr),
                Func(self.reverseHead),
                ActorInterval(self, 'Fb_firstHit'),
                ActorInterval(self, 'Fb_down2Up'))),
            (1.0, Func(self.setChatAbsolute, hadEnough, CFSpeech)),
            (5.5, Parallel(
                Func(camera.setPosHpr, 100, -315, 16, -20, 0, 0),
                Func(self.hideBattleThreeObjects),
                Func(self.forwardHead),
                Func(self.loop, 'Ff_neutral'),
                rollTrack,
                self.door3.posInterval(2.5, Point3(0, 0, 25), startPos=Point3(0, 0, 18)))),
            (5.5, Func(self.setChatAbsolute, outtaHere, CFSpeech)),
            (5.5, SoundInterval(trainPassingSfx)),
            (8.1, Func(self.clearChat)),
            (9.4, Sequence(
                Func(loco.reparentTo, render),
                Func(car1.reparentTo, render),
                Func(car2.reparentTo, render),
                trainTrack,
                Func(loco.detachNode),
                Func(car1.detachNode),
                Func(car2.detachNode),
                Wait(2))),
            (9.5, SoundInterval(boomSfx)),
            (9.5, Sequence(
                self.posInterval(0.4, Point3(0, -250, 0)),
                Func(self.stash))))
        return bossTrack

    def setBossDamage(self, bossDamage, avId=0, objId=0, isGoon=False):

        if avId != base.localAvatar.doId or isGoon or (objId not in self.myHits):
            if bossDamage > self.bossDamage:
                delta = bossDamage - self.bossDamage
                self.flashRed()

                # Animate the hit if the CFO should flinch
                if self.ruleset.CFO_FLINCHES_ON_HIT:
                    self.doAnimate('hit', now=1)

                self.showHpText(-delta, scale=5)

        if objId in self.myHits:
            self.myHits.remove(objId)

        self.bossDamage = bossDamage
        self.updateHealthBar()
        self.bossHealthBar.update(self.ruleset.CFO_MAX_HP - bossDamage, self.ruleset.CFO_MAX_HP)
        self.processingHp = False
        self.tempHp = self.ruleset.CFO_MAX_HP - self.bossDamage

    def setCraneSpawn(self, want, spawn, toonId):
        self.wantCustomCraneSpawns = want
        self.customSpawnPositions[toonId] = spawn

    def prepareBossForBattle(self):
        if self.bossHealthBar:
            self.bossHealthBar.cleanup()
            self.bossHealthBar = BossHealthBar.BossHealthBar(self.style.dept)

        self.cleanupIntervals()

        self.clearChat()
        self.reparentTo(render)

        self.setPosHpr(*ToontownGlobals.CashbotBossBattleThreePosHpr)

        self.happy = 1
        self.raised = 1
        self.forward = 1
        self.doAnimate()

        self.generateHealthBar()
        self.updateHealthBar()

        # Display Health Bar
        self.bossHealthBar.initialize(self.ruleset.CFO_MAX_HP - self.bossDamage, self.ruleset.CFO_MAX_HP)

    def cleanupBossBattle(self):
        self.cleanupIntervals()
        self.stopAnimate()
        self.cleanupAttacks()
        self.setDizzy(0)
        self.removeHealthBar()

    def saySomething(self, chatString):
        intervalName = 'CFOTaunt'
        seq = Sequence(name=intervalName)
        seq.append(Func(self.setChatAbsolute, chatString, CFSpeech))
        seq.append(Wait(4.0))
        seq.append(Func(self.clearChat))
        oldSeq = self.activeIntervals.get(intervalName)
        if oldSeq:
            oldSeq.finish()
        seq.start()
        self.storeInterval(seq, intervalName)

    def setAttackCode(self, attackCode, avId=0, delayTime=0):
        super().setAttackCode(attackCode, avId)

        if attackCode == ToontownGlobals.BossCogAreaAttack:
            self.saySomething(TTLocalizer.CashbotBossAreaAttackTaunt)
            base.playSfx(self.warningSfx)

        if attackCode in (ToontownGlobals.BossCogDizzy, ToontownGlobals.BossCogDizzyNow):
            self.stunEndTime = globalClock.getFrameTime() + delayTime
        else:
            self.stunEndTime = 0

    def localToonDied(self):
        super().localToonDied()
        self.localToonIsSafe = 1

    def grabObject(self, obj):
        # Grab a safe and put it on as a helmet.  This method mirrors
        # a similar method on DistributedCashbotBossCrane.py; it goes
        # through the same API as a crane picking up a safe.

        # This is only called by DistributedCashbotBossObject.enterGrabbed().
        obj.wrtReparentTo(self.neck)
        obj.hideShadows()
        obj.stashCollisions()
        if obj.lerpInterval:
            obj.lerpInterval.finish()
        obj.lerpInterval = Parallel(obj.posInterval(ToontownGlobals.CashbotBossToMagnetTime, Point3(-1, 0, 0.2)),
                                    obj.quatInterval(ToontownGlobals.CashbotBossToMagnetTime, VBase3(0, -90, 90)),
                                    Sequence(Wait(ToontownGlobals.CashbotBossToMagnetTime), ShowInterval(self.eyes)),
                                    obj.toMagnetSoundInterval)
        obj.lerpInterval.start()
        self.heldObject = obj

    def dropObject(self, obj):
        # Drop a helmet on the ground.

        # This is only called by DistributedCashbotBossObject.exitGrabbed().
        assert self.heldObject == obj

        if obj.lerpInterval:
            obj.lerpInterval.finish()
            obj.lerpInterval = None

        obj = self.heldObject
        obj.wrtReparentTo(render)
        obj.setHpr(obj.getH(), 0, 0)
        self.eyes.hide()

        # Actually, we shouldn't reveal the shadows until it
        # reaches the ground again.  This will do for now.
        obj.showShadows()
        obj.unstashCollisions()

        self.heldObject = None
