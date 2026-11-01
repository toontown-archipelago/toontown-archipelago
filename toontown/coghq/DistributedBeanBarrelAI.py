from . import DistributedBarrelBaseAI
from direct.directnotify import DirectNotifyGlobal
from direct.task import Task
import random

class DistributedBeanBarrelAI(DistributedBarrelBaseAI.DistributedBarrelBaseAI):

    def __init__(self, level, entityId):
        x = y = z = h = 0
        DistributedBarrelBaseAI.DistributedBarrelBaseAI.__init__(self, level, entityId)

    def d_setGrab(self, avId):
        self.notify.debug('d_setGrab %s' % avId)
        self.sendUpdate('setGrab', [avId])
        av = self.air.doId2do.get(avId)
        if av:
            av.addMoney(random.randint(750, 1250))
