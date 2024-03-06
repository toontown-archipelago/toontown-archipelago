from typing import Dict

from BaseClasses import CollectionState

from .locations import *


class RegionLock:

    def __init__(self, locks: Dict[str, int]):
        self.locks: Dict[str, int] = locks

    # Wrapper function so we can avoid using lambda
    def get_lock_function(self, player):
        def ret(state: CollectionState):
            # Loop through all the items contained in the lock
            for item, quantity_needed in self.locks.items():
                # If we do not have the required items needed we cannot progress
                if not state.has(item, player, quantity_needed):
                    return False
            # We had all required items, we can progress
            return True

        return ret


class ToontownRegionDefinition:
    """
    Define Regions to be registered as containers for locations

    unique_name will be used as the name shown in game and for others
    locations is the "checks" this region contains
    connects_to is a list of other regions by str id that this connects to
    locked_by is a str representing an item that unlocks this area. None means it is always unlocked

    """

    def __init__(self, unique_name: str, locations=None, connects_to=None, locks: RegionLock = None):

        # check if we have locations, if not, empty list, if one was given, contain it in a list
        if locations is None:
            locations = []
        elif isinstance(locations, str):
            locations = [locations]

        if connects_to is None:
            connects_to = []
        elif isinstance(connects_to, str):
            connects_to = [connects_to]

        if not isinstance(locations, list):
            raise Exception("locations should be a list!")

        if not isinstance(connects_to, list):
            raise Exception("connects_to should be a list!")

        self.unique_name: str = unique_name
        self.locations: List[str] = locations
        self.connects_to: List[str] = connects_to
        self.lock: RegionLock = locks

    def always_unlocked(self):
        return self.lock is None


# Define names of regions here as variables for easy reference
# Regions are containers for Locations

# START
REGION_MENU = "Menu"

# Login
REGION_LOGIN = "Login"

# Misc Book Stuff
REGION_GALLERY = "Cog Gallery"

REGION_FISHING_10 = "Fishing (10 Species)"
REGION_FISHING_20 = "Fishing (20 Species)"
REGION_FISHING_30 = "Fishing (30 Species)"
REGION_FISHING_40 = "Fishing (40 Species)"
REGION_FISHING_50 = "Fishing (50 Species)"
REGION_FISHING_60 = "Fishing (60 Species)"
REGION_FISHING_70 = "Fishing (Maxed)"

# Discovery
REGION_DISCOVER_PLAYGROUNDS = "Discover Playgrounds"

# Playgrounds
REGION_TTC = "Toontown Central"
REGION_DD = "Donald's Dock"
REGION_DG = "Daisy's Gardens"
REGION_MM = "Minnie's Melodyland"
REGION_TB = "The Brrrgh"
REGION_DDL = "Donald's Dreamland"

# SBHQ
REGION_SBHQ_TUNNEL = "Sellbot HQ Tunnel"
REGION_FRONT_FACTORY = "Front Factory"
REGION_SIDE_FACTORY = "Side Factory"
REGION_VP = "Sellbot VP"

# CBHQ
REGION_CBHQ_TUNNEL = "Cashbot HQ Tunnel"
REGION_COIN_MINT = "Coin Mint"
REGION_DOLLAR_MINT = "Dollar Mint"
REGION_BULLION_MINT = "Bullion Mint"
REGION_CFO = "Cashbot CFO"

# LBHQ
REGION_LBHQ_TUNNEL = "Lawbot HQ Tunnel"
REGION_OFFICE_A = "Office A"
REGION_OFFICE_B = "Office B"
REGION_OFFICE_C = "Office C"
REGION_OFFICE_D = "Office D"
REGION_CJ = "Lawbot CJ"

# BBHQ
REGION_BBHQ_TUNNEL = "Bossbot HQ Tunnel"
REGION_FRONT_THREE = "Front One"
REGION_MIDDLE_THREE = "Middle Two"
REGION_BACK_THREE = "Back Three"
REGION_CEO = "Bossbot CEO"

# Win condition
REGION_FLIPPY_COMPLETE = "Flippy (Saved Toontown)"

# Some helpers to group regions up for easy connection access

# What regions are immediately accessible when starting a new game?
REGION_GROUP_INITIAL_ACCESSIBLE_REGIONS = [
    REGION_LOGIN,
    REGION_GALLERY,
    REGION_DISCOVER_PLAYGROUNDS,
    REGION_FISHING_10,
    REGION_TTC,
    REGION_DD,
    REGION_DG,
    REGION_MM,
    REGION_TB,
    REGION_DDL,
    REGION_SBHQ_TUNNEL,
    REGION_CBHQ_TUNNEL,
    REGION_LBHQ_TUNNEL,
    REGION_BBHQ_TUNNEL,
    REGION_FLIPPY_COMPLETE
]

# Regions for grouping activities in cog HQs
REGION_GROUP_SELLBOT_HQ = [
    REGION_FRONT_FACTORY,
    REGION_SIDE_FACTORY,
    REGION_VP,
]

REGION_GROUP_CASHBOT_HQ = [
    REGION_COIN_MINT,
    REGION_DOLLAR_MINT,
    REGION_BULLION_MINT,
    REGION_CFO
]

REGION_GROUP_LAWBOT_HQ = [
    REGION_OFFICE_A,
    REGION_OFFICE_B,
    REGION_OFFICE_C,
    REGION_OFFICE_D,
    REGION_CJ
]

REGION_GROUP_BOSSBOT_HQ = [
    REGION_FRONT_THREE,
    REGION_MIDDLE_THREE,
    REGION_BACK_THREE,
    REGION_CEO
]

# A list of all regions in the game. Regions are progression stages that contain "checks"
# A region is typically defined as something that needs progression for a group of locations to be unlocked
REGION_DEFINITIONS = (

    # Default Region, connects to initial unlocks of the game
    ToontownRegionDefinition(REGION_MENU, connects_to=REGION_GROUP_INITIAL_ACCESSIBLE_REGIONS),

    # Collection of checks received for logging in
    ToontownRegionDefinition(REGION_LOGIN, locations=LOGIN_LOCATIONS),

    # Cog Gallery is always accessible right away, has 32 checks and is the end of its branch
    ToontownRegionDefinition(REGION_GALLERY, locations=GALLERY_LOCATIONS),

    ToontownRegionDefinition(REGION_DISCOVER_PLAYGROUNDS, locations=DISCOVER_PLAYGROUND_LOCATIONS),

    # Fishing is a linear progression track where every 10 species you unlock the next check, 7 checks
    ToontownRegionDefinition(REGION_FISHING_10, locations=FISHING_10_SPECIES, connects_to=REGION_FISHING_20),
    ToontownRegionDefinition(REGION_FISHING_20, locations=FISHING_20_SPECIES, connects_to=REGION_FISHING_30),
    ToontownRegionDefinition(REGION_FISHING_30, locations=FISHING_30_SPECIES, connects_to=REGION_FISHING_40),
    ToontownRegionDefinition(REGION_FISHING_40, locations=FISHING_40_SPECIES, connects_to=REGION_FISHING_50),
    ToontownRegionDefinition(REGION_FISHING_50, locations=FISHING_50_SPECIES, connects_to=REGION_FISHING_60),
    ToontownRegionDefinition(REGION_FISHING_60, locations=FISHING_60_SPECIES, connects_to=REGION_FISHING_70),
    ToontownRegionDefinition(REGION_FISHING_70, locations=FISHING_COMPLETE_ALBUM),

    # Players spawn in Toontown Central, have 12 tasks (checks) to complete, and that is it for this branch
    ToontownRegionDefinition(REGION_TTC, locations=TTC_TASK_LOCATIONS),

    # For the other 5, same as TTC, except it is locked behind its HQ clearance item
    ToontownRegionDefinition(REGION_DD, locations=DD_TASK_LOCATIONS,   locks=RegionLock({"Donald's Dock HQ Clearance": 1})),
    ToontownRegionDefinition(REGION_DG, locations=DG_TASK_LOCATIONS,   locks=RegionLock({"Daisy's Gardens HQ Clearance": 1})),
    ToontownRegionDefinition(REGION_MM, locations=MM_TASK_LOCATIONS,   locks=RegionLock({"Minnie's Melodyland HQ Clearance": 1})),
    ToontownRegionDefinition(REGION_TB, locations=TB_TASK_LOCATIONS,   locks=RegionLock({"The Brrrgh HQ Clearance": 1})),
    ToontownRegionDefinition(REGION_DDL, locations=DDL_TASK_LOCATIONS, locks=RegionLock({"Donald's Dreamland HQ Clearance": 1})),

    # For Sellbot HQ, we first need to hit the tunnel region (accessible always) then we unlock all the activities
    # in the HQ, however these activities have locks behind them and can be done in any order
    ToontownRegionDefinition(REGION_SBHQ_TUNNEL, locations=DISCOVER_SBHQ, connects_to=REGION_GROUP_SELLBOT_HQ),
    # Now for all the regions defined in REGION_GROUP_SELLBOT_HQ, and define their locks. They are end of branch
    ToontownRegionDefinition(REGION_FRONT_FACTORY, locations=CLEAR_FRONT_FACTORY, locks=RegionLock({"Front Factory Key": 1})),
    ToontownRegionDefinition(REGION_SIDE_FACTORY, locations=CLEAR_SIDE_FACTORY, locks=RegionLock({"Side Factory Key": 1})),
    # Boss will connect to flippy for the victory condition check
    ToontownRegionDefinition(REGION_VP, locations=[CLEAR_VP, SELLBOT_PROOF], locks=RegionLock({"Sellbot Disguise": 1})),

    # Now repeat for the other 3 HQs
    # CBHQ
    ToontownRegionDefinition(REGION_CBHQ_TUNNEL, locations=DISCOVER_CBHQ, connects_to=REGION_GROUP_CASHBOT_HQ),
    ToontownRegionDefinition(REGION_COIN_MINT, locations=CLEAR_COIN_MINT, locks=RegionLock({"Coin Mint Key": 1})),
    ToontownRegionDefinition(REGION_DOLLAR_MINT, locations=CLEAR_DOLLAR_MINT, locks=RegionLock({"Dollar Mint Key": 1})),
    ToontownRegionDefinition(REGION_BULLION_MINT, locations=CLEAR_BULLION_MINT, locks=RegionLock({"Bullion Mint Key": 1})),
    ToontownRegionDefinition(REGION_CFO, locations=[CLEAR_CFO, CASHBOT_PROOF], locks=RegionLock({"Cashbot Disguise": 1})),

    # LBHQ
    ToontownRegionDefinition(REGION_LBHQ_TUNNEL, locations=DISCOVER_LBHQ, connects_to=REGION_GROUP_LAWBOT_HQ),
    ToontownRegionDefinition(REGION_OFFICE_A, locations=CLEAR_A_OFFICE, locks=RegionLock({"A Office Key": 1})),
    ToontownRegionDefinition(REGION_OFFICE_B, locations=CLEAR_B_OFFICE, locks=RegionLock({"B Office Key": 1})),
    ToontownRegionDefinition(REGION_OFFICE_C, locations=CLEAR_C_OFFICE, locks=RegionLock({"C Office Key": 1})),
    ToontownRegionDefinition(REGION_OFFICE_D, locations=CLEAR_D_OFFICE, locks=RegionLock({"D Office Key": 1})),
    ToontownRegionDefinition(REGION_CJ, locations=[CLEAR_CJ, LAWBOT_PROOF], locks=RegionLock({"Lawbot Disguise": 1})),

    # BBHQ
    ToontownRegionDefinition(REGION_BBHQ_TUNNEL, locations=DISCOVER_BBHQ, connects_to=REGION_GROUP_BOSSBOT_HQ),
    ToontownRegionDefinition(REGION_FRONT_THREE, locations=CLEAR_FRONT_THREE, locks=RegionLock({"Front One Key": 1})),
    ToontownRegionDefinition(REGION_MIDDLE_THREE, locations=CLEAR_MIDDLE_THREE, locks=RegionLock({"Middle Two Key": 1})),
    ToontownRegionDefinition(REGION_BACK_THREE, locations=CLEAR_BACK_THREE, locks=RegionLock({"Back Three Key": 1})),
    ToontownRegionDefinition(REGION_CEO, locations=[CLEAR_CEO, BOSSBOT_PROOF], locks=RegionLock({"Bossbot Disguise": 1})),

    # Flippy's office basically, talk to him and win the game
    ToontownRegionDefinition(REGION_FLIPPY_COMPLETE, locations=SAVED_TOONTOWN, locks=RegionLock({"Sellbot Proof": 1, "Cashbot Proof": 1, "Lawbot Proof": 1, "Bossbot Proof": 1})),

)

REGION_NAME_TO_REGION_DEFINITION: Dict[str, ToontownRegionDefinition] = {
    reg_def.unique_name: reg_def for reg_def in REGION_DEFINITIONS
}
