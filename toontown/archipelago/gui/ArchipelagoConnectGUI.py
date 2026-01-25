from panda3d.core import *
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from direct.gui.DirectButton import DirectButton
from direct.gui.DirectFrame import DirectFrame
from direct.gui.DirectLabel import DirectLabel
from panda3d.core import TextNode, TransparencyAttrib
YOFFSET = 0.265
BOTTOM_X = -0.185
class ArchipelagoConnectGUI(DirectFrame):

    def __init__(self):
        self.guiButton = loader.loadModel('phase_3/models/gui/quit_button')
        self.cdrGui = loader.loadModel('phase_3.5/models/gui/tt_m_gui_sbk_codeRedemptionGui')
        DirectFrame.__init__(self, parent=aspect2dp, relief=None, image=self.cdrGui.find('**/tt_t_gui_sbk_cdrCodeBox'), pos=(-0.46, 0.0, 0.53), scale=(1.0, 1.0, 1.0))
        self.load()

    def load(self):
        self.container_frame = DirectFrame(parent=self, relief=None, image=DGG.getDefaultDialogGeom(),
                                           pos=(0, 0.0, -0.066), scale=(1.1, 1, 0.95))
        self.loadSlotItems()
        self.loadIpItems()
        self.loadPassItems()
        self.loadButtons()

    def updateFields(self):
        if hasattr(base, 'localAvatar'):
            self.ipBarEntry.set(str(base.localAvatar.getArchipelagoIP()))
            self.slotBarEntry.set(str(base.localAvatar.getSlotName()))

    def loadSlotItems(self):
        self.slotBarFrame = DirectFrame(parent=self, relief=None, image=self.cdrGui.find('**/tt_t_gui_sbk_cdrCodeBox'),
                                        pos=(-0.01, 0.0, YOFFSET), scale=(1.3, 1, 0.7))
        self.slotLabel = DirectLabel(parent=self.slotBarFrame, relief=None, text="Slot Name", text_scale=(0.06, 0.06, 0.18),
                                     text_wordwrap=12, text_align=TextNode.ACenter, textMayChange=1,
                                     pos=(0, 0, 0.15))
        self.slotBarEntry = DirectEntry(parent=self.slotBarFrame, relief=None, text_scale=(0.05, 0.07, 0.07), width=13.25,
                                        textMayChange=1,
                                        pos=(-0.33, 0, 0), text_align=TextNode.ALeft, backgroundFocus=0,
                                        focusInCommand=self.entrySlot)

    def loadIpItems(self):
        self.ipBarFrame = DirectFrame(parent=self, relief=None, image=self.cdrGui.find('**/tt_t_gui_sbk_cdrCodeBox'),
                                        pos=(-0.01, 0.0, (YOFFSET-0.23)), scale=(1.3, 1, 0.7))
        self.ipLabel = DirectLabel(parent=self.ipBarFrame, relief=None, text="Archipelago IP", text_scale=(0.06, 0.06, 0.18),
                                     text_wordwrap=12, text_align=TextNode.ACenter, textMayChange=1,
                                     pos=(0, 0, 0.15))
        self.ipBarEntry = DirectEntry(parent=self.ipBarFrame, relief=None, text_scale=(0.05, 0.07, 0.07), width=13.25,
                                        textMayChange=1,
                                        pos=(-0.33, 0, 0), text_align=TextNode.ALeft, backgroundFocus=0,
                                        focusInCommand=self.entryIp)

    def loadPassItems(self):
        self.passBarFrame = DirectFrame(parent=self, relief=None, image=self.cdrGui.find('**/tt_t_gui_sbk_cdrCodeBox'),
                                        pos=(-0.01, 0.0, (YOFFSET-0.46)), scale=(1.3, 1, 0.7))
        self.passLabel = DirectLabel(parent=self.passBarFrame, relief=None, text="Room Password", text_scale=(0.06, 0.06, 0.18),
                                     text_wordwrap=12, text_align=TextNode.ACenter, textMayChange=1,
                                     pos=(0, 0, 0.15))
        self.passBarEntry = DirectEntry(parent=self.passBarFrame, relief=None, text_scale=(0.05, 0.07, 0.07), width=13.25,
                                        textMayChange=1,
                                        pos=(-0.33, 0, 0), text_align=TextNode.ALeft, backgroundFocus=0,
                                        focusInCommand=self.entryPass, obscured=1)

    def loadButtons(self):
        self.connectButton = DirectButton(parent=self, relief=None, image=(self.guiButton.find('**/QuitBtn_UP'),
                                                                        self.guiButton.find('**/QuitBtn_DN'),
                                                                        self.guiButton.find('**/QuitBtn_RLVR')),
                                       image_scale=(0.7, 1, 1), text="Connect",
                                       text_scale=0.045, text_pos=(0, -0.01), pos=(0.35, 0.0, (YOFFSET-0.605)),
                                       command=self.handleConnect)
        self.disconnectButton = DirectButton(parent=self, relief=None, image=(self.guiButton.find('**/QuitBtn_UP'),
                                                                         self.guiButton.find('**/QuitBtn_DN'),
                                                                         self.guiButton.find('**/QuitBtn_RLVR')),
                                        image_scale=(0.7, 1, 1), text="Disconnect",
                                        text_scale=0.045, text_pos=(0, -0.01), pos=(0, 0.0, (YOFFSET-0.605)),
                                        command=self.handleDisconnect)
        self.resetButton = DirectButton(parent=self, relief=None, image=(self.guiButton.find('**/QuitBtn_UP'),
                                                                           self.guiButton.find('**/QuitBtn_DN'),
                                                                           self.guiButton.find('**/QuitBtn_RLVR')),
                                          image_scale=(0.7, 1, 1), text="Reset Toon",
                                          text_scale=0.045, text_pos=(0, -0.01), pos=(-0.35, 0.0, (YOFFSET-0.605)),
                                          command=self.handleReset)
        self.deathlinkButton = DirectButton(parent=self, relief=None, image=(self.guiButton.find('**/QuitBtn_UP'),
                                                                         self.guiButton.find('**/QuitBtn_DN'),
                                                                         self.guiButton.find('**/QuitBtn_RLVR')),
                                        image_scale=(1.2, 1, 1), text="Change Deathlink Mode",
                                        text_scale=0.045, text_pos=(0, -0.01), pos=(BOTTOM_X, 0.0, (YOFFSET - 0.73)),
                                        command=self.handleDeathlink)
        self.ringlinkButton = DirectButton(parent=self, relief=None, image=(self.guiButton.find('**/QuitBtn_UP'),
                                                                             self.guiButton.find('**/QuitBtn_DN'),
                                                                             self.guiButton.find('**/QuitBtn_RLVR')),
                                            image_scale=(0.73, 1, 1), text="Toggle Ringlink",
                                            text_scale=0.045, text_pos=(0, -0.01), pos=((BOTTOM_X + 0.46), 0.0, (YOFFSET - 0.73)),
                                            command=self.handleRinglink)

    def handleConnect(self):
        base.talkAssistant.sendOpenTalk(f"~ap slot {self.slotBarEntry.get()}")
        base.talkAssistant.sendOpenTalk(f"~ap password {self.passBarEntry.get()}")
        base.talkAssistant.sendOpenTalk(f"~ap connect {self.ipBarEntry.get()}")
        self.toggleEntryFocus(True)

    def handleDisconnect(self):
        base.talkAssistant.sendOpenTalk("~ap disconnect")
        self.toggleEntryFocus(True)

    def handleReset(self):
        base.talkAssistant.sendOpenTalk("~ap clear")
        self.toggleEntryFocus(True)

    def handleDeathlink(self):
        base.talkAssistant.sendOpenTalk("~ap deathlink")
        self.toggleEntryFocus(True)

    def handleRinglink(self):
        base.talkAssistant.sendOpenTalk("~ap ringlink")
        self.toggleEntryFocus(True)

    def entrySlot(self):
        self.toggleEntryFocus()
        self.slotBarEntry.setCursorPosition(len(self.slotBarEntry.get()))

    def entryIp(self):
        self.toggleEntryFocus()
        self.ipBarEntry.setCursorPosition(len(self.ipBarEntry.get()))

    def entryPass(self):
        self.toggleEntryFocus()
        self.passBarEntry.setCursorPosition(len(self.passBarEntry.get()))

    def toggleEntryFocus(self, lose=False):
        if not hasattr(base, "localAvatar"):
            self.ignore('mouse1')
            return
        if lose:
            self.slotBarEntry['focus'] = 0
            self.ipBarEntry['focus'] = 0
            self.passBarEntry['focus'] = 0
            messenger.send("enable-hotkeys")
            base.localAvatar.enableControls()
        else:
            messenger.send("disable-hotkeys")
            base.localAvatar.disableControls()
            self.acceptOnce('mouse1', self.toggleEntryFocus, extraArgs=[True])