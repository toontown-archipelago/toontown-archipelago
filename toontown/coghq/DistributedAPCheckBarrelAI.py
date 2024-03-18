from apworld.toontown import locations
from . import DistributedBarrelBaseAI
from direct.directnotify import DirectNotifyGlobal
from direct.task import Task

from ..archipelago.definitions import util
from ..toonbase import ToontownGlobals


class DistributedAPCheckBarrelAI(DistributedBarrelBaseAI.DistributedBarrelBaseAI):


    # This is kinda hacky and a bit of a mouthful but basically we are mapping
    # (FactoryID, apBarrelIndex, floor) -> AP location check
    # Since factories and mints don't have floors, we can just default them to 0
    # If multiple barrels are in the same spec, they need to have differing apBarrelIndex attributes so we can
    # differentiate them here
    FACILITY_BARREL_TO_AP_CHECK = {

        # Factory barrels (2nd number in tuple is the ApBarrelIndex, 3rd is floor (0) bc we don't have floors)
        (ToontownGlobals.SellbotFactoryInt, 0, 0): locations.ToontownLocationName.FRONT_FACTORY_BARREL_1.value,
        (ToontownGlobals.SellbotFactoryInt, 1, 0): locations.ToontownLocationName.FRONT_FACTORY_BARREL_2.value,
        (ToontownGlobals.SellbotFactoryInt, 2, 0): locations.ToontownLocationName.FRONT_FACTORY_BARREL_3.value,
        (ToontownGlobals.SellbotFactoryIntS, 0, 0): locations.ToontownLocationName.SIDE_FACTORY_BARREL_1.value,
        (ToontownGlobals.SellbotFactoryIntS, 1, 0): locations.ToontownLocationName.SIDE_FACTORY_BARREL_2.value,
        (ToontownGlobals.SellbotFactoryIntS, 2, 0): locations.ToontownLocationName.SIDE_FACTORY_BARREL_3.value,

        # Mint barrels (2nd number in tuple is the ApBarrelIndex, 3rd is floor (0) bc we don't have floors)
        (ToontownGlobals.CashbotMintIntA, 0, 0): locations.ToontownLocationName.COIN_MINT_BARREL_1.value,
        (ToontownGlobals.CashbotMintIntA, 1, 0): locations.ToontownLocationName.COIN_MINT_BARREL_2.value,
        (ToontownGlobals.CashbotMintIntA, 2, 0): locations.ToontownLocationName.COIN_MINT_BARREL_3.value,
        (ToontownGlobals.CashbotMintIntB, 0, 0): locations.ToontownLocationName.DOLLAR_MINT_BARREL_1.value,
        (ToontownGlobals.CashbotMintIntB, 1, 0): locations.ToontownLocationName.DOLLAR_MINT_BARREL_2.value,
        (ToontownGlobals.CashbotMintIntB, 2, 0): locations.ToontownLocationName.DOLLAR_MINT_BARREL_3.value,
        (ToontownGlobals.CashbotMintIntC, 0, 0): locations.ToontownLocationName.BULLION_MINT_BARREL_1.value,
        (ToontownGlobals.CashbotMintIntC, 1, 0): locations.ToontownLocationName.BULLION_MINT_BARREL_2.value,
        (ToontownGlobals.CashbotMintIntC, 2, 0): locations.ToontownLocationName.BULLION_MINT_BARREL_3.value,

        # Office barrels (2nd is apBarrelIndex like before, 3rd number in tuple is the floorNum)
        (ToontownGlobals.LawbotStageIntA, 0, 0): locations.ToontownLocationName.A_OFFICE_BARREL_1.value,
        (ToontownGlobals.LawbotStageIntA, 0, 1): locations.ToontownLocationName.A_OFFICE_BARREL_2.value,
        (ToontownGlobals.LawbotStageIntA, 1, 0): locations.ToontownLocationName.A_OFFICE_BARREL_3.value,
        (ToontownGlobals.LawbotStageIntA, 1, 1): locations.ToontownLocationName.A_OFFICE_BARREL_4.value,
        (ToontownGlobals.LawbotStageIntB, 0, 0): locations.ToontownLocationName.B_OFFICE_BARREL_1.value,
        (ToontownGlobals.LawbotStageIntB, 0, 1): locations.ToontownLocationName.B_OFFICE_BARREL_2.value,
        (ToontownGlobals.LawbotStageIntB, 1, 0): locations.ToontownLocationName.B_OFFICE_BARREL_3.value,
        (ToontownGlobals.LawbotStageIntB, 1, 1): locations.ToontownLocationName.B_OFFICE_BARREL_4.value,
        (ToontownGlobals.LawbotStageIntC, 0, 0): locations.ToontownLocationName.C_OFFICE_BARREL_1.value,
        (ToontownGlobals.LawbotStageIntC, 0, 1): locations.ToontownLocationName.C_OFFICE_BARREL_2.value,
        (ToontownGlobals.LawbotStageIntC, 1, 0): locations.ToontownLocationName.C_OFFICE_BARREL_3.value,
        (ToontownGlobals.LawbotStageIntC, 1, 1): locations.ToontownLocationName.C_OFFICE_BARREL_4.value,
        (ToontownGlobals.LawbotStageIntD, 0, 0): locations.ToontownLocationName.D_OFFICE_BARREL_1.value,
        (ToontownGlobals.LawbotStageIntD, 0, 1): locations.ToontownLocationName.D_OFFICE_BARREL_2.value,
        (ToontownGlobals.LawbotStageIntD, 1, 0): locations.ToontownLocationName.D_OFFICE_BARREL_3.value,
        (ToontownGlobals.LawbotStageIntD, 1, 1): locations.ToontownLocationName.D_OFFICE_BARREL_4.value,

        # CGC barrels (2nd is apBarrelIndex like before, 3rd number in tuple is the floorNum)
        (ToontownGlobals.BossbotCountryClubIntA, 0, 0): locations.ToontownLocationName.FRONT_ONE_BARREL_1.value,
        (ToontownGlobals.BossbotCountryClubIntA, 1, 0): locations.ToontownLocationName.FRONT_ONE_BARREL_2.value,
        (ToontownGlobals.BossbotCountryClubIntB, 0, 0): locations.ToontownLocationName.MIDDLE_TWO_BARREL_1.value,
        (ToontownGlobals.BossbotCountryClubIntB, 0, 1): locations.ToontownLocationName.MIDDLE_TWO_BARREL_2.value,
        (ToontownGlobals.BossbotCountryClubIntB, 1, 0): locations.ToontownLocationName.MIDDLE_TWO_BARREL_3.value,
        (ToontownGlobals.BossbotCountryClubIntB, 1, 1): locations.ToontownLocationName.MIDDLE_TWO_BARREL_4.value,
        (ToontownGlobals.BossbotCountryClubIntC, 0, 0): locations.ToontownLocationName.BACK_THREE_BARREL_1.value,
        (ToontownGlobals.BossbotCountryClubIntC, 0, 1): locations.ToontownLocationName.BACK_THREE_BARREL_2.value,
        (ToontownGlobals.BossbotCountryClubIntC, 0, 2): locations.ToontownLocationName.BACK_THREE_BARREL_3.value,
        (ToontownGlobals.BossbotCountryClubIntC, 1, 0): locations.ToontownLocationName.BACK_THREE_BARREL_4.value,
        (ToontownGlobals.BossbotCountryClubIntC, 1, 1): locations.ToontownLocationName.BACK_THREE_BARREL_5.value,
        (ToontownGlobals.BossbotCountryClubIntC, 1, 2): locations.ToontownLocationName.BACK_THREE_BARREL_6.value,
    }

    def __init__(self, level, entId):
        DistributedBarrelBaseAI.DistributedBarrelBaseAI.__init__(self, level, entId)
        self.locationCheckId = util.ap_location_name_to_id(self.getAPLocationMapping())
        # Debug statement, use for when making new barrels
        # print(f"ap barrel: entid={entId} - level is a {type(level)} FactoryID/Floor: {self.getFacilityIdAndFloor()}, apBarrelIndex?: {self.getAPRewardIndex()}")

    # Kinda hacky but keep calling getFactoryId/getMintId etc etc until we get something bc abstraction is not real
    # apparently at Disney
    def getFacilityIdAndFloor(self):

        from .DistributedCountryClubRoomAI import DistributedCountryClubRoomAI
        from .DistributedFactoryAI import DistributedFactoryAI
        from .DistributedMintRoomAI import DistributedMintRoomAI
        from .DistributedStageRoomAI import DistributedStageRoomAI

        # If level is a factory
        if isinstance(self.level, DistributedFactoryAI):
            return self.level.getFactoryId(), 0  # no floors in factories

        # If level is a mint room
        if isinstance(self.level, DistributedMintRoomAI):
            return self.level.getMintId(), 0  # no floors in mints

        # If level is an office room
        if isinstance(self.level, DistributedStageRoomAI):
            return self.level.getStageId(), self.level.getFloorNum()

        # If level is a cgc room
        if isinstance(self.level, DistributedCountryClubRoomAI):
            return self.level.getCountryClubId(), self.level.getFloorNum()

        # This should never run i think?
        raise ValueError(f"Unknown facility class for AP barrel: {self.level.__class__.__name__}")

    # Get the location mapping that this barrel should have from the dict above (facilityID, apreward index, floor)
    def getAPLocationMapping(self):
        facilityID, floor = self.getFacilityIdAndFloor()
        mappingKey = (facilityID, self.getAPRewardIndex(), floor)
        return self.FACILITY_BARREL_TO_AP_CHECK[mappingKey]

    def b_setLocationCheckId(self, locationCheckId):
        self.setLocationCheckId(locationCheckId)
        self.d_setLocationCheckId(locationCheckId)

    def setLocationCheckId(self, locationCheckId):
        self.locationCheckId = locationCheckId

    def getLocationCheckId(self):
        return self.locationCheckId

    def d_setLocationCheckId(self, locationCheckId):
        self.sendUpdate('setLocationCheckId', [locationCheckId])

    def d_setGrab(self, avId):
        self.notify.debug('d_setGrab %s' % avId)
        self.sendUpdate('setGrab', [avId])
        av = self.air.doId2do.get(avId)
        ap_check_id: int = util.ap_location_name_to_id(self.getAPLocationMapping())
        if av:
            av.addCheckedLocation(ap_check_id)
