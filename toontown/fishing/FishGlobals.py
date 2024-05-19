from typing import List, Tuple, Dict

from apworld.toontown.fish import FishGenus, ROD_DICT, FISH_DICT, FishDef, FishingRodDef, FishZone, get_catchable_fish, FishLocation
from toontown.toonbase import TTLocalizer
from math import ceil, pow
import random
from toontown.toonbase import ToontownGlobals
import copy

NoMovie = 0
EnterMovie = 1
ExitMovie = 2
CastMovie = 3
PullInMovie = 4
CastTimeout = 45.0
Nothing = 0
QuestItem = 1
FishItem = 2
JellybeanItem = 3
BootItem = 4
GagItem = 5
OverTankLimit = 8
FishItemNewEntry = 9
FishItemNewRecord = 10
BingoBoot = (BootItem, 99)
ProbabilityDict = {93: FishItem,
 94: JellybeanItem,
 100: BootItem}
SortedProbabilityCutoffs = list(ProbabilityDict.keys())
SortedProbabilityCutoffs.sort()
Rod2JellybeanDict = {0: 150,
 1: 200,
 2: 250,
 3: 300,
 4: 450}
HealAmount = 1
JellybeanFishingHolidayScoreMultiplier = 2
GlobalRarityDialBase = 4.3
FishingAngleMax = 50.0
OVERALL_VALUE_SCALE = 95
RARITY_VALUE_SCALE = 0.2
WEIGHT_VALUE_SCALE = 0.05 / 16.0
COLLECT_NO_UPDATE = 0
COLLECT_NEW_ENTRY = 1
COLLECT_NEW_RECORD = 2
RodFileDict = {0: 'phase_4/models/props/pole_treebranch-mod',
 1: 'phase_4/models/props/pole_bamboo-mod',
 2: 'phase_4/models/props/pole_wood-mod',
 3: 'phase_4/models/props/pole_steel-mod',
 4: 'phase_4/models/props/pole_gold-mod'}
RodPriceDict = {0: 0,
 1: 400,
 2: 800,
 3: 1200,
 4: 2000}
RodRarityFactor = {0: 1.0 / (GlobalRarityDialBase * 1),
 1: 1.0 / (GlobalRarityDialBase * 0.975),
 2: 1.0 / (GlobalRarityDialBase * 0.95),
 3: 1.0 / (GlobalRarityDialBase * 0.9),
 4: 1.0 / (GlobalRarityDialBase * 0.85)}
MaxRodId = 4
FishAudioFileDict = {
    -1: ("Clownfish.ogg", 1, 1.5, 1.0),
    FishGenus.BalloonFish: ("BalloonFish.ogg", 1, 0, 1.23),
    FishGenus.CatFish: ("CatFish.ogg", 1, 0, 1.26),
    FishGenus.Clownfish: ("Clownfish.ogg", 1, 1.5, 1.0),
    FishGenus.Frozen_Fish: ("Frozen_Fish.ogg", 1, 0, 1.0),
    FishGenus.Starfish: ("Starfish.ogg", 0, 0, 1.25),
    FishGenus.Holy_Mackerel: ("Holy_Mackerel.ogg", 1, 0.9, 1.0),
    FishGenus.Dog_Fish: ("Dog_Fish.ogg", 1, 0, 1.25),
    FishGenus.AmoreEel: ("AmoreEel.ogg", 1, 0, 1.0),
    FishGenus.Nurse_Shark: ("Nurse_Shark.ogg", 0, 0, 1.0),
    FishGenus.King_Crab: ("King_Crab.ogg", 0, 0, 1.0),
    FishGenus.Moon_Fish: ("Moon_Fish.ogg", 0, 1.0, 1.0),
    FishGenus.Seahorse: ("Seahorse.ogg", 1, 0, 1.26),
    FishGenus.Pool_Shark: ("Pool_Shark.ogg", 1, 2.0, 1.0),
    FishGenus.Bear_Acuda: ("Bear_Acuda.ogg", 1, 0, 1.0),
    FishGenus.CutThroatTrout: ("CutThroatTrout.ogg", 1, 0, 1.0),
    FishGenus.Piano_Tuna: ("Piano_Tuna.ogg", 0, 0, 1.0),
    FishGenus.PBJ_Fish: ("PBJ_Fish.ogg", 1, 0, 1.25),
    FishGenus.DevilRay: ("DevilRay.ogg", 0, 0, 1.0),
}
FishFileDict = {
    -1: (4, "clownFish-zero", "clownFish-swim", "clownFish-swim", None, (0.12, 0, -0.15), 0.38, -35, 20),
    FishGenus.BalloonFish:    (4, "balloonFish-zero", "balloonFish-swim", "balloonFish-swim", None, (0.0, 0, 0.0), 1.0, 0, 0),
    FishGenus.CatFish:        (4, "catFish-zero", "catFish-swim", "catFish-swim", None, (1.2, -2.0, 0.5), 0.22, -35, 10),
    FishGenus.Clownfish:      (4, "clownFish-zero", "clownFish-swim", "clownFish-swim", None, (0.12, 0, -0.15), 0.38, -35, 20),
    FishGenus.Frozen_Fish:    (4, "frozenFish-zero", "frozenFish-swim", "frozenFish-swim", None, (0, 0, 0), 0.5, -35, 20),
    FishGenus.Starfish:       (4, "starFish-zero", "starFish-swim", "starFish-swimLOOP", None, (0, 0, -0.38), 0.36, -35, 20),
    FishGenus.Holy_Mackerel:  (4, "holeyMackerel-zero", "holeyMackerel-swim", "holeyMackerel-swim", None, None, 0.4, 0, 0),
    FishGenus.Dog_Fish:       (4, "dogFish-zero", "dogFish-swim", "dogFish-swim", None, (0.8, -1.0, 0.275), 0.33, -38, 10),
    FishGenus.AmoreEel:       (4, "amoreEel-zero", "amoreEel-swim", "amoreEel-swim", None, (0.425, 0, 1.15), 0.5, 0, 60),
    FishGenus.Nurse_Shark:    (4, "nurseShark-zero", "nurseShark-swim", "nurseShark-swim", None, (0, 0, -0.15), 0.3, -40, 10),
    FishGenus.King_Crab:      (4, "kingCrab-zero", "kingCrab-swim", "kingCrab-swimLOOP", None, None, 0.4, 0, 0),
    FishGenus.Moon_Fish:      (4, "moonFish-zero", "moonFish-swim", "moonFish-swimLOOP", None, (-1.2, 14, -2.0), 0.33, 0, -10),
    FishGenus.Seahorse:       (4, "seaHorse-zero", "seaHorse-swim", "seaHorse-swim", None, (-0.57, 0.0, -2.1), 0.23, 33, -10),
    FishGenus.Pool_Shark:     (4, "poolShark-zero", "poolShark-swim", "poolShark-swim", None, (-0.45, 0, -1.8), 0.33, 45, 0),
    FishGenus.Bear_Acuda:     (4, "BearAcuda-zero", "BearAcuda-swim", "BearAcuda-swim", None, (0.65, 0, -3.3), 0.2, -35, 20),
    FishGenus.CutThroatTrout: (4, "cutThroatTrout-zero", "cutThroatTrout-swim", "cutThroatTrout-swim", None, (-0.2, 0, -0.1), 0.5, 35, 20),
    FishGenus.Piano_Tuna:     (4, "pianoTuna-zero", "pianoTuna-swim", "pianoTuna-swim", None, (0.3, 0, 0.0), 0.6, 40, 30),
    FishGenus.PBJ_Fish:       (4, "PBJfish-zero", "PBJfish-swim", "PBJfish-swim", None, (0, 0, 0.72), 0.31, -35, 10),
    FishGenus.DevilRay:       (4, "devilRay-zero", "devilRay-swim", "devilRay-swim", None, (0, 0, 0), 0.4, -35, 20),
}

TrophyDict = {0: (TTLocalizer.FishTrophyNameDict[0],),
 1: (TTLocalizer.FishTrophyNameDict[1],),
 2: (TTLocalizer.FishTrophyNameDict[2],),
 3: (TTLocalizer.FishTrophyNameDict[3],),
 4: (TTLocalizer.FishTrophyNameDict[4],),
 5: (TTLocalizer.FishTrophyNameDict[5],),
 6: (TTLocalizer.FishTrophyNameDict[6],)}
TTG = ToontownGlobals


def getSpecies(genus: FishGenus) -> Tuple[FishDef]:
    return FISH_DICT[genus]


def getGenera() -> List[int]:
    return [int(genus) for genus in FISH_DICT]


def getNumRods():
    return len(ROD_DICT)


def getCastCost(rodId: int):
    return ROD_DICT[rodId].cast_cost


def canBeCaughtByRod(genus: FishGenus, species: int, rodIndex: int):
    minFishWeight, maxFishWeight = getWeightRange(genus, species)
    minRodWeight, maxRodWeight = getRodWeightRange(rodIndex)
    if minRodWeight <= maxFishWeight and maxRodWeight >= minFishWeight:
        return 1
    else:
        return 0


def getRodWeightRange(rodIndex: int):
    return ROD_DICT[rodIndex].weight_range


def __rollRarityDice(rodId: int, rNumGen):
    if rNumGen is None:
        diceRoll = random.random()
    else:
        diceRoll = rNumGen.random()
    exp = RodRarityFactor[rodId]
    rarity = int(ceil(10 * (1 - pow(diceRoll, exp))))
    if rarity <= 0:
        rarity = 1
    return rarity


def getRandomWeight(genus: FishGenus, species: int, rodIndex = None, rNumGen = None):
    minFishWeight, maxFishWeight = getWeightRange(genus, species)
    if rodIndex is None:
        minWeight = minFishWeight
        maxWeight = maxFishWeight
    else:
        minRodWeight, maxRodWeight = getRodWeightRange(rodIndex)
        minWeight = max(minFishWeight, minRodWeight)
        maxWeight = min(maxFishWeight, maxRodWeight)

    randNumA = (rNumGen or random).random()
    randNumB = (rNumGen or random).random()
    randNum = (randNumA + randNumB) / 2.0
    randWeight = minWeight + (maxWeight - minWeight) * randNum
    return int(round(randWeight * 16))


__fish_rarity_cache = {}


def getRandomFishVitals(zoneId, rodId, rNumGen = None, location = FishLocation.Vanilla, forceRarity = None):
    catchable_fish = get_catchable_fish(zoneId, rodId, location)
    rolledRarity = forceRarity or __rollRarityDice(rodId, rNumGen)

    # Obtain cached value for this rarity.
    __fish_rarity_cache.setdefault(zoneId, {})
    __fish_rarity_cache[zoneId].setdefault(rodId, {})
    __fish_rarity_cache[zoneId][rodId].setdefault(location, {})
    __fish_rarity_cache[zoneId][rodId][location].setdefault(rolledRarity, None)
    catchableFishOfRarity = __fish_rarity_cache[zoneId][rodId][location][rolledRarity]

    # If cache miss, fill cache here.
    if catchableFishOfRarity is None:
        # Filter for all catchable fish in this rarity.
        catchableFishOfRarity = [
            (fishGenus, speciesIndex)
            for fishGenus, speciesIndex, rarity in catchable_fish
            if rarity == rolledRarity
        ]
        __fish_rarity_cache[zoneId][rodId][location][rolledRarity] = catchableFishOfRarity

    # Pick a random fish (if present).
    if catchableFishOfRarity:
        genus, species = (rNumGen or random).choice(catchableFishOfRarity)
        weight = getRandomWeight(genus, species, rodId, rNumGen)
        return 1, genus, species, weight

    return 0, 0, 0, 0


def getWeightRange(genus: FishGenus, species: int):
    return FISH_DICT[genus][species].weight_range


def getRarity(genus, species):
    return FISH_DICT[genus][species].rarity


def getValue(genus, species, weight):
    rarity = getRarity(genus, species)
    rarityValue = pow(RARITY_VALUE_SCALE * rarity, 1.5)
    weightValue = pow(WEIGHT_VALUE_SCALE * weight, 1.1)
    value = OVERALL_VALUE_SCALE * (rarityValue + weightValue)
    finalValue = int(ceil(value))
    base = getBase()
    if hasattr(base, 'cr') and base.cr:
        if hasattr(base.cr, 'newsManager') and base.cr.newsManager:
            holidayIds = base.cr.newsManager.getHolidayIdList()
            if ToontownGlobals.JELLYBEAN_FISHING_HOLIDAY in holidayIds or ToontownGlobals.JELLYBEAN_FISHING_HOLIDAY_MONTH in holidayIds:
                finalValue *= JellybeanFishingHolidayScoreMultiplier
    elif ToontownGlobals.JELLYBEAN_FISHING_HOLIDAY in simbase.air.holidayManager.currentHolidays or ToontownGlobals.JELLYBEAN_FISHING_HOLIDAY_MONTH in simbase.air.holidayManager.currentHolidays:
        finalValue *= JellybeanFishingHolidayScoreMultiplier
    return finalValue


__totalNumFish = len([
    (fishGenus, speciesIndex)
    for fishGenus in FISH_DICT
    for speciesIndex in FISH_DICT[fishGenus]
])


def getTotalNumFish():
    return __totalNumFish


def getAllFish() -> List[Tuple[FishGenus, int]]:

    fishies = []

    for genusID, thisGenusSpeciesList in FISH_DICT.items():
        for speciesID in range(len(thisGenusSpeciesList)):
            fishies.append((genusID, speciesID))

    return fishies


def getPondGeneraList(pondId):
    genusSet = set()
    catchableFish = get_catchable_fish(pondId, MaxRodId, FishLocation.Vanilla)
    for fishGenus, speciesIndex, rarity in catchableFish:
        genusSet.add(fishGenus)
    return list(genusSet)
