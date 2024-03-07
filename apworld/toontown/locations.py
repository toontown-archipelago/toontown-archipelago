from enum import IntEnum
from typing import Optional, List, Set

from BaseClasses import Location, Region, LocationProgressType
from .locks import LockBase
from .locks.GagFrameQuantityLock import GagFrameQuantityLock
from .locks.GagItemLock import GagItemLock

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
    GAG_TRAINING = 7  # Locations for training gags

    STARTER = 8  # Location that is considered a "starting" check on login, typically we force checks here


class ToontownLocationDefinition:
    """
    Define Locations to be registered as "checks" in this world.

    unique_name will be used as the name shown in game and for others
    classification is the type of location it is to be used for the placement algorithm
    lock is an optional argument that lets you define a lock object that this location is locked behind (i.e. must have some item)

    """

    def __init__(self, unique_name: str, unique_id: int, location_type: ToontownLocationType = ToontownLocationType.BASE,
                 classification: LocationProgressType = LocationProgressType.DEFAULT, lock: LockBase=None):
        self.unique_name: str = unique_name
        self.unique_id: int = unique_id
        self.location_type: ToontownLocationType = location_type
        self.classification: LocationProgressType = classification
        self.lock: LockBase=None

    # Returns True if this location is always accessible
    # Note: regions defined in regions.py can have their own locks as well if this location is contained in one
    def always_unlocked(self) -> bool:
        return self.lock is None


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

COLD_CALLER_MAXED_LOCATION = "Cog Gallery Maxed (Cold Caller)"
SHORT_CHANGE_MAXED_LOCATION = "Cog Gallery Maxed (Short Change)"
BOTTOM_FEEDER_MAXED_LOCATION = "Cog Gallery Maxed (Bottom Feeder)"
FLUNKY_MAXED_LOCATION = "Cog Gallery Maxed (Flunky)"

TELEMARKETER_MAXED_LOCATION = "Cog Gallery Maxed (Telemarketer)"
PENNY_PINCHER_MAXED_LOCATION = "Cog Gallery Maxed (Penny Pincher)"
BLOODSUCKER_MAXED_LOCATION = "Cog Gallery Maxed (Bloodsucker)"
PENCIL_PUSHER_MAXED_LOCATION = "Cog Gallery Maxed (Pencil Pusher)"

NAME_DROPPER_MAXED_LOCATION = "Cog Gallery Maxed (Name Dropper)"
TIGHTWAD_MAXED_LOCATION = "Cog Gallery Maxed (Tightwad)"
DOUBLE_TALKER_MAXED_LOCATION = "Cog Gallery Maxed (Double Talker)"
YESMAN_MAXED_LOCATION = "Cog Gallery Maxed (Yesman)"

GLAD_HANDER_MAXED_LOCATION = "Cog Gallery Maxed (Glad Hander)"
BEAN_COUNTER_MAXED_LOCATION = "Cog Gallery Maxed (Bean Counter)"
AMBULANCE_CHASER_MAXED_LOCATION = "Cog Gallery Maxed (Ambulance Chaser)"
MICROMANAGER_MAXED_LOCATION = "Cog Gallery Maxed (Micromanager)"

MOVER_AND_SHAKER_MAXED_LOCATION = "Cog Gallery Maxed (Mover and Shaker)"
NUMBER_CRUNCHER_MAXED_LOCATION = "Cog Gallery Maxed (Number Cruncher)"
BACKSTABBER_MAXED_LOCATION = "Cog Gallery Maxed (Backstabber)"
DOWNSIZER_MAXED_LOCATION = "Cog Gallery Maxed (Downsizer)"

TWO_FACE_MAXED_LOCATION = "Cog Gallery Maxed (Two Face)"
MONEY_BAGS_MAXED_LOCATION = "Cog Gallery Maxed (Money Bags)"
SPIN_DOCTOR_MAXED_LOCATION = "Cog Gallery Maxed (Spin Doctor)"
HEAD_HUNTER_MAXED_LOCATION = "Cog Gallery Maxed (Head Hunter)"

MINGLER_MAXED_LOCATION = "Cog Gallery Maxed (Mingler)"
LOAN_SHARK_MAXED_LOCATION = "Cog Gallery Maxed (Loan Shark)"
LEGAL_EAGLE_MAXED_LOCATION = "Cog Gallery Maxed (Legal Eagle)"
CORPORATE_RAIDER_MAXED_LOCATION = "Cog Gallery Maxed (Corporate Raider)"

MR_HOLLYWOOD_MAXED_LOCATION = "Cog Gallery Maxed (Mr. Hollywood)"
ROBBER_BARRON_MAXED_LOCATION = "Cog Gallery Maxed (Robber Baron)"
BIG_WIG_MAXED_LOCATION = "Cog Gallery Maxed (Big Wig)"
BIG_CHEESE_MAXED_LOCATION = "Cog Gallery Maxed (Big Cheese)"

TOONUP_FEATHER_UNLOCKED = "Feather Unlocked (Toon-up Training)"
TOONUP_MEGAPHONE_UNLOCKED = "Megaphone Unlocked (Toon-up Training)"
TOONUP_LIPSTICK_UNLOCKED = "Lipstick Unlocked (Toon-up Training)"
TOONUP_CANE_UNLOCKED = "Bamboo Cane Unlocked (Toon-up Training)"
TOONUP_PIXIE_UNLOCKED = "Pixie Dust Unlocked (Toon-up Training)"
TOONUP_JUGGLING_UNLOCKED = "Juggling Cubes Unlocked (Toon-up Training)"
TOONUP_HIGHDIVE_UNLOCKED = "High Dive Unlocked (MAXED Toon-up)"

TRAP_BANANA_UNLOCKED = "Banana Peel Unlocked (Trap Training)"
TRAP_RAKE_UNLOCKED = "Rake Unlocked (Trap Training)"
TRAP_MARBLES_UNLOCKED = "Marbles Unlocked (Trap Training)"
TRAP_QUICKSAND_UNLOCKED = "Quicksand Unlocked (Trap Training)"
TRAP_TRAPDOOR_UNLOCKED = "Trapdoor Unlocked (Trap Training)"
TRAP_TNT_UNLOCKED = "TNT Unlocked (Trap Training)"
TRAP_TRAIN_UNLOCKED = "Railroad Unlocked (MAXED Trap)"

LURE_ONEBILL_UNLOCKED = "$1 Bill Unlocked (Lure Training)"
LURE_SMALLMAGNET_UNLOCKED = "Small Magnet Unlocked (Lure Training)"
LURE_FIVEBILL_UNLOCKED = "$5 Bill Unlocked (Lure Training)"
LURE_BIGMAGNET_UNLOCKED = "Big Magnet Unlocked (Lure Training)"
LURE_TENBILL_UNLOCKED = "$10 Bill Unlocked (Lure Training)"
LURE_HYPNO_UNLOCKED = "Hypno-Goggles Unlocked (Lure Training)"
LURE_PRESENTATION_UNLOCKED = "Presentation Unlocked (MAXED Lure)"

SOUND_BIKEHORN_UNLOCKED = "Bike Horn Unlocked (Sound Training)"
SOUND_WHISTLE_UNLOCKED = "Whistle Unlocked (Sound Training)"
SOUND_BUGLE_UNLOCKED = "Bugle Unlocked (Sound Training)"
SOUND_AOOGAH_UNLOCKED = "Aoogah Unlocked (Sound Training)"
SOUND_TRUNK_UNLOCKED = "Elephant Trunk Unlocked (Sound Training)"
SOUND_FOG_UNLOCKED = "Foghorn Unlocked (Sound Training)"
SOUND_OPERA_UNLOCKED = "Opera Singer Unlocked (MAXED Sound)"

THROW_CUPCAKE_UNLOCKED = "Cupcake Unlocked (Throw Training)"
THROW_FRUITPIESLICE_UNLOCKED = "Fruit Pie Slice Unlocked (Throw Training)"
THROW_CREAMPIESLICE_UNLOCKED = "Cream Pie Slice Unlocked (Throw Training)"
THROW_WHOLEFRUIT_UNLOCKED = "Whole Fruit Pie Unlocked (Throw Training)"
THROW_WHOLECREAM_UNLOCKED = "Whole Cream Pie Unlocked (Throw Training)"
THROW_CAKE_UNLOCKED = "Birthday Cake Unlocked (Throw Training)"
THROW_WEDDING_UNLOCKED = "Wedding Cake Unlocked (MAXED Throw)"

SQUIRT_SQUIRTFLOWER_UNLOCKED = "Squirting Flower Unlocked (Squirt Training)"
SQUIRT_GLASS_UNLOCKED = "Glass of Water Unlocked (Squirt Training)"
SQUIRT_SQUIRTGUN_UNLOCKED = "Squirt Gun Unlocked (Squirt Training)"
SQUIRT_SELTZER_UNLOCKED = "Seltzer Bottle Unlocked (Squirt Training)"
SQUIRT_HOSE_UNLOCKED = "Firehose Unlocked (Squirt Training)"
SQUIRT_CLOUD_UNLOCKED = "Stormcloud Unlocked (Squirt Training)"
SQUIRT_GEYSER_UNLOCKED = "Geyser Unlocked (MAXED Squirt)"

DROP_FLOWERPOT_UNLOCKED = "Flowerpot Unlocked (Drop Training)"
DROP_SANDBAG_UNLOCKED = "Sandbag Unlocked (Drop Training)"
DROP_ANVIL_UNLOCKED = "Anvil Unlocked (Drop Training)"
DROP_BIGWEIGHT_UNLOCKED = "Big Weight Unlocked (Drop Training)"
DROP_SAFE_UNLOCKED = "Safe Unlocked (Drop Training)"
DROP_PIANO_UNLOCKED = "Piano Unlocked (Drop Training)"
DROP_BOAT_UNLOCKED = "Toontanic Unlocked (MAXED Drop)"

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

DAISYS_GARDENS_TASK_1 = "Daisy Gardens Task #1"
DAISYS_GARDENS_TASK_2 = "Daisy Gardens Task #2"
DAISYS_GARDENS_TASK_3 = "Daisy Gardens Task #3"
DAISYS_GARDENS_TASK_4 = "Daisy Gardens Task #4"
DAISYS_GARDENS_TASK_5 = "Daisy Gardens Task #5"
DAISYS_GARDENS_TASK_6 = "Daisy Gardens Task #6"
DAISYS_GARDENS_TASK_7 = "Daisy Gardens Task #7"
DAISYS_GARDENS_TASK_8 = "Daisy Gardens Task #8"
DAISYS_GARDENS_TASK_9 = "Daisy Gardens Task #9"
DAISYS_GARDENS_TASK_10 = "Daisy Gardens Task #10"
DAISYS_GARDENS_TASK_11 = "Daisy Gardens Task #11"
DAISYS_GARDENS_TASK_12 = "Daisy Gardens Task #12"

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
DISCOVER_DG = "Discover Daisy Gardens"
DISCOVER_MM = "Discover Minnie's Melodyland"
DISCOVER_TB = "Discover The Brrrgh"
DISCOVER_DDL = "Discover Donald's Dreamland"

DISCOVER_GS = "Discover Goofy Speedway"
DISCOVER_AA = "Discover Acorn Acres"

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
    ToontownLocationDefinition(CLEAR_VP, BASE_ID+128, location_type=ToontownLocationType.BOSSES, lock=GagFrameQuantityLock(30)),
    ToontownLocationDefinition(CLEAR_CFO, BASE_ID+129, location_type=ToontownLocationType.BOSSES, lock=GagFrameQuantityLock(35)),
    ToontownLocationDefinition(CLEAR_CJ, BASE_ID+130, location_type=ToontownLocationType.BOSSES, lock=GagFrameQuantityLock(40)),
    ToontownLocationDefinition(CLEAR_CEO, BASE_ID+131, location_type=ToontownLocationType.BOSSES, lock=GagFrameQuantityLock(45)),

    ToontownLocationDefinition(SELLBOT_PROOF, BASE_ID+132, location_type=ToontownLocationType.BOSSES, lock=GagFrameQuantityLock(30)),
    ToontownLocationDefinition(CASHBOT_PROOF, BASE_ID+133, location_type=ToontownLocationType.BOSSES, lock=GagFrameQuantityLock(35)),
    ToontownLocationDefinition(LAWBOT_PROOF, BASE_ID+134, location_type=ToontownLocationType.BOSSES, lock=GagFrameQuantityLock(40)),
    ToontownLocationDefinition(BOSSBOT_PROOF, BASE_ID+135, location_type=ToontownLocationType.BOSSES, lock=GagFrameQuantityLock(45)),

    ToontownLocationDefinition(SAVED_TOONTOWN, BASE_ID+136),

    # Discover Playgrounds
    ToontownLocationDefinition(DISCOVER_TTC, BASE_ID+137, location_type=ToontownLocationType.DISCOVER_PLAYGROUND),
    ToontownLocationDefinition(DISCOVER_DD, BASE_ID+138, location_type=ToontownLocationType.DISCOVER_PLAYGROUND),
    ToontownLocationDefinition(DISCOVER_DG, BASE_ID+139, location_type=ToontownLocationType.DISCOVER_PLAYGROUND),
    ToontownLocationDefinition(DISCOVER_MM, BASE_ID+140, location_type=ToontownLocationType.DISCOVER_PLAYGROUND),
    ToontownLocationDefinition(DISCOVER_TB, BASE_ID+141, location_type=ToontownLocationType.DISCOVER_PLAYGROUND),
    ToontownLocationDefinition(DISCOVER_DDL, BASE_ID+142, location_type=ToontownLocationType.DISCOVER_PLAYGROUND),

    ToontownLocationDefinition(DISCOVER_GS, BASE_ID + 143, location_type=ToontownLocationType.DISCOVER_PLAYGROUND),
    ToontownLocationDefinition(DISCOVER_AA, BASE_ID + 144, location_type=ToontownLocationType.DISCOVER_PLAYGROUND),

    # Cog Gallery Maxing (32)
    ToontownLocationDefinition(COLD_CALLER_MAXED_LOCATION, BASE_ID + 145, location_type=ToontownLocationType.GALLERY),
    ToontownLocationDefinition(SHORT_CHANGE_MAXED_LOCATION, BASE_ID + 146, location_type=ToontownLocationType.GALLERY),
    ToontownLocationDefinition(BOTTOM_FEEDER_MAXED_LOCATION, BASE_ID + 147, location_type=ToontownLocationType.GALLERY),
    ToontownLocationDefinition(FLUNKY_MAXED_LOCATION, BASE_ID + 148, location_type=ToontownLocationType.GALLERY),

    ToontownLocationDefinition(TELEMARKETER_MAXED_LOCATION, BASE_ID + 149, location_type=ToontownLocationType.GALLERY),
    ToontownLocationDefinition(PENNY_PINCHER_MAXED_LOCATION, BASE_ID + 150, location_type=ToontownLocationType.GALLERY),
    ToontownLocationDefinition(BLOODSUCKER_MAXED_LOCATION, BASE_ID + 151, location_type=ToontownLocationType.GALLERY),
    ToontownLocationDefinition(PENCIL_PUSHER_MAXED_LOCATION, BASE_ID + 152, location_type=ToontownLocationType.GALLERY),

    ToontownLocationDefinition(NAME_DROPPER_MAXED_LOCATION, BASE_ID + 153, location_type=ToontownLocationType.GALLERY),
    ToontownLocationDefinition(TIGHTWAD_MAXED_LOCATION, BASE_ID + 154, location_type=ToontownLocationType.GALLERY),
    ToontownLocationDefinition(DOUBLE_TALKER_MAXED_LOCATION, BASE_ID + 155, location_type=ToontownLocationType.GALLERY),
    ToontownLocationDefinition(YESMAN_MAXED_LOCATION, BASE_ID + 156, location_type=ToontownLocationType.GALLERY),

    ToontownLocationDefinition(GLAD_HANDER_MAXED_LOCATION, BASE_ID + 157, location_type=ToontownLocationType.GALLERY),
    ToontownLocationDefinition(BEAN_COUNTER_MAXED_LOCATION, BASE_ID + 158, location_type=ToontownLocationType.GALLERY),
    ToontownLocationDefinition(AMBULANCE_CHASER_MAXED_LOCATION, BASE_ID + 159, location_type=ToontownLocationType.GALLERY),
    ToontownLocationDefinition(MICROMANAGER_MAXED_LOCATION, BASE_ID + 160, location_type=ToontownLocationType.GALLERY),

    ToontownLocationDefinition(MOVER_AND_SHAKER_MAXED_LOCATION, BASE_ID + 161, location_type=ToontownLocationType.GALLERY),
    ToontownLocationDefinition(NUMBER_CRUNCHER_MAXED_LOCATION, BASE_ID + 162, location_type=ToontownLocationType.GALLERY),
    ToontownLocationDefinition(BACKSTABBER_MAXED_LOCATION, BASE_ID + 163, location_type=ToontownLocationType.GALLERY),
    ToontownLocationDefinition(DOWNSIZER_MAXED_LOCATION, BASE_ID + 164, location_type=ToontownLocationType.GALLERY),

    ToontownLocationDefinition(TWO_FACE_MAXED_LOCATION, BASE_ID + 165, location_type=ToontownLocationType.GALLERY),
    ToontownLocationDefinition(MONEY_BAGS_MAXED_LOCATION, BASE_ID + 166, location_type=ToontownLocationType.GALLERY),
    ToontownLocationDefinition(SPIN_DOCTOR_MAXED_LOCATION, BASE_ID + 167, location_type=ToontownLocationType.GALLERY),
    ToontownLocationDefinition(HEAD_HUNTER_MAXED_LOCATION, BASE_ID + 168, location_type=ToontownLocationType.GALLERY),

    ToontownLocationDefinition(MINGLER_MAXED_LOCATION, BASE_ID + 169, location_type=ToontownLocationType.GALLERY),
    ToontownLocationDefinition(LOAN_SHARK_MAXED_LOCATION, BASE_ID + 170, location_type=ToontownLocationType.GALLERY),
    ToontownLocationDefinition(LEGAL_EAGLE_MAXED_LOCATION, BASE_ID + 171, location_type=ToontownLocationType.GALLERY),
    ToontownLocationDefinition(CORPORATE_RAIDER_MAXED_LOCATION, BASE_ID + 172, location_type=ToontownLocationType.GALLERY),

    ToontownLocationDefinition(MR_HOLLYWOOD_MAXED_LOCATION, BASE_ID + 173, location_type=ToontownLocationType.GALLERY),
    ToontownLocationDefinition(ROBBER_BARRON_MAXED_LOCATION, BASE_ID + 174, location_type=ToontownLocationType.GALLERY),
    ToontownLocationDefinition(BIG_WIG_MAXED_LOCATION, BASE_ID + 175, location_type=ToontownLocationType.GALLERY),
    ToontownLocationDefinition(BIG_CHEESE_MAXED_LOCATION, BASE_ID + 176, location_type=ToontownLocationType.GALLERY),

    # Gag Training (49)
    ToontownLocationDefinition(TOONUP_FEATHER_UNLOCKED, BASE_ID+177, location_type=ToontownLocationType.GAG_TRAINING, lock=GagItemLock(GagItemLock.Track.TOONUP, 1)),
    ToontownLocationDefinition(TOONUP_MEGAPHONE_UNLOCKED, BASE_ID+178, location_type=ToontownLocationType.GAG_TRAINING, lock=GagItemLock(GagItemLock.Track.TOONUP, 2)),
    ToontownLocationDefinition(TOONUP_LIPSTICK_UNLOCKED, BASE_ID+179, location_type=ToontownLocationType.GAG_TRAINING, lock=GagItemLock(GagItemLock.Track.TOONUP, 3)),
    ToontownLocationDefinition(TOONUP_CANE_UNLOCKED, BASE_ID+180, location_type=ToontownLocationType.GAG_TRAINING, lock=GagItemLock(GagItemLock.Track.TOONUP, 4)),
    ToontownLocationDefinition(TOONUP_PIXIE_UNLOCKED, BASE_ID+181, location_type=ToontownLocationType.GAG_TRAINING, lock=GagItemLock(GagItemLock.Track.TOONUP, 5)),
    ToontownLocationDefinition(TOONUP_JUGGLING_UNLOCKED, BASE_ID+182, location_type=ToontownLocationType.GAG_TRAINING, lock=GagItemLock(GagItemLock.Track.TOONUP, 6)),
    ToontownLocationDefinition(TOONUP_HIGHDIVE_UNLOCKED, BASE_ID+183, location_type=ToontownLocationType.GAG_TRAINING, lock=GagItemLock(GagItemLock.Track.TOONUP, 7)),

    ToontownLocationDefinition(TRAP_BANANA_UNLOCKED, BASE_ID+184, location_type=ToontownLocationType.GAG_TRAINING, lock=GagItemLock(GagItemLock.Track.TRAP, 1)),
    ToontownLocationDefinition(TRAP_RAKE_UNLOCKED, BASE_ID+185, location_type=ToontownLocationType.GAG_TRAINING, lock=GagItemLock(GagItemLock.Track.TRAP, 2)),
    ToontownLocationDefinition(TRAP_MARBLES_UNLOCKED, BASE_ID+186, location_type=ToontownLocationType.GAG_TRAINING, lock=GagItemLock(GagItemLock.Track.TRAP, 3)),
    ToontownLocationDefinition(TRAP_QUICKSAND_UNLOCKED, BASE_ID+187, location_type=ToontownLocationType.GAG_TRAINING, lock=GagItemLock(GagItemLock.Track.TRAP, 4)),
    ToontownLocationDefinition(TRAP_TRAPDOOR_UNLOCKED, BASE_ID+188, location_type=ToontownLocationType.GAG_TRAINING, lock=GagItemLock(GagItemLock.Track.TRAP, 5)),
    ToontownLocationDefinition(TRAP_TNT_UNLOCKED, BASE_ID+189, location_type=ToontownLocationType.GAG_TRAINING, lock=GagItemLock(GagItemLock.Track.TRAP, 6)),
    ToontownLocationDefinition(TRAP_TRAIN_UNLOCKED, BASE_ID+190, location_type=ToontownLocationType.GAG_TRAINING, lock=GagItemLock(GagItemLock.Track.TRAP, 7)),

    ToontownLocationDefinition(LURE_ONEBILL_UNLOCKED, BASE_ID+191, location_type=ToontownLocationType.GAG_TRAINING, lock=GagItemLock(GagItemLock.Track.LURE, 1)),
    ToontownLocationDefinition(LURE_SMALLMAGNET_UNLOCKED, BASE_ID+192, location_type=ToontownLocationType.GAG_TRAINING, lock=GagItemLock(GagItemLock.Track.LURE, 2)),
    ToontownLocationDefinition(LURE_FIVEBILL_UNLOCKED, BASE_ID+193, location_type=ToontownLocationType.GAG_TRAINING, lock=GagItemLock(GagItemLock.Track.LURE, 3)),
    ToontownLocationDefinition(LURE_BIGMAGNET_UNLOCKED, BASE_ID+194, location_type=ToontownLocationType.GAG_TRAINING, lock=GagItemLock(GagItemLock.Track.LURE, 4)),
    ToontownLocationDefinition(LURE_TENBILL_UNLOCKED, BASE_ID+195, location_type=ToontownLocationType.GAG_TRAINING, lock=GagItemLock(GagItemLock.Track.LURE, 5)),
    ToontownLocationDefinition(LURE_HYPNO_UNLOCKED, BASE_ID+196, location_type=ToontownLocationType.GAG_TRAINING, lock=GagItemLock(GagItemLock.Track.LURE, 6)),
    ToontownLocationDefinition(LURE_PRESENTATION_UNLOCKED, BASE_ID+197, location_type=ToontownLocationType.GAG_TRAINING, lock=GagItemLock(GagItemLock.Track.LURE, 7)),

    ToontownLocationDefinition(SOUND_BIKEHORN_UNLOCKED, BASE_ID+198, location_type=ToontownLocationType.GAG_TRAINING, lock=GagItemLock(GagItemLock.Track.SOUND, 1)),
    ToontownLocationDefinition(SOUND_WHISTLE_UNLOCKED, BASE_ID+199, location_type=ToontownLocationType.GAG_TRAINING, lock=GagItemLock(GagItemLock.Track.SOUND, 2)),
    ToontownLocationDefinition(SOUND_BUGLE_UNLOCKED, BASE_ID+200, location_type=ToontownLocationType.GAG_TRAINING, lock=GagItemLock(GagItemLock.Track.SOUND, 3)),
    ToontownLocationDefinition(SOUND_AOOGAH_UNLOCKED, BASE_ID+201, location_type=ToontownLocationType.GAG_TRAINING, lock=GagItemLock(GagItemLock.Track.SOUND, 4)),
    ToontownLocationDefinition(SOUND_TRUNK_UNLOCKED, BASE_ID+202, location_type=ToontownLocationType.GAG_TRAINING, lock=GagItemLock(GagItemLock.Track.SOUND, 5)),
    ToontownLocationDefinition(SOUND_FOG_UNLOCKED, BASE_ID+203, location_type=ToontownLocationType.GAG_TRAINING, lock=GagItemLock(GagItemLock.Track.SOUND, 6)),
    ToontownLocationDefinition(SOUND_OPERA_UNLOCKED, BASE_ID+204, location_type=ToontownLocationType.GAG_TRAINING, lock=GagItemLock(GagItemLock.Track.SOUND, 7)),

    ToontownLocationDefinition(THROW_CUPCAKE_UNLOCKED, BASE_ID+205, location_type=ToontownLocationType.GAG_TRAINING, lock=GagItemLock(GagItemLock.Track.THROW, 1)),
    ToontownLocationDefinition(THROW_FRUITPIESLICE_UNLOCKED, BASE_ID+206, location_type=ToontownLocationType.GAG_TRAINING, lock=GagItemLock(GagItemLock.Track.THROW, 2)),
    ToontownLocationDefinition(THROW_CREAMPIESLICE_UNLOCKED, BASE_ID+207, location_type=ToontownLocationType.GAG_TRAINING, lock=GagItemLock(GagItemLock.Track.THROW, 3)),
    ToontownLocationDefinition(THROW_WHOLEFRUIT_UNLOCKED, BASE_ID+208, location_type=ToontownLocationType.GAG_TRAINING, lock=GagItemLock(GagItemLock.Track.THROW, 4)),
    ToontownLocationDefinition(THROW_WHOLECREAM_UNLOCKED, BASE_ID+209, location_type=ToontownLocationType.GAG_TRAINING, lock=GagItemLock(GagItemLock.Track.THROW, 5)),
    ToontownLocationDefinition(THROW_CAKE_UNLOCKED, BASE_ID+210, location_type=ToontownLocationType.GAG_TRAINING, lock=GagItemLock(GagItemLock.Track.THROW, 6)),
    ToontownLocationDefinition(THROW_WEDDING_UNLOCKED, BASE_ID+211, location_type=ToontownLocationType.GAG_TRAINING, lock=GagItemLock(GagItemLock.Track.THROW, 7)),

    ToontownLocationDefinition(SQUIRT_SQUIRTFLOWER_UNLOCKED, BASE_ID+212, location_type=ToontownLocationType.GAG_TRAINING, lock=GagItemLock(GagItemLock.Track.SQUIRT, 1)),
    ToontownLocationDefinition(SQUIRT_GLASS_UNLOCKED, BASE_ID+213, location_type=ToontownLocationType.GAG_TRAINING, lock=GagItemLock(GagItemLock.Track.SQUIRT, 2)),
    ToontownLocationDefinition(SQUIRT_SQUIRTGUN_UNLOCKED, BASE_ID+214, location_type=ToontownLocationType.GAG_TRAINING, lock=GagItemLock(GagItemLock.Track.SQUIRT, 3)),
    ToontownLocationDefinition(SQUIRT_SELTZER_UNLOCKED, BASE_ID+215, location_type=ToontownLocationType.GAG_TRAINING, lock=GagItemLock(GagItemLock.Track.SQUIRT, 4)),
    ToontownLocationDefinition(SQUIRT_HOSE_UNLOCKED, BASE_ID+216, location_type=ToontownLocationType.GAG_TRAINING, lock=GagItemLock(GagItemLock.Track.SQUIRT, 5)),
    ToontownLocationDefinition(SQUIRT_CLOUD_UNLOCKED, BASE_ID+217, location_type=ToontownLocationType.GAG_TRAINING, lock=GagItemLock(GagItemLock.Track.SQUIRT, 6)),
    ToontownLocationDefinition(SQUIRT_GEYSER_UNLOCKED, BASE_ID+218, location_type=ToontownLocationType.GAG_TRAINING, lock=GagItemLock(GagItemLock.Track.SQUIRT, 7)),

    ToontownLocationDefinition(DROP_FLOWERPOT_UNLOCKED, BASE_ID+219, location_type=ToontownLocationType.GAG_TRAINING, lock=GagItemLock(GagItemLock.Track.DROP, 1)),
    ToontownLocationDefinition(DROP_SANDBAG_UNLOCKED, BASE_ID+220, location_type=ToontownLocationType.GAG_TRAINING, lock=GagItemLock(GagItemLock.Track.DROP, 2)),
    ToontownLocationDefinition(DROP_ANVIL_UNLOCKED, BASE_ID+221, location_type=ToontownLocationType.GAG_TRAINING, lock=GagItemLock(GagItemLock.Track.DROP, 3)),
    ToontownLocationDefinition(DROP_BIGWEIGHT_UNLOCKED, BASE_ID+222, location_type=ToontownLocationType.GAG_TRAINING, lock=GagItemLock(GagItemLock.Track.DROP, 4)),
    ToontownLocationDefinition(DROP_SAFE_UNLOCKED, BASE_ID+223, location_type=ToontownLocationType.GAG_TRAINING, lock=GagItemLock(GagItemLock.Track.DROP, 5)),
    ToontownLocationDefinition(DROP_PIANO_UNLOCKED, BASE_ID+224, location_type=ToontownLocationType.GAG_TRAINING, lock=GagItemLock(GagItemLock.Track.DROP, 6)),
    ToontownLocationDefinition(DROP_BOAT_UNLOCKED, BASE_ID+225, location_type=ToontownLocationType.GAG_TRAINING, lock=GagItemLock(GagItemLock.Track.DROP, 7)),

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

GAG_TRAINING_LOCATIONS: List[str] = [
    check.unique_name for check in LIST_OF_LOCATION_DEFINITIONS if check.location_type == ToontownLocationType.GAG_TRAINING
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
