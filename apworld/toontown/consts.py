"""
Constants for Archipelago generation.
"""
from BaseClasses import Item, Location

BASE_ID = 0x501100

TWO_LAFF_BOOST_RATIO = 9 / 100
THREE_LAFF_BOOST_RATIO = 5 / 100
FOUR_LAFF_BOOST_RATIO = 3 / 100
FIVE_LAFF_BOOST_RATIO = 2 / 100

TWO_XP_BOOST_RATIO = 2 / 13


# The ratio of XP items required to reach a given gag level.
XP_RATIO_FOR_GAG_LEVEL = {
    1: 0.00,
    2: 0.00,
    3: 0.10,
    4: 0.20,
    5: 0.30,
    6: 0.40,
    7: 0.50,
    8: 0.60
}


class ToontownItem(Item):
    game: str = "Toontown"


class ToontownLocation(Location):
    game: str = "Toontown"


# The ratio of XP items required to reach a given gag level.
XP_RATIO_FOR_GAG_LEVEL = {
    1: 0.00,
    2: 0.00,
    3: 0.10,
    4: 0.20,
    5: 0.30,
    6: 0.40,
    7: 0.50,
    8: 0.60
}

# Max species obtainable for each rod tier.
## WARNING !!! FISHING LOCATION RULES MUST BE UPDATED IF THIS DICT IS CHANGED !!!
MAX_SPECIES_PER_ROD_TIER = {
    0: 10,
    1: 20,
    2: 35,
    3: 50,
    4: 70,
}


def can_catch_new_species(species: int, rod_tier: int) -> bool:
    return species < MAX_SPECIES_PER_ROD_TIER[rod_tier]
