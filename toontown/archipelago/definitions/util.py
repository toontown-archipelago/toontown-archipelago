from toontown.archipelago.definitions import locations
from toontown.hood import ZoneUtil
from toontown.toonbase import ToontownGlobals


# Given cog code (bf, nc, etc) return the AP location counterpart
# if not a valid cog, just returns an empty string
def cog_code_to_ap_location(cog_code: str) -> str:

    return {
        'cc': locations.COLD_CALLER_DEFEATED_LOCATION,
        'tm': locations.TELEMARKETER_DEFEATED_LOCATION,
        'nd': locations.NAME_DROPPER_DEFEATED_LOCATION,
        'gh': locations.GLAD_HANDER_DEFEATED_LOCATION,
        'ms': locations.MOVER_AND_SHAKER_DEFEATED_LOCATION,
        'tf': locations.TWO_FACE_DEFEATED_LOCATION,
        'm': locations.MINGLER_DEFEATED_LOCATION,
        'mh': locations.MR_HOLLYWOOD_DEFEATED_LOCATION,

        'sc': locations.SHORT_CHANGE_DEFEATED_LOCATION,
        'pp': locations.PENNY_PINCHER_DEFEATED_LOCATION,
        'tw': locations.TIGHTWAD_DEFEATED_LOCATION,
        'bc': locations.BEAN_COUNTER_DEFEATED_LOCATION,
        'nc': locations.NUMBER_CRUNCHER_DEFEATED_LOCATION,
        'mb': locations.MONEY_BAGS_DEFEATED_LOCATION,
        'ls': locations.LOAN_SHARK_DEFEATED_LOCATION,
        'rb': locations.ROBBER_BARRON_DEFEATED_LOCATION,

        'bf': locations.BOTTOM_FEEDER_DEFEATED_LOCATION,
        'b': locations.BLOODSUCKER_DEFEATED_LOCATION,
        'dt': locations.DOUBLE_TALKER_DEFEATED_LOCATION,
        'ac': locations.AMBULANCE_CHASER_DEFEATED_LOCATION,
        'bs': locations.BACKSTABBER_DEFEATED_LOCATION,
        'sd': locations.SPIN_DOCTOR_DEFEATED_LOCATION,
        'le': locations.LEGAL_EAGLE_DEFEATED_LOCATION,
        'bw': locations.BIG_WIG_DEFEATED_LOCATION,

        'f': locations.FLUNKY_DEFEATED_LOCATION,
        'p': locations.PENCIL_PUSHER_DEFEATED_LOCATION,
        'ym': locations.YESMAN_DEFEATED_LOCATION,
        'mm': locations.MICROMANAGER_DEFEATED_LOCATION,
        'ds': locations.DOWNSIZER_DEFEATED_LOCATION,
        'hh': locations.HEAD_HUNTER_DEFEATED_LOCATION,
        'cr': locations.CORPORATE_RAIDER_DEFEATED_LOCATION,
        'tbc': locations.BIG_CHEESE_DEFEATED_LOCATION

    }.get(cog_code, '')


# Given the string representation of a location, retrieve the numeric ID
def ap_location_name_to_id(location_name: str) -> int:
    return locations.LOCATION_DEFINITIONS.get(location_name, -1).unique_id


# Given a Zone ID, give the ID of an AP location award the player.
# returns -1 if this isn't a zone we have to worry about
def get_zone_discovery_id(zoneId: int) -> int:

    pgZone = ZoneUtil.getHoodId(zoneId)

    ZONE_TO_LOCATION = {
        ToontownGlobals.ToontownCentral: locations.DISCOVER_TTC,
        ToontownGlobals.DonaldsDock: locations.DISCOVER_DD,
        ToontownGlobals.DaisyGardens: locations.DISCOVER_DG,
        ToontownGlobals.MinniesMelodyland: locations.DISCOVER_MM,
        ToontownGlobals.TheBrrrgh: locations.DISCOVER_TB,
        ToontownGlobals.DonaldsDreamland: locations.DISCOVER_DDL,

        ToontownGlobals.SellbotHQ: locations.DISCOVER_SBHQ,
        ToontownGlobals.CashbotHQ: locations.DISCOVER_CBHQ,
        ToontownGlobals.LawbotHQ: locations.DISCOVER_LBHQ,
        ToontownGlobals.BossbotHQ: locations.DISCOVER_BBHQ,
    }

    # Valid zone?
    loc = ZONE_TO_LOCATION.get(pgZone)
    if not loc:
        return -1

    # We have a location, convert it to its ID
    return ap_location_name_to_id(loc)


# Gets the AP location ID from a ToontownGlobals facility ID definition
def get_facility_id(facility_id: int) -> int:

    FACILITY_LOCATION_CHECKS = {
        ToontownGlobals.SellbotFactoryInt: locations.CLEAR_FRONT_FACTORY,
        ToontownGlobals.SellbotFactoryIntS: locations.CLEAR_SIDE_FACTORY,

        ToontownGlobals.CashbotMintIntA: locations.CLEAR_COIN_MINT,
        ToontownGlobals.CashbotMintIntB: locations.CLEAR_DOLLAR_MINT,
        ToontownGlobals.CashbotMintIntC: locations.CLEAR_BULLION_MINT,

        ToontownGlobals.LawbotStageIntA: locations.CLEAR_A_OFFICE,
        ToontownGlobals.LawbotStageIntB: locations.CLEAR_B_OFFICE,
        ToontownGlobals.LawbotStageIntC: locations.CLEAR_C_OFFICE,
        ToontownGlobals.LawbotStageIntD: locations.CLEAR_D_OFFICE,

        ToontownGlobals.BossbotCountryClubIntA: locations.CLEAR_FRONT_THREE,
        ToontownGlobals.BossbotCountryClubIntB: locations.CLEAR_MIDDLE_THREE,
        ToontownGlobals.BossbotCountryClubIntC: locations.CLEAR_BACK_THREE,
    }

    loc = FACILITY_LOCATION_CHECKS.get(facility_id)
    if not loc:
        return -1

    return ap_location_name_to_id(loc)


# Given a hood ID, return a list of AP check location names present in that hood
def hood_to_task_locations(hoodId: int):
    return {
        ToontownGlobals.ToontownCentral: locations.TTC_TASK_LOCATIONS,
        ToontownGlobals.DonaldsDock: locations.DD_TASK_LOCATIONS,
        ToontownGlobals.DaisyGardens: locations.DG_TASK_LOCATIONS,
        ToontownGlobals.MinniesMelodyland: locations.MM_TASK_LOCATIONS,
        ToontownGlobals.TheBrrrgh: locations.TB_TASK_LOCATIONS,
        ToontownGlobals.DonaldsDreamland: locations.DDL_TASK_LOCATIONS,
    }.get(hoodId, [])

