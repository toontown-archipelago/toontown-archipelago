from enum import Enum

from .. import items
from .LockBase import LockBase


class GagItemLock(LockBase):

    class Track(Enum):
        TOONUP = items.ITEM_TOONUP_FRAME
        TRAP = items.ITEM_TRAP_FRAME
        LURE = items.ITEM_LURE_FRAME
        SOUND = items.ITEM_SOUND_FRAME
        THROW = items.ITEM_THROW_FRAME
        SQUIRT = items.ITEM_SQUIRT_FRAME
        DROP = items.ITEM_DROP_FRAME

    def __init__(self, track: Track, frames_required: int):

        requirements = {track.value: frames_required}
        super().__init__(requirements)
