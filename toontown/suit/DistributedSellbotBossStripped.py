import math
import random

from direct.directnotify import DirectNotifyGlobal
from direct.directutil import Mopath
from direct.distributed.ClockDelta import *
from direct.fsm import FSM
from direct.interval.IntervalGlobal import *
from direct.task import Task
from direct.task.TaskManagerGlobal import taskMgr

from libotp import *
from toontown.battle.BattleProps import *
from toontown.coghq import CogDisguiseGlobals
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals
from . import SuitDNA
from .DistributedBossCogStripped import DistributedBossCogStripped


class DistributedSellbotBossStripped(DistributedBossCogStripped):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedSellbotBoss')

    def __init__(self, cr):
        DistributedBossCogStripped.__init__(self, cr)
        self.bossDamage = 0
        self.attackCode = None
        self.attackAvId = 0
        self.recoverRate = 0
        self.recoverStartTime = 0
        self.bossDamageMovie = None
        self.insidesANodePath = None
        self.insidesBNodePath = None
        self.strafeInterval = None
        self.bossMaxDamage = ToontownGlobals.SellbotBossMaxDamage

    def announceGenerate(self):
        DistributedBossCogStripped.announceGenerate(self)
        self.setName(TTLocalizer.SellbotBossName)
        nameInfo = TTLocalizer.BossCogNameWithDept % {'name': self._name,
         'dept': SuitDNA.getDeptFullname(self.style.dept)}
        self.setDisplayName(nameInfo)
        self.cageDoorSfx = loader.loadSfx('phase_5/audio/sfx/CHQ_SOS_cage_door.ogg')
        self.cageLandSfx = loader.loadSfx('phase_9/audio/sfx/CHQ_SOS_cage_land.ogg')
        self.cageLowerSfx = loader.loadSfx('phase_5/audio/sfx/CHQ_SOS_cage_lower.ogg')
        self.strafeSfx = []
        for i in range(10):
            self.strafeSfx.append(loader.loadSfx('phase_3.5/audio/sfx/SA_shred.ogg'))

        render.setTag('pieCode', str(ToontownGlobals.PieCodeNotBossCog))
        insidesA = CollisionPolygon(Point3(4.0, -2.0, 5.0), Point3(-4.0, -2.0, 5.0), Point3(-4.0, -2.0, 0.5), Point3(4.0, -2.0, 0.5))
        insidesANode = CollisionNode('BossZap')
        insidesANode.addSolid(insidesA)
        insidesANode.setCollideMask(ToontownGlobals.PieBitmask | ToontownGlobals.WallBitmask)
        self.insidesANodePath = self.axle.attachNewNode(insidesANode)
        self.insidesANodePath.setTag('pieCode', str(ToontownGlobals.PieCodeBossInsides))
        self.insidesANodePath.stash()
        insidesB = CollisionPolygon(Point3(-4.0, 2.0, 5.0), Point3(4.0, 2.0, 5.0), Point3(4.0, 2.0, 0.5), Point3(-4.0, 2.0, 0.5))
        insidesBNode = CollisionNode('BossZap')
        insidesBNode.addSolid(insidesB)
        insidesBNode.setCollideMask(ToontownGlobals.PieBitmask | ToontownGlobals.WallBitmask)
        self.insidesBNodePath = self.axle.attachNewNode(insidesBNode)
        self.insidesBNodePath.setTag('pieCode', str(ToontownGlobals.PieCodeBossInsides))
        self.insidesBNodePath.stash()
        target = CollisionTube(0, -1, 4, 0, -1, 9, 3.5)
        targetNode = CollisionNode('BossZap')
        targetNode.addSolid(target)
        targetNode.setCollideMask(ToontownGlobals.PieBitmask)
        self.targetNodePath = self.pelvis.attachNewNode(targetNode)
        self.targetNodePath.setTag('pieCode', str(ToontownGlobals.PieCodeBossCog))
        shield = CollisionTube(0, 1, 4, 0, 1, 7, 3.5)
        shieldNode = CollisionNode('BossZap')
        shieldNode.addSolid(shield)
        shieldNode.setCollideMask(ToontownGlobals.PieBitmask | ToontownGlobals.CameraBitmask)
        shieldNodePath = self.pelvis.attachNewNode(shieldNode)
        disk = loader.loadModel('phase_9/models/char/bossCog-gearCollide')
        disk.find('**/+CollisionNode').setName('BossZap')
        disk.reparentTo(self.pelvis)
        disk.setZ(0.8)

    def disable(self):
        DistributedBossCogStripped.disable(self)
        self.__cleanupStrafe()
        render.clearTag('pieCode')
        self.targetNodePath.detachNode()

    def d_hitBoss(self, bossDamage):
        self.sendUpdate('hitBoss', [bossDamage])

    def d_hitBossInsides(self):
        self.sendUpdate('hitBossInsides', [])

    def d_hitToon(self, toonId):
        self.sendUpdate('hitToon', [toonId])

    def setBossDamage(self, bossDamage, recoverRate, timestamp):
        self.bossHealthBar.update(self.bossMaxDamage - bossDamage, self.bossMaxDamage)
        recoverStartTime = globalClockDelta.networkToLocalTime(timestamp)
        self.bossDamage = bossDamage
        self.recoverRate = recoverRate
        self.recoverStartTime = recoverStartTime
        taskName = 'RecoverBossDamage'
        taskMgr.remove(taskName)
        if self.bossDamageMovie:
            if self.bossDamage >= self.bossMaxDamage:
                self.bossDamageMovie.resumeUntil(self.bossDamageMovie.getDuration())
            else:
                self.bossDamageMovie.resumeUntil(self.bossDamage * self.bossDamageToMovie)
                if self.recoverRate:
                    taskMgr.add(self.__recoverBossDamage, taskName)

    def getBossDamage(self):
        now = globalClock.getFrameTime()
        elapsed = now - self.recoverStartTime
        return max(self.bossDamage - self.recoverRate * elapsed / 60.0, 0)

    def __recoverBossDamage(self, task):
        self.bossDamageMovie.setT(self.getBossDamage() * self.bossDamageToMovie)
        return Task.cont

    def __makeBossDamageMovie(self):
        startPos = Point3(ToontownGlobals.SellbotBossBattleTwoPosHpr[0], ToontownGlobals.SellbotBossBattleTwoPosHpr[1], ToontownGlobals.SellbotBossBattleTwoPosHpr[2])
        startHpr = Point3(*ToontownGlobals.SellbotBossBattleThreeHpr)
        bottomPos = Point3(*ToontownGlobals.SellbotBossBottomPos)
        deathPos = Point3(*ToontownGlobals.SellbotBossDeathPos)
        self.setPosHpr(startPos, startHpr)
        bossTrack = Sequence()
        bossTrack.append(Func(self.loop, 'Fb_neutral'))
        track, hpr = self.rollBossToPoint(startPos, startHpr, bottomPos, None, 1)
        bossTrack.append(track)
        track, hpr = self.rollBossToPoint(bottomPos, startHpr, deathPos, None, 1)
        bossTrack.append(track)
        duration = bossTrack.getDuration()
        return bossTrack

    def prepareBossForBattle(self) -> None:
        self.cleanupIntervals()
        self.clearChat()
        self.reparentTo(render)
        self.happy = 0
        self.raised = 1
        self.forward = 1
        self.doAnimate()
        self.accept('pieSplat', self.__pieSplat)
        self.accept('localPieSplat', self.__localPieSplat)
        self.stickBossToFloor()
        self.bossDamageMovie = self.__makeBossDamageMovie()
        self.bossDamageToMovie = self.bossDamageMovie.getDuration() / self.bossMaxDamage
        self.bossDamageMovie.setT(self.bossDamage * self.bossDamageToMovie)
        self.bossHealthBar.initialize(self.bossMaxDamage - self.bossDamage, self.bossMaxDamage)

    def cleanupBossBattle(self):
        self.cleanupIntervals()
        self.stopAnimate()
        self.cleanupAttacks()
        self.setDizzy(0)
        self.removeHealthBar()

        self.ignore('pieSplat')
        self.ignore('localPieSplat')

        taskMgr.remove(self.uniqueName('StandUp'))
        self.bossDamageMovie.finish()
        self.bossDamageMovie = None
        self.unstickBoss()
        taskMgr.remove('RecoverBossDamage')

    def doorACallback(self, isOpen):
        if self.insidesANodePath:
            if isOpen:
                self.insidesANodePath.unstash()
            else:
                self.insidesANodePath.stash()

    def doorBCallback(self, isOpen):
        if self.insidesBNodePath:
            if isOpen:
                self.insidesBNodePath.unstash()
            else:
                self.insidesBNodePath.stash()

    def __pieSplat(self, toon, pieCode):
        if pieCode == ToontownGlobals.PieCodeBossInsides:
            if toon == localAvatar:
                self.d_hitBossInsides()
            self.flashRed()
        elif pieCode == ToontownGlobals.PieCodeBossCog:
            if toon == localAvatar:
                self.d_hitBoss(1)
            if self.dizzy:
                self.flashRed()
                self.doAnimate('hit', now=1)

    def __localPieSplat(self, pieCode, entry):
        if pieCode != ToontownGlobals.PieCodeToon:
            return
        avatarDoId = entry.getIntoNodePath().getNetTag('avatarDoId')
        if avatarDoId == '':
            self.notify.warning('Toon %s has no avatarDoId tag.' % repr(entry.getIntoNodePath()))
            return
        doId = int(avatarDoId)
        if doId != localAvatar.doId:
            self.d_hitToon(doId)

    def cleanupAttacks(self):
        self.__cleanupStrafe()

    def __cleanupStrafe(self):
        if self.strafeInterval:
            self.strafeInterval.finish()
            self.strafeInterval = None
        return

    def doStrafe(self, side, direction):
        gearRoot = self.rotateNode.attachNewNode('gearRoot')
        if side == 0:
            gearRoot.setPos(0, -7, 3)
            gearRoot.setHpr(180, 0, 0)
            door = self.doorA
        else:
            gearRoot.setPos(0, 7, 3)
            door = self.doorB
        gearRoot.setTag('attackCode', str(ToontownGlobals.BossCogStrafeAttack))
        gearModel = self.getGearFrisbee()
        gearModel.setScale(0.1)
        t = self.getBossDamage() / self.bossMaxDamage
        gearTrack = Parallel()
        numGears = int(4 + 6 * t + 0.5)
        time = 5.0 - 4.0 * t
        spread = 60 * math.pi / 180.0
        if direction == 1:
            spread = -spread
        dist = 50
        rate = time / numGears
        for i in range(numGears):
            node = gearRoot.attachNewNode(str(i))
            node.hide()
            node.setPos(0, 0, 0)
            gear = gearModel.instanceTo(node)
            angle = (float(i) / (numGears - 1) - 0.5) * spread
            x = dist * math.sin(angle)
            y = dist * math.cos(angle)
            h = random.uniform(-720, 720)
            gearTrack.append(Sequence(Wait(i * rate), Func(node.show), Parallel(node.posInterval(1, Point3(x, y, 0), fluid=1), node.hprInterval(1, VBase3(h, 0, 0), fluid=1), Sequence(SoundInterval(self.strafeSfx[i], volume=0.2, node=self), duration=0)), Func(node.detachNode)))

        seq = Sequence(Func(door.request, 'open'), Wait(0.7), gearTrack, Func(door.request, 'close'))
        self.__cleanupStrafe()
        self.strafeInterval = seq
        seq.start()
