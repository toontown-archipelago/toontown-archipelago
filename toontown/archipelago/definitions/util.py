from toontown.archipelago.definitions import locations


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
