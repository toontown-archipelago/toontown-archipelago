from .LockBase import LockBase


class ItemLock(LockBase):

    def __init__(self, item: str, amount=1):
        locks = {item: amount}
        super().__init__(locks)
