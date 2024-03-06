from .LockBase import LockBase


# Creates a lock that requires 1 of some items given in the constuctor
class MultiItemLock(LockBase):
    def __init__(self, *required_items):
        locks = {}
        for item in required_items:
            locks[item] = 1
        super().__init__(locks)
