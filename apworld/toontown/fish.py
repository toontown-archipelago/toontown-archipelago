"""
This module contains APWorld globals for fishing.
The game also uses these values for fishing as well.
"""
from dataclasses import dataclass, field
from enum import IntEnum, auto
from typing import Tuple, Dict, List, Set, Optional

from . import ToontownLocationName, ToontownItemName, ToontownRegionName


class FishLocation(IntEnum):
    """
    Determines where fish can spawn.
    """
    Playgrounds = 0
    Vanilla = 1
    Global = 2


class FishChecks(IntEnum):
    """
    Determines the amount of items that can be found from fishing.
    """
    AllSpecies = 0
    AllGalleryAndGenus = 1
    AllGallery = 2
    Nonne = 3


class FishProgression(IntEnum):
    """
    Determines the progression for fishing.
    """
    LicensesAndRods = 0
    Licenses = 1
    Rods = 2
    Nonne = 3


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


FishZoneToName: Dict[FishZone, str] = {
    FishZone.Anywhere: 'Anywhere',
    FishZone.MyEstate: 'My Estate',
    FishZone.DonaldsDock: 'Donald\'s Dock',
    FishZone.ToontownCentral: 'Toontown Central',
    FishZone.TheBrrrgh: 'The Brrrgh',
    FishZone.MinniesMelodyland: 'Minnie\'s Melodyland',
    FishZone.DaisyGardens: 'Daisy Gardens',
    FishZone.DonaldsDreamland: 'Donald\'s Dreamland',
    FishZone.BarnacleBoulevard: 'Barnacle Boulevard',
    FishZone.SeaweedStreet: 'Seaweed Street',
    FishZone.LighthouseLane: 'Lighthouse Lane',
    FishZone.SillyStreet: 'Silly Street',
    FishZone.LoopyLane: 'Loopy Lane',
    FishZone.PunchlinePlace: 'Punchline Place',
    FishZone.WalrusWay: 'Walrus Way',
    FishZone.SleetStreet: 'Sleet Street',
    FishZone.PolarPlace: 'Polar Place',
    FishZone.AltoAvenue: 'Alto Avenue',
    FishZone.BaritoneBoulevard: 'Baritone Boulevard',
    FishZone.TenorTerrace: 'Tenor Terrace',
    FishZone.ElmStreet: 'Elm Street',
    FishZone.MapleStreet: 'Maple Street',
    FishZone.OakStreet: 'Oak Street',
    FishZone.LullabyLane: 'Lullaby Lane',
    FishZone.PajamaPlace: 'Pajama Place',
}


PlaygroundFishZoneGroups: Dict[FishZone, Set[FishZone]] = {
    FishZone.DonaldsDock:       {FishZone.BarnacleBoulevard, FishZone.SeaweedStreet,     FishZone.LighthouseLane},
    FishZone.ToontownCentral:   {FishZone.SillyStreet,       FishZone.LoopyLane,         FishZone.PunchlinePlace},
    FishZone.TheBrrrgh:         {FishZone.WalrusWay,         FishZone.SleetStreet,       FishZone.PolarPlace},
    FishZone.MinniesMelodyland: {FishZone.AltoAvenue,        FishZone.BaritoneBoulevard, FishZone.TenorTerrace},
    FishZone.DaisyGardens:      {FishZone.ElmStreet,         FishZone.MapleStreet,       FishZone.OakStreet},
    FishZone.DonaldsDreamland:  {FishZone.LullabyLane,       FishZone.PajamaPlace},
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

    def get_filtered_zones(self, location: FishLocation) -> List[FishZone]:
        if location == FishLocation.Global or FishZone.Anywhere in self.zone_list:
            return [FishZone.Anywhere]

        filtered_zones = set()
        for zone in self.zone_list:
            if zone == FishZone.MyEstate:
                continue
            if location == FishLocation.Playgrounds:
                zone = get_playground_fish_zone(zone)
            filtered_zones.add(zone)

        # Remove redundant zones (aka, streets when their playground is already in)
        for zone in filtered_zones.copy():
            pgZone = get_playground_fish_zone(zone)
            if pgZone == zone:
                continue
            if pgZone in filtered_zones:
                filtered_zones.remove(zone)

        return list(filtered_zones)


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


def get_fish_def(genus: FishGenus, species: int) -> FishDef:
    return FISH_DICT[genus][species]


def can_catch_fish(fish: FishDef, rodId: int) -> bool:
    rod = ROD_DICT[rodId]
    return rod.weight_range[0] <= fish.weight_range[1] and rod.weight_range[1] >= fish.weight_range[0]


def get_required_rod(fish: FishDef) -> int:
    for rodId in ROD_DICT:
        if can_catch_fish(fish, rodId):
            return rodId
    raise KeyError(fish)


def get_effective_rarity(rarity: int, offset: int) -> int:
    return min(10, rarity + offset)


TTC_FISHING_MISSING = 32
DD_FISHING_MISSING = 33
DG_FISHING_MISSING = 34
MM_FISHING_MISSING = 35
TB_FISHING_MISSING = 36
DDL_FISHING_MISSING = 37
LICENSE_NONE = -1


LICENSE_TO_ACCESS_CODE = {
    FishZone.ToontownCentral: TTC_FISHING_MISSING,
    FishZone.DonaldsDock: DD_FISHING_MISSING,
    FishZone.DaisyGardens: DG_FISHING_MISSING,
    FishZone.MinniesMelodyland: MM_FISHING_MISSING,
    FishZone.TheBrrrgh: TB_FISHING_MISSING,
    FishZone.DonaldsDreamland: DDL_FISHING_MISSING,
    6000: LICENSE_NONE,
    8000: LICENSE_NONE,
    10000: LICENSE_NONE,
    11000: LICENSE_NONE,
    12000: LICENSE_NONE,
    13000: LICENSE_NONE,
    17000: LICENSE_NONE
}


def can_av_fish_here(av, zoneId) -> int:
    fishProgression = FishProgression(av.slotData.get('fish_progression', 3))
    needLicense = fishProgression in (FishProgression.Licenses, FishProgression.LicensesAndRods)
    if needLicense:
        hoodId = zoneId - zoneId % 1000
        accessCode = LICENSE_TO_ACCESS_CODE.get(hoodId)
        if not accessCode:
            raise KeyError("This is a bug, tell Mica (zoneId=%s, hoodId=%s)" % (zoneId, hoodId))
        if accessCode not in av.getAccessKeys():
            return accessCode
    return -1


def can_av_fish_at_zone(av, fishZone) -> bool:
    if fishZone == FishZone.MyEstate:
        return False
    elif fishZone == FishZone.Anywhere:
        fishProgression = FishProgression(av.slotData.get('fish_progression', 3))
        needLicense = fishProgression in (FishProgression.Licenses, FishProgression.LicensesAndRods)
        if needLicense:
            # True as long as they have any license.
            accessKeys = av.getAccessKeys()
            return any(
                accessCode in accessKeys
                for accessCode in LICENSE_TO_ACCESS_CODE.values()
            )
        else:
            return True
    else:
        return can_av_fish_here(av, fishZone) == -1


# A cache for the below function.
__catchable_fish_cache = {}


def get_catchable_fish(zone: FishZone, rodId: int, location: FishLocation) -> Set[Tuple[FishGenus, int, int]]:
    """
    Gets all catchable fish within a given zone with the current rod.
    """
    # Convert to branch ID.
    zone = zone - zone % 100
    if zone % 1000 >= 500:
        zone -= 500

    # Filter zone for their respective playground.
    if location == FishLocation.Playgrounds:
        zone = get_playground_fish_zone(zone)

    # Check cache.
    __catchable_fish_cache.setdefault(zone, {})
    __catchable_fish_cache[zone].setdefault(rodId, {})
    __catchable_fish_cache[zone][rodId].setdefault(location, set())
    __cached_result = __catchable_fish_cache[zone][rodId][location]
    if __cached_result:
        return __catchable_fish_cache[zone][rodId][location]

    # A set containg tuples of (FishGenus, SpeciesIndex, Rarity)
    fish_set: Set[Tuple[FishGenus, int, int]] = set()

    for fishGenus in FISH_DICT:
        for speciesIndex in range(len(FISH_DICT[fishGenus])):
            fishDef: FishDef = FISH_DICT[fishGenus][speciesIndex]

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
                if zone == fishZone or fishZone == FishZone.Anywhere:
                    # Add this fish.
                    rarity = get_effective_rarity(fishDef.rarity, zoneIndex)
                    fish_set.add((fishGenus, speciesIndex, rarity))

    # We're done here.
    __catchable_fish_cache[zone][rodId][location] = fish_set
    return fish_set


__catchable_fish_cache_no_rarity = {}


def get_catchable_fish_no_rarity(zone: FishZone, rodId: int, location: FishLocation) -> Set[Tuple[FishGenus, int]]:
    """
    Gets all catchable fish within a given zone with the current rod (no rarity)
    """
    # Filter zone for their respective playground.
    if location == FishLocation.Playgrounds:
        zone = get_playground_fish_zone(zone)

    # Check cache.
    __catchable_fish_cache_no_rarity.setdefault(zone, {})
    __catchable_fish_cache_no_rarity[zone].setdefault(rodId, {})
    __catchable_fish_cache_no_rarity[zone][rodId].setdefault(location, set())
    __cached_result = __catchable_fish_cache_no_rarity[zone][rodId][location]
    if __cached_result:
        return __catchable_fish_cache_no_rarity[zone][rodId][location]

    # A set containg tuples of (FishGenus, SpeciesIndex)
    fish_set: Set[Tuple[FishGenus, int]] = set()

    for fishData in get_catchable_fish(zone, rodId, location):
        genus, species, rarity = fishData
        fish_set.add((genus, species))

    # We're done here.
    __catchable_fish_cache_no_rarity[zone][rodId][location] = fish_set
    return fish_set


# Max species obtainable for each rod tier.
MAX_SPECIES_PER_ROD_TIER = {}

for rodTier in range(5):
    MAX_SPECIES_PER_ROD_TIER[rodTier] = len(get_catchable_fish(FishZone.ToontownCentral, rodTier, FishLocation.Global))


def can_catch_new_species(species: int, rod_tier: int) -> bool:
    return species < MAX_SPECIES_PER_ROD_TIER[rod_tier]


"""
Location definitions
"""

LOCATION_TO_GENUS_SPECIES: Dict[ToontownLocationName, Tuple[FishGenus, int]] = {
    ToontownLocationName.BALLOON_FISH_0:    (FishGenus.BalloonFish, 0),
    ToontownLocationName.BALLOON_FISH_1:    (FishGenus.BalloonFish, 1),
    ToontownLocationName.BALLOON_FISH_2:    (FishGenus.BalloonFish, 2),
    ToontownLocationName.BALLOON_FISH_3:    (FishGenus.BalloonFish, 3),
    ToontownLocationName.BALLOON_FISH_4:    (FishGenus.BalloonFish, 4),

    ToontownLocationName.JELLYFISH_0:       (FishGenus.PBJ_Fish, 0),
    ToontownLocationName.JELLYFISH_1:       (FishGenus.PBJ_Fish, 1),
    ToontownLocationName.JELLYFISH_2:       (FishGenus.PBJ_Fish, 2),
    ToontownLocationName.JELLYFISH_3:       (FishGenus.PBJ_Fish, 3),
    ToontownLocationName.JELLYFISH_4:       (FishGenus.PBJ_Fish, 4),

    ToontownLocationName.CAT_FISH_0:        (FishGenus.CatFish, 0),
    ToontownLocationName.CAT_FISH_1:        (FishGenus.CatFish, 1),
    ToontownLocationName.CAT_FISH_2:        (FishGenus.CatFish, 2),
    ToontownLocationName.CAT_FISH_3:        (FishGenus.CatFish, 3),
    ToontownLocationName.CAT_FISH_4:        (FishGenus.CatFish, 4),

    ToontownLocationName.CLOWN_FISH_0:      (FishGenus.Clownfish, 0),
    ToontownLocationName.CLOWN_FISH_1:      (FishGenus.Clownfish, 1),
    ToontownLocationName.CLOWN_FISH_2:      (FishGenus.Clownfish, 2),
    ToontownLocationName.CLOWN_FISH_3:      (FishGenus.Clownfish, 3),

    ToontownLocationName.FROZEN_FISH_0:     (FishGenus.Frozen_Fish, 0),

    ToontownLocationName.STAR_FISH_0:       (FishGenus.Starfish, 0),
    ToontownLocationName.STAR_FISH_1:       (FishGenus.Starfish, 1),
    ToontownLocationName.STAR_FISH_2:       (FishGenus.Starfish, 2),
    ToontownLocationName.STAR_FISH_3:       (FishGenus.Starfish, 3),
    ToontownLocationName.STAR_FISH_4:       (FishGenus.Starfish, 4),

    ToontownLocationName.HOLEY_MACKEREL_0:  (FishGenus.Holy_Mackerel, 0),

    ToontownLocationName.DOG_FISH_0:        (FishGenus.Dog_Fish, 0),
    ToontownLocationName.DOG_FISH_1:        (FishGenus.Dog_Fish, 1),
    ToontownLocationName.DOG_FISH_2:        (FishGenus.Dog_Fish, 2),
    ToontownLocationName.DOG_FISH_3:        (FishGenus.Dog_Fish, 3),
    ToontownLocationName.DOG_FISH_4:        (FishGenus.Dog_Fish, 4),

    ToontownLocationName.DEVIL_RAY_0:       (FishGenus.DevilRay, 0),

    ToontownLocationName.AMORE_EEL_0:       (FishGenus.AmoreEel, 0),
    ToontownLocationName.AMORE_EEL_1:       (FishGenus.AmoreEel, 1),

    ToontownLocationName.NURSE_SHARK_0:     (FishGenus.Nurse_Shark, 0),
    ToontownLocationName.NURSE_SHARK_1:     (FishGenus.Nurse_Shark, 1),
    ToontownLocationName.NURSE_SHARK_2:     (FishGenus.Nurse_Shark, 2),

    ToontownLocationName.KING_CRAB_0:       (FishGenus.King_Crab, 0),
    ToontownLocationName.KING_CRAB_1:       (FishGenus.King_Crab, 1),
    ToontownLocationName.KING_CRAB_2:       (FishGenus.King_Crab, 2),

    ToontownLocationName.MOON_FISH_0:       (FishGenus.Moon_Fish, 0),
    ToontownLocationName.MOON_FISH_1:       (FishGenus.Moon_Fish, 1),
    ToontownLocationName.MOON_FISH_2:       (FishGenus.Moon_Fish, 2),
    ToontownLocationName.MOON_FISH_3:       (FishGenus.Moon_Fish, 3),
    ToontownLocationName.MOON_FISH_4:       (FishGenus.Moon_Fish, 4),
    ToontownLocationName.MOON_FISH_5:       (FishGenus.Moon_Fish, 5),

    ToontownLocationName.SEA_HORSE_0:       (FishGenus.Seahorse, 0),
    ToontownLocationName.SEA_HORSE_1:       (FishGenus.Seahorse, 1),
    ToontownLocationName.SEA_HORSE_2:       (FishGenus.Seahorse, 2),
    ToontownLocationName.SEA_HORSE_3:       (FishGenus.Seahorse, 3),

    ToontownLocationName.POOL_SHARK_0:      (FishGenus.Pool_Shark, 0),
    ToontownLocationName.POOL_SHARK_1:      (FishGenus.Pool_Shark, 1),
    ToontownLocationName.POOL_SHARK_2:      (FishGenus.Pool_Shark, 2),
    ToontownLocationName.POOL_SHARK_3:      (FishGenus.Pool_Shark, 3),

    ToontownLocationName.BEAR_ACUDA_0:      (FishGenus.Bear_Acuda, 0),
    ToontownLocationName.BEAR_ACUDA_1:      (FishGenus.Bear_Acuda, 1),
    ToontownLocationName.BEAR_ACUDA_2:      (FishGenus.Bear_Acuda, 2),
    ToontownLocationName.BEAR_ACUDA_3:      (FishGenus.Bear_Acuda, 3),
    ToontownLocationName.BEAR_ACUDA_4:      (FishGenus.Bear_Acuda, 4),
    ToontownLocationName.BEAR_ACUDA_5:      (FishGenus.Bear_Acuda, 5),
    ToontownLocationName.BEAR_ACUDA_6:      (FishGenus.Bear_Acuda, 6),
    ToontownLocationName.BEAR_ACUDA_7:      (FishGenus.Bear_Acuda, 7),

    ToontownLocationName.CUTTHROAT_TROUT_0: (FishGenus.CutThroatTrout, 0),
    ToontownLocationName.CUTTHROAT_TROUT_1: (FishGenus.CutThroatTrout, 1),
    ToontownLocationName.CUTTHROAT_TROUT_2: (FishGenus.CutThroatTrout, 2),

    ToontownLocationName.PIANO_TUNA_0:      (FishGenus.Piano_Tuna, 0),
    ToontownLocationName.PIANO_TUNA_1:      (FishGenus.Piano_Tuna, 1),
    ToontownLocationName.PIANO_TUNA_2:      (FishGenus.Piano_Tuna, 2),
    ToontownLocationName.PIANO_TUNA_3:      (FishGenus.Piano_Tuna, 3),
    ToontownLocationName.PIANO_TUNA_4:      (FishGenus.Piano_Tuna, 4),
}
GENUS_SPECIES_TO_LOCATION: Dict[Tuple[FishGenus, int], ToontownLocationName] = {a: b for b, a in LOCATION_TO_GENUS_SPECIES.items()}


LOCATION_TO_GENUS: Dict[ToontownLocationName, FishGenus] = {
    ToontownLocationName.GENUS_BALLOON_FISH:    FishGenus.BalloonFish,
    ToontownLocationName.GENUS_CAT_FISH:        FishGenus.CatFish,
    ToontownLocationName.GENUS_CLOWN_FISH:      FishGenus.Clownfish,
    ToontownLocationName.GENUS_FROZEN_FISH:     FishGenus.Frozen_Fish,
    ToontownLocationName.GENUS_STAR_FISH:       FishGenus.Starfish,
    ToontownLocationName.GENUS_HOLEY_MACKEREL:  FishGenus.Holy_Mackerel,
    ToontownLocationName.GENUS_DOG_FISH:        FishGenus.Dog_Fish,
    ToontownLocationName.GENUS_AMORE_EEL:       FishGenus.AmoreEel,
    ToontownLocationName.GENUS_NURSE_SHARK:     FishGenus.Nurse_Shark,
    ToontownLocationName.GENUS_KING_CRAB:       FishGenus.King_Crab,
    ToontownLocationName.GENUS_MOON_FISH:       FishGenus.Moon_Fish,
    ToontownLocationName.GENUS_SEA_HORSE:       FishGenus.Seahorse,
    ToontownLocationName.GENUS_POOL_SHARK:      FishGenus.Pool_Shark,
    ToontownLocationName.GENUS_BEAR_ACUDA:      FishGenus.Bear_Acuda,
    ToontownLocationName.GENUS_CUTTHROAT_TROUT: FishGenus.CutThroatTrout,
    ToontownLocationName.GENUS_PIANO_TUNA:      FishGenus.Piano_Tuna,
    ToontownLocationName.GENUS_JELLYFISH:       FishGenus.PBJ_Fish,
    ToontownLocationName.GENUS_DEVIL_RAY:       FishGenus.DevilRay,
}
GENUS_TO_LOCATION: Dict[FishGenus, ToontownLocationName] = {a: b for b, a in LOCATION_TO_GENUS.items()}


FISH_ZONE_TO_LICENSE: Dict[FishZone, ToontownItemName] = {
    FishZone.ToontownCentral:   ToontownItemName.TTC_FISHING,
    FishZone.DonaldsDock:       ToontownItemName.DD_FISHING,
    FishZone.DaisyGardens:      ToontownItemName.DG_FISHING,
    FishZone.MinniesMelodyland: ToontownItemName.MML_FISHING,
    FishZone.TheBrrrgh:         ToontownItemName.TB_FISHING,
    FishZone.DonaldsDreamland:  ToontownItemName.DDL_FISHING,

    FishZone.BarnacleBoulevard: ToontownItemName.DD_FISHING,
    FishZone.SeaweedStreet:     ToontownItemName.DD_FISHING,
    FishZone.LighthouseLane:    ToontownItemName.DD_FISHING,
    FishZone.SillyStreet:       ToontownItemName.TTC_FISHING,
    FishZone.LoopyLane:         ToontownItemName.TTC_FISHING,
    FishZone.PunchlinePlace:    ToontownItemName.TTC_FISHING,
    FishZone.WalrusWay:         ToontownItemName.TB_FISHING,
    FishZone.SleetStreet:       ToontownItemName.TB_FISHING,
    FishZone.PolarPlace:        ToontownItemName.TB_FISHING,
    FishZone.AltoAvenue:        ToontownItemName.MML_FISHING,
    FishZone.BaritoneBoulevard: ToontownItemName.MML_FISHING,
    FishZone.TenorTerrace:      ToontownItemName.MML_FISHING,
    FishZone.ElmStreet:         ToontownItemName.DG_FISHING,
    FishZone.MapleStreet:       ToontownItemName.DG_FISHING,
    FishZone.OakStreet:         ToontownItemName.DG_FISHING,
    FishZone.LullabyLane:       ToontownItemName.DDL_FISHING,
    FishZone.PajamaPlace:       ToontownItemName.DDL_FISHING,
}

FISH_ZONE_TO_REGION: Dict[FishZone, ToontownRegionName] = {
    FishZone.ToontownCentral:   ToontownRegionName.TTC,
    FishZone.DonaldsDock:       ToontownRegionName.DD,
    FishZone.DaisyGardens:      ToontownRegionName.DG,
    FishZone.MinniesMelodyland: ToontownRegionName.MML,
    FishZone.TheBrrrgh:         ToontownRegionName.TB,
    FishZone.DonaldsDreamland:  ToontownRegionName.DDL,

    FishZone.BarnacleBoulevard: ToontownRegionName.DD,
    FishZone.SeaweedStreet:     ToontownRegionName.DD,
    FishZone.LighthouseLane:    ToontownRegionName.DD,
    FishZone.SillyStreet:       ToontownRegionName.TTC,
    FishZone.LoopyLane:         ToontownRegionName.TTC,
    FishZone.PunchlinePlace:    ToontownRegionName.TTC,
    FishZone.WalrusWay:         ToontownRegionName.TB,
    FishZone.SleetStreet:       ToontownRegionName.TB,
    FishZone.PolarPlace:        ToontownRegionName.TB,
    FishZone.AltoAvenue:        ToontownRegionName.MML,
    FishZone.BaritoneBoulevard: ToontownRegionName.MML,
    FishZone.TenorTerrace:      ToontownRegionName.MML,
    FishZone.ElmStreet:         ToontownRegionName.DG,
    FishZone.MapleStreet:       ToontownRegionName.DG,
    FishZone.OakStreet:         ToontownRegionName.DG,
    FishZone.LullabyLane:       ToontownRegionName.DDL,
    FishZone.PajamaPlace:       ToontownRegionName.DDL,
}

