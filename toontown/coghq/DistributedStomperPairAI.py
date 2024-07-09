from otp.ai.AIBase import *
from direct.directnotify import DirectNotifyGlobal
from otp.level import DistributedEntityAI
from toontown.toonbase import ToontownGlobals
from . import StomperGlobals
from direct.distributed import ClockDelta

from ..archipelago.definitions.death_reason import DeathReason
import math

class DistributedStomperPairAI(DistributedEntityAI.DistributedEntityAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedStomperAI')

    def __init__(self, level, entId):
        DistributedEntityAI.DistributedEntityAI.__init__(self, level, entId)
        self.stompers = [None, None]
        self.hitPtsTaken = 3
        return

    def generate(self):
        DistributedEntityAI.DistributedEntityAI.generate(self)

    def delete(self):
        DistributedEntityAI.DistributedEntityAI.delete(self)

    def setChildren(self, doIds):
        for id in doIds:
            self.children = simbase.air.doId2do[id]

        self.sendUpdate('setChildren', [doIds])

    def setSquash(self):
        avId = self.air.getAvatarIdFromSender()
        av = simbase.air.doId2do.get(avId)
        hitPtsTakenExtra = 0
        if hasattr(self, 'level') and hasattr(self.level, 'stageId'):
            if self.level.stageId in [ToontownGlobals.LawbotStageIntC, ToontownGlobals.LawbotStageIntD]:
                hitPtsTakenExtra = int(math.ceil(self.hitPtsTaken * 0.5))
        if hasattr(self, 'level') and hasattr(self.level, 'mintId'):
            if self.level.mintId == ToontownGlobals.CashbotMintIntC:
                hitPtsTakenExtra = int(math.ceil(self.hitPtsTaken * 0.5))
        if av:
            av.setDeathReason(DeathReason.STOMPER)
            av.takeDamage(self.hitPtsTaken + hitPtsTakenExtra)
