from dataclasses import dataclass
from enum import auto, IntEnum
from typing import Set, Dict, Tuple, Union, Any, List

import random
from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPLocalizer
from toontown.toonbase import TTLocalizer

notify = DirectNotifyGlobal.directNotify.newCategory('SuitBattleGlobals')


"""
Legacy code that still needs to be refactored and is currently deprecated.

Various enums and a few helper functions.
"""
MAX_SUIT_DEFENSE = 55

ATK_TGT_UNKNOWN = 1
ATK_TGT_SINGLE = 2
ATK_TGT_GROUP = 3


def pickFromFreqList(freqList):
    randNum = random.randint(0, 99)
    count = 0
    index = 0
    level = None
    for f in freqList:
        count = count + f
        if randNum < count:
            level = index
            break
        index = index + 1

    return level


"""
Enum and dataclass definitions to store information relating to basic suit vitals and attack definitions.

SuitAttackType:      Enum for all the different types of suit attacks.
SuitAttackAttribute: Dataclass that stores information about a specific suit's attacks. (damage, accuracy, etc.)
SuitAttributes:      Dataclass that stores information regarding a suit's vitals. (HP, evasion, list of attacks, etc.) 
"""


# Define enums for every suit attack.
class SuitAttackType(IntEnum):
    NO_ATTACK = auto()
    AUDIT = auto()
    BITE = auto()
    BOUNCE_CHECK = auto()
    BRAIN_STORM = auto()
    BUZZ_WORD = auto()
    CALCULATE = auto()
    CANNED = auto()
    CHOMP = auto()
    CIGAR_SMOKE = auto()
    CLIPON_TIE = auto()
    CRUNCH = auto()
    DEMOTION = auto()
    DOWNSIZE = auto()
    DOUBLE_TALK = auto()
    EVICTION_NOTICE = auto()
    EVIL_EYE = auto()
    FILIBUSTER = auto()
    FILL_WITH_LEAD = auto()
    FINGER_WAG = auto()
    FIRED = auto()
    FIVE_O_CLOCK_SHADOW = auto()
    FLOOD_THE_MARKET = auto()
    FOUNTAIN_PEN = auto()
    FREEZE_ASSETS = auto()
    GAVEL = auto()
    GLOWER_POWER = auto()
    GUILT_TRIP = auto()
    HALF_WINDSOR = auto()
    HANG_UP = auto()
    HEAD_SHRINK = auto()
    HOT_AIR = auto()
    JARGON = auto()
    LEGALESE = auto()
    LIQUIDATE = auto()
    MARKET_CRASH = auto()
    MUMBO_JUMBO = auto()
    PARADIGM_SHIFT = auto()
    PECKING_ORDER = auto()
    PICK_POCKET = auto()
    PINK_SLIP = auto()
    PLAY_HARDBALL = auto()
    POUND_KEY = auto()
    POWER_TIE = auto()
    POWER_TRIP = auto()
    QUAKE = auto()
    RAZZLE_DAZZLE = auto()
    RED_TAPE = auto()
    RE_ORG = auto()
    RESTRAINING_ORDER = auto()
    ROLODEX = auto()
    RUBBER_STAMP = auto()
    RUB_OUT = auto()
    SACKED = auto()
    SANDTRAP = auto()
    SCHMOOZE = auto()
    SHAKE = auto()
    SHRED = auto()
    SONG_AND_DANCE = auto()
    SPIN = auto()
    SYNERGY = auto()
    TABULATE = auto()
    TEE_OFF = auto()
    THROW_BOOK = auto()
    TREMOR = auto()
    WATERCOOLER = auto()
    WITHDRAWAL = auto()
    WRITE_OFF = auto()

    def getId(self) -> int:
        return self.__index__()

    @classmethod
    def fromId(cls, _id: int):
        for attackType in cls.__members__.values():
            if attackType.getId() == _id:
                return attackType

        raise KeyError(f"Unknown suit attack type with ID: {_id}")

    # Specifies if a certain attack is a group attack.
    # If you add a group attack, don't forget to add it to this set.
    # todo maybe a better way to do this with per enum definitions?
    def isGroupAttack(self) -> bool:
        return self in {self.GUILT_TRIP, self.PARADIGM_SHIFT, self.POWER_TRIP, self.QUAKE, self.SHAKE,
                        self.SONG_AND_DANCE, self.SYNERGY, self.TREMOR}


# Represents an attack definition for a suit.
# Holds data such as attack damage, accuracy, and attack type that a suit can have per attack.
# There is no error checking for not defining at least one level of attack damage for an attribute so we will always
# assume that any data structure contained within this class is not empty.
@dataclass
class SuitAttackAttribute:
    attack: SuitAttackType  # The type of attack.
    damage: Dict[int, int]  # Actual suit level -> damage of an attack.
    accuracy: int  # Base accuracy of this attack.
    weight: int  # How much weight this attack should have. Higher number = Higher frequency.

    # Return a tuple of the level and its corresponding damage for highest level registered for this attack.
    def getStrongestAttackLevelAndDamage(self) -> Tuple[int, int]:

        # Extract the highest level definition from the keys of levels.
        highestLevel = max(self.damage.keys())
        # Return this level and its damage.
        return highestLevel, self.damage[highestLevel]

    # Same as above, but do it for the lowest level registered.
    def getWeakestAttackLevelAndDamage(self) -> Tuple[int, int]:
        lowestLevel = min(self.damage.keys())
        return lowestLevel, self.damage[lowestLevel]

    # Given an amount of levels we are overflowed by, return how much extra damage an attack should do.
    def __getOverflowDamage(self, overflow):
        return overflow * 3  # Simply just 3 damage per level of overflow this suit is for a given attack definition.

    # Given an amount of levels we are underflowed by, return how less damage an attack should do.
    def __getUnderflowDamage(self, underflow):
        return -underflow  # Simply just subtract one per level of underflow.

    # Given an actual suit level, return how much damage this attack should do.
    # If an attack is not defined for a specific level, we just find the strongest registered damage value
    # for this attack and multiply it by 3 for every level we are above it.
    def getBaseAttackDamage(self, suitLevel):

        # Attempt to find the damage for this level. If it was defined, simply just return it.
        damage = self.damage.get(suitLevel)
        if damage is not None:
            return damage

        # This suit is either underleveled or overleveled. Dynamically generate how much damage this attack should do.
        lowestLevel, lowestDamage = self.getWeakestAttackLevelAndDamage()
        highestLevel, highestDamage = self.getStrongestAttackLevelAndDamage()

        # Are we underleveled? If so return an underflow modified amount of damage that is no less than 1.
        if suitLevel < lowestLevel:
            levelDiff = lowestLevel - suitLevel
            return max(1, lowestDamage + self.__getUnderflowDamage(levelDiff))

        # We are overleveled. Return an overflow modified amount of damage.
        levelDiff = suitLevel - highestLevel
        return highestDamage + self.__getOverflowDamage(levelDiff)

    def isGroupAttack(self) -> bool:
        return self.attack.isGroupAttack()

    # When stored in dicts and sets, uniqueness of this element is determined solely by the attack key.
    def __hash__(self):
        return self.attack.value


@dataclass
class SuitAttributes:
    key: str  # The unique identifier of this suit. 'f' = flunky 'bf' = bottom feeder etc.
    name: str  # The basic name of the suit for localizer purposes.
    singular: str  # The singular representation of this suit for localizer purposes.
    plural: str  # The plural representation of this suit.
    tier: int  # The level this cog starts at minus one. Flunkies are tier 0 and Pencil Pushers are tier 1.

    # The attacks this suit is allowed to perform, this will be used on init to generate a dict for easier access.
    attacks: Set[SuitAttackAttribute]

    # Generate a dict version of the attacks after initialization for easier access.
    def __post_init__(self):
        self.__attackMap: Dict[SuitAttackType, SuitAttackAttribute] = {attack.attack: attack for attack in self.attacks}

    # The max HP this suit will have based on their actual level.
    # Override in a child class if a certain suit with certain attributes should stray from the original formula.
    def getBaseMaxHp(self, actualLevel: int) -> int:
        return (actualLevel + 1) * (actualLevel + 2)

    # The highest possible evasion (defense) stat a suit with these attributes is allowed to have.
    # Referred to as "Cog Defense" in legacy toontown code.
    # Override in a child class if a certain suit with certain attributes should be allowed to surpass this.
    def getMaxEvasion(self) -> int:
        return 55

    # The evasion stat this suit will have based on their actual level. Referred to as "Cog Defense" in legacy TT code.
    # Override in a child class if a certain suit with certain attributes should stray from the original formula.
    def getBaseEvasion(self, actualLevel: int) -> int:
        return min(actualLevel * 5, self.getMaxEvasion())

    # Returns the minimum level this suit is allowed to be under normal circumstances.
    # Suits do however have support to be any level you wish though.
    def getMinLevel(self) -> int:
        return self.tier + 1

    # When suits are a higher level than their minimum level, they get accuracy boosts for their attacks.
    # This method returns that boost that is applied on top of an attack's base accuracy.
    def getAccuracyBoost(self, actualLevel: int) -> int:
        levelsAboveMin = max(0, actualLevel - self.getMinLevel())
        return levelsAboveMin * 5

    # Given an attack key, return this suit's statistics for it. None if this suit cannot perform this attack.
    def getAttack(self, key: SuitAttackType) -> Union[SuitAttackAttribute, None]:
        return self.__attackMap.get(key)

    # When stored in dicts and sets, uniqueness of this element is determined solely by the suit key.
    def __hash__(self):
        return self.key.__hash__()

    # Deprecated, used to convert this attribute class to its old dictionary form to maintain backwards compatibility.
    # Not guaranteed to be a faithful 1 to 1 recreation of the legacy info.
    def legacy(self) -> Dict[str, Any]:
        data = {}
        data['name'] = self.name
        data['singularname'] = self.singular
        data['pluralname'] = self.plural
        data['level'] = self.tier
        minLevel = self.getMinLevel()
        endLevel = minLevel + 5
        data['hp'] = (self.getBaseMaxHp(level) for level in range(minLevel, endLevel+1))
        data['def'] = (self.getBaseEvasion(level) for level in range(minLevel, endLevel+1))
        data['freq'] = (50, 30, 10, 5, 5)
        data['acc'] = (self.getAccuracyBoost(level) + 35 for level in range(minLevel, endLevel+1))

        attacks = []
        for attack in self.attacks:
            split_name = attack.attack.name.split(' ')
            for i, word in enumerate(split_name):
                split_name[i] = word[0] + word[1:].lower()
            name = ''.join(split_name)
            attacks.append((
                name,
                (attack.getBaseAttackDamage(level) for level in range(minLevel, endLevel+1)),
                (attack.accuracy + self.getAccuracyBoost(level) for level in range(minLevel, endLevel+1)),
                (attack.weight for level in range(minLevel, endLevel+1)),
            ))
        data['attacks'] = attacks
        return data


# Tier 1 (0 in code) suits have a less aggressive defense formula than standard cogs.
# Adjust the evasion method to reflect that.
class T1SuitAttributes(SuitAttributes):

    def getBaseEvasion(self, actualLevel: int) -> int:
        if actualLevel <= 1:
            return 0
        if actualLevel <= 2:
            return 3
        return super().getBaseEvasion(actualLevel-2)


__ALL_SUIT_ATTRIBUTES: Dict[str, SuitAttributes] = {}


def __registerSuitAttributes(attributes: SuitAttributes):
    if attributes.key in __ALL_SUIT_ATTRIBUTES:
        raise ValueError(f"Already registered suit code: {attributes.key}. Check for duplicates.")

    __ALL_SUIT_ATTRIBUTES[attributes.key] = attributes


# Begin defining suit attributes for every cog in the game.
__FLUNKY_ATTACKS = set()
__FLUNKY_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.POUND_KEY,
    damage={1: 2, 2: 2, 3: 3, 4: 4, 5: 6},
    accuracy=75,
    weight=50,
))
__FLUNKY_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.SHRED,
    damage={1: 3, 2: 4, 3: 5, 4: 6, 5: 7},
    accuracy=50,
    weight=30,
))
__FLUNKY_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.CLIPON_TIE,
    damage={1: 1, 2: 1, 3: 2, 4: 2, 5: 3},
    accuracy=75,
    weight=20,
))
__FLUNKY: SuitAttributes = T1SuitAttributes(key='f', name=TTLocalizer.SuitFlunky, singular=TTLocalizer.SuitFlunkyS, plural=TTLocalizer.SuitFlunkyP, tier=0, attacks=__FLUNKY_ATTACKS)
__registerSuitAttributes(__FLUNKY)

__PENCIL_PUSHER_ATTACKS = set()
__PENCIL_PUSHER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.FOUNTAIN_PEN,
    damage={2: 2, 3: 3, 4: 4, 5: 6, 6: 9},
    accuracy=75,
    weight=20,
))
__PENCIL_PUSHER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.RUB_OUT,
    damage={2: 4, 3: 5, 4: 6, 5: 8, 6: 12},
    accuracy=75,
    weight=20,
))
__PENCIL_PUSHER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.FINGER_WAG,
    damage={2: 1, 3: 2, 4: 2, 5: 3, 6: 4},
    accuracy=75,
    weight=15,
))
__PENCIL_PUSHER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.WRITE_OFF,
    damage={2: 4, 3: 6, 4: 8, 5: 10, 6: 12},
    accuracy=75,
    weight=25,
))
__PENCIL_PUSHER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.FILL_WITH_LEAD,
    damage={2: 3, 3: 4, 4: 5, 5: 6, 6: 7},
    accuracy=75,
    weight=20,
))
__PENCIL_PUSHER: SuitAttributes = SuitAttributes(key='p', name=TTLocalizer.SuitPencilPusher, singular=TTLocalizer.SuitPencilPusherS, plural=TTLocalizer.SuitPencilPusherP, tier=1, attacks=__PENCIL_PUSHER_ATTACKS)
__registerSuitAttributes(__PENCIL_PUSHER)

__YESMAN_ATTACKS = set()
__YESMAN_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.RUBBER_STAMP,
    damage={3: 2, 4: 2, 5: 3, 6: 3, 7: 4},
    accuracy=75,
    weight=35,
))
__YESMAN_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.RAZZLE_DAZZLE,
    damage={3: 1, 4: 1, 5: 1, 6: 1, 7: 1},
    accuracy=50,
    weight=5,
))
__YESMAN_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.SYNERGY,
    damage={3: 4, 4: 5, 5: 6, 6: 7, 7: 8},
    accuracy=50,
    weight=25,
))
__YESMAN_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.TEE_OFF,
    damage={3: 3, 4: 3, 5: 4, 6: 4, 7: 5},
    accuracy=50,
    weight=35,
))
__YESMAN: SuitAttributes = SuitAttributes(key='ym', name=TTLocalizer.SuitYesman, singular=TTLocalizer.SuitYesmanS, plural=TTLocalizer.SuitYesmanP, tier=2, attacks=__YESMAN_ATTACKS)
__registerSuitAttributes(__YESMAN)

__MICROMANAGER_ATTACKS = set()
__MICROMANAGER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.DEMOTION,
    damage={4: 6, 5: 8, 6: 12, 7: 15, 8: 17},
    accuracy=50,
    weight=30,
))
__MICROMANAGER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.FINGER_WAG,
    damage={4: 4, 5: 6, 6: 9, 7: 12, 8: 15},
    accuracy=50,
    weight=10,
))
__MICROMANAGER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.FOUNTAIN_PEN,
    damage={4: 3, 5: 4, 6: 6, 7: 8, 8: 10},
    accuracy=50,
    weight=15,
))
__MICROMANAGER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.BRAIN_STORM,
    damage={4: 4, 5: 6, 6: 9, 7: 12, 8: 15},
    accuracy=5,
    weight=25,
))
__MICROMANAGER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.BUZZ_WORD,
    damage={4: 4, 5: 6, 6: 9, 7: 12, 8: 15},
    accuracy=50,
    weight=20,
))
__MICROMANAGER: SuitAttributes = SuitAttributes(key='mm', name=TTLocalizer.SuitMicromanager, singular=TTLocalizer.SuitMicromanagerS, plural=TTLocalizer.SuitMicromanagerP, tier=3, attacks=__MICROMANAGER_ATTACKS)
__registerSuitAttributes(__MICROMANAGER)

__DOWNSIZER_ATTACKS = set()
__DOWNSIZER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.CANNED,
    damage={5: 5, 6: 6, 7: 8, 8: 10, 9: 12},
    accuracy=60,
    weight=25,
))
__DOWNSIZER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.DOWNSIZE,
    damage={5: 8, 6: 9, 7: 11, 8: 13, 9: 15},
    accuracy=50,
    weight=35,
))
__DOWNSIZER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.PINK_SLIP,
    damage={5: 4, 6: 5, 7: 6, 8: 7, 9: 8},
    accuracy=60,
    weight=25,
))
__DOWNSIZER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.SACKED,
    damage={5: 5, 6: 6, 7: 7, 8: 8, 9: 9},
    accuracy=50,
    weight=15,
))
__DOWNSIZER: SuitAttributes = SuitAttributes(key='ds', name=TTLocalizer.SuitDownsizer, singular=TTLocalizer.SuitDownsizerS, plural=TTLocalizer.SuitDownsizerP, tier=4, attacks=__DOWNSIZER_ATTACKS)
__registerSuitAttributes(__DOWNSIZER)

__HEAD_HUNTER_ATTACKS = set()
__HEAD_HUNTER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.FOUNTAIN_PEN,
    damage={6: 5, 7: 6, 8: 8, 9: 10, 10: 12},
    accuracy=60,
    weight=10,
))
__HEAD_HUNTER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.POWER_TRIP,
    damage={6: 10, 7: 11, 8: 12, 9: 14, 10: 16},
    accuracy=50,
    weight=20,
))
__HEAD_HUNTER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.GLOWER_POWER,
    damage={6: 8, 7: 9, 8: 10, 9: 11, 10: 12},
    accuracy=75,
    weight=15,
))
__HEAD_HUNTER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.HALF_WINDSOR,
    damage={6: 8, 7: 10, 8: 12, 9: 14, 10: 16},
    accuracy=60,
    weight=15,
))
__HEAD_HUNTER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.HEAD_SHRINK,
    damage={6: 13, 7: 15, 8: 17, 9: 18, 10: 19},
    accuracy=65,
    weight=30,
))
__HEAD_HUNTER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.ROLODEX,
    damage={6: 10, 7: 12, 8: 14, 9: 16, 10: 18},
    accuracy=60,
    weight=10,
))
__HEAD_HUNTER: SuitAttributes = SuitAttributes(key='hh', name=TTLocalizer.SuitHeadHunter, singular=TTLocalizer.SuitHeadHunterS, plural=TTLocalizer.SuitHeadHunterP, tier=5, attacks=__HEAD_HUNTER_ATTACKS)
__registerSuitAttributes(__HEAD_HUNTER)

__CORPORATE_RAIDER_ATTACKS = set()
__CORPORATE_RAIDER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.CANNED,
    damage={7: 10, 8: 11, 9: 12, 10: 14, 11: 16},
    accuracy=80,
    weight=20,
))
__CORPORATE_RAIDER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.EVIL_EYE,
    damage={7: 12, 8: 14, 9: 16, 10: 18, 11: 20},
    accuracy=65,
    weight=35,
))
__CORPORATE_RAIDER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.PLAY_HARDBALL,
    damage={7: 12, 8: 15, 9: 18, 10: 20, 11: 22},
    accuracy=55,
    weight=30,
))
__CORPORATE_RAIDER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.POWER_TIE,
    damage={7: 10, 8: 12, 9: 14, 10: 16, 11: 18},
    accuracy=65,
    weight=15,
))
__CORPORATE_RAIDER: SuitAttributes = SuitAttributes(key='cr', name=TTLocalizer.SuitCorporateRaider, singular=TTLocalizer.SuitCorporateRaiderS, plural=TTLocalizer.SuitCorporateRaiderP, tier=6, attacks=__CORPORATE_RAIDER_ATTACKS)
__registerSuitAttributes(__CORPORATE_RAIDER)

__THE_BIG_CHEESE_ATTACKS = set()
__THE_BIG_CHEESE_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.CIGAR_SMOKE,
    damage={8: 12, 9: 14, 10: 16, 11: 18, 12: 20},
    accuracy=85,
    weight=20,
))
__THE_BIG_CHEESE_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.FLOOD_THE_MARKET,
    damage={8: 8, 9: 10, 10: 12, 11: 14, 12: 16},
    accuracy=95,
    weight=10,
))
__THE_BIG_CHEESE_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.POWER_TRIP,
    damage={8: 12, 9: 15, 10: 18, 11: 21, 12: 24},
    accuracy=60,
    weight=50,
))
__THE_BIG_CHEESE_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.TEE_OFF,
    damage={8: 16, 9: 18, 10: 20, 11: 22, 12: 24},
    accuracy=70,
    weight=20,
))
__THE_BIG_CHEESE: SuitAttributes = SuitAttributes(key='tbc', name=TTLocalizer.SuitTheBigCheese, singular=TTLocalizer.SuitTheBigCheeseS, plural=TTLocalizer.SuitTheBigCheeseP, tier=7, attacks=__THE_BIG_CHEESE_ATTACKS)
__registerSuitAttributes(__THE_BIG_CHEESE)

# Begin defining suit attributes for every cog in the game.
__BAG_HOLDER_ATTACKS = set()
__BAG_HOLDER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.CLIPON_TIE,
    damage={1: 3, 2: 4, 3: 5, 4: 6, 5: 8},
    accuracy=75,
    weight=50,
))
__BAG_HOLDER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.SACKED,
    damage={1: 3, 2: 5, 3: 7, 4: 9, 5: 11},
    accuracy=50,
    weight=30,
))
__BAG_HOLDER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.SCHMOOZE,
    damage={1: 2, 2: 3, 3: 4, 4: 5, 5: 6},
    accuracy=75,
    weight=20,
))
__BAG_HOLDER: SuitAttributes = T1SuitAttributes(key='bgh', name=TTLocalizer.SuitBagHolder, singular=TTLocalizer.SuitBagHolderS, plural=TTLocalizer.SuitBagHolderP, tier=0, attacks=__BAG_HOLDER_ATTACKS)
__registerSuitAttributes(__BAG_HOLDER)

__COLD_CALLER_ATTACKS = set()
__COLD_CALLER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.FREEZE_ASSETS,
    damage={1: 1, 2: 1, 3: 1, 4: 1, 5: 1},
    accuracy=90,
    weight=25,
))
__COLD_CALLER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.POUND_KEY,
    damage={1: 2, 2: 2, 3: 3, 4: 4, 5: 5},
    accuracy=75,
    weight=25,
))
__COLD_CALLER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.DOUBLE_TALK,
    damage={1: 2, 2: 3, 3: 4, 4: 6, 5: 8},
    accuracy=50,
    weight=25,
))
__COLD_CALLER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.HOT_AIR,
    damage={1: 3, 2: 4, 3: 6, 4: 8, 5: 10},
    accuracy=50,
    weight=25,
))
__COLD_CALLER: SuitAttributes = T1SuitAttributes(key='cc', name=TTLocalizer.SuitColdCaller, singular=TTLocalizer.SuitColdCallerS, plural=TTLocalizer.SuitColdCallerP, tier=0, attacks=__COLD_CALLER_ATTACKS)
__registerSuitAttributes(__COLD_CALLER)

__TELEMARKETER_ATTACKS = set()
__TELEMARKETER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.CLIPON_TIE,
    damage={2: 2, 3: 2, 4: 3, 5: 3, 6: 4},
    accuracy=75,
    weight=15,
))
__TELEMARKETER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.PICK_POCKET,
    damage={2: 1, 3: 1, 4: 1, 5: 1, 6: 1},
    accuracy=75,
    weight=15,
))
__TELEMARKETER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.ROLODEX,
    damage={2: 4, 3: 6, 4: 7, 5: 9, 6: 12},
    accuracy=50,
    weight=30,
))
__TELEMARKETER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.DOUBLE_TALK,
    damage={2: 4, 3: 6, 4: 7, 5: 9, 6: 12},
    accuracy=75,
    weight=40,
))
__TELEMARKETER: SuitAttributes = SuitAttributes(key='tm', name=TTLocalizer.SuitTelemarketer, singular=TTLocalizer.SuitTelemarketerS, plural=TTLocalizer.SuitTelemarketerP, tier=1, attacks=__TELEMARKETER_ATTACKS)
__registerSuitAttributes(__TELEMARKETER)

__NAME_DROPPER_ATTACKS = set()
__NAME_DROPPER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.RAZZLE_DAZZLE,
    damage={3: 4, 4: 5, 5: 6, 6: 9, 7: 12},
    accuracy=75,
    weight=30,
))
__NAME_DROPPER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.ROLODEX,
    damage={3: 5, 4: 6, 5: 7, 6: 10, 7: 14},
    accuracy=95,
    weight=40,
))
__NAME_DROPPER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.SYNERGY,
    damage={3: 3, 4: 4, 5: 6, 6: 9, 7: 12},
    accuracy=50,
    weight=15,
))
__NAME_DROPPER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.PICK_POCKET,
    damage={3: 2, 4: 2, 5: 2, 6: 2, 7: 2},
    accuracy=95,
    weight=15,
))
__NAME_DROPPER: SuitAttributes = SuitAttributes(key='nd', name=TTLocalizer.SuitNameDropper, singular=TTLocalizer.SuitNameDropperS, plural=TTLocalizer.SuitNameDropperP, tier=2, attacks=__NAME_DROPPER_ATTACKS)
__registerSuitAttributes(__NAME_DROPPER)

__GLAD_HANDER_ATTACKS = set()
__GLAD_HANDER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.RUBBER_STAMP,
    damage={4: 4, 5: 3, 6: 3, 7: 2, 8: 1},
    accuracy=90,
    weight=5,
))
__GLAD_HANDER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.FOUNTAIN_PEN,
    damage={4: 3, 5: 3, 6: 2, 7: 1, 8: 1},
    accuracy=70,
    weight=5,
))
__GLAD_HANDER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.FILIBUSTER,
    damage={4: 4, 5: 6, 6: 9, 7: 12, 8: 15},
    accuracy=30,
    weight=45,
))
__GLAD_HANDER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.SCHMOOZE,
    damage={4: 5, 5: 7, 6: 11, 7: 14, 8: 17},
    accuracy=55,
    weight=45,
))
__GLAD_HANDER: SuitAttributes = SuitAttributes(key='gh', name=TTLocalizer.SuitGladHander, singular=TTLocalizer.SuitGladHanderS, plural=TTLocalizer.SuitGladHanderP, tier=3, attacks=__GLAD_HANDER_ATTACKS)
__registerSuitAttributes(__GLAD_HANDER)

__MOVER__SHAKER_ATTACKS = set()
__MOVER__SHAKER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.BRAIN_STORM,
    damage={5: 5, 6: 6, 7: 8, 8: 10, 9: 12},
    accuracy=60,
    weight=15,
))
__MOVER__SHAKER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.HALF_WINDSOR,
    damage={5: 6, 6: 9, 7: 11, 8: 13, 9: 16},
    accuracy=50,
    weight=20,
))
__MOVER__SHAKER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.QUAKE,
    damage={5: 10, 6: 12, 7: 14, 8: 16, 9: 18},
    accuracy=60,
    weight=20,
))
__MOVER__SHAKER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.SHAKE,
    damage={5: 6, 6: 8, 7: 10, 8: 12, 9: 14},
    accuracy=70,
    weight=25,
))
__MOVER__SHAKER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.TREMOR,
    damage={5: 5, 6: 6, 7: 7, 8: 8, 9: 9},
    accuracy=50,
    weight=20,
))
__MOVER__SHAKER: SuitAttributes = SuitAttributes(key='ms', name=TTLocalizer.SuitMoverShaker, singular=TTLocalizer.SuitMoverShakerS, plural=TTLocalizer.SuitMoverShakerP, tier=4, attacks=__MOVER__SHAKER_ATTACKS)
__registerSuitAttributes(__MOVER__SHAKER)

__TWOFACE_ATTACKS = set()
__TWOFACE_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.EVIL_EYE,
    damage={6: 10, 7: 12, 8: 14, 9: 16, 10: 18},
    accuracy=60,
    weight=30,
))
__TWOFACE_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.HANG_UP,
    damage={6: 7, 7: 8, 8: 10, 9: 12, 10: 13},
    accuracy=50,
    weight=15,
))
__TWOFACE_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.RAZZLE_DAZZLE,
    damage={6: 8, 7: 10, 8: 12, 9: 14, 10: 16},
    accuracy=60,
    weight=30,
))
__TWOFACE_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.RED_TAPE,
    damage={6: 6, 7: 7, 8: 8, 9: 9, 10: 10},
    accuracy=60,
    weight=25,
))
__TWOFACE: SuitAttributes = SuitAttributes(key='tf', name=TTLocalizer.SuitTwoFace, singular=TTLocalizer.SuitTwoFaceS, plural=TTLocalizer.SuitTwoFaceP, tier=5, attacks=__TWOFACE_ATTACKS)
__registerSuitAttributes(__TWOFACE)

__THE_MINGLER_ATTACKS = set()
__THE_MINGLER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.BUZZ_WORD,
    damage={7: 10, 8: 11, 9: 13, 10: 15, 11: 16},
    accuracy=60,
    weight=25,
))
__THE_MINGLER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.PARADIGM_SHIFT,
    damage={7: 10, 8: 12, 9: 15, 10: 18, 11: 21},
    accuracy=65,
    weight=25,
))
__THE_MINGLER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.SCHMOOZE,
    damage={7: 7, 8: 8, 9: 12, 10: 15, 11: 16},
    accuracy=55,
    weight=35,
))
__THE_MINGLER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.TEE_OFF,
    damage={7: 8, 8: 9, 9: 10, 10: 11, 11: 12},
    accuracy=70,
    weight=15,
))
__THE_MINGLER: SuitAttributes = SuitAttributes(key='m', name=TTLocalizer.SuitTheMingler, singular=TTLocalizer.SuitTheMinglerS, plural=TTLocalizer.SuitTheMinglerP, tier=6, attacks=__THE_MINGLER_ATTACKS)
__registerSuitAttributes(__THE_MINGLER)

__MR_HOLLYWOOD_ATTACKS = set()
__MR_HOLLYWOOD_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.SONG_AND_DANCE,
    damage={8: 12, 9: 14, 10: 16, 11: 18, 12: 20},
    accuracy=50,
    weight=50,
))
__MR_HOLLYWOOD_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.RAZZLE_DAZZLE,
    damage={8: 14, 9: 16, 10: 18, 11: 21, 12: 24},
    accuracy=75,
    weight=50,
))
__MR_HOLLYWOOD: SuitAttributes = SuitAttributes(key='mh', name=TTLocalizer.SuitMrHollywood, singular=TTLocalizer.SuitMrHollywoodS, plural=TTLocalizer.SuitMrHollywoodP, tier=7, attacks=__MR_HOLLYWOOD_ATTACKS)
__registerSuitAttributes(__MR_HOLLYWOOD)

__TRAFFIC_MANAGER_ATTACKS = set()
__TRAFFIC_MANAGER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.EVIL_EYE,
    damage={6: 9, 7: 11, 8: 13, 9: 14, 10: 16},
    accuracy=60,
    weight=30,
))
__TRAFFIC_MANAGER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.POWER_TRIP,
    damage={6: 7, 7: 9, 8: 11, 9: 14, 10: 17},
    accuracy=50,
    weight=15,
))
__TRAFFIC_MANAGER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.PLAY_HARDBALL,
    damage={6: 11, 7: 13, 8: 15, 9: 18, 10: 21},
    accuracy=60,
    weight=30,
))
__TRAFFIC_MANAGER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.RED_TAPE,
    damage={6: 8, 7: 10, 8: 11, 9: 13, 10: 15},
    accuracy=60,
    weight=25,
))
__TRAFFIC_MANAGER: SuitAttributes = SuitAttributes(key='trf', name=TTLocalizer.SuitTrafficManager, singular=TTLocalizer.SuitTrafficManagerS, plural=TTLocalizer.SuitTrafficManagerP, tier=5, attacks=__TRAFFIC_MANAGER_ATTACKS)
__registerSuitAttributes(__TRAFFIC_MANAGER)

__SHORT_CHANGE_ATTACKS = set()
__SHORT_CHANGE_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.WATERCOOLER,
    damage={1: 2, 2: 2, 3: 3, 4: 4, 5: 6},
    accuracy=50,
    weight=20,
))
__SHORT_CHANGE_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.BOUNCE_CHECK,
    damage={1: 3, 2: 5, 3: 7, 4: 9, 5: 11},
    accuracy=75,
    weight=15,
))
__SHORT_CHANGE_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.CLIPON_TIE,
    damage={1: 1, 2: 1, 3: 2, 4: 2, 5: 3},
    accuracy=50,
    weight=25,
))
__SHORT_CHANGE_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.PICK_POCKET,
    damage={1: 2, 2: 2, 3: 3, 4: 4, 5: 6},
    accuracy=95,
    weight=40,
))
__SHORT_CHANGE: SuitAttributes = T1SuitAttributes(key='sc', name=TTLocalizer.SuitShortChange, singular=TTLocalizer.SuitShortChangeS, plural=TTLocalizer.SuitShortChangeP, tier=0, attacks=__SHORT_CHANGE_ATTACKS)
__registerSuitAttributes(__SHORT_CHANGE)

__PENNY_PINCHER_ATTACKS = set()
__PENNY_PINCHER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.BOUNCE_CHECK,
    damage={2: 4, 3: 5, 4: 6, 5: 8, 6: 12},
    accuracy=75,
    weight=45,
))
__PENNY_PINCHER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.FREEZE_ASSETS,
    damage={2: 2, 3: 3, 4: 4, 5: 6, 6: 9},
    accuracy=75,
    weight=20,
))
__PENNY_PINCHER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.FINGER_WAG,
    damage={2: 1, 3: 2, 4: 3, 5: 4, 6: 6},
    accuracy=50,
    weight=35,
))
__PENNY_PINCHER: SuitAttributes = SuitAttributes(key='pp', name=TTLocalizer.SuitPennyPincher, singular=TTLocalizer.SuitPennyPincherS, plural=TTLocalizer.SuitPennyPincherP, tier=1, attacks=__PENNY_PINCHER_ATTACKS)
__registerSuitAttributes(__PENNY_PINCHER)

__TIGHTWAD_ATTACKS = set()
__TIGHTWAD_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.FIRED,
    damage={3: 3, 4: 4, 5: 5, 6: 5, 7: 6},
    accuracy=75,
    weight=5,
))
__TIGHTWAD_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.GLOWER_POWER,
    damage={3: 3, 4: 4, 5: 6, 6: 9, 7: 12},
    accuracy=95,
    weight=30,
))
__TIGHTWAD_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.FINGER_WAG,
    damage={3: 3, 4: 3, 5: 4, 6: 4, 7: 5},
    accuracy=75,
    weight=5,
))
__TIGHTWAD_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.FREEZE_ASSETS,
    damage={3: 3, 4: 4, 5: 6, 6: 9, 7: 12},
    accuracy=75,
    weight=30,
))
__TIGHTWAD_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.BOUNCE_CHECK,
    damage={3: 5, 4: 6, 5: 9, 6: 12, 7: 15},
    accuracy=75,
    weight=30,
))
__TIGHTWAD: SuitAttributes = SuitAttributes(key='tw', name=TTLocalizer.SuitTightwad, singular=TTLocalizer.SuitTightwadS, plural=TTLocalizer.SuitTightwadP, tier=2, attacks=__TIGHTWAD_ATTACKS)
__registerSuitAttributes(__TIGHTWAD)

__BEAN_COUNTER_ATTACKS = set()
__BEAN_COUNTER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.AUDIT,
    damage={4: 4, 5: 6, 6: 9, 7: 12, 8: 15},
    accuracy=95,
    weight=20,
))
__BEAN_COUNTER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.CALCULATE,
    damage={4: 4, 5: 6, 6: 9, 7: 12, 8: 15},
    accuracy=75,
    weight=25,
))
__BEAN_COUNTER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.TABULATE,
    damage={4: 4, 5: 6, 6: 9, 7: 12, 8: 15},
    accuracy=75,
    weight=25,
))
__BEAN_COUNTER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.WRITE_OFF,
    damage={4: 4, 5: 6, 6: 9, 7: 12, 8: 15},
    accuracy=95,
    weight=30,
))
__BEAN_COUNTER: SuitAttributes = SuitAttributes(key='bc', name=TTLocalizer.SuitBeanCounter, singular=TTLocalizer.SuitBeanCounterS, plural=TTLocalizer.SuitBeanCounterP, tier=3, attacks=__BEAN_COUNTER_ATTACKS)
__registerSuitAttributes(__BEAN_COUNTER)

__NUMBER_CRUNCHER_ATTACKS = set()
__NUMBER_CRUNCHER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.AUDIT,
    damage={5: 5, 6: 6, 7: 8, 8: 10, 9: 12},
    accuracy=60,
    weight=10,
))
__NUMBER_CRUNCHER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.CALCULATE,
    damage={5: 6, 6: 7, 7: 9, 8: 11, 9: 13},
    accuracy=50,
    weight=25,
))
__NUMBER_CRUNCHER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.SYNERGY,
    damage={5: 6, 6: 7, 7: 8, 8: 9, 9: 10},
    accuracy=50,
    weight=20,
))
__NUMBER_CRUNCHER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.CRUNCH,
    damage={5: 8, 6: 9, 7: 11, 8: 13, 9: 15},
    accuracy=60,
    weight=30,
))
__NUMBER_CRUNCHER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.TABULATE,
    damage={5: 5, 6: 6, 7: 7, 8: 8, 9: 9},
    accuracy=50,
    weight=15,
))
__NUMBER_CRUNCHER: SuitAttributes = SuitAttributes(key='nc', name=TTLocalizer.SuitNumberCruncher, singular=TTLocalizer.SuitNumberCruncherS, plural=TTLocalizer.SuitNumberCruncherP, tier=4, attacks=__NUMBER_CRUNCHER_ATTACKS)
__registerSuitAttributes(__NUMBER_CRUNCHER)

__MONEY_BAGS_ATTACKS = set()
__MONEY_BAGS_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.LIQUIDATE,
    damage={6: 10, 7: 12, 8: 14, 9: 16, 10: 18},
    accuracy=60,
    weight=30,
))
__MONEY_BAGS_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.MARKET_CRASH,
    damage={6: 8, 7: 10, 8: 12, 9: 14, 10: 16},
    accuracy=60,
    weight=45,
))
__MONEY_BAGS_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.POWER_TIE,
    damage={6: 6, 7: 7, 8: 8, 9: 9, 10: 10},
    accuracy=60,
    weight=25,
))
__MONEY_BAGS: SuitAttributes = SuitAttributes(key='mb', name=TTLocalizer.SuitMoneyBags, singular=TTLocalizer.SuitMoneyBagsS, plural=TTLocalizer.SuitMoneyBagsP, tier=5, attacks=__MONEY_BAGS_ATTACKS)
__registerSuitAttributes(__MONEY_BAGS)

__LOAN_SHARK_ATTACKS = set()
__LOAN_SHARK_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.BITE,
    damage={7: 10, 8: 11, 9: 13, 10: 15, 11: 16},
    accuracy=60,
    weight=30,
))
__LOAN_SHARK_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.CHOMP,
    damage={7: 13, 8: 15, 9: 17, 10: 19, 11: 21},
    accuracy=60,
    weight=35,
))
__LOAN_SHARK_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.PLAY_HARDBALL,
    damage={7: 9, 8: 11, 9: 12, 10: 13, 11: 15},
    accuracy=55,
    weight=20,
))
__LOAN_SHARK_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.WRITE_OFF,
    damage={7: 6, 8: 8, 9: 10, 10: 12, 11: 14},
    accuracy=70,
    weight=15,
))
__LOAN_SHARK: SuitAttributes = SuitAttributes(key='ls', name=TTLocalizer.SuitLoanShark, singular=TTLocalizer.SuitLoanSharkS, plural=TTLocalizer.SuitLoanSharkP, tier=6, attacks=__LOAN_SHARK_ATTACKS)
__registerSuitAttributes(__LOAN_SHARK)

__ROBBER_BARON_ATTACKS = set()
__ROBBER_BARON_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.SYNERGY,
    damage={8: 12, 9: 15, 10: 18, 11: 21, 12: 24},
    accuracy=60,
    weight=50,
))
__ROBBER_BARON_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.TEE_OFF,
    damage={8: 10, 9: 12, 10: 14, 11: 16, 12: 18},
    accuracy=60,
    weight=50,
))
__ROBBER_BARON: SuitAttributes = SuitAttributes(key='rb', name=TTLocalizer.SuitRobberBaron, singular=TTLocalizer.SuitRobberBaronS, plural=TTLocalizer.SuitRobberBaronP, tier=7, attacks=__ROBBER_BARON_ATTACKS)
__registerSuitAttributes(__ROBBER_BARON)

__SKIN_FLINT_ATTACKS = set()
__SKIN_FLINT_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.PICK_POCKET,
    damage={6: 11, 7: 13, 8: 15, 9: 17, 10: 19},
    accuracy=60,
    weight=30,
))
__SKIN_FLINT_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.FINGER_WAG,
    damage={6: 8, 7: 10, 8: 12, 9: 14, 10: 16},
    accuracy=60,
    weight=45,
))
__SKIN_FLINT_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.POWER_TIE,
    damage={6: 6, 7: 8, 8: 9, 9: 11, 10: 12},
    accuracy=60,
    weight=25,
))
__SKIN_FLINT: SuitAttributes = SuitAttributes(key='ski', name=TTLocalizer.SuitSkinflint, singular=TTLocalizer.SuitSkinflintS, plural=TTLocalizer.SuitSkinflintP, tier=5, attacks=__SKIN_FLINT_ATTACKS)
__registerSuitAttributes(__SKIN_FLINT)

__BOTTOM_FEEDER_ATTACKS = set()
__BOTTOM_FEEDER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.RUBBER_STAMP,
    damage={1: 2, 2: 3, 3: 4, 4: 5, 5: 6},
    accuracy=75,
    weight=20,
))
__BOTTOM_FEEDER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.SHRED,
    damage={1: 2, 2: 4, 3: 6, 4: 8, 5: 10},
    accuracy=50,
    weight=20,
))
__BOTTOM_FEEDER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.WATERCOOLER,
    damage={1: 3, 2: 4, 3: 5, 4: 6, 5: 7},
    accuracy=95,
    weight=10,
))
__BOTTOM_FEEDER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.PICK_POCKET,
    damage={1: 1, 2: 1, 3: 2, 4: 2, 5: 3},
    accuracy=25,
    weight=50,
))
__BOTTOM_FEEDER: SuitAttributes = T1SuitAttributes(key='bf', name=TTLocalizer.SuitBottomFeeder, singular=TTLocalizer.SuitBottomFeederS, plural=TTLocalizer.SuitBottomFeederP, tier=0, attacks=__BOTTOM_FEEDER_ATTACKS)
__registerSuitAttributes(__BOTTOM_FEEDER)

__BLOODSUCKER_ATTACKS = set()
__BLOODSUCKER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.EVICTION_NOTICE,
    damage={2: 1, 3: 2, 4: 3, 5: 3, 6: 4},
    accuracy=75,
    weight=20,
))
__BLOODSUCKER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.RED_TAPE,
    damage={2: 2, 3: 3, 4: 4, 5: 6, 6: 9},
    accuracy=75,
    weight=20,
))
__BLOODSUCKER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.WITHDRAWAL,
    damage={2: 4, 3: 6, 4: 8, 5: 10, 6: 12},
    accuracy=95,
    weight=10,
))
__BLOODSUCKER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.LIQUIDATE,
    damage={2: 2, 3: 3, 4: 4, 5: 6, 6: 9},
    accuracy=50,
    weight=50,
))
__BLOODSUCKER: SuitAttributes = SuitAttributes(key='b', name=TTLocalizer.SuitBloodsucker, singular=TTLocalizer.SuitBloodsuckerS, plural=TTLocalizer.SuitBloodsuckerP, tier=1, attacks=__BLOODSUCKER_ATTACKS)
__registerSuitAttributes(__BLOODSUCKER)

__DOUBLE_TALKER_ATTACKS = set()
__DOUBLE_TALKER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.RUBBER_STAMP,
    damage={3: 1, 4: 1, 5: 1, 6: 1, 7: 1},
    accuracy=50,
    weight=5,
))
__DOUBLE_TALKER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.BOUNCE_CHECK,
    damage={3: 1, 4: 1, 5: 1, 6: 1, 7: 1},
    accuracy=50,
    weight=5,
))
__DOUBLE_TALKER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.BUZZ_WORD,
    damage={3: 1, 4: 2, 5: 3, 6: 5, 7: 6},
    accuracy=50,
    weight=20,
))
__DOUBLE_TALKER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.DOUBLE_TALK,
    damage={3: 6, 4: 6, 5: 9, 6: 12, 7: 15},
    accuracy=50,
    weight=25,
))
__DOUBLE_TALKER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.JARGON,
    damage={3: 3, 4: 4, 5: 6, 6: 9, 7: 12},
    accuracy=50,
    weight=25,
))
__DOUBLE_TALKER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.MUMBO_JUMBO,
    damage={3: 3, 4: 4, 5: 6, 6: 9, 7: 12},
    accuracy=50,
    weight=20,
))
__DOUBLE_TALKER: SuitAttributes = SuitAttributes(key='dt', name=TTLocalizer.SuitDoubleTalker, singular=TTLocalizer.SuitDoubleTalkerS, plural=TTLocalizer.SuitDoubleTalkerP, tier=2, attacks=__DOUBLE_TALKER_ATTACKS)
__registerSuitAttributes(__DOUBLE_TALKER)

__AMBULANCE_CHASER_ATTACKS = set()
__AMBULANCE_CHASER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.SHAKE,
    damage={4: 4, 5: 6, 6: 9, 7: 12, 8: 15},
    accuracy=75,
    weight=15,
))
__AMBULANCE_CHASER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.RED_TAPE,
    damage={4: 6, 5: 8, 6: 12, 7: 14, 8: 16},
    accuracy=75,
    weight=30,
))
__AMBULANCE_CHASER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.ROLODEX,
    damage={4: 3, 5: 4, 6: 5, 7: 6, 8: 7},
    accuracy=75,
    weight=20,
))
__AMBULANCE_CHASER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.HANG_UP,
    damage={4: 2, 5: 3, 6: 4, 7: 5, 8: 6},
    accuracy=75,
    weight=35,
))
__AMBULANCE_CHASER: SuitAttributes = SuitAttributes(key='ac', name=TTLocalizer.SuitAmbulanceChaser, singular=TTLocalizer.SuitAmbulanceChaserS, plural=TTLocalizer.SuitAmbulanceChaserP, tier=3, attacks=__AMBULANCE_CHASER_ATTACKS)
__registerSuitAttributes(__AMBULANCE_CHASER)

__BACK_STABBER_ATTACKS = set()
__BACK_STABBER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.GUILT_TRIP,
    damage={5: 8, 6: 11, 7: 13, 8: 15, 9: 18},
    accuracy=60,
    weight=40,
))
__BACK_STABBER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.RESTRAINING_ORDER,
    damage={5: 6, 6: 7, 7: 9, 8: 11, 9: 13},
    accuracy=50,
    weight=25,
))
__BACK_STABBER_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.FINGER_WAG,
    damage={5: 5, 6: 6, 7: 7, 8: 8, 9: 9},
    accuracy=50,
    weight=35,
))
__BACK_STABBER: SuitAttributes = SuitAttributes(key='bs', name=TTLocalizer.SuitBackStabber, singular=TTLocalizer.SuitBackStabberS, plural=TTLocalizer.SuitBackStabberP, tier=4, attacks=__BACK_STABBER_ATTACKS)
__registerSuitAttributes(__BACK_STABBER)

__SPIN_DOCTOR_ATTACKS = set()
__SPIN_DOCTOR_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.PARADIGM_SHIFT,
    damage={6: 9, 7: 10, 8: 13, 9: 16, 10: 17},
    accuracy=60,
    weight=30,
))
__SPIN_DOCTOR_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.QUAKE,
    damage={6: 8, 7: 10, 8: 12, 9: 14, 10: 16},
    accuracy=60,
    weight=20,
))
__SPIN_DOCTOR_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.SPIN,
    damage={6: 10, 7: 12, 8: 15, 9: 18, 10: 20},
    accuracy=70,
    weight=35,
))
__SPIN_DOCTOR_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.WRITE_OFF,
    damage={6: 6, 7: 7, 8: 8, 9: 9, 10: 10},
    accuracy=60,
    weight=15,
))
__SPIN_DOCTOR: SuitAttributes = SuitAttributes(key='sd', name=TTLocalizer.SuitSpinDoctor, singular=TTLocalizer.SuitSpinDoctorS, plural=TTLocalizer.SuitSpinDoctorP, tier=5, attacks=__SPIN_DOCTOR_ATTACKS)
__registerSuitAttributes(__SPIN_DOCTOR)

__LEGAL_EAGLE_ATTACKS = set()
__LEGAL_EAGLE_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.EVIL_EYE,
    damage={7: 10, 8: 11, 9: 13, 10: 15, 11: 16},
    accuracy=60,
    weight=20,
))
__LEGAL_EAGLE_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.JARGON,
    damage={7: 7, 8: 9, 9: 11, 10: 13, 11: 15},
    accuracy=60,
    weight=15,
))
__LEGAL_EAGLE_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.LEGALESE,
    damage={7: 11, 8: 13, 9: 16, 10: 19, 11: 21},
    accuracy=55,
    weight=35,
))
__LEGAL_EAGLE_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.PECKING_ORDER,
    damage={7: 12, 8: 15, 9: 17, 10: 19, 11: 22},
    accuracy=70,
    weight=30,
))
__LEGAL_EAGLE: SuitAttributes = SuitAttributes(key='le', name=TTLocalizer.SuitLegalEagle, singular=TTLocalizer.SuitLegalEagleS, plural=TTLocalizer.SuitLegalEagleP, tier=6, attacks=__LEGAL_EAGLE_ATTACKS)
__registerSuitAttributes(__LEGAL_EAGLE)

__BIG_WIG_ATTACKS = set()
__BIG_WIG_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.GUILT_TRIP,
    damage={8: 15, 9: 17, 10: 19, 11: 21, 12: 24},
    accuracy=60,
    weight=50,
))

# todo code animation for this
# __BIG_WIG_ATTACKS.add(SuitAttackAttribute(
#     attack=SuitAttackType.THROW_BOOK,
#     damage={8: 16, 9: 18, 10: 20, 11: 22, 12: 24},
#     accuracy=80,
#     weight=50,
# ))

__BIG_WIG_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.FINGER_WAG,
    damage={8: 16, 9: 18, 10: 20, 11: 22, 12: 24},
    accuracy=80,
    weight=50,
))
__BIG_WIG: SuitAttributes = SuitAttributes(key='bw', name=TTLocalizer.SuitBigWig, singular=TTLocalizer.SuitBigWigS, plural=TTLocalizer.SuitBigWigP, tier=7, attacks=__BIG_WIG_ATTACKS)
__registerSuitAttributes(__BIG_WIG)

__DEFENDENT_ATTACKS = set()
__DEFENDENT_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.MUMBO_JUMBO,
    damage={4: 5, 5: 7, 6: 10, 7: 12, 8: 14},
    accuracy=95,
    weight=20,
))
__DEFENDENT_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.JARGON,
    damage={4: 6, 5: 8, 6: 10, 7: 12, 8: 14},
    accuracy=75,
    weight=25,
))
__DEFENDENT_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.GUILT_TRIP,
    damage={4: 5, 5: 7, 6: 8, 7: 11, 8: 13},
    accuracy=75,
    weight=25,
))
__DEFENDENT_ATTACKS.add(SuitAttackAttribute(
    attack=SuitAttackType.LEGALESE,
    damage={4: 8, 5: 10, 6: 12, 7: 15, 8: 17},
    accuracy=95,
    weight=30,
))
__DEFENDENT: SuitAttributes = SuitAttributes(key='def', name=TTLocalizer.SuitDefendent, singular=TTLocalizer.SuitDefendentS, plural=TTLocalizer.SuitDefendentP, tier=3, attacks=__DEFENDENT_ATTACKS)
__registerSuitAttributes(__DEFENDENT)


"""
Helper methods for retrieving suit vitals and attack information.
"""


def getSuitAttributes(suitCode: str) -> SuitAttributes:
    return __ALL_SUIT_ATTRIBUTES.get(suitCode)


def getSuitAttacks(suitCode: str) -> Set[SuitAttackAttribute]:
    return getSuitAttributes(suitCode).attacks


# Given a set of SuitAttackAttribute instances, return a SuitAttackType.
# Use given weights in the set of attack attributes to randomly select one.
def pickSuitAttack(attacks: Set[SuitAttackAttribute], suitLevel: int) -> SuitAttackType:

    # todo this can 100% be optimized, but for now we just generate a weight map.
    choices = []

    # Loop through every attack
    for attack in attacks:
        # Add as many instances of the attack as the weight specifies. Higher weight = more chance to pick.
        choices.extend([attack.attack for _ in range(attack.weight)])

    debugWeightMap = {attack.attack.name: attack.weight for attack in attacks}
    notify.debug(f"pickSuitAttack() - Picking attack from {len(attacks)} options. Weight map: {debugWeightMap}")
    # Now pick a random one.
    return random.choice(choices)


# Given a suit attack type and the suits info, return an ugly dictionary representing the data within it.
# todo this is gross stop using cringe dicts
def getSuitAttack(suitName: str, suitLevel: int, attackType: SuitAttackType = SuitAttackType.NO_ATTACK):

    # If we passed in no attack or didn't specify one then generate a new one.
    attackChoices = getSuitAttacks(suitName)
    if attackType == SuitAttackType.NO_ATTACK:
        notify.debug('getSuitAttack: picking attacking for %s' % suitName)
        attackType = pickSuitAttack(attackChoices, suitLevel)

    suitAttributes: SuitAttributes = getSuitAttributes(suitName)
    attack: SuitAttackAttribute = suitAttributes.getAttack(attackType)
    notify.debug(f'getSuitAttack: querying attack data for suit {suitName} for attackType: {attackType.name}')
    adict = {'suitName': suitName}
    name = attack.attack.name
    adict['name'] = name
    adict['id'] = attack.attack.getId()
    adict['animName'] = __SuitAttacksToDefaultAnimation.get(attackType, 'magic1')
    adict['hp'] = attack.getBaseAttackDamage(suitLevel)
    adict['acc'] = suitAttributes.getAccuracyBoost(suitLevel) + attack.accuracy
    adict['freq'] = attack.weight
    adict['group'] = ATK_TGT_GROUP if attack.isGroupAttack() else ATK_TGT_SINGLE  # TODO refactor
    return adict


# Used to retrieve a list of all registered suits in the game. This is a fresh mutable list containing unique keys.
# For example, ['f', 'pp', 'ym', ...]
def getAllRegisteredSuits() -> List[str]:
    return list(__ALL_SUIT_ATTRIBUTES.keys())


"""
Utilities for Suit animations and Taunts and various text displaying properties for suits and attacks.
"""


__SuitAttacksToDefaultAnimation = {
    SuitAttackType.AUDIT:               'phone',
    SuitAttackType.BITE:                'throw-paper',
    SuitAttackType.BOUNCE_CHECK:        'throw-paper',
    SuitAttackType.BRAIN_STORM:         'effort',
    SuitAttackType.BUZZ_WORD:           'speak',
    SuitAttackType.CALCULATE:           'phone',
    SuitAttackType.CANNED:              'throw-paper',
    SuitAttackType.CHOMP:               'throw-paper',
    SuitAttackType.CIGAR_SMOKE:         'cigar-smoke',
    SuitAttackType.CLIPON_TIE:          'throw-paper',
    SuitAttackType.CRUNCH:              'throw-object',
    SuitAttackType.DEMOTION:            'magic1',
    SuitAttackType.DOUBLE_TALK:         'speak',
    SuitAttackType.DOWNSIZE:            'magic2',
    SuitAttackType.EVICTION_NOTICE:     'throw-paper',
    SuitAttackType.EVIL_EYE:            'glower',
    SuitAttackType.FILIBUSTER:          'speak',
    SuitAttackType.FILL_WITH_LEAD:      'pencil-sharpener',
    SuitAttackType.FINGER_WAG:          'finger-wag',
    SuitAttackType.FIRED:               'magic2',
    SuitAttackType.FIVE_O_CLOCK_SHADOW: 'glower',
    SuitAttackType.FLOOD_THE_MARKET:    'glower',
    SuitAttackType.FOUNTAIN_PEN:        'pen-squirt',
    SuitAttackType.FREEZE_ASSETS:       'glower',
    SuitAttackType.GAVEL:               'gavel',
    SuitAttackType.GLOWER_POWER:        'glower',
    SuitAttackType.GUILT_TRIP:          'magic1',
    SuitAttackType.HALF_WINDSOR:        'throw-paper',
    SuitAttackType.HANG_UP:             'phone',
    SuitAttackType.HEAD_SHRINK:         'magic1',
    SuitAttackType.HOT_AIR:             'speak',
    SuitAttackType.JARGON:              'speak',
    SuitAttackType.LEGALESE:            'speak',
    SuitAttackType.LIQUIDATE:           'magic1',
    SuitAttackType.MARKET_CRASH:        'throw-paper',
    SuitAttackType.MUMBO_JUMBO:         'speak',
    SuitAttackType.PARADIGM_SHIFT:      'magic2',
    SuitAttackType.PECKING_ORDER:       'throw-object',
    SuitAttackType.PICK_POCKET:         'pickpocket',
    SuitAttackType.PINK_SLIP:           'throw-paper',
    SuitAttackType.PLAY_HARDBALL:       'throw-paper',
    SuitAttackType.POUND_KEY:           'phone',
    SuitAttackType.POWER_TIE:           'throw-paper',
    SuitAttackType.POWER_TRIP:          'magic1',
    SuitAttackType.QUAKE:               'quick-jump',
    SuitAttackType.RAZZLE_DAZZLE:       'smile',
    SuitAttackType.RED_TAPE:            'throw-object',
    SuitAttackType.RE_ORG:              'magic3',
    SuitAttackType.RESTRAINING_ORDER:   'throw-paper',
    SuitAttackType.ROLODEX:             'roll-o-dex',
    SuitAttackType.RUBBER_STAMP:        'rubber-stamp',
    SuitAttackType.RUB_OUT:             'hold-eraser',
    SuitAttackType.SACKED:              'throw-paper',
    SuitAttackType.SANDTRAP:            'golf-club-swing',
    SuitAttackType.SCHMOOZE:            'speak',
    SuitAttackType.SHAKE:               'stomp',
    SuitAttackType.SHRED:               'shredder',
    SuitAttackType.SONG_AND_DANCE:      'song-and-dance',
    SuitAttackType.SPIN:                'magic3',
    SuitAttackType.SYNERGY:             'magic3',
    SuitAttackType.TABULATE:            'phone',
    SuitAttackType.TEE_OFF:             'golf-club-swing',
    SuitAttackType.THROW_BOOK:          'throw-object',
    SuitAttackType.TREMOR:              'stomp',
    SuitAttackType.WATERCOOLER:         'watercooler',
    SuitAttackType.WITHDRAWAL:          'magic1',
    SuitAttackType.WRITE_OFF:           'hold-pencil'
}

# Given an attack type, returns the default animation the suit will play for it.
def getSuitAnimationForAttack(attackType: SuitAttackType) -> str:
    return __SuitAttacksToDefaultAnimation.get(attackType, 'magic1')


def getFaceoffTaunt(suitName, doId):
    if suitName in SuitFaceoffTaunts:
        taunts = SuitFaceoffTaunts[suitName]
    else:
        taunts = TTLocalizer.SuitFaceoffDefaultTaunts
    return taunts[doId % len(taunts)]


SuitFaceoffTaunts = OTPLocalizer.SuitFaceoffTaunts


def getAttackTauntIndexFromIndex(suit, attackType: SuitAttackType):
    adict = getSuitAttack(suit.getStyleName(), suit.getActualLevel(), attackType)
    return getAttackTauntIndex(adict['name'])


def getAttackTauntIndex(attackName):
    if attackName in SuitAttackTaunts:
        taunts = SuitAttackTaunts[attackName]
        return random.randint(0, len(taunts) - 1)
    else:
        return 1


def getAttackTaunt(attackName, index=None):
    if attackName in SuitAttackTaunts:
        taunts = SuitAttackTaunts[attackName]
    else:
        taunts = TTLocalizer.SuitAttackDefaultTaunts
    if index != None:
        if index >= len(taunts):
            notify.warning('index exceeds length of taunts list in getAttackTaunt')
            return TTLocalizer.SuitAttackDefaultTaunts[0]
        return taunts[index]

    return random.choice(taunts)


# Similarly to getAttacksForSuit(), just returns the key representation of an attack instead.
def getAttackAnimationNamesForSuit(suitName: str) -> Set[str]:
    attackAnimNames: Set[str] = set()
    for attackType in getSuitAttacks(suitName):
        attackAnimNames.add(getSuitAnimationForAttack(attackType.attack))
    return attackAnimNames


SuitAttackTaunts = TTLocalizer.SuitAttackTaunts
