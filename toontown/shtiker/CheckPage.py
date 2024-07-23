from typing import Dict
from . import ShtikerPage
from apworld.toontown import ToontownItemDefinition, get_item_def_from_id
from toontown.toonbase import TTLocalizer
from direct.gui.DirectGui import *
from panda3d.core import *

from ..util.ui import make_dsl_scrollable


class CheckPage(ShtikerPage.ShtikerPage):

    def __init__(self):
        ShtikerPage.ShtikerPage.__init__(self)
        self.scrollList = None
        self.hintPointsTitle = None
        self.textRolloverColor = Vec4(1, 1, 0, 1)
        self.textDownColor = Vec4(0.5, 0.9, 1, 1)
        self.textDisabledColor = Vec4(0.4, 0.8, 0.4, 1)
        self.checkButtons = []

    def load(self):
        main_text_scale = 0.06
        title_text_scale = 0.12
        self.title = DirectLabel(parent=self, relief=None, text=TTLocalizer.CheckPageTitle, text_scale=title_text_scale, textMayChange=0, pos=(0, 0, 0.6))
        #helpText_ycoord = 0.403
        #self.helpText = DirectLabel(parent=self, relief=None, text='', text_scale=main_text_scale, text_wordwrap=12, text_align=TextNode.ALeft, textMayChange=1, pos=(0.058, 0, helpText_ycoord))
        self.gui = loader.loadModel('phase_3.5/models/gui/friendslist_gui')
        self.listXorigin = -0.02
        self.listFrameSizeX = 0.9
        self.listZorigin = -0.96
        self.listFrameSizeZ = 1.04
        self.arrowButtonScale = 1.3
        self.itemFrameXorigin = -0.237
        self.itemFrameZorigin = 0.365
        self.buttonXstart = self.itemFrameXorigin + 0.425
        self.regenerateScrollList()
        self.hintPointsTitle = DirectFrame(parent=self, text=TTLocalizer.HintPointsTitle % 0,
                                            text_scale=main_text_scale, text_align=TextNode.ACenter, relief=None,
                                            pos=(0, 0, 0.525))
        scrollTitle = DirectFrame(parent=self.scrollList, text=TTLocalizer.ShardPageScrollTitle, text_scale=main_text_scale, text_align=TextNode.ACenter, relief=None, pos=(self.buttonXstart, 0, self.itemFrameZorigin + 0.127))
        return

    def enter(self):
        ShtikerPage.ShtikerPage.enter(self)
        self.regenerateScrollList()
        base.localAvatar.sendUpdate('requestHintPoints')

    def regenerateScrollList(self):
        selectedIndex = 0
        if self.scrollList:
            selectedIndex = self.scrollList.getSelectedIndex()
            self.updateCheckButtons()
            self.scrollList.destroy()
            self.scrollList = None

        hostUi = loader.loadModel('phase_4/models/parties/schtickerbookHostingGUI')
        checkmarkGeom = hostUi.find('**/checkmark')
        self.scrollList = DirectScrolledList(parent=self, relief=None, pos=(-0.625, 0, 0), incButton_image=(self.gui.find('**/FndsLst_ScrollUp'),
         self.gui.find('**/FndsLst_ScrollDN'),
         self.gui.find('**/FndsLst_ScrollUp_Rllvr'),
         self.gui.find('**/FndsLst_ScrollUp')), incButton_relief=None, incButton_scale=(self.arrowButtonScale * 1.5, self.arrowButtonScale, -self.arrowButtonScale), incButton_pos=(self.buttonXstart, 0, self.itemFrameZorigin - 0.999), incButton_image3_color=Vec4(1, 1, 1, 0.2), decButton_image=(self.gui.find('**/FndsLst_ScrollUp'),
         self.gui.find('**/FndsLst_ScrollDN'),
         self.gui.find('**/FndsLst_ScrollUp_Rllvr'),
         self.gui.find('**/FndsLst_ScrollUp')), decButton_relief=None, decButton_scale=(self.arrowButtonScale * 1.5, self.arrowButtonScale, self.arrowButtonScale), decButton_pos=(self.buttonXstart, 0, self.itemFrameZorigin + 0.125), decButton_image3_color=Vec4(1, 1, 1, 0.2), itemFrame_pos=(self.itemFrameXorigin, 0, self.itemFrameZorigin), itemFrame_scale=1.0, itemFrame_relief=DGG.SUNKEN, itemFrame_frameSize=(self.listXorigin,
         self.listXorigin + self.listFrameSizeX,
         self.listZorigin,
         self.listZorigin + self.listFrameSizeZ), itemFrame_frameColor=(0.85, 0.95, 1, 1), itemFrame_borderWidth=(0.01, 0.01), numItemsVisible=15, forceHeight=0.065, items=self.checkButtons)
        make_dsl_scrollable(self.scrollList)
        self.scrollList.scrollTo(selectedIndex)
        return

    def updateHintPointText(self):
        self.hintPointsTitle['text'] = TTLocalizer.HintPointsTitle % base.localAvatar.hintPoints

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
        keyItems = []
        progressionItems = []
        usefulItems = []
        junkItems = []
        # Generate new buttons
        for item_id, quantity in allItems.items():
            itemDef = get_item_def_from_id(item_id)
            if itemDef is None:
                print("ALERT I DON'T KNOW WHAT %s IS -- ENRAGE AT MICA" % item_id)
                continue

            button = self.makeCheckButton(itemDef.name, itemsAndCount.get(itemDef.unique_id, 0), quantity)
            itemName = itemDef.name.value
            if "Key" in itemName or "Disguise" in itemName:
                keyItems.append(button[0])
                continue
            if itemDef.classification == 0b0001:  # Progression Items
                progressionItems.append(button[0])
            elif itemDef.classification == 0b0010:  # Useful Items
                usefulItems.append(button[0])
            else:
                junkItems.append(button[0])
        self.checkButtons = keyItems + progressionItems + usefulItems + junkItems

    def makeCheckButton(self, checkName, checkCount, checkMax):
        checkButtonParent = DirectFrame()
        checkButtonL = DirectButton(parent=checkButtonParent, relief=None, text=checkName.value, text_scale=0.06, text_align=TextNode.ALeft, text1_bg=self.textDownColor, text2_bg=self.textRolloverColor, text3_fg=self.textDisabledColor, textMayChange=0, command=None)
        model = loader.loadModel('phase_4/models/parties/schtickerbookHostingGUI')
        check = model.find('**/checkmark')
        x = model.find('**/x')
        hinted = model.find('**/questionMark')
        hasBeenHinted = False  # TODO: Check for player hinting
        if checkCount >= checkMax:
            geomToUse = check
        elif hasBeenHinted:
            geomToUse = hinted
        else:
            geomToUse = x
        checkButtonR = DirectButton(parent=checkButtonParent, relief=None, image=geomToUse, image_scale=(1.25, 1.25, 1.25), pos=(0.99, 0, 0.0125), text=str(checkCount) + '/' + str(checkMax), text_scale=0.06, text_align=TextNode.ACenter, text_pos=(-0.075, -0.0125), text_fg=Vec4(0, 0, 0, 0), text1_fg=Vec4(0, 0, 0, 0), text2_fg=Vec4(0, 0, 0, 1), text3_fg=Vec4(0, 0, 0, 0), command=None)
        model.removeNode()
        del model
        del check
        del hinted
        del x
        return (checkButtonParent, checkButtonR, checkButtonL)
