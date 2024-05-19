from typing import Dict

from direct.interval.FunctionInterval import Wait, Func
from direct.interval.LerpInterval import LerpScaleInterval
from direct.interval.MetaInterval import Parallel, Sequence
from direct.interval.SoundInterval import SoundInterval

from .PurchaseBase import *
from toontown.toonbase import ToontownTimer, ToontownBattleGlobals

COUNT_UP_RATE = 0.15
DELAY_BEFORE_COUNT_UP = 1.25
DELAY_AFTER_COUNT_UP = 1.75
COUNT_DOWN_RATE = 0.075
DELAY_AFTER_COUNT_DOWN = 0.0
DELAY_AFTER_CELEBRATE = 3.0

class ClerkPurchase(PurchaseBase):
    activateMode = 'storePurchase'

    def __init__(self, toon, remain, doneEvent):
        PurchaseBase.__init__(self, toon, doneEvent)
        self.remain = remain

    def load(self):
        purchaseModels = loader.loadModel('phase_4/models/gui/gag_shop_purchase_gui')
        PurchaseBase.load(self, purchaseModels)
        self.backToPlayground = DirectButton(parent=self.frame, relief=None, scale=1.04, pos=(0.71, 0, -0.045), image=(purchaseModels.find('**/PurchScrn_BTN_UP'), purchaseModels.find('**/PurchScrn_BTN_DN'), purchaseModels.find('**/PurchScrn_BTN_RLVR')), text=TTLocalizer.GagShopDoneShopping, text_fg=(0, 0.1, 0.7, 1), text_scale=0.05, text_pos=(0, 0.015, 0), command=self.__handleBackToPlayground)
        self.fastRestockButton = DirectButton(parent=self.frame, relief=None, scale=.80, pos=(-0.55, 0, -0.26), image=(purchaseModels.find('**/PurchScrn_BTN_UP'), purchaseModels.find('**/PurchScrn_BTN_DN'), purchaseModels.find('**/PurchScrn_BTN_RLVR')), text=TTLocalizer.GagShopFastRestock, text_fg=(0, 0.1, 0.7, 1), text_scale=0.06, text_pos=(0, 0.015, 0), command=self.__handleFastRestock)
        self.timer = ToontownTimer.ToontownTimer()
        self.timer.reparentTo(self.frame)
        self.timer.posInTopRightCorner()
        purchaseModels.removeNode()
        return

    def unload(self):
        self.timer.destroy()
        PurchaseBase.unload(self)
        del self.backToPlayground
        del self.fastRestockButton
        del self.timer

    def __handleBackToPlayground(self):
        self.toon.inventory.reparentTo(hidden)
        self.toon.inventory.hide()
        self.handleDone(0)

    def __timerExpired(self):
        self.handleDone(0)

    def __getPropCounts(self) -> Dict[tuple, int]:
        counts = {}
        for track in range(len(ToontownBattleGlobals.Tracks)):
            for level in range(ToontownBattleGlobals.LAST_REGULAR_GAG_LEVEL):
                counts[(track, level)] = self.toon.inventory.numItem(track, level)
        return counts

    def __calculateRestockCost(self, oldGags: Dict[tuple, int], newGags: Dict[tuple, int]) -> int:

        # Loop through the old gags and remove any counts we have from the new gags since we already 'had them'
        for gag, count in oldGags.items():

            # If this gag is not in our new inventory, assume it was deleted and do nothing
            if gag not in newGags:
                continue

            # Decrement the amount we had for the new gags
            newGags[gag] -= count

        # Make sure nothing went below zero
        for gag, count in newGags.items():
            if count < 0:
                newGags[gag] = 0

        # See how many gags are new
        return sum(newGags.values())

    def __handleFastRestock(self):
        # First, get the old gags we had for cost calculation purposes and reset the inventory
        oldGags = self.__getPropCounts()
        self.toon.inventory.clearInventory()
        self.toon.inventory.updateGUI()  # We update the GUI here to reflect that we have 0 gags for our animation.

        # Now max out our inventory with default settings (Balanced fill, no clearing etc)
        self.toon.inventory.maxInventory()
        newGags = self.__getPropCounts()
        gagCost = self.__calculateRestockCost(oldGags, newGags)

        # add the cost of getting laff back
        laffCost = (self.toon.getMaxHp() - self.toon.getHp())
        cost = laffCost + gagCost

        # If we didn't do anything
        if cost <= 0:
            self.toon.inventory.updateGUI()
            return

        # If we can't afford this revert back to the old inventory and cancel
        if self.toon.getMoney() < cost:
            self.toon.inventory.clearInventory()
            for gag, count in oldGags.items():
                track, level = gag
                self.toon.inventory.setItem(track, level, count)
            self.toon.inventory.updateGUI()
            return

        # It is now safe to animate the gags being fast restocked!

        # We put the sfx in a method here so it sounds cleaner to be played properly, not sure if better way to do this
        def doTickSfx():
            tickSfx = base.loader.loadSfx('phase_3.5/audio/sfx/tick_counter.ogg')
            base.playSfx(tickSfx)

        # Callback method for when the animation is finished. Set our money, update the GUI and send this purchase out
        def callback():
            self.toon.setMoney(self.toon.getMoney() - cost)
            self.toon.inventory.updateGUI()
            messenger.send('boughtGagFast')


        popoutIval = Parallel()
        delay = 0
        # we only need to do this if we're getting gags
        if gagCost:
            for level in range(ToontownBattleGlobals.LAST_REGULAR_GAG_LEVEL+1):
                thisLevelSeq = Parallel()
                thisLevelSeq.append(Func(doTickSfx))
                numItemsTrack = 0
                for track in range(len(ToontownBattleGlobals.Tracks)):
                    numGags = self.toon.inventory.numItem(track, level)
                    numItemsTrack += numGags
                    button = self.toon.inventory.buttons[track][level]

                    if numGags > 0:
                        thisLevelSeq.append(Parallel(
                            LerpScaleInterval(button, startScale=1.0, scale=1+(numGags*.05), duration=.07),
                            Func(self.toon.inventory.updateGUI, track, level),
                            LerpScaleInterval(button, startScale=1+(numGags*.05), scale=1.0, duration=.07),
                        ))

                if numItemsTrack > 0:
                    popoutIval.append(Sequence(Wait(delay), thisLevelSeq))
                    delay += .05

        popoutIval.append(Sequence(Wait(delay), Func(callback)))
        popoutIval.start()

    def enterPurchase(self):
        PurchaseBase.enterPurchase(self)
        self.backToPlayground.reparentTo(self.toon.inventory.storePurchaseFrame)
        self.fastRestockButton.reparentTo(self.toon.inventory.storePurchaseFrame)
        self.pointDisplay.reparentTo(self.toon.inventory.storePurchaseFrame)
        self.statusLabel.reparentTo(self.toon.inventory.storePurchaseFrame)
        self.toon.inventory.deleteEnterButton.setPos(-0.75, 0, -0.89)
        self.timer.countdown(self.remain, self.__timerExpired)

    def exitPurchase(self):
        PurchaseBase.exitPurchase(self)
        self.backToPlayground.reparentTo(self.frame)
        self.fastRestockButton.reparentTo(self.frame)
        self.pointDisplay.reparentTo(self.frame)
        self.statusLabel.reparentTo(self.frame)
        self.ignore('purchaseStateChange')
