from . import DistributedSZTreasureAI
from ..archipelago.definitions import util

from apworld.archipelago.worlds.toontown import locations
from toontown.toonbase import ToontownGlobals

ARCHI_CODE_TO_LOCATION = {
    ToontownGlobals.ToontownCentral: util.ap_location_name_to_id(locations.ToontownLocationName.TTC_TREASURE_1.value),
    ToontownGlobals.ToontownCentral + 1: util.ap_location_name_to_id(
        locations.ToontownLocationName.TTC_TREASURE_2.value),
    ToontownGlobals.DonaldsDock: util.ap_location_name_to_id(locations.ToontownLocationName.DD_TREASURE_1.value),
    ToontownGlobals.DonaldsDock + 1: util.ap_location_name_to_id(locations.ToontownLocationName.DD_TREASURE_2.value),
    ToontownGlobals.DaisyGardens: util.ap_location_name_to_id(locations.ToontownLocationName.DG_TREASURE_1.value),
    ToontownGlobals.DaisyGardens + 1: util.ap_location_name_to_id(locations.ToontownLocationName.DG_TREASURE_2.value),
    ToontownGlobals.MinniesMelodyland: util.ap_location_name_to_id(locations.ToontownLocationName.MML_TREASURE_1.value),
    ToontownGlobals.MinniesMelodyland + 1: util.ap_location_name_to_id(
        locations.ToontownLocationName.MML_TREASURE_2.value),
    ToontownGlobals.TheBrrrgh: util.ap_location_name_to_id(locations.ToontownLocationName.TB_TREASURE_1.value),
    ToontownGlobals.TheBrrrgh + 1: util.ap_location_name_to_id(locations.ToontownLocationName.TB_TREASURE_2.value),
    ToontownGlobals.DonaldsDreamland: util.ap_location_name_to_id(locations.ToontownLocationName.DDL_TREASURE_1.value),
    ToontownGlobals.DonaldsDreamland + 1: util.ap_location_name_to_id(
        locations.ToontownLocationName.DDL_TREASURE_2.value),
    ToontownGlobals.OutdoorZone: util.ap_location_name_to_id(locations.ToontownLocationName.AA_TREASURE_1.value),
    ToontownGlobals.OutdoorZone + 1: util.ap_location_name_to_id(locations.ToontownLocationName.AA_TREASURE_2.value),
    ToontownGlobals.GoofySpeedway: util.ap_location_name_to_id(locations.ToontownLocationName.GS_TREASURE_1.value),
    ToontownGlobals.GoofySpeedway + 1: util.ap_location_name_to_id(locations.ToontownLocationName.GS_TREASURE_2.value),
    ToontownGlobals.SellbotHQ: util.ap_location_name_to_id(locations.ToontownLocationName.SBHQ_TREASURE_1.value),
    ToontownGlobals.SellbotHQ + 1: util.ap_location_name_to_id(locations.ToontownLocationName.SBHQ_TREASURE_2.value),
    ToontownGlobals.CashbotHQ: util.ap_location_name_to_id(locations.ToontownLocationName.CBHQ_TREASURE_1.value),
    ToontownGlobals.CashbotHQ + 1: util.ap_location_name_to_id(locations.ToontownLocationName.CBHQ_TREASURE_2.value),
    ToontownGlobals.LawbotHQ: util.ap_location_name_to_id(locations.ToontownLocationName.LBHQ_TREASURE_1.value),
    ToontownGlobals.LawbotHQ + 1: util.ap_location_name_to_id(locations.ToontownLocationName.LBHQ_TREASURE_2.value),
    ToontownGlobals.BossbotHQ: util.ap_location_name_to_id(locations.ToontownLocationName.BBHQ_TREASURE_1.value),
    ToontownGlobals.BossbotHQ + 1: util.ap_location_name_to_id(locations.ToontownLocationName.BBHQ_TREASURE_2.value),
}


class DistributedArchiTreasureAI(DistributedSZTreasureAI.DistributedSZTreasureAI):

    def __init__(self, air, treasurePlanner, x, y, z):
        DistributedSZTreasureAI.DistributedSZTreasureAI.__init__(self, air, treasurePlanner, x, y, z)

    def getLocationFromCode(self, archiCode):
        return ARCHI_CODE_TO_LOCATION[archiCode]

    def validAvatar(self, av, archiCode):
        if av:
            return self.getLocationFromCode(archiCode) not in av.getCheckedLocations()
        return False

    def d_setGrab(self, avId, archiCode):
        #DistributedTreasureAI.DistributedTreasureAI.d_setGrab(self, avId)
        self.notify.debug('d_setGrab %s' % avId)
        self.sendUpdate('setGrab', [avId])
        av = self.air.doId2do[avId]
        if av:
            av.addCheckedLocation(self.getLocationFromCode(archiCode))

