from enum import IntEnum
from typing import Optional, List, Set

from BaseClasses import Location, Region, LocationProgressType

# Fill in if some items need more context
LOCATION_DESCRIPTIONS = {

}


class ToontownLocationType(IntEnum):
    BASE = 1  # Stuff that should always be included in the base pool of locations
    GALLERY = 2  # Locations for discovering cogs in the gallery
    FACILITIES = 3  # Locations for clearing facilities
    BOSSES = 4  # Locations for clearing bosses
    FISHING = 5  # Locations for fishing trophies
    DISCOVER_PLAYGROUND = 6  # Locations for discovering playgrounds

    STARTER = 7  # Location that is considered a "starting" check on login, typically we force checks here


class ToontownLocationDefinition:
    """
    Define Locations to be registered as "checks" in this world.

    unique_name will be used as the name shown in game and for others
    classification is the type of location it is to be used for the placement algorithm

    """

    def __init__(self, unique_name: str, unique_id: int, location_type: ToontownLocationType = ToontownLocationType.BASE,
                 classification: LocationProgressType = LocationProgressType.DEFAULT):
        self.unique_name: str = unique_name
        self.unique_id: int = unique_id
        self.location_type: ToontownLocationType = location_type
        self.classification: LocationProgressType = classification


# Name of every location as a string for easy access
STARTING_NEW_GAME_LOCATION = "Create a Toon (Create a Toon)"
STARTING_TRACK_ONE_LOCATION = "Starter Track #1 (Create a Toon)"
STARTING_TRACK_TWO_LOCATION = "Starter Track #2 (Create a Toon)"

COLD_CALLER_DEFEATED_LOCATION = "Cog Gallery (Cold Caller)"
SHORT_CHANGE_DEFEATED_LOCATION = "Cog Gallery (Short Change)"
BOTTOM_FEEDER_DEFEATED_LOCATION = "Cog Gallery (Bottom Feeder)"
FLUNKY_DEFEATED_LOCATION = "Cog Gallery (Flunky)"

TELEMARKETER_DEFEATED_LOCATION = "Cog Gallery (Telemarketer)"
PENNY_PINCHER_DEFEATED_LOCATION = "Cog Gallery (Penny Pincher)"
BLOODSUCKER_DEFEATED_LOCATION = "Cog Gallery (Bloodsucker)"
PENCIL_PUSHER_DEFEATED_LOCATION = "Cog Gallery (Pencil Pusher)"

NAME_DROPPER_DEFEATED_LOCATION = "Cog Gallery (Name Dropper)"
TIGHTWAD_DEFEATED_LOCATION = "Cog Gallery (Tightwad)"
DOUBLE_TALKER_DEFEATED_LOCATION = "Cog Gallery (Double Talker)"
YESMAN_DEFEATED_LOCATION = "Cog Gallery (Yesman)"

GLAD_HANDER_DEFEATED_LOCATION = "Cog Gallery (Glad Hander)"
BEAN_COUNTER_DEFEATED_LOCATION = "Cog Gallery (Bean Counter)"
AMBULANCE_CHASER_DEFEATED_LOCATION = "Cog Gallery (Ambulance Chaser)"
MICROMANAGER_DEFEATED_LOCATION = "Cog Gallery (Micromanager)"

MOVER_AND_SHAKER_DEFEATED_LOCATION = "Cog Gallery (Mover and Shaker)"
NUMBER_CRUNCHER_DEFEATED_LOCATION = "Cog Gallery (Number Cruncher)"
BACKSTABBER_DEFEATED_LOCATION = "Cog Gallery (Backstabber)"
DOWNSIZER_DEFEATED_LOCATION = "Cog Gallery (Downsizer)"

TWO_FACE_DEFEATED_LOCATION = "Cog Gallery (Two Face)"
MONEY_BAGS_DEFEATED_LOCATION = "Cog Gallery (Money Bags)"
SPIN_DOCTOR_DEFEATED_LOCATION = "Cog Gallery (Spin Doctor)"
HEAD_HUNTER_DEFEATED_LOCATION = "Cog Gallery (Head Hunter)"

MINGLER_DEFEATED_LOCATION = "Cog Gallery (Mingler)"
LOAN_SHARK_DEFEATED_LOCATION = "Cog Gallery (Loan Shark)"
LEGAL_EAGLE_DEFEATED_LOCATION = "Cog Gallery (Legal Eagle)"
CORPORATE_RAIDER_DEFEATED_LOCATION = "Cog Gallery (Corporate Raider)"

MR_HOLLYWOOD_DEFEATED_LOCATION = "Cog Gallery (Mr. Hollywood)"
ROBBER_BARRON_DEFEATED_LOCATION = "Cog Gallery (Robber Baron)"
BIG_WIG_DEFEATED_LOCATION = "Cog Gallery (Big Wig)"
BIG_CHEESE_DEFEATED_LOCATION = "Cog Gallery (Big Cheese)"

FISHING_10_SPECIES = "(Fishing) 10 Species Caught Trophy"
FISHING_20_SPECIES = "(Fishing) 20 Species Caught Trophy"
FISHING_30_SPECIES = "(Fishing) 30 Species Caught Trophy"
FISHING_40_SPECIES = "(Fishing) 40 Species Caught Trophy"
FISHING_50_SPECIES = "(Fishing) 50 Species Caught Trophy"
FISHING_60_SPECIES = "(Fishing) 60 Species Caught Trophy"
FISHING_COMPLETE_ALBUM = "(Fishing) All 70 Species Caught Trophy"

TOONTOWN_CENTRAL_TASK_1 = "Toontown Central Task #1"
TOONTOWN_CENTRAL_TASK_2 = "Toontown Central Task #2"
TOONTOWN_CENTRAL_TASK_3 = "Toontown Central Task #3"
TOONTOWN_CENTRAL_TASK_4 = "Toontown Central Task #4"
TOONTOWN_CENTRAL_TASK_5 = "Toontown Central Task #5"
TOONTOWN_CENTRAL_TASK_6 = "Toontown Central Task #6"
TOONTOWN_CENTRAL_TASK_7 = "Toontown Central Task #7"
TOONTOWN_CENTRAL_TASK_8 = "Toontown Central Task #8"
TOONTOWN_CENTRAL_TASK_9 = "Toontown Central Task #9"
TOONTOWN_CENTRAL_TASK_10 = "Toontown Central Task #10"
TOONTOWN_CENTRAL_TASK_11 = "Toontown Central Task #11"
TOONTOWN_CENTRAL_TASK_12 = "Toontown Central Task #12"

DONALDS_DOCK_TASK_1 = "Donald's Dock Task #1"
DONALDS_DOCK_TASK_2 = "Donald's Dock Task #2"
DONALDS_DOCK_TASK_3 = "Donald's Dock Task #3"
DONALDS_DOCK_TASK_4 = "Donald's Dock Task #4"
DONALDS_DOCK_TASK_5 = "Donald's Dock Task #5"
DONALDS_DOCK_TASK_6 = "Donald's Dock Task #6"
DONALDS_DOCK_TASK_7 = "Donald's Dock Task #7"
DONALDS_DOCK_TASK_8 = "Donald's Dock Task #8"
DONALDS_DOCK_TASK_9 = "Donald's Dock Task #9"
DONALDS_DOCK_TASK_10 = "Donald's Dock Task #10"
DONALDS_DOCK_TASK_11 = "Donald's Dock Task #11"
DONALDS_DOCK_TASK_12 = "Donald's Dock Task #12"

DAISYS_GARDENS_TASK_1 = "Daisy's Gardens Task #1"
DAISYS_GARDENS_TASK_2 = "Daisy's Gardens Task #2"
DAISYS_GARDENS_TASK_3 = "Daisy's Gardens Task #3"
DAISYS_GARDENS_TASK_4 = "Daisy's Gardens Task #4"
DAISYS_GARDENS_TASK_5 = "Daisy's Gardens Task #5"
DAISYS_GARDENS_TASK_6 = "Daisy's Gardens Task #6"
DAISYS_GARDENS_TASK_7 = "Daisy's Gardens Task #7"
DAISYS_GARDENS_TASK_8 = "Daisy's Gardens Task #8"
DAISYS_GARDENS_TASK_9 = "Daisy's Gardens Task #9"
DAISYS_GARDENS_TASK_10 = "Daisy's Gardens Task #10"
DAISYS_GARDENS_TASK_11 = "Daisy's Gardens Task #11"
DAISYS_GARDENS_TASK_12 = "Daisy's Gardens Task #12"

MINNIES_MELODYLAND_TASK_1 = "Minnie's Melodyland Task #1"
MINNIES_MELODYLAND_TASK_2 = "Minnie's Melodyland Task #2"
MINNIES_MELODYLAND_TASK_3 = "Minnie's Melodyland Task #3"
MINNIES_MELODYLAND_TASK_4 = "Minnie's Melodyland Task #4"
MINNIES_MELODYLAND_TASK_5 = "Minnie's Melodyland Task #5"
MINNIES_MELODYLAND_TASK_6 = "Minnie's Melodyland Task #6"
MINNIES_MELODYLAND_TASK_7 = "Minnie's Melodyland Task #7"
MINNIES_MELODYLAND_TASK_8 = "Minnie's Melodyland Task #8"
MINNIES_MELODYLAND_TASK_9 = "Minnie's Melodyland Task #9"
MINNIES_MELODYLAND_TASK_10 = "Minnie's Melodyland Task #10"
MINNIES_MELODYLAND_TASK_11 = "Minnie's Melodyland Task #11"
MINNIES_MELODYLAND_TASK_12 = "Minnie's Melodyland Task #12"

THE_BRRRGH_TASK_1 = "The Brrrgh Task #1"
THE_BRRRGH_TASK_2 = "The Brrrgh Task #2"
THE_BRRRGH_TASK_3 = "The Brrrgh Task #3"
THE_BRRRGH_TASK_4 = "The Brrrgh Task #4"
THE_BRRRGH_TASK_5 = "The Brrrgh Task #5"
THE_BRRRGH_TASK_6 = "The Brrrgh Task #6"
THE_BRRRGH_TASK_7 = "The Brrrgh Task #7"
THE_BRRRGH_TASK_8 = "The Brrrgh Task #8"
THE_BRRRGH_TASK_9 = "The Brrrgh Task #9"
THE_BRRRGH_TASK_10 = "The Brrrgh Task #10"
THE_BRRRGH_TASK_11 = "The Brrrgh Task #11"
THE_BRRRGH_TASK_12 = "The Brrrgh Task #12"

DONALDS_DREAMLAND_TASK_1 = "Donald's Dreamland Task #1"
DONALDS_DREAMLAND_TASK_2 = "Donald's Dreamland Task #2"
DONALDS_DREAMLAND_TASK_3 = "Donald's Dreamland Task #3"
DONALDS_DREAMLAND_TASK_4 = "Donald's Dreamland Task #4"
DONALDS_DREAMLAND_TASK_5 = "Donald's Dreamland Task #5"
DONALDS_DREAMLAND_TASK_6 = "Donald's Dreamland Task #6"
DONALDS_DREAMLAND_TASK_7 = "Donald's Dreamland Task #7"
DONALDS_DREAMLAND_TASK_8 = "Donald's Dreamland Task #8"
DONALDS_DREAMLAND_TASK_9 = "Donald's Dreamland Task #9"
DONALDS_DREAMLAND_TASK_10 = "Donald's Dreamland Task #10"
DONALDS_DREAMLAND_TASK_11 = "Donald's Dreamland Task #11"
DONALDS_DREAMLAND_TASK_12 = "Donald's Dreamland Task #12"

DISCOVER_TTC = "Discover Toontown Central"
DISCOVER_DD = "Discover Donald's Dock"
DISCOVER_DG = "Discover Daisy's Gardens"
DISCOVER_MM = "Discover Minnie's Melodyland"
DISCOVER_TB = "Discover The Brrrgh"
DISCOVER_DDL = "Discover Donald's Dreamland"

DISCOVER_SBHQ = "Discover Sellbot HQ"
DISCOVER_CBHQ = "Discover Cashbot HQ"
DISCOVER_LBHQ = "Discover Lawbot HQ"
DISCOVER_BBHQ = "Discover Bossbot HQ"

CLEAR_FRONT_FACTORY = "Front Factory Cleared"
CLEAR_SIDE_FACTORY = "Side Factory Cleared"

CLEAR_COIN_MINT = "Coin Mint Cleared"
CLEAR_DOLLAR_MINT = "Dollar Mint Cleared"
CLEAR_BULLION_MINT = "Bullion Mint Cleared"

CLEAR_A_OFFICE = "A Office Cleared"
CLEAR_B_OFFICE = "B Office Cleared"
CLEAR_C_OFFICE = "C Office Cleared"
CLEAR_D_OFFICE = "D Office Cleared"

CLEAR_FRONT_THREE = "Front One Cleared"
CLEAR_MIDDLE_THREE = "Middle Two Cleared"
CLEAR_BACK_THREE = "Back Three Cleared"

CLEAR_VP = "Clear VP"
SELLBOT_PROOF = "Sellbot Proof"

CLEAR_CFO = "Clear CFO"
CASHBOT_PROOF = "Cashbot Proof"

CLEAR_CJ = "Clear CJ"
LAWBOT_PROOF = "Lawbot Proof"

CLEAR_CEO = "Clear CEO"
BOSSBOT_PROOF = "Bossbot Proof"

CLEAR_BOSSES = [CLEAR_VP, CLEAR_CFO, CLEAR_CJ, CLEAR_CEO]
ALL_BOSS_PROOFS = [SELLBOT_PROOF, CASHBOT_PROOF, LAWBOT_PROOF, BOSSBOT_PROOF]

SAVED_TOONTOWN = "Save Toontown"

# Used to offset all location ids to be compatible in the multiworld
BASE_ID = 0x501100

# Only define locations here that our game needs to be aware of (not events)
LIST_OF_LOCATION_DEFINITIONS: Set[ToontownLocationDefinition] = {

    # Checks for simply logging in the game
    ToontownLocationDefinition(STARTING_NEW_GAME_LOCATION, BASE_ID-3, location_type=ToontownLocationType.STARTER),
    ToontownLocationDefinition(STARTING_TRACK_ONE_LOCATION, BASE_ID-2, location_type=ToontownLocationType.STARTER),
    ToontownLocationDefinition(STARTING_TRACK_TWO_LOCATION, BASE_ID-1, location_type=ToontownLocationType.STARTER),

    # Cog Gallery Discoveries (32)
    ToontownLocationDefinition(COLD_CALLER_DEFEATED_LOCATION, BASE_ID+0, location_type=ToontownLocationType.GALLERY),
    ToontownLocationDefinition(SHORT_CHANGE_DEFEATED_LOCATION, BASE_ID+1, location_type=ToontownLocationType.GALLERY),
    ToontownLocationDefinition(BOTTOM_FEEDER_DEFEATED_LOCATION, BASE_ID+2, location_type=ToontownLocationType.GALLERY),
    ToontownLocationDefinition(FLUNKY_DEFEATED_LOCATION, BASE_ID+3, location_type=ToontownLocationType.GALLERY),

    ToontownLocationDefinition(TELEMARKETER_DEFEATED_LOCATION, BASE_ID+4, location_type=ToontownLocationType.GALLERY),
    ToontownLocationDefinition(PENNY_PINCHER_DEFEATED_LOCATION, BASE_ID+5, location_type=ToontownLocationType.GALLERY),
    ToontownLocationDefinition(BLOODSUCKER_DEFEATED_LOCATION, BASE_ID+6, location_type=ToontownLocationType.GALLERY),
    ToontownLocationDefinition(PENCIL_PUSHER_DEFEATED_LOCATION, BASE_ID+7, location_type=ToontownLocationType.GALLERY),

    ToontownLocationDefinition(NAME_DROPPER_DEFEATED_LOCATION, BASE_ID+8, location_type=ToontownLocationType.GALLERY),
    ToontownLocationDefinition(TIGHTWAD_DEFEATED_LOCATION, BASE_ID+9, location_type=ToontownLocationType.GALLERY),
    ToontownLocationDefinition(DOUBLE_TALKER_DEFEATED_LOCATION, BASE_ID+10, location_type=ToontownLocationType.GALLERY),
    ToontownLocationDefinition(YESMAN_DEFEATED_LOCATION, BASE_ID+11, location_type=ToontownLocationType.GALLERY),

    ToontownLocationDefinition(GLAD_HANDER_DEFEATED_LOCATION, BASE_ID+12, location_type=ToontownLocationType.GALLERY),
    ToontownLocationDefinition(BEAN_COUNTER_DEFEATED_LOCATION, BASE_ID+13, location_type=ToontownLocationType.GALLERY),
    ToontownLocationDefinition(AMBULANCE_CHASER_DEFEATED_LOCATION, BASE_ID+14, location_type=ToontownLocationType.GALLERY),
    ToontownLocationDefinition(MICROMANAGER_DEFEATED_LOCATION, BASE_ID+15, location_type=ToontownLocationType.GALLERY),

    ToontownLocationDefinition(MOVER_AND_SHAKER_DEFEATED_LOCATION, BASE_ID+16, location_type=ToontownLocationType.GALLERY),
    ToontownLocationDefinition(NUMBER_CRUNCHER_DEFEATED_LOCATION, BASE_ID+17, location_type=ToontownLocationType.GALLERY),
    ToontownLocationDefinition(BACKSTABBER_DEFEATED_LOCATION, BASE_ID+18, location_type=ToontownLocationType.GALLERY),
    ToontownLocationDefinition(DOWNSIZER_DEFEATED_LOCATION, BASE_ID+19, location_type=ToontownLocationType.GALLERY),

    ToontownLocationDefinition(TWO_FACE_DEFEATED_LOCATION, BASE_ID+20, location_type=ToontownLocationType.GALLERY),
    ToontownLocationDefinition(MONEY_BAGS_DEFEATED_LOCATION, BASE_ID+21, location_type=ToontownLocationType.GALLERY),
    ToontownLocationDefinition(SPIN_DOCTOR_DEFEATED_LOCATION, BASE_ID+22, location_type=ToontownLocationType.GALLERY),
    ToontownLocationDefinition(HEAD_HUNTER_DEFEATED_LOCATION, BASE_ID+23, location_type=ToontownLocationType.GALLERY),

    ToontownLocationDefinition(MINGLER_DEFEATED_LOCATION, BASE_ID+24, location_type=ToontownLocationType.GALLERY),
    ToontownLocationDefinition(LOAN_SHARK_DEFEATED_LOCATION, BASE_ID+25, location_type=ToontownLocationType.GALLERY),
    ToontownLocationDefinition(LEGAL_EAGLE_DEFEATED_LOCATION, BASE_ID+26, location_type=ToontownLocationType.GALLERY),
    ToontownLocationDefinition(CORPORATE_RAIDER_DEFEATED_LOCATION, BASE_ID+27, location_type=ToontownLocationType.GALLERY),

    ToontownLocationDefinition(MR_HOLLYWOOD_DEFEATED_LOCATION, BASE_ID+28, location_type=ToontownLocationType.GALLERY),
    ToontownLocationDefinition(ROBBER_BARRON_DEFEATED_LOCATION, BASE_ID+29, location_type=ToontownLocationType.GALLERY),
    ToontownLocationDefinition(BIG_WIG_DEFEATED_LOCATION, BASE_ID+30, location_type=ToontownLocationType.GALLERY),
    ToontownLocationDefinition(BIG_CHEESE_DEFEATED_LOCATION, BASE_ID+31, location_type=ToontownLocationType.GALLERY),

    # Fishing Trophies (7)
    ToontownLocationDefinition(FISHING_10_SPECIES, BASE_ID+32, location_type=ToontownLocationType.FISHING),
    ToontownLocationDefinition(FISHING_20_SPECIES, BASE_ID+33, location_type=ToontownLocationType.FISHING),
    ToontownLocationDefinition(FISHING_30_SPECIES, BASE_ID+34, location_type=ToontownLocationType.FISHING),
    ToontownLocationDefinition(FISHING_40_SPECIES, BASE_ID+35, location_type=ToontownLocationType.FISHING),
    ToontownLocationDefinition(FISHING_50_SPECIES, BASE_ID+36, location_type=ToontownLocationType.FISHING),
    ToontownLocationDefinition(FISHING_60_SPECIES, BASE_ID+37, location_type=ToontownLocationType.FISHING),
    ToontownLocationDefinition(FISHING_COMPLETE_ALBUM, BASE_ID+38, location_type=ToontownLocationType.FISHING),

    # TTC Tasks (12)
    ToontownLocationDefinition(TOONTOWN_CENTRAL_TASK_1, BASE_ID+39),
    ToontownLocationDefinition(TOONTOWN_CENTRAL_TASK_2, BASE_ID+40),
    ToontownLocationDefinition(TOONTOWN_CENTRAL_TASK_3, BASE_ID+41),
    ToontownLocationDefinition(TOONTOWN_CENTRAL_TASK_4, BASE_ID+42),
    ToontownLocationDefinition(TOONTOWN_CENTRAL_TASK_5, BASE_ID+43),
    ToontownLocationDefinition(TOONTOWN_CENTRAL_TASK_6, BASE_ID+44),
    ToontownLocationDefinition(TOONTOWN_CENTRAL_TASK_7, BASE_ID+45),
    ToontownLocationDefinition(TOONTOWN_CENTRAL_TASK_8, BASE_ID+46),
    ToontownLocationDefinition(TOONTOWN_CENTRAL_TASK_9, BASE_ID+47),
    ToontownLocationDefinition(TOONTOWN_CENTRAL_TASK_10, BASE_ID+48),
    ToontownLocationDefinition(TOONTOWN_CENTRAL_TASK_11, BASE_ID+49),
    ToontownLocationDefinition(TOONTOWN_CENTRAL_TASK_12, BASE_ID+50),

    # DD Tasks (12)
    ToontownLocationDefinition(DONALDS_DOCK_TASK_1, BASE_ID+51),
    ToontownLocationDefinition(DONALDS_DOCK_TASK_2, BASE_ID+52),
    ToontownLocationDefinition(DONALDS_DOCK_TASK_3, BASE_ID+53),
    ToontownLocationDefinition(DONALDS_DOCK_TASK_4, BASE_ID+54),
    ToontownLocationDefinition(DONALDS_DOCK_TASK_5, BASE_ID+55),
    ToontownLocationDefinition(DONALDS_DOCK_TASK_6, BASE_ID+56),
    ToontownLocationDefinition(DONALDS_DOCK_TASK_7, BASE_ID+57),
    ToontownLocationDefinition(DONALDS_DOCK_TASK_8, BASE_ID+58),
    ToontownLocationDefinition(DONALDS_DOCK_TASK_9, BASE_ID+59),
    ToontownLocationDefinition(DONALDS_DOCK_TASK_10, BASE_ID+60),
    ToontownLocationDefinition(DONALDS_DOCK_TASK_11, BASE_ID+61),
    ToontownLocationDefinition(DONALDS_DOCK_TASK_12, BASE_ID+62),

    # DG Tasks (12)
    ToontownLocationDefinition(DAISYS_GARDENS_TASK_1, BASE_ID+63),
    ToontownLocationDefinition(DAISYS_GARDENS_TASK_2, BASE_ID+64),
    ToontownLocationDefinition(DAISYS_GARDENS_TASK_3, BASE_ID+65),
    ToontownLocationDefinition(DAISYS_GARDENS_TASK_4, BASE_ID+66),
    ToontownLocationDefinition(DAISYS_GARDENS_TASK_5, BASE_ID+67),
    ToontownLocationDefinition(DAISYS_GARDENS_TASK_6, BASE_ID+68),
    ToontownLocationDefinition(DAISYS_GARDENS_TASK_7, BASE_ID+69),
    ToontownLocationDefinition(DAISYS_GARDENS_TASK_8, BASE_ID+70),
    ToontownLocationDefinition(DAISYS_GARDENS_TASK_9, BASE_ID+71),
    ToontownLocationDefinition(DAISYS_GARDENS_TASK_10, BASE_ID+72),
    ToontownLocationDefinition(DAISYS_GARDENS_TASK_11, BASE_ID+73),
    ToontownLocationDefinition(DAISYS_GARDENS_TASK_12, BASE_ID+74),

    # MM Tasks (12)
    ToontownLocationDefinition(MINNIES_MELODYLAND_TASK_1, BASE_ID+75),
    ToontownLocationDefinition(MINNIES_MELODYLAND_TASK_2, BASE_ID+76),
    ToontownLocationDefinition(MINNIES_MELODYLAND_TASK_3, BASE_ID+77),
    ToontownLocationDefinition(MINNIES_MELODYLAND_TASK_4, BASE_ID+78),
    ToontownLocationDefinition(MINNIES_MELODYLAND_TASK_5, BASE_ID+79),
    ToontownLocationDefinition(MINNIES_MELODYLAND_TASK_6, BASE_ID+80),
    ToontownLocationDefinition(MINNIES_MELODYLAND_TASK_7, BASE_ID+81),
    ToontownLocationDefinition(MINNIES_MELODYLAND_TASK_8, BASE_ID+82),
    ToontownLocationDefinition(MINNIES_MELODYLAND_TASK_9, BASE_ID+83),
    ToontownLocationDefinition(MINNIES_MELODYLAND_TASK_10, BASE_ID+84),
    ToontownLocationDefinition(MINNIES_MELODYLAND_TASK_11, BASE_ID+85),
    ToontownLocationDefinition(MINNIES_MELODYLAND_TASK_12, BASE_ID+86),

    # TB Tasks (12)
    ToontownLocationDefinition(THE_BRRRGH_TASK_1, BASE_ID+87),
    ToontownLocationDefinition(THE_BRRRGH_TASK_2, BASE_ID+88),
    ToontownLocationDefinition(THE_BRRRGH_TASK_3, BASE_ID+89),
    ToontownLocationDefinition(THE_BRRRGH_TASK_4, BASE_ID+90),
    ToontownLocationDefinition(THE_BRRRGH_TASK_5, BASE_ID+91),
    ToontownLocationDefinition(THE_BRRRGH_TASK_6, BASE_ID+92),
    ToontownLocationDefinition(THE_BRRRGH_TASK_7, BASE_ID+93),
    ToontownLocationDefinition(THE_BRRRGH_TASK_8, BASE_ID+94),
    ToontownLocationDefinition(THE_BRRRGH_TASK_9, BASE_ID+95),
    ToontownLocationDefinition(THE_BRRRGH_TASK_10, BASE_ID+96),
    ToontownLocationDefinition(THE_BRRRGH_TASK_11, BASE_ID+97),
    ToontownLocationDefinition(THE_BRRRGH_TASK_12, BASE_ID+98),

    # DDL Tasks (12)
    ToontownLocationDefinition(DONALDS_DREAMLAND_TASK_1, BASE_ID+99),
    ToontownLocationDefinition(DONALDS_DREAMLAND_TASK_2, BASE_ID+100),
    ToontownLocationDefinition(DONALDS_DREAMLAND_TASK_3, BASE_ID+101),
    ToontownLocationDefinition(DONALDS_DREAMLAND_TASK_4, BASE_ID+103),
    ToontownLocationDefinition(DONALDS_DREAMLAND_TASK_5, BASE_ID+104),
    ToontownLocationDefinition(DONALDS_DREAMLAND_TASK_6, BASE_ID+105),
    ToontownLocationDefinition(DONALDS_DREAMLAND_TASK_7, BASE_ID+106),
    ToontownLocationDefinition(DONALDS_DREAMLAND_TASK_8, BASE_ID+107),
    ToontownLocationDefinition(DONALDS_DREAMLAND_TASK_9, BASE_ID+108),
    ToontownLocationDefinition(DONALDS_DREAMLAND_TASK_10, BASE_ID+109),
    ToontownLocationDefinition(DONALDS_DREAMLAND_TASK_11, BASE_ID+110),
    ToontownLocationDefinition(DONALDS_DREAMLAND_TASK_12, BASE_ID+111),

    # Visit HQs (4)
    ToontownLocationDefinition(DISCOVER_SBHQ, BASE_ID+112),
    ToontownLocationDefinition(DISCOVER_CBHQ, BASE_ID+113),
    ToontownLocationDefinition(DISCOVER_LBHQ, BASE_ID+114),
    ToontownLocationDefinition(DISCOVER_BBHQ, BASE_ID+115),

    # Factory Completions (2)
    ToontownLocationDefinition(CLEAR_FRONT_FACTORY, BASE_ID+116, location_type=ToontownLocationType.FACILITIES),
    ToontownLocationDefinition(CLEAR_SIDE_FACTORY, BASE_ID+117, location_type=ToontownLocationType.FACILITIES),

    # Mint Completions (3)
    ToontownLocationDefinition(CLEAR_COIN_MINT, BASE_ID+118, location_type=ToontownLocationType.FACILITIES),
    ToontownLocationDefinition(CLEAR_DOLLAR_MINT, BASE_ID+119, location_type=ToontownLocationType.FACILITIES),
    ToontownLocationDefinition(CLEAR_BULLION_MINT, BASE_ID+120, location_type=ToontownLocationType.FACILITIES),

    # Office Completions (4)
    ToontownLocationDefinition(CLEAR_A_OFFICE, BASE_ID+121, location_type=ToontownLocationType.FACILITIES),
    ToontownLocationDefinition(CLEAR_B_OFFICE, BASE_ID+122, location_type=ToontownLocationType.FACILITIES),
    ToontownLocationDefinition(CLEAR_C_OFFICE, BASE_ID+123, location_type=ToontownLocationType.FACILITIES),
    ToontownLocationDefinition(CLEAR_D_OFFICE, BASE_ID+124, location_type=ToontownLocationType.FACILITIES),

    # Golf Course Completions (3)
    ToontownLocationDefinition(CLEAR_FRONT_THREE, BASE_ID+125, location_type=ToontownLocationType.FACILITIES),
    ToontownLocationDefinition(CLEAR_MIDDLE_THREE, BASE_ID+126, location_type=ToontownLocationType.FACILITIES),
    ToontownLocationDefinition(CLEAR_BACK_THREE, BASE_ID+127, location_type=ToontownLocationType.FACILITIES),

    # VP Victory (2)
    # CFO Victory (2)
    # CJ Victory (2)
    # CEO Victory (2)
    ToontownLocationDefinition(CLEAR_VP, BASE_ID+128, location_type=ToontownLocationType.BOSSES),
    ToontownLocationDefinition(CLEAR_CFO, BASE_ID+129, location_type=ToontownLocationType.BOSSES),
    ToontownLocationDefinition(CLEAR_CJ, BASE_ID+130, location_type=ToontownLocationType.BOSSES),
    ToontownLocationDefinition(CLEAR_CEO, BASE_ID+131, location_type=ToontownLocationType.BOSSES),

    ToontownLocationDefinition(SELLBOT_PROOF, BASE_ID+132, location_type=ToontownLocationType.BOSSES),
    ToontownLocationDefinition(CASHBOT_PROOF, BASE_ID+133, location_type=ToontownLocationType.BOSSES),
    ToontownLocationDefinition(LAWBOT_PROOF, BASE_ID+134, location_type=ToontownLocationType.BOSSES),
    ToontownLocationDefinition(BOSSBOT_PROOF, BASE_ID+135, location_type=ToontownLocationType.BOSSES),

    ToontownLocationDefinition(SAVED_TOONTOWN, BASE_ID+136),

    # Discover Playgrounds
    ToontownLocationDefinition(DISCOVER_TTC, BASE_ID+137, location_type=ToontownLocationType.DISCOVER_PLAYGROUND),
    ToontownLocationDefinition(DISCOVER_DD, BASE_ID+138, location_type=ToontownLocationType.DISCOVER_PLAYGROUND),
    ToontownLocationDefinition(DISCOVER_DG, BASE_ID+139, location_type=ToontownLocationType.DISCOVER_PLAYGROUND),
    ToontownLocationDefinition(DISCOVER_MM, BASE_ID+140, location_type=ToontownLocationType.DISCOVER_PLAYGROUND),
    ToontownLocationDefinition(DISCOVER_TB, BASE_ID+141, location_type=ToontownLocationType.DISCOVER_PLAYGROUND),
    ToontownLocationDefinition(DISCOVER_DDL, BASE_ID+142, location_type=ToontownLocationType.DISCOVER_PLAYGROUND),
}

# Maps Location Definitions by location name -> location definition
LOCATION_DEFINITIONS = {
    loc_def.unique_name: loc_def for loc_def in LIST_OF_LOCATION_DEFINITIONS
}

# Maps Location Definitions by location id -> location definition
ID_TO_LOCATION_DEFINITION = {
    loc_def.unique_id: loc_def for loc_def in LIST_OF_LOCATION_DEFINITIONS
}

LOGIN_LOCATIONS: List[str] = [
    check.unique_name for check in LIST_OF_LOCATION_DEFINITIONS if check.location_type == ToontownLocationType.STARTER
]

GALLERY_LOCATIONS: List[str] = [
    check.unique_name for check in LIST_OF_LOCATION_DEFINITIONS if check.location_type == ToontownLocationType.GALLERY
]

FISHING_LOCATIONS: List[str] = [
    check.unique_name for check in LIST_OF_LOCATION_DEFINITIONS if check.location_type == ToontownLocationType.FISHING
]

DISCOVER_PLAYGROUND_LOCATIONS: List[str] = [
    check.unique_name for check in LIST_OF_LOCATION_DEFINITIONS if check.location_type == ToontownLocationType.DISCOVER_PLAYGROUND
]


TTC_TASK_LOCATIONS = [
    TOONTOWN_CENTRAL_TASK_1,
    TOONTOWN_CENTRAL_TASK_2,
    TOONTOWN_CENTRAL_TASK_3,
    TOONTOWN_CENTRAL_TASK_4,
    TOONTOWN_CENTRAL_TASK_5,
    TOONTOWN_CENTRAL_TASK_6,
    TOONTOWN_CENTRAL_TASK_7,
    TOONTOWN_CENTRAL_TASK_8,
    TOONTOWN_CENTRAL_TASK_9,
    TOONTOWN_CENTRAL_TASK_10,
    TOONTOWN_CENTRAL_TASK_11,
    TOONTOWN_CENTRAL_TASK_12,
]

DD_TASK_LOCATIONS = [
    DONALDS_DOCK_TASK_1,
    DONALDS_DOCK_TASK_2,
    DONALDS_DOCK_TASK_3,
    DONALDS_DOCK_TASK_4,
    DONALDS_DOCK_TASK_5,
    DONALDS_DOCK_TASK_6,
    DONALDS_DOCK_TASK_7,
    DONALDS_DOCK_TASK_8,
    DONALDS_DOCK_TASK_9,
    DONALDS_DOCK_TASK_10,
    DONALDS_DOCK_TASK_11,
    DONALDS_DOCK_TASK_12,
]

DG_TASK_LOCATIONS = [
    DAISYS_GARDENS_TASK_1,
    DAISYS_GARDENS_TASK_2,
    DAISYS_GARDENS_TASK_3,
    DAISYS_GARDENS_TASK_4,
    DAISYS_GARDENS_TASK_5,
    DAISYS_GARDENS_TASK_6,
    DAISYS_GARDENS_TASK_7,
    DAISYS_GARDENS_TASK_8,
    DAISYS_GARDENS_TASK_9,
    DAISYS_GARDENS_TASK_10,
    DAISYS_GARDENS_TASK_11,
    DAISYS_GARDENS_TASK_12,
]

MM_TASK_LOCATIONS = [
    MINNIES_MELODYLAND_TASK_1,
    MINNIES_MELODYLAND_TASK_2,
    MINNIES_MELODYLAND_TASK_3,
    MINNIES_MELODYLAND_TASK_4,
    MINNIES_MELODYLAND_TASK_5,
    MINNIES_MELODYLAND_TASK_6,
    MINNIES_MELODYLAND_TASK_7,
    MINNIES_MELODYLAND_TASK_8,
    MINNIES_MELODYLAND_TASK_9,
    MINNIES_MELODYLAND_TASK_10,
    MINNIES_MELODYLAND_TASK_11,
    MINNIES_MELODYLAND_TASK_12,
]

TB_TASK_LOCATIONS = [
    THE_BRRRGH_TASK_1,
    THE_BRRRGH_TASK_2,
    THE_BRRRGH_TASK_3,
    THE_BRRRGH_TASK_4,
    THE_BRRRGH_TASK_5,
    THE_BRRRGH_TASK_6,
    THE_BRRRGH_TASK_7,
    THE_BRRRGH_TASK_8,
    THE_BRRRGH_TASK_9,
    THE_BRRRGH_TASK_10,
    THE_BRRRGH_TASK_11,
    THE_BRRRGH_TASK_12,
]

DDL_TASK_LOCATIONS = [
    DONALDS_DREAMLAND_TASK_1,
    DONALDS_DREAMLAND_TASK_2,
    DONALDS_DREAMLAND_TASK_3,
    DONALDS_DREAMLAND_TASK_4,
    DONALDS_DREAMLAND_TASK_5,
    DONALDS_DREAMLAND_TASK_6,
    DONALDS_DREAMLAND_TASK_7,
    DONALDS_DREAMLAND_TASK_8,
    DONALDS_DREAMLAND_TASK_9,
    DONALDS_DREAMLAND_TASK_10,
    DONALDS_DREAMLAND_TASK_11,
    DONALDS_DREAMLAND_TASK_12,
]

ALL_TASK_LOCATIONS = (TTC_TASK_LOCATIONS + DD_TASK_LOCATIONS + DG_TASK_LOCATIONS
                      + MM_TASK_LOCATIONS + TB_TASK_LOCATIONS + DDL_TASK_LOCATIONS)


SCOUTING_REQUIRED_LOCATIONS = ALL_TASK_LOCATIONS.copy()


class ToontownLocation(Location):
    game: str = "Toontown"

    def __init__(self, player: int, name: str = "", address: Optional[int] = None,
                 parent: Optional[Region] = None) -> None:
        super().__init__(player, name, address, parent)
        self.event = address is None
