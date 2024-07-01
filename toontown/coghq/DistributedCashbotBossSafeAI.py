from panda3d.core import *

from toontown.coghq import CraneLeagueGlobals
from toontown.coghq.DistributedCashbotBossHeavyCraneAI import DistributedCashbotBossHeavyCraneAI
from toontown.coghq.DistributedCashbotBossSideCraneAI import DistributedCashbotBossSideCraneAI
from toontown.toonbase import ToontownGlobals
from otp.otpbase import OTPGlobals
from . import DistributedCashbotBossObjectAI
import math

class DistributedCashbotBossSafeAI(DistributedCashbotBossObjectAI.DistributedCashbotBossObjectAI):

    """ This is a safe sitting around in the Cashbot CFO final battle
    room.  It's used as a prop for toons to pick up and throw at the
    CFO's head.  Also, the special safe with self.index == 0
    represents the safe that the CFO uses to put on his own head as a
    safety helmet from time to time. """

    # A safe remains under physical control of whichever client
    # last dropped it, even after it stops moving.  This allows
    # goons to push safes out of the way.
    wantsWatchDrift = 0

    def __init__(self, air, boss, index):
        DistributedCashbotBossObjectAI.DistributedCashbotBossObjectAI.__init__(self, air, boss)
        self.index = index
        
        self.avoidHelmet = 0
        
        # A sphere so goons will see and avoid us.
        cn = CollisionNode('sphere')
        cs = CollisionSphere(0, 0, 0, 6)
        cn.addSolid(cs)
        self.attachNewNode(cn)

    def resetToInitialPosition(self):
        posHpr = CraneLeagueGlobals.SAFE_POSHPR[self.index]
        self.setPosHpr(*posHpr)
        
        
    ### Messages ###

    def getIndex(self):
        return self.index

    def getMinImpact(self):
        if self.boss.heldObject:
            return self.boss.ruleset.MIN_DEHELMET_IMPACT
        else:
            return self.boss.ruleset.MIN_SAFE_IMPACT

    def hitBoss(self, impact, craneId):
        avId = self.air.getAvatarIdFromSender()
        
        self.validate(avId, 1.0 >= impact >= 0, 'invalid hitBoss impact %s' % impact)
        
        if avId not in self.boss.involvedToons:
            return
            
        if self.state != 'Dropped' and self.state != 'Grabbed':
            return
            
        if self.avoidHelmet or self == self.boss.heldObject:
            # Ignore the helmet we just knocked off.
            return

        self.boss.debug(doId=avId, content='Safe hit with impact=%.2f' % impact)

        if impact <= self.getMinImpact():
            self.boss.d_updateLowImpactHits(avId)
            return

        # The client reports successfully striking the boss in the
        # head with this object.
        if self.boss.heldObject == None:
            if self.boss.attackCode == ToontownGlobals.BossCogDizzy:
                # While the boss is dizzy, a safe hitting him in the
                # head does lots of damage.
                damage = int(impact * 50)
                crane = simbase.air.doId2do.get(craneId)
                
                # Apply a multiplier if needed (heavy cranes)
                damage *= crane.getDamageMultiplier()
                damage *= self.boss.ruleset.SAFE_CFO_DAMAGE_MULTIPLIER
                damage = math.ceil(damage)
                
                self.boss.recordHit(max(damage, 2), impact, craneId)
                
            elif self.boss.acceptHelmetFrom(avId):
                # If he's not dizzy, he grabs the safe and makes a
                # helmet out of it only if he is allowed to safe helmet.
                if self.boss.ruleset.DISABLE_SAFE_HELMETS:
                    return

                self.demand('Grabbed', self.boss.doId, self.boss.doId)
                self.boss.heldObject = self
                self.boss.d_updateSafePoints(avId, self.boss.ruleset.POINTS_PENALTY_SAFEHEAD)
                
        elif impact >= self.getMinImpact():
            self.boss.d_updateSafePoints(avId, self.boss.ruleset.POINTS_DESAFE)
            self.boss.heldObject.demand('Dropped', avId, self.boss.doId)
            self.boss.heldObject.avoidHelmet = 1
            self.boss.heldObject = None
            self.avoidHelmet = 1
            self.boss.waitForNextHelmet()
        return

    def requestInitial(self):
        # The client controlling the safe dropped it through the
        # world; reset it to its initial state.
        
        avId = self.air.getAvatarIdFromSender()
        
        if avId == self.avId:
            self.demand('Initial')

    def requestGrab(self):
        avId = self.air.getAvatarIdFromSender()
        if self.state != 'Grabbed' and self.state != 'Off':
            craneId, objectId = self.__getCraneAndObject(avId)
            crane = simbase.air.doId2do.get(craneId)
            if crane:
                if craneId != 0 and objectId == 0:
                    # If it is a sidecrane, dont pick up the safe
                    if isinstance(crane, DistributedCashbotBossSideCraneAI):
                        self.sendUpdateToAvatarId(avId, 'rejectGrab', [])
                        return
                    self.demand('Grabbed', avId, craneId)
                    return
            self.sendUpdateToAvatarId(avId, 'rejectGrab', [])
            
    def __getCraneAndObject(self, avId):
        if self.boss and self.boss.cranes != None:
            for crane in self.boss.cranes:
                if crane.avId == avId:
                    return (crane.doId, crane.objectId)
        return (0, 0)
        
        

    ### FSM States ###

    def enterGrabbed(self, avId, craneId):
        DistributedCashbotBossObjectAI.DistributedCashbotBossObjectAI.enterGrabbed(self, avId, craneId)
        self.avoidHelmet = 0

    def enterInitial(self):
        # The safe is in its initial, resting position.
        self.avoidHelmet = 0
        self.resetToInitialPosition()
        
        if self.index == 0:
            # The special "helmet-only" safe goes away completely when
            # it's in Initial mode.
            self.stash()
            
        self.d_setObjectState('I', 0, 0)

    def exitInitial(self):
        if self.index == 0:
            self.unstash()

    def enterFree(self):
        # The safe is somewhere on the floor, but not under anyone's
        # control. This can only happen to a safe when the player who
        # was controlling it disconnects during battle
        
        DistributedCashbotBossObjectAI.DistributedCashbotBossObjectAI.enterFree(self)
        self.avoidHelmet = 0
        
    def move(self, x, y, z, rotation):
        self.setPosHpr(x, y, z, rotation, 0, 0)
        self.sendUpdate('move', [x, y, z, rotation])

    # Called from client when a safe destroys a goon
    def destroyedGoon(self):
        avId = self.air.getAvatarIdFromSender()
        self.boss.d_updateGoonKilledBySafe(avId)
