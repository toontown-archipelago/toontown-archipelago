"""
This module contains APWorld globals for fishing.
The game also uses these values for fishing as well.
"""
from dataclasses import dataclass, field
from enum import IntEnum, auto
from typing import Tuple, Dict, List, Set, Optional


class FishGenus(IntEnum):
    BalloonFish    = 0
    CatFish        = 2
    Clownfish      = 4
    Frozen_Fish    = 6
    Starfish       = 8
    Holy_Mackerel  = 10
    Dog_Fish       = 12
    AmoreEel       = 14
    Nurse_Shark    = 16
    King_Crab      = 18
    Moon_Fish      = 20
    Seahorse       = 22
    Pool_Shark     = 24
    Bear_Acuda     = 26
    CutThroatTrout = 28
    Piano_Tuna     = 30
    PBJ_Fish       = 32
    DevilRay       = 34


class FishZone(IntEnum):
    Anywhere = 0  # used when populating the anywhere dict
    MyEstate = 1  # kept to preserve old rarities
    DonaldsDock = 1000
    ToontownCentral = 2000
    TheBrrrgh = 3000
    MinniesMelodyland = 4000
    DaisyGardens = 5000
    DonaldsDreamland = 9000
    BarnacleBoulevard = 1100
    SeaweedStreet = 1200
    LighthouseLane = 1300
    SillyStreet = 2100
    LoopyLane = 2200
    PunchlinePlace = 2300
    WalrusWay = 3100
    SleetStreet = 3200
    PolarPlace = 3300
    AltoAvenue = 4100
    BaritoneBoulevard = 4200
    TenorTerrace = 4300
    ElmStreet = 5100
    MapleStreet = 5200
    OakStreet = 5300
    LullabyLane = 9100
    PajamaPlace = 9200


PlaygroundFishZoneGroups: Dict[FishZone, Set[FishZone]] = {
    FishZone.DonaldsDock:       {FishZone.BarnacleBoulevard, FishZone.SeaweedStreet, FishZone.LighthouseLane},
    FishZone.ToontownCentral:   {FishZone.SillyStreet, FishZone.LoopyLane, FishZone.PunchlinePlace},
    FishZone.TheBrrrgh:         {FishZone.WalrusWay, FishZone.SleetStreet, FishZone.PolarPlace},
    FishZone.MinniesMelodyland: {FishZone.AltoAvenue, FishZone.BaritoneBoulevard, FishZone.TenorTerrace},
    FishZone.DaisyGardens:      {FishZone.ElmStreet, FishZone.MapleStreet, FishZone.OakStreet},
    FishZone.DonaldsDreamland:  {FishZone.LullabyLane, FishZone.PajamaPlace},
}


def get_playground_fish_zone(fish_zone: FishZone) -> FishZone:
    for pgFishZone, streetSet in PlaygroundFishZoneGroups.items():
        if fish_zone in streetSet:
            return pgFishZone
    return fish_zone


@dataclass
class FishDef:
    weight_range: Tuple[int, int]
    rarity: int
    zone_list: List[FishZone] = field(default_factory=list)


class FishLocation(IntEnum):
    """
    Determines the locations for how fish can spawn.
    """
    Playgrounds = 0
    Vanilla = 1
    Global = 2


# Fish dict is moved here from FishGlobals
FISH_DICT: Dict[FishGenus, Tuple[FishDef]] = {
    FishGenus.BalloonFish: (
        FishDef((1, 3), 1, [FishZone.Anywhere]),
        FishDef((1, 1), 4, [FishZone.ToontownCentral, FishZone.Anywhere]),
        FishDef((3, 5), 5, [FishZone.PunchlinePlace, FishZone.TheBrrrgh]),
        FishDef((3, 5), 3, [FishZone.SillyStreet, FishZone.DaisyGardens]),
        FishDef((1, 5), 2, [FishZone.LoopyLane, FishZone.ToontownCentral]),
    ),
    FishGenus.CatFish: (
        FishDef((2, 6), 1,  [FishZone.DaisyGardens, FishZone.Anywhere]),
        FishDef((2, 6), 9,  [FishZone.ElmStreet, FishZone.DaisyGardens]),
        FishDef((5, 11), 4, [FishZone.LullabyLane]),
        FishDef((2, 6), 3,  [FishZone.DaisyGardens, FishZone.MyEstate]),
        FishDef((5, 11), 2, [FishZone.DonaldsDreamland, FishZone.MyEstate]),
    ),
    FishGenus.Clownfish: (
        FishDef((2, 8), 1, [FishZone.ToontownCentral, FishZone.Anywhere]),
        FishDef((2, 8), 4, [FishZone.ToontownCentral, FishZone.Anywhere]),
        FishDef((2, 8), 2, [FishZone.ToontownCentral, FishZone.Anywhere]),
        FishDef((2, 8), 6, [FishZone.ToontownCentral, FishZone.MinniesMelodyland]),
    ),
    FishGenus.Frozen_Fish: (
        FishDef((8, 12), 1, [FishZone.TheBrrrgh]),
    ),
    FishGenus.Starfish: (
        FishDef((1, 5), 1,  [FishZone.Anywhere]),
        FishDef((2, 6), 2,  [FishZone.MinniesMelodyland, FishZone.Anywhere]),
        FishDef((5, 10), 5, [FishZone.MinniesMelodyland, FishZone.Anywhere]),
        FishDef((1, 5), 7,  [FishZone.MyEstate, FishZone.Anywhere]),
        FishDef((1, 5), 10, [FishZone.MyEstate, FishZone.Anywhere]),
    ),
    FishGenus.Holy_Mackerel: (
        FishDef((6, 10), 9, [FishZone.MyEstate, FishZone.Anywhere]),
    ),
    FishGenus.Dog_Fish: (
        FishDef((7, 15), 1,  [FishZone.DonaldsDock, FishZone.Anywhere]),
        FishDef((18, 20), 6, [FishZone.DonaldsDock, FishZone.MyEstate]),
        FishDef((1, 5), 5,   [FishZone.DonaldsDock, FishZone.MyEstate]),
        FishDef((3, 7), 4,   [FishZone.DonaldsDock, FishZone.MyEstate]),
        FishDef((1, 2), 2,   [FishZone.DonaldsDock, FishZone.Anywhere]),
    ),
    FishGenus.AmoreEel: (
        FishDef((2, 6), 1, [FishZone.DaisyGardens, FishZone.MyEstate, FishZone.Anywhere]),
        FishDef((2, 6), 3, [FishZone.DaisyGardens, FishZone.MyEstate]),
    ),
    FishGenus.Nurse_Shark: (
        FishDef((4, 12), 5, [FishZone.MinniesMelodyland, FishZone.Anywhere]),
        FishDef((4, 12), 7, [FishZone.BaritoneBoulevard, FishZone.MinniesMelodyland]),
        FishDef((4, 12), 8, [FishZone.TenorTerrace, FishZone.MinniesMelodyland]),
    ),
    FishGenus.King_Crab: (
        FishDef((2, 4), 3, [FishZone.DonaldsDock, FishZone.Anywhere]),
        FishDef((5, 8), 7, [FishZone.TheBrrrgh]),
        FishDef((4, 6), 8, [FishZone.LighthouseLane]),
    ),
    FishGenus.Moon_Fish: (
        FishDef((4, 6), 1,    [FishZone.DonaldsDreamland]),
        FishDef((14, 18), 10, [FishZone.DonaldsDreamland]),
        FishDef((6, 10), 8,   [FishZone.LullabyLane]),
        FishDef((1, 1), 3,    [FishZone.DonaldsDreamland]),
        FishDef((2, 6), 6,    [FishZone.LullabyLane]),
        FishDef((10, 14), 4,  [FishZone.DonaldsDreamland, FishZone.DaisyGardens]),
    ),
    FishGenus.Seahorse: (
        FishDef((12, 16), 2, [FishZone.MyEstate, FishZone.DaisyGardens, FishZone.Anywhere]),
        FishDef((14, 18), 3, [FishZone.MyEstate, FishZone.DaisyGardens, FishZone.Anywhere]),
        FishDef((14, 20), 5, [FishZone.MyEstate, FishZone.DaisyGardens]),
        FishDef((14, 20), 7, [FishZone.MyEstate, FishZone.DaisyGardens]),
    ),
    FishGenus.Pool_Shark: (
        FishDef((9, 11), 3, [FishZone.Anywhere]),
        FishDef((8, 12), 5, [FishZone.DaisyGardens, FishZone.DonaldsDock]),
        FishDef((8, 12), 6, [FishZone.DaisyGardens, FishZone.DonaldsDock]),
        FishDef((8, 16), 7, [FishZone.DaisyGardens, FishZone.DonaldsDock]),
    ),
    FishGenus.Bear_Acuda: (
        FishDef((10, 18), 2,  [FishZone.TheBrrrgh]),
        FishDef((10, 18), 3,  [FishZone.TheBrrrgh]),
        FishDef((10, 18), 4,  [FishZone.TheBrrrgh]),
        FishDef((10, 18), 5,  [FishZone.TheBrrrgh]),
        FishDef((12, 20), 6,  [FishZone.TheBrrrgh]),
        FishDef((14, 20), 7,  [FishZone.TheBrrrgh]),
        FishDef((14, 20), 8,  [FishZone.SleetStreet, FishZone.TheBrrrgh]),
        FishDef((16, 20), 10, [FishZone.WalrusWay, FishZone.TheBrrrgh]),
    ),
    FishGenus.CutThroatTrout: (
        FishDef((2, 10), 2, [FishZone.DonaldsDock, FishZone.Anywhere]),
        FishDef((4, 10), 6, [FishZone.BarnacleBoulevard, FishZone.DonaldsDock]),
        FishDef((4, 10), 7, [FishZone.SeaweedStreet, FishZone.DonaldsDock]),
    ),
    FishGenus.Piano_Tuna: (
        FishDef((13, 17), 5,  [FishZone.MinniesMelodyland, FishZone.Anywhere]),
        FishDef((16, 20), 10, [FishZone.AltoAvenue, FishZone.MinniesMelodyland]),
        FishDef((12, 18), 9,  [FishZone.TenorTerrace, FishZone.MinniesMelodyland]),
        FishDef((12, 18), 6,  [FishZone.MinniesMelodyland,]),
        FishDef((12, 18), 7,  [FishZone.MinniesMelodyland,]),
    ),
    FishGenus.PBJ_Fish: (
        FishDef((1, 5), 2,  [FishZone.ToontownCentral, FishZone.MyEstate, FishZone.Anywhere]),
        FishDef((1, 5), 3,  [FishZone.TheBrrrgh, FishZone.MyEstate, FishZone.Anywhere]),
        FishDef((1, 5), 4,  [FishZone.DaisyGardens, FishZone.MyEstate]),
        FishDef((1, 5), 5,  [FishZone.DonaldsDreamland, FishZone.MyEstate]),
        FishDef((1, 5), 10, [FishZone.TheBrrrgh, FishZone.DonaldsDreamland]),
    ),
    FishGenus.DevilRay: (
        FishDef((1, 20), 10, [FishZone.DonaldsDreamland, FishZone.Anywhere]),
    ),
}


@dataclass
class FishingRodDef:
    weight_range: Tuple[int, int]
    cast_cost: int


ROD_DICT: Dict[int, FishingRodDef] = {
    0: FishingRodDef((0, 4),  1),
    1: FishingRodDef((0, 8),  2),
    2: FishingRodDef((0, 12), 3),
    3: FishingRodDef((0, 16), 4),
    4: FishingRodDef((0, 20), 5),
}


def can_catch_fish(fish: FishDef, rodId: int) -> bool:
    rod = ROD_DICT[rodId]
    return rod.weight_range[0] <= fish.weight_range[1] and rod.weight_range[1] >= fish.weight_range[0]


def get_effective_rarity(rarity: int, offset: int) -> int:
    return min(10, rarity + offset)


# A cache for the below function.
__catchable_fish_cache = {}


def get_catchable_fish(zone: FishZone, rodId: int, location: FishLocation) -> Set[Tuple[FishGenus, int, int]]:
    """
    Gets all catchable fish within a given zone with the current rod.
    """
    __catchable_fish_cache.setdefault(zone, {})
    __catchable_fish_cache[zone].setdefault(rodId, {})
    __catchable_fish_cache[zone][rodId].setdefault(location, set())
    __cached_result = __catchable_fish_cache[zone][rodId][location]
    if __cached_result:
        return __catchable_fish_cache[zone][rodId][location]

    # A set containg tuples of (FishGenus, SpeciesIndex, Rarity)
    fish_set: Set[Tuple[FishGenus, int, int]] = set()

    # Filter zone for their respective playground.
    if location == FishLocation.Playgrounds:
        zone = get_playground_fish_zone(zone)

    for fishGenus in FISH_DICT:
        for speciesIndex in range(len(FISH_DICT[fishGenus])):
            fishDef: FishDef = FISH_DICT[fishGenus][speciesIndex]

            # In global locations, we collect all fish geni.
            # We can catch anything and everything!
            if location == FishLocation.Global:
                fish_set.add((fishGenus, speciesIndex, fishDef.rarity))
            else:
                # Determine the valid zones this fish can spawn in.
                for zoneIndex, fishZone in enumerate(fishDef.zone_list):
                    # Ignore the fish if it is not catchable.
                    if not can_catch_fish(fishDef, rodId):
                        continue

                    # Just add the fish now if we're in global locations.
                    if location == FishLocation.Global:
                        fish_set.add((fishGenus, speciesIndex, fishDef.rarity))
                        continue
                    # Playground locations treat the fish zone like the playground zone.
                    elif location == FishLocation.Playgrounds:
                        fishZone = get_playground_fish_zone(fishZone)

                    # Are we fishing here?
                    if zone == fishZone:
                        # Add this fish.
                        rarity = get_effective_rarity(fishDef.rarity, zoneIndex)
                        fish_set.add((fishGenus, speciesIndex, rarity))

    # We're done here.
    __catchable_fish_cache[zone][rodId][location] = fish_set
    return fish_set


__catchable_fish_no_rarity_cache = {}


def get_catchable_fish_without_rarity(zone: FishZone, rodId: int, location: FishLocation) -> Set[Tuple[FishGenus, int]]:
    # Get cached result.
    __catchable_fish_no_rarity_cache.setdefault(zone, {})
    __catchable_fish_no_rarity_cache[zone].setdefault(rodId, {})
    __catchable_fish_no_rarity_cache[zone][rodId].setdefault(location, set())
    __cached_result = __catchable_fish_no_rarity_cache[zone][rodId][location]
    if __cached_result:
        return __catchable_fish_no_rarity_cache[zone][rodId][location]

    # Set cached result.
    catchableFish = set()
    for fishGenus, speciesIndex, rarity in get_catchable_fish(zone, rodId, location):
        catchableFish.add((fishGenus, speciesIndex))
    __catchable_fish_no_rarity_cache[zone][rodId][location] = catchableFish
    return catchableFish
