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
        if hasattr(base, 'ttAccess') and base.ttAccess and base.ttAccess.canAccess():
            return True
        return False

    def handleOkTeaser(self):
        self.dialog.destroy()
        del self.dialog
        place = base.cr.playGame.getPlace()
        if place:
            place.fsm.request('walk')

    def handleCollisionSphereEnter(self, collEntry):
        base.cr.playGame.getPlace().fsm.request('purchase')
        self.sendUpdate('avatarEnter', [])
        self.setBusyWithLocalToon(True)

    def __handleUnexpectedExit(self):
        self.notify.warning('unexpected exit')
        return

    def resetClerk(self):
        self.ignoreAll()
        taskMgr.remove(self.uniqueName('popupPurchaseGUI'))
        if self.cameraLerp:
            self.cameraLerp.finish()
            self.cameraLerp = None
        if self.purchase:
            self.purchase.exit()
            self.purchase.unload()
            self.purchase = None
        self.clearMat()
        self.startLookAround()
        self.detectAvatars()
        if self.isBusyWithLocalToon():
            self.freeAvatar()

        self.initToonState()
        self.setBusyWithLocalToon(False)
        return Task.done

    def setMovie(self, mode, npcId, avId, timestamp):
        timeStamp = ClockDelta.globalClockDelta.localElapsedTime(timestamp)
        isLocalToon = avId == base.localAvatar.doId

        # Under no circumstances, if this movie was sent from someone else and we are currently busy with this NPC stop
        if self.isBusyWithLocalToon() and not isLocalToon:
            return

        self.remain = NPCToons.CLERK_COUNTDOWN_TIME - timeStamp

        if mode == NPCToons.PURCHASE_MOVIE_CLEAR:
            return
        if mode == NPCToons.PURCHASE_MOVIE_TIMEOUT:
            taskMgr.remove(self.uniqueName('popupPurchaseGUI'))
            if self.cameraLerp:
                self.cameraLerp.finish()
                self.cameraLerp = None
            if isLocalToon:
                self.ignore(self.purchaseDoneEvent)
            if self.purchase:
                self.__handlePurchaseDone()
            self.setChatAbsolute(TTLocalizer.STOREOWNER_TOOKTOOLONG, CFSpeech | CFTimeout)
            self.resetClerk()
        elif mode == NPCToons.PURCHASE_MOVIE_START:
            av = base.cr.doId2do.get(avId)
            if av is None:
                self.notify.warning('Avatar %d not found in doId' % avId)
                return
            else:
                self.accept(av.uniqueName('disable'), self.__handleUnexpectedExit)
            self.setupAvatars(av)
            if isLocalToon:
                camera.wrtReparentTo(render)
                self.cameraLerp = LerpPosQuatInterval(camera, 1, Point3(-5, 9, self.getHeight() - 0.5), Point3(-150, -2, 0), other=self, blendType='easeOut', name=self.uniqueName('lerpCamera'))
                self.cameraLerp.start()
            self.setChatAbsolute(TTLocalizer.STOREOWNER_GREETING, CFSpeech | CFTimeout)
            if isLocalToon:
                taskMgr.doMethodLater(1.0, self.popupPurchaseGUI, self.uniqueName('popupPurchaseGUI'))
        elif mode == NPCToons.PURCHASE_MOVIE_COMPLETE:
            self.setChatAbsolute(TTLocalizer.STOREOWNER_GOODBYE, CFSpeech | CFTimeout)
            self.resetClerk()
        elif mode == NPCToons.PURCHASE_MOVIE_NO_MONEY:
            self.setChatAbsolute(TTLocalizer.STOREOWNER_NEEDJELLYBEANS, CFSpeech | CFTimeout)
            self.resetClerk()
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
        return

    def d_setInventory(self, invString, money, done):
        self.sendUpdate('setInventory', [invString, money, done])
