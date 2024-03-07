from panda3d.core import *
from direct.interval.IntervalGlobal import *
from .DistributedNPCToonBase import *
from toontown.minigame import ClerkPurchase
from toontown.shtiker.PurchaseManagerConstants import *
from . import NPCToons
from direct.task.Task import Task
from toontown.toonbase import TTLocalizer
from toontown.hood import ZoneUtil
from toontown.toontowngui import TeaserPanel

class DistributedNPCClerk(DistributedNPCToonBase):

    def __init__(self, cr):
        DistributedNPCToonBase.__init__(self, cr)
        self.purchase = None
        self.isLocalToon = False
        self.av = None
        self.purchaseDoneEvent = 'purchaseDone'
        self.cameraLerp = None
        return

    def disable(self):
        self.ignoreAll()
        taskMgr.remove(self.uniqueName('popupPurchaseGUI'))
        if self.cameraLerp:
            self.cameraLerp.finish()
            self.cameraLerp = None
        if self.purchase:
            self.purchase.exit()
            self.purchase.unload()
            self.purchase = None
        self.av = None
        base.localAvatar.posCamera(0, 0)
        DistributedNPCToonBase.disable(self)
        return

    def initToonState(self):
        self.setAnimState('neutral', 0.9, None, None)
        npcOrigin = render.find('**/npc_origin_' + repr((self.posIndex)))
        if not npcOrigin.isEmpty():
            self.reparentTo(npcOrigin)
            self.initPos()
        else:
            self.reparentTo(render)
            self.initPos()
            zonePosDict = {ToontownGlobals.SellbotHQ: (2, -164, -19.594, -180, 'cc'),
                           ToontownGlobals.CashbotHQ: (62, 128, -23.439, -135, 'sc'),
                           ToontownGlobals.LawbotHQ: (90, -366, -68.367, 0, 'bf'),
                           ToontownGlobals.BossbotHQ: (75, 120, 0, 145, 'f')}
            posData = zonePosDict.get(self.zoneId)
            self.setPos(posData[0], posData[1], posData[2])
            self.setH(posData[3])
            self.putOnSuit(posData[4])
        return

    def allowedToEnter(self):
        return True

    def handleOkTeaser(self):
        self.dialog.destroy()
        del self.dialog
        place = base.cr.playGame.getPlace()
        if place:
            place.fsm.request('walk')

    def handleCollisionSphereEnter(self, collEntry):
        base.cr.playGame.getPlace().fsm.request('purchase')
        self.sendUpdate('avatarEnter', [])

    def __handleUnexpectedExit(self):
        self.notify.warning('unexpected exit')
        self.av = None
        return

    def cleanupPurchase(self):

        if not self.isLocalToon:
            return

        self.isLocalToon = False
        self.freeAvatar()
        taskMgr.remove(self.uniqueName('popupPurchaseGUI'))
        if self.cameraLerp:
            self.cameraLerp.finish()
            self.cameraLerp = None
        if self.purchase:
            self.purchase.exit()
            self.purchase.unload()
            self.purchase = None

    def resetClerk(self):

        self.initToonState()

        if not self.isLocalToon:
            return Task.done

        self.cleanupPurchase()
        self.ignoreAll()
        self.clearMat()
        self.startLookAround()
        self.detectAvatars()

        return Task.done

    def setMovie(self, mode, npcId, avId, timestamp):
        timeStamp = ClockDelta.globalClockDelta.localElapsedTime(timestamp)
        self.remain = NPCToons.CLERK_COUNTDOWN_TIME - timeStamp

        isLocal = avId == base.localAvatar.doId

        if mode == NPCToons.PURCHASE_MOVIE_CLEAR:
            return

        if mode == NPCToons.PURCHASE_MOVIE_TIMEOUT:

            self.setChatAbsolute(TTLocalizer.STOREOWNER_TOOKTOOLONG, CFSpeech | CFTimeout)

            if not isLocal:
                return

            self.freeAvatar()
            taskMgr.remove(self.uniqueName('popupPurchaseGUI'))
            self.ignore(self.purchaseDoneEvent)
            if self.purchase:
                self.__handlePurchaseDone()

        elif mode == NPCToons.PURCHASE_MOVIE_START:
            self.av = base.cr.doId2do.get(avId)
            if self.av is None:
                self.notify.warning('Avatar %d not found in doId' % avId)
                return
            else:
                self.accept(self.av.uniqueName('disable'), self.__handleUnexpectedExit)
            self.setupAvatars(self.av)
            if isLocal:
                camera.wrtReparentTo(render)
                self.cameraLerp = LerpPosQuatInterval(camera, 1, Point3(-5, 9, self.getHeight() - 0.5), Point3(-150, -2, 0), other=self, blendType='easeOut', name=self.uniqueName('lerpCamera'))
                self.cameraLerp.start()
            self.setChatAbsolute(TTLocalizer.STOREOWNER_GREETING, CFSpeech | CFTimeout)
            if isLocal:
                taskMgr.doMethodLater(1.0, self.popupPurchaseGUI, self.uniqueName('popupPurchaseGUI'))
        elif mode == NPCToons.PURCHASE_MOVIE_COMPLETE:
            self.setChatAbsolute(TTLocalizer.STOREOWNER_GOODBYE, CFSpeech | CFTimeout)

            if isLocal:
                self.cleanupPurchase()
                self.initToonState()
                self.freeAvatar()

        elif mode == NPCToons.PURCHASE_MOVIE_NO_MONEY:
            self.setChatAbsolute(TTLocalizer.STOREOWNER_NEEDJELLYBEANS, CFSpeech | CFTimeout)
        return

    def popupPurchaseGUI(self, task):
        self.setChatAbsolute('', CFSpeech)
        self.acceptOnce(self.purchaseDoneEvent, self.__handlePurchaseDone)
        self.accept('boughtGag', self.__handleBoughtGag)
        self.purchase = ClerkPurchase.ClerkPurchase(base.localAvatar, self.remain, self.purchaseDoneEvent)
        self.purchase.load()
        self.purchase.enter()
        return Task.done

    def __handleBoughtGag(self):
        self.d_setInventory(base.localAvatar.inventory.makeNetString(), base.localAvatar.getMoney(), 0)

    def __handlePurchaseDone(self):
        self.ignore('boughtGag')
        self.d_setInventory(base.localAvatar.inventory.makeNetString(), base.localAvatar.getMoney(), 1)
        self.purchase.exit()
        self.purchase.unload()
        self.purchase = None
        self.cleanupPurchase()
        return

    def d_setInventory(self, invString, money, done):
        self.sendUpdate('setInventory', [invString, money, done])
