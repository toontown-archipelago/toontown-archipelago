from . import DistributedSZTreasureAI
from toontown.toonbase import ToontownGlobals
import math

class DistributedArchiTreasureAI(DistributedSZTreasureAI.DistributedSZTreasureAI):

    def __init__(self, air, treasurePlanner, x, y, z):
        DistributedSZTreasureAI.DistributedSZTreasureAI.__init__(self, air, treasurePlanner, x, y, z)
        self.healAmount = 0.15

    def getLocationFromCode(self, archiCode, index):
        return ToontownGlobals.ARCHI_CODE_TO_LOCATION[archiCode][index]

    def validAvatar(self, av, archiCode):
        if av:
            treasureCount = av.slotData.get('treasures_per_location', 4)
            if not treasureCount:
                return self.isValidHp(av)
            for treasure in range(treasureCount):
                if self.getLocationFromCode(archiCode, treasure) in av.getCheckedLocations():
                    continue
                else:
                    return True
            return self.isValidHp(av)
        return False

    def isValidHp(self, av):
        return (av.hp > 0 and av.hp < av.maxHp)

    def d_setGrab(self, avId, archiCode):
        self.notify.debug('d_setGrab %s' % avId)
        self.sendUpdate('setGrab', [avId])
        av = self.air.doId2do[avId]
        if av:
            treasureCount = av.slotData.get('treasures_per_location', 4)
            for treasure in range(treasureCount):
                if self.getLocationFromCode(archiCode, treasure) in av.getCheckedLocations():
                    continue
                else:
                    av.addCheckedLocation(self.getLocationFromCode(archiCode, treasure))
                    return
            # We've gone through the loop, meaning we've gotten all checks. Let's heal the toon.
            av.toonUp(math.ceil(av.maxHp * self.healAmount))
