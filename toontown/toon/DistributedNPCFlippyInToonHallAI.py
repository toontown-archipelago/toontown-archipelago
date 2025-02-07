from .DistributedNPCToonAI import *


class DistributedNPCFlippyInToonHallAI(DistributedNPCToonAI):

    def __init__(self, air, npcId, questCallback=None, hq=0):
        DistributedNPCToonAI.__init__(self, air, npcId, questCallback)

    def avatarEnter(self):
        DistributedNPCToonBaseAI.avatarEnter(self)
        avId = self.air.getAvatarIdFromSender()
        self.notify.debug(f"{avId} speaking to flippy")

        toon: DistributedToonAI.DistributedToonAI = self.air.doId2do.get(avId)
        if not toon:
            return

        self.rejectAvatar(avId)
