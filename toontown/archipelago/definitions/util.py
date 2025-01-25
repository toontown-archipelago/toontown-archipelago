from typing import Union
from apworld.toontown import consts, ToontownLocationName, LOCATION_DEFINITIONS
from apworld.toontown.locations import TTC_TASK_LOCATIONS, DD_TASK_LOCATIONS, DG_TASK_LOCATIONS, MML_TASK_LOCATIONS, \
    TB_TASK_LOCATIONS, DDL_TASK_LOCATIONS, EVENT_DEFINITIONS, ToontownLocationDefinition, get_location_def_from_name
from toontown.shtiker import CogPageGlobals
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

# Given AP location name return the cog code
# Correct this before committing, use `ToontownLocationName`s instead of the raw strings...
def ap_location_to_cog_code(location: str) -> tuple[str, int]:
    return {
        ToontownLocationName.FLUNKY_DEFEATED.value: ('f', CogPageGlobals.COG_COMPLETE1), ToontownLocationName.FLUNKY_MAXED.value: ('f', CogPageGlobals.COG_COMPLETE2),
        ToontownLocationName.PENCIL_PUSHER_DEFEATED.value: ('p', CogPageGlobals.COG_COMPLETE1), ToontownLocationName.PENCIL_PUSHER_MAXED.value: ('p', CogPageGlobals.COG_COMPLETE2),
        ToontownLocationName.YESMAN_DEFEATED.value: ('ym', CogPageGlobals.COG_COMPLETE1), ToontownLocationName.YESMAN_MAXED.value: ('ym', CogPageGlobals.COG_COMPLETE2),
        ToontownLocationName.MICROMANAGER_DEFEATED.value: ('mm', CogPageGlobals.COG_COMPLETE1), ToontownLocationName.MICROMANAGER_MAXED.value: ('mm', CogPageGlobals.COG_COMPLETE2),
        ToontownLocationName.DOWNSIZER_DEFEATED.value: ('ds', CogPageGlobals.COG_COMPLETE1), ToontownLocationName.DOWNSIZER_MAXED.value: ('ds', CogPageGlobals.COG_COMPLETE2),
        ToontownLocationName.HEAD_HUNTER_DEFEATED.value: ('hh', CogPageGlobals.COG_COMPLETE1), ToontownLocationName.HEAD_HUNTER_MAXED.value: ('hh', CogPageGlobals.COG_COMPLETE2),
        ToontownLocationName.CORPORATE_RAIDER_DEFEATED.value: ('cr', CogPageGlobals.COG_COMPLETE1), ToontownLocationName.CORPORATE_RAIDER_MAXED.value: ('cr', CogPageGlobals.COG_COMPLETE2),
        ToontownLocationName.BIG_CHEESE_DEFEATED.value: ('tbc', CogPageGlobals.COG_COMPLETE1), ToontownLocationName.BIG_CHEESE_MAXED.value: ('tbc', CogPageGlobals.COG_COMPLETE2),

        ToontownLocationName.BOTTOM_FEEDER_DEFEATED.value: ('bf', CogPageGlobals.COG_COMPLETE1), ToontownLocationName.BOTTOM_FEEDER_MAXED.value: ('bf', CogPageGlobals.COG_COMPLETE2),
        ToontownLocationName.BLOODSUCKER_DEFEATED.value: ('b', CogPageGlobals.COG_COMPLETE1), ToontownLocationName.BLOODSUCKER_MAXED.value: ('b', CogPageGlobals.COG_COMPLETE2),
        ToontownLocationName.DOUBLE_TALKER_DEFEATED.value: ('dt', CogPageGlobals.COG_COMPLETE1), ToontownLocationName.DOUBLE_TALKER_MAXED.value: ('dt', CogPageGlobals.COG_COMPLETE2),
        ToontownLocationName.AMBULANCE_CHASER_DEFEATED.value: ('ac', CogPageGlobals.COG_COMPLETE1), ToontownLocationName.AMBULANCE_CHASER_MAXED.value: ('ac', CogPageGlobals.COG_COMPLETE2),
        ToontownLocationName.BACKSTABBER_DEFEATED.value: ('bs', CogPageGlobals.COG_COMPLETE1), ToontownLocationName.BACKSTABBER_MAXED.value: ('bs', CogPageGlobals.COG_COMPLETE2),
        ToontownLocationName.SPIN_DOCTOR_DEFEATED.value: ('sd', CogPageGlobals.COG_COMPLETE1), ToontownLocationName.SPIN_DOCTOR_MAXED.value: ('sd', CogPageGlobals.COG_COMPLETE2),
        ToontownLocationName.LEGAL_EAGLE_DEFEATED.value: ('le', CogPageGlobals.COG_COMPLETE1), ToontownLocationName.LEGAL_EAGLE_MAXED.value: ('le', CogPageGlobals.COG_COMPLETE2),
        ToontownLocationName.BIG_WIG_DEFEATED.value: ('bw', CogPageGlobals.COG_COMPLETE1), ToontownLocationName.BIG_WIG_MAXED.value: ('bw', CogPageGlobals.COG_COMPLETE2),

        ToontownLocationName.SHORT_CHANGE_DEFEATED.value: ('sc', CogPageGlobals.COG_COMPLETE1), ToontownLocationName.SHORT_CHANGE_MAXED.value: ('sc', CogPageGlobals.COG_COMPLETE2),
        ToontownLocationName.PENNY_PINCHER_DEFEATED.value: ('pp', CogPageGlobals.COG_COMPLETE1), ToontownLocationName.PENNY_PINCHER_MAXED.value: ('pp', CogPageGlobals.COG_COMPLETE2),
        ToontownLocationName.TIGHTWAD_DEFEATED.value: ('tw', CogPageGlobals.COG_COMPLETE1), ToontownLocationName.TIGHTWAD_MAXED.value: ('tw', CogPageGlobals.COG_COMPLETE2),
        ToontownLocationName.BEAN_COUNTER_DEFEATED.value: ('bc', CogPageGlobals.COG_COMPLETE1), ToontownLocationName.BEAN_COUNTER_MAXED.value: ('bc', CogPageGlobals.COG_COMPLETE2),
        ToontownLocationName.NUMBER_CRUNCHER_DEFEATED.value: ('nc', CogPageGlobals.COG_COMPLETE1), ToontownLocationName.NUMBER_CRUNCHER_MAXED.value: ('nc', CogPageGlobals.COG_COMPLETE2),
        ToontownLocationName.MONEY_BAGS_DEFEATED.value: ('mb', CogPageGlobals.COG_COMPLETE1), ToontownLocationName.MONEY_BAGS_MAXED.value: ('mb', CogPageGlobals.COG_COMPLETE2),
        ToontownLocationName.LOAN_SHARK_DEFEATED.value: ('ls', CogPageGlobals.COG_COMPLETE1), ToontownLocationName.LOAN_SHARK_MAXED.value: ('ls', CogPageGlobals.COG_COMPLETE2),
        ToontownLocationName.ROBBER_BARRON_DEFEATED.value: ('rb', CogPageGlobals.COG_COMPLETE1), ToontownLocationName.ROBBER_BARRON_MAXED.value: ('rb', CogPageGlobals.COG_COMPLETE2),

        ToontownLocationName.COLD_CALLER_DEFEATED.value: ('cc', CogPageGlobals.COG_COMPLETE1), ToontownLocationName.COLD_CALLER_MAXED.value: ('cc', CogPageGlobals.COG_COMPLETE2),
        ToontownLocationName.TELEMARKETER_DEFEATED.value: ('tm', CogPageGlobals.COG_COMPLETE1), ToontownLocationName.TELEMARKETER_MAXED.value: ('tm', CogPageGlobals.COG_COMPLETE2),
        ToontownLocationName.NAME_DROPPER_DEFEATED.value: ('nd', CogPageGlobals.COG_COMPLETE1), ToontownLocationName.NAME_DROPPER_MAXED.value: ('nd', CogPageGlobals.COG_COMPLETE2),
        ToontownLocationName.GLAD_HANDER_DEFEATED.value: ('gh', CogPageGlobals.COG_COMPLETE1), ToontownLocationName.GLAD_HANDER_MAXED.value: ('gh', CogPageGlobals.COG_COMPLETE2),
        ToontownLocationName.MOVER_AND_SHAKER_DEFEATED.value: ('ms', CogPageGlobals.COG_COMPLETE1), ToontownLocationName.MOVER_AND_SHAKER_MAXED.value: ('ms', CogPageGlobals.COG_COMPLETE2),
        ToontownLocationName.TWO_FACE_DEFEATED.value: ('tf', CogPageGlobals.COG_COMPLETE1), ToontownLocationName.TWO_FACE_MAXED.value: ('tf', CogPageGlobals.COG_COMPLETE2),
        ToontownLocationName.MINGLER_DEFEATED.value: ('m', CogPageGlobals.COG_COMPLETE1), ToontownLocationName.MINGLER_MAXED.value: ('m', CogPageGlobals.COG_COMPLETE2),
        ToontownLocationName.MR_HOLLYWOOD_DEFEATED.value: ('mh', CogPageGlobals.COG_COMPLETE1), ToontownLocationName.MR_HOLLYWOOD_MAXED.value: ('mh', CogPageGlobals.COG_COMPLETE2)
    }.get(location, ('', 0))

# Given the string representation of a location, retrieve the numeric ID
def ap_location_name_to_id(location_name: Union[str, ToontownLocationName]) -> int:
    for location_definition in (LOCATION_DEFINITIONS + EVENT_DEFINITIONS):
        if (isinstance(location_name, str) and location_definition.name.value == location_name) or \
           (isinstance(location_name, ToontownLocationName) and location_definition.name == location_name):
            return location_definition.unique_id
    raise KeyError(f"AP location: {location_name}<type={type(location_name)}> is not defined in Location/Event definitions")

# Given a numeric ID, return the string representation of a location
def ap_location_id_to_name(location_id: int) -> str:
    for location_definition in (LOCATION_DEFINITIONS + EVENT_DEFINITIONS):
        if location_definition.unique_id == location_id:
            return location_definition.name.value
    raise KeyError(f"AP location: {location_id}<type={type(location_id)}> is not defined in Location/Event definitions")

# Given an AP ID or NAME, return the definition.
def ap_location_to_definition(location: Union[int, str]) -> ToontownLocationDefinition:
    if isinstance(location, int):
        for location_definition in (LOCATION_DEFINITIONS + EVENT_DEFINITIONS):
            if location_definition.unique_id == location:
                return location_definition
    if isinstance(location, str):
        for location_definition in (LOCATION_DEFINITIONS + EVENT_DEFINITIONS):
            if location_definition.name.value == location:
                return location_definition
    raise KeyError(f"AP location: {location}<type={type(location)}> is not defined in Location/Event definitions")

# Given a Zone ID, give the ID of an AP location award the player.
# returns -1 if this isn't a zone we have to worry about
def get_zone_discovery_id(zoneId: int) -> int:

    pgZone = ZoneUtil.getHoodId(zoneId)

    ZONE_TO_LOCATION = {
        ToontownGlobals.ToontownCentral: ToontownLocationName.TTC_TREASURE_1.value,
        ToontownGlobals.DonaldsDock: ToontownLocationName.DD_TREASURE_1.value,
        ToontownGlobals.DaisyGardens: ToontownLocationName.DG_TREASURE_1.value,
        ToontownGlobals.MinniesMelodyland: ToontownLocationName.MML_TREASURE_1.value,
        ToontownGlobals.TheBrrrgh: ToontownLocationName.TB_TREASURE_1.value,
        ToontownGlobals.DonaldsDreamland: ToontownLocationName.DDL_TREASURE_1.value,

        ToontownGlobals.GoofySpeedway: ToontownLocationName.GS_TREASURE_1.value,
        ToontownGlobals.OutdoorZone: ToontownLocationName.AA_TREASURE_1.value,

        ToontownGlobals.SellbotHQ: ToontownLocationName.SBHQ_TREASURE_1.value,
        ToontownGlobals.CashbotHQ: ToontownLocationName.CBHQ_TREASURE_1.value,
        ToontownGlobals.LawbotHQ: ToontownLocationName.LBHQ_TREASURE_1.value,
        ToontownGlobals.BossbotHQ: ToontownLocationName.BBHQ_TREASURE_1.value,
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
    locs = {
        ToontownGlobals.ToontownCentral: TTC_TASK_LOCATIONS,
        ToontownGlobals.DonaldsDock: DD_TASK_LOCATIONS,
        ToontownGlobals.DaisyGardens: DG_TASK_LOCATIONS,
        ToontownGlobals.MinniesMelodyland: MML_TASK_LOCATIONS,
        ToontownGlobals.TheBrrrgh: TB_TASK_LOCATIONS,
        ToontownGlobals.DonaldsDreamland: DDL_TASK_LOCATIONS,
    }.get(hoodId, [])

    # Because of the way AP is setup, we need to extract the raw string value from the location enums
    ret = []
    for loc in locs:
        ret.append(loc.value)

    return ret


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
