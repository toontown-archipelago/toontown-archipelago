from typing import Dict, List

from apworld.toontown.locations import LOCATION_ID_TO_NAME
from . import ShtikerPage
import random
from apworld.toontown import ToontownItemName, ToontownItemDefinition, get_item_def_from_id
from toontown.toonbase import TTLocalizer
from direct.gui.DirectGui import *
from panda3d.core import *

from ..archipelago.util.HintContainer import HintContainer, HintedItem
from ..archipelago.util.archipelago_information import ArchipelagoInformation
from ..archipelago.util.global_text_properties import get_raw_formatted_string, MinimalJsonMessagePart
from ..util.ui import make_dsl_scrollable


class HintNode(DirectFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.title = DirectLabel(parent=self, scale=0.07, pos=(0, 0, -0.08), text="Select an Item", textMayChange=True, relief=None)
        self.scrollList = None

        gui = loader.loadModel('phase_3/models/gui/pick_a_toon_gui')
        quitHover = gui.find('**/QuitBtn_UP')

        self.hintButton = DirectButton(
            text=('Give me a hint', 'Give me a hint', 'Give me a hint', 'Select an Item'),
            command=self.askForHint,
            text_scale=0.05,
            parent=self,
            pos=(0, 0, -0.16),
            relief=None,
            image=(quitHover, quitHover, quitHover),
            image_scale=0.85,
            text_pos=(0, -0.015),
        )
        self.hintButton['state'] = DGG.DISABLED

        self.hintName = None
        self.hintNodes = []

        gui.removeNode()

    def askForHint(self):
        if self.hintName is None:
            base.talkAssistant.sendOpenTalk("!hint")
            return
        base.talkAssistant.sendOpenTalk("!hint " + self.hintName.value)

    def getHintContainer(self) -> HintContainer:
        return base.localAvatar.getHintContainer()

    def __createHintDisplay(self, text, icon, yOffset) -> DirectLabel:
        return DirectLabel(
            parent=self, relief=None, image=icon, image_scale=(1.25, 1.25, 1.25),
            pos=(0, 0, 0), text=text, text_scale=0.032,
            text_align=TextNode.ALeft, text_pos=(0.03, -0.0125), text_fg=Vec4(0, 0, 0, 1),
            text_wordwrap=24
        )

    def updateHintDisplays(self, checkDef, checkMax):
        # Clear the old hint lines
        for h in self.hintNodes:
            h.destroy()
        self.hintNodes.clear()

        self.title["text"] = checkDef.name.value

        # If the archipelago manager is not defined we cannot continue
        if base.cr.archipelagoManager is None:
            return

        localToonInformation: ArchipelagoInformation = base.cr.archipelagoManager.getLocalInformation()
        if localToonInformation is None:
            return

        model = loader.loadModel('phase_4/models/parties/schtickerbookHostingGUI')
        checkIcon = model.find('**/checkmark')
        xIcon = model.find('**/x')
        questionMarkIcon = model.find('**/questionMark')

        hintContainer: HintContainer = self.getHintContainer()
        hints: List[HintedItem] = hintContainer.getHintsForItemAndSlot(checkDef.unique_id, localToonInformation.slotId)

        # Using our hints we have so far, start constructing text to show that
        foundHints = []
        lostHints = []
        notHinted = []
        for labelIndex in range(checkMax):

            # If we do not have a hint for this, set defaults
            if labelIndex >= len(hints):
                text = random.choice(["Where is it?", "Looking for me?", "Has to be somewhere...", "Got Hints? TM", "Wasted your hint points, didn't you?",
                                      "Recover me from the Cogs!", "A check has fallen into the river in Lego City!", "Find me, I dare you.", "Hope this wasn't in sphere 1.",
                                      "This one is going to be on the D Office, watch.", "*Crickets chirping*", "Check the tracker.", "Can you find it?"])
                node = self.__createHintDisplay(text, xIcon, labelIndex)
                notHinted.append(node)
                continue

            # We have a hint! Set up the text to tell the player where it is
            hint: HintedItem = hints[labelIndex]
            text = get_raw_formatted_string([
                MinimalJsonMessagePart(hint.player_name, color='magenta'),
                MinimalJsonMessagePart('\'s ', color='black'),
                MinimalJsonMessagePart(hint.location_name, color='green'),
            ])
            icon = checkIcon if hint.found else questionMarkIcon
            node = self.__createHintDisplay(text, icon, labelIndex)
            if hint.found:
                foundHints.append(node)
            else:
                lostHints.append(node)
        self.hintNodes = foundHints + lostHints + notHinted

        self.regenScrollList()

        # If we know where everything is, allow refreshing to check status
        if len(hints) >= checkMax:
            self.hintButton['text'] = "Refresh hints?"
        else:
            self.hintButton['text'] = "Give me a hint"
        self.hintButton['state'] = DGG.NORMAL

        model.removeNode()

    def regenScrollList(self):
        if self.scrollList:
            self.scrollList.hide()
            self.scrollList.destroy()
            self.scrollList = None

        self.gui = loader.loadModel('phase_3.5/models/gui/friendslist_gui')
        self.listXorigin = 0.02
        self.listFrameSizeX = 0.75
        self.listZorigin = -0.765
        self.listFrameSizeZ = 0.8
        self.arrowButtonScale = 1
        self.itemFrameXorigin = -0.237
        self.itemFrameZorigin = 0.32
        self.buttonXstart = self.itemFrameXorigin + 0.318
        self.scrollList = DirectScrolledList(
            parent=self, relief=None, pos=(-0.09, 0, -0.65),
            incButton_image=(self.gui.find('**/FndsLst_ScrollUp'),
                             self.gui.find('**/FndsLst_ScrollDN'),
                             self.gui.find('**/FndsLst_ScrollUp_Rllvr'),
                             self.gui.find('**/FndsLst_ScrollUp')), incButton_relief=None,
            incButton_scale=(self.arrowButtonScale * 1.5, self.arrowButtonScale, -self.arrowButtonScale),
            incButton_pos=(self.buttonXstart, 0, self.itemFrameZorigin - 0.79),
            incButton_image3_color=Vec4(1, 1, 1, 0.2), decButton_image=(self.gui.find('**/FndsLst_ScrollUp'),
                                                                        self.gui.find('**/FndsLst_ScrollDN'),
                                                                        self.gui.find('**/FndsLst_ScrollUp_Rllvr'),
                                                                        self.gui.find('**/FndsLst_ScrollUp')),
            decButton_relief=None,
            decButton_scale=(self.arrowButtonScale * 1.5, self.arrowButtonScale, self.arrowButtonScale),
            decButton_pos=(self.buttonXstart, 0, self.itemFrameZorigin + 0.07),
            decButton_image3_color=Vec4(1, 1, 1, 0.2), itemFrame_pos=(self.itemFrameXorigin, 0, self.itemFrameZorigin),
            itemFrame_scale=1.0, itemFrame_relief=DGG.SUNKEN, itemFrame_frameSize=(self.listXorigin,
                                                                                   self.listXorigin + self.listFrameSizeX,
                                                                                   self.listZorigin,
                                                                                   self.listZorigin + self.listFrameSizeZ),
            itemFrame_frameColor=(0.85, 0.95, 1, 1),
            itemFrame_borderWidth=(0.01, 0.01), numItemsVisible=13, forceHeight=0.06, items=self.hintNodes
        )
        make_dsl_scrollable(self.scrollList)


    def __createDefaultDisplay(self, text, yOffset) -> DirectLabel:
        return DirectLabel(
            parent=self, relief=None, image_scale=(1.25, 1.25, 1.25),
            pos=(-0.36, 0, -0.25 - 0.05 * yOffset), text=text, text_scale=0.032,
            text_align=TextNode.ALeft, text_pos=(0.03, -0.0125), text_fg=Vec4(0, 0, 0, 1),
            text_wordwrap=24
        )

    def showDefaultDisplay(self):
        # Clear the old lines (needed for re-entering the page)
        for h in self.hintNodes:
            h.destroy()
        self.hintNodes.clear()
        self.hintName = None

        label = "Select an item to view hints for it."
        self.title["text"] = 'Select an Item'
        self.hintButton["text"] = 'Refresh Hints?'
        self.hintButton['state'] = DGG.NORMAL
        defaultNode = self.__createDefaultDisplay(label, 0)
        self.hintNodes.append(defaultNode)
        self.regenScrollList()


class CheckPage(ShtikerPage.ShtikerPage):

    def __init__(self):
        ShtikerPage.ShtikerPage.__init__(self)
        self.scrollList = None
        self.hintPointsTitle = None
        self.textRolloverColor = Vec4(1, 1, 0, 1)
        self.textDownColor = Vec4(0.5, 0.9, 1, 1)
        self.textDisabledColor = Vec4(0.4, 0.8, 0.4, 1)
        self.checkButtons = []
        self.hintNode = HintNode(self)
        self.hintNode.setPos(0.42, 0, 0.5)
        self.hintNode.hide()
        self.viewingHint: bool | tuple = False

    def load(self):
        main_text_scale = 0.06
        title_text_scale = 0.12
        self.title = DirectLabel(parent=self, relief=None, text=TTLocalizer.CheckPageTitle, text_scale=title_text_scale, textMayChange=0, pos=(0, 0, 0.6))
        #helpText_ycoord = 0.403
        #self.helpText = DirectLabel(parent=self, relief=None, text='', text_scale=main_text_scale, text_wordwrap=12, text_align=TextNode.ALeft, textMayChange=1, pos=(0.058, 0, helpText_ycoord))
        self.gui = loader.loadModel('phase_3.5/models/gui/friendslist_gui')
        self.listXorigin = 0.02
        self.listFrameSizeX = 0.7
        self.listZorigin = -0.96
        self.listFrameSizeZ = 1.04
        self.arrowButtonScale = 1.3
        self.itemFrameXorigin = -0.237
        self.itemFrameZorigin = 0.365
        self.buttonXstart = self.itemFrameXorigin + 0.425
        self.regenerateScrollList()
        self.hintPointsTitle = DirectFrame(parent=self, text=TTLocalizer.HintPointsTitle % (0, 0),
                                            text_scale=main_text_scale, text_align=TextNode.ACenter, relief=None,
                                            pos=(0, 0, 0.525))
        scrollTitle = DirectFrame(parent=self.scrollList, text=TTLocalizer.ShardPageScrollTitle, text_scale=main_text_scale, text_align=TextNode.ACenter, relief=None, pos=(self.buttonXstart, 0, self.itemFrameZorigin + 0.127))

        return

    def enter(self):
        ShtikerPage.ShtikerPage.enter(self)
        # Request our hints
        base.cr.archipelagoManager.d_requestHints()
        self.regenerateScrollList()
        base.localAvatar.sendUpdate('requestHintPoints')

        self.hintNode.show()
        self.hintNode.showDefaultDisplay()

        self.accept('archipelago-hints-updated', self.__handleHintsUpdated)
        self.viewingHint = False

    def exit(self):
        super().exit()
        self.ignore('archipelago-hints-updated')
        self.viewingHint = False

    def __handleHintsUpdated(self, _=None):
        self.regenerateScrollList()

    def regenerateScrollList(self):
        selectedIndex = 0
        if self.scrollList:
            selectedIndex = self.scrollList.getSelectedIndex()
            self.updateCheckButtons()
            self.scrollList.destroy()
            self.scrollList = None

        hostUi = loader.loadModel('phase_4/models/parties/schtickerbookHostingGUI')
        checkmarkGeom = hostUi.find('**/checkmark')
        self.scrollList = DirectScrolledList(
            parent=self, relief=None, pos=(-0.625, 0, 0),
            # scale=0.75,
            incButton_image=(self.gui.find('**/FndsLst_ScrollUp'),
            self.gui.find('**/FndsLst_ScrollDN'),
            self.gui.find('**/FndsLst_ScrollUp_Rllvr'),
            self.gui.find('**/FndsLst_ScrollUp')), incButton_relief=None,
            incButton_scale=(self.arrowButtonScale * 1.5, self.arrowButtonScale, -self.arrowButtonScale),
            incButton_pos=(self.buttonXstart, 0, self.itemFrameZorigin - 0.999),
            incButton_image3_color=Vec4(1, 1, 1, 0.2), decButton_image=(self.gui.find('**/FndsLst_ScrollUp'),
            self.gui.find('**/FndsLst_ScrollDN'),
            self.gui.find('**/FndsLst_ScrollUp_Rllvr'),
            self.gui.find('**/FndsLst_ScrollUp')), decButton_relief=None,
            decButton_scale=(self.arrowButtonScale * 1.5, self.arrowButtonScale, self.arrowButtonScale),
            decButton_pos=(self.buttonXstart, 0, self.itemFrameZorigin + 0.125),
            decButton_image3_color=Vec4(1, 1, 1, 0.2), itemFrame_pos=(self.itemFrameXorigin, 0, self.itemFrameZorigin),
            itemFrame_scale=1.0, itemFrame_relief=DGG.SUNKEN, itemFrame_frameSize=(self.listXorigin,
            self.listXorigin + self.listFrameSizeX,
            self.listZorigin,
            self.listZorigin + self.listFrameSizeZ), itemFrame_frameColor=(0.85, 0.95, 1, 1),
            itemFrame_borderWidth=(0.01, 0.01), numItemsVisible=15, forceHeight=0.065, items=self.checkButtons
        )
        make_dsl_scrollable(self.scrollList)
        self.scrollList.scrollTo(selectedIndex)

        # If we were viewing a hint, force the button command to execute as if we clicked it to refresh the page
        if self.viewingHint and isinstance(self.viewingHint, tuple):
            self.setHint(*self.viewingHint)

        return

    def updateHintPointText(self):
        self.hintPointsTitle['text'] = TTLocalizer.HintPointsTitle % (base.localAvatar.hintPoints, base.localAvatar.hintCost)

    def updateCheckButtons(self):
        # Cleanup buttons
        for button in self.checkButtons:
            button.detachNode()
            del button
        self.checkButtons = []

        # Maps item ids to the quantity that we have
        itemsAndCount: Dict[int, int] = {}
        for item in base.localAvatar.getReceivedItems():
            index_received, item_id = item
            itemsAndCount[item_id] = itemsAndCount.get(item_id, 0) + 1

        # Count total items in item pool
        allItems: dict[ToontownItemDefinition, int] = {}
        for item_id in sorted(base.localAvatar.slotData.get("local_itempool", [])):
            allItems.setdefault(item_id, 0)
            allItems[item_id] += 1

        # Container Lists for Item Classes
        bounties = []
        keyItems = []
        progressionItems = []
        usefulItems = []
        junkItems = []
        # Generate new buttons
        model = loader.loadModel('phase_4/models/parties/schtickerbookHostingGUI')
        for item_id, quantity in allItems.items():
            itemDef = get_item_def_from_id(item_id)
            if itemDef is None:
                print("ALERT I DON'T KNOW WHAT %s IS -- ENRAGE AT MICA" % item_id)
                continue
            itemName = itemDef.name.value
            if itemName.startswith("Defeated "):
                continue 
            playgroundKeys = [ToontownItemName.TTC_ACCESS.value, ToontownItemName.DD_ACCESS.value,
                              ToontownItemName.DG_ACCESS.value,  ToontownItemName.MML_ACCESS.value,
                              ToontownItemName.TB_ACCESS.value,  ToontownItemName.DDL_ACCESS.value]
            button = self._makeCheckButton(model, itemDef, itemsAndCount.get(itemDef.unique_id, 0), quantity)
            if itemName in playgroundKeys:
                quantity = 2
            if itemName == "Bounty":
                bounties.append(button[0])
                continue
            if "Key" in itemName or "Disguise" in itemName:
                if "Access" in itemName:
                    progressionItems.append(button[0])
                    continue
                keyItems.append(button[0])
                continue
            if itemDef.classification == 0b0001:  # Progression Items
                if button[0] not in (progressionItems + keyItems):  # Make sure item isn't already in one of these
                    progressionItems.append(button[0])
            elif itemDef.classification == 0b0010:  # Useful Items
                usefulItems.append(button[0])
            else:
                junkItems.append(button[0])
        model.removeNode()
        del model
        self.checkButtons = bounties + keyItems + progressionItems + usefulItems + junkItems

    def _makeCheckButton(self, model, itemDef, checkCount, checkMax):
        """
        model: loader.loadModel(loader.loadModel('phase_4/models/parties/schtickerbookHostingGUI') # avoiding loading this many times.
        """
        checkName = itemDef.name
        command = lambda: self.setHint(checkName, itemDef, checkMax)
        checkButtonParent = DirectFrame()
        checkButtonL = DirectButton(parent=checkButtonParent, relief=None, text=checkName.value, text_pos=(0.04, 0), text_scale=0.051, text_align=TextNode.ALeft, text1_bg=self.textDownColor, text2_bg=self.textRolloverColor, text3_fg=self.textDisabledColor, textMayChange=0, command=command)
        check = model.find('**/checkmark')
        x = model.find('**/x')
        hinted = model.find('**/questionMark')

        # Check if this item has been hinted safely
        isHinted = False
        if base.cr.archipelagoManager is not None and (localToonInformation := base.cr.archipelagoManager.getLocalInformation()) is not None:
            isHinted = any(hint.found for hint in base.localAvatar.getHintContainer().getHintsForItemAndSlot(itemDef.unique_id, localToonInformation.slotId))
        if checkCount >= checkMax:
            geomToUse = check
        elif isHinted:
            geomToUse = hinted
        else:
            geomToUse = x
        checkButtonR = DirectButton(parent=checkButtonParent, relief=None, image=geomToUse, image_scale=(1.25, 1.25, 1.25), pos=(0.75, 0, 0.0125), text=str(checkCount) + '/' + str(checkMax), text_scale=0.06, text_align=TextNode.ARight, text_pos=(-0.03, -0.0125), text_fg=Vec4(0, 0, 0, 0), text1_fg=Vec4(0, 0, 0, 0), text2_fg=Vec4(0, 0, 0, 1), text3_fg=Vec4(0, 0, 0, 0), command=command, text_wordwrap=13)
        # checkButtonR.bind(DirectGuiGlobals.ENTER, lambda t: self.setHint(checkName, itemDef, checkMax, hintLocations))
        # checkButtonR.bind(DirectGuiGlobals.EXIT, lambda t: self.clearHintIf(checkName))
        del check
        del hinted
        del x
        return (checkButtonParent, checkButtonR, checkButtonL)

    def setHint(self, checkName, checkDef, checkMax):
        self.viewingHint = (checkName, checkDef, checkMax)
        self.hintNode.hintName = checkName
        self.hintNode.hintButton['state'] = DGG.NORMAL
        self.hintNode.show()
        self.hintNode.updateHintDisplays(checkDef, checkMax)
