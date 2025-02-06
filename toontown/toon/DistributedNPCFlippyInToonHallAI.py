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

    # We reject the avatar when their completion condition isn't met
    def rejectAvatar(self, avId):
        self.busy = avId
        self.sendUpdate('setMovie',
                        [
                            NPCToons.QUEST_MOVIE_AP_WIN_CONDITION_NOT_MET,
                            self.npcId,
                            avId,
                            [],
                            ClockDelta.globalClockDelta.getRealNetworkTime()
                        ])

    # Called when a toon interacted with us and has satisfied their win condition
    def doAvatarVictory(self, av: DistributedToonAI):
        av.APVictory()
        self.sendUpdate('doToonVictory', [av.doId])
