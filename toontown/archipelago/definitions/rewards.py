# Represents logic for what to do when we are given an item from AP
import math
from enum import IntEnum

import random
from typing import List, Tuple

from apworld.toontown import ToontownItemName, get_item_def_from_id
from apworld.toontown.fish import LICENSE_TO_ACCESS_CODE
from apworld.toontown.options import GagTrainingFrameBehavior
from otp.otpbase.OTPLocalizerEnglish import EmoteFuncDict
from toontown.archipelago.util import global_text_properties
from toontown.archipelago.util.global_text_properties import MinimalJsonMessagePart
from toontown.battle import BattleBase

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

    # Return a color formatted header to display in the on screen display, this should be overridden
    def formatted_header(self):
        return f"UNIMPLEMENTED REWARD STR:\n{self.__class__.__name__}"

    # Returns a color formatted footer so we don't have to call this ugly code a million times
    def _formatted_footer(self, player, isSelf=False):
        color = 'yellow' if not isSelf else 'magenta'
        name = player if not isSelf else "You"
        return global_text_properties.get_raw_formatted_string([
            MinimalJsonMessagePart("\n\nFrom: "),
            MinimalJsonMessagePart(f"{name}", color=color)
        ])

    # Override to set an image path to show up on the display, assumes png and square shaped
    # If not overridden, will show the AP logo
    def get_image_path(self) -> str:
        return 'phase_14/maps/ap_icon.png'

    # Override to set the scale of an image you want to show up on the display
    def get_image_scale(self) -> float:
        return .08

    # Override to set the position of an image you want to show up on the display
    def get_image_pos(self):
        return (.12, 0, .1)

    # Returns a string to show on the display when received, should follow the basic format like so:
    # Your x is now y!\n\nFrom: {fromPlayer}
    def get_reward_string(self, fromPlayer: str, isSelf=False) -> str:
        return f"{self.formatted_header()}{self._formatted_footer(fromPlayer, isSelf)}"

    def apply(self, av: "DistributedToonAI"):
        raise NotImplementedError("Please implement the apply() method!")


class LaffBoostReward(APReward):
    def __init__(self, amount: int):
        self.amount = amount

    def formatted_header(self) -> str:
        return global_text_properties.get_raw_formatted_string([
            MinimalJsonMessagePart("Increased your\nmax laff by "),
            MinimalJsonMessagePart(f"+{self.amount}", color='green'),
            MinimalJsonMessagePart("!"),
        ])

    def apply(self, av: "DistributedToonAI"):
        av.b_setMaxHp(av.maxHp + self.amount)
        av.toonUp(self.amount)
        av.checkWinCondition()


class GagCapacityReward(APReward):

    def __init__(self, amount: int):
        self.amount: int = amount

    def formatted_header(self) -> str:
        return global_text_properties.get_raw_formatted_string([
            MinimalJsonMessagePart("Increased your gag\npouch capacity by "),
            MinimalJsonMessagePart(f"+{self.amount}", color='green'),
            MinimalJsonMessagePart("!"),
        ])

    def apply(self, av: "DistributedToonAI"):
        av.b_setMaxCarry(av.maxCarry + self.amount)


class JellybeanJarUpgradeReward(APReward):

    def __init__(self, amount: int):
        self.amount: int = amount

    def formatted_header(self) -> str:
        return global_text_properties.get_raw_formatted_string([
            MinimalJsonMessagePart("Increased your jellybean\njar capacity by "),
            MinimalJsonMessagePart(f"+{self.amount}", color='green'),
            MinimalJsonMessagePart("!"),
        ])

    def apply(self, av: "DistributedToonAI"):
        av.b_setMaxMoney(av.maxMoney + self.amount)

class TaskCapacityReward(APReward):
    
        def __init__(self, amount: int):
            self.amount: int = amount
    
        def formatted_header(self) -> str:
            return global_text_properties.get_raw_formatted_string([
                MinimalJsonMessagePart("Increased your task\ncapacity by "),
                MinimalJsonMessagePart(f"+{self.amount}", color='green'),
                MinimalJsonMessagePart("!"),
            ])
    
        def apply(self, av: "DistributedToonAI"):
            av.b_setQuestCarryLimit(av.getQuestCarryLimit() + self.amount)

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

    TRACK_TO_COLOR = {
        TOONUP: 'slateblue',
        TRAP: 'yellow',
        LURE: 'green',
        SOUND: 'plum',
        THROW: 'yellow',  #  todo add a gold text property
        SQUIRT: 'slateblue',  # todo add a pinkish text property
        DROP: 'cyan'
    }

    TRACK_TO_ICON = {
        TOONUP: "toonup_%s",
        TRAP: "trap_%s",
        LURE: "lure_%s",
        SOUND: "sound_%s",
        THROW: "throw_%s",
        SQUIRT: "squirt_%s",
        DROP: "drop_%s",
    }

    def __init__(self, track):
        self.track = track

    # todo: find a way to show dynamic info based on what this reward did for us exactly
    # todo: new system was two steps forward one step back in this regard
    def formatted_header(self) -> str:
        track_name_color = self.TRACK_TO_COLOR.get(self.track)
        level = base.localAvatar.getTrackAccessLevel(self.track)
        # Check for new levels
        if level <= 7:
            return global_text_properties.get_raw_formatted_string([
                MinimalJsonMessagePart("Received a training frame!\nYour "),
                MinimalJsonMessagePart(f"{self.TRACK_TO_NAME[self.track]}".upper(), color=track_name_color),
                MinimalJsonMessagePart(" Gags have more potential!"),
                ])
        else:
            return global_text_properties.get_raw_formatted_string([
                MinimalJsonMessagePart("Received a training frame!\nYour "),
                MinimalJsonMessagePart(f"{self.TRACK_TO_NAME[self.track]}".upper(), color=track_name_color),
                MinimalJsonMessagePart(" experience can now overflow!"),
            ])

    def get_image_path(self) -> str:
        level = base.localAvatar.getTrackAccessLevel(self.track)
        ap_icon = self.TRACK_TO_ICON[(self.track)] % str(min(max(level, 1), 7))
        return f'phase_14/maps/gags/{ap_icon}.png'

    def apply(self, av: "DistributedToonAI"):
        
        # Store option for behavior
        behaviorMode = av.slotData.get("gag_frame_item_behavior", 0)

        # Increment track access level by 1
        oldLevel = av.getTrackAccessLevel(self.track)
        newLevel = oldLevel + 1

        # Before we do anything, we need to see if they were capped before this so we can award them gags later
        curExp = av.experience.getExp(self.track)
        wasCapped = curExp == av.experience.getExperienceCapForTrack(self.track)

        # Otherwise increment the gag level allowed
        av.setTrackAccessLevel(self.track, newLevel)

        # Edge case, nothing else should happen if we are unlocking the "overflow xp" mechanic
        if newLevel >= 8:
            return

        # Max the gag and give the new gag if the behavior mode is to max gags 
        elif behaviorMode == GagTrainingFrameBehavior.option_trained:
            av.experience.setExp(self.track, av.experience.getExperienceCapForTrack(track=self.track)) # max the gag exp.
            av.ap_setExperience(av.experience.getCurrentExperience())
            av.inventory.addItemsWithListMax([(self.track, newLevel-1)])  # Give the new gags!!
            av.b_setInventory(av.inventory.makeNetString())
        # Consider the case where we just learned a new gag track, we should give them as many of them as possible
        elif newLevel == 1:
            av.inventory.addItemsWithListMax([(self.track, 0)])
            av.b_setInventory(av.inventory.makeNetString())
        # Now consider the case where we were maxed previously and want to upgrade by giving 1 xp and giving new gags
        # This will also trigger the new gag check to unlock :3
        elif (wasCapped and behaviorMode == GagTrainingFrameBehavior.option_vanilla
            or behaviorMode == GagTrainingFrameBehavior.option_unlock):
            toNext = av.experience.getNextExpValue(track=self.track, curSkill=curExp)
            av.experience.setExp(track=self.track, exp=toNext)  # Give them enough xp to learn the gag :)
            av.ap_setExperience(av.experience.getCurrentExperience())
            av.inventory.addItemsWithListMax([(self.track, newLevel-1)])  # Give the new gags!!
            av.b_setInventory(av.inventory.makeNetString())

class GagUpgradeReward(APReward):
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

    TRACK_TO_COLOR = {
        TOONUP: 'slateblue',
        TRAP: 'yellow',
        LURE: 'green',
        SOUND: 'plum',
        THROW: 'yellow',  #  todo add a gold text property
        SQUIRT: 'slateblue',  # todo add a pinkish text property
        DROP: 'cyan'
    }

    TRACK_TO_ICON = {
        TOONUP: "toonup_%s",
        TRAP: "trap_%s",
        LURE: "lure_%s",
        SOUND: "sound_%s",
        THROW: "throw_%s",
        SQUIRT: "squirt_%s",
        DROP: "drop_%s",
    }

    def __init__(self, track):
        self.track = track

    # todo: find a way to show dynamic info based on what this reward did for us exactly
    # todo: new system was two steps forward one step back in this regard
    def formatted_header(self) -> str:
        track_name_color = self.TRACK_TO_COLOR.get(self.track)
        return global_text_properties.get_raw_formatted_string([
            MinimalJsonMessagePart("Trees have been planted!\nYour "),
            MinimalJsonMessagePart(f"{self.TRACK_TO_NAME[self.track]}".upper(), color=track_name_color),
            MinimalJsonMessagePart(" Gags are now organic!"),
        ])

    def get_image_path(self) -> str:
        level = base.localAvatar.getTrackAccessLevel(self.track)
        if not level:
            level = 1
        ap_icon = self.TRACK_TO_ICON[(self.track)] % str(min(level, 7))
        return f'phase_14/maps/gags/{ap_icon}.png'

    def apply(self, av: "DistributedToonAI"):
        bonusArray = av.getTrackBonusLevel()
        bonusArray[self.track] = 7
        av.b_setTrackBonusLevel(bonusArray)


class GagTrainingMultiplierReward(APReward):

    def __init__(self, amount: int):
        self.amount: int = amount

    # todo, again nice to have this tell us WHAT it is, not what we got
    def formatted_header(self) -> str:
        return global_text_properties.get_raw_formatted_string([
            MinimalJsonMessagePart("Increased your global XP\nmultiplier by "),
            MinimalJsonMessagePart(f"+{self.amount}", color='green'),
            MinimalJsonMessagePart("!"),
        ])

    def apply(self, av: "DistributedToonAI"):
        oldMultiplier = av.getBaseGagSkillMultiplier()
        newMultiplier = oldMultiplier + self.amount
        av.b_setBaseGagSkillMultiplier(newMultiplier)


class GolfPutterReward(APReward):

    def formatted_header(self) -> str:
        return global_text_properties.get_raw_formatted_string([
            MinimalJsonMessagePart("Get ready to go mini-golfing\nwith your new "),
            MinimalJsonMessagePart("Golf Putter", color='cyan'),
            MinimalJsonMessagePart("!"),
        ])

    def apply(self, av: "DistributedToonAI"):
        av.addAccessKey(ToontownGlobals.PUTTER_KEY)


class GoKartReward(APReward):

    def formatted_header(self) -> str:
        return global_text_properties.get_raw_formatted_string([
            MinimalJsonMessagePart("Get ready to go racing\nwith your new "),
            MinimalJsonMessagePart("Go-Kart", color='cyan'),
            MinimalJsonMessagePart("!"),
        ])

    def apply(self, av: "DistributedToonAI"):
        av.b_setKartBodyType(1)


class FishingRodUpgradeReward(APReward):

    def formatted_header(self) -> str:
        return global_text_properties.get_raw_formatted_string([
            MinimalJsonMessagePart("Your "),
            MinimalJsonMessagePart(f"Fishing Rod", color='plum'),
            MinimalJsonMessagePart("\nhas been upgraded!"),
        ])

    def apply(self, av: "DistributedToonAI"):
        nextRodID = min(av.fishingRod + 1, FishGlobals.MaxRodId)

        av.b_setFishingRod(nextRodID)


class AccessKeyReward(APReward):
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

    ACORN_ACRES = ToontownGlobals.OutdoorZone
    GOOFY_SPEEDWAY = ToontownGlobals.GoofySpeedway

    LINKED_PGS = {ACORN_ACRES: [ToontownGlobals.GolfZone]}

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
        ACORN_ACRES: "Acorn Acres",
        GOOFY_SPEEDWAY: "Goofy Speedway",
    }

    ZONE_TO_ACCESS_ITEM = {
        TOONTOWN_CENTRAL: ToontownItemName.TTC_ACCESS,
        DONALDS_DOCK: ToontownItemName.DD_ACCESS,
        DAISYS_GARDENS: ToontownItemName.DG_ACCESS,
        MINNIES_MELODYLAND: ToontownItemName.MML_ACCESS,
        THE_BRRRGH: ToontownItemName.TB_ACCESS,
        DONALDS_DREAMLAND: ToontownItemName.DDL_ACCESS,
        SELLBOT_HQ: ToontownItemName.SBHQ_ACCESS,
        CASHBOT_HQ: ToontownItemName.CBHQ_ACCESS,
        LAWBOT_HQ: ToontownItemName.LBHQ_ACCESS,
        BOSSBOT_HQ: ToontownItemName.BBHQ_ACCESS,
        ACORN_ACRES: ToontownItemName.AA_ACCESS,
        GOOFY_SPEEDWAY: ToontownItemName.GS_ACCESS,
    }

    COG_ZONES = (SELLBOT_HQ, CASHBOT_HQ,  LAWBOT_HQ, BOSSBOT_HQ)

    def __init__(self, playground: int):
        self.playground: int = playground

    def formatted_header(self) -> str:
        accessCount = 0
        items = base.localAvatar.getReceivedItems()
        for item in items:
            index_received, item_id = item
            if get_item_def_from_id(item_id).name == self.ZONE_TO_ACCESS_ITEM.get(self.playground, ToontownGlobals.ToontownCentral):
                accessCount += 1
        if accessCount >= 2:
            if self.playground in self.COG_ZONES:
                return global_text_properties.get_raw_formatted_string([
                    MinimalJsonMessagePart("You may now infiltrate facilities\nin "),
                    MinimalJsonMessagePart(f"{self.ZONE_TO_DISPLAY_NAME.get(self.playground, 'unknown zone: ' + str(self.playground))}", color='green'),
                    MinimalJsonMessagePart("!"),
                    ])
            return global_text_properties.get_raw_formatted_string([
                MinimalJsonMessagePart("You may now complete ToonTasks\nin "),
                MinimalJsonMessagePart(f"{self.ZONE_TO_DISPLAY_NAME.get(self.playground, 'unknown zone: ' + str(self.playground))}", color='green'),
                MinimalJsonMessagePart("!"),
            ])
        else:
            return global_text_properties.get_raw_formatted_string([
                MinimalJsonMessagePart("You can now teleport\nto "),
                MinimalJsonMessagePart(f"{self.ZONE_TO_DISPLAY_NAME.get(self.playground, 'unknown zone: ' + str(self.playground))}", color='green'),
                MinimalJsonMessagePart("!"),
            ])

    def apply(self, av: "DistributedToonAI"):
        # Apply TP before HQ or facilities
        if not av.hasTeleportAccess(self.playground):
            av.addTeleportAccess(self.playground)
            for pg in self.LINKED_PGS.get(self.playground, []):
                av.addTeleportAccess(pg)
        else:
            # Get the key ID for this playground
            if self.playground in list(FADoorCodes.ZONE_TO_ACCESS_CODE.keys()):
                key = FADoorCodes.ZONE_TO_ACCESS_CODE[self.playground]
                av.addAccessKey(key)


class FishingLicenseReward(APReward):
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

    def formatted_header(self) -> str:
        return global_text_properties.get_raw_formatted_string([
            MinimalJsonMessagePart("You may now Fish\nin "),
            MinimalJsonMessagePart(f"{self.ZONE_TO_DISPLAY_NAME.get(self.playground, 'unknown zone: ' + str(self.playground))}", color='green'),
            MinimalJsonMessagePart("!"),
        ])

    def apply(self, av: "DistributedToonAI"):
        # Get the key ID for this playground
        key = LICENSE_TO_ACCESS_CODE[self.playground]
        av.addAccessKey(key)


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

    def formatted_header(self) -> str:
        key_name = self.FACILITY_ID_TO_DISPLAY.get(self.key, f"UNKNOWN-KEY[{self.key}]")
        return global_text_properties.get_raw_formatted_string([
            MinimalJsonMessagePart("You may now infiltrate\nthe "),
            MinimalJsonMessagePart(f"{key_name}", color='salmon'),
            MinimalJsonMessagePart(" facility!"),
        ])

    def apply(self, av: "DistributedToonAI"):
        # Get the key ID for this playground
        av.addAccessKey(self.key)


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

    def formatted_header(self) -> str:
        dept = self.ENUM_TO_NAME[self.dept]
        return global_text_properties.get_raw_formatted_string([
            MinimalJsonMessagePart("You were given\nyour "),
            MinimalJsonMessagePart(f"{dept} Disguise", color='plum'),
            MinimalJsonMessagePart("!"),
        ])

    def apply(self, av: "DistributedToonAI"):
        parts = av.getCogParts()
        parts[self.dept] = PartsPerSuitBitmasks[self.dept]
        av.b_setCogParts(parts)


class JellybeanReward(APReward):

    def __init__(self, amount: int):
        self.amount: int = amount

    def formatted_header(self) -> str:
        return global_text_properties.get_raw_formatted_string([
            MinimalJsonMessagePart("You were given\n"),
            MinimalJsonMessagePart(f"+{self.amount} jellybeans", color='cyan'),
            MinimalJsonMessagePart("!"),
        ])

    def apply(self, av: "DistributedToonAI"):
        av.ap_setMoney(av.getMoney() + self.amount)


class UberTrapAward(APReward):

    def formatted_header(self) -> str:
        return global_text_properties.get_raw_formatted_string([
            MinimalJsonMessagePart("UBER TRAP\n", color='salmon'),
            MinimalJsonMessagePart(f"Will you survive?"),
        ])

    def apply(self, av: "DistributedToonAI"):
        newHp = 15 if av.getHp() > 15 else 1
        damage = av.getHp() - newHp
        if av.getHp() > 0:
            av.takeDamage(damage)
        av.inventory.maxInventory(clearFirst=True, restockAmount=20)
        av.b_setInventory(av.inventory.makeNetString())
        if newHp == 1:
            av.playSound('phase_4/audio/sfx/BLACK_KNIGHT.ogg')
        else:
            av.playSound('phase_4/audio/sfx/NO_NO_NO.ogg')
        av.d_broadcastHpString("UBERFIED!", (.35, .7, .35))
        av.d_playEmote(EmoteFuncDict['Cry'], 1)


class BeanTaxTrapAward(APReward):
    def __init__(self, tax: int):
        self.tax: int = tax

    def formatted_header(self) -> str:
        if base.localAvatar.getHasPaidTaxes():
            return global_text_properties.get_raw_formatted_string([
                MinimalJsonMessagePart("BEAN TAX PAID\n", color='salmon'),
                MinimalJsonMessagePart("You paid the tax for "),
                MinimalJsonMessagePart(f"{self.tax} beans.", color='cyan'),
            ])

        else:
            return global_text_properties.get_raw_formatted_string([
                MinimalJsonMessagePart("BEAN TAX FAILED\n", color='salmon'),
                MinimalJsonMessagePart("You tried evading the tax for "),
                MinimalJsonMessagePart(f"{self.tax} beans.", color='cyan'),
            ])

    def getPassed(self, avMoney):
        if avMoney >= self.tax:
            return True
        else:
            return False

    def apply(self, av: "DistributedToonAI"):
        avMoney = av.getMoney()

        if self.getPassed(avMoney):
            av.b_setHasPaidTaxes(True)
            av.ap_setMoney(max(avMoney - self.tax, 0))
            av.playSound('phase_4/audio/sfx/tax_paid.ogg')
            av.d_broadcastHpString("TAXES PAID!", (.35, .7, .35))
            av.d_playEmote(EmoteFuncDict['Happy'], 1)
        else:
            av.b_setHasPaidTaxes(False)
            if av.getMoney() >= 100:
                av.ap_setMoney(100)
            damage = av.getHp() - 1
            if av.getHp() > 0:
                av.takeDamage(damage)
            av.playSound('phase_4/audio/sfx/tax_evasion.ogg')
            av.d_broadcastHpString("EVASION ATTEMPTED!", (.3, .5, .8))
            av.d_playEmote(EmoteFuncDict['Belly Flop'], 1)



class DripTrapAward(APReward):

    def formatted_header(self) -> str:
        return global_text_properties.get_raw_formatted_string([
            MinimalJsonMessagePart("DRIP TRAP\n", color='salmon'),
            MinimalJsonMessagePart(f"Did someone say the door to drip?"),
        ])

    def apply(self, av: "DistributedToonAI"):
        av.playSound('phase_4/audio/sfx/avatar_emotion_drip.ogg')
        av.b_setShoes(1, random.randint(1, 48), 0)
        av.b_setBackpack(random.randint(1, 24), 0, 0)
        av.b_setGlasses(random.randint(1, 21), 0, 0)
        av.b_setHat(random.randint(1, 56), 0, 0)

        av.d_broadcastHpString("FASHION STATEMENT!", (.9, .8, .2))
        av.d_playEmote(EmoteFuncDict['Surprise'], 1)


class GagShuffleAward(APReward):

    def formatted_header(self) -> str:
        return global_text_properties.get_raw_formatted_string([
            MinimalJsonMessagePart("GAG SHUFFLE TRAP\n", color='salmon'),
            MinimalJsonMessagePart(f"Got gags?")
        ])

    def apply(self, av: "DistributedToonAI"):
        # Let's make sure we aren't already being shuffled
        avId = av.getDoId()
        if av.getBeingShuffled():
            av.playSound('phase_4/audio/sfx/LETS_GO_GAMBLING.ogg')
            av.d_broadcastHpString("GAG SHUFFLE!", (.3, .5, .8))
            av.d_playEmote(EmoteFuncDict['Confused'], 1)
            return

        # Clear inventory, set being shuffled, randomly choose gags and add them until we fill up
        av.setBeingShuffled(True)
        av.inventory.calcTotalProps()  # Might not be necessary, but just to be safe
        target = av.inventory.totalProps
        av.inventory.clearInventory()  # Wipe inventory
        # Get allowed track level pairs
        allowedGags: List[Tuple[int, int]] = av.experience.getAllowedGagsAndLevels()
        # Only do enough attempts to fill us back up to what we were
        for _ in range(target):
            # Randomly select a gag and attempt to add it
            if allowedGags:  # sanity check for possible empty list
                gag: Tuple[int, int] = random.choice(allowedGags)
                track, level = gag
                gagsAdded = av.inventory.addItem(track, level)

                # If this gag failed to add, we can no longer query for this gag. Remove it.
                if gagsAdded <= 0:
                    allowedGags.remove(gag)

                # Edge case, if we are out of gags we need to stop (in theory this should never happen but let's be safe :p)
                if len(allowedGags) <= 0:
                    break
            else:
                print(f"archipelago rewards WARNING: Could not find any allowed gags. For avId: {avId}")
                break
        # We're done shuffling, should be good now
        av.setBeingShuffled(False)
        av.playSound('phase_4/audio/sfx/LETS_GO_GAMBLING.ogg')
        av.b_setInventory(av.inventory.makeNetString())
        av.d_broadcastHpString("GAG SHUFFLE!", (.3, .5, .8))
        av.d_playEmote(EmoteFuncDict['Confused'], 1)


class GagExpBundleAward(APReward):

    def __init__(self, amount: int):
        self.amount: int = amount

    def formatted_header(self) -> str:
        return global_text_properties.get_raw_formatted_string([
            MinimalJsonMessagePart("You were given a fill of\n"),
            MinimalJsonMessagePart(f"{self.amount}% experience", color='cyan'),
            MinimalJsonMessagePart(" in each Gag Track!"),
        ])

    def apply(self, av: "DistributedToonAI"):
        for index, _ in enumerate(ToontownBattleGlobals.Tracks):
            currentCap = min(av.experience.getExperienceCapForTrack(index), ToontownBattleGlobals.regMaxSkill)
            exptoAdd = math.ceil(currentCap * (self.amount/100))
            av.experience.addExp(index, exptoAdd)
        av.ap_setExperience(av.experience.getCurrentExperience())
        # now check for win condition since we have one for maxxed gags
        av.checkWinCondition()


class BossRewardAward(APReward):
    SOS = 0
    UNITE = 1
    PINK_SLIP = 2

    REWARD_TO_DISPLAY_STR = {
        SOS: "SOS Card",
        UNITE: "Unite",
        PINK_SLIP: "amount of Pink Slips",
    }

    def __init__(self, reward: int):
        self.reward: int = reward

    def formatted_header(self) -> str:
        return global_text_properties.get_raw_formatted_string([
            MinimalJsonMessagePart("You were given a\nrandom "),
            MinimalJsonMessagePart(f"{self.REWARD_TO_DISPLAY_STR[self.reward]}", color='cyan'),
            MinimalJsonMessagePart("!"),
        ])

    def apply(self, av: "DistributedToonAI"):
        if self.reward == BossRewardAward.SOS:
            av.attemptAddNPCFriend(random.choice(NPCToons.npcFriendsMinMaxStars(3, 5)))
        elif self.reward == BossRewardAward.UNITE:
            uniteType = random.choice([ResistanceChat.RESISTANCE_TOONUP, ResistanceChat.RESISTANCE_RESTOCK])
            uniteChoice = random.choice(ResistanceChat.getItems(uniteType))
            av.addResistanceMessage(ResistanceChat.encodeId(uniteType, uniteChoice))
        elif self.reward == BossRewardAward.PINK_SLIP:
            slipAmount = random.randint(1, 2)
            av.addPinkSlips(slipAmount)


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

    def formatted_header(self) -> str:
        return global_text_properties.get_raw_formatted_string([
            MinimalJsonMessagePart("Proof Obtained!\n", color='green'),
            MinimalJsonMessagePart(f"{self.proofType.to_display()}"),
        ])

    def apply(self, av: "DistributedToonAI"):
        # todo keep track of these
        pass


class VictoryReward(APReward):

    def formatted_header(self) -> str:
        return global_text_properties.get_raw_formatted_string([
            MinimalJsonMessagePart("VICTORY!\n", color='green'),
            MinimalJsonMessagePart(f"You have completed your goal!"),
        ])

    def apply(self, av: "DistributedToonAI"):
        av.APVictory()


class UndefinedReward(APReward):

    def __init__(self, desc):
        self.desc = desc

    def apply(self, av: "DistributedToonAI"):
        av.d_setSystemMessage(0, f"Unknown AP reward: {self.desc}")


class IgnoreReward(APReward):

    def apply(self, av: "DistributedToonAI"):
        pass


ITEM_NAME_TO_AP_REWARD: [str, APReward] = {
    ToontownItemName.LAFF_BOOST_1.value: LaffBoostReward(1),
    ToontownItemName.LAFF_BOOST_2.value: LaffBoostReward(2),
    ToontownItemName.LAFF_BOOST_3.value: LaffBoostReward(3),
    ToontownItemName.LAFF_BOOST_4.value: LaffBoostReward(4),
    ToontownItemName.LAFF_BOOST_5.value: LaffBoostReward(5),
    ToontownItemName.GAG_CAPACITY_5.value: GagCapacityReward(5),
    ToontownItemName.GAG_CAPACITY_10.value: GagCapacityReward(10),
    ToontownItemName.GAG_CAPACITY_15.value: GagCapacityReward(15),
    ToontownItemName.MONEY_CAP_1000.value: JellybeanJarUpgradeReward(1000),
    ToontownItemName.TASK_CAPACITY.value: TaskCapacityReward(1),
    ToontownItemName.TOONUP_FRAME.value: GagTrainingFrameReward(GagTrainingFrameReward.TOONUP),
    ToontownItemName.TRAP_FRAME.value: GagTrainingFrameReward(GagTrainingFrameReward.TRAP),
    ToontownItemName.LURE_FRAME.value: GagTrainingFrameReward(GagTrainingFrameReward.LURE),
    ToontownItemName.SOUND_FRAME.value: GagTrainingFrameReward(GagTrainingFrameReward.SOUND),
    ToontownItemName.THROW_FRAME.value: GagTrainingFrameReward(GagTrainingFrameReward.THROW),
    ToontownItemName.SQUIRT_FRAME.value: GagTrainingFrameReward(GagTrainingFrameReward.SQUIRT),
    ToontownItemName.DROP_FRAME.value: GagTrainingFrameReward(GagTrainingFrameReward.DROP),
    ToontownItemName.TOONUP_UPGRADE.value: GagUpgradeReward(GagUpgradeReward.TOONUP),
    ToontownItemName.TRAP_UPGRADE.value: GagUpgradeReward(GagUpgradeReward.TRAP),
    ToontownItemName.LURE_UPGRADE.value: GagUpgradeReward(GagUpgradeReward.LURE),
    ToontownItemName.SOUND_UPGRADE.value: GagUpgradeReward(GagUpgradeReward.SOUND),
    ToontownItemName.THROW_UPGRADE.value: GagUpgradeReward(GagUpgradeReward.THROW),
    ToontownItemName.SQUIRT_UPGRADE.value: GagUpgradeReward(GagUpgradeReward.SQUIRT),
    ToontownItemName.DROP_UPGRADE.value: GagUpgradeReward(GagUpgradeReward.DROP),
    ToontownItemName.GAG_MULTIPLIER_1.value: GagTrainingMultiplierReward(1),
    ToontownItemName.GAG_MULTIPLIER_2.value: GagTrainingMultiplierReward(2),
    ToontownItemName.FISHING_ROD_UPGRADE.value: FishingRodUpgradeReward(),
    ToontownItemName.TTC_ACCESS.value: AccessKeyReward(AccessKeyReward.TOONTOWN_CENTRAL),
    ToontownItemName.DD_ACCESS.value: AccessKeyReward(AccessKeyReward.DONALDS_DOCK),
    ToontownItemName.DG_ACCESS.value: AccessKeyReward(AccessKeyReward.DAISYS_GARDENS),
    ToontownItemName.MML_ACCESS.value: AccessKeyReward(AccessKeyReward.MINNIES_MELODYLAND),
    ToontownItemName.TB_ACCESS.value: AccessKeyReward(AccessKeyReward.THE_BRRRGH),
    ToontownItemName.DDL_ACCESS.value: AccessKeyReward(AccessKeyReward.DONALDS_DREAMLAND),
    ToontownItemName.SBHQ_ACCESS.value: AccessKeyReward(AccessKeyReward.SELLBOT_HQ),
    ToontownItemName.CBHQ_ACCESS.value: AccessKeyReward(AccessKeyReward.CASHBOT_HQ),
    ToontownItemName.LBHQ_ACCESS.value: AccessKeyReward(AccessKeyReward.LAWBOT_HQ),
    ToontownItemName.BBHQ_ACCESS.value: AccessKeyReward(AccessKeyReward.BOSSBOT_HQ),
    ToontownItemName.AA_ACCESS.value: AccessKeyReward(AccessKeyReward.ACORN_ACRES),
    ToontownItemName.GS_ACCESS.value: AccessKeyReward(AccessKeyReward.GOOFY_SPEEDWAY),
    ToontownItemName.TTC_FISHING.value: FishingLicenseReward(FishingLicenseReward.TOONTOWN_CENTRAL),
    ToontownItemName.DD_FISHING.value: FishingLicenseReward(FishingLicenseReward.DONALDS_DOCK),
    ToontownItemName.DG_FISHING.value: FishingLicenseReward(FishingLicenseReward.DAISYS_GARDENS),
    ToontownItemName.MML_FISHING.value: FishingLicenseReward(FishingLicenseReward.MINNIES_MELODYLAND),
    ToontownItemName.TB_FISHING.value: FishingLicenseReward(FishingLicenseReward.THE_BRRRGH),
    ToontownItemName.DDL_FISHING.value: FishingLicenseReward(FishingLicenseReward.DONALDS_DREAMLAND),
    ToontownItemName.FISH.value: IgnoreReward(),
    ToontownItemName.GOLF_PUTTER.value: GolfPutterReward(),
    ToontownItemName.GO_KART.value: GoKartReward(),
    ToontownItemName.FRONT_FACTORY_ACCESS.value: FacilityAccessReward(FADoorCodes.FRONT_FACTORY_ACCESS_MISSING),
    ToontownItemName.SIDE_FACTORY_ACCESS.value: FacilityAccessReward(FADoorCodes.SIDE_FACTORY_ACCESS_MISSING),
    ToontownItemName.COIN_MINT_ACCESS.value: FacilityAccessReward(FADoorCodes.COIN_MINT_ACCESS_MISSING),
    ToontownItemName.DOLLAR_MINT_ACCESS.value: FacilityAccessReward(FADoorCodes.DOLLAR_MINT_ACCESS_MISSING),
    ToontownItemName.BULLION_MINT_ACCESS.value: FacilityAccessReward(FADoorCodes.BULLION_MINT_ACCESS_MISSING),
    ToontownItemName.A_OFFICE_ACCESS.value: FacilityAccessReward(FADoorCodes.OFFICE_A_ACCESS_MISSING),
    ToontownItemName.B_OFFICE_ACCESS.value: FacilityAccessReward(FADoorCodes.OFFICE_B_ACCESS_MISSING),
    ToontownItemName.C_OFFICE_ACCESS.value: FacilityAccessReward(FADoorCodes.OFFICE_C_ACCESS_MISSING),
    ToontownItemName.D_OFFICE_ACCESS.value: FacilityAccessReward(FADoorCodes.OFFICE_D_ACCESS_MISSING),
    ToontownItemName.FRONT_ONE_ACCESS.value: FacilityAccessReward(FADoorCodes.FRONT_THREE_ACCESS_MISSING),
    ToontownItemName.MIDDLE_TWO_ACCESS.value: FacilityAccessReward(FADoorCodes.MIDDLE_SIX_ACCESS_MISSING),
    ToontownItemName.BACK_THREE_ACCESS.value: FacilityAccessReward(FADoorCodes.BACK_NINE_ACCESS_MISSING),
    ToontownItemName.SELLBOT_DISGUISE.value: CogDisguiseReward(CogDisguiseReward.SELLBOT),
    ToontownItemName.CASHBOT_DISGUISE.value: CogDisguiseReward(CogDisguiseReward.CASHBOT),
    ToontownItemName.LAWBOT_DISGUISE.value: CogDisguiseReward(CogDisguiseReward.LAWBOT),
    ToontownItemName.BOSSBOT_DISGUISE.value: CogDisguiseReward(CogDisguiseReward.BOSSBOT),
    ToontownItemName.MONEY_150.value: JellybeanReward(150),
    ToontownItemName.MONEY_400.value: JellybeanReward(400),
    ToontownItemName.MONEY_700.value: JellybeanReward(700),
    ToontownItemName.MONEY_1000.value: JellybeanReward(1000),
    ToontownItemName.XP_10.value: GagExpBundleAward(10),
    ToontownItemName.XP_15.value: GagExpBundleAward(15),
    ToontownItemName.XP_20.value: GagExpBundleAward(20),
    ToontownItemName.SOS_REWARD.value: BossRewardAward(BossRewardAward.SOS),
    ToontownItemName.UNITE_REWARD.value: BossRewardAward(BossRewardAward.UNITE),
    ToontownItemName.PINK_SLIP_REWARD.value: BossRewardAward(BossRewardAward.PINK_SLIP),
    ToontownItemName.UBER_TRAP.value: UberTrapAward(),
    ToontownItemName.BEAN_TAX_TRAP_750.value: BeanTaxTrapAward(750),
    ToontownItemName.BEAN_TAX_TRAP_1000.value: BeanTaxTrapAward(1000),
    ToontownItemName.BEAN_TAX_TRAP_1250.value: BeanTaxTrapAward(1250),
    ToontownItemName.DRIP_TRAP.value: DripTrapAward(),
    ToontownItemName.GAG_SHUFFLE_TRAP.value: GagShuffleAward(),
}


def get_ap_reward_from_name(name: str) -> APReward:
    return ITEM_NAME_TO_AP_REWARD.get(name, UndefinedReward(name))


# The id we are given from a packet from archipelago
def get_ap_reward_from_id(_id: int) -> APReward:
    definition = get_item_def_from_id(_id)

    if not definition:
        return UndefinedReward(_id)

    ap_reward: APReward = ITEM_NAME_TO_AP_REWARD.get(definition.name.value)

    if not ap_reward:
        ap_reward = UndefinedReward(definition.name.value)

    return ap_reward


# Wrapper class for APReward that holds not only the APReward, but also additional attributes such as:
# - index reward was received
# - item ID of the Archipelago item
# - Name of the player who got this reward for us
class EarnedAPReward:

    def __init__(self, av, reward: APReward, rewardIndex: int, itemId: int, fromName: str, isLocal: bool):
        self.av = av
        self.reward = reward
        self.rewardIndex = rewardIndex
        self.itemId = itemId
        self.fromName = fromName
        self.isLocal = isLocal

    def apply(self):
        self.reward.apply(self.av)  # Actually give the effects
        self.av.d_showReward(self.itemId, self.fromName, self.isLocal)  # Display the popup to the client
