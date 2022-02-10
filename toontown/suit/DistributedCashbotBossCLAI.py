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
