import random
from typing import Dict

from panda3d.core import *
from direct.gui.DirectGui import *
from direct.interval.FunctionInterval import Wait, Func
from direct.interval.LerpInterval import LerpColorScaleInterval
from direct.interval.MetaInterval import Sequence


class ArchipelagoOnscreenLog(DirectFrame):
    NUM_ITEMS_VISIBLE = 20
    X_OFFSET = 0.05
    Z_OFFSET = -0.15
    ENTRY_VISIBLITY_LENGTH = 15

    def __init__(self):
        DirectFrame.__init__(self, parent=base.a2dTopLeft, relief=None)
        self.log = DirectScrolledList(parent=self, pos=(self.X_OFFSET, 0, self.Z_OFFSET), items=['' for _ in range(self.NUM_ITEMS_VISIBLE)],
                                      numItemsVisible=self.NUM_ITEMS_VISIBLE, decButton_relief=None,
                                      incButton_relief=None, forceHeight=0.08)

        self.sequenceCache: Dict[int, Sequence] = {}
        self.accept("f2", self.showAllEntries)  # todo remove this for better version

    def destroy(self):
        self.__cleanupAllSequences()
        self.log.removeAndDestroyAllItems()
        self.log.destroy()
        super().destroy()

    def addToLog(self, msg):

        # We need to correctly scrub for color properties
        text_scale_modifier = max(0.4, base.settings.get('archipelago-textsize'))
        msg_label = DirectLabel(relief=None, text=msg, text_scale=(0.06 * text_scale_modifier), text_style=3,
                                text_align=TextNode.ALeft, text_wordwrap=40, text_fg=(1, 1, 1, 1), text_bg=(0, 0, 0, 0),
                                text_shadow=(0, 0, 0, 1))
        if base.localAvatar.wantLogBg:
            msg_label['text_bg'] = (0, 0, 0, 0.3)
        self.log.addItem(msg_label)
        pos = len(self.log['items']) - 1
        # Change any possible still visible entries after we change settings and add something
        numItems = len(self.log['items'])
        if numItems > 1:
            if self.log['items'][pos-1]['text_scale'] != (0.06 * text_scale_modifier):
                for item in range(numItems):
                    self.log['items'][item]['text_scale'] = (0.06 * text_scale_modifier)
            if base.localAvatar.wantLogBg:
                bg_color = (0, 0, 0, 0.3)
            else:
                bg_color = (0, 0, 0, 0)
            for item in range(numItems):
                self.log['items'][item]['text_bg'] = bg_color

        self.log.scrollTo(pos)
        self.doFadeoutSequence(pos, msg_label)

    def getFadeoutSequence(self, __id, __label):
        return Sequence(
            Wait(self.ENTRY_VISIBLITY_LENGTH),
            LerpColorScaleInterval(__label, duration=3, colorScale=(1, 1, 1, 0), startColorScale=(1, 1, 1, 1)),
            Func(__label.hide),
            Func(self.__cleanupSequence, __id)
        )

    def doFadeoutSequence(self, pos, label):
        self.__cleanupSequence(pos)
        seq = self.getFadeoutSequence(pos, label)
        self.sequenceCache[pos] = seq
        seq.start()

    def __cleanupSequence(self, seqID):
        if seqID not in self.sequenceCache:
            return

        seq = self.sequenceCache[seqID]
        del self.sequenceCache[seqID]

        if seq is None:
            return

        seq.finish()

    def __cleanupAllSequences(self):
        for seqID in list(self.sequenceCache.keys()):
            self.__cleanupSequence(seqID)

    def showAllEntries(self):

        numItems = len(self.log['items'])
        # If there are so many items that we shouldn't show some of them, splice the list
        startShowIndex = 0
        if numItems > self.NUM_ITEMS_VISIBLE:
            startShowIndex = numItems - self.NUM_ITEMS_VISIBLE

        text_scale_modifier = max(0.4, base.settings.get('archipelago-textsize'))
        for labelIndex in range(startShowIndex, numItems):
            entry = self.log['items'][labelIndex]
            self.doFadeoutSequence(labelIndex, entry)
            # Used to resize old entries if we change the setting mid session and haven't added anything new since
            entry['text_scale'] = (0.06 * text_scale_modifier)
            if base.localAvatar.wantLogBg:
                entry['text_bg'] = (0, 0, 0, 0.3)
            else:
                entry['text_bg'] = (0, 0, 0, 0)
            entry.setColorScale(1, 1, 1, 1)
            entry.show()

    def hideAllEntries(self):
        for i, entry in enumerate(self.log['items']):
            self.__cleanupSequence(i)
            entry.hide()
