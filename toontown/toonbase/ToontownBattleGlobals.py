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

regMaxSkill = 10000
MaxSkill = 999999  # How high should we allow xp to go


def getUberDamageBonus(experience) -> float:
    overflow = experience - regMaxSkill
    if overflow < 0:
        overflow = 0

    # Returns a multiplier to multiply base damage by, default is 1% damage per 100 xp
    multiplier = 1 + overflow / 10000
    multiplier = round(multiplier, 2)
    return multiplier


# Returns a clean string representation of the damage bonus from above
def getUberDamageBonusString(experience) -> str:
    return str(int((getUberDamageBonus(experience) - 1) * 100))

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
    ((10, 0, 0, 0, 0, 0, 0), (10, 5, 0, 0, 0, 0, 0), (15, 10, 5, 0, 0, 0, 0), (20, 15, 10, 5, 0, 0, 0), (25, 20, 15, 7, 3, 0, 0), (30, 25, 20, 10, 5, 2, 0), (30, 25, 20, 15, 7, 3, 1)),
    ((10, 0, 0, 0, 0, 0, 0), (10, 5, 0, 0, 0, 0, 0), (15, 10, 5, 0, 0, 0, 0), (20, 15, 10, 5, 0, 0, 0), (25, 20, 15, 7, 3, 0, 0), (30, 25, 20, 10, 5, 2, 0), (30, 25, 20, 15, 7, 3, 1)),
    ((10, 0, 0, 0, 0, 0, 0), (10, 5, 0, 0, 0, 0, 0), (15, 10, 5, 0, 0, 0, 0), (20, 15, 10, 5, 0, 0, 0), (25, 20, 15, 7, 3, 0, 0), (30, 25, 20, 10, 5, 2, 0), (30, 25, 20, 15, 7, 3, 1)),
    ((10, 0, 0, 0, 0, 0, 0), (10, 5, 0, 0, 0, 0, 0), (15, 10, 5, 0, 0, 0, 0), (20, 15, 10, 5, 0, 0, 0), (25, 20, 15, 7, 3, 0, 0), (30, 25, 20, 10, 5, 2, 0), (30, 25, 20, 15, 7, 3, 1)),
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
    (0, 0, 0, 0, 0, 0, 0),          # Trap
    (50, 50, 60, 60, 70, 70, 95),   # Lure
    (95, 95, 95, 95, 95, 95, 95),   # Sound
    (75, 75, 75, 75, 75, 75, 75),   # Throw
    (95, 95, 95, 95, 95, 95, 95),   # Squirt
    (50, 50, 50, 50, 50, 50, 50)    # Drop
)

AvLureBonusAccuracy = (60, 60, 70, 70, 80, 80, 100)

AvTrackAccStrings = TTLocalizer.BattleGlobalAvTrackAccStrings


AvPropDamage = (
    (   # Toonup
        ((8, 10), (Levels[0][0], Levels[0][1])),
        ((15, 20), (Levels[0][1], Levels[0][2])),
        ((20, 25), (Levels[0][2], Levels[0][3])),
        ((36, 48), (Levels[0][3], Levels[0][4])),
        ((50, 60), (Levels[0][4], Levels[0][5])),
        ((80, 120), (Levels[0][5], Levels[0][6])),
        ((200, 200), (Levels[0][6], MaxSkill))
    ),
    (   # Trap
        ((12, 15), (Levels[1][0], Levels[1][1])),
        ((20, 25), (Levels[1][1], Levels[1][2])),
        ((35, 40), (Levels[1][2], Levels[1][3])),
        ((50, 60), (Levels[1][3], Levels[1][4])),
        ((70, 85), (Levels[1][4], Levels[1][5])),
        ((95, 185), (Levels[1][5], Levels[1][6])),
        ((195, 195), (Levels[1][6], MaxSkill))
    ),
    (   # Lure
        ((0, 0), (0, 0)),
        ((0, 0), (0, 0)),
        ((0, 0), (0, 0)),
        ((0, 0), (0, 0)),
        ((0, 0), (0, 0)),
        ((0, 0), (0, 0)),
        ((0, 0), (0, 0))
    ),
    (   # Sound
        ((2, 3), (Levels[3][0], Levels[3][1])),
        ((5, 7), (Levels[3][1], Levels[3][2])),
        ((9, 11), (Levels[3][2], Levels[3][3])),
        ((14, 16), (Levels[3][3], Levels[3][4])),
        ((20, 25), (Levels[3][4], Levels[3][5])),
        ((35, 60), (Levels[3][5], Levels[3][6])),
        ((80, 80), (Levels[3][6], MaxSkill))
    ),
    (   # Throw
        ((4, 6), (Levels[4][0], Levels[4][1])),
        ((8, 10), (Levels[4][1], Levels[4][2])),
        ((14, 17), (Levels[4][2], Levels[4][3])),
        ((24, 27), (Levels[4][3], Levels[4][4])),
        ((36, 40), (Levels[4][4], Levels[4][5])),
        ((48, 100), (Levels[4][5], Levels[4][6])),
        ((110, 110), (Levels[4][6], MaxSkill))
    ),
    (   # Squirt
        ((3, 4), (Levels[5][0], Levels[5][1])),
        ((6, 8), (Levels[5][1], Levels[5][2])),
        ((10, 12), (Levels[5][2], Levels[5][3])),
        ((18, 21), (Levels[5][3], Levels[5][4])),
        ((27, 30), (Levels[5][4], Levels[5][5])),
        ((36, 80), (Levels[5][5], Levels[5][6])),
        ((90, 90), (Levels[5][6], MaxSkill))
    ),
    (   # Drop
        ((10, 10), (Levels[6][0], Levels[6][1])),
        ((18, 18), (Levels[6][1], Levels[6][2])),
        ((30, 30), (Levels[6][2], Levels[6][3])),
        ((45, 45), (Levels[6][3], Levels[6][4])),
        ((60, 60), (Levels[6][4], Levels[6][5])),
        ((85, 170), (Levels[6][5], Levels[6][6])),
        ((180, 180), (Levels[6][6], MaxSkill))
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
                    organicBonus=False, propBonus=False, propAndOrganicBonusStack=False):

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

    multiplier = experience.getUberDamageBonus(attackTrack)
    damage *= multiplier

    if propAndOrganicBonusStack:
        originalDamage = damage
        if organicBonus:
            damage += getDamageBonus(originalDamage)
        if propBonus:
            damage += getDamageBonus(originalDamage)
    elif organicBonus or propBonus:
        damage += getDamageBonus(damage)
    return math.floor(damage)


def getDamageBonus(normal):
    bonus = math.floor(normal * 0.1)
    if bonus < 1 and normal > 0:
        bonus = 1
    return bonus


def isGroup(track, level):
    return AvPropTargetCat[AvPropTarget[track]][level]


def getInteriorCreditMultiplier(numFloors):
    return 1 + numFloors


def getFactoryCreditMultiplier(factoryId):

    if factoryId == ToontownGlobals.SellbotFactoryIntS:
        return 4.0

    return 3.0


def getFactoryMeritMultiplier(factoryId):
    if factoryId == ToontownGlobals.SellbotFactoryIntS:
        return 5.0

    return 4.0


def getMintCreditMultiplier(mintId):
    return {
        CashbotMintIntA: 4.0,
        CashbotMintIntB: 5.0,
        CashbotMintIntC: 6.0
    }.get(mintId, 3.0)


def getStageCreditMultiplier(stageId):
    return {
        LawbotStageIntA: 4.0,
        LawbotStageIntB: 5.0,
        LawbotStageIntC: 6.0,
        LawbotStageIntD: 7.0,
    }.get(stageId, 4.0)


def getCountryClubCreditMultiplier(countryClubId):
    return {
        BossbotCountryClubIntA: 5.0,
        BossbotCountryClubIntB: 6.0,
        BossbotCountryClubIntC: 7.0
    }.get(countryClubId, 4.0)


def getBossBattleCreditMultiplier(battleNumber):
    return 4 + battleNumber  # First round is usually battleNumber=1 btw


def getInvasionMultiplier():
    return 1.0


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
