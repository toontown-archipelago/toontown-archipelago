from .ToontownGlobals import *
import math
from . import TTLocalizer, ToontownGlobals
from ..toon.Experience import Experience

BattleCamFaceOffFov = 30.0
BattleCamFaceOffPos = Point3(0, -10, 4)
BattleCamDefaultPos = Point3(0, -8.6, 16.5)
BattleCamDefaultHpr = Vec3(0, -61, 0)
BattleCamDefaultFov = 80.0
BattleCamMenuFov = 65.0
BattleCamJoinPos = Point3(0, -12, 13)
BattleCamJoinHpr = Vec3(0, -45, 0)
SkipMovie = 0
BaseHp = 15
Tracks = TTLocalizer.BattleGlobalTracks
NPCTracks = TTLocalizer.BattleGlobalNPCTracks
TrackColors = ((211 / 255.0, 148 / 255.0, 255 / 255.0),
               (249 / 255.0, 255 / 255.0, 93 / 255.0),
               (79 / 255.0, 190 / 255.0, 76 / 255.0),
               (93 / 255.0, 108 / 255.0, 239 / 255.0),
               (255 / 255.0, 145 / 255.0, 66 / 255.0),
               (255 / 255.0, 65 / 255.0, 199 / 255.0),
               (67 / 255.0, 243 / 255.0, 255 / 255.0))
HEAL_TRACK = 0
TRAP_TRACK = 1
LURE_TRACK = 2
SOUND_TRACK = 3
THROW_TRACK = 4
SQUIRT_TRACK = 5
DROP_TRACK = 6
NPC_RESTOCK_GAGS = 7
NPC_TOONS_HIT = 8
NPC_COGS_MISS = 9
MIN_TRACK_INDEX = 0
MAX_TRACK_INDEX = 6
MIN_LEVEL_INDEX = 0
MAX_LEVEL_INDEX = 6
MAX_UNPAID_LEVEL_INDEX = 4
LAST_REGULAR_GAG_LEVEL = 6
UBER_GAG_LEVEL_INDEX = 6
NUM_GAG_TRACKS = 7
AvLureRounds = (2,
                2,
                3,
                3,
                4,
                4,
                10)
PropTypeToTrackBonus = {AnimPropTypes.Hydrant: SQUIRT_TRACK,
                        AnimPropTypes.Mailbox: THROW_TRACK,
                        AnimPropTypes.Trashcan: HEAL_TRACK}
Levels = [
          [0, 10, 40, 300, 1500, 4000, 10000],
          [0, 10, 40, 300, 1500, 4000, 10000],
          [0, 10, 40, 300, 1500, 4000, 10000],
          [0, 10, 40, 300, 1500, 4000, 10000],
          [0, 10, 40, 300, 1500, 4000, 10000],
          [0, 10, 40, 300, 1500, 4000, 10000],
          [0, 10, 40, 300, 1500, 4000, 10000]
]

regMaxSkill = 20000
MaxSkill = 999999  # How high should we allow xp to go

# Exp needed per % increase
overflowRates = [600, 300, 600, 700, 300, 300, 300]

def getUberDamageBonus(experience, track, overflowMod=None) -> float:
    overflow = experience - regMaxSkill
    if overflow < 0:
        overflow = 0
    if not overflowMod:
        overflowMod = base.localAvatar.getOverflowMod()
    adjustedOverflow = overflowRates[track] / (overflowMod / 100)
    multiplier = 1 + (overflow / adjustedOverflow / 100)
    multiplier = round(multiplier, 2)
    return multiplier


# Returns a clean string representation of the damage bonus from above
def getUberDamageBonusString(experience, track) -> str:
    return str(int((getUberDamageBonus(experience, track) - 1) * 100))

UnpaidMaxSkills = [Levels[0][1] - 1,
                   Levels[1][1] - 1,
                   Levels[2][1] - 1,
                   Levels[3][1] - 1,
                   Levels[4][4] - 1,
                   Levels[5][4] - 1,
                   Levels[6][1] - 1]
ExperienceCap = 99999

MaxToonAcc = 95
StartingLevel = 0
CarryLimits = (
    ((10, 0, 0, 0, 0, 0, 0), (10, 5, 0, 0, 0, 0, 0), (15, 10, 5, 0, 0, 0, 0), (20, 15, 10, 5, 0, 0, 0), (25, 20, 15, 7, 3, 0, 0), (30, 25, 20, 10, 5, 2, 0), (30, 25, 20, 10, 5, 2, 1)),
    ((10, 0, 0, 0, 0, 0, 0), (10, 5, 0, 0, 0, 0, 0), (15, 10, 5, 0, 0, 0, 0), (20, 15, 10, 5, 0, 0, 0), (25, 20, 15, 7, 3, 0, 0), (30, 25, 20, 10, 5, 2, 0), (30, 25, 20, 15, 7, 3, 1)),
    ((10, 0, 0, 0, 0, 0, 0), (10, 5, 0, 0, 0, 0, 0), (15, 10, 5, 0, 0, 0, 0), (20, 15, 10, 5, 0, 0, 0), (25, 20, 15, 7, 3, 0, 0), (30, 25, 20, 10, 4, 2, 0), (30, 25, 20, 15, 4, 3, 1)),
    ((10, 0, 0, 0, 0, 0, 0), (10, 5, 0, 0, 0, 0, 0), (15, 10, 5, 0, 0, 0, 0), (20, 15, 10, 5, 0, 0, 0), (25, 20, 15, 7, 3, 0, 0), (30, 25, 20, 10, 5, 2, 0), (30, 25, 20, 10, 5, 2, 1)),
    ((10, 0, 0, 0, 0, 0, 0), (10, 5, 0, 0, 0, 0, 0), (15, 10, 5, 0, 0, 0, 0), (20, 15, 10, 5, 0, 0, 0), (25, 20, 15, 7, 3, 0, 0), (30, 25, 20, 10, 5, 2, 0), (30, 25, 20, 15, 7, 3, 1)),
    ((10, 0, 0, 0, 0, 0, 0), (10, 5, 0, 0, 0, 0, 0), (15, 10, 5, 0, 0, 0, 0), (20, 15, 10, 5, 0, 0, 0), (25, 20, 15, 7, 3, 0, 0), (30, 25, 20, 10, 5, 2, 0), (30, 25, 20, 15, 7, 3, 1)),
    ((10, 0, 0, 0, 0, 0, 0), (10, 5, 0, 0, 0, 0, 0), (15, 10, 5, 0, 0, 0, 0), (20, 15, 10, 5, 0, 0, 0), (25, 20, 15, 7, 3, 0, 0), (30, 25, 20, 10, 5, 2, 0), (30, 25, 20, 15, 7, 3, 1)),
)

MaxProps = ((15, 40), (30, 60), (75, 80))
DLF_SKELECOG = 1
DLF_FOREMAN = 2
DLF_VP = 4
DLF_CFO = 8
DLF_SUPERVISOR = 16
DLF_VIRTUAL = 32
DLF_REVIVES = 64
pieNames = ['tart',
            'fruitpie-slice',
            'creampie-slice',
            'fruitpie',
            'creampie',
            'birthday-cake',
            'wedding-cake',
            'lawbook']
AvProps = (('feather',
            'bullhorn',
            'lipstick',
            'bamboocane',
            'pixiedust',
            'baton',
            'baton'),
           ('banana',
            'rake',
            'marbles',
            'quicksand',
            'trapdoor',
            'tnt',
            'traintrack'),
           ('1dollar',
            'smmagnet',
            '5dollar',
            'bigmagnet',
            '10dollar',
            'hypnogogs',
            'hypnogogs'),
           ('bikehorn',
            'whistle',
            'bugle',
            'aoogah',
            'elephant',
            'foghorn',
            'singing'),
           ('cupcake',
            'fruitpieslice',
            'creampieslice',
            'fruitpie',
            'creampie',
            'cake',
            'cake'),
           ('flower',
            'waterglass',
            'waterballoon',
            'bottle',
            'firehose',
            'stormcloud',
            'stormcloud'),
           ('flowerpot',
            'sandbag',
            'anvil',
            'weight',
            'safe',
            'piano',
            'piano'))
AvPropsNew = (('inventory_feather',
               'inventory_megaphone',
               'inventory_lipstick',
               'inventory_bamboo_cane',
               'inventory_pixiedust',
               'inventory_juggling_cubes',
               'inventory_ladder'),
              ('inventory_bannana_peel',
               'inventory_rake',
               'inventory_marbles',
               'inventory_quicksand_icon',
               'inventory_trapdoor',
               'inventory_tnt',
               'inventory_traintracks'),
              ('inventory_1dollarbill',
               'inventory_small_magnet',
               'inventory_5dollarbill',
               'inventory_big_magnet',
               'inventory_10dollarbill',
               'inventory_hypno_goggles',
               'inventory_screen'),
              ('inventory_bikehorn',
               'inventory_whistle',
               'inventory_bugle',
               'inventory_aoogah',
               'inventory_elephant',
               'inventory_fog_horn',
               'inventory_opera_singer'),
              ('inventory_tart',
               'inventory_fruit_pie_slice',
               'inventory_cream_pie_slice',
               'inventory_fruitpie',
               'inventory_creampie',
               'inventory_cake',
               'inventory_wedding'),
              ('inventory_squirt_flower',
               'inventory_glass_of_water',
               'inventory_water_gun',
               'inventory_seltzer_bottle',
               'inventory_firehose',
               'inventory_storm_cloud',
               'inventory_geyser'),
              ('inventory_flower_pot',
               'inventory_sandbag',
               'inventory_anvil',
               'inventory_weight',
               'inventory_safe_box',
               'inventory_piano',
               'inventory_ship'))
AvPropStrings = TTLocalizer.BattleGlobalAvPropStrings
AvPropStringsSingular = TTLocalizer.BattleGlobalAvPropStringsSingular
AvPropStringsPlural = TTLocalizer.BattleGlobalAvPropStringsPlural

AvPropAccuracy = (
    (100, 100, 100, 100, 100, 100, 100),  # Toonup
    (100, 100, 100, 100, 100, 100, 100),  # Trap
    (70, 70, 70, 70, 70, 70, 95),   # Lure
    (95, 95, 95, 95, 95, 95, 95),   # Sound
    (75, 75, 75, 75, 75, 75, 75),   # Throw
    (95, 95, 95, 95, 95, 95, 95),   # Squirt
    (70, 70, 70, 70, 70, 70, 70)    # Drop
)

AvLureBonusAccuracy = (80, 80, 80, 80, 80, 80, 100)


# Util method to show a clean percentage accuracy (base) string for a specific gag utilizing AvPropAccuracy defined here
def getAccuracyPercentString(track, level):
    return f"{AvPropAccuracy[track][level]}%"


AvPropDamage = (
    (   # Toonup
        ((8, 10), (Levels[0][0], Levels[0][1])),
        ((12, 16), (Levels[0][1], Levels[0][2])),
        ((18, 24), (Levels[0][2], Levels[0][3])),
        ((32, 40), (Levels[0][3], Levels[0][4])),
        ((45, 50), (Levels[0][4], Levels[0][5])),
        ((72, 96), (Levels[0][5], Levels[0][6])),
        ((100, 160), (Levels[0][6], regMaxSkill))
    ),
    (   # Trap
        ((12, 18), (Levels[1][0], Levels[1][1])),
        ((24, 30), (Levels[1][1], Levels[1][2])),
        ((35, 45), (Levels[1][2], Levels[1][3])),
        ((50, 75), (Levels[1][3], Levels[1][4])),
        ((85, 100), (Levels[1][4], Levels[1][5])),
        ((110, 195), (Levels[1][5], Levels[1][6])),
        ((200, 240), (Levels[1][6], regMaxSkill))
    ),
    (   # Lure
        ((30, 40), (Levels[2][0], Levels[2][1])),
        ((30, 40), (Levels[2][1], Levels[2][2])),
        ((40, 50), (Levels[2][2], Levels[2][3])),
        ((40, 50), (Levels[2][3], Levels[2][4])),
        ((50, 60), (Levels[2][4], Levels[2][5])),
        ((50, 60), (Levels[2][5], Levels[2][6])),
        ((65, 100), (Levels[2][6], regMaxSkill))
    ),
    (   # Sound
        ((2, 4), (Levels[3][0], Levels[3][1])),
        ((5, 8), (Levels[3][1], Levels[3][2])),
        ((9, 12), (Levels[3][2], Levels[3][3])),
        ((16, 20), (Levels[3][3], Levels[3][4])),
        ((25, 30), (Levels[3][4], Levels[3][5])),
        ((45, 75), (Levels[3][5], Levels[3][6])),
        ((90, 110), (Levels[3][6], regMaxSkill))
    ),
    (   # Throw
        ((4, 6), (Levels[4][0], Levels[4][1])),
        ((8, 10), (Levels[4][1], Levels[4][2])),
        ((14, 17), (Levels[4][2], Levels[4][3])),
        ((24, 27), (Levels[4][3], Levels[4][4])),
        ((36, 40), (Levels[4][4], Levels[4][5])),
        ((48, 100), (Levels[4][5], Levels[4][6])),
        ((110, 140), (Levels[4][6], regMaxSkill))
    ),
    (   # Squirt
        ((3, 4), (Levels[5][0], Levels[5][1])),
        ((6, 8), (Levels[5][1], Levels[5][2])),
        ((10, 12), (Levels[5][2], Levels[5][3])),
        ((18, 21), (Levels[5][3], Levels[5][4])),
        ((27, 30), (Levels[5][4], Levels[5][5])),
        ((36, 80), (Levels[5][5], Levels[5][6])),
        ((85, 110), (Levels[5][6], regMaxSkill))
    ),
    (   # Drop
        ((8, 10), (Levels[6][0], Levels[6][1])),
        ((15, 18), (Levels[6][1], Levels[6][2])),
        ((25, 30), (Levels[6][2], Levels[6][3])),
        ((42, 50), (Levels[6][3], Levels[6][4])),
        ((60, 75), (Levels[6][4], Levels[6][5])),
        ((90, 170), (Levels[6][5], Levels[6][6])),
        ((175, 210), (Levels[6][6], regMaxSkill))
    )
)
ATK_SINGLE_TARGET = 0
ATK_GROUP_TARGET = 1
AvPropTargetCat = ((ATK_SINGLE_TARGET,
                    ATK_GROUP_TARGET,
                    ATK_SINGLE_TARGET,
                    ATK_GROUP_TARGET,
                    ATK_SINGLE_TARGET,
                    ATK_GROUP_TARGET,
                    ATK_GROUP_TARGET),
                   (ATK_SINGLE_TARGET,
                    ATK_SINGLE_TARGET,
                    ATK_SINGLE_TARGET,
                    ATK_SINGLE_TARGET,
                    ATK_SINGLE_TARGET,
                    ATK_SINGLE_TARGET,
                    ATK_SINGLE_TARGET),
                   (ATK_GROUP_TARGET,
                    ATK_GROUP_TARGET,
                    ATK_GROUP_TARGET,
                    ATK_GROUP_TARGET,
                    ATK_GROUP_TARGET,
                    ATK_GROUP_TARGET,
                    ATK_GROUP_TARGET),
                   (ATK_SINGLE_TARGET,
                    ATK_SINGLE_TARGET,
                    ATK_SINGLE_TARGET,
                    ATK_SINGLE_TARGET,
                    ATK_SINGLE_TARGET,
                    ATK_SINGLE_TARGET,
                    ATK_GROUP_TARGET))
AvPropTarget = (0, 3, 0, 2, 3, 3, 3)


def getAvPropDamage(attackTrack, attackLevel, experience: Experience,
                    organicBonus=False, propBonus=False, propAndOrganicBonusStack=False, npc=False, toonDamageMultiplier=100, overflowMod=100):

    exp = experience.getExp(attackTrack)

    minD = AvPropDamage[attackTrack][attackLevel][0][0]
    maxD = AvPropDamage[attackTrack][attackLevel][0][1]
    minE = AvPropDamage[attackTrack][attackLevel][1][0]
    maxE = AvPropDamage[attackTrack][attackLevel][1][1]

    expVal = min(exp, maxE)
    expPerHp = float(maxE - minE + 1) / float(maxD - minD + 1)
    damage = math.floor((expVal - minE) / expPerHp) + minD

    if damage <= 0:
        damage = minD

    if not npc:
        multiplier = experience.getUberDamageBonus(attackTrack, overflowMod=overflowMod)
        damage *= multiplier
        damage *= toonDamageMultiplier / 100

    if propAndOrganicBonusStack:
        originalDamage = damage
        if organicBonus:
            damage += getDamageBonus(originalDamage)
        if propBonus:
            damage += getDamageBonus(originalDamage)
    elif organicBonus or propBonus:
        damage += getDamageBonus(damage)

    return math.ceil(damage)


def getDamageBonus(normal):
    bonus = math.ceil(normal * 0.1)
    if bonus < 1 and normal > 0:
        bonus = 1
    return bonus


def isGroup(track, level):
    return AvPropTargetCat[AvPropTarget[track]][level]


def getInteriorCreditMultiplier(numFloors):
    return 2 + numFloors


def getFactoryCreditMultiplier(factoryId):

    if factoryId == ToontownGlobals.SellbotFactoryIntS:
        return 6.0

    return 5.0


def getFactoryMeritMultiplier(factoryId):
    if factoryId == ToontownGlobals.SellbotFactoryIntS:
        return 6.0

    return 5.0


def getMintCreditMultiplier(mintId):
    return {
        CashbotMintIntA: 5.0,
        CashbotMintIntB: 6.0,
        CashbotMintIntC: 7.0
    }.get(mintId, 3.0)


def getStageCreditMultiplier(stageId):
    return {
        LawbotStageIntA: 6.0,
        LawbotStageIntB: 7.0,
        LawbotStageIntC: 8.0,
        LawbotStageIntD: 9.0,
    }.get(stageId, 4.0)


def getCountryClubCreditMultiplier(countryClubId):
    return {
        BossbotCountryClubIntA: 7.0,
        BossbotCountryClubIntB: 8.0,
        BossbotCountryClubIntC: 9.0
    }.get(countryClubId, 4.0)


def getBossBattleCreditMultiplier(battleNumber):
    return 4 + battleNumber  # First round is usually battleNumber=1 btw


def getMoreXpHolidayMultiplier():
    return 1.0


# Define any hoods that should have a special skill multiplier
def getHoodSkillCreditMultiplier(hoodId: int):
    return {

        ToontownGlobals.MinniesMelodyland: 2.0,
        ToontownGlobals.TheBrrrgh: 2.0,
        ToontownGlobals.DonaldsDreamland: 3.0,

        ToontownGlobals.SellbotHQ: 3.0,
        ToontownGlobals.CashbotHQ: 3.0,
        ToontownGlobals.LawbotHQ: 4.0,
        ToontownGlobals.BossbotHQ: 4.0,
    }.get(hoodId, 1.0)
