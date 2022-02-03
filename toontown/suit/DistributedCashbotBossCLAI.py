from direct.directnotify import DirectNotifyGlobal
from toontown.suit import DistributedCashbotBossAI


class DistributedCashbotBossCLAI(DistributedCashbotBossAI.DistributedCashbotBossAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedCashbotBossCLAI')

    def __init__(self, air):
        DistributedCashbotBossAI.DistributedCashbotBossAI.__init__(self, air)
