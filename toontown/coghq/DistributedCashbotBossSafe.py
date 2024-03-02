from panda3d.core import *
from panda3d.physics import *
from direct.interval.IntervalGlobal import *
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownGlobals
from otp.otpbase import OTPGlobals
from . import DistributedCashbotBossObject
import copy

from toontown.coghq import CraneLeagueGlobals

class DistributedCashbotBossSafe(DistributedCashbotBossObject.DistributedCashbotBossObject):

    """ This is a safe sitting around in the Cashbot CFO final battle
    room.  It's used as a prop for toons to pick up and throw at the
    CFO's head.  Also, the special safe with self.index == 0
    represents the safe that the CFO uses to put on his own head as a
    safety helmet from time to time. """
    
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedCashbotBossSafe')
    
    grabPos = (0, 0, -8.2)
    
    # What happens to the crane and its cable when this object is picked up?
    craneFrictionCoef = 0.2
    craneSlideSpeed = 11
    craneRotateSpeed = 16

    # A safe remains under physical control of whichever client
    # last dropped it, even after it stops moving.  This allows
    # goons to push safes out of the way.
    wantsWatchDrift = 0

    def __init__(self, cr):
        DistributedCashbotBossObject.DistributedCashbotBossObject.__init__(self, cr)
        NodePath.__init__(self, 'object')
        self.index = None
        
        self.flyToMagnetSfx = loader.loadSfx('phase_5/audio/sfx/TL_rake_throw_only.ogg')
        self.hitMagnetSfx = loader.loadSfx('phase_5/audio/sfx/AA_drop_safe.ogg')
        # We want these sfx's to overlap just a smidge for effect.
        self.toMagnetSoundInterval = Parallel(SoundInterval(self.flyToMagnetSfx, duration=ToontownGlobals.CashbotBossToMagnetTime, node=self), Sequence(Wait(ToontownGlobals.CashbotBossToMagnetTime - 0.02), SoundInterval(self.hitMagnetSfx, duration=1.0, node=self)))
        self.hitFloorSfx = loader.loadSfx('phase_5/audio/sfx/AA_drop_bigweight_miss.ogg')
        self.hitFloorSoundInterval = SoundInterval(self.hitFloorSfx, node=self)
        self.name = 'safe'
        return

    def announceGenerate(self):
        DistributedCashbotBossObject.DistributedCashbotBossObject.announceGenerate(self)
        self.name = 'safe-%s' % self.doId
        self.setName(self.name)
        
        self.boss.safe.copyTo(self)
        self.shadow = self.find('**/shadow')
        
        self.collisionNode.setName('safe')
        #cs = CollisionSphere(0, 0, 4, 4) #TTR Collisions
        cs = CollisionCapsule(0, 0, 4, 0, 0, 4, 4) #TTCC Collisions
        self.collisionNode.addSolid(cs)
        
        if self.index == 0:
            # If this is safe 0, it's the safe that the CFO uses when
            # he wants to put on his own helmet.  This one can't be
            # picked up by magnets, and it doesn't stick around for
            # any length of time when it's knocked off his head--it
            # just falls through the floor and resets.
            
            self.collisionNode.setIntoCollideMask(ToontownGlobals.PieBitmask | OTPGlobals.WallBitmask)
            self.collisionNode.setFromCollideMask(ToontownGlobals.PieBitmask)
            
        self.boss.safes[self.index] = self
        
        #print(self)
        #self.setH(CraneLeagueGlobals.SAFE_H[self.index])
        #print(self.getH())
        
        #self.setH(180)
        self.setupPhysics('safe')
        #print("Safe: %s, Node: %s" % (self.getH(), self.collisionNodePath.getH()))
        self.resetToInitialPosition()
        #print("AFTER RESET: Safe: %s, Node: %s" % (self.getH(), self.collisionNodePath.getH()))
        
        #print(self.getH())
        #print(self.physicsObject.getOrientation())
        #print("")

    def disable(self):
        del self.boss.safes[self.index]
        DistributedCashbotBossObject.DistributedCashbotBossObject.disable(self)

    def hideShadows(self):
        self.shadow.hide()

    def showShadows(self):
        self.shadow.show()
        
    def setupPhysics(self, name):
        an = ActorNode('%s-%s' % (name, self.doId))
        an.getPhysicsObject().setOrientation(LOrientationf(0, 0, 0, 1))
        anp = NodePath(an)
        if not self.isEmpty():
            self.reparentTo(anp)

        # It is important that there be no messenger hooks added on
        # this object at the time we reassign the NodePath.
        NodePath.assign(self, anp)
        
        self.physicsObject = an.getPhysicsObject()
        #self.copy.physicsObject = an.getPhysicsObject()
        #print(self.copy.physicsObject.getOrientation())
        #print(self.copy.physicsObject.getOrientation().getAngle())
        #self.physicsObject.setOriented(False)
        self.setTag('object', str(self.doId))
       
        self.collisionNodePath.reparentTo(self)
        #self.collisionNodePath.setH(180)
        self.handler = PhysicsCollisionHandler()
        #self.copy = copy.copy(self)
        #print(self.copy)
        self.handler.addCollider(self.collisionNodePath, self)

        # Set up a collision event so we know when the object hits the
        # floor, or the boss's target.
        self.collideName = self.uniqueName('collide')
        self.handler.addInPattern(self.collideName + '-%in')
        self.handler.addAgainPattern(self.collideName + '-%in')
        
        self.watchDriftName = self.uniqueName('watchDrift')
        self.startCacheName = self.uniqueName('startSpeedCaching')

    def getMinImpact(self):
        # This method returns the minimum impact, in feet per second,
        # with which the object should hit the boss before we bother
        # to tell the server.
        if self.boss.heldObject:
            return self.boss.ruleset.MIN_DEHELMET_IMPACT
        else:
            return self.boss.ruleset.MIN_SAFE_IMPACT

    def doHitGoon(self, goon):

        # Should we disable or destroy?
        if self.boss.ruleset.SAFES_STUN_GOONS:
            goon.doLocalStun()
        else:
            goon.b_destroyGoon()
            self.sendUpdate('destroyedGoon', [])

    def resetToInitialPosition(self):
        posHpr = CraneLeagueGlobals.SAFE_POSHPR[self.index]
        self.setPosHpr(*posHpr)
        self.physicsObject.setVelocity(0, 0, 0)

    def fellOut(self):
        # The safe fell out of the world.  Reset it back to its
        # original position.
        self.deactivatePhysics()
        self.d_requestInitial()
        
    def setIndex(self, index):
        self.index = index

        
 
    ##### Messages To/From The Server #####
    
    def setObjectState(self, state, avId, craneId):
        if state == 'I':
            self.demand('Initial')
        else:
            DistributedCashbotBossObject.DistributedCashbotBossObject.setObjectState(self, state, avId, craneId)

    def d_requestInitial(self):
        self.sendUpdate('requestInitial')



    ### FSM States ###
    
    def enterInitial(self):
        self.resetSpeedCaching()
        self.resetToInitialPosition()
        self.showShadows()
        
        if self.index == 0:
            # The special "helmet-only" safe goes away completely when
            # it's in Initial mode.
            self.stash()

    def exitInitial(self):
        if self.index == 0:
            self.unstash()
            
    def move(self, x, y, z, rotation):
        self.setPosHpr(x, y, z, rotation, 0, 0)
