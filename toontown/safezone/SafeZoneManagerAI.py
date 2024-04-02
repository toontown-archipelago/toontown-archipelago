from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

from toontown.toon.DistributedToonAI import DistributedToonAI
from toontown.toonbase import ToontownGlobals


class SafeZoneManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('SafeZoneManagerAI')

    def enterSafeZone(self):
        avId = self.air.getAvatarIdFromSender()
        if not avId:
            return

        # When a toon enters this zone, start a toon up task for them no matter what
        av = self.air.getDo(avId)
        if isinstance(av, DistributedToonAI):
            av.startToonUp(ToontownGlobals.PassiveHealFrequency)

    def exitSafeZone(self):
        avId = self.air.getAvatarIdFromSender()
        if not avId:
            return

        # When a toon leaves this zone, stop their toon up task
        av = self.air.getDo(avId)
        if isinstance(av, DistributedToonAI):
            av.stopToonUp()
