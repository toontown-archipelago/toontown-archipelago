import random

from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import globalClockDelta
from direct.interval.IntervalGlobal import Sequence, Wait, Func, Parallel, ActorInterval, ParallelEndTogether, \
    SoundInterval
from direct.showbase import PythonUtil
from direct.showbase.MessengerGlobal import messenger
from direct.task import Task
from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import VBase3, CollisionNode, CollisionSphere, CollisionTube, NodePath, Vec3, \
    Vec2, Point3, BitMask32, CollisionHandlerEvent, TextureStage, VBase4, BoundingSphere, decomposeMatrix, CSDefault, \
    headsUp, Mat3

from libotp import CFSpeech
from toontown.coghq import SeltzerLeagueGlobals
from toontown.distributed import DelayDelete
from toontown.effects import DustCloud
from toontown.suit import Suit
from toontown.suit import SuitDNA
from toontown.suit.DistributedBossCogStripped import DistributedBossCogStripped
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals

TTL = TTLocalizer


class DistributedBossbotBossStripped(DistributedBossCogStripped):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBossbotBoss')
    BallLaunchOffset = Point3(10.5, 8.5, -5)

    def __init__(self, cr):
        self.notify.debug('----- __init___')
        DistributedBossCogStripped.__init__(self, cr)
        self.ruleset = SeltzerLeagueGlobals.CEORuleset()
        self.bossDamage = 0
        self.bossMaxDamage = self.ruleset.CEO_MAX_HP
        self.moveTrack = None
        self.speedDamage = 0
        self.maxSpeedDamage = ToontownGlobals.BossbotMaxSpeedDamage
        self.speedRecoverRate = 0
        self.speedRecoverStartTime = 0
        self.ballLaunch = None
        self.moveTrack = None
        self.lastZapLocalTime = 0
        self.numAttacks = 0
        return

    def announceGenerate(self):
        DistributedBossCogStripped.announceGenerate(self)
        render.setTag('pieCode', str(ToontownGlobals.PieCodeNotBossCog))
        self.setTag('attackCode', str(ToontownGlobals.BossCogGolfAttack))
        target = CollisionTube(0, -2, -2, 0, -1, 9, 4.0)
        targetNode = CollisionNode('BossZap')
        targetNode.addSolid(target)
        targetNode.setCollideMask(ToontownGlobals.PieBitmask)
        self.targetNodePath = self.pelvis.attachNewNode(targetNode)
        self.targetNodePath.setTag('pieCode', str(ToontownGlobals.PieCodeBossCog))
        self.axle.getParent().setTag('pieCode', str(ToontownGlobals.PieCodeBossCog))
        disk = loader.loadModel('phase_9/models/char/bossCog-gearCollide')
        disk.find('**/+CollisionNode').setName('BossZap')
        disk.reparentTo(self.pelvis)
        disk.setZ(0.8)
        closeBubble = CollisionSphere(0, 0, 0, 10)
        closeBubble.setTangible(0)
        closeBubbleNode = CollisionNode('CloseBoss')
        closeBubbleNode.setIntoCollideMask(BitMask32(0))
        closeBubbleNode.setFromCollideMask(ToontownGlobals.BanquetTableBitmask)
        closeBubbleNode.addSolid(closeBubble)
        self.closeBubbleNode = closeBubbleNode
        self.closeHandler = CollisionHandlerEvent()
        self.closeHandler.addInPattern('closeEnter')
        self.closeHandler.addOutPattern('closeExit')
        self.closeBubbleNodePath = self.attachNewNode(closeBubbleNode)
        (base.cTrav.addCollider(self.closeBubbleNodePath, self.closeHandler),)
        self.accept('closeEnter', self.closeEnter)
        self.accept('closeExit', self.closeExit)
        self.treads = self.find('**/treads')
        demotedCeo = Suit.Suit()
        demotedCeo.dna = SuitDNA.SuitDNA()
        demotedCeo.dna.newSuit('f')
        demotedCeo.setDNA(demotedCeo.dna)
        demotedCeo.reparentTo(render)
        demotedCeo.loop('neutral')
        demotedCeo.stash()
        self.demotedCeo = demotedCeo
        self.bossClub = loader.loadModel('phase_12/models/char/bossbotBoss-golfclub')
        overtimeOneClubSequence = Sequence(self.bossClub.colorScaleInterval(0.1, colorScale=VBase4(0, 1, 0, 1)),
                                           self.bossClub.colorScaleInterval(0.3, colorScale=VBase4(1, 1, 1, 1)))
        overtimeTwoClubSequence = Sequence(self.bossClub.colorScaleInterval(0.1, colorScale=VBase4(1, 0, 0, 1)),
                                           self.bossClub.colorScaleInterval(0.3, colorScale=VBase4(1, 1, 1, 1)))
        self.bossClubIntervals = [overtimeOneClubSequence, overtimeTwoClubSequence]
        self.rightHandJoint = self.find('**/joint17')
        self.setPosHpr(*ToontownGlobals.BossbotBossBattleOnePosHpr)
        self.reparentTo(render)
        self.toonUpSfx = loader.loadSfx('phase_11/audio/sfx/LB_toonup.ogg')
        self.warningSfx = loader.loadSfx('phase_5/audio/sfx/Skel_COG_VO_grunt.ogg')
        self.swingClubSfx = loader.loadSfx('phase_5/audio/sfx/SA_hardball.ogg')
        self.explodeSfx = loader.loadSfx('phase_4/audio/sfx/firework_distance_02.ogg')
        self.moveBossTaskName = 'CEOMoveTask'

    def disable(self):
        self.notify.debug('----- disable')
        DistributedBossCogStripped.disable(self)
        self.demotedCeo.delete()
        base.cTrav.removeCollider(self.closeBubbleNodePath)
        taskMgr.remove('RecoverSpeedDamage')
        self.interruptMove()
        for ival in self.bossClubIntervals:
            ival.finish()

        self.removeAllTasks()

    def cleanupIntervals(self):
        super().cleanupIntervals()
        for table in list(self.game.tables.values()):
            table.cleanupIntervals()

    def prepareBossForBattle(self):
        self.cleanupIntervals()
        self.clearChat()
        self.reparentTo(render)
        self.happy = 1
        self.raised = 1
        self.forward = 1
        self.doAnimate()
        self.stickBossToFloor()
        self.bossHealthBar.initialize(self.bossMaxDamage - self.bossDamage, self.bossMaxDamage)
        self.bossHealthBar.update(self.bossMaxDamage, self.bossMaxDamage)
        # For whatever reason, an update was needed here in order for the bar to show as soon as the round starts.
        # Without, the health bar would show as soon as he took damage.
        self.bossClub.reparentTo(self.rightHandJoint)
        self.generateHealthBar()
        self.updateHealthBar()

    def cleanupBossBattle(self):
        self.cleanupIntervals()

    def d_hitBoss(self, bossDamage):
        self.sendUpdate('hitBoss', [bossDamage])

    def d_ballHitBoss(self, bossDamage):
        self.sendUpdate('ballHitBoss', [bossDamage])

    def setBossDamage(self, bossDamage, recoverRate, recoverStartTime):
        if bossDamage > self.bossDamage:
            delta = bossDamage - self.bossDamage
            self.flashRed()
            self.showHpText(-delta, scale=5)
        self.bossDamage = bossDamage
        self.updateHealthBar()
        self.bossHealthBar.update(self.bossMaxDamage - bossDamage, self.bossMaxDamage)

    def makeVictoryMovie(self):
        self.show()
        dustCloud = DustCloud.DustCloud(fBillboard=0, wantSound=1)
        dustCloud.reparentTo(self)
        dustCloud.setPos(0, -10, 3)
        dustCloud.setScale(4)
        dustCloud.wrtReparentTo(render)
        dustCloud.createTrack(12)
        newHpr = self.getHpr()
        newHpr.setX(newHpr.getX() + 180)
        bossTrack = Sequence(
            Func(self.show),
            Func(camera.reparentTo, self),
            Func(camera.setPos, Point3(0, -35, 25)),
            Func(camera.setHpr, Point3(0, -20, 0)),
            Func(self.setChatAbsolute, TTL.BossbotRewardSpeech1, CFSpeech),
            Wait(3.0),
            Func(self.setChatAbsolute, TTL.BossbotRewardSpeech2, CFSpeech),
            Wait(2.0),
            Func(self.clearChat),
            Parallel(
                Sequence(
                    Wait(0.5),
                    Func(self.demotedCeo.setPos, self.getPos()),
                    Func(self.demotedCeo.setHpr, newHpr),
                    Func(self.hide),
                    Wait(0.5),
                    Func(self.demotedCeo.reparentTo, render),
                    Func(self.demotedCeo.unstash)),
                Sequence(dustCloud.track)),
            Wait(2.0),
            Func(dustCloud.destroy))
        return bossTrack

    def doDirectedAttack(self, avId, attackCode):
        toon = base.cr.doId2do.get(avId)
        if toon:
            distance = toon.getDistance(self)
            gearRoot = self.rotateNode.attachNewNode('gearRoot-atk%d' % self.numAttacks)
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
                nodeName = '%s-%s' % (str(i), globalClock.getFrameTime())
                node = gearRoot.attachNewNode(nodeName)
                node.hide()
                node.setPos(0, 5.85, 4.0)
                gear = gearModel.instanceTo(node)
                x = random.uniform(-5, 5)
                z = random.uniform(-3, 3)
                h = random.uniform(-720, 720)
                if i == 2:
                    x = 0
                    z = 0

                def detachNode(node):
                    if not node.isEmpty():
                        node.detachNode()
                    return Task.done

                def detachNodeLater(node=node):
                    if node.isEmpty():
                        return
                    center = node.node().getBounds().getCenter()
                    node.node().setBounds(BoundingSphere(center, distance * 1.5))
                    node.node().setFinal(1)
                    self.doMethodLater(0.005, detachNode, 'detach-%s-%s' % (gearRoot.getName(), node.getName()),
                                       extraArgs=[node])

                gearTrack.append(Sequence(Wait(i * 0.15), Func(node.show),
                                          Parallel(node.posInterval(1, Point3(x, distance, z), fluid=1),
                                                   node.hprInterval(1, VBase3(h, 0, 0), fluid=1)),
                                          Func(detachNodeLater)))

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

            def detachGearRoot(task, gearRoot=gearRoot):
                if not gearRoot.isEmpty():
                    gearRoot.detachNode()
                return task.done

            def detachGearRootLater(gearRoot=gearRoot):
                if gearRoot.isEmpty():
                    return
                self.doMethodLater(0.01, detachGearRoot, 'detach-%s' % gearRoot.getName())

            seq = Sequence(ParallelEndTogether(self.pelvis.hprInterval(1, VBase3(toToonH, 0, 0)), neutral1Anim),
                           extraAnim, Parallel(Sequence(Wait(0.19), gearTrack, Func(detachGearRootLater),
                                                        self.pelvis.hprInterval(0.2, VBase3(0, 0, 0))),
                                               Sequence(throwAnim, neutral2Anim)))
            self.doAnimate(seq, now=1, raised=1)

    def setBattleDifficulty(self, diff):
        self.notify.debug('battleDifficulty = %d' % diff)
        self.battleDifficulty = diff

    def doMoveAttack(self, tableIndex):
        self.tableIndex = tableIndex
        table = self.game.tables[tableIndex]
        fromPos = self.getPos()
        fromHpr = self.getHpr()
        toPos = table.getPos()
        foo = render.attachNewNode('foo')
        foo.setPos(self.getPos())
        foo.setHpr(self.getHpr())
        foo.lookAt(table.getLocator())
        toHpr = foo.getHpr()
        toHpr.setX(toHpr.getX() - 180)
        foo.removeNode()
        reverse = False
        moveTrack, hpr = self.moveBossToPoint(fromPos, fromHpr, toPos, toHpr, reverse)
        self.moveTrack = moveTrack
        self.moveTrack.start()
        self.storeInterval(self.moveTrack, 'moveTrack')

    def interruptMove(self):
        if self.moveTrack and self.moveTrack.isPlaying():
            self.moveTrack.pause()
        self.stopMoveTask()

    def setAttackCode(self, attackCode, avId=0):
        self.numAttacks += 1
        self.notify.debug('numAttacks=%d' % self.numAttacks)
        self.attackCode = attackCode
        self.attackAvId = avId
        if attackCode == ToontownGlobals.BossCogMoveAttack:
            self.interruptMove()
            self.doMoveAttack(avId)
        elif attackCode == ToontownGlobals.BossCogGolfAttack:
            self.interruptMove()
            self.cleanupAttacks()
            self.doGolfAttack(avId, attackCode)
        elif attackCode == ToontownGlobals.BossCogDizzy:
            self.interruptMove()
            self.setDizzy(1)
            self.cleanupAttacks()
            self.doAnimate(None, raised=0, happy=1)
        elif attackCode == ToontownGlobals.BossCogDizzyNow:
            self.interruptMove()
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
        elif attackCode == ToontownGlobals.BossCogDirectedAttack or attackCode == ToontownGlobals.BossCogSlowDirectedAttack or attackCode == ToontownGlobals.BossCogGearDirectedAttack:
            self.interruptMove()
            self.setDizzy(0)
            self.doDirectedAttack(avId, attackCode)
        elif attackCode == ToontownGlobals.BossCogGolfAreaAttack:
            self.interruptMove()
            self.setDizzy(0)
            self.doGolfAreaAttack()
        elif attackCode == ToontownGlobals.BossCogNoAttack:
            self.setDizzy(0)
            self.doAnimate(None, raised=1)
        elif attackCode == ToontownGlobals.BossCogOvertimeAttack:
            self.interruptMove()
            self.setDizzy(0)
            self.cleanupAttacks()
            self.doOvertimeAttack(avId)
        return

    def signalAtTable(self):
        self.sendUpdate('reachedTable', [self.tableIndex])

    def closeEnter(self, colEntry):
        tableStr = colEntry.getIntoNodePath().getNetTag('tableIndex')
        if tableStr:
            tableIndex = int(tableStr)
            self.sendUpdate('hitTable', [tableIndex])

    def closeExit(self, colEntry):
        tableStr = colEntry.getIntoNodePath().getNetTag('tableIndex')
        if tableStr:
            tableIndex = int(tableStr)
            if self.tableIndex != tableIndex:
                self.sendUpdate('awayFromTable', [tableIndex])

    def setSpeedDamage(self, speedDamage, recoverRate, timestamp):
        recoverStartTime = globalClockDelta.networkToLocalTime(timestamp)
        self.speedDamage = speedDamage
        self.speedRecoverRate = recoverRate
        self.speedRecoverStartTime = recoverStartTime
        speedFraction = max(1 - speedDamage / self.maxSpeedDamage, 0)
        self.treads.setColorScale(1, speedFraction, speedFraction, 1)
        taskName = 'RecoverSpeedDamage'
        taskMgr.remove(taskName)
        if self.speedRecoverRate:
            taskMgr.add(self.__recoverSpeedDamage, taskName)

    def getSpeedDamage(self):
        now = globalClock.getFrameTime()
        elapsed = now - self.speedRecoverStartTime
        return max(self.speedDamage - self.speedRecoverRate * elapsed / 60.0, 0)

    def getFractionalSpeedDamage(self):
        result = self.getSpeedDamage() / self.maxSpeedDamage
        return result

    def __recoverSpeedDamage(self, task):
        speedDamage = self.getSpeedDamage()
        speedFraction = max(1 - speedDamage / self.maxSpeedDamage, 0)
        self.treads.setColorScale(1, speedFraction, speedFraction, 1)
        return task.cont

    def moveBossToPoint(self, fromPos, fromHpr, toPos, toHpr, reverse):
        vector = Vec3(toPos - fromPos)
        distance = vector.length()
        self.distanceToTravel = distance
        self.notify.debug('self.distanceToTravel = %s' % self.distanceToTravel)
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
        turnTime = abs(toHpr[0] - fromHpr[0]) / self.getCurTurnSpeed()
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
        self.toPos = toPos
        self.fromPos = fromPos
        self.dirVector = self.toPos - self.fromPos
        self.dirVector.normalize()
        track = Sequence(Func(self.setPos, fromPos), Func(self.headsUp, toPos),
                         Parallel(self.hprInterval(turnTime, toHpr, fromHpr), self.rollLeftTreads(turnTime, leftRate),
                                  self.rollRightTreads(turnTime, -leftRate)), Func(self.startMoveTask))
        return (track, toHpr)

    def getCurTurnSpeed(self):
        result = ToontownGlobals.BossbotTurnSpeedMax - (
                    ToontownGlobals.BossbotTurnSpeedMax - ToontownGlobals.BossbotTurnSpeedMin) * self.getFractionalSpeedDamage()
        return result

    def getCurRollSpeed(self):
        result = ToontownGlobals.BossbotRollSpeedMax - (
                    ToontownGlobals.BossbotRollSpeedMax - ToontownGlobals.BossbotRollSpeedMin) * self.getFractionalSpeedDamage()
        return result

    def getCurTreadSpeed(self):
        result = ToontownGlobals.BossbotTreadSpeedMax - (
                    ToontownGlobals.BossbotTreadSpeedMax - ToontownGlobals.BossbotTreadSpeedMin) * self.getFractionalSpeedDamage()
        return result

    def startMoveTask(self):
        taskMgr.add(self.moveBossTask, self.moveBossTaskName)

    def stopMoveTask(self):
        taskMgr.remove(self.moveBossTaskName)

    def moveBossTask(self, task):
        dt = globalClock.getDt()
        distanceTravelledThisFrame = dt * self.getCurRollSpeed()
        diff = self.toPos - self.getPos()
        distanceLeft = diff.length()

        def rollTexMatrix(t, object=object):
            object.setTexOffset(TextureStage.getDefault(), t, 0)

        self.treadsLeftPos += dt * self.getCurTreadSpeed()
        self.treadsRightPos += dt * self.getCurTreadSpeed()
        rollTexMatrix(self.treadsLeftPos, self.treadsLeft)
        rollTexMatrix(self.treadsRightPos, self.treadsRight)
        if distanceTravelledThisFrame >= distanceLeft:
            self.setPos(self.toPos)
            self.signalAtTable()
            return Task.done
        else:
            newPos = self.getPos() + self.dirVector * dt * self.getCurRollSpeed()
            self.setPos(newPos)
            return Task.cont

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
            if self.isToonRoaming(toon.doId):
                toonTrack += [ActorInterval(toon, 'slip-backward')]
                toonTrack += [toon.posInterval(0.5, getSlideToPos, fluid=1)]
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
        zapTrack.delayDelete = DelayDelete.DelayDelete(toon, 'BossbotBoss.doZapToon')
        zapTrack.start(startTime)
        self.storeInterval(zapTrack, zapName)
        return

    def zapLocalToon(self, attackCode, origin=None):

        # Don't hurt us if the boss is dizzy and we got hit by a golf ball flying at mach 10 (sequence finishing)
        if hasattr(self, 'attackCode') and self.attackCode in ToontownGlobals.BossCogDizzyStates and attackCode in (
        ToontownGlobals.BossCogGolfAttack, ToontownGlobals.BossCogGolfAreaAttack):
            return

        if self.localToonIsSafe or localAvatar.ghostMode or localAvatar.isStunned:
            return
        if globalClock.getFrameTime() < self.lastZapLocalTime + 1.0:
            return
        self.lastZapLocalTime = globalClock.getFrameTime()
        self.notify.debug('zapLocalToon frameTime=%s' % globalClock.getFrameTime())
        messenger.send('interrupt-pie')
        self.notify.debug('continuing zap')
        toon = localAvatar
        fling = 1
        shake = 0
        if attackCode == ToontownGlobals.BossCogAreaAttack:
            fling = 0
            shake = 1
        if fling:
            if origin == None:
                origin = self
            if self.isToonRoaming(toon.doId):
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
                                    hpr[0],
                                    hpr[1],
                                    hpr[2],
                                    bp2d[0],
                                    bp2d[1],
                                    attackCode,
                                    timestamp])
        toon.stunToon()
        self.doZapToon(toon, fling=fling, shake=shake)
        return

    def getToonTableIndex(self, toonId):
        tableIndex = -1
        for table in list(self.game.tables.values()):
            if table.avId == toonId:
                tableIndex = table.index
                break

        return tableIndex

    def getToonGolfSpotIndex(self, toonId):
        golfSpotIndex = -1
        for golfSpot in list(self.game.golfSpots.values()):
            if golfSpot.avId == toonId:
                golfSpotIndex = golfSpot.index
                break

        return golfSpotIndex

    def isToonOnTable(self, toonId):
        result = self.getToonTableIndex(toonId) != -1
        return result

    def isToonOnGolfSpot(self, toonId):
        result = self.getToonGolfSpotIndex(toonId) != -1
        return result

    def isToonRoaming(self, toonId):
        result = not self.isToonOnTable(toonId) and not self.isToonOnGolfSpot(toonId)
        return result

    def getGolfBall(self):
        golfRoot = NodePath('golfRoot')
        golfBall = loader.loadModel('phase_6/models/golf/golf_ball')
        golfBall.setColorScale(0.75, 0.75, 0.75, 0.5)
        golfBall.setTransparency(1)
        ballScale = 5
        golfBall.setScale(ballScale)
        golfBall.reparentTo(golfRoot)
        cs = CollisionSphere(0, 0, 0, ballScale * 0.25)
        cs.setTangible(0)
        cn = CollisionNode('BossZap')
        cn.addSolid(cs)
        cn.setIntoCollideMask(ToontownGlobals.WallBitmask)
        cnp = golfRoot.attachNewNode(cn)
        return golfRoot

    def doGolfAttack(self, avId, attackCode):
        toon = base.cr.doId2do.get(avId)
        if toon:
            distance = toon.getDistance(self)
            self.notify.debug('distance = %s' % distance)
            gearRoot = self.rotateNode.attachNewNode('gearRoot-atk%d' % self.numAttacks)
            gearRoot.setZ(10)
            gearRoot.setTag('attackCode', str(attackCode))
            gearModel = self.getGolfBall()
            self.ballLaunch = NodePath('')
            self.ballLaunch.reparentTo(gearRoot)
            self.ballLaunch.setPos(self.BallLaunchOffset)
            gearRoot.headsUp(toon)
            toToonH = PythonUtil.fitDestAngle2Src(0, gearRoot.getH() + 180)
            gearRoot.lookAt(toon)
            neutral = 'Fb_neutral'
            if not self.twoFaced:
                neutral = 'Ff_neutral'
            gearTrack = Parallel()
            for i in range(5):
                nodeName = '%s-%s' % (str(i), globalClock.getFrameTime())
                node = gearRoot.attachNewNode(nodeName)
                node.hide()
                node.reparentTo(self.ballLaunch)
                node.wrtReparentTo(gearRoot)
                distance = toon.getDistance(node)
                gear = gearModel.instanceTo(node)
                x = random.uniform(-5, 5)
                z = random.uniform(-3, 3)
                p = random.uniform(-720, -90)
                y = distance + random.uniform(5, 15)
                if i == 2:
                    x = 0
                    z = 0
                    y = distance + 10

                def detachNode(node):
                    if not node.isEmpty():
                        node.detachNode()
                    return Task.done

                def detachNodeLater(node=node):
                    if node.isEmpty():
                        return
                    node.node().setBounds(BoundingSphere(Point3(0, 0, 0), distance * 1.5))
                    node.node().setFinal(1)
                    self.doMethodLater(0.005, detachNode, 'detach-%s-%s' % (gearRoot.getName(), node.getName()),
                                       extraArgs=[node])

                gearTrack.append(Sequence(Wait(26.0 / 24.0), Wait(i * 0.15), Func(node.show),
                                          Parallel(node.posInterval(1, Point3(x, y, z), fluid=1),
                                                   node.hprInterval(1, VBase3(0, p, 0), fluid=1)),
                                          Func(detachNodeLater)))

            if not self.raised:
                neutral1Anim = self.getAnim('down2Up')
                self.raised = 1
            else:
                neutral1Anim = ActorInterval(self, neutral, startFrame=48)
            throwAnim = self.getAnim('golf_swing')
            neutral2Anim = ActorInterval(self, neutral)
            extraAnim = Sequence()
            if attackCode == ToontownGlobals.BossCogSlowDirectedAttack:
                extraAnim = ActorInterval(self, neutral)

            def detachGearRoot(task, gearRoot=gearRoot):
                if not gearRoot.isEmpty():
                    gearRoot.detachNode()
                return task.done

            def detachGearRootLater(gearRoot=gearRoot):
                self.doMethodLater(0.01, detachGearRoot, 'detach-%s' % gearRoot.getName())

            seq = Sequence(ParallelEndTogether(self.pelvis.hprInterval(1, VBase3(toToonH, 0, 0)), neutral1Anim),
                           extraAnim, Parallel(Sequence(Wait(0.19), gearTrack, Func(detachGearRootLater),
                                                        self.pelvis.hprInterval(0.2, VBase3(0, 0, 0))),
                                               Sequence(throwAnim, neutral2Anim), Sequence(Wait(0.85), SoundInterval(
                        self.swingClubSfx, node=self, duration=0.45, cutOff=300, listenerNode=base.localAvatar))))
            self.doAnimate(seq, now=1, raised=1)

    def doGolfAreaAttack(self):
        toons = []
        for toonId in self.game.avIdList:
            toon = base.cr.doId2do.get(toonId)
            if toon and toon.getHp() > 0:
                toons.append(toon)

        if not toons:
            return
        neutral = 'Fb_neutral'
        if not self.twoFaced:
            neutral = 'Ff_neutral'
        if not self.raised:
            neutral1Anim = self.getAnim('down2Up')
            self.raised = 1
        else:
            neutral1Anim = ActorInterval(self, neutral, startFrame=48)
        throwAnim = self.getAnim('golf_swing')
        neutral2Anim = ActorInterval(self, neutral)
        extraAnim = Sequence()
        gearModel = self.getGolfBall()
        toToonH = self.rotateNode.getH() + 360
        self.notify.debug('toToonH = %s' % toToonH)
        gearRoots = []
        allGearTracks = Parallel()
        for toon in toons:
            gearRoot = self.rotateNode.attachNewNode('gearRoot-atk%d-%d' % (self.numAttacks, toons.index(toon)))
            gearRoot.setZ(10)
            gearRoot.setTag('attackCode', str(ToontownGlobals.BossCogGolfAreaAttack))
            gearRoot.lookAt(toon)
            ballLaunch = NodePath('')
            ballLaunch.reparentTo(gearRoot)
            ballLaunch.setPos(self.BallLaunchOffset)
            gearTrack = Parallel()
            for i in range(5):
                nodeName = '%s-%s' % (str(i), globalClock.getFrameTime())
                node = gearRoot.attachNewNode(nodeName)
                node.hide()
                node.reparentTo(ballLaunch)
                node.wrtReparentTo(gearRoot)
                distance = toon.getDistance(node)
                toonPos = toon.getPos(render)
                nodePos = node.getPos(render)
                vector = toonPos - nodePos
                gear = gearModel.instanceTo(node)
                x = random.uniform(-5, 5)
                z = random.uniform(-3, 3)
                p = random.uniform(-720, -90)
                y = distance + random.uniform(5, 15)
                if i == 2:
                    x = 0
                    z = 0
                    y = distance + 10

                def detachNode(node):
                    if not node.isEmpty():
                        node.detachNode()
                    return Task.done

                def detachNodeLater(node=node):
                    if node.isEmpty():
                        return
                    node.node().setBounds(BoundingSphere(Point3(0, 0, 0), distance * 1.5))
                    node.node().setFinal(1)
                    self.doMethodLater(0.005, detachNode, 'detach-%s-%s' % (gearRoot.getName(), node.getName()),
                                       extraArgs=[node])

                gearTrack.append(Sequence(Wait(26.0 / 24.0), Wait(i * 0.15), Func(node.show),
                                          Parallel(node.posInterval(1, Point3(x, y, z), fluid=1),
                                                   node.hprInterval(1, VBase3(0, p, 0), fluid=1)),
                                          Func(detachNodeLater)))

            allGearTracks.append(gearTrack)

        def detachGearRoots(gearRoots=gearRoots):
            for gearRoot in gearRoots:

                def detachGearRoot(task, gearRoot=gearRoot):
                    if not gearRoot.isEmpty():
                        gearRoot.detachNode()
                    return task.done

                if gearRoot.isEmpty():
                    continue
                self.doMethodLater(0.01, detachGearRoot, 'detach-%s' % gearRoot.getName())

            gearRoots = []

        rotateFire = Parallel(self.pelvis.hprInterval(2, VBase3(toToonH + 1440, 0, 0)), allGearTracks)
        seq = Sequence(Func(base.playSfx, self.warningSfx), Func(self.saySomething, TTLocalizer.GolfAreaAttackTaunt),
                       ParallelEndTogether(self.pelvis.hprInterval(2, VBase3(toToonH, 0, 0)), neutral1Anim), extraAnim,
                       Parallel(Sequence(rotateFire, Func(detachGearRoots), Func(self.pelvis.setHpr, VBase3(0, 0, 0))),
                                Sequence(throwAnim, neutral2Anim), Sequence(Wait(0.85),
                                                                            SoundInterval(self.swingClubSfx, node=self,
                                                                                          duration=0.45, cutOff=300,
                                                                                          listenerNode=base.localAvatar))))
        self.doAnimate(seq, now=1, raised=1)

    def saySomething(self, chatString):
        intervalName = 'CEOTaunt'
        seq = Sequence(name=intervalName)
        seq.append(Func(self.setChatAbsolute, chatString, CFSpeech))
        seq.append(Wait(4.0))
        seq.append(Func(self.clearChat))
        oldSeq = self.activeIntervals.get(intervalName)
        if oldSeq:
            oldSeq.finish()
        seq.start()
        self.activeIntervals[intervalName] = seq

    def d_hitToon(self, toonId):
        self.notify.debug('----- d_hitToon')
        self.sendUpdate('hitToon', [toonId])

    def toonGotHealed(self, toonId):
        toon = base.cr.doId2do.get(toonId)
        if toon:
            base.playSfx(self.toonUpSfx, node=toon)

    def toonGotToonup(self, avId, beltIndex, toonupIndex, toonupNum):
        if self.game.belts[beltIndex]:
            self.game.belts[beltIndex].removeToonup(toonupIndex)
        toon = base.cr.doId2do.get(avId)
        if toon:
            base.playSfx(self.toonUpSfx, node=toon)

    def doOvertimeAttack(self, index):
        attackCode = ToontownGlobals.BossCogOvertimeAttack
        attackBelts = Sequence()
        if index < len(self.game.belts):
            belt = self.game.belts[index]
            self.saySomething(TTLocalizer.OvertimeAttackTaunts[index])
            if index:
                self.bossClubIntervals[0].finish()
                self.bossClubIntervals[1].loop()
            else:
                self.bossClubIntervals[1].finish()
                self.bossClubIntervals[0].loop()
            distance = belt.beltModel.getDistance(self)
            gearRoot = self.rotateNode.attachNewNode('gearRoot')
            gearRoot.setZ(10)
            gearRoot.setTag('attackCode', str(attackCode))
            gearModel = self.getGearFrisbee()
            gearModel.setScale(0.2)
            gearRoot.headsUp(belt.beltModel)
            toToonH = PythonUtil.fitDestAngle2Src(0, gearRoot.getH() + 180)
            gearRoot.lookAt(belt.beltModel)
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
                                          Parallel(node.posInterval(1, Point3(x, distance, z), fluid=1),
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
                           extraAnim, Parallel(
                    Sequence(Wait(0.19), gearTrack, Func(gearRoot.detachNode), Func(self.explodeSfx.play),
                             self.pelvis.hprInterval(0.2, VBase3(0, 0, 0))), Sequence(throwAnim, neutral2Anim)),
                           Func(belt.request, 'Inactive'))
            attackBelts.append(seq)
        self.notify.debug('attackBelts duration= %.2f' % attackBelts.getDuration())
        self.doAnimate(attackBelts, now=1, raised=1)
