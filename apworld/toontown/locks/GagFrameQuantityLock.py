from BaseClasses import CollectionState
from ..import items
from .LockBase import LockBase


class GagFrameQuantityLock(LockBase):

    def __init__(self, amount: int):
        self.amount = amount
        super().__init__({})

    def get_lock_function(self, player):

        def ret(state: CollectionState):

            num_frames = 0

            # Loop through all gag frame items and count how many we have
            for frame in items.GAG_TRAINING_FRAMES:
                num_frames += state.count(frame.value, player)

            # If we have enough this is unlocked
            return num_frames >= self.amount

        return ret
