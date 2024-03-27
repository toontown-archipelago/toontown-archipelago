from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal


class DistributedArchipelagoManager(DistributedObjectGlobal):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedArchipelagoManager")

    def __init__(self, cr):
        super().__init__(cr)
        print("DistributedArchipelagoManager starting up....")

