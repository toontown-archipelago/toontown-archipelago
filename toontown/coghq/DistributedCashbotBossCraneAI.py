from panda3d.core import *
from direct.distributed import DistributedObjectAI
from toontown.coghq import CraneLeagueGlobals
from toontown.toonbase import ToontownGlobals
from otp.otpbase import OTPGlobals
from direct.fsm import FSM

class DistributedCashbotBossCraneAI(DistributedObjectAI.DistributedObjectAI, FSM.FSM):

    """ This is one of four/six/eight magnet cranes in the corner of the CFO
    boss battle room.  """

    def __init__(self, air, boss, index):
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)
        FSM.FSM.__init__(self, 'DistributedCashbotBossCraneAI')
        
        self.boss = boss
        self.index = index

        # A collision bubble to discourage the goons from walking
        # through the control area.
        cn = CollisionNode('controls')
        cs = CollisionSphere(0, -6, 0, 6)
        cn.addSolid(cs)
        self.goonShield = NodePath(cn)
        self.goonShield.setPosHpr(*CraneLeagueGlobals.ALL_CRANE_POSHPR[self.index])
        
        self.avId = 0
        self.objectId = 0
        
        self.setBroadcastStateChanges(True)

    def getName(self):
        return 'NormalCrane-%s' % self.index

    def setObjectID(self, objId):
        self.objectId = objId

    # Should we multiply any damage done from this crane?
    def getDamageMultiplier(self):
        return 1.0

    def getPointsForStun(self):
        return self.boss.ruleset.POINTS_STUN

    def getBossCogId(self):
        return self.boss.doId

    def getIndex(self):
        return self.index

    def d_setState(self, state, avId):
        self.sendUpdate('setState', [state, avId])

    def requestControl(self):
        # A client wants to start controlling the crane.
        avId = self.air.getAvatarIdFromSender()
        if avId not in self.air.doId2do:
            return

        av = self.air.doId2do[avId]
        if av.getHp() > 0 and avId in self.boss.involvedToons and self.avId == 0:
            # Also make sure the client isn't controlling some other
            # crane.
            craneId = self.__getCraneId(avId)
            if craneId == 0:
                self.request('Controlled', avId)

    def requestFree(self):
        # The client is done controlling the crane.
        avId = self.air.getAvatarIdFromSender()
        if avId == self.avId:
            self.request('Free')

    def removeToon(self, avId):
        if avId == self.avId:
            self.request('Free')

    def __getCraneId(self, avId):
        # Returns the craneId for the crane that the indicated avatar
        # is controlling, or 0 if none.
        
        if self.boss and self.boss.cranes != None:
            for crane in self.boss.cranes:
                if crane.avId == avId:
                    return crane.doId

        return 0



    ### FSM States ###
    
    def enterOff(self):
        self.goonShield.detachNode()

    def exitOff(self):
        self.goonShield.reparentTo(self.boss.scene)

    def enterControlled(self, avId):
        self.avId = avId
        self.d_setState('C', avId)

    def exitControlled(self):
        if self.objectId:
            # This will be filled in if an object has requested a
            # grab.  In this case, drop the object.
            obj = self.air.doId2do[self.objectId]
            obj.request('Dropped', self.avId, self.doId)

    def enterFree(self):
        self.avId = 0
        self.d_setState('F', 0)

    def exitFree(self):
        pass
