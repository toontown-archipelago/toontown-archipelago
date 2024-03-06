from typing import Dict

from BaseClasses import CollectionState


class LockBase:

    # To define a lock, simply pass in a dictionary that maps a dictionary of AP items (by string) to the amount
    # required
    def __init__(self, locks: Dict[str, int]):
        self.locks: Dict[str, int] = locks

    # Wrapper function so we can avoid using lambda
    def get_lock_function(self, player):
        def ret(state: CollectionState):
            # Loop through all the items contained in the lock
            for item, quantity_needed in self.locks.items():
                # If we do not have the required items needed we cannot progress
                if not state.has(item, player, quantity_needed):
                    return False
            # We had all required items, we can progress
            return True

        return ret