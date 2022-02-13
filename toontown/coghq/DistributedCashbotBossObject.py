from panda3d.core import *
from panda3d.physics import *
from direct.interval.IntervalGlobal import *
from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedSmoothNode
from toontown.coghq import CraneLeagueGlobals
from toontown.toonbase import ToontownGlobals
from otp.otpbase import OTPGlobals
from direct.fsm import FSM
from direct.task import Task
smileyDoId = 1

class DistributedCashbotBossObject(DistributedSmoothNode.DistributedSmoothNode, FSM.FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedCashbotBossObject')
    wantsWatchDrift = 1

    def __init__(self, cr):
        DistributedSmoothNode.DistributedSmoothNode.__init__(self, cr)
        FSM.FSM.__init__(self, 'DistributedCashbotBossObject')
        self.boss = None
        self.avId = 0
        self.craneId = 0
        self.cleanedUp = 0
        self.collisionNode = CollisionNode('object')
        self.collisionNode.setIntoCollideMask(ToontownGlobals.PieBitmask | OTPGlobals.WallBitmask | ToontownGlobals.CashbotBossObjectBitmask | OTPGlobals.CameraBitmask)
        self.collisionNode.setFromCollideMask(ToontownGlobals.PieBitmask | OTPGlobals.FloorBitmask)
        self.collisionNodePath = NodePath(self.collisionNode)
        self.physicsActivated = 0
        self.toMagnetSoundInterval = Sequence()
        self.hitFloorSoundInterval = Sequence()
        self.hitBossSfx = loader.loadSfx('phase_5/audio/sfx/AA_drop_safe_miss.ogg')
        self.hitBossSoundInterval = SoundInterval(self.hitBossSfx)
        self.touchedBossSfx = loader.loadSfx('phase_5/audio/sfx/AA_drop_sandbag.ogg')
        self.touchedBossSoundInterval = SoundInterval(self.touchedBossSfx, duration=0.8)
        self.lerpInterval = None
        return

    def disable(self):
        self.cleanup()
        self.stopSmooth()
        DistributedSmoothNode.DistributedSmoothNode.disable(self)

    def cleanup(self):
        if self.cleanedUp:
            return
        else:
            self.cleanedUp = 1
        self.demand('Off')
        self.detachNode()
        self.toMagnetSoundInterval.finish()
        self.hitFloorSoundInterval.finish()
        self.hitBossSoundInterval.finish()
        self.touchedBossSoundInterval.finish()
        del self.toMagnetSoundInterval
        del self.hitFloorSoundInterval
        del self.hitBossSoundInterval
        del self.touchedBossSoundInterval
        self.boss = None
        return

    def setupPhysics(self, name):
        an = ActorNode('%s-%s' % (name, self.doId))
        anp = NodePath(an)
        if not self.isEmpty():
            self.reparentTo(anp)
        NodePath.assign(self, anp)
        self.physicsObject = an.getPhysicsObject()
        self.setTag('object', str(self.doId))
        self.collisionNodePath.reparentTo(self)
        self.handler = PhysicsCollisionHandler()
        self.handler.addCollider(self.collisionNodePath, self)
        self.collideName = self.uniqueName('collide')
        self.handler.addInPattern(self.collideName + '-%in')
        self.handler.addAgainPattern(self.collideName + '-%in')
        self.watchDriftName = self.uniqueName('watchDrift')

    def activatePhysics(self):
        if not self.physicsActivated:
            self.boss.physicsMgr.attachPhysicalNode(self.node())
            base.cTrav.addCollider(self.collisionNodePath, self.handler)
            self.physicsActivated = 1
            self.accept(self.collideName + '-floor', self.__hitFloor)
            self.accept(self.collideName + '-goon', self.__hitGoon)
            self.acceptOnce(self.collideName + '-headTarget', self.__hitBoss)
            self.accept(self.collideName + '-dropPlane', self.__hitDropPlane)

    def deactivatePhysics(self):
        if self.physicsActivated:
            self.boss.physicsMgr.removePhysicalNode(self.node())
            base.cTrav.removeCollider(self.collisionNodePath)
            self.physicsActivated = 0
            self.ignore(self.collideName + '-floor')
            self.ignore(self.collideName + '-goon')
            self.ignore(self.collideName + '-headTarget')
            self.ignore(self.collideName + '-dropPlane')

    def hideShadows(self):
        pass

    def showShadows(self):
        pass

    def stashCollisions(self):
        self.collisionNodePath.stash()

    def unstashCollisions(self):
        self.collisionNodePath.unstash()

    def __hitFloor(self, entry):
        if self.state == 'Dropped':
            self.d_hitFloor()
            self.demand('SlidingFloor', localAvatar.doId)

    def __hitGoon(self, entry):
        if self.state == 'Dropped':
            goonId = int(entry.getIntoNodePath().getNetTag('doId'))
            goon = self.cr.doId2do.get(goonId)
            if goon:
                self.doHitGoon(goon)

    def doHitGoon(self, goon):
        pass

    def __hitBoss(self, entry):
        if (self.state == 'Dropped') and self.craneId != self.boss.doId:
            vel = self.physicsObject.getVelocity()
            vel = self.crane.root.getRelativeVector(render, vel)
            vel.normalize()
            impact = vel[1]

            if impact >= self.getMinImpact():
                self.hitBossSoundInterval.start()
            else:
                self.touchedBossSoundInterval.start()

            impact = max(0, impact)

            self.doHitBoss(impact, self.craneId)

    def doHitBoss(self, impact, craneId):
        self.d_hitBoss(impact, craneId)

    def __hitDropPlane(self, entry):
        self.notify.info('%s fell out of the world.' % self.doId)
        self.fellOut()

    def fellOut(self):
        raise StandardError, 'fellOut unimplented'

    def getMinImpact(self):
        return 0

    def __watchDrift(self, task):
        v = self.physicsObject.getVelocity()
        if abs(v[0]) < 0.0001 and abs(v[1]) < 0.0001:
            self.d_requestFree()
            self.demand('Free')
        return Task.cont

    def prepareGrab(self):
        pass

    def prepareRelease(self):
        pass

    def setBossCogId(self, bossCogId):
        self.bossCogId = bossCogId
        self.boss = base.cr.doId2do[bossCogId]

    def setObjectState(self, state, avId, craneId):
        if state == 'G':
            if self.boss.doId == avId or base.localAvatar.doId != avId:
                self.demand('Grabbed', avId, craneId)
        elif state == 'D':
            if self.boss.doId == craneId or base.localAvatar.doId != avId:
                self.demand('Dropped', avId, craneId)
            pass
        elif state == 's':
            if self.state != 'SlidingFloor':
                self.demand('SlidingFloor', avId)
        elif state == 'F':
            self.demand('Free')
        else:
            self.notify.error('Invalid state from AI: %s' % state)
            
    def __getCraneAndObject(self, avId):
        if self.boss and self.boss.cranes != None:
            for crane in self.boss.cranes.values():
                if crane.avId == avId:
                    return (crane.doId, self.doId)

        return (0, 0)

    def d_requestGrab(self):
        self.sendUpdate('requestGrab')

    def rejectGrab(self):
        if self.state == 'Grabbed':
            self.demand('Dropped', self.avId, self.craneId)

    def d_requestDrop(self):
        self.sendUpdate('requestDrop')

    def d_hitFloor(self):
        self.sendUpdate('hitFloor')

    def d_requestFree(self):
        self.sendUpdate('requestFree', [self.getX(),
         self.getY(),
         self.getZ(),
         self.getH()])

    def d_hitBoss(self, impact, craneId):
        self.sendUpdate('hitBoss', [impact, craneId])

    def defaultFilter(self, request, args):
        if self.boss == None:
            raise FSM.RequestDenied, request
        return FSM.FSM.defaultFilter(self, request, args)

    def enterOff(self):
        self.detachNode()
        if self.lerpInterval:
            self.lerpInterval.finish()
            self.lerpInterval = None
        return

    def exitOff(self):
        self.reparentTo(render)

    def enterGrabbed(self, avId, craneId):
        self.crane = self.cr.doId2do.get(craneId)
        if self.oldState == 'LocalGrabbed':
            if craneId == self.craneId:
                return
            else:
                if self.crane:
                    self.crane.dropObject(self)
                self.prepareRelease()
        self.avId = avId
        self.craneId = craneId
        self.hideShadows()
        self.prepareGrab()
        if self.crane:
            self.crane.grabObject(self)

    def exitGrabbed(self):
        if self.crane:
            self.crane.dropObject(self)
        self.prepareRelease()
        self.showShadows()
        del self.crane

    def enterDropped(self, avId, craneId):
        self.avId = avId
        self.craneId = craneId
        self.crane = self.cr.doId2do.get(craneId)
        if self.avId == base.localAvatar.doId:
            self.activatePhysics()
            self.startPosHprBroadcast(period=.05)
            self.handler.setStaticFrictionCoef(0)
            self.handler.setDynamicFrictionCoef(0)
        else:
            self.startSmooth()
        self.hideShadows()

    def exitDropped(self):
        if self.avId == base.localAvatar.doId:
            if self.newState != 'SlidingFloor':
                self.deactivatePhysics()
                self.stopPosHprBroadcast()
        else:
            self.stopSmooth()
        del self.crane
        self.showShadows()

    def enterSlidingFloor(self, avId):
        self.avId = avId
        if self.lerpInterval:
            self.lerpInterval.finish()
            self.lerpInterval = None
        if self.avId == base.localAvatar.doId:
            self.activatePhysics()
            self.startPosHprBroadcast(period=.05)
            self.handler.setStaticFrictionCoef(0.9)
            self.handler.setDynamicFrictionCoef(0.5)
            if self.wantsWatchDrift:
                taskMgr.add(self.__watchDrift, self.watchDriftName)
        else:
            self.startSmooth()
        self.hitFloorSoundInterval.start()
        return

    def exitSlidingFloor(self):
        if self.avId == base.localAvatar.doId:
            taskMgr.remove(self.watchDriftName)
            self.deactivatePhysics()
            self.stopPosHprBroadcast()
        else:
            self.stopSmooth()

    def enterFree(self):
        self.avId = 0
        self.craneId = 0

    def exitFree(self):
        pass
