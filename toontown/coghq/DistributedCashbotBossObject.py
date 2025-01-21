from enum import IntEnum
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
from direct.task.TaskManagerGlobal import taskMgr
import math
import copy
smileyDoId = 1

class DummyTaskClass:
    def setDelay(self, blah):
        pass

DummyTask = DummyTaskClass()

class DistributedCashbotBossObject(DistributedSmoothNode.DistributedSmoothNode, FSM.FSM):

    """ This is an object that can be picked up an dropped in the
    final battle scene with the Cashbot CFO.  In particular, it's a
    safe or a goon.  """
    
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedCashbotBossObject')

    # This should be true for objects that will eventually transition
    # from SlidingFloor to Free when they stop moving.
    wantsWatchDrift = 1

    def __init__(self, cr):
        DistributedSmoothNode.DistributedSmoothNode.__init__(self, cr)
        FSM.FSM.__init__(self, 'DistributedCashbotBossObject')
        
        self.boss = None
        self.avId = 0
        self.craneId = 0
        self.cleanedUp = 0
        
        # An attribute to cache the last 7 speed for the object
        self.speeds = []
            
        # A CollisionNode to keep me out of walls and floors, and to
        # keep others from bumping into me.  We use PieBitmask instead
        # of WallBitmask, to protect against objects (like goons)
        # self-colliding.
        self.collisionNode = CollisionNode('object')
        self.collisionNode.setIntoCollideMask(ToontownGlobals.PieBitmask | OTPGlobals.WallBitmask | ToontownGlobals.CashbotBossObjectBitmask | OTPGlobals.CameraBitmask)
        self.collisionNode.setFromCollideMask(ToontownGlobals.PieBitmask | OTPGlobals.FloorBitmask)
        self.collisionNodePath = NodePath(self.collisionNode)
        
        self.physicsActivated = 0
        
        self.toMagnetSoundInterval = Sequence()
        self.hitFloorSoundInterval = Sequence()
        
        # A solid sound for when we get a good hit on the boss.
        self.hitBossSfx = loader.loadSfx('phase_5/audio/sfx/AA_drop_safe_miss.ogg')
        self.hitBossSoundInterval = SoundInterval(self.hitBossSfx)
        
        # A squishy sound for when we hit the boss, but not hard enough.
        self.touchedBossSfx = loader.loadSfx('phase_5/audio/sfx/AA_drop_sandbag.ogg')
        self.touchedBossSoundInterval = SoundInterval(self.touchedBossSfx, duration=0.8)
        
        # Cranes will fill in this with the interval to lerp the
        # object to the crane.
        self.lerpInterval = None
        
        self.setBroadcastStateChanges(True)
        self.accept(self.getStateChangeEvent(), self._doDebug)
        
        self.__broadcastPeriod = None
        self.broadcasting = False

    def _doDebug(self, _=None):
        pass

    def disable(self):
        self.cleanup()
        self.stopSmooth()
        DistributedSmoothNode.DistributedSmoothNode.disable(self)

    def cleanup(self):
        # is this being called twice?
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

        # It is important that there be no messenger hooks added on
        # this object at the time we reassign the NodePath.
        NodePath.assign(self, anp)
        
        self.physicsObject = an.getPhysicsObject()
        self.setTag('object', str(self.doId))
       
        self.collisionNodePath.reparentTo(self)
        self.handler = PhysicsCollisionHandler()
        self.handler.addCollider(self.collisionNodePath, self)

        # Set up a collision event so we know when the object hits the
        # floor, or the boss's target.
        self.collideName = self.uniqueName('collide')
        self.handler.addInPattern(self.collideName + '-%in')
        self.handler.addAgainPattern(self.collideName + '-%in')
        
        self.watchDriftName = self.uniqueName('watchDrift')
        self.startCacheName = self.uniqueName('startSpeedCaching')
        self.resetSpeedCaching()
        
    def startSpeedCaching(self, task):

        speed = self.physicsObject.getVelocity().length()

        if len(self.speeds) > 6:
            self.speeds.pop(0)
        
        self.speeds.append(speed)

        return Task.again
        
    def resetSpeedCaching(self):
        
        self.speeds = []
        taskMgr.remove(self.startCacheName)

    def activatePhysics(self):
        if not self.physicsActivated:
            self.speeds.append(self.physicsObject.getVelocity().length())
            taskMgr.doMethodLater(0.1, self.startSpeedCaching, self.startCacheName)
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
        if self.state == 'Dropped' or self.state == 'LocalDropped':
            self.d_hitFloor()
            self.demand('SlidingFloor', localAvatar.doId)

    def __hitGoon(self, entry):
        if self.state == 'Dropped' or self.state == 'LocalDropped':
            goonId = int(entry.getIntoNodePath().getNetTag('doId'))
            goon = self.cr.doId2do.get(goonId)
            if goon:
                self.doHitGoon(goon)

    def doHitGoon(self, goon):
        # Override in a derived class to do something if the object is
        # dropped on a goon.
        pass

    def __hitBoss(self, entry):
        if (self.state == 'Dropped' or self.state == 'LocalDropped') and self.craneId != self.boss.doId:
            
            #get the velocity of the object, relative to the crane
            speed = max(self.speeds)
            impact = min(1.0, max(pow(speed, 1.75)/466.475, 0.0))
            
            if impact >= self.getMinImpact():
                self.hitBossSoundInterval.start()
            else:
                self.touchedBossSoundInterval.start()

            self.doHitBoss(impact, self.craneId)
            self.resetSpeedCaching()

    def showTempHitEffect(self, impact, craneId):

        if not hasattr(self.boss.getBoss(), 'attackCode'):
            return

        if self.boss.getBoss().heldObject or self.boss.getBoss().attackCode != ToontownGlobals.BossCogDizzy:
            return
        
        timeUntilStunEnd = self.boss.getBoss().stunEndTime - globalClock.getFrameTime()
        if self.boss.getBoss().stunEndTime == 0 or timeUntilStunEnd < 1.5:
            return

        # Get the crane to check its damage multiplier 
        crane = self.cr.doId2do.get(craneId)
        if not crane:
            return

        damage = int(impact * 50)
        damage *= crane.getDamageMultiplier()
        damage *= self.boss.ruleset.SAFE_CFO_DAMAGE_MULTIPLIER
            
        damage = math.ceil(damage)

        if damage <= 0:
            return

        if self.boss.processingHp:
            curHp = self.boss.tempHp
        else:
            curHp = self.boss.ruleset.CFO_MAX_HP - self.boss.getBoss().bossDamage
        
        self.boss.tempHp = curHp - damage

        if damage < curHp:
            self.boss.getBoss().myHits.append(self.doId)
            self.boss.getBoss().processingHp = True
            self.boss.getBoss().flashRed()
            if self.boss.ruleset.CFO_FLINCHES_ON_HIT:
                self.boss.getBoss().doAnimate('hit', now=1)
            self.boss.getBoss().showHpText(-damage, scale=5)

    def doHitBoss(self, impact, craneId):
        # Derived classes can override this to do something specific
        # when we successfully hit the boss.
        self.d_hitBoss(impact, craneId)
        self.showTempHitEffect(impact, craneId)

    def __hitDropPlane(self, entry):
        self.notify.info('%s fell out of the world.' % self.doId)
        self.fellOut()

    def fellOut(self):
        # Override in a derived class to do the right thing when the
        # object falls out of the world.
        raise Exception('fellOut unimplented')

    def getMinImpact(self):
        # This method returns the minimum impact, in feet per second,
        # with which the object should hit the boss before we bother
        # to tell the server.
        return 0

    def __watchDrift(self, task):
        # Checks the object for non-zero velocity.  When the velocity
        # reaches zero in the XY plane, we tell the AI we're done
        # moving it around.
        v = self.physicsObject.getVelocity()
        
        if abs(v[0]) < 0.0001 and abs(v[1]) < 0.0001:
            self.d_requestFree()
            self.demand('Free')
            
        return Task.cont

    def prepareGrab(self):
        # Specialized classes will override this method to do
        # something appropriate when the object is grabbed by a
        # magnet.
        pass

    def prepareRelease(self):
        pass


        
    ##### Messages To/From The Server #####

    def setBossCogId(self, bossCogId):
        self.bossCogId = bossCogId

        # This would be risky if we had toons entering the zone during
        # a battle--but since all the toons are always there from the
        # beginning, we can be confident that the BossCog has already
        # been generated by the time we receive the generate for its
        # associated objects.
        self.boss = base.cr.doId2do[bossCogId]

    def setObjectState(self, state, avId, craneId):

        if self.state == 'Off':
            return

        if state == 'G':
            if self.state in ['SlidingFloor']:
                if avId == localAvatar.doId:
                    return
            if self.state != 'LocalDropped':
                self.demand('Grabbed', avId, craneId)
        elif state == 'D':
            if self.state in ['SlidingFloor']:
                if avId == localAvatar.doId:
                    return
            self.demand('Dropped', avId, craneId)
        elif state == 's':
            if self.state != 'SlidingFloor':
                self.demand('SlidingFloor', avId)
        elif state == 'F':
            if self.state in ['LocalGrabbed', 'LocalDropped']:
                return
            self.demand('Free')
        else:
            self.notify.error('Invalid state from AI: %s' % state)

    def d_requestGrab(self):
        self.sendUpdate('requestGrab')

    def rejectGrab(self):
        # The server tells us we can't have it for whatever reason.
        if self.state == 'LocalGrabbed':
            self.demand('LocalDropped', self.avId, self.craneId)

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
        # We overload the default filter function to disallow *any*
        # state transitions after the object has been disabled or
        # deleted, or before it has been fully generated.
        if self.boss == None:
            raise FSM.RequestDenied(request)
            
        return FSM.FSM.defaultFilter(self, request, args)



    ### FSM States ###

    def enterOff(self):
        # In state Off, the object is not parented to the scene graph.
        # In all other states, it is.
        self.detachNode()
        
        if self.lerpInterval:
            self.lerpInterval.finish()
            self.lerpInterval = None
        return

    def exitOff(self):
        self.reparentTo(render)

    def enterLocalGrabbed(self, avId, craneId):
        # This state is like Grabbed, except that it is only triggered
        # locally.  In this state, we have requested a grab, and we
        # will act as if we have grabbed the object successfully, but
        # we have not yet heard confirmation from the AI so we might
        # later discover that we didn't grab it after all.

        # We're not allowed to drop the object directly from this
        # state.
        self.avId = avId
        self.craneId = craneId

        self.crane = self.cr.doId2do.get(craneId)

        self.hideShadows()
        self.prepareGrab()

        # Add this to establish local control and
        # stop receiving incoming position updates
        # from other players:
        self.stopSmooth()
        self.localControl = True 
        self.crane.grabObject(self)

    def exitLocalGrabbed(self):
        if self.newState != 'Grabbed':
            if self.crane:
                self.crane.dropObject(self)
            self.prepareRelease()
            del self.crane

            self.showShadows()

    def enterGrabbed(self, avId, craneId):
        # Grabbed by a crane, or by the boss for a helmet.  craneId is
        # the doId of the crane or the doId of the boss himself.

        if avId != base.localAvatar.doId:
            self.localControl = False

        if self.oldState == 'LocalGrabbed':
            if craneId == self.craneId:
                # This is just the confirmation from the AI that we
                # did, in fact, grab this object with the expected
                # crane; we don't need to do anything else in this
                # state.
                return
            else:
                # Whoops, we had previously grabbed it locally, but it
                # turns out someone else grabbed it instead.
                self.crane.dropObject(self)
                self.prepareRelease()
        
        self.avId = avId
        self.craneId = craneId

        self.crane = self.cr.doId2do.get(craneId)

        # The "crane" might actually be the boss cog himself!  This
        # happens when the boss takes a safe to wear as a helmet.

        self.hideShadows()
        self.prepareGrab()
        self.crane.grabObject(self)

    def exitGrabbed(self):
        if hasattr(self, 'crane'):
            if self.crane:
                self.crane.dropObject(self)
        self.prepareRelease()
        self.showShadows()
        if hasattr(self, 'crane'):
            del self.crane

    def enterLocalDropped(self, avId, craneId):
        # As in LocalGrabbed, above, this state is entered locally
        # when we drop the safe, but we have not yet received
        # acknowledgement from the AI that we've dropped it.
        
        self.avId = avId
        self.craneId = craneId

        self.crane = self.cr.doId2do.get(craneId)
        
        self.activatePhysics()
        self.startPosHprBroadcast(avId=self.avId, period=.05)
        self.hideShadows()

        # Set slippery physics so it will slide off the boss.
        self.handler.setStaticFrictionCoef(0)
        self.handler.setDynamicFrictionCoef(0)

    def exitLocalDropped(self):
        if self.newState != 'SlidingFloor' and self.newState != 'Dropped':
            self.deactivatePhysics()
            self.stopPosHprBroadcast()
        del self.crane
        self.showShadows()

    def enterDropped(self, avId, craneId):
        
        self.avId = avId
        self.craneId = craneId

        self.crane = self.cr.doId2do.get(craneId)
        
        # If I'm the one who dropped it
        # Then I should be the one to broadcast
        # the position updates
        if self.avId == base.localAvatar.doId:
            self.activatePhysics()
            self.startPosHprBroadcast(avId=self.avId, period=.05)
            self.handler.setStaticFrictionCoef(0)
            self.handler.setDynamicFrictionCoef(0)
        # Otherwise, I'm the one receiving the
        # position updates
        else:
            if self.broadcasting:
                self.deactivatePhysics()
                self.stopPosHprBroadcast()
            self.startSmooth()
        self.hideShadows()

    def exitDropped(self):
        # If I'm the one who dropped it
        # Then I should stop broadcasting
        # the position updates
        if self.avId == base.localAvatar.doId:
            if self.newState != 'SlidingFloor':
                self.deactivatePhysics()
                self.stopPosHprBroadcast()
        # Otherwise, I'm the one receiving the
        # position updates so I should stop
        else:
            self.stopSmooth()

        if hasattr(self, 'crane'):
            del self.crane
        self.showShadows()

    def enterSlidingFloor(self, avId):
        # The object is now sliding across the floor under local
        # control.  Crank up the friction so it will slow down more
        # quickly.
        
        self.avId = avId
        
        if self.lerpInterval:
            self.lerpInterval.finish()
            self.lerpInterval = None
            
        if self.avId == base.localAvatar.doId:
            self.activatePhysics()
            self.startPosHprBroadcast(avId=self.avId, period=.05)
            
            self.handler.setStaticFrictionCoef(0.9)
            self.handler.setDynamicFrictionCoef(0.5)

            # Start up a task to watch for it to actually stop drifting.
            # When it does, we notify the AI.
            if self.wantsWatchDrift:
                taskMgr.add(self.__watchDrift, self.watchDriftName)
        else:
            if self.broadcasting:
                self.deactivatePhysics()
                self.stopPosHprBroadcast()
            self.startSmooth()
            
        self.hitFloorSoundInterval.start()

    def exitSlidingFloor(self):
        if self.avId == base.localAvatar.doId:
            taskMgr.remove(self.watchDriftName)
            self.deactivatePhysics()
            self.stopPosHprBroadcast()
        else:
            self.stopSmooth()

    def enterFree(self):
        self.localControl = False
        self.resetSpeedCaching()
        self.avId = 0
        self.craneId = 0

    def exitFree(self):
        pass

    class BroadcastTypes(IntEnum):
        FULL = 0
        XYH = 1
        XY = 2

    def _posHprBroadcast(self, task=DummyTask):
        # TODO: we explicitly stagger the initial task timing in
        # startPosHprBroadcast; we should at least make an effort to keep
        # this task accurately aligned with its period and starting time.
        if base.localAvatar.doId == self.avId:
            self.d_broadcastPosHpr()
            task.setDelay(self.__broadcastPeriod)
            return Task.again
        else:
            return Task.done

    def setPosHprBroadcastPeriod(self, period):
        # call this at any time to change the delay between broadcasts
        self.__broadcastPeriod = period

    def getPosHprBroadcastPeriod(self):
        # query the current delay between broadcasts
        return self.__broadcastPeriod
    
    def startPosHprBroadcast(self, avId=None, period=.01568, stagger=0, type=None):
        if self.cnode is None:
            self.initializeCnode()

        BT = self.BroadcastTypes
        if type is None:
            type = BT.FULL
        # set the broadcast type
        self.broadcastType = type

        broadcastFuncs = {
            BT.FULL: self.cnode.broadcastPosHprFull,
            BT.XYH:  self.cnode.broadcastPosHprXyh,
            BT.XY:  self.cnode.broadcastPosHprXy,
            }
        # this comment is here so it will show up in a grep for 'def d_broadcastPosHpr'
        self.d_broadcastPosHpr = broadcastFuncs[self.broadcastType]

        # Set stagger to non-zero to randomly delay the initial task execution
        # over 'period' seconds, to spread out task processing over time
        # when a large number of SmoothNodes are created simultaneously.
        taskName = self.getPosHprBroadcastTaskName() + '-%s' % avId

        # Set up telemetry optimization variables
        self.cnode.initialize(self, self.dclass, self.doId)

        self.setPosHprBroadcastPeriod(period)
        # Broadcast our initial position
        self.b_clearSmoothing()
        self.cnode.sendEverything()

        # remove any old tasks
        taskMgr.remove(taskName)
        # spawn the new task
        delay = 0.
        if stagger:
            delay = randFloat(period)
        if self.wantSmoothPosBroadcastTask():
            taskMgr.doMethodLater(self.__broadcastPeriod + delay,
                                  self._posHprBroadcast, taskName)
        
        self.broadcasting = True
            
    def stopPosHprBroadcast(self):
        taskMgr.remove(self.getPosHprBroadcastTaskName() + '-%s' % base.localAvatar.doId)
        # Delete this callback because it maintains a reference to self
        self.d_broadcastPosHpr = None
        self.broadcasting = False