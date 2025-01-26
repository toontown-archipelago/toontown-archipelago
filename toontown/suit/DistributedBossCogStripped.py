import json
import random

from direct.controls.ControlManager import CollisionHandlerRayStart
from direct.distributed.ClockDelta import *
from direct.gui.OnscreenText import OnscreenText
from direct.interval.IntervalGlobal import *
from direct.showbase import PythonUtil
from direct.showbase.MessengerGlobal import messenger
from panda3d.core import *

from otp.avatar import DistributedAvatar
from toontown.battle import BattleBase
from toontown.building import ElevatorConstants
from toontown.coghq import BossHealthBar
from toontown.coghq import CogDisguiseGlobals
from toontown.distributed import DelayDelete
from toontown.effects import DustCloud
from toontown.toonbase import ToontownGlobals
from . import BossCog
from . import SuitDNA


class DistributedBossCogStripped(DistributedAvatar.DistributedAvatar, BossCog.BossCog):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBossCog')
    allowClickedNameTag = True

    def __init__(self, cr):
        DistributedAvatar.DistributedAvatar.__init__(self, cr)
        BossCog.BossCog.__init__(self)
        self.gotAllToons = 0
        self.bossDamage = 0
        self.toonsA = []
        self.toonsB = []
        self.involvedToons = []
        self.toonRequest = None
        self.battleNumber = 0
        self.arenaSide = 0
        self.toonSphere = None
        self.localToonIsSafe = 0
        self.__toonsStuckToFloor = []
        self.cqueue = None
        self.rays = None
        self.ray1 = None
        self.ray2 = None
        self.ray3 = None
        self.e1 = None
        self.e2 = None
        self.e3 = None
        self.activeIntervals = {}
        self.flashInterval = None
        self.elevatorType = ElevatorConstants.ELEVATOR_VP
        self.cutsceneSpeed = 1.0
        fileSystem = VirtualFileSystem.getGlobalPtr()
        self.musicJson = json.loads(fileSystem.readFile(ToontownGlobals.musicJsonFilePath, True))

    def announceGenerate(self):
        DistributedAvatar.DistributedAvatar.announceGenerate(self)
        self.bossHealthBar = BossHealthBar.BossHealthBar(self.style.dept)
        self.prevCogSuitLevel = localAvatar.getCogLevels()[CogDisguiseGlobals.dept2deptIndex(self.style.dept)]
        nearBubble = CollisionSphere(0, 0, 0, 50)
        nearBubble.setTangible(0)
        nearBubbleNode = CollisionNode('NearBoss')
        nearBubbleNode.setCollideMask(ToontownGlobals.WallBitmask)
        nearBubbleNode.addSolid(nearBubble)
        self.attachNewNode(nearBubbleNode)
        self.accept('enterNearBoss', self.avatarNearEnter)
        self.accept('exitNearBoss', self.avatarNearExit)
        self.collNode.removeSolid(0)

        # function to create and add collision solids to the collision node
        self.createCollisionSolids()
        self.collNodePath.reparentTo(self.axle)
        self.collNode.setCollideMask(
            ToontownGlobals.PieBitmask | ToontownGlobals.WallBitmask | ToontownGlobals.CameraBitmask)
        self.collNode.setName('BossZap')
        self.setTag('attackCode', str(ToontownGlobals.BossCogElectricFence))
        self.accept('enterBossZap', self.__touchedBoss)
        bubbleL = CollisionSphere(10, -5, 0, 10)
        bubbleL.setTangible(0)
        bubbleLNode = CollisionNode('BossZap')
        bubbleLNode.setCollideMask(ToontownGlobals.WallBitmask)
        bubbleLNode.addSolid(bubbleL)
        self.bubbleL = self.axle.attachNewNode(bubbleLNode)
        self.bubbleL.setTag('attackCode', str(ToontownGlobals.BossCogSwatLeft))
        self.bubbleL.stash()
        bubbleR = CollisionSphere(-10, -5, 0, 10)
        bubbleR.setTangible(0)
        bubbleRNode = CollisionNode('BossZap')
        bubbleRNode.setCollideMask(ToontownGlobals.WallBitmask)
        bubbleRNode.addSolid(bubbleR)
        self.bubbleR = self.axle.attachNewNode(bubbleRNode)
        self.bubbleR.setTag('attackCode', str(ToontownGlobals.BossCogSwatRight))
        self.bubbleR.stash()
        bubbleF = CollisionSphere(0, -25, 0, 12)
        bubbleF.setTangible(0)
        bubbleFNode = CollisionNode('BossZap')
        bubbleFNode.setCollideMask(ToontownGlobals.WallBitmask)
        bubbleFNode.addSolid(bubbleF)
        self.bubbleF = self.rotateNode.attachNewNode(bubbleFNode)
        self.bubbleF.setTag('attackCode', str(ToontownGlobals.BossCogFrontAttack))
        self.bubbleF.stash()

    def createCollisionSolids(self):
        """
        Create the collision solids for the boss cog.
        Then add the solids to the collision node.
        This allows overriding for the specific collision solids
        """
        tube1 = CollisionTube(6.5, -7.5, 2, 6.5, 7.5, 2, 2.5)
        tube2 = CollisionTube(-6.5, -7.5, 2, -6.5, 7.5, 2, 2.5)
        roof = CollisionPolygon(Point3(-4.4, 7.1, 5.5), Point3(-4.4, -7.1, 5.5), Point3(4.4, -7.1, 5.5),
                                Point3(4.4, 7.1, 5.5))
        side1 = CollisionPolygon(Point3(-4.4, -7.1, 5.5), Point3(-4.4, 7.1, 5.5), Point3(-4.4, 7.1, 0),
                                 Point3(-4.4, -7.1, 0))
        side2 = CollisionPolygon(Point3(4.4, 7.1, 5.5), Point3(4.4, -7.1, 5.5), Point3(4.4, -7.1, 0),
                                 Point3(4.4, 7.1, 0))
        front1 = CollisionPolygon(Point3(4.4, -7.1, 5.5), Point3(-4.4, -7.1, 5.5), Point3(-4.4, -7.1, 5.2),
                                  Point3(4.4, -7.1, 5.2))
        back1 = CollisionPolygon(Point3(-4.4, 7.1, 5.5), Point3(4.4, 7.1, 5.5), Point3(4.4, 7.1, 5.2),
                                 Point3(-4.4, 7.1, 5.2))
        self.collNode.addSolid(tube1)
        self.collNode.addSolid(tube2)
        self.collNode.addSolid(roof)
        self.collNode.addSolid(side1)
        self.collNode.addSolid(side2)
        self.collNode.addSolid(front1)
        self.collNode.addSolid(back1)

    def disable(self):
        DistributedAvatar.DistributedAvatar.disable(self)
        self.cr.relatedObjectMgr.abortRequest(self.toonRequest)
        self.toonRequest = None
        self.stopAnimate()
        self.cleanupIntervals()
        self.cleanupFlash()
        self.disableLocalToonSimpleCollisions()
        self.ignoreAll()
        self.bossHealthBar.cleanup()
        return

    def delete(self):
        try:
            self.DistributedBossCog_deleted
        except:
            self.DistributedBossCog_deleted = 1
            self.ignoreAll()
            DistributedAvatar.DistributedAvatar.delete(self)
            BossCog.BossCog.delete(self)
            localAvatar.inventory.setDefaultBattleCreditMultiplier()

    def setDNAString(self, dnaString):
        BossCog.BossCog.setDNAString(self, dnaString)

    def getDNAString(self):
        return self.dna.makeNetString()

    def setDNA(self, dna):
        BossCog.BossCog.setDNA(self, dna)

    def getDialogueArray(self, *args):
        return BossCog.BossCog.getDialogueArray(self, *args)

    def storeInterval(self, interval, name):
        if name in self.activeIntervals:
            ival = self.activeIntervals[name]
            if hasattr(ival, 'delayDelete') or hasattr(ival, 'delayDeletes'):
                self.clearInterval(name, finish=1)
        self.activeIntervals[name] = interval

    def cleanupIntervals(self):
        # Copy the current intervals into a local list
        intervals = list(self.activeIntervals.values())

        # Iterate over that list
        for interval in intervals:
            interval.finish()
            DelayDelete.cleanupDelayDeletes(interval)

        # Clear the dictionary once you’re done
        self.activeIntervals.clear()

    def clearInterval(self, name, finish=1):
        if name in self.activeIntervals:
            ival = self.activeIntervals[name]
            if finish:
                ival.finish()
            else:
                ival.pause()
            if name in self.activeIntervals:
                DelayDelete.cleanupDelayDeletes(ival)
                del self.activeIntervals[name]
        else:
            self.notify.debug('interval: %s already cleared' % name)

    def finishInterval(self, name):
        if name in self.activeIntervals:
            interval = self.activeIntervals[name]
            interval.finish()

    def d_avatarEnter(self):
        self.sendUpdate('avatarEnter', [])

    def d_avatarExit(self):
        self.sendUpdate('avatarExit', [])

    def avatarNearEnter(self, entry):
        self.sendUpdate('avatarNearEnter', [])

    def avatarNearExit(self, entry):
        self.sendUpdate('avatarNearExit', [])

    def hasLocalToon(self):
        doId = localAvatar.doId
        return doId in self.toonsA or doId in self.toonsB

    def setArenaSide(self, arenaSide):
        self.arenaSide = arenaSide

    def makeEndOfBattleMovie(self, hasLocalToon):
        return Sequence()

    def makeLocalToonSafe(self):
        """
        Puts our local toon in a state where they are safe from taking damage so they can freely watch.
        """
        self.localToonIsSafe = True

    def makeLocalToonUnsafe(self):
        """
        Ensures our local toon can take damage and interact with the fight.
        """
        self.localToonIsSafe = False

    def enableLocalToonSimpleCollisions(self):
        if not self.toonSphere:
            sphere = CollisionSphere(0, 0, 1, 1)
            sphere.setRespectEffectiveNormal(0)
            sphereNode = CollisionNode('SimpleCollisions')
            sphereNode.setFromCollideMask(ToontownGlobals.WallBitmask | ToontownGlobals.FloorBitmask)
            sphereNode.setIntoCollideMask(BitMask32.allOff())
            sphereNode.addSolid(sphere)
            self.toonSphere = NodePath(sphereNode)
            self.toonSphereHandler = CollisionHandlerPusher()
            self.toonSphereHandler.addCollider(self.toonSphere, localAvatar)
        self.toonSphere.reparentTo(localAvatar)
        base.cTrav.addCollider(self.toonSphere, self.toonSphereHandler)

    def disableLocalToonSimpleCollisions(self):
        if self.toonSphere:
            base.cTrav.removeCollider(self.toonSphere)
            self.toonSphere.detachNode()

    def stickToonsToFloor(self):
        self.unstickToons()
        rayNode = CollisionNode('stickToonsToFloor')
        rayNode.addSolid(CollisionRay(0.0, 0.0, CollisionHandlerRayStart, 0.0, 0.0, -1.0))
        rayNode.setFromCollideMask(ToontownGlobals.FloorBitmask)
        rayNode.setIntoCollideMask(BitMask32.allOff())
        ray = NodePath(rayNode)
        lifter = CollisionHandlerFloor()
        lifter.setOffset(ToontownGlobals.FloorOffset)
        lifter.setReach(10.0)
        for toonId in self.involvedToons:
            toon = base.cr.doId2do.get(toonId)
            if toon:
                toonRay = ray.instanceTo(toon)
                lifter.addCollider(toonRay, toon)
                base.cTrav.addCollider(toonRay, lifter)
                self.__toonsStuckToFloor.append(toonRay)

    def unstickToons(self):
        for toonRay in self.__toonsStuckToFloor:
            base.cTrav.removeCollider(toonRay)
            toonRay.removeNode()

        self.__toonsStuckToFloor = []

    def stickBossToFloor(self):
        self.unstickBoss()
        self.ray1 = CollisionRay(0.0, 10.0, 20.0, 0.0, 0.0, -1.0)
        self.ray2 = CollisionRay(0.0, 0.0, 20.0, 0.0, 0.0, -1.0)
        self.ray3 = CollisionRay(0.0, -10.0, 20.0, 0.0, 0.0, -1.0)
        rayNode = CollisionNode('stickBossToFloor')
        rayNode.addSolid(self.ray1)
        rayNode.addSolid(self.ray2)
        rayNode.addSolid(self.ray3)
        rayNode.setFromCollideMask(ToontownGlobals.FloorBitmask)
        rayNode.setIntoCollideMask(BitMask32.allOff())
        self.rays = self.attachNewNode(rayNode)
        self.cqueue = CollisionHandlerQueue()
        base.cTrav.addCollider(self.rays, self.cqueue)

    def rollBoss(self, t, fromPos, deltaPos):
        self.setPos(fromPos + deltaPos * t)
        if not self.cqueue:
            return
        self.cqueue.sortEntries()
        numEntries = self.cqueue.getNumEntries()
        if numEntries != 0:
            for i in range(self.cqueue.getNumEntries() - 1, -1, -1):
                entry = self.cqueue.getEntry(i)
                solid = entry.getFrom()
                if solid == self.ray1:
                    self.e1 = entry
                elif solid == self.ray2:
                    self.e2 = entry
                elif solid == self.ray3:
                    self.e3 = entry
                else:
                    self.notify.warning('Unexpected ray in __liftBoss')
                    return

            self.cqueue.clearEntries()
        if not (self.e1 and self.e2 and self.e3):
            self.notify.debug('Some points missed in __liftBoss')
            return
        p1 = self.e1.getSurfacePoint(self)
        p2 = self.e2.getSurfacePoint(self)
        p3 = self.e3.getSurfacePoint(self)
        p2a = (p1 + p3) / 2
        if p2a[2] > p2[2]:
            center = p2a
        else:
            center = p2
        self.setZ(self, center[2])
        if p1[2] > p2[2] + 0.01 or p3[2] > p2[2] + 0.01:
            mat = Mat4(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
            if abs(p3[2] - center[2]) < abs(p1[2] - center[2]):
                lookAt(mat, Vec3(p1 - center), CSDefault)
            else:
                lookAt(mat, Vec3(center - p3), CSDefault)
            self.rotateNode.setMat(mat)
        else:
            self.rotateNode.clearTransform()

    def unstickBoss(self):
        if self.rays:
            base.cTrav.removeCollider(self.rays)
            self.rays.removeNode()
        self.rays = None
        self.ray1 = None
        self.ray2 = None
        self.ray3 = None
        self.e1 = None
        self.e2 = None
        self.e3 = None
        self.rotateNode.clearTransform()
        self.cqueue = None
        return

    def rollBossToPoint(self, fromPos, fromHpr, toPos, toHpr, reverse):
        vector = Vec3(toPos - fromPos)
        distance = vector.length()
        if toHpr == None:
            mat = Mat3(0, 0, 0, 0, 0, 0, 0, 0, 0)
            headsUp(mat, vector, CSDefault)
            scale = VBase3(0, 0, 0)
            shear = VBase3(0, 0, 0)
            toHpr = VBase3(0, 0, 0)
            decomposeMatrix(mat, scale, shear, toHpr, CSDefault)
        if fromHpr:
            newH = PythonUtil.fitDestAngle2Src(fromHpr[0], toHpr[0])
            toHpr = VBase3(newH, 0, 0)
        else:
            fromHpr = toHpr
        turnTime = abs(toHpr[0] - fromHpr[0]) / ToontownGlobals.BossCogTurnSpeed
        if toHpr[0] < fromHpr[0]:
            leftRate = ToontownGlobals.BossCogTreadSpeed
        else:
            leftRate = -ToontownGlobals.BossCogTreadSpeed
        if reverse:
            rollTreadRate = -ToontownGlobals.BossCogTreadSpeed
        else:
            rollTreadRate = ToontownGlobals.BossCogTreadSpeed
        rollTime = distance / ToontownGlobals.BossCogRollSpeed
        deltaPos = toPos - fromPos
        track = Sequence(Func(self.setPos, fromPos), Func(self.headsUp, toPos),
                         Parallel(self.hprInterval(turnTime, toHpr, fromHpr), self.rollLeftTreads(turnTime, leftRate),
                                  self.rollRightTreads(turnTime, -leftRate)),
                         Parallel(LerpFunctionInterval(self.rollBoss, duration=rollTime, extraArgs=[fromPos, deltaPos]),
                                  self.rollLeftTreads(rollTime, rollTreadRate),
                                  self.rollRightTreads(rollTime, rollTreadRate)))
        return (track, toHpr)

    def putToonInCogSuit(self, toon):
        if not toon.isDisguised:
            deptIndex = SuitDNA.suitDepts.index(self.style.dept)
            toon.setCogIndex(deptIndex)
        toon.getGeomNode().hide()

    def placeToonInElevator(self, toon):
        self.putToonInCogSuit(toon)
        toonIndex = self.involvedToons.index(toon.doId)
        toon.reparentTo(self.elevatorModel)
        toon.setPos(*ElevatorConstants.BigElevatorPoints[toonIndex])
        toon.setHpr(180, 0, 0)
        toon.suit.loop('neutral')

    def toonNormalEyes(self, toons, bArrayOfObjs=False):
        if bArrayOfObjs:
            toonObjs = toons
        else:
            toonObjs = []
            for toonId in toons:
                toon = base.cr.doId2do.get(toonId)
                if toon:
                    toonObjs.append(toon)

        seq = Sequence()
        for toon in toonObjs:
            seq.append(Func(toon.normalEyes))
            seq.append(Func(toon.blinkEyes))

        return seq

    def displayDefeatText(self):
        title = OnscreenText(parent=aspect2d, text='Defeat!', style=3, fg=(.8, .2, .2, 1),
                             align=TextNode.ACenter, scale=.15, pos=(0, .35))
        sub = OnscreenText(parent=aspect2d, text='Everyone is being sent to the playground!', style=3,
                           fg=(.8, .8, .8, 1),
                           align=TextNode.ACenter, scale=.09, pos=(0, .2))

        Parallel(
            Sequence(
                LerpColorScaleInterval(title, .25, colorScale=(1, 1, 1, 1), startColorScale=(1, 1, 1, 0),
                                       blendType='easeInOut'),
                Wait(3.75),
                LerpColorScaleInterval(title, 1.25, colorScale=(1, 1, 1, 0), startColorScale=(1, 1, 1, 1),
                                       blendType='easeInOut'),
                Func(lambda: title.cleanup())
            ),
            Sequence(
                LerpColorScaleInterval(sub, .25, colorScale=(1, 1, 1, 1), startColorScale=(1, 1, 1, 0),
                                       blendType='easeInOut'),
                Wait(3.75),
                LerpColorScaleInterval(sub, 1.25, colorScale=(1, 1, 1, 0), startColorScale=(1, 1, 1, 1),
                                       blendType='easeInOut'),
                Func(lambda: sub.cleanup())
            ),
        ).start()

    def __touchedBoss(self, entry):
        self.notify.debug('%s' % entry)
        self.notify.debug('fromPos = %s' % entry.getFromNodePath().getPos(render))
        self.notify.debug('intoPos = %s' % entry.getIntoNodePath().getPos(render))
        attackCodeStr = entry.getIntoNodePath().getNetTag('attackCode')
        if attackCodeStr == '':
            self.notify.warning('Node %s has no attackCode tag.' % repr(entry.getIntoNodePath()))
            return
        attackCode = int(attackCodeStr)
        if attackCode == ToontownGlobals.BossCogLawyerAttack and self.dna.dept != 'l':
            self.notify.warning('got lawyer attack but not in CJ boss battle')
            return
        self.zapLocalToon(attackCode)

    def zapLocalToon(self, attackCode, origin=None):
        if self.localToonIsSafe or localAvatar.ghostMode or localAvatar.isStunned:
            return
        if (attackCode in ToontownGlobals.NonBossCogAttacks):
            pass
        elif (self.attackCode in ToontownGlobals.BossCogDizzyStates):
            return
        messenger.send('interrupt-pie')
        toon = localAvatar
        fling = 1
        shake = 0
        if attackCode == ToontownGlobals.BossCogAreaAttack:
            fling = 0
            shake = 1
        if fling:
            if origin == None:
                origin = self
            camera.wrtReparentTo(render)
            toon.headsUp(origin)
            camera.wrtReparentTo(toon)
        bossRelativePos = toon.getPos(self.getGeomNode())
        bp2d = Vec2(bossRelativePos[0], bossRelativePos[1])
        bp2d.normalize()
        pos = toon.getPos()
        hpr = toon.getHpr()
        timestamp = globalClockDelta.getFrameNetworkTime()
        self.sendUpdate('zapToon', [pos[0],
                                    pos[1],
                                    pos[2],
                                    hpr[0] % 360.0,
                                    hpr[1],
                                    hpr[2],
                                    bp2d[0],
                                    bp2d[1],
                                    attackCode,
                                    timestamp])
        toon.stunToon()
        self.doZapToon(toon, fling=fling, shake=shake)
        return

    def showZapToon(self, toonId, x, y, z, h, p, r, attackCode, timestamp):
        if toonId == localAvatar.doId:
            return
        ts = globalClockDelta.localElapsedTime(timestamp)
        pos = Point3(x, y, z)
        hpr = VBase3(h, p, r)
        fling = 1
        toon = self.cr.doId2do.get(toonId)
        if toon:
            if attackCode == ToontownGlobals.BossCogAreaAttack:
                pos = None
                hpr = None
                fling = 0
            else:
                ts -= toon.smoother.getDelay()
            self.doZapToon(toon, pos=pos, hpr=hpr, ts=ts, fling=fling)
        return

    def doZapToon(self, toon, pos=None, hpr=None, ts=0, fling=1, shake=1):
        zapName = toon.uniqueName('zap')
        self.clearInterval(zapName)
        zapTrack = Sequence(name=zapName)
        if toon == localAvatar:
            messenger.send("LocalSetOuchMode")
            messenger.send('interrupt-pie')
            self.enableLocalToonSimpleCollisions()
        else:
            zapTrack.append(Func(toon.stopSmooth))

        def getSlideToPos(toon=toon):
            return render.getRelativePoint(toon, Point3(0, -5, 0))

        if pos != None and hpr != None:
            (zapTrack.append(Func(toon.setPosHpr, pos, hpr)),)
        toonTrack = Parallel()
        if shake and toon == localAvatar:
            toonTrack.append(
                Sequence(Func(camera.setZ, camera, 1), Wait(0.15), Func(camera.setZ, camera, -2), Wait(0.15),
                         Func(camera.setZ, camera, 1)))
        if fling:
            toonTrack += [ActorInterval(toon, 'slip-backward'), toon.posInterval(0.5, getSlideToPos, fluid=1)]
        else:
            toonTrack += [ActorInterval(toon, 'slip-forward')]
        zapTrack.append(toonTrack)
        if toon == localAvatar:
            zapTrack.append(Func(self.disableLocalToonSimpleCollisions))
            zapTrack.append(Func(messenger.send, "LocalSetFinalBattleMode"))
        else:
            zapTrack.append(Func(toon.startSmooth))
        if ts > 0:
            startTime = ts
        else:
            zapTrack = Sequence(Wait(-ts), zapTrack)
            startTime = 0
        zapTrack.append(Func(self.clearInterval, zapName))
        zapTrack.delayDelete = DelayDelete.DelayDelete(toon, 'BossCog.doZapToon')
        zapTrack.start(startTime)
        self.storeInterval(zapTrack, zapName)
        return

    def setAttackCode(self, attackCode, avId=0):
        self.attackCode = attackCode
        self.attackAvId = avId
        if attackCode == ToontownGlobals.BossCogDizzy:
            self.setDizzy(1)
            self.cleanupAttacks()
            self.doAnimate(None, raised=0, happy=1)
        elif attackCode == ToontownGlobals.BossCogDizzyNow:
            self.setDizzy(1)
            self.cleanupAttacks()
            self.doAnimate('hit', happy=1, now=1)
        elif attackCode == ToontownGlobals.BossCogSwatLeft:
            self.setDizzy(0)
            self.doAnimate('ltSwing', now=1)
        elif attackCode == ToontownGlobals.BossCogSwatRight:
            self.setDizzy(0)
            self.doAnimate('rtSwing', now=1)
        elif attackCode == ToontownGlobals.BossCogAreaAttack:
            self.setDizzy(0)
            self.doAnimate('areaAttack', now=1)
        elif attackCode == ToontownGlobals.BossCogFrontAttack:
            self.setDizzy(0)
            self.doAnimate('frontAttack', now=1)
        elif attackCode == ToontownGlobals.BossCogRecoverDizzyAttack:
            self.setDizzy(0)
            self.doAnimate('frontAttack', now=1)
        elif attackCode == ToontownGlobals.BossCogDirectedAttack or attackCode == ToontownGlobals.BossCogSlowDirectedAttack:
            self.setDizzy(0)
            self.doDirectedAttack(avId, attackCode)
        elif attackCode == ToontownGlobals.BossCogNoAttack:
            self.setDizzy(0)
            self.doAnimate(None, raised=1)
        return

    def cleanupAttacks(self):
        pass

    def cleanupFlash(self):
        if self.flashInterval:
            self.flashInterval.finish()
            self.flashInterval = None
        return

    def flashRed(self):
        self.cleanupFlash()
        self.setColorScale(1, 1, 1, 1)
        i = Sequence(self.colorScaleInterval(0.1, colorScale=VBase4(1, 0, 0, 1)),
                     self.colorScaleInterval(0.3, colorScale=VBase4(1, 1, 1, 1)))
        self.flashInterval = i
        i.start()

    def flashGreen(self):
        self.cleanupFlash()
        if not self.isEmpty():
            self.setColorScale(1, 1, 1, 1)
            i = Sequence(self.colorScaleInterval(0.1, colorScale=VBase4(0, 1, 0, 1)),
                         self.colorScaleInterval(0.3, colorScale=VBase4(1, 1, 1, 1)))
            self.flashInterval = i
            i.start()

    def getGearFrisbee(self):
        return loader.loadModel('phase_9/models/char/gearProp')

    def backupToonsToBattlePosition(self, toonIds, battleNode):
        self.notify.debug('backupToonsToBattlePosition:')
        ival = Parallel()
        points = BattleBase.BattleBase.toonPoints[len(toonIds) - 1]
        for i in range(len(toonIds)):
            toon = base.cr.doId2do.get(toonIds[i])
            if toon:
                pos, h = points[i]
                pos = render.getRelativePoint(battleNode, pos)
                ival.append(
                    Sequence(Func(toon.setPlayRate, -0.8, 'walk'), Func(toon.loop, 'walk'), toon.posInterval(3, pos),
                             Func(toon.setPlayRate, 1, 'walk'), Func(toon.loop, 'neutral')))

        return ival

    def loseCogSuits(self, toons, battleNode, camLoc, arrayOfObjs=False):
        seq = Sequence()
        if not toons:
            return seq
        self.notify.debug('battleNode=%s camLoc=%s' % (battleNode, camLoc))
        seq.append(Func(camera.setPosHpr, battleNode, *camLoc))
        suitsOff = Parallel()
        if arrayOfObjs:
            toonArray = toons
        else:
            toonArray = []
            for toonId in toons:
                toon = base.cr.doId2do.get(toonId)
                if toon:
                    toonArray.append(toon)

        for toon in toonArray:
            dustCloud = DustCloud.DustCloud()
            dustCloud.setPos(0, 2, 3)
            dustCloud.setScale(0.5)
            dustCloud.setDepthWrite(0)
            dustCloud.setBin('fixed', 0)
            dustCloud.createTrack()
            suitsOff.append(Sequence(Func(dustCloud.reparentTo, toon), Parallel(dustCloud.track, Sequence(Wait(0.3),
                                                                                                          Func(
                                                                                                              toon.takeOffSuit),
                                                                                                          Func(
                                                                                                              toon.sadEyes),
                                                                                                          Func(
                                                                                                              toon.blinkEyes),
                                                                                                          Func(
                                                                                                              toon.play,
                                                                                                              'slip-backward'),
                                                                                                          Wait(0.7))),
                                     Func(dustCloud.detachNode), Func(dustCloud.destroy)))

        seq.append(suitsOff)
        return seq

    def doDirectedAttack(self, avId, attackCode):
        toon = base.cr.doId2do.get(avId)
        if toon:
            gearRoot = self.rotateNode.attachNewNode('gearRoot')
            gearRoot.setZ(10)
            gearRoot.setTag('attackCode', str(attackCode))
            gearModel = self.getGearFrisbee()
            gearModel.setScale(0.2)
            gearRoot.headsUp(toon)
            toToonH = PythonUtil.fitDestAngle2Src(0, gearRoot.getH() + 180)
            gearRoot.lookAt(toon)
            neutral = 'Fb_neutral'
            if not self.twoFaced:
                neutral = 'Ff_neutral'
            gearTrack = Parallel()
            for i in range(4):
                node = gearRoot.attachNewNode(str(i))
                node.hide()
                node.setPos(0, 5.85, 4.0)
                gear = gearModel.instanceTo(node)
                x = random.uniform(-5, 5)
                z = random.uniform(-3, 3)
                h = random.uniform(-720, 720)
                gearTrack.append(Sequence(Wait(i * 0.15), Func(node.show),
                                          Parallel(node.posInterval(1, Point3(x, 50, z), fluid=1),
                                                   node.hprInterval(1, VBase3(h, 0, 0), fluid=1)),
                                          Func(node.detachNode)))

            if not self.raised:
                neutral1Anim = self.getAnim('down2Up')
                self.raised = 1
            else:
                neutral1Anim = ActorInterval(self, neutral, startFrame=48)
            throwAnim = self.getAnim('throw')
            neutral2Anim = ActorInterval(self, neutral)
            extraAnim = Sequence()
            if attackCode == ToontownGlobals.BossCogSlowDirectedAttack:
                extraAnim = ActorInterval(self, neutral)
            seq = Sequence(ParallelEndTogether(self.pelvis.hprInterval(1, VBase3(toToonH, 0, 0)), neutral1Anim),
                           extraAnim, Parallel(Sequence(Wait(0.19), gearTrack, Func(gearRoot.detachNode),
                                                        self.pelvis.hprInterval(0.2, VBase3(0, 0, 0))),
                                               Sequence(throwAnim, neutral2Anim)))
            self.doAnimate(seq, now=1, raised=1)

    def announceAreaAttack(self):
        if not getattr(localAvatar.controlManager.currentControls, 'isAirborne', 0):
            self.zapLocalToon(ToontownGlobals.BossCogAreaAttack)

    def setToonsToNeutral(self, toonIds):
        for i in range(len(toonIds)):
            toon = base.cr.doId2do.get(toonIds[i])
            if toon:
                if toon.isDisguised:
                    toon.suit.loop('neutral')
                toon.loop('neutral')

    def wearCogSuits(self, toons, battleNode, camLoc, arrayOfObjs=False, waiter=False):
        seq = Sequence()
        if not toons:
            return seq
        self.notify.debug('battleNode=%s camLoc=%s' % (battleNode, camLoc))
        if camLoc:
            seq.append(Func(camera.setPosHpr, battleNode, *camLoc))
        suitsOff = Parallel()
        if arrayOfObjs:
            toonArray = toons
        else:
            toonArray = []
            for toonId in toons:
                toon = base.cr.doId2do.get(toonId)
                if toon:
                    toonArray.append(toon)

        for toon in toonArray:
            dustCloud = DustCloud.DustCloud()
            dustCloud.setPos(0, 2, 3)
            dustCloud.setScale(0.5)
            dustCloud.setDepthWrite(0)
            dustCloud.setBin('fixed', 0)
            dustCloud.createTrack()
            makeWaiter = Sequence()
            if waiter:
                makeWaiter = Func(toon.makeWaiter)
            suitsOff.append(Sequence(Func(dustCloud.reparentTo, toon), Parallel(dustCloud.track, Sequence(Wait(0.3),
                                                                                                          Func(
                                                                                                              self.putToonInCogSuit,
                                                                                                              toon),
                                                                                                          makeWaiter,
                                                                                                          Wait(0.7))),
                                     Func(dustCloud.detachNode)))

        seq.append(suitsOff)
        return seq
