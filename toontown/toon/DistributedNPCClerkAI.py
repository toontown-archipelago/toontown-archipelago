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

    def sendStartMovie(self, avId):
        self.sendUpdate('setMovie', [NPCToons.PURCHASE_MOVIE_START,
         self.npcId,
         avId,
         ClockDelta.globalClockDelta.getRealNetworkTime()])
        # taskMgr.doMethodLater(NPCToons.CLERK_COUNTDOWN_TIME, self.sendTimeoutMovie, self.uniqueName('clearMovie'), extraArgs=[avId])

    def sendNoMoneyMovie(self, avId):
        self.sendUpdate('setMovie', [NPCToons.PURCHASE_MOVIE_NO_MONEY,
         self.npcId,
         avId,
         ClockDelta.globalClockDelta.getRealNetworkTime()])
        self.sendClearMovie(avId, None)
        return

    def sendTimeoutMovie(self, avId=0, task=None):
        self.sendUpdate('setMovie', [NPCToons.PURCHASE_MOVIE_TIMEOUT,
         self.npcId,
         avId,
         ClockDelta.globalClockDelta.getRealNetworkTime()])
        self.sendClearMovie(avId, None)
        return Task.done

    def sendClearMovie(self, avId=0, task=None):
        self.ignore(self.air.getAvatarExitEvent(avId))
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
        self.sendClearMovie(avId, None)
        return

    def setInventory(self, blob, newMoney, done, laff):
        avId = self.air.getAvatarIdFromSender()

        if avId in self.air.doId2do:
            av = self.air.doId2do[avId]
            newInventory = av.inventory.makeFromNetString(blob)
            currentMoney = av.getMoney()
            if laff:
                av.toonUp(av.getMaxHp())
            if av.inventory.validatePurchase(newInventory, currentMoney, newMoney):
                # wontfix: due to removing the constantly updating currentMoney here,
                # disconnecting while buying gags won't charge the toon. this is to prevent
                # spamming archipelago with changing jellybeans by 1 repeatedly.
                if done:
                    av.d_setInventory(av.inventory.makeNetString())
                    av.takeMoney(currentMoney - newMoney)
            else:
                self.air.writeServerEvent('suspicious', avId, 'DistributedNPCClerkAI.setInventory invalid purchase')
                self.notify.warning('Avatar ' + str(avId) + ' attempted an invalid purchase.')
                av.d_setInventory(av.inventory.makeNetString())
                av.d_setMoney(av.getMoney())

        if done:
            self.completePurchase(avId)

    def __handleUnexpectedExit(self, avId):
        self.notify.warning('avatar:' + str(avId) + ' has exited unexpectedly')
        self.sendTimeoutMovie(avId, None)
        return
