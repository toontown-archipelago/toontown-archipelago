# Represents logic for what to do when we are given an item from AP
from enum import IntEnum

import random

from apworld.toontown import items

from toontown.building import FADoorCodes
from toontown.coghq.CogDisguiseGlobals import PartsPerSuitBitmasks
from toontown.fishing import FishGlobals
from toontown.toonbase import ToontownBattleGlobals
from toontown.toonbase import ToontownGlobals
from toontown.toon import NPCToons
from toontown.chat import ResistanceChat

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
        av.b_setMaxHp(av.maxHp + self.amount)
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
        newLevel = oldLevel + 1

        bonusArray = av.getTrackBonusLevel()

        # If we get a frame when we already maxed, make the track organic. No need to do anything else
        if newLevel > 7:
            bonusArray[self.track] = 7
            av.b_setTrackBonusLevel(bonusArray)
            av.d_setSystemMessage(0, f"Your {self.TRACK_TO_NAME[self.track]} gags are now organic!")
            return

        # Before we do anything, we need to see if they were capped before this so we can award them gags later
        wasCapped = av.experience.getExp(self.track) == av.experience.getExperienceCapForTrack(self.track)

        # Otherwise increment the gag level allowed and make sure it is not organic
        av.setTrackAccessLevel(self.track, newLevel)
        bonusArray[self.track] = -1
        av.b_setTrackBonusLevel(bonusArray)

        # Consider the case where we just learned a new gag track, we should give them as many of them as possible
        if newLevel == 1:
            av.inventory.addItemsWithListMax([(self.track, 0)])
            av.b_setInventory(av.inventory.makeNetString())
        # Now consider the case where we were maxed previously and want to upgrade by giving 1 xp and giving new gags
        # This will also trigger the new gag check to unlock :3
        elif wasCapped:
            av.experience.addExp(track=self.track, amount=1)  # Give them enough xp to learn the gag :)
            av.b_setExperience(av.experience.getCurrentExperience())
            av.inventory.addItemsWithListMax([self.track, newLevel-1])  # Give the new gags!!
            av.b_setInventory(av.inventory.makeNetString())

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
        nextRodID = min(av.fishingRod + 1, FishGlobals.MaxRodId)

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
        DAISYS_GARDENS: "Daisy Gardens",
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
        av.d_setSystemMessage(0,
                              f"You can now teleport to {self.ZONE_TO_DISPLAY_NAME.get(self.playground, 'unknown zone: ' + str(self.playground))}!")


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
        DAISYS_GARDENS: "Daisy Gardens",
        MINNIES_MELODYLAND: "Minnie's Melodyland",
        THE_BRRRGH: "The Brrrgh",
        DONALDS_DREAMLAND: "Donald's Dreamland",
    }

    def __init__(self, playground: int):
        self.playground: int = playground

    def apply(self, av: "DistributedToonAI"):
        # Get the key ID for this playground
        key = FADoorCodes.ZONE_TO_ACCESS_CODE[self.playground]
        av.addAccessKey(key)
        av.d_setSystemMessage(0,f"You have been given {self.ZONE_TO_DISPLAY_NAME.get(self.playground, 'UNKNOWN PG ' + str(self.playground))} HQ Clearance and can now complete toontasks there!")


class FacilityAccessReward(APReward):
    FACILITY_ID_TO_DISPLAY = {
        FADoorCodes.FRONT_FACTORY_ACCESS_MISSING: "Front Factory",
        FADoorCodes.SIDE_FACTORY_ACCESS_MISSING: "Side Factory",

        FADoorCodes.COIN_MINT_ACCESS_MISSING: "Coin Mint",
        FADoorCodes.DOLLAR_MINT_ACCESS_MISSING: "Dollar Mint",
        FADoorCodes.BULLION_MINT_ACCESS_MISSING: "Bullion Mint",

        FADoorCodes.OFFICE_A_ACCESS_MISSING: "Office A",
        FADoorCodes.OFFICE_B_ACCESS_MISSING: "Office B",
        FADoorCodes.OFFICE_C_ACCESS_MISSING: "Office C",
        FADoorCodes.OFFICE_D_ACCESS_MISSING: "Office D",

        FADoorCodes.FRONT_THREE_ACCESS_MISSING: "Front One",
        FADoorCodes.MIDDLE_SIX_ACCESS_MISSING: "Middle Two",
        FADoorCodes.BACK_NINE_ACCESS_MISSING: "Back Three",
    }

    def __init__(self, key):
        self.key = key

    def apply(self, av: "DistributedToonAI"):
        # Get the key ID for this playground
        av.addAccessKey(self.key)
        key_name = self.FACILITY_ID_TO_DISPLAY.get(self.key, f"UNKNOWN-KEY[{self.key}]")
        av.d_setSystemMessage(0, f"You have been given a {key_name} key and can now infiltrate this facility!")


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
        parts = av.getCogParts()
        parts[self.dept] = PartsPerSuitBitmasks[self.dept]
        av.b_setCogParts(parts)
        av.d_setSystemMessage(0, f"You were given your {self.ENUM_TO_NAME[self.dept]} disguise!")


class JellybeanReward(APReward):

    def __init__(self, amount: int):
        self.amount: int = amount

    def apply(self, av: "DistributedToonAI"):
        av.addMoney(self.amount)
        av.d_setSystemMessage(0, f"You were given {self.amount} jellybeans!")


class UberTrapAward(APReward):

    def apply(self, av: "DistributedToonAI"):
        av.playSound('phase_4/audio/sfx/avatar_emotion_very_sad.ogg')
        av.b_setHp(15)
        av.inventory.NPCMaxOutInv(maxLevel=6)
        av.b_setInventory(av.inventory.makeNetString())
        av.d_setSystemMessage(0, "Don't get hit!")


class DripTrapAward(APReward):

    def apply(self, av: "DistributedToonAI"):
        av.playSound('phase_4/audio/sfx/avatar_emotion_drip.ogg')
        av.b_setShoes(1, random.randint(1, 48), 0)
        av.b_setBackpack(random.randint(1, 24), 0, 0)
        av.b_setGlasses(random.randint(1, 21), 0, 0)
        av.b_setHat(random.randint(1, 56), 0, 0)
        av.d_setSystemMessage(0, "Did someone say the door to drip?")

class GagExpBundleAward(APReward):

    def __init__(self, amount: int):
        self.amount: int = amount

    def apply(self, av: "DistributedToonAI"):
        for index, _ in enumerate(ToontownBattleGlobals.Tracks):
            av.experience.addExp(index, self.amount)
        av.b_setExperience(av.experience.getCurrentExperience())
        av.d_setSystemMessage(0, f"You were given a bundle of {self.amount} gag experience!")


class BossRewardAward(APReward):
    SOS = 0
    UNITE = 1
    PINK_SLIP = 2

    def __init__(self, reward: int):
        self.reward: int = reward

    def apply(self, av: "DistributedToonAI"):
        if self.reward == BossRewardAward.SOS:
            av.attemptAddNPCFriend(random.choice(NPCToons.npcFriendsMinMaxStars(3, 4)))
            av.d_setSystemMessage(0, "You were given a random SOS card!")
        elif self.reward == BossRewardAward.UNITE:
            uniteType = random.choice([ResistanceChat.RESISTANCE_TOONUP, ResistanceChat.RESISTANCE_RESTOCK])
            av.addResistanceMessage(random.choice(ResistanceChat.getItems(uniteType)))
            av.d_setSystemMessage(0, "You were given a random unite!")
        elif self.reward == BossRewardAward.PINK_SLIP:
            slipAmount = random.randint(1, 3)
            av.addPinkSlips(slipAmount)
            if slipAmount > 1:
                av.d_setSystemMessage(0, f"You were given {slipAmount} pink slips!")
            else:
                av.d_setSystemMessage(0, f"You were given {slipAmount} pink slip!")


class ProofReward(APReward):
    class ProofType(IntEnum):
        SellbotBossFirstTime = 0
        CashbotBossFirstTime = 1
        LawbotBossFirstTime = 2
        BossbotBossFirstTime = 3

        def to_display(self):
            return {
                self.SellbotBossFirstTime: "First VP Defeated",
                self.CashbotBossFirstTime: "First CFO Defeated",
                self.LawbotBossFirstTime: "First CJ Defeated",
                self.BossbotBossFirstTime: "First CEO Defeated"
            }.get(self, f"Unknown Proof ({self.value})")

    def __init__(self, proofType: ProofType):
        self.proofType: ProofReward.ProofType = proofType

    def apply(self, av: "DistributedToonAI"):
        # todo keep track of these
        av.d_setSystemMessage(0, f"Proof obtained!: {self.proofType.to_display()}")


class VictoryReward(APReward):

    def apply(self, av: "DistributedToonAI"):
        av.APVictory()
        av.d_setSystemMessage(0, "DEBUG: Victory condition achieved")


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

    items.ITEM_5_GAG_CAPACITY: GagCapacityReward(5),
    items.ITEM_10_GAG_CAPACITY: GagCapacityReward(10),
    items.ITEM_15_GAG_CAPACITY: GagCapacityReward(15),

    items.ITEM_750_MONEY_CAP: JellybeanJarUpgradeReward(750),
    items.ITEM_1000_MONEY_CAP: JellybeanJarUpgradeReward(1000),
    items.ITEM_1250_MONEY_CAP: JellybeanJarUpgradeReward(1250),
    items.ITEM_1500_MONEY_CAP: JellybeanJarUpgradeReward(1500),
    items.ITEM_2000_MONEY_CAP: JellybeanJarUpgradeReward(2000),
    items.ITEM_2500_MONEY_CAP: JellybeanJarUpgradeReward(2500),

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

    items.ITEM_TTC_HQ_ACCESS: TaskAccessReward(TaskAccessReward.TOONTOWN_CENTRAL),
    items.ITEM_DD_HQ_ACCESS: TaskAccessReward(TaskAccessReward.DONALDS_DOCK),
    items.ITEM_DG_HQ_ACCESS: TaskAccessReward(TaskAccessReward.DAISYS_GARDENS),
    items.ITEM_MML_HQ_ACCESS: TaskAccessReward(TaskAccessReward.MINNIES_MELODYLAND),
    items.ITEM_TB_HQ_ACCESS: TaskAccessReward(TaskAccessReward.THE_BRRRGH),
    items.ITEM_DDL_HQ_ACCESS: TaskAccessReward(TaskAccessReward.DONALDS_DREAMLAND),

    items.ITEM_FRONT_FACTORY_ACCESS: FacilityAccessReward(FADoorCodes.FRONT_FACTORY_ACCESS_MISSING),
    items.ITEM_SIDE_FACTORY_ACCESS: FacilityAccessReward(FADoorCodes.SIDE_FACTORY_ACCESS_MISSING),

    items.ITEM_COIN_MINT_ACCESS: FacilityAccessReward(FADoorCodes.COIN_MINT_ACCESS_MISSING),
    items.ITEM_DOLLAR_MINT_ACCESS: FacilityAccessReward(FADoorCodes.DOLLAR_MINT_ACCESS_MISSING),
    items.ITEM_BULLION_MINT_ACCESS: FacilityAccessReward(FADoorCodes.BULLION_MINT_ACCESS_MISSING),

    items.ITEM_A_OFFICE_ACCESS: FacilityAccessReward(FADoorCodes.OFFICE_A_ACCESS_MISSING),
    items.ITEM_B_OFFICE_ACCESS: FacilityAccessReward(FADoorCodes.OFFICE_B_ACCESS_MISSING),
    items.ITEM_C_OFFICE_ACCESS: FacilityAccessReward(FADoorCodes.OFFICE_C_ACCESS_MISSING),
    items.ITEM_D_OFFICE_ACCESS: FacilityAccessReward(FADoorCodes.OFFICE_D_ACCESS_MISSING),

    items.ITEM_FRONT_THREE_ACCESS: FacilityAccessReward(FADoorCodes.FRONT_THREE_ACCESS_MISSING),
    items.ITEM_MIDDLE_THREE_ACCESS: FacilityAccessReward(FADoorCodes.MIDDLE_SIX_ACCESS_MISSING),
    items.ITEM_BACK_THREE_ACCESS: FacilityAccessReward(FADoorCodes.BACK_NINE_ACCESS_MISSING),

    items.ITEM_SELLBOT_DISGUISE: CogDisguiseReward(CogDisguiseReward.SELLBOT),
    items.ITEM_CASHBOT_DISGUISE: CogDisguiseReward(CogDisguiseReward.CASHBOT),
    items.ITEM_LAWBOT_DISGUISE: CogDisguiseReward(CogDisguiseReward.LAWBOT),
    items.ITEM_BOSSBOT_DISGUISE: CogDisguiseReward(CogDisguiseReward.BOSSBOT),

    items.ITEM_SELLBOT_PROOF: ProofReward(ProofReward.ProofType.SellbotBossFirstTime),
    items.ITEM_CASHBOT_PROOF: ProofReward(ProofReward.ProofType.CashbotBossFirstTime),
    items.ITEM_LAWBOT_PROOF: ProofReward(ProofReward.ProofType.LawbotBossFirstTime),
    items.ITEM_BOSSBOT_PROOF: ProofReward(ProofReward.ProofType.BossbotBossFirstTime),

    items.ITEM_VICTORY: VictoryReward(),

    items.ITEM_250_MONEY: JellybeanReward(250),
    items.ITEM_500_MONEY: JellybeanReward(500),
    items.ITEM_1000_MONEY: JellybeanReward(1000),
    items.ITEM_2000_MONEY: JellybeanReward(2000),

    items.ITEM_500_XP: GagExpBundleAward(500),
    items.ITEM_1000_XP: GagExpBundleAward(1000),
    items.ITEM_1500_XP: GagExpBundleAward(1500),
    items.ITEM_2000_XP: GagExpBundleAward(2000),
    items.ITEM_2500_XP: GagExpBundleAward(2500),

    items.ITEM_SOS_REWARD: BossRewardAward(BossRewardAward.SOS),
    items.ITEM_UNITE_REWARD: BossRewardAward(BossRewardAward.UNITE),
    items.ITEM_PINK_SLIP_REWARD: BossRewardAward(BossRewardAward.PINK_SLIP),

    items.ITEM_UBER_TRAP: UberTrapAward(),
    items.ITEM_DRIP_TRAP: DripTrapAward(),
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
