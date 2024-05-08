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

    ### Gag Capacity ###
    GAG_CAPACITY_5  = "+5 Gag Capacity"
    GAG_CAPACITY_10 = "+10 Gag Capacity"
    GAG_CAPACITY_15 = "+15 Gag Capacity"

    ### Gag Multiplier ###
    GAG_MULTIPLIER_1 = "+1 Base Gag XP Multiplier"
    GAG_MULTIPLIER_2 = "+2 Base Gag XP Multiplier"

    ### Teleport Access ###
    TTC_TELEPORT  = "TTC TP Access"
    DD_TELEPORT   = "DD TP Access"
    DG_TELEPORT   = "DG TP Access"
    MML_TELEPORT  = "MML TP Access"
    TB_TELEPORT   = "TB TP Access"
    DDL_TELEPORT  = "DDL TP Access"
    SBHQ_TELEPORT = "SBHQ TP Access"
    CBHQ_TELEPORT = "CBHQ TP Access"
    LBHQ_TELEPORT = "LBHQ TP Access"
    BBHQ_TELEPORT = "BBHQ TP Access"

    AA_TELEPORT = "AA TP Access"
    GS_TELEPORT = 'GS TP Access'

    ### HQ Access ###
    TTC_HQ_ACCESS = "TTC HQ Access"
    DD_HQ_ACCESS  = "DD HQ Access"
    DG_HQ_ACCESS  = "DG HQ Access"
    MML_HQ_ACCESS = "MML HQ Access"
    TB_HQ_ACCESS  = "TB HQ Access"
    DDL_HQ_ACCESS = "DDL HQ Access"

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
    MONEY_300  = "300 Jellybeans"
    MONEY_500 = "500 Jellybeans"
    MONEY_750 = "750 Jellybeans"

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
    ToontownItemDefinition(ToontownItemName.TTC_TELEPORT,  ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.DD_TELEPORT,   ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.DG_TELEPORT,   ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.MML_TELEPORT,  ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.TB_TELEPORT,   ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.DDL_TELEPORT,  ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.SBHQ_TELEPORT, ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.CBHQ_TELEPORT, ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.LBHQ_TELEPORT, ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.BBHQ_TELEPORT, ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.AA_TELEPORT,   ItemClassification.progression),
    ToontownItemDefinition(ToontownItemName.GS_TELEPORT,   ItemClassification.progression),
    # endregion
    # region Tasking Access (Playground HQ entry access)
    ToontownItemDefinition(ToontownItemName.TTC_HQ_ACCESS, ItemClassification.progression),  # Given as a starting item ATM
    ToontownItemDefinition(ToontownItemName.DD_HQ_ACCESS,  ItemClassification.progression, quantity=1),
    ToontownItemDefinition(ToontownItemName.DG_HQ_ACCESS,  ItemClassification.progression, quantity=1),
    ToontownItemDefinition(ToontownItemName.MML_HQ_ACCESS, ItemClassification.progression, quantity=1),
    ToontownItemDefinition(ToontownItemName.TB_HQ_ACCESS,  ItemClassification.progression, quantity=1),
    ToontownItemDefinition(ToontownItemName.DDL_HQ_ACCESS, ItemClassification.progression, quantity=1),
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
    ToontownItemDefinition(ToontownItemName.MONEY_300,        ItemClassification.filler),
    ToontownItemDefinition(ToontownItemName.MONEY_500,       ItemClassification.filler),
    ToontownItemDefinition(ToontownItemName.MONEY_750,       ItemClassification.filler),
    ToontownItemDefinition(ToontownItemName.XP_10,           ItemClassification.filler),
    ToontownItemDefinition(ToontownItemName.XP_15,          ItemClassification.filler),
    ToontownItemDefinition(ToontownItemName.XP_20,          ItemClassification.filler),
    ToontownItemDefinition(ToontownItemName.SOS_REWARD,       ItemClassification.filler),
    ToontownItemDefinition(ToontownItemName.UNITE_REWARD,     ItemClassification.filler),
    ToontownItemDefinition(ToontownItemName.PINK_SLIP_REWARD, ItemClassification.filler),
    # endregion
    # region Traps
    ToontownItemDefinition(ToontownItemName.UBER_TRAP,        ItemClassification.trap),
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

FISHING_LICENSES = (
    ToontownItemName.TTC_FISHING,
    ToontownItemName.DD_FISHING,
    ToontownItemName.DG_FISHING,
    ToontownItemName.MML_FISHING,
    ToontownItemName.TB_FISHING,
    ToontownItemName.DDL_FISHING,
)
TELEPORT_ACCESS_ITEMS = (
    ToontownItemName.TTC_TELEPORT,
    ToontownItemName.DD_TELEPORT,
    ToontownItemName.DG_TELEPORT,
    ToontownItemName.MML_TELEPORT,
    ToontownItemName.TB_TELEPORT,
    ToontownItemName.DDL_TELEPORT,
    ToontownItemName.SBHQ_TELEPORT,
    ToontownItemName.CBHQ_TELEPORT,
    ToontownItemName.LBHQ_TELEPORT,
    ToontownItemName.BBHQ_TELEPORT,
    ToontownItemName.AA_TELEPORT,
    ToontownItemName.GS_TELEPORT,
)


def hood_to_tp_item_name(hoodId: int) -> ToontownItemName:
    return {
        2000: ToontownItemName.TTC_TELEPORT,
        1000: ToontownItemName.DD_TELEPORT,
        5000: ToontownItemName.DG_TELEPORT,
        4000: ToontownItemName.MML_TELEPORT,
        3000: ToontownItemName.TB_TELEPORT,
        9000: ToontownItemName.DDL_TELEPORT,
        11000: ToontownItemName.SBHQ_TELEPORT,
        12000: ToontownItemName.CBHQ_TELEPORT,
        13000: ToontownItemName.LBHQ_TELEPORT,
        10000: ToontownItemName.BBHQ_TELEPORT,
        6000: ToontownItemName.AA_TELEPORT,
        17000: ToontownItemName.AA_TELEPORT,
        8000: ToontownItemName.GS_TELEPORT,
    }.get(hoodId)


JUNK_WEIGHTS = {
    ToontownItemName.MONEY_150:        0.5,
    ToontownItemName.MONEY_300:        0.5,
    ToontownItemName.MONEY_500:        0.5,
    ToontownItemName.MONEY_750:        0.5,

    ToontownItemName.XP_10:            0.7,
    ToontownItemName.XP_15:            0.5,
    ToontownItemName.XP_20:            0.3,

    ToontownItemName.SOS_REWARD:       0.65,
    ToontownItemName.UNITE_REWARD:     0.65,
    ToontownItemName.PINK_SLIP_REWARD: 0.65,
}
TRAP_WEIGHTS = {
    ToontownItemName.UBER_TRAP:        1.0,
    ToontownItemName.DRIP_TRAP:        0.5,
    ToontownItemName.GAG_SHUFFLE_TRAP: 1.0,
}


def get_item_def_from_id(_id: int) -> Optional[ToontownItemDefinition]:
    index = _id - consts.BASE_ID
    if 0 <= index < len(ITEM_DEFINITIONS):
        return ITEM_DEFINITIONS[index]
    return None


def random_junk() -> ToontownItemName:
    JUNK_ITEMS = list(JUNK_WEIGHTS.keys())
    return random.choices(JUNK_ITEMS, weights=[JUNK_WEIGHTS[i] for i in JUNK_ITEMS])[0]


def random_trap() -> ToontownItemName:
    TRAP_ITEMS = list(TRAP_WEIGHTS.keys())
    return random.choices(TRAP_ITEMS, weights=[TRAP_WEIGHTS[i] for i in TRAP_ITEMS])[0]


ITEM_NAME_TO_ID = {item.name.value: i + consts.BASE_ID for i, item in enumerate(ITEM_DEFINITIONS)}
