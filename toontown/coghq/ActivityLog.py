from panda3d.core import *
from direct.gui.DirectGui import *
from direct.interval.FunctionInterval import Wait
from direct.interval.LerpInterval import LerpColorScaleInterval
from direct.interval.MetaInterval import Sequence


class ActivityLog(DirectFrame):
    def __init__(self):
        DirectFrame.__init__(self, relief=None)
        self.log = DirectScrolledList(parent=self, pos=(.6, 0, .3), items=['' for _ in range(12)], numItemsVisible=12, decButton_relief=None, incButton_relief=None, forceHeight=.1)

    def destroy(self):
        self.log.destroy()
        self.destroy()

    def addToLog(self, msg):
        msg_label = DirectLabel(relief=None, text=msg, text_scale=0.04, text_pos=(1.2, 0), text_style=3,
                                text_align=TextNode.ARight, text_wordwrap=30, text_fg=(.8, .8, .8, 1),
                                text_shadow=(0, 0, 0, 1))

        Sequence(
            Wait(10),
            LerpColorScaleInterval(msg_label, duration=2.5, colorScale=(1, 1, 1, 0), startColorScale=(1, 1, 1, 1))
        ).start()

        self.log.addItem(msg_label)
        self.log.scrollTo(len(self.log['items']) - 1)
