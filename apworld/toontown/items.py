import random
import enum
from dataclasses import dataclass
from typing import Optional, List
from BaseClasses import ItemClassification
from . import consts


class ToontownItemName(enum.Enum):
    ### Laff Boost ###
    LAFF_BOOST_1 = "+1 Laff Boost"
    LAFF_BOOST_2 = "+2 Laff Boost"
    LAFF_BOOST_3 = "+3 Laff Boost"
    LAFF_BOOST_4 = "+4 Laff Boost"
    LAFF_BOOST_5 = "+5 Laff Boost"

    ### Damage Increase ###
    DMG_BOOST_1 = "+1% Damage Boost"
    DMG_BOOST_2 = "+2% Damage Boost"
    DMG_BOOST_3 = "+3% Damage Boost"
    DMG_BOOST_4 = "+4% Damage Boost"

    ### Jellybean Jar Capacity ###
    MONEY_CAP_1000 = "Progressive Jellybean Jar"
    
    ### Task Carry Capacity ###
    TASK_CAPACITY = "Progressive Task Capacity"

    ### Fishing ###
    FISHING_ROD_UPGRADE = "Progressive Fishing Rod"
    TTC_FISHING = "TTC Fishing License"
    DD_FISHING  = "DD Fishing License"
    DG_FISHING  = "DG Fishing License"
    MML_FISHING = "MML Fishing License"
    TB_FISHING  = "TB Fishing License"
    DDL_FISHING = "DDL Fishing License"
    FISH = "Fish"

    ### Gag Training Frames ###
    TOONUP_FRAME = "Toon-Up Training Frame"
    TRAP_FRAME   = "Trap Training Frame"
    LURE_FRAME   = "Lure Training Frame"
    SOUND_FRAME  = "Sound Training Frame"
    THROW_FRAME  = "Throw Training Frame"
    SQUIRT_FRAME = "Squirt Training Frame"
    DROP_FRAME   = "Drop Training Frame"

    ### Gag Upgrades ###
    TOONUP_UPGRADE = "Organic Toon-Up Upgrade"
    TRAP_UPGRADE   = "Organic Trap Upgrade"
    LURE_UPGRADE   = "Organic Lure Upgrade"
    SOUND_UPGRADE  = "Organic Sound Upgrade"
    THROW_UPGRADE  = "Organic Throw Upgrade"
    SQUIRT_UPGRADE = "Organic Squirt Upgrade"
    DROP_UPGRADE   = "Organic Drop Upgrade"

    ### Gag Capacity ###
    GAG_CAPACITY_5  = "+5 Gag Capacity"
    GAG_CAPACITY_10 = "+10 Gag Capacity"
    GAG_CAPACITY_15 = "+15 Gag Capacity"

    ### Gag Multiplier ###
    GAG_MULTIPLIER_1 = "+1 Base Gag XP Multiplier"
    GAG_MULTIPLIER_2 = "+2 Base Gag XP Multiplier"

    ### Access Keys ###
    TTC_ACCESS  = "TTC Access Key"
    DD_ACCESS   = "DD Access Key"
    DG_ACCESS   = "DG Access Key"
    MML_ACCESS  = "MML Access Key"
    TB_ACCESS   = "TB Access Key"
    DDL_ACCESS  = "DDL Access Key"
    SBHQ_ACCESS = "SBHQ Access Key"
    CBHQ_ACCESS = "CBHQ Access Key"
    LBHQ_ACCESS = "LBHQ Access Key"
    BBHQ_ACCESS = "BBHQ Access Key"
    AA_ACCESS = "AA Access Key"
    GS_ACCESS = 'GS Access Key'

    ### Joke Books ###
    TTC_JOKE_BOOK = "TTC Joke Book"
    DD_JOKE_BOOK = "DD Joke Book"
    DG_JOKE_BOOK = "DG Joke Book"
    MML_JOKE_BOOK = "MML Joke Book"
    TB_JOKE_BOOK = "TB Joke Book"
    DDL_JOKE_BOOK = "DDL Joke Book"

    ### Facility Keys ###
    FRONT_FACTORY_ACCESS = "Front Factory Key"
    SIDE_FACTORY_ACCESS  = "Side Factory Key"

    COIN_MINT_ACCESS    = "Coin Mint Key"
    DOLLAR_MINT_ACCESS  = "Dollar Mint Key"
    BULLION_MINT_ACCESS = "Bullion Mint Key"

    A_OFFICE_ACCESS = "Office A Key"
    B_OFFICE_ACCESS = "Office B Key"
    C_OFFICE_ACCESS = "Office C Key"
    D_OFFICE_ACCESS = "Office D Key"

    FRONT_ONE_ACCESS  = "Front One Key"
    MIDDLE_TWO_ACCESS = "Middle Two Key"
    BACK_THREE_ACCESS = "Back Three Key"

    ### Cog Disguises ###
    SELLBOT_DISGUISE = "Sellbot Disguise"
    CASHBOT_DISGUISE = "Cashbot Disguise"
    LAWBOT_DISGUISE  = "Lawbot Disguise"
    BOSSBOT_DISGUISE = "Bossbot Disguise"

    ### Jellybean Bundles ###
    MONEY_150  = "150 Jellybeans"
    MONEY_400  = "400 Jellybeans"
    MONEY_700 = "700 Jellybeans"
    MONEY_1000 = "1000 Jellybeans"

    ### Gag XP Bundles ###
    XP_10 = "10% Gag XP Bundle"
    XP_15 = "15% Gag XP Bundle"
    XP_20 = "20% Gag XP Bundle"

    ### Activity Items ###
    GOLF_PUTTER = "Golf Putter"
    GO_KART = "Go-Kart"

    ### Bounty Items ###
    BOUNTY = "Bounty"

    ### Reward Bundles ###
    SOS_REWARD_3        = "Random 3-Star SOS Card"
    SOS_REWARD_4        = "Random 4-Star SOS Card"
    SOS_REWARD_5        = "Random 5-Star SOS Card"
    UNITE_REWARD_GAG    = "Random Gag Unite"
    UNITE_REWARD_TOONUP = "Random Toon-Up Unite"
    PINK_SLIP_REWARD    = "Pink Slip"
    SUMMON_REWARD       = "Cog Summon"

    ### Healing Items ###
    HEAL_10 = "10% Toon-Up"
    HEAL_20 = "20% Toon-Up"

    ### Traps ###
    UBER_TRAP = "Uber Trap"
    BEAN_TAX_TRAP_750 = "750 Bean Tax"
    BEAN_TAX_TRAP_1000 = "1000 Bean Tax"
    BEAN_TAX_TRAP_1250 = "1250 Bean Tax"
    DRIP_TRAP = "Drip Trap"
    GAG_SHUFFLE_TRAP = "Gag Shuffle Trap"
    DAMAGE_15 = "15% Damage Trap"
    DAMAGE_25 = "25% Damage Trap"

    ### META ###
    VP = "Defeated Sellbot VP"
    CFO = "Defeated Cashbot CFO"
    CJ = "Defeated Lawbot CJ"
    CEO =  "Defeated Bossbot CEO"


@dataclass
class ToontownItemDefinition:
    name: ToontownItemName
    classification: ItemClassification
    quantity: int = 0  # 0 implies manually/dynamically generated in World
    description: Optional[str] = None
    unique_id: int = 0


ITEM_DEFINITIONS: List[ToontownItemDefinition] = [
    # region Laff Boosts
    ToontownItemDefinition(ToontownItemName.LAFF_BOOST_1, ItemClassification.progression_deprioritized),
    ToontownItemDefinition(ToontownItemName.LAFF_BOOST_2, ItemClassification.progression_deprioritized),
    ToontownItemDefinition(ToontownItemName.LAFF_BOOST_3, ItemClassification.progression_deprioritized),
    ToontownItemDefinition(ToontownItemName.LAFF_BOOST_4, ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.LAFF_BOOST_5, ItemClassification.progression),
    # endregion
    # region Laff Boosts
    ToontownItemDefinition(ToontownItemName.DMG_BOOST_1, ItemClassification.progression_deprioritized),
    ToontownItemDefinition(ToontownItemName.DMG_BOOST_2, ItemClassification.progression_deprioritized),
    ToontownItemDefinition(ToontownItemName.DMG_BOOST_3, ItemClassification.progression_deprioritized),
    ToontownItemDefinition(ToontownItemName.DMG_BOOST_4, ItemClassification.progression),
    # endregion
    # region Gag Capacity
    ToontownItemDefinition(ToontownItemName.GAG_CAPACITY_5,  ItemClassification.progression_deprioritized, quantity=12),  # NOTE: update values in has_collected_items_for_gag_level to match quantity
    ToontownItemDefinition(ToontownItemName.GAG_CAPACITY_10, ItemClassification.progression, quantity=2),  # NOTE: update values in has_collected_items_for_gag_level to match quantity
    ToontownItemDefinition(ToontownItemName.GAG_CAPACITY_15, ItemClassification.progression, quantity=0),  # NOTE: update values in has_collected_items_for_gag_level to match quantity
    # endregion
    # region Jellybean Capacity
    ToontownItemDefinition(ToontownItemName.MONEY_CAP_1000, ItemClassification.progression, quantity=9),
    # region Task Capacity
    # range depends on the starting capacity
    ToontownItemDefinition(ToontownItemName.TASK_CAPACITY, ItemClassification.progression_deprioritized_skip_balancing),
    # endregion
    # region Gag Training Frames
    ToontownItemDefinition(ToontownItemName.TOONUP_FRAME, ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.TRAP_FRAME,   ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.LURE_FRAME,   ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.SOUND_FRAME,  ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.THROW_FRAME,  ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.SQUIRT_FRAME, ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.DROP_FRAME,   ItemClassification.progression),
    # endregion
    # region Gag Upgrades
    ToontownItemDefinition(ToontownItemName.TOONUP_UPGRADE, ItemClassification.useful),
    ToontownItemDefinition(ToontownItemName.TRAP_UPGRADE,   ItemClassification.useful),
    ToontownItemDefinition(ToontownItemName.LURE_UPGRADE,   ItemClassification.useful),
    ToontownItemDefinition(ToontownItemName.SOUND_UPGRADE,  ItemClassification.useful),
    ToontownItemDefinition(ToontownItemName.THROW_UPGRADE,  ItemClassification.useful),
    ToontownItemDefinition(ToontownItemName.SQUIRT_UPGRADE, ItemClassification.useful),
    ToontownItemDefinition(ToontownItemName.DROP_UPGRADE,   ItemClassification.useful),
    # endregion
    # region Gag Training Multipliers
    ToontownItemDefinition(ToontownItemName.GAG_MULTIPLIER_1, ItemClassification.progression_deprioritized),
    ToontownItemDefinition(ToontownItemName.GAG_MULTIPLIER_2, ItemClassification.progression_deprioritized),
    # endregion
    # region Fishing Items
    ToontownItemDefinition(ToontownItemName.FISHING_ROD_UPGRADE, ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.TTC_FISHING, ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.DD_FISHING,  ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.DG_FISHING,  ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.MML_FISHING, ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.TB_FISHING,  ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.DDL_FISHING, ItemClassification.progression),
    # endregion
    # region Teleport Access
    ToontownItemDefinition(ToontownItemName.TTC_ACCESS,  ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.DD_ACCESS,   ItemClassification.progression, quantity=1),
    ToontownItemDefinition(ToontownItemName.DG_ACCESS,   ItemClassification.progression, quantity=1),
    ToontownItemDefinition(ToontownItemName.MML_ACCESS,  ItemClassification.progression, quantity=1),
    ToontownItemDefinition(ToontownItemName.TB_ACCESS,   ItemClassification.progression, quantity=1),
    ToontownItemDefinition(ToontownItemName.DDL_ACCESS,  ItemClassification.progression, quantity=1),
    ToontownItemDefinition(ToontownItemName.SBHQ_ACCESS, ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.CBHQ_ACCESS, ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.LBHQ_ACCESS, ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.BBHQ_ACCESS, ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.AA_ACCESS,   ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.GS_ACCESS,   ItemClassification.progression),
    # endregion
    # region Joke Books
    ToontownItemDefinition(ToontownItemName.TTC_JOKE_BOOK,  ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.DD_JOKE_BOOK,   ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.DG_JOKE_BOOK,   ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.MML_JOKE_BOOK,  ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.TB_JOKE_BOOK,   ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.DDL_JOKE_BOOK,  ItemClassification.progression),
    # endregion
    # region Facility Access
    ToontownItemDefinition(ToontownItemName.FRONT_FACTORY_ACCESS, ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.SIDE_FACTORY_ACCESS,  ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.COIN_MINT_ACCESS,     ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.DOLLAR_MINT_ACCESS,   ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.BULLION_MINT_ACCESS,  ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.A_OFFICE_ACCESS,      ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.B_OFFICE_ACCESS,      ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.C_OFFICE_ACCESS,      ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.D_OFFICE_ACCESS,      ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.FRONT_ONE_ACCESS,     ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.MIDDLE_TWO_ACCESS,    ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.BACK_THREE_ACCESS,    ItemClassification.progression),
    # endregion
    # region Boss Disguises
    ToontownItemDefinition(ToontownItemName.SELLBOT_DISGUISE, ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.CASHBOT_DISGUISE, ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.LAWBOT_DISGUISE,  ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.BOSSBOT_DISGUISE, ItemClassification.progression),
    # endregion
    # region activities
    ToontownItemDefinition(ToontownItemName.GOLF_PUTTER, ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.GO_KART, ItemClassification.progression),
    # endregion
    # region bounties
    ToontownItemDefinition(ToontownItemName.BOUNTY, ItemClassification.progression_skip_balancing),
    # endregion
    # region Filler Items
    ToontownItemDefinition(ToontownItemName.MONEY_150,            ItemClassification.filler),
    ToontownItemDefinition(ToontownItemName.MONEY_400,            ItemClassification.filler),
    ToontownItemDefinition(ToontownItemName.MONEY_700,            ItemClassification.filler),
    ToontownItemDefinition(ToontownItemName.MONEY_1000,           ItemClassification.filler),
    ToontownItemDefinition(ToontownItemName.XP_10,                ItemClassification.filler),
    ToontownItemDefinition(ToontownItemName.XP_15,                ItemClassification.filler),
    ToontownItemDefinition(ToontownItemName.XP_20,                ItemClassification.filler),
    ToontownItemDefinition(ToontownItemName.SOS_REWARD_3,         ItemClassification.filler),
    ToontownItemDefinition(ToontownItemName.SOS_REWARD_4,         ItemClassification.filler),
    ToontownItemDefinition(ToontownItemName.SOS_REWARD_5,         ItemClassification.filler),
    ToontownItemDefinition(ToontownItemName.UNITE_REWARD_GAG,     ItemClassification.filler),
    ToontownItemDefinition(ToontownItemName.UNITE_REWARD_TOONUP,  ItemClassification.filler),
    ToontownItemDefinition(ToontownItemName.PINK_SLIP_REWARD,     ItemClassification.filler),
    ToontownItemDefinition(ToontownItemName.SUMMON_REWARD,        ItemClassification.filler),
    ToontownItemDefinition(ToontownItemName.HEAL_10,              ItemClassification.filler),
    ToontownItemDefinition(ToontownItemName.HEAL_20,              ItemClassification.filler),
    ToontownItemDefinition(ToontownItemName.FISH,                 ItemClassification.filler),
    # endregion
    # region Traps
    ToontownItemDefinition(ToontownItemName.UBER_TRAP,             ItemClassification.trap),
    ToontownItemDefinition(ToontownItemName.BEAN_TAX_TRAP_750,     ItemClassification.trap),
    ToontownItemDefinition(ToontownItemName.BEAN_TAX_TRAP_1000,    ItemClassification.trap),
    ToontownItemDefinition(ToontownItemName.BEAN_TAX_TRAP_1250,    ItemClassification.trap),
    ToontownItemDefinition(ToontownItemName.DRIP_TRAP,             ItemClassification.trap),
    ToontownItemDefinition(ToontownItemName.GAG_SHUFFLE_TRAP,      ItemClassification.trap),
    ToontownItemDefinition(ToontownItemName.DAMAGE_15,             ItemClassification.trap),
    ToontownItemDefinition(ToontownItemName.DAMAGE_25,             ItemClassification.trap),
    # endregion
    # region BossDefeatItems
    ToontownItemDefinition(ToontownItemName.VP,                   ItemClassification.progression_skip_balancing),
    ToontownItemDefinition(ToontownItemName.CFO,                  ItemClassification.progression_skip_balancing),
    ToontownItemDefinition(ToontownItemName.CJ,                   ItemClassification.progression_skip_balancing),
    ToontownItemDefinition(ToontownItemName.CEO,                  ItemClassification.progression_skip_balancing),
    # endregion
]

ITEM_DESCRIPTIONS = {
    ToontownItemName.SELLBOT_DISGUISE.value: "Grants access to fight the Sellbot VP",
    ToontownItemName.CASHBOT_DISGUISE.value: "Grants access to fight the Cashbot CFO",
    ToontownItemName.LAWBOT_DISGUISE.value:  "Grants access to fight the Lawbot CJ",
    ToontownItemName.BOSSBOT_DISGUISE.value: "Grants access to fight the Bossbot CEO",
    ToontownItemName.VP: "Rewarded for defeating the Sellbot VP", 
    ToontownItemName.CFO: "Rewarded for defeating the Cashbot CFO",
    ToontownItemName.CJ: "Rewarded for defeating the Lawbot CJ", 
    ToontownItemName.CEO: "Rewarded for defeating the Bossbot CEO",
}


for i in range(len(ITEM_DEFINITIONS)):
    ITEM_DEFINITIONS[i].unique_id = i + consts.BASE_ID

def hood_to_tp_item_name(hoodId: int) -> ToontownItemName:
    return {
        2000: ToontownItemName.TTC_ACCESS,
        1000: ToontownItemName.DD_ACCESS,
        5000: ToontownItemName.DG_ACCESS,
        4000: ToontownItemName.MML_ACCESS,
        3000: ToontownItemName.TB_ACCESS,
        9000: ToontownItemName.DDL_ACCESS,
        11000: ToontownItemName.SBHQ_ACCESS,
        12000: ToontownItemName.CBHQ_ACCESS,
        13000: ToontownItemName.LBHQ_ACCESS,
        10000: ToontownItemName.BBHQ_ACCESS,
        6000: ToontownItemName.AA_ACCESS,
        17000: ToontownItemName.AA_ACCESS,
        8000: ToontownItemName.GS_ACCESS,
    }.get(hoodId)


def get_item_def_from_id(_id: int) -> Optional[ToontownItemDefinition]:
    index = _id - consts.BASE_ID
    if 0 <= index < len(ITEM_DEFINITIONS):
        return ITEM_DEFINITIONS[index]
    return None

ITEM_NAME_TO_ID = {item.name.value: i + consts.BASE_ID for i, item in enumerate(ITEM_DEFINITIONS)}

FISHING_LICENSES = (
    ToontownItemName.TTC_FISHING,
    ToontownItemName.DD_FISHING,
    ToontownItemName.DG_FISHING,
    ToontownItemName.MML_FISHING,
    ToontownItemName.TB_FISHING,
    ToontownItemName.DDL_FISHING,
    # ToontownItemName.FISHING_ROD_UPGRADE
)
TELEPORT_ACCESS_ITEMS = (
    ToontownItemName.TTC_ACCESS,
    ToontownItemName.DD_ACCESS,
    ToontownItemName.DG_ACCESS,
    ToontownItemName.MML_ACCESS,
    ToontownItemName.TB_ACCESS,
    ToontownItemName.DDL_ACCESS,
    ToontownItemName.SBHQ_ACCESS,
    ToontownItemName.CBHQ_ACCESS,
    ToontownItemName.LBHQ_ACCESS,
    ToontownItemName.BBHQ_ACCESS,
    ToontownItemName.AA_ACCESS,
    ToontownItemName.GS_ACCESS,
)

DISGUISE_ITEMS = (
    ToontownItemName.SELLBOT_DISGUISE,
    ToontownItemName.CASHBOT_DISGUISE,
    ToontownItemName.LAWBOT_DISGUISE,
    ToontownItemName.BOSSBOT_DISGUISE
)

FACILITY_KEY_ITEMS = (
    ToontownItemName.FRONT_FACTORY_ACCESS,
    ToontownItemName.SIDE_FACTORY_ACCESS,
    ToontownItemName.COIN_MINT_ACCESS,
    ToontownItemName.DOLLAR_MINT_ACCESS,
    ToontownItemName.BULLION_MINT_ACCESS,
    ToontownItemName.A_OFFICE_ACCESS,
    ToontownItemName.B_OFFICE_ACCESS,
    ToontownItemName.C_OFFICE_ACCESS,
    ToontownItemName.D_OFFICE_ACCESS,
    ToontownItemName.FRONT_ONE_ACCESS,
    ToontownItemName.MIDDLE_TWO_ACCESS,
    ToontownItemName.BACK_THREE_ACCESS,
)

GAG_TRAINING_FRAMES = (
    ToontownItemName.TOONUP_FRAME,
    ToontownItemName.TRAP_FRAME,
    ToontownItemName.LURE_FRAME,
    ToontownItemName.SOUND_FRAME,
    ToontownItemName.THROW_FRAME,
    ToontownItemName.SQUIRT_FRAME,
    ToontownItemName.DROP_FRAME
)
GAG_UPGRADES = (
    ToontownItemName.TOONUP_UPGRADE,
    ToontownItemName.TRAP_UPGRADE,
    ToontownItemName.LURE_UPGRADE,
    ToontownItemName.SOUND_UPGRADE,
    ToontownItemName.THROW_UPGRADE,
    ToontownItemName.SQUIRT_UPGRADE,
    ToontownItemName.DROP_UPGRADE
)


def get_item_groups():
    GAG_CAPACITY = (
        ToontownItemName.GAG_CAPACITY_5,
        ToontownItemName.GAG_CAPACITY_10,
        ToontownItemName.GAG_CAPACITY_15
    )
    
    LAFF_BOOSTS = (
        ToontownItemName.LAFF_BOOST_1,
        ToontownItemName.LAFF_BOOST_2,
        ToontownItemName.LAFF_BOOST_3,
        ToontownItemName.LAFF_BOOST_4,
        ToontownItemName.LAFF_BOOST_5
    )

    DMG_BOOSTS = (
        ToontownItemName.DMG_BOOST_1,
        ToontownItemName.DMG_BOOST_2,
        ToontownItemName.DMG_BOOST_3,
        ToontownItemName.DMG_BOOST_4
    )

    TRAINING_BOOSTS = (
        ToontownItemName.GAG_MULTIPLIER_1,
        ToontownItemName.GAG_MULTIPLIER_2
    )

    ACTIVITY_KEYS = (
        ToontownItemName.GOLF_PUTTER,
        ToontownItemName.GO_KART
    )

    REWARD_BUNDLES = (
        ToontownItemName.SOS_REWARD_3,
        ToontownItemName.SOS_REWARD_4,
        ToontownItemName.SOS_REWARD_5,
        ToontownItemName.UNITE_REWARD_TOONUP,
        ToontownItemName.UNITE_REWARD_GAG,
        ToontownItemName.PINK_SLIP_REWARD,
        ToontownItemName.SUMMON_REWARD
    )

    HEALS = (
        ToontownItemName.HEAL_10,
        ToontownItemName.HEAL_20
    )

    TRAPS = (
        ToontownItemName.DRIP_TRAP,
        ToontownItemName.UBER_TRAP,
        ToontownItemName.BEAN_TAX_TRAP_1000,
        ToontownItemName.BEAN_TAX_TRAP_1250,
        ToontownItemName.BEAN_TAX_TRAP_750,
        ToontownItemName.GAG_SHUFFLE_TRAP,
        ToontownItemName.DAMAGE_15,
        ToontownItemName.DAMAGE_25,
    )

    COG_DISGUISES = (
        ToontownItemName.SELLBOT_DISGUISE,
        ToontownItemName.CASHBOT_DISGUISE,
        ToontownItemName.LAWBOT_DISGUISE,
        ToontownItemName.BOSSBOT_DISGUISE
    )

    GAG_EXP = (
        ToontownItemName.XP_10,
        ToontownItemName.XP_15,
        ToontownItemName.XP_20
    )

    JELLYBEANS = (
        ToontownItemName.MONEY_150,
        ToontownItemName.MONEY_400,
        ToontownItemName.MONEY_700,
        ToontownItemName.MONEY_1000
    )

    JELLYBEAN_CAPACITY = (
        ToontownItemName.MONEY_CAP_1000,
    )

    TASK_CAPACITY = (
        ToontownItemName.TASK_CAPACITY,
    )

    JOKE_BOOKS = (
        ToontownItemName.TTC_JOKE_BOOK,
        ToontownItemName.DD_JOKE_BOOK,
        ToontownItemName.DG_JOKE_BOOK,
        ToontownItemName.MML_JOKE_BOOK,
        ToontownItemName.TB_JOKE_BOOK,
        ToontownItemName.DDL_JOKE_BOOK,
    )

    ITEM_NAME_GROUPS_OBJECT = {
        "Cog Disguises": COG_DISGUISES,
        "Facility Keys": FACILITY_KEY_ITEMS,
        "Access Keys": TELEPORT_ACCESS_ITEMS,
        "Gag Training Frames": GAG_TRAINING_FRAMES,
        "Gag Capacity Increase": GAG_CAPACITY,
        "Gag Training Boosts": TRAINING_BOOSTS,
        "Gag Upgrades": GAG_UPGRADES,
        "Damage Boosts": DMG_BOOSTS,
        "Fishing Licenses": FISHING_LICENSES,
        "Jellybean Capacity": JELLYBEAN_CAPACITY,
        "Side Activity Keys": ACTIVITY_KEYS,
        "Task Capacity": TASK_CAPACITY,
        "Laff Boosts": LAFF_BOOSTS,
        "Reward Bundles": REWARD_BUNDLES,
        "Heals": HEALS,
        "Jellybeans": JELLYBEANS,
        "Gag Exp Reward": GAG_EXP,
        "Traps": TRAPS,
        "Joke Books": JOKE_BOOKS
    }

    return {k:[i.value for i in v] for k,v in ITEM_NAME_GROUPS_OBJECT.items()}
