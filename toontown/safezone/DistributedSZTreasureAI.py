import math
from . import DistributedTreasureAI
from toontown.toonbase import ToontownGlobals

class DistributedSZTreasureAI(DistributedTreasureAI.DistributedTreasureAI):

    def __init__(self, air, treasurePlanner, x, y, z):
        DistributedTreasureAI.DistributedTreasureAI.__init__(self, air, treasurePlanner, x, y, z)
        if hasattr(treasurePlanner, 'healAmount'):
            self.healAmount = treasurePlanner.healAmount
        else:
            self.healAmount = 0.10

    def validAvatar(self, av):
        return av.hp > 0 and av.hp < av.maxHp

    def d_setGrab(self, avId):
        DistributedTreasureAI.DistributedTreasureAI.d_setGrab(self, avId)
        if avId in self.air.doId2do:
            av = self.air.doId2do[avId]
            av.toonUp(math.ceil(av.maxHp * self.healAmount))
