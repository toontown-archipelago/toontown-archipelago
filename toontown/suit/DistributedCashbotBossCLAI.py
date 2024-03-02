from direct.directnotify import DirectNotifyGlobal
from toontown.suit import DistributedCashbotBossAI


class DistributedCashbotBossCLAI(DistributedCashbotBossAI.DistributedCashbotBossAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedCashbotBossCLAI')

    def __init__(self, air):
        DistributedCashbotBossAI.DistributedCashbotBossAI.__init__(self, air)

    def enterPrepareBattleThree(self):
        super(DistributedCashbotBossCLAI, self).enterPrepareBattleThree()

        # Only the first two toons are considered active participants
        if len(self.involvedToons) > 2:
            for spec in self.involvedToons[2:]:
                t = self.air.doId2do.get(spec)
                if t:
                    self.enableSpectator(t)

    # Put a toon in the required state to be a spectator
    def enableSpectator(self, av):
        if av.doId not in self.spectators:
            self.spectators.append(av.doId)
            av.b_setGhostMode(True)
            av.b_setImmortalMode(True)
            self.d_updateSpectators()

    # Put a toon in the required state to be participant
    def disableSpectator(self, av):
        if av.doId in self.spectators:
            self.spectators.remove(av.doId)
            av.b_setGhostMode(False)
            av.b_setImmortalMode(False)
            self.d_updateSpectators()

    def d_updateSpectators(self):
        self.sendUpdate('updateSpectators', [self.spectators])