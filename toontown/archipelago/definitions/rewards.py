# Represents logic for what to do when we are given an item from AP
from toontown.archipelago.definitions import items
from toontown.archipelago.definitions.items import ToontownItemDefinition
from toontown.coghq.CogDisguiseGlobals import PartsPerSuitBitmasks
from toontown.fishing import FishGlobals
from toontown.toonbase import ToontownGlobals, TTLocalizer

# Typing hack, can remove later
TYPING = False
if TYPING:
    from toontown.toon.DistributedToonAI import DistributedToonAI


class APReward:
    def apply(self, av: "DistributedToonAI"):
        raise NotImplementedError("Please implement the apply() method!")


class LaffBoostReward(APReward):
    def __init__(self, amount: int):
        self.amount = amount

    def apply(self, av: "DistributedToonAI"):
        av.b_setMaxHp(av.maxHp+self.amount)
        av.toonUp(self.amount)
        av.d_setSystemMessage(0, f"Increased your max laff by {self.amount}!")


class GagCapacityReward(APReward):

    def __init__(self, amount: int):
        self.amount: int = amount

    def apply(self, av: "DistributedToonAI"):
        av.b_setMaxCarry(av.maxCarry + self.amount)
        av.d_setSystemMessage(0, f"Increased your gag pouch capacity by {self.amount}!")


class JellybeanJarUpgradeReward(APReward):

    def __init__(self, amount: int):
        self.amount: int = amount

    def apply(self, av: "DistributedToonAI"):
        av.b_setMaxMoney(av.maxMoney + self.amount)
        av.d_setSystemMessage(0, f"Increased your jellybean jar capacity by {self.amount}!")


class GagTrainingFrameReward(APReward):

    TOONUP = 0
    TRAP = 1
    LURE = 2
    SOUND = 3
    THROW = 4
    SQUIRT = 5
    DROP = 6

    TRACK_TO_NAME = {
        TOONUP: "Toon-Up",
        TRAP: "Trap",
        LURE: "Lure",
        SOUND: "Sound",
        THROW: "Throw",
        SQUIRT: "Squirt",
        DROP: "Drop",
    }

    def __init__(self, track):
        self.track = track

    def apply(self, av: "DistributedToonAI"):

        # Increment track access level by 1
        oldLevel = av.getTrackAccessLevel(self.track)
        newLevel = oldLevel+1

        # If we get a frame when we already maxed, make the track organic
        if newLevel > 7:
            oldBonusArray = av.getTrackBonusLevel()
            newBonusArray = oldBonusArray[self.track] = 7
            av.b_setTrackBonusLevel(newBonusArray)
            av.d_setSystemMessage(0, f"Your {self.TRACK_TO_NAME[self.track]} gags are now organic!")
            return

        # Otherwise increment the gag level allowed
        av.setTrackAccessLevel(self.track, newLevel)
        av.d_setSystemMessage(0, f"You can now train {self.TRACK_TO_NAME[self.track]} gags up to {newLevel}!")


class GagTrainingMultiplierReward(APReward):

    def __init__(self, amount: int):
        self.amount: int = amount

    def apply(self, av: "DistributedToonAI"):
        oldMultiplier = av.getBaseGagSkillMultiplier()
        newMultiplier = oldMultiplier + self.amount
        av.b_setBaseGagSkillMultiplier(newMultiplier)
        av.d_setSystemMessage(0, f"Your base gag XP multiplier is now {newMultiplier}x!")


class FishingRodUpgradeReward(APReward):

    def apply(self, av: "DistributedToonAI"):

        nextRodID = min(av.fishingRod+1, FishGlobals.MaxRodId)

        av.b_setFishingRod(nextRodID)
        av.d_setSystemMessage(0, f"Upgraded your fishing rod!")


class TeleportAccessUpgradeReward(APReward):

    TOONTOWN_CENTRAL = ToontownGlobals.ToontownCentral
    DONALDS_DOCK = ToontownGlobals.DonaldsDock
    DAISYS_GARDENS = ToontownGlobals.DaisyGardens
    MINNIES_MELODYLAND = ToontownGlobals.MinniesMelodyland
    THE_BRRRGH = ToontownGlobals.TheBrrrgh
    DONALDS_DREAMLAND = ToontownGlobals.DonaldsDreamland

    SELLBOT_HQ = ToontownGlobals.SellbotHQ
    CASHBOT_HQ = ToontownGlobals.CashbotHQ
    LAWBOT_HQ = ToontownGlobals.LawbotHQ
    BOSSBOT_HQ = ToontownGlobals.BossbotHQ

    ZONE_TO_DISPLAY_NAME = {
        TOONTOWN_CENTRAL: "Toontown Central",
        DONALDS_DOCK: "Donald's Dock",
        DAISYS_GARDENS: "Daisy's Gardens",
        MINNIES_MELODYLAND: "Minnie's Melodyland",
        THE_BRRRGH: "The Brrrgh",
        DONALDS_DREAMLAND: "Donald's Dreamland",
        SELLBOT_HQ: "Sellbot HQ",
        CASHBOT_HQ: "Cashbot HQ",
        LAWBOT_HQ: "Lawbot HQ",
        BOSSBOT_HQ: "Bossbot HQ",
    }

    def __init__(self, playground: int):
        self.playground: int = playground

    def apply(self, av: "DistributedToonAI"):
        av.addTeleportAccess(self.playground)
        av.d_setSystemMessage(0, f"You can now teleport to {self.ZONE_TO_DISPLAY_NAME.get(self.playground, 'unknown zone: ' + str(self.playground))}!")


class TaskAccessReward(APReward):

    TOONTOWN_CENTRAL = ToontownGlobals.ToontownCentral
    DONALDS_DOCK = ToontownGlobals.DonaldsDock
    DAISYS_GARDENS = ToontownGlobals.DaisyGardens
    MINNIES_MELODYLAND = ToontownGlobals.MinniesMelodyland
    THE_BRRRGH = ToontownGlobals.TheBrrrgh
    DONALDS_DREAMLAND = ToontownGlobals.DonaldsDreamland

    ZONE_TO_DISPLAY_NAME = {
        TOONTOWN_CENTRAL: "Toontown Central",
        DONALDS_DOCK: "Donald's Dock",
        DAISYS_GARDENS: "Daisy's Gardens",
        MINNIES_MELODYLAND: "Minnie's Melodyland",
        THE_BRRRGH: "The Brrrgh",
        DONALDS_DREAMLAND: "Donald's Dreamland",
    }

    def __init__(self, playground: int):
        self.playground: int = playground

    def apply(self, av: "DistributedToonAI"):
        av.d_setSystemMessage(0, f"todo you can now task in {self.playground}")


class FacilityAccessReward(APReward):

    # todo add correct IDs

    FRONT_FACTORY = 0
    SIDE_FACTORY = 1

    COIN_MINT = 2
    DOLLAR_MINT = 3
    BULLION_MINT = 4

    OFFICE_A = 5
    OFFICE_B = 6
    OFFICE_C = 7
    OFFICE_D = 8

    FRONT_THREE = 9
    MIDDLE_THREE = 10
    BACK_THREE = 11

    FACILITY_ID_TO_DISPLAY = {
        FRONT_FACTORY: "Front Factory",
        SIDE_FACTORY: "Side Factory",

        COIN_MINT: "Coin Mint",
        DOLLAR_MINT: "Dollar Mint",
        BULLION_MINT: "Bullion Mint",

        OFFICE_A: "Office A",
        OFFICE_B: "Office B",
        OFFICE_C: "Office C",
        OFFICE_D: "Office D",

        FRONT_THREE: "Front Three",
        MIDDLE_THREE: "Middle Three",
        BACK_THREE: "Back Three",
    }

    def __init__(self, facilityID):
        self.facilityID = facilityID

    def apply(self, av: "DistributedToonAI"):
        av.d_setSystemMessage(0, f"todo you can now access facility: {self.FACILITY_ID_TO_DISPLAY.get(self.facilityID, 'Unknown facility: ' + str(self.facilityID))}")


class CogDisguiseReward(APReward):

    BOSSBOT = 0
    LAWBOT = 1
    CASHBOT = 2
    SELLBOT = 3

    ENUM_TO_NAME = {
        BOSSBOT: "Bossbot",
        LAWBOT: "Lawbot",
        CASHBOT: "Cashbot",
        SELLBOT: "Sellbot",
    }

    # When instantiating this, use the attributes defined above, i'm not here to fix shit toontown code
    def __init__(self, dept: int):
        self.dept: int = dept

    def apply(self, av: "DistributedToonAI"):
        av.b_setCogParts(PartsPerSuitBitmasks[self.dept])
        av.d_setSystemMessage(0, f"You were given your {self.ENUM_TO_NAME[self.dept]} disguise!")


class JellybeanReward(APReward):

    def __init__(self, amount: int):
        self.amount: int = amount

    def apply(self, av: "DistributedToonAI"):
        av.addMoney(self.amount)
        av.d_setSystemMessage(0, f"You were given {self.amount} jellybeans!")


class UndefinedReward(APReward):

    def __init__(self, desc):
        self.desc = desc

    def apply(self, av: "DistributedToonAI"):
        av.d_setSystemMessage(0, f"Unknown AP reward: {self.desc}")


ITEM_NAME_TO_AP_REWARD: [str, APReward] = {
    items.ITEM_1_LAFF_BOOST: LaffBoostReward(1),
    items.ITEM_2_LAFF_BOOST: LaffBoostReward(2),
    items.ITEM_3_LAFF_BOOST: LaffBoostReward(3),
    items.ITEM_4_LAFF_BOOST: LaffBoostReward(4),
    items.ITEM_5_LAFF_BOOST: LaffBoostReward(5),

    items.ITEM_10_GAG_CAPACITY: GagCapacityReward(10),
    items.ITEM_15_GAG_CAPACITY: GagCapacityReward(15),
    items.ITEM_20_GAG_CAPACITY: GagCapacityReward(20),

    items.ITEM_150_MONEY_CAP: JellybeanJarUpgradeReward(150),
    items.ITEM_250_MONEY_CAP: JellybeanJarUpgradeReward(250),
    items.ITEM_500_MONEY_CAP: JellybeanJarUpgradeReward(500),
    items.ITEM_750_MONEY_CAP: JellybeanJarUpgradeReward(750),
    items.ITEM_1000_MONEY_CAP: JellybeanJarUpgradeReward(1000),
    items.ITEM_1250_MONEY_CAP: JellybeanJarUpgradeReward(1250),

    items.ITEM_TOONUP_FRAME: GagTrainingFrameReward(GagTrainingFrameReward.TOONUP),
    items.ITEM_TRAP_FRAME: GagTrainingFrameReward(GagTrainingFrameReward.TRAP),
    items.ITEM_LURE_FRAME: GagTrainingFrameReward(GagTrainingFrameReward.LURE),
    items.ITEM_SOUND_FRAME: GagTrainingFrameReward(GagTrainingFrameReward.SOUND),
    items.ITEM_THROW_FRAME: GagTrainingFrameReward(GagTrainingFrameReward.THROW),
    items.ITEM_SQUIRT_FRAME: GagTrainingFrameReward(GagTrainingFrameReward.SQUIRT),
    items.ITEM_DROP_FRAME: GagTrainingFrameReward(GagTrainingFrameReward.DROP),

    items.ITEM_1_GAG_MULTIPLIER: GagTrainingMultiplierReward(1),
    items.ITEM_2_GAG_MULTIPLIER: GagTrainingMultiplierReward(2),

    items.ITEM_FISHING_ROD_UPGRADE: FishingRodUpgradeReward(),

    items.ITEM_TTC_TELEPORT: TeleportAccessUpgradeReward(TeleportAccessUpgradeReward.TOONTOWN_CENTRAL),
    items.ITEM_DD_TELEPORT: TeleportAccessUpgradeReward(TeleportAccessUpgradeReward.DONALDS_DOCK),
    items.ITEM_DG_TELEPORT: TeleportAccessUpgradeReward(TeleportAccessUpgradeReward.DAISYS_GARDENS),
    items.ITEM_MML_TELEPORT: TeleportAccessUpgradeReward(TeleportAccessUpgradeReward.MINNIES_MELODYLAND),
    items.ITEM_TB_TELEPORT: TeleportAccessUpgradeReward(TeleportAccessUpgradeReward.THE_BRRRGH),
    items.ITEM_DDL_TELEPORT: TeleportAccessUpgradeReward(TeleportAccessUpgradeReward.DONALDS_DREAMLAND),

    items.ITEM_SBHQ_TELEPORT: TeleportAccessUpgradeReward(TeleportAccessUpgradeReward.SELLBOT_HQ),
    items.ITEM_CBHQ_TELEPORT: TeleportAccessUpgradeReward(TeleportAccessUpgradeReward.CASHBOT_HQ),
    items.ITEM_LBHQ_TELEPORT: TeleportAccessUpgradeReward(TeleportAccessUpgradeReward.LAWBOT_HQ),
    items.ITEM_BBHQ_TELEPORT: TeleportAccessUpgradeReward(TeleportAccessUpgradeReward.BOSSBOT_HQ),

    items.ITEM_DD_HQ_ACCESS: TaskAccessReward(TaskAccessReward.DONALDS_DOCK),
    items.ITEM_DG_HQ_ACCESS: TaskAccessReward(TaskAccessReward.DAISYS_GARDENS),
    items.ITEM_MML_HQ_ACCESS: TaskAccessReward(TaskAccessReward.MINNIES_MELODYLAND),
    items.ITEM_TB_HQ_ACCESS: TaskAccessReward(TaskAccessReward.THE_BRRRGH),
    items.ITEM_DDL_HQ_ACCESS: TaskAccessReward(TaskAccessReward.DONALDS_DREAMLAND),

    items.ITEM_FRONT_FACTORY_ACCESS: FacilityAccessReward(FacilityAccessReward.FRONT_FACTORY),
    items.ITEM_SIDE_FACTORY_ACCESS: FacilityAccessReward(FacilityAccessReward.SIDE_FACTORY),

    items.ITEM_COIN_MINT_ACCESS: FacilityAccessReward(FacilityAccessReward.COIN_MINT),
    items.ITEM_DOLLAR_MINT_ACCESS: FacilityAccessReward(FacilityAccessReward.DOLLAR_MINT),
    items.ITEM_BULLION_MINT_ACCESS: FacilityAccessReward(FacilityAccessReward.BULLION_MINT),

    items.ITEM_A_OFFICE_ACCESS: FacilityAccessReward(FacilityAccessReward.OFFICE_A),
    items.ITEM_B_OFFICE_ACCESS: FacilityAccessReward(FacilityAccessReward.OFFICE_B),
    items.ITEM_C_OFFICE_ACCESS: FacilityAccessReward(FacilityAccessReward.OFFICE_C),
    items.ITEM_D_OFFICE_ACCESS: FacilityAccessReward(FacilityAccessReward.OFFICE_D),

    items.ITEM_FRONT_THREE_ACCESS: FacilityAccessReward(FacilityAccessReward.FRONT_THREE),
    items.ITEM_MIDDLE_THREE_ACCESS: FacilityAccessReward(FacilityAccessReward.MIDDLE_THREE),
    items.ITEM_BACK_THREE_ACCESS: FacilityAccessReward(FacilityAccessReward.BACK_THREE),

    items.ITEM_SELLBOT_DISGUISE: CogDisguiseReward(CogDisguiseReward.SELLBOT),
    items.ITEM_CASHBOT_DISGUISE: CogDisguiseReward(CogDisguiseReward.CASHBOT),
    items.ITEM_LAWBOT_DISGUISE: CogDisguiseReward(CogDisguiseReward.LAWBOT),
    items.ITEM_BOSSBOT_DISGUISE: CogDisguiseReward(CogDisguiseReward.BOSSBOT),

    items.ITEM_250_MONEY: JellybeanReward(250),
    items.ITEM_500_MONEY: JellybeanReward(500),
    items.ITEM_1000_MONEY: JellybeanReward(1000),
    items.ITEM_2000_MONEY: JellybeanReward(2000),
}


def get_ap_reward_from_name(name: str) -> APReward:
    return ITEM_NAME_TO_AP_REWARD.get(name, UndefinedReward(name))


# The id we are given from a packet from archipelago
def get_ap_reward_from_id(_id: int) -> APReward:
    definition = items.ID_TO_ITEM_DEFINITION.get(_id, None)

    if not definition:
        return UndefinedReward(_id)

    ap_reward: APReward = ITEM_NAME_TO_AP_REWARD.get(definition.unique_name)

    if not ap_reward:
        ap_reward = UndefinedReward(definition.unique_name)

    return ap_reward

