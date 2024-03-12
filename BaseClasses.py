# Taken from https://github.com/ArchipelagoMW/Archipelago/blob/main/BaseClasses.py to assist with keeping
# definition files contained in this repo as 1 to 1 as possible to the files in the AP repo
# If you are modifying the apworld package, visit that link to see what methods and classes you can utilize.

# The purpose of this file is to simply allow us to use the same exact items and locations files in the toontown
# codebase and for the apworld package with no issue, so most of these classes are left empty
from enum import IntEnum, IntFlag


class LocationProgressType(IntEnum):
    DEFAULT = 1
    PRIORITY = 2
    EXCLUDED = 3


class ItemClassification(IntFlag):
    filler = 0b0000  # aka trash, as in filler items like ammo, currency etc,
    progression = 0b0001  # Item that is logically relevant
    useful = 0b0010  # Item that is generally quite useful, but not required for anything logical
    trap = 0b0100  # detrimental or entirely useless (nothing) item
    skip_balancing = 0b1000  # should technically never occur on its own
    # Item that is logically relevant, but progression balancing should not touch.
    # Typically currency or other counted items.
    progression_skip_balancing = 0b1001  # only progression gets balanced

    def as_flag(self) -> int:
        """As Network API flag int."""
        return int(self & 0b0111)


class CollectionState:

    def has(self, item: str, player_slot: int, quantity: int = 1) -> bool:
        return False

    def count(self, item: str, player :int) -> bool:
        return False


class Item:
    name: str


class Location:
    pass


class Region:
    pass


class Tutorial:
    def __init__(self, *args):
        pass


class MultiWorld:
    pass
