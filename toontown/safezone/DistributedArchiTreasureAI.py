from . import DistributedSZTreasureAI
from toontown.toonbase import ToontownGlobals

class DistributedArchiTreasureAI(DistributedSZTreasureAI.DistributedSZTreasureAI):

    def __init__(self, air, treasurePlanner, x, y, z):
        DistributedSZTreasureAI.DistributedSZTreasureAI.__init__(self, air, treasurePlanner, x, y, z)

    def getLocationFromCode(self, archiCode, index):
        return ToontownGlobals.ARCHI_CODE_TO_LOCATION[archiCode][index]

    def validAvatar(self, av, archiCode):
        if av:
            treasureCount = av.slotData.get('treasures_per_location', 4)
            if not treasureCount:
                return False
            for treasure in range(treasureCount):
                if self.getLocationFromCode(archiCode, treasure) in av.getCheckedLocations():
                    continue
                else:
                    return True
            return False
        return False

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

