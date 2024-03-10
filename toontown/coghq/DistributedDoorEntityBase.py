

def stubFunction(*args):
    pass


class LockBase:
    stateNames = ['off',
     'locking',
     'locked',
     'unlocking',
     'unlocked']
    stateDurations = [None,
     3.5,
     None,
     2.0,
     None]


class DistributedDoorEntityBase:
    stateNames = ['off',
     'opening',
     'open',
     'closing',
     'closed']
    stateDurations = [None,
     2.5,
     1.0,
     6.0,
     None]
