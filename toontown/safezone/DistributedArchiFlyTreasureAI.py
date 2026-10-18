from . import DistributedSZTreasureAI
from toontown.toonbase import ToontownGlobals
import math

class DistributedArchiFlyTreasureAI(DistributedSZTreasureAI.DistributedSZTreasureAI):

    def __init__(self, air, treasurePlanner, x, y, z):
        DistributedSZTreasureAI.DistributedSZTreasureAI.__init__(self, air, treasurePlanner, x, y, z)
        self.healAmount = 0.25

    def getLocationFromZone(self, zone):
        return ToontownGlobals.ARCHI_JUMP_ZONE_TO_LOCATION[zone]

    def validAvatar(self, av, zone):
        if av:
            restrict_jump = av.slotData.get('restrict_jump', False)
            if not restrict_jump:
                return self.isValidHp(av)
            if self.getLocationFromZone(zone) not in av.getCheckedLocations():
                return True
            else:
                return self.isValidHp(av)
        return False

    def isValidHp(self, av):
        return av.hp < av.maxHp

    def d_setGrab(self, avId, zone):
        self.notify.debug('d_setGrab %s' % avId)
        self.sendUpdate('setGrab', [avId])
        av = self.air.doId2do[avId]
        if av:
            restrict_jump = av.slotData.get('restrict_jump', False)
            location = self.getLocationFromZone(zone)
            if location not in av.getCheckedLocations() and restrict_jump:
                av.addCheckedLocation(location)
                return
            av.toonUp(math.ceil(av.maxHp * self.healAmount))
