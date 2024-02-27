import random

from panda3d.core import *
from direct.gui.DirectGui import *
from direct.interval.FunctionInterval import Wait
from direct.interval.LerpInterval import LerpColorScaleInterval
from direct.interval.MetaInterval import Sequence


class ArchipelagoOnscreenLog(DirectFrame):
    NUM_ITEMS_VISIBLE = 16
    X_OFFSET = 0.05
    Z_OFFSET = -0.65

    DEBUG = True

    def __init__(self):
        DirectFrame.__init__(self, parent=base.a2dTopLeft, relief=None)
        self.log = DirectScrolledList(parent=self, pos=(self.X_OFFSET, 0, self.Z_OFFSET), items=['' for _ in range(self.NUM_ITEMS_VISIBLE)],
                                      numItemsVisible=self.NUM_ITEMS_VISIBLE, decButton_relief=None,
                                      incButton_relief=None, forceHeight=0.065)

    def destroy(self):
        self.log.removeAndDestroyAllItems()
        self.log.destroy()
        super().destroy()

    def addToLog(self, msg):
        msg_label = DirectLabel(relief=None, text=msg, text_scale=0.03, text_style=3,
                                text_align=TextNode.ALeft, text_wordwrap=40, text_fg=(1, 1, 1, 1),
                                text_shadow=(0, 0, 0, 1))

        Sequence(
            Wait(10),
            LerpColorScaleInterval(msg_label, duration=2.5, colorScale=(1, 1, 1, 0), startColorScale=(1, 1, 1, 1))
        ).start()

        self.log.addItem(msg_label)
        self.log.scrollTo(len(self.log['items']) - 1)
