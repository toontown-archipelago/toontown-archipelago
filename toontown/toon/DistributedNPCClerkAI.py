from otp.ai.AIBaseGlobal import *
from direct.task.Task import Task
from panda3d.core import *
from .DistributedNPCToonBaseAI import *

class DistributedNPCClerkAI(DistributedNPCToonBaseAI):

    def __init__(self, air, npcId):
        DistributedNPCToonBaseAI.__init__(self, air, npcId)

    def delete(self):
        taskMgr.remove(self.uniqueName('clearMovie'))
        self.ignoreAll()
        DistributedNPCToonBaseAI.delete(self)

    def avatarEnter(self):
        avId = self.air.getAvatarIdFromSender()
        DistributedNPCToonBaseAI.avatarEnter(self)
        av = self.air.doId2do.get(avId)
        if av is None:
            self.notify.warning('toon isnt there! toon: %s' % avId)
            return
        self.acceptOnce(self.air.getAvatarExitEvent(avId), self.__handleUnexpectedExit, extraArgs=[avId])

        if av.getMoney():
            self.sendStartMovie(avId)
        else:
            self.sendNoMoneyMovie(avId)
        return

    def sendStartMovie(self, avId):
        self.sendUpdate('setMovie', [NPCToons.PURCHASE_MOVIE_START,
         self.npcId,
         avId,
         ClockDelta.globalClockDelta.getRealNetworkTime()])
        taskMgr.doMethodLater(NPCToons.CLERK_COUNTDOWN_TIME, self.sendTimeoutMovie, self.uniqueName('clearMovie'), extraArgs=[avId])

    def sendNoMoneyMovie(self, avId):
        self.sendUpdate('setMovie', [NPCToons.PURCHASE_MOVIE_NO_MONEY,
         self.npcId,
         avId,
         ClockDelta.globalClockDelta.getRealNetworkTime()])
        self.sendClearMovie(avId, None)
        return

    def sendTimeoutMovie(self, avId, task=None):
        self.sendUpdate('setMovie', [NPCToons.PURCHASE_MOVIE_TIMEOUT,
         self.npcId,
         avId,
         ClockDelta.globalClockDelta.getRealNetworkTime()])
        self.sendClearMovie(avId, None)
        return Task.done

    def sendClearMovie(self, avId, task):
        self.sendUpdate('setMovie', [NPCToons.PURCHASE_MOVIE_CLEAR,
         self.npcId,
         avId,
         ClockDelta.globalClockDelta.getRealNetworkTime()])
        return Task.done

    def completePurchase(self, avId):
        self.sendUpdate('setMovie', [NPCToons.PURCHASE_MOVIE_COMPLETE,
         self.npcId,
         avId,
         ClockDelta.globalClockDelta.getRealNetworkTime()])
        return

    def setInventory(self, blob, newMoney, done):
        avId = self.air.getAvatarIdFromSender()
        if avId in self.air.doId2do:
            av = self.air.doId2do[avId]
            newInventory = av.inventory.makeFromNetString(blob)
            currentMoney = av.getMoney()
            if av.inventory.validatePurchase(newInventory, currentMoney, newMoney):
                av.setMoney(newMoney)
                if done:
                    av.d_setInventory(av.inventory.makeNetString())
                    av.d_setMoney(newMoney)
            else:
                self.air.writeServerEvent('suspicious', avId, 'DistributedNPCClerkAI.setInventory invalid purchase')
                self.notify.warning('Avatar ' + str(avId) + ' attempted an invalid purchase.')
                av.d_setInventory(av.inventory.makeNetString())
                av.d_setMoney(av.getMoney())

        if done:
            taskMgr.remove(self.uniqueName('clearMovie'))
            self.completePurchase(avId)

    def __handleUnexpectedExit(self, avId):
        self.notify.warning('avatar:' + str(avId) + ' has exited unexpectedly')
        self.sendTimeoutTimeoutMovie(avId, None)
        return
