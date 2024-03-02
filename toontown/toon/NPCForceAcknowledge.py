from panda3d.core import *
from toontown.toontowngui import TTDialog
from toontown.toonbase import TTLocalizer
from direct.gui import DirectLabel
from toontown.quest import Quests

class NPCForceAcknowledge:

    def __init__(self, doneEvent):
        self.doneEvent = doneEvent
        self.dialog = None
        return

    def enter(self):
        doneStatus = {}
        doneStatus['mode'] = 'complete'
        messenger.send(self.doneEvent, [doneStatus])

    def exit(self):
        if self.dialog:
            self.dialog.cleanup()
            self.dialog = None
        return