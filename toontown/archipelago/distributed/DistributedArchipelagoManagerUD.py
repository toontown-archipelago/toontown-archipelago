from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD


class DistributedArchipelagoManagerUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedArchipelagoManagerUD")

    def __init__(self, air):
        super().__init__(air)
        print("DistributedArchipelagoManager starting up....")
