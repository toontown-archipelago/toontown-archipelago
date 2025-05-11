from otp.ai.AIBaseGlobal import *
from direct.distributed.ClockDelta import *
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM
from . import DistributedAnimatedPropAI
from direct.task.Task import Task
from direct.fsm import State
from toontown.hood import ZoneUtil
from toontown.safezone import TreasureGlobals
from toontown.toonbase import ToontownGlobals

class DistributedKnockKnockDoorAI(DistributedAnimatedPropAI.DistributedAnimatedPropAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedKnockKnockDoorAI')

    def __init__(self, air, propId):
        DistributedAnimatedPropAI.DistributedAnimatedPropAI.__init__(self, air, propId)
        self.fsm.setName('DistributedKnockKnockDoor')
        self.propId = propId
        self.doLaterTask = None
        return
    
    def attractTask(self, task):
        self.fsm.request('attract')

    def enterPlaying(self):
        DistributedAnimatedPropAI.DistributedAnimatedPropAI.enterPlaying(self)
        self.doLaterTask = taskMgr.doMethodLater(9, self.attractTask, self.uniqueName('knockKnock-timer'))

    def exitPlaying(self):
        DistributedAnimatedPropAI.DistributedAnimatedPropAI.exitPlaying(self)
        taskMgr.remove(self.doLaterTask)
        self.doLaterTask = None
        return

    def healToon(self):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        zoneId = ZoneUtil.getCanonicalHoodId(av.zoneId)
        self.notify.debug(f'zoneId: {zoneId}')
        healAmount = TreasureGlobals.healAmounts[zoneId]
        if av:
            av.toonUp(healAmount * av.getMaxHp())

    def knockKnockCheck(self, streetId):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        if av:
            jokeCount = av.slotData.get('jokes_per_street', 3)
            for joke in range(jokeCount):
                if self.getLocationFromStreedId(streetId, joke) in av.getCheckedLocations():
                    continue
                else:
                    av.addCheckedLocation(self.getLocationFromStreedId(streetId, joke))
                    break

    def getLocationFromStreedId(self, streetId, index):
        return ToontownGlobals.KNOCK_CODE_TO_LOCATION[streetId][index]