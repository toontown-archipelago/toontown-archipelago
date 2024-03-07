import random
from typing import Dict, Set

from BaseClasses import Item, ItemClassification

class ToontownItemDefinition:
    """
    Define items to be registered as drops in the multiworld.

    unique_name will be used as the name shown in game and for others
    classification is the type of item it is to be used for the placement algorithm
    quantity is how many items will always be present in the pool when they are not filler items

    """
    def __init__(self, unique_name: str, unique_id: int, classification: ItemClassification,  quantity=0):
        self.unique_name: str = unique_name
        self.unique_id: int = unique_id
        self.classification: ItemClassification = classification
        self.quantity: int = quantity


ITEM_1_LAFF_BOOST = "+1 Laff Boost"
ITEM_2_LAFF_BOOST = "+2 Laff Boost"
ITEM_3_LAFF_BOOST = "+3 Laff Boost"
ITEM_4_LAFF_BOOST = "+4 Laff Boost"
ITEM_5_LAFF_BOOST = "+5 Laff Boost"

ITEM_5_GAG_CAPACITY = "+5 Gag Capacity"
ITEM_10_GAG_CAPACITY = "+10 Gag Capacity"
ITEM_15_GAG_CAPACITY = "+15 Gag Capacity"

ITEM_750_MONEY_CAP = "+750 Jellybean Jar Capacity"
ITEM_1000_MONEY_CAP = "+1000 Jellybean Jar Capacity"
ITEM_1250_MONEY_CAP = "+1250 Jellybean Jar Capacity"
ITEM_1500_MONEY_CAP = "+1500 Jellybean Jar Capacity"
ITEM_2000_MONEY_CAP = "+2000 Jellybean Jar Capacity"
ITEM_2500_MONEY_CAP = "+2500 Jellybean Jar Capacity"

ITEM_TOONUP_FRAME = "Toon-up Gag Training Frame"
ITEM_TRAP_FRAME = "Trap Gag Training Frame"
ITEM_LURE_FRAME = "Lure Gag Training Frame"
ITEM_SOUND_FRAME = "Sound Gag Training Frame"
ITEM_THROW_FRAME = "Throw Gag Training Frame"
ITEM_SQUIRT_FRAME = "Squirt Gag Training Frame"
ITEM_DROP_FRAME = "Drop Gag Training Frame"

ITEM_1_GAG_MULTIPLIER = "+1 Base Gag XP Multiplier"
ITEM_2_GAG_MULTIPLIER = "+2 Base Gag XP Multiplier"

ITEM_FISHING_ROD_UPGRADE = "Progressional Fishing Rod Upgrade"

ITEM_TTC_TELEPORT = "TTC Teleport Access"
ITEM_DD_TELEPORT = "DD Teleport Access"
ITEM_DG_TELEPORT = "DG Teleport Access"
ITEM_MML_TELEPORT = "MM Teleport Access"
ITEM_TB_TELEPORT = "TB Teleport Access"
ITEM_DDL_TELEPORT = "DDL Teleport Access"

ITEM_SBHQ_TELEPORT = "SBHQ Teleport Access"
ITEM_CBHQ_TELEPORT = "CBHQ Teleport Access"
ITEM_LBHQ_TELEPORT = "LBHQ Teleport Access"
ITEM_BBHQ_TELEPORT = "BBHQ Teleport Access"

ITEM_TTC_HQ_ACCESS = "Toontown Central HQ Clearance"
ITEM_DD_HQ_ACCESS = "Donald's Dock HQ Clearance"
ITEM_DG_HQ_ACCESS = "Daisy Gardens HQ Clearance"
ITEM_MML_HQ_ACCESS = "Minnie's Melodyland HQ Clearance"
ITEM_TB_HQ_ACCESS = "The Brrrgh HQ Clearance"
ITEM_DDL_HQ_ACCESS = "Donald's Dreamland HQ Clearance"

ITEM_FRONT_FACTORY_ACCESS = "Front Factory Key"
ITEM_SIDE_FACTORY_ACCESS = "Side Factory Key"

ITEM_COIN_MINT_ACCESS = "Coin Mint Key"
ITEM_DOLLAR_MINT_ACCESS = "Dollar Mint Key"
ITEM_BULLION_MINT_ACCESS = "Bullion Mint Key"

ITEM_A_OFFICE_ACCESS = "Office A Key"
ITEM_B_OFFICE_ACCESS = "Office B Key"
ITEM_C_OFFICE_ACCESS = "Office C Key"
ITEM_D_OFFICE_ACCESS = "Office D Key"

ITEM_FRONT_THREE_ACCESS = "Front One Key"
ITEM_MIDDLE_THREE_ACCESS = "Middle Two Key"
ITEM_BACK_THREE_ACCESS = "Back Three Key"

ITEM_SELLBOT_DISGUISE = "Sellbot Disguise"
ITEM_CASHBOT_DISGUISE = "Cashbot Disguise"
ITEM_LAWBOT_DISGUISE = "Lawbot Disguise"
ITEM_BOSSBOT_DISGUISE = "Bossbot Disguise"

ITEM_SELLBOT_PROOF = "Sellbot Proof"
ITEM_CASHBOT_PROOF = "Cashbot Proof"
ITEM_LAWBOT_PROOF = "Lawbot Proof"
ITEM_BOSSBOT_PROOF = "Bossbot Proof"
ITEM_VICTORY = "Victory"

ITEM_250_MONEY = "250 Jellybeans"
ITEM_500_MONEY = "500 Jellybeans"
ITEM_1000_MONEY = "1000 Jellybeans"
ITEM_2000_MONEY = "2000 Jellybeans"

ITEM_500_XP = "500 Gag XP Bundle"
ITEM_1000_XP = "1000 Gag XP Bundle"
ITEM_1500_XP = "1500 Gag XP Bundle"
ITEM_2000_XP = "2000 Gag XP Bundle"
ITEM_2500_XP = "2500 Gag XP Bundle"

ITEM_SOS_REWARD = "Random SOS Card"
ITEM_UNITE_REWARD = "Random Unite"
ITEM_PINK_SLIP_REWARD = "Pink Slip Bundle"

ITEM_UBER_TRAP = "Uber Trap"
ITEM_DRIP_TRAP = "Drip Trap"

# Fill in if some items need more context
ITEM_DESCRIPTIONS = {
    ITEM_SELLBOT_DISGUISE: "Grants access to fight the Sellbot VP",
    ITEM_CASHBOT_DISGUISE: "Grants access to fight the Cashbot CFO",
    ITEM_LAWBOT_DISGUISE: "Grants access to fight the Lawbot CJ",
    ITEM_BOSSBOT_DISGUISE: "Grants access to fight the Bossbot CEO",
}

# Used to offset all item ids to be compatible in the multiworld, this is essentially just a random number
# and can be changed to anything that will not conflict with any other AP games
BASE_ITEM_ID = 0x501100


# When defining base quantities for items (quantity=x argument), try and get the required pool of items to be around
# 80-90% of the pool so that we can maintain a good ratio of meaningful checks to give/receive and reduce the amount
# of junk, for example if we have 225 checks in the game, we should aim for about 190-205 ish meaningful items

# Definition for unique instances of items and how much we should guarantee in the pool
LIST_OF_ITEM_DEFINITIONS: Set[ToontownItemDefinition] = {

    # Laff boosts (Ideally we have 100 laff in the pool, subject to change however)
    ToontownItemDefinition(ITEM_1_LAFF_BOOST, BASE_ITEM_ID+0, ItemClassification.useful, quantity=44),
    ToontownItemDefinition(ITEM_2_LAFF_BOOST, BASE_ITEM_ID+1, ItemClassification.useful, quantity=9),
    ToontownItemDefinition(ITEM_3_LAFF_BOOST, BASE_ITEM_ID+2, ItemClassification.useful, quantity=5),
    ToontownItemDefinition(ITEM_4_LAFF_BOOST, BASE_ITEM_ID+3, ItemClassification.useful, quantity=3),
    ToontownItemDefinition(ITEM_5_LAFF_BOOST, BASE_ITEM_ID+4, ItemClassification.useful, quantity=2),

    # Gag Cap+
    ToontownItemDefinition(ITEM_5_GAG_CAPACITY, BASE_ITEM_ID + 5, ItemClassification.useful, quantity=9),
    ToontownItemDefinition(ITEM_10_GAG_CAPACITY, BASE_ITEM_ID + 6, ItemClassification.useful, quantity=2),
    ToontownItemDefinition(ITEM_15_GAG_CAPACITY, BASE_ITEM_ID + 7, ItemClassification.useful, quantity=1),

    # Jellybean Cap+ (We should go from 1,000 -> 10,000 cap)
    ToontownItemDefinition(ITEM_750_MONEY_CAP, BASE_ITEM_ID + 8, ItemClassification.useful, quantity=1),
    ToontownItemDefinition(ITEM_1000_MONEY_CAP, BASE_ITEM_ID + 9, ItemClassification.useful, quantity=1),
    ToontownItemDefinition(ITEM_1250_MONEY_CAP, BASE_ITEM_ID + 10, ItemClassification.useful, quantity=1),
    ToontownItemDefinition(ITEM_1500_MONEY_CAP, BASE_ITEM_ID + 11, ItemClassification.useful, quantity=1),
    ToontownItemDefinition(ITEM_2000_MONEY_CAP, BASE_ITEM_ID + 12, ItemClassification.useful, quantity=1),
    ToontownItemDefinition(ITEM_2500_MONEY_CAP, BASE_ITEM_ID + 13, ItemClassification.useful, quantity=1),

    # Gag Training Frames (assume all are in pool, remove starting tracks before generation
    ToontownItemDefinition(ITEM_TOONUP_FRAME, BASE_ITEM_ID+14, ItemClassification.progression, quantity=8),
    ToontownItemDefinition(ITEM_TRAP_FRAME, BASE_ITEM_ID+15, ItemClassification.progression, quantity=8),
    ToontownItemDefinition(ITEM_LURE_FRAME, BASE_ITEM_ID+16, ItemClassification.progression, quantity=8),
    ToontownItemDefinition(ITEM_SOUND_FRAME, BASE_ITEM_ID+17, ItemClassification.progression, quantity=8),
    ToontownItemDefinition(ITEM_THROW_FRAME, BASE_ITEM_ID+18, ItemClassification.progression, quantity=8),
    ToontownItemDefinition(ITEM_SQUIRT_FRAME, BASE_ITEM_ID+19, ItemClassification.progression, quantity=8),
    ToontownItemDefinition(ITEM_DROP_FRAME, BASE_ITEM_ID+20, ItemClassification.progression, quantity=8),

    # Gag Training Multipliers
    ToontownItemDefinition(ITEM_1_GAG_MULTIPLIER, BASE_ITEM_ID+21, ItemClassification.useful, quantity=9),
    ToontownItemDefinition(ITEM_2_GAG_MULTIPLIER, BASE_ITEM_ID+22, ItemClassification.useful, quantity=2),

    # Fishing Rod Upgrades
    ToontownItemDefinition(ITEM_FISHING_ROD_UPGRADE, BASE_ITEM_ID+23, ItemClassification.progression, quantity=4),

    # Teleport Access
    ToontownItemDefinition(ITEM_TTC_TELEPORT, BASE_ITEM_ID+24, ItemClassification.useful, quantity=1),
    ToontownItemDefinition(ITEM_DD_TELEPORT, BASE_ITEM_ID+25, ItemClassification.useful, quantity=1),
    ToontownItemDefinition(ITEM_DG_TELEPORT, BASE_ITEM_ID+26, ItemClassification.useful, quantity=1),
    ToontownItemDefinition(ITEM_MML_TELEPORT, BASE_ITEM_ID+27, ItemClassification.useful, quantity=1),
    ToontownItemDefinition(ITEM_TB_TELEPORT, BASE_ITEM_ID+28, ItemClassification.useful, quantity=1),
    ToontownItemDefinition(ITEM_DDL_TELEPORT, BASE_ITEM_ID+29, ItemClassification.useful, quantity=1),

    ToontownItemDefinition(ITEM_SBHQ_TELEPORT, BASE_ITEM_ID+30, ItemClassification.useful, quantity=1),
    ToontownItemDefinition(ITEM_CBHQ_TELEPORT, BASE_ITEM_ID+31, ItemClassification.useful, quantity=1),
    ToontownItemDefinition(ITEM_LBHQ_TELEPORT, BASE_ITEM_ID+32, ItemClassification.useful, quantity=1),
    ToontownItemDefinition(ITEM_BBHQ_TELEPORT, BASE_ITEM_ID+33, ItemClassification.useful, quantity=1),

    # Tasking Access (Playground HQ entry access)
    ToontownItemDefinition(ITEM_DD_HQ_ACCESS, BASE_ITEM_ID+34, ItemClassification.progression, quantity=1),
    ToontownItemDefinition(ITEM_DG_HQ_ACCESS, BASE_ITEM_ID+35, ItemClassification.progression, quantity=1),
    ToontownItemDefinition(ITEM_MML_HQ_ACCESS, BASE_ITEM_ID+36, ItemClassification.progression, quantity=1),
    ToontownItemDefinition(ITEM_TB_HQ_ACCESS, BASE_ITEM_ID+37, ItemClassification.progression, quantity=1),
    ToontownItemDefinition(ITEM_DDL_HQ_ACCESS, BASE_ITEM_ID+38, ItemClassification.progression, quantity=1),

    # Facility Access
    ToontownItemDefinition(ITEM_FRONT_FACTORY_ACCESS, BASE_ITEM_ID+39, ItemClassification.progression, quantity=1),
    ToontownItemDefinition(ITEM_SIDE_FACTORY_ACCESS, BASE_ITEM_ID+40, ItemClassification.progression, quantity=1),

    ToontownItemDefinition(ITEM_COIN_MINT_ACCESS, BASE_ITEM_ID+41, ItemClassification.progression, quantity=1),
    ToontownItemDefinition(ITEM_DOLLAR_MINT_ACCESS, BASE_ITEM_ID+42, ItemClassification.progression, quantity=1),
    ToontownItemDefinition(ITEM_BULLION_MINT_ACCESS, BASE_ITEM_ID+43, ItemClassification.progression, quantity=1),

    ToontownItemDefinition(ITEM_A_OFFICE_ACCESS, BASE_ITEM_ID+44, ItemClassification.progression, quantity=1),
    ToontownItemDefinition(ITEM_B_OFFICE_ACCESS, BASE_ITEM_ID+45, ItemClassification.progression, quantity=1),
    ToontownItemDefinition(ITEM_C_OFFICE_ACCESS, BASE_ITEM_ID+46, ItemClassification.progression, quantity=1),
    ToontownItemDefinition(ITEM_D_OFFICE_ACCESS, BASE_ITEM_ID+47, ItemClassification.progression, quantity=1),

    ToontownItemDefinition(ITEM_FRONT_THREE_ACCESS, BASE_ITEM_ID+48, ItemClassification.progression, quantity=1),
    ToontownItemDefinition(ITEM_MIDDLE_THREE_ACCESS, BASE_ITEM_ID+49, ItemClassification.progression, quantity=1),
    ToontownItemDefinition(ITEM_BACK_THREE_ACCESS, BASE_ITEM_ID+50, ItemClassification.progression, quantity=1),

    # Boss Access
    ToontownItemDefinition(ITEM_SELLBOT_DISGUISE, BASE_ITEM_ID+51, ItemClassification.progression, quantity=1),
    ToontownItemDefinition(ITEM_CASHBOT_DISGUISE, BASE_ITEM_ID+52, ItemClassification.progression, quantity=1),
    ToontownItemDefinition(ITEM_LAWBOT_DISGUISE, BASE_ITEM_ID+53, ItemClassification.progression, quantity=1),
    ToontownItemDefinition(ITEM_BOSSBOT_DISGUISE, BASE_ITEM_ID+54, ItemClassification.progression, quantity=1),

    # Proofs (These have a quantity of 0 because we force place these under all circumstances)
    ToontownItemDefinition(ITEM_SELLBOT_PROOF, BASE_ITEM_ID+55, ItemClassification.progression, quantity=0),
    ToontownItemDefinition(ITEM_CASHBOT_PROOF, BASE_ITEM_ID+56, ItemClassification.progression, quantity=0),
    ToontownItemDefinition(ITEM_LAWBOT_PROOF, BASE_ITEM_ID+57, ItemClassification.progression, quantity=0),
    ToontownItemDefinition(ITEM_BOSSBOT_PROOF, BASE_ITEM_ID+58, ItemClassification.progression, quantity=0),

    # todo add filler items (jellybeans more laff maybe gag xp or something idk)
    ToontownItemDefinition(ITEM_250_MONEY, BASE_ITEM_ID+59, ItemClassification.filler),
    ToontownItemDefinition(ITEM_500_MONEY, BASE_ITEM_ID+60, ItemClassification.filler),
    ToontownItemDefinition(ITEM_1000_MONEY, BASE_ITEM_ID+61, ItemClassification.filler),
    ToontownItemDefinition(ITEM_2000_MONEY, BASE_ITEM_ID+62, ItemClassification.filler),

    ToontownItemDefinition(ITEM_500_XP, BASE_ITEM_ID + 63, ItemClassification.filler),
    ToontownItemDefinition(ITEM_1000_XP, BASE_ITEM_ID + 64, ItemClassification.filler),
    ToontownItemDefinition(ITEM_1500_XP, BASE_ITEM_ID + 65, ItemClassification.filler),
    ToontownItemDefinition(ITEM_2000_XP, BASE_ITEM_ID + 66, ItemClassification.filler),
    ToontownItemDefinition(ITEM_2500_XP, BASE_ITEM_ID + 67, ItemClassification.filler),

    ToontownItemDefinition(ITEM_SOS_REWARD, BASE_ITEM_ID + 68, ItemClassification.filler),
    ToontownItemDefinition(ITEM_UNITE_REWARD, BASE_ITEM_ID + 69, ItemClassification.filler),
    ToontownItemDefinition(ITEM_PINK_SLIP_REWARD, BASE_ITEM_ID + 70, ItemClassification.filler),

    # Items added in hindsight, #todo do this better
    ToontownItemDefinition(ITEM_TTC_HQ_ACCESS, BASE_ITEM_ID+71, ItemClassification.progression, quantity=0),
    ToontownItemDefinition(ITEM_VICTORY, BASE_ITEM_ID+72, ItemClassification.progression, quantity=0),

    # Traps
    ToontownItemDefinition(ITEM_UBER_TRAP, BASE_ITEM_ID+73, ItemClassification.trap),
    ToontownItemDefinition(ITEM_DRIP_TRAP, BASE_ITEM_ID+74, ItemClassification.trap),
}

ITEM_DEFINITIONS = {
    item_def.unique_name: item_def for item_def in LIST_OF_ITEM_DEFINITIONS
}

# Junk items are items where they are classified as filler
# todo add quality/rarity to filler items and add weighting options as a setting so junk is better sometimes
JUNK_ITEMS = [
    item for item in ITEM_DEFINITIONS.values() if item.classification == ItemClassification.filler
]

# Trap items are items that cause some form of potentially negative action to the player
TRAP_ITEMS = [
    item for item in ITEM_DEFINITIONS.values() if item.classification == ItemClassification.trap
]

ID_TO_ITEM_DEFINITION = {
    item.unique_id: item for item in ITEM_DEFINITIONS.values()
}


class ToontownItem(Item):
    game: str = "Toontown"


def random_junk() -> ToontownItemDefinition:
    return random.choice(JUNK_ITEMS)


def random_trap() -> ToontownItemDefinition:
    return random.choice(TRAP_ITEMS)


# A quick debug script for various purposes, use this to hit our item "target" when changing amounts of items in pool
if __name__ == "__main__":
    pool: Dict[str, int] = {}
    for item_name, item in ITEM_DEFINITIONS.items():
        if item.quantity <= 0:
            continue

        pool[item_name] = item.quantity

    sorted_keys = list(pool.keys())
    sorted_keys.sort()

    for item_name in sorted_keys:
        print(pool[item_name], item_name)

    print(f"\n\n{len(pool)} item types in the required pool")
    print(f"{sum(pool.values())} total item count in the required pool")
