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


    ### Reward Bundles ###
    SOS_REWARD       = "Random SOS Card"
    UNITE_REWARD     = "Random Unite"
    PINK_SLIP_REWARD = "Pink Slip Bundle"

    ### Traps ###
    UBER_TRAP = "Uber Trap"
    BEAN_TAX_TRAP_750 = "750 Bean Tax"
    BEAN_TAX_TRAP_1000 = "1000 Bean Tax"
    BEAN_TAX_TRAP_1250 = "1250 Bean Tax"
    DRIP_TRAP = "Drip Trap"
    GAG_SHUFFLE_TRAP = "Gag Shuffle Trap"


@dataclass
class ToontownItemDefinition:
    name: ToontownItemName
    classification: ItemClassification
    quantity: int = 0  # 0 implies manually/dynamically generated in World
    description: Optional[str] = None
    unique_id: int = 0


ITEM_DEFINITIONS: List[ToontownItemDefinition] = [
    # region Laff Boosts
    ToontownItemDefinition(ToontownItemName.LAFF_BOOST_1, ItemClassification.useful),
    ToontownItemDefinition(ToontownItemName.LAFF_BOOST_2, ItemClassification.useful),
    ToontownItemDefinition(ToontownItemName.LAFF_BOOST_3, ItemClassification.useful),
    ToontownItemDefinition(ToontownItemName.LAFF_BOOST_4, ItemClassification.useful),
    ToontownItemDefinition(ToontownItemName.LAFF_BOOST_5, ItemClassification.useful),
    # endregion
    # region Gag Capacity
    ToontownItemDefinition(ToontownItemName.GAG_CAPACITY_5,  ItemClassification.progression, quantity=12),  # NOTE: update values in has_collected_items_for_gag_level to match quantity
    ToontownItemDefinition(ToontownItemName.GAG_CAPACITY_10, ItemClassification.progression, quantity=2),  # NOTE: update values in has_collected_items_for_gag_level to match quantity
    ToontownItemDefinition(ToontownItemName.GAG_CAPACITY_15, ItemClassification.progression, quantity=0),  # NOTE: update values in has_collected_items_for_gag_level to match quantity
    # endregion
    # region Jellybean Capacity
    ToontownItemDefinition(ToontownItemName.MONEY_CAP_1000, ItemClassification.progression, quantity=9),
    # region Task Capacity
    # range depends on the starting capacity
    ToontownItemDefinition(ToontownItemName.TASK_CAPACITY, ItemClassification.progression),
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
    ToontownItemDefinition(ToontownItemName.GAG_MULTIPLIER_1, ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.GAG_MULTIPLIER_2, ItemClassification.progression),
    # endregion
    # region Fishing Items
    ToontownItemDefinition(ToontownItemName.FISHING_ROD_UPGRADE, ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.TTC_FISHING, ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.DD_FISHING,  ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.DG_FISHING,  ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.MML_FISHING, ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.TB_FISHING,  ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.DDL_FISHING, ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.FISH, ItemClassification.filler),
    # endregion
    # region Teleport Access
    ToontownItemDefinition(ToontownItemName.TTC_ACCESS, ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.DD_ACCESS, ItemClassification.progression, quantity=1),
    ToontownItemDefinition(ToontownItemName.DG_ACCESS, ItemClassification.progression, quantity=1),
    ToontownItemDefinition(ToontownItemName.MML_ACCESS, ItemClassification.progression, quantity=1),
    ToontownItemDefinition(ToontownItemName.TB_ACCESS, ItemClassification.progression, quantity=1),
    ToontownItemDefinition(ToontownItemName.DDL_ACCESS, ItemClassification.progression, quantity=1),
    ToontownItemDefinition(ToontownItemName.SBHQ_ACCESS, ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.CBHQ_ACCESS, ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.LBHQ_ACCESS, ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.BBHQ_ACCESS, ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.AA_ACCESS, ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.GS_ACCESS, ItemClassification.progression),
    # endregion
    # region Facility Access
    ToontownItemDefinition(ToontownItemName.FRONT_FACTORY_ACCESS, ItemClassification.progression, quantity=1),
    ToontownItemDefinition(ToontownItemName.SIDE_FACTORY_ACCESS,  ItemClassification.progression, quantity=1),
    ToontownItemDefinition(ToontownItemName.COIN_MINT_ACCESS,     ItemClassification.progression, quantity=1),
    ToontownItemDefinition(ToontownItemName.DOLLAR_MINT_ACCESS,   ItemClassification.progression, quantity=1),
    ToontownItemDefinition(ToontownItemName.BULLION_MINT_ACCESS,  ItemClassification.progression, quantity=1),
    ToontownItemDefinition(ToontownItemName.A_OFFICE_ACCESS,      ItemClassification.progression, quantity=1),
    ToontownItemDefinition(ToontownItemName.B_OFFICE_ACCESS,      ItemClassification.progression, quantity=1),
    ToontownItemDefinition(ToontownItemName.C_OFFICE_ACCESS,      ItemClassification.progression, quantity=1),
    ToontownItemDefinition(ToontownItemName.D_OFFICE_ACCESS,      ItemClassification.progression, quantity=1),
    ToontownItemDefinition(ToontownItemName.FRONT_ONE_ACCESS,   ItemClassification.progression, quantity=1),
    ToontownItemDefinition(ToontownItemName.MIDDLE_TWO_ACCESS,  ItemClassification.progression, quantity=1),
    ToontownItemDefinition(ToontownItemName.BACK_THREE_ACCESS,    ItemClassification.progression, quantity=1),
    # endregion
    # region Boss Disguises
    ToontownItemDefinition(ToontownItemName.SELLBOT_DISGUISE, ItemClassification.progression, quantity=1),
    ToontownItemDefinition(ToontownItemName.CASHBOT_DISGUISE, ItemClassification.progression, quantity=1),
    ToontownItemDefinition(ToontownItemName.LAWBOT_DISGUISE,  ItemClassification.progression, quantity=1),
    ToontownItemDefinition(ToontownItemName.BOSSBOT_DISGUISE, ItemClassification.progression, quantity=1),
    # endregion
    # region Filler Items
    # TODO - remember to account for the Fish filler when implementing weights here
    ToontownItemDefinition(ToontownItemName.MONEY_150,        ItemClassification.filler),
    ToontownItemDefinition(ToontownItemName.MONEY_400,        ItemClassification.filler),
    ToontownItemDefinition(ToontownItemName.MONEY_700,       ItemClassification.filler),
    ToontownItemDefinition(ToontownItemName.MONEY_1000,       ItemClassification.filler),
    ToontownItemDefinition(ToontownItemName.XP_10,           ItemClassification.filler),
    ToontownItemDefinition(ToontownItemName.XP_15,          ItemClassification.filler),
    ToontownItemDefinition(ToontownItemName.XP_20,          ItemClassification.filler),
    ToontownItemDefinition(ToontownItemName.SOS_REWARD,       ItemClassification.filler),
    ToontownItemDefinition(ToontownItemName.UNITE_REWARD,     ItemClassification.filler),
    ToontownItemDefinition(ToontownItemName.PINK_SLIP_REWARD, ItemClassification.filler),
    # endregion
    # region Traps
    ToontownItemDefinition(ToontownItemName.UBER_TRAP,        ItemClassification.trap),
    ToontownItemDefinition(ToontownItemName.BEAN_TAX_TRAP_750,    ItemClassification.trap),
    ToontownItemDefinition(ToontownItemName.BEAN_TAX_TRAP_1000,    ItemClassification.trap),
    ToontownItemDefinition(ToontownItemName.BEAN_TAX_TRAP_1250,    ItemClassification.trap),
    ToontownItemDefinition(ToontownItemName.DRIP_TRAP,        ItemClassification.trap),
    ToontownItemDefinition(ToontownItemName.GAG_SHUFFLE_TRAP, ItemClassification.trap),
    # endregion
]

ITEM_DESCRIPTIONS = {
    ToontownItemName.SELLBOT_DISGUISE.value: "Grants access to fight the Sellbot VP",
    ToontownItemName.CASHBOT_DISGUISE.value: "Grants access to fight the Cashbot CFO",
    ToontownItemName.LAWBOT_DISGUISE.value:  "Grants access to fight the Lawbot CJ",
    ToontownItemName.BOSSBOT_DISGUISE.value: "Grants access to fight the Bossbot CEO",
}


for i in range(len(ITEM_DEFINITIONS)):
    ITEM_DEFINITIONS[i].unique_id = i + consts.BASE_ID

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

FISHING_LICENSES = (
    ToontownItemName.TTC_FISHING,
    ToontownItemName.DD_FISHING,
    ToontownItemName.DG_FISHING,
    ToontownItemName.MML_FISHING,
    ToontownItemName.TB_FISHING,
    ToontownItemName.DDL_FISHING,
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


JUNK_WEIGHTS = {
    ToontownItemName.MONEY_150:        0.5,
    ToontownItemName.MONEY_400:        0.5,
    ToontownItemName.MONEY_700:        0.5,
    ToontownItemName.MONEY_1000:        0.5,

    ToontownItemName.XP_10:            0.7,
    ToontownItemName.XP_15:            0.5,
    ToontownItemName.XP_20:            0.3,

    ToontownItemName.SOS_REWARD:       0.65,
    ToontownItemName.UNITE_REWARD:     0.65,
    ToontownItemName.PINK_SLIP_REWARD: 0.65,
}


def get_item_def_from_id(_id: int) -> Optional[ToontownItemDefinition]:
    index = _id - consts.BASE_ID
    if 0 <= index < len(ITEM_DEFINITIONS):
        return ITEM_DEFINITIONS[index]
    return None


def random_junk() -> ToontownItemName:
    JUNK_ITEMS = list(JUNK_WEIGHTS.keys())
    return random.choices(JUNK_ITEMS, weights=[JUNK_WEIGHTS[i] for i in JUNK_ITEMS])[0]


ITEM_NAME_TO_ID = {item.name.value: i + consts.BASE_ID for i, item in enumerate(ITEM_DEFINITIONS)}
