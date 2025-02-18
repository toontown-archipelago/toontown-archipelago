from otp.ai.AIBaseGlobal import *
from direct.distributed.ClockDelta import *
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM
from . import DistributedAnimatedPropAI
from direct.task.Task import Task
from direct.fsm import State
from toontown.hood import ZoneUtil
from toontown.safezone import  TreasureGlobals

class DistributedKnockKnockDoorAI(DistributedAnimatedPropAI.DistributedAnimatedPropAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedKnockKnockDoorAI')

    def __init__(self, air, propId):
        DistributedAnimatedPropAI.DistributedAnimatedPropAI.__init__(self, air, propId)
        self.fsm.setName('DistributedKnockKnockDoor')
        self.propId = propId
        self.doLaterTask = None
        self.cooldown = False
        return
    
    def attractTask(self, task):
        self.fsm.request('attract')
    
    def setCooldown(self):
        self.cooldown = True
        taskMgr.doMethodLater(60, self.resetCooldown, self.uniqueName('knockKnock-cooldown'))

    def resetCooldown(self, task):
        self.cooldown = False
        return Task.done

    def enterPlaying(self):
        DistributedAnimatedPropAI.DistributedAnimatedPropAI.enterPlaying(self)
        self.doLaterTask = taskMgr.doMethodLater(9, self.attractTask, self.uniqueName('knockKnock-timer'))

    def exitPlaying(self):
        DistributedAnimatedPropAI.DistributedAnimatedPropAI.exitPlaying(self)
        taskMgr.remove(self.doLaterTask)
        self.doLaterTask = None
        return

    def healToon(self, avId):
        if self.cooldown:
            return
        av = self.air.doId2do.get(avId)
        zoneId = ZoneUtil.getCanonicalHoodId(av.zoneId)
        self.notify.debug(f'zoneId: {zoneId}')
        healAmount = TreasureGlobals.healAmounts[zoneId]
        if av:
            av.toonUp(healAmount * av.getMaxHp())
            self.setCooldown()