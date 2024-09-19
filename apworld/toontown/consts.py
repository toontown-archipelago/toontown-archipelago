"""
Constants for Archipelago generation.
"""
from enum import IntFlag, auto
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

# The ratio of Gag Capacity items required to reach a given gag level.
CAP_RATIO_FOR_GAG_LEVEL = {
    1: 0.00,
    2: 0.00,
    3: 0.10,
    4: 0.15,
    5: 0.20,
    6: 0.25,
    7: 0.35,
    8: 0.40
}


class ToontownItem(Item):
    game: str = "Toontown"


class ToontownLocation(Location):
    game: str = "Toontown"


class ToontownWinCondition(IntFlag):
    cog_bosses = auto()
    total_tasks = auto()
    hood_tasks = auto()
    gag_tracks = auto()
    fish_species = auto()
    laff_o_lympics = auto()

    @classmethod
    def from_options(cls, options):
        """expects archipelago world options."""
        win_conditions = cls(0)
        if options.win_condition_cog_bosses.value:
            win_conditions = win_conditions | ToontownWinCondition.cog_bosses
        if options.win_condition_total_tasks.value:
            win_conditions = win_conditions | ToontownWinCondition.total_tasks
        if options.win_condition_hood_tasks.value:
            win_conditions = win_conditions | ToontownWinCondition.hood_tasks
        if options.win_condition_gag_tracks.value:
            win_conditions = win_conditions | ToontownWinCondition.gag_tracks
        if options.win_condition_fish_species.value:
            win_conditions = win_conditions | ToontownWinCondition.fish_species
        if options.win_condition_laff_o_lympics.value:
            win_conditions = win_conditions | ToontownWinCondition.laff_o_lympics
        return win_conditions
