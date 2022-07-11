from direct.fsm import ClassicFSM, State

from toontown.shtiker.OptionsPageGUI import OptionButton
from toontown.toonbase import TTLocalizer
from toontown.toonbase.ToontownGlobals import OptionsPageHotkey
from toontown.toontowngui import TTDialog


class KeybindRemap:

    UP = 0
    LEFT = 1
    DOWN = 2
    RIGHT = 3
    JUMP = 4
    ACTION_BUTTON = 5
    OPTIONS_PAGE_HOTKEY = 6
    CHAT_HOTKEY = 7
    SCREENSHOT_KEY = 8
    CRANE_GRAB_KEY = 9
    SPRINT_KEY = 10

    def __init__(self):
        self.dialog = TTDialog.TTGlobalDialog(
            dialogName="KeybindRemap",
            doneEvent="doneRemapping",
            style=TTDialog.TwoChoice,
            suppressKeys=True,
            suppressMouse=True,
        )
        scale = self.dialog.component("image0").getScale()
        scale.setX(((scale[0] * 5) / base.aspectRatio) * 1.2)
        scale.setZ(scale[2] * 2.25)
        self.dialog.component("image0").setScale(scale)
        button_x = -0.6
        button_y = 0.3
        labelPos = (0, 0, 0.1)

        self.upKey = OptionButton(
            parent=self.dialog,
            text=base.MOVE_UP,
            pos=(button_x, 0.0, button_y),
            command=self.enterWaitForKey,
            extraArgs=[self.UP],
            wantLabel=True,
            labelOrientation="top",
            labelPos=labelPos,
            labelText=TTLocalizer.Controls[0],
        )

        self.leftKey = OptionButton(
            parent=self.dialog,
            text=base.MOVE_LEFT,
            pos=(button_x + 0.4, 0.0, button_y),
            command=self.enterWaitForKey,
            extraArgs=[self.LEFT],
            wantLabel=True,
            labelOrientation="top",
            labelPos=labelPos,
            labelText=TTLocalizer.Controls[1],
        )

        self.downKey = OptionButton(
            parent=self.dialog,
            text=base.MOVE_DOWN,
            pos=(button_x + 0.8, 0.0, button_y),
            command=self.enterWaitForKey,
            extraArgs=[self.DOWN],
            wantLabel=True,
            labelOrientation="top",
            labelPos=labelPos,
            labelText=TTLocalizer.Controls[2],
        )

        self.rightKey = OptionButton(
            parent=self.dialog,
            text=base.MOVE_RIGHT,
            pos=(button_x + 1.2, 0.0, button_y),
            command=self.enterWaitForKey,
            extraArgs=[self.RIGHT],
            wantLabel=True,
            labelOrientation="top",
            labelPos=labelPos,
            labelText=TTLocalizer.Controls[3],
        )

        self.jumpKey = OptionButton(
            parent=self.dialog,
            text=base.JUMP,
            pos=(button_x, 0.0, button_y - 0.3),
            command=self.enterWaitForKey,
            extraArgs=[self.JUMP],
            wantLabel=True,
            labelOrientation="top",
            labelPos=labelPos,
            labelText=TTLocalizer.Controls[4],
        )

        self.actionKey = OptionButton(
            parent=self.dialog,
            text=base.ACTION_BUTTON,
            pos=(button_x + 0.4, 0.0, button_y - 0.3),
            command=self.enterWaitForKey,
            extraArgs=[self.ACTION_BUTTON],
            wantLabel=True,
            labelOrientation="top",
            labelPos=labelPos,
            labelText=TTLocalizer.Controls[5],
        )

        self.optionsKey = OptionButton(
            parent=self.dialog,
            text=OptionsPageHotkey,
            pos=(button_x + 0.8, 0.0, button_y - 0.3),
            command=self.enterWaitForKey,
            extraArgs=[self.OPTIONS_PAGE_HOTKEY],
            wantLabel=True,
            labelOrientation="top",
            labelPos=labelPos,
            labelText=TTLocalizer.Controls[6],
        )

        self.chatHotkey = OptionButton(
            parent=self.dialog,
            text=base.CHAT_HOTKEY,
            pos=(button_x + 1.2, 0.0, button_y - 0.3),
            command=self.enterWaitForKey,
            extraArgs=[self.CHAT_HOTKEY],
            wantLabel=True,
            labelOrientation="top",
            labelPos=labelPos,
            labelText=TTLocalizer.Controls[7],
        )

        self.screenshotKey = OptionButton(
            parent=self.dialog,
            text=base.SCREENSHOT_KEY,
            pos=(button_x, 0.0, button_y - 0.6),
            command=self.enterWaitForKey,
            extraArgs=[self.SCREENSHOT_KEY],
            wantLabel=True,
            labelOrientation="top",
            labelPos=labelPos,
            labelText=TTLocalizer.Controls[8],
        )

        self.craneGrabKey = OptionButton(
            parent=self.dialog,
            text=base.CRANE_GRAB_KEY,
            pos=(button_x + 0.4, 0.0, button_y - 0.6),
            command=self.enterWaitForKey,
            extraArgs=[self.CRANE_GRAB_KEY],
            wantLabel=True,
            labelOrientation="top",
            labelPos=labelPos,
            labelText=TTLocalizer.Controls[9],
        )

        self.sprintKey = OptionButton(
            parent=self.dialog,
            text=base.SPRINT,
            pos=(button_x + 0.8, 0.0, button_y - 0.6),
            command=self.enterWaitForKey,
            extraArgs=[self.SPRINT_KEY],
            wantLabel=True,
            labelOrientation="top",
            labelPos=labelPos,
            labelText=TTLocalizer.Controls[10],
        )

        self.controlsToBeSaved = {
            self.UP: base.MOVE_UP,
            self.LEFT: base.MOVE_LEFT,
            self.DOWN: base.MOVE_DOWN,
            self.RIGHT: base.MOVE_RIGHT,
            self.JUMP: base.JUMP,
            self.ACTION_BUTTON: base.ACTION_BUTTON,
            self.OPTIONS_PAGE_HOTKEY: OptionsPageHotkey,
            self.CHAT_HOTKEY: base.CHAT_HOTKEY,
            self.SCREENSHOT_KEY: base.SCREENSHOT_KEY,
            self.CRANE_GRAB_KEY: base.CRANE_GRAB_KEY,
            self.SPRINT_KEY: base.SPRINT
        }

        self.popupDialog = None
        self.dialog.show()

        self.fsm = ClassicFSM.ClassicFSM(
            "ControlRemapDialog",
            [
                State.State("off", self.enterShow, self.exitShow, ["waitForKey"]),
                State.State(
                    "waitForKey", self.enterWaitForKey, self.exitWaitForKey, ["off"]
                ),
            ],
            "off",
            "off",
        )

        self.fsm.enterInitialState()
        self.dialog.accept("doneRemapping", self.exit)
        messenger.send("disable-hotkeys")
        try:
            base.localAvatar.chatMgr.disableBackgroundFocus()
        except:
            pass

        for button in self.dialog.buttonList:
            button.setZ(-0.5)

    def enterShow(self):
        pass

    def exitShow(self):
        pass

    def enterWaitForKey(self, controlNum):
        base.transitions.fadeScreen(0.9)
        self.dialog.hide()

        if self.popupDialog:
            self.popupDialog.cleanup()

        self.popupDialog = TTDialog.TTDialog(
            style=TTDialog.NoButtons,
            text=TTLocalizer.RemapPopup,
            suppressMouse=True,
            suppressKeys=True,
        )

        scale = self.popupDialog.component("image0").getScale()
        scale.setX((scale[0] * 1.75) / base.aspectRatio)
        scale.setZ(scale[2] * 1.75)
        self.popupDialog.setScale(scale)
        self.popupDialog.show()

        base.buttonThrowers[0].node().setButtonDownEvent("buttonPress" + str(controlNum))
        self.dialog.accept("buttonPress" + str(controlNum), self.registerKey, [controlNum])

    def registerKey(self, controlNum, keyName):
        self.popupDialog.cleanup()
        self.controlsToBeSaved[controlNum] = keyName
        if controlNum == self.UP:
            self.upKey["text"] = keyName
        elif controlNum == self.LEFT:
            self.leftKey["text"] = keyName
        elif controlNum == self.DOWN:
            self.downKey["text"] = keyName
        elif controlNum == self.RIGHT:
            self.rightKey["text"] = keyName
        elif controlNum == self.JUMP:
            self.jumpKey["text"] = keyName
        elif controlNum == self.ACTION_BUTTON:
            self.actionKey["text"] = keyName
        elif controlNum == self.OPTIONS_PAGE_HOTKEY:
            self.optionsKey["text"] = keyName
        elif controlNum == self.CHAT_HOTKEY:
            self.chatHotkey["text"] = keyName
        elif controlNum == self.SCREENSHOT_KEY:
            self.screenshotKey["text"] = keyName
        elif controlNum == self.CRANE_GRAB_KEY:
            self.craneGrabKey['text'] = keyName
        elif controlNum == self.SPRINT_KEY:
            self.sprintKey['text'] = keyName
        self.dialog.show()
        self.exitWaitForKey(controlNum, keyName)

    def exitWaitForKey(self, controlNum, keyName):
        self.dialog.ignore("buttonPress" + str(controlNum))

    def exit(self):
        if self.dialog.doneStatus == "ok":
            self.enterSave()
        else:
            self.enterCancel()

    def enterSave(self):
        keymap = base.settings.getOption("game", "keymap", {})
        keymap["MOVE_UP"] = self.controlsToBeSaved[self.UP]
        keymap["MOVE_LEFT"] = self.controlsToBeSaved[self.LEFT]
        keymap["MOVE_DOWN"] = self.controlsToBeSaved[self.DOWN]
        keymap["MOVE_RIGHT"] = self.controlsToBeSaved[self.RIGHT]
        keymap["JUMP"] = self.controlsToBeSaved[self.JUMP]
        keymap["ACTION_BUTTON"] = self.controlsToBeSaved[self.ACTION_BUTTON]
        keymap["OPTIONS_PAGE_HOTKEY"] = self.controlsToBeSaved[self.OPTIONS_PAGE_HOTKEY]
        keymap["CHAT_HOTKEY"] = self.controlsToBeSaved[self.CHAT_HOTKEY]
        keymap["CRANE_GRAB_KEY"] = self.controlsToBeSaved[self.CRANE_GRAB_KEY]
        keymap["SPRINT_KEY"] = self.controlsToBeSaved[self.SPRINT_KEY]
        base.settings.updateSetting('game', 'keymap', keymap)

        base.reloadControls()
        try:
            base.localAvatar.controlManager.reload()
            base.localAvatar.chatMgr.reloadWASD()
            self.unload()

            base.localAvatar.controlManager.disable()
        except:
            self.unload()

    def exitSave(self):
        pass

    def enterCancel(self):
        self.unload()

    def exitCancel(self):
        pass

    def unload(self):
        if self.popupDialog:
            self.popupDialog.cleanup()
        del self.popupDialog
        self.dialog.cleanup()
        del self.dialog
        messenger.send("enable-hotkeys")
