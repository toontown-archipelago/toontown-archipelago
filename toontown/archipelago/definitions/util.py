from apworld.toontown import consts, ToontownLocationName, LOCATION_DEFINITIONS
from apworld.toontown.locations import TTC_TASK_LOCATIONS, DD_TASK_LOCATIONS, DG_TASK_LOCATIONS, MML_TASK_LOCATIONS, TB_TASK_LOCATIONS, DDL_TASK_LOCATIONS

from typing import Union

from toontown.hood import ZoneUtil
from toontown.toonbase import ToontownGlobals


# Given cog code (bf, nc, etc) return the AP location counterpart
# if not a valid cog, just returns an empty string
def cog_code_to_ap_location(cog_code: str) -> str:

    return {
        'cc': (ToontownLocationName.COLD_CALLER_DEFEATED.value, ToontownLocationName.COLD_CALLER_MAXED.value),
        'tm': (ToontownLocationName.TELEMARKETER_DEFEATED.value, ToontownLocationName.TELEMARKETER_MAXED.value),
        'nd': (ToontownLocationName.NAME_DROPPER_DEFEATED.value, ToontownLocationName.NAME_DROPPER_MAXED.value),
        'gh': (ToontownLocationName.GLAD_HANDER_DEFEATED.value, ToontownLocationName.GLAD_HANDER_MAXED.value),
        'ms': (ToontownLocationName.MOVER_AND_SHAKER_DEFEATED.value, ToontownLocationName.MOVER_AND_SHAKER_MAXED.value),
        'tf': (ToontownLocationName.TWO_FACE_DEFEATED.value, ToontownLocationName.TWO_FACE_MAXED.value),
        'm': (ToontownLocationName.MINGLER_DEFEATED.value, ToontownLocationName.MINGLER_MAXED.value),
        'mh': (ToontownLocationName.MR_HOLLYWOOD_DEFEATED.value, ToontownLocationName.MR_HOLLYWOOD_MAXED.value),

        'sc': (ToontownLocationName.SHORT_CHANGE_DEFEATED.value, ToontownLocationName.SHORT_CHANGE_MAXED.value),
        'pp': (ToontownLocationName.PENNY_PINCHER_DEFEATED.value, ToontownLocationName.PENNY_PINCHER_MAXED.value),
        'tw': (ToontownLocationName.TIGHTWAD_DEFEATED.value, ToontownLocationName.TIGHTWAD_MAXED.value),
        'bc': (ToontownLocationName.BEAN_COUNTER_DEFEATED.value, ToontownLocationName.BEAN_COUNTER_MAXED.value),
        'nc': (ToontownLocationName.NUMBER_CRUNCHER_DEFEATED.value, ToontownLocationName.NUMBER_CRUNCHER_MAXED.value),
        'mb': (ToontownLocationName.MONEY_BAGS_DEFEATED.value, ToontownLocationName.MONEY_BAGS_MAXED.value),
        'ls': (ToontownLocationName.LOAN_SHARK_DEFEATED.value, ToontownLocationName.LOAN_SHARK_MAXED.value),
        'rb': (ToontownLocationName.ROBBER_BARRON_DEFEATED.value, ToontownLocationName.ROBBER_BARRON_MAXED.value),

        'bf': (ToontownLocationName.BOTTOM_FEEDER_DEFEATED.value, ToontownLocationName.BOTTOM_FEEDER_MAXED.value),
        'b': (ToontownLocationName.BLOODSUCKER_DEFEATED.value, ToontownLocationName.BLOODSUCKER_MAXED.value),
        'dt': (ToontownLocationName.DOUBLE_TALKER_DEFEATED.value, ToontownLocationName.DOUBLE_TALKER_MAXED.value),
        'ac': (ToontownLocationName.AMBULANCE_CHASER_DEFEATED.value, ToontownLocationName.AMBULANCE_CHASER_MAXED.value),
        'bs': (ToontownLocationName.BACKSTABBER_DEFEATED.value, ToontownLocationName.BACKSTABBER_MAXED.value),
        'sd': (ToontownLocationName.SPIN_DOCTOR_DEFEATED.value, ToontownLocationName.SPIN_DOCTOR_MAXED.value),
        'le': (ToontownLocationName.LEGAL_EAGLE_DEFEATED.value, ToontownLocationName.LEGAL_EAGLE_MAXED.value),
        'bw': (ToontownLocationName.BIG_WIG_DEFEATED.value, ToontownLocationName.BIG_WIG_MAXED.value),

        'f': (ToontownLocationName.FLUNKY_DEFEATED.value, ToontownLocationName.FLUNKY_MAXED.value),
        'p': (ToontownLocationName.PENCIL_PUSHER_DEFEATED.value, ToontownLocationName.PENCIL_PUSHER_MAXED.value),
        'ym': (ToontownLocationName.YESMAN_DEFEATED.value, ToontownLocationName.YESMAN_MAXED.value),
        'mm': (ToontownLocationName.MICROMANAGER_DEFEATED.value, ToontownLocationName.MICROMANAGER_MAXED.value),
        'ds': (ToontownLocationName.DOWNSIZER_DEFEATED.value, ToontownLocationName.DOWNSIZER_MAXED.value),
        'hh': (ToontownLocationName.HEAD_HUNTER_DEFEATED.value, ToontownLocationName.HEAD_HUNTER_MAXED.value),
        'cr': (ToontownLocationName.CORPORATE_RAIDER_DEFEATED.value, ToontownLocationName.CORPORATE_RAIDER_MAXED.value),
        'tbc': (ToontownLocationName.BIG_CHEESE_DEFEATED.value, ToontownLocationName.BIG_CHEESE_MAXED.value)

    }.get(cog_code, '')


# Given the string representation of a location, retrieve the numeric ID
def ap_location_name_to_id(location_name: Union[str, ToontownLocationName]) -> int:
    for i, loc in enumerate(LOCATION_DEFINITIONS):
        if (type(location_name) is str and loc.name.value == location_name) or \
           (type(location_name) is ToontownLocationName and loc.name == location_name):
            return loc.unique_id
    raise Exception("AP location could not be found")


# Given a Zone ID, give the ID of an AP location award the player.
# returns -1 if this isn't a zone we have to worry about
def get_zone_discovery_id(zoneId: int) -> int:

    pgZone = ZoneUtil.getHoodId(zoneId)

    ZONE_TO_LOCATION = {
        ToontownGlobals.ToontownCentral: ToontownLocationName.DISCOVER_TTC.value,
        ToontownGlobals.DonaldsDock: ToontownLocationName.DISCOVER_DD.value,
        ToontownGlobals.DaisyGardens: ToontownLocationName.DISCOVER_DG.value,
        ToontownGlobals.MinniesMelodyland: ToontownLocationName.DISCOVER_MML.value,
        ToontownGlobals.TheBrrrgh: ToontownLocationName.DISCOVER_TB.value,
        ToontownGlobals.DonaldsDreamland: ToontownLocationName.DISCOVER_DDL.value,

        ToontownGlobals.GoofySpeedway: ToontownLocationName.DISCOVER_GS.value,
        ToontownGlobals.OutdoorZone: ToontownLocationName.DISCOVER_AA.value,

        ToontownGlobals.SellbotHQ: ToontownLocationName.DISCOVER_SBHQ.value,
        ToontownGlobals.CashbotHQ: ToontownLocationName.DISCOVER_CBHQ.value,
        ToontownGlobals.LawbotHQ: ToontownLocationName.DISCOVER_LBHQ.value,
        ToontownGlobals.BossbotHQ: ToontownLocationName.DISCOVER_BBHQ.value,
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
        ToontownGlobals.SellbotFactoryInt: ToontownLocationName.CLEAR_FRONT_FACTORY.value,
        ToontownGlobals.SellbotFactoryIntS: ToontownLocationName.CLEAR_SIDE_FACTORY.value,

        ToontownGlobals.CashbotMintIntA: ToontownLocationName.CLEAR_COIN_MINT.value,
        ToontownGlobals.CashbotMintIntB: ToontownLocationName.CLEAR_DOLLAR_MINT.value,
        ToontownGlobals.CashbotMintIntC: ToontownLocationName.CLEAR_BULLION_MINT.value,

        ToontownGlobals.LawbotStageIntA: ToontownLocationName.CLEAR_A_OFFICE.value,
        ToontownGlobals.LawbotStageIntB: ToontownLocationName.CLEAR_B_OFFICE.value,
        ToontownGlobals.LawbotStageIntC: ToontownLocationName.CLEAR_C_OFFICE.value,
        ToontownGlobals.LawbotStageIntD: ToontownLocationName.CLEAR_D_OFFICE.value,

        ToontownGlobals.BossbotCountryClubIntA: ToontownLocationName.CLEAR_FRONT_ONE.value,
        ToontownGlobals.BossbotCountryClubIntB: ToontownLocationName.CLEAR_MIDDLE_TWO.value,
        ToontownGlobals.BossbotCountryClubIntC: ToontownLocationName.CLEAR_BACK_THREE.value,
    }

    loc = FACILITY_LOCATION_CHECKS.get(facility_id)
    if not loc:
        return -1

    return ap_location_name_to_id(loc)


# Given a hood ID, return a list of AP check location names present in that hood
def hood_to_task_locations(hoodId: int):
    return {
        ToontownGlobals.ToontownCentral: TTC_TASK_LOCATIONS,
        ToontownGlobals.DonaldsDock: DD_TASK_LOCATIONS,
        ToontownGlobals.DaisyGardens: DG_TASK_LOCATIONS,
        ToontownGlobals.MinniesMelodyland: MML_TASK_LOCATIONS,
        ToontownGlobals.TheBrrrgh: TB_TASK_LOCATIONS,
        ToontownGlobals.DonaldsDreamland: DDL_TASK_LOCATIONS,
    }.get(hoodId, [])


def track_and_level_to_location(track: int, level: int):
    trackAndLevels = (
        (ToontownLocationName.TOONUP_FEATHER_UNLOCKED.value, ToontownLocationName.TOONUP_MEGAPHONE_UNLOCKED.value, ToontownLocationName.TOONUP_LIPSTICK_UNLOCKED.value, ToontownLocationName.TOONUP_CANE_UNLOCKED.value, ToontownLocationName.TOONUP_PIXIE_UNLOCKED.value, ToontownLocationName.TOONUP_JUGGLING_UNLOCKED.value, ToontownLocationName.TOONUP_HIGHDIVE_UNLOCKED.value),
        (ToontownLocationName.TRAP_BANANA_UNLOCKED.value, ToontownLocationName.TRAP_RAKE_UNLOCKED.value, ToontownLocationName.TRAP_MARBLES_UNLOCKED.value, ToontownLocationName.TRAP_QUICKSAND_UNLOCKED.value, ToontownLocationName.TRAP_TRAPDOOR_UNLOCKED.value, ToontownLocationName.TRAP_TNT_UNLOCKED.value, ToontownLocationName.TRAP_TRAIN_UNLOCKED.value),
        (ToontownLocationName.LURE_ONEBILL_UNLOCKED.value, ToontownLocationName.LURE_SMALLMAGNET_UNLOCKED.value, ToontownLocationName.LURE_FIVEBILL_UNLOCKED.value, ToontownLocationName.LURE_BIGMAGNET_UNLOCKED.value, ToontownLocationName.LURE_TENBILL_UNLOCKED.value, ToontownLocationName.LURE_HYPNO_UNLOCKED.value, ToontownLocationName.LURE_PRESENTATION_UNLOCKED.value),
        (ToontownLocationName.SOUND_BIKEHORN_UNLOCKED.value, ToontownLocationName.SOUND_WHISTLE_UNLOCKED.value, ToontownLocationName.SOUND_BUGLE_UNLOCKED.value, ToontownLocationName.SOUND_AOOGAH_UNLOCKED.value, ToontownLocationName.SOUND_TRUNK_UNLOCKED.value, ToontownLocationName.SOUND_FOG_UNLOCKED.value, ToontownLocationName.SOUND_OPERA_UNLOCKED.value),
        (ToontownLocationName.THROW_CUPCAKE_UNLOCKED.value, ToontownLocationName.THROW_FRUITPIESLICE_UNLOCKED.value, ToontownLocationName.THROW_CREAMPIESLICE_UNLOCKED.value, ToontownLocationName.THROW_WHOLEFRUIT_UNLOCKED.value, ToontownLocationName.THROW_WHOLECREAM_UNLOCKED.value, ToontownLocationName.THROW_CAKE_UNLOCKED.value, ToontownLocationName.THROW_WEDDING_UNLOCKED.value),
        (ToontownLocationName.SQUIRT_SQUIRTFLOWER_UNLOCKED.value, ToontownLocationName.SQUIRT_GLASS_UNLOCKED.value, ToontownLocationName.SQUIRT_SQUIRTGUN_UNLOCKED.value, ToontownLocationName.SQUIRT_SELTZER_UNLOCKED.value, ToontownLocationName.SQUIRT_HOSE_UNLOCKED.value, ToontownLocationName.SQUIRT_CLOUD_UNLOCKED.value, ToontownLocationName.SQUIRT_GEYSER_UNLOCKED.value),
        (ToontownLocationName.DROP_FLOWERPOT_UNLOCKED.value, ToontownLocationName.DROP_SANDBAG_UNLOCKED.value, ToontownLocationName.DROP_ANVIL_UNLOCKED.value, ToontownLocationName.DROP_BIGWEIGHT_UNLOCKED.value, ToontownLocationName.DROP_SAFE_UNLOCKED.value, ToontownLocationName.DROP_PIANO_UNLOCKED.value, ToontownLocationName.DROP_BOAT_UNLOCKED.value),
    )
    return trackAndLevels[track][level]
