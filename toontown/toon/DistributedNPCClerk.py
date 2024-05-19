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

# Hardcoded positioning that maps zone IDs to NPC positions.
# When modifying positions of clerks on the street, the zone ID must match the position's
# zone ID on the street. This also needs to be reflected in the NPCToons dict and HoodDataAI
# For the respective Hood. Very annoying i know sobbing
MISSING_ORIGIN_ZONE_POSITION_FALLBACK = {
    ToontownGlobals.SellbotHQ: (2, -164, -19.594, -180),
    ToontownGlobals.CashbotHQ: (62, 128, -23.439, -135),
    ToontownGlobals.LawbotHQ: (90, -366, -68.367, 0),
    ToontownGlobals.BossbotHQ: (75, 120, 0, 145),

    # Begin hacky street NPC positioning. As a reminder, if you modify any of these either:
    # - Be sure that the position is in the same zone.
    # - Change the zone to match the new position in: HERE, NPC dict and HoodDataAI

    # Silly Street, Loopy Lane, Punchline Place
    2114: (-68.941,  -346.560,  0.025, -30),
    2218: (-367.476,  70.804,  0.025, -150),
    2326: (507.170,  139.359,  0.025, 150),

    # Barnacle Blvd., Seaweed Street, Lighthouse Lane
    1128: (355.628,  75.177,  0.025, 60),
    1218: (-49.409,  -400.088,  0.025, -30),
    1309: (185.504,  -190.694,  0.025, -30),

    # Elm Street, Maple Street, Oak Street
    5123: (350.256,  37.952,  0.025, 45),
    5243: (331.984,  149.510,  0.025, -270),
    5320: (-137.707,  30.293,  0.025, -360),

    # Alto Ave., Baritone Blvd., Tenor Terrace
    4115: (-330.216,  -1.400,  0.025, -180),
    4214: (-0.076,  516.400,  0.026, -360),
    4343: (303.573,  166.602,  5.025, -130),

    # Walrus Way, Sleet Street, Polar Place
    3115: (134.511,  38.332,  0.025, -150),
    3235: (241.119,  179.771,  0.050, -50),
    3309: (251.204,  234.028,  4.367, 25),

    # Lullaby Lane, Pajama Place
    9130: (-240.765,  -154.315,  0.026, 290),
    9223: (324.012,  -53.569,  0.025, 15),
}

# If an NPC is in a specific zone, put on a disguise :p
ZONE_TO_DISGUISE = {
    ToontownGlobals.SellbotHQ: 'cc',
    ToontownGlobals.CashbotHQ: 'sc',
    ToontownGlobals.LawbotHQ: 'bf',
    ToontownGlobals.BossbotHQ: 'f',
}


class DistributedNPCClerk(DistributedNPCToonBase):

    def __init__(self, cr):
        DistributedNPCToonBase.__init__(self, cr)
        self.purchase = None
        self.purchaseDoneEvent = 'purchaseDone'
        self.cameraLerp = None
        self.collisionDebounce = False
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

        # Attempt to find a defined origin for us in the scene.
        # NPCs defined in the vanilla game are typically done this way.
        npcOrigin = render.find('**/npc_origin_' + repr((self.posIndex)))
        if not npcOrigin.isEmpty():
            self.reparentTo(npcOrigin)
            self.initPos()
            return

        # This NPC doesn't have a set spot for them, so they are probably
        # Hacked in by us, check for a defined position.
        pos = MISSING_ORIGIN_ZONE_POSITION_FALLBACK.get(self.zoneId)
        # Is there nothing?
        if pos is None:
            self.notify.warning(f'NPC {self.getName()} has no zone position data for {self.zoneId}!')
            return

        # Place them!
        x, y, z, h = pos
        self.reparentTo(render)
        self.initPos()
        self.setPos(x, y, z)
        self.setH(h)

        # Check if we should put on a suit.
        suit = ZONE_TO_DISGUISE.get(self.zoneId)
        if suit is not None:
            self.putOnSuit(suit, True, False, True)

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
        if self.collisionDebounce:
            return
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

        self.collisionDebounce = True
        def resetDebounce(*_):
            self.collisionDebounce = False
        taskMgr.doMethodLater(0.5, resetDebounce, self.uniqueName('collisionDebounce'))

        self.initToonState()
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
        self.accept('boughtGagFast', self.__handleBoughtGagFast)
        self.purchase = ClerkPurchase.ClerkPurchase(base.localAvatar, self.remain, self.purchaseDoneEvent)
        self.purchase.load()
        self.purchase.enter()
        return Task.done

    def __handleBoughtGag(self):
        self.d_setInventory(base.localAvatar.inventory.makeNetString(), base.localAvatar.getMoney(), 0)

    def __handleBoughtGagFast(self):
        self.d_setInventory(base.localAvatar.inventory.makeNetString(), base.localAvatar.getMoney(), 0, laff=1)

    def __handlePurchaseDone(self):
        self.ignore('boughtGag')
        self.ignore('boughtGagFast')
        self.d_setInventory(base.localAvatar.inventory.makeNetString(), base.localAvatar.getMoney(), 1)
        self.purchase.exit()
        self.purchase.unload()
        self.purchase = None
        self.setBusyWithLocalToon(False)
        self.freeAvatar()
        return

    def d_setInventory(self, invString, money, done, laff=0):
        self.sendUpdate('setInventory', [invString, money, done, laff])
