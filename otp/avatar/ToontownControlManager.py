from direct.controls.ControlManager import ControlManager
from direct.directnotify import DirectNotifyGlobal
from direct.showbase.InputStateGlobal import inputState


class ToontownControlManager(ControlManager):
    notify = DirectNotifyGlobal.directNotify.newCategory("TTControlManager")

    def __init__(self, enable=True):
        self.forceTokens = None
        self.craneControlsEnabled = False
        super().__init__(enable)

    def enable(self):
        assert self.notify.debugCall(id(self))

        if self.isEnabled:
            assert self.notify.debug('already isEnabled')
            return

        self.isEnabled = 1

        self.enableControls()

        # keep track of what we do on the inputState so we can undo it later on
        # self.inputStateTokens = []

        controls = base.controls
        up = controls.MOVE_UP
        down = controls.MOVE_DOWN
        left = controls.MOVE_LEFT
        right = controls.MOVE_RIGHT
        jump = controls.JUMP

        self.inputStateTokens.extend((
            inputState.watch("run", 'runningEvent', "running-on", "running-off"),

            inputState.watchWithModifiers("forward", up, inputSource=inputState.ArrowKeys),
            inputState.watch("forward", "force-forward", "force-forward-stop"),

            inputState.watchWithModifiers("reverse", down, inputSource=inputState.ArrowKeys),
            inputState.watchWithModifiers("reverse", "mouse4", inputSource=inputState.Mouse),

            inputState.watchWithModifiers("turnLeft", left, inputSource=inputState.ArrowKeys),
            inputState.watch("turnLeft", "mouse-look_left", "mouse-look_left-done"),
            inputState.watch("turnLeft", "force-turnLeft", "force-turnLeft-stop"),

            inputState.watchWithModifiers("turnRight", right, inputSource=inputState.ArrowKeys),
            inputState.watch("turnRight", "mouse-look_right", "mouse-look_right-done"),
            inputState.watch("turnRight", "force-turnRight", "force-turnRight-stop"),

            inputState.watchWithModifiers("jump", jump),
        ))

        self.setTurn(1)

        if self.currentControls:
            self.currentControls.enableAvatarControls()

    def enableControls(self):
        if self.forceTokens:
            for token in self.forceTokens:
                token.release()
            self.forceTokens = []

    def disableControls(self):
        self.forceTokens = [
            inputState.force('jump', 0, 'TTControlManager.disableControls'),
            inputState.force('forward', 0, 'TTControlManager.disableControls'),
            inputState.force('turnLeft', 0, 'TTControlManager.disableControls'),
            inputState.force('slideLeft', 0, 'TTControlManager.disableControls'),
            inputState.force('reverse', 0, 'TTControlManager.disableControls'),
            inputState.force('turnRight', 0, 'TTControlManager.disableControls'),
            inputState.force('slideRight', 0, 'TTControlManager.disableControls')
        ]

    def setTurn(self, turn):
        self.__WASDTurn = turn

        if not self.isEnabled:
            return

        turnLeftWASDSet = inputState.isSet("turnLeft", inputSource=inputState.ArrowKeys)
        turnRightWASDSet = inputState.isSet("turnRight", inputSource=inputState.ArrowKeys)
        slideLeftWASDSet = inputState.isSet("slideLeft", inputSource=inputState.ArrowKeys)
        slideRightWASDSet = inputState.isSet("slideRight", inputSource=inputState.ArrowKeys)

        for token in self.WASDTurnTokens:
            token.release()

        controls = base.controls
        left = controls.MOVE_LEFT
        right = controls.MOVE_RIGHT

        if turn:
            self.WASDTurnTokens = (
                inputState.watchWithModifiers("turnLeft", left, inputSource=inputState.ArrowKeys),
                inputState.watchWithModifiers("turnRight", right, inputSource=inputState.ArrowKeys),
            )

            inputState.set("turnLeft", slideLeftWASDSet, inputSource=inputState.ArrowKeys)
            inputState.set("turnRight", slideRightWASDSet, inputSource=inputState.ArrowKeys)

            inputState.set("slideLeft", False, inputSource=inputState.ArrowKeys)
            inputState.set("slideRight", False, inputSource=inputState.ArrowKeys)

        else:
            self.WASDTurnTokens = (
                inputState.watchWithModifiers("slideLeft", left, inputSource=inputState.ArrowKeys),
                inputState.watchWithModifiers("slideRight", right, inputSource=inputState.ArrowKeys),
            )

            inputState.set("slideLeft", turnLeftWASDSet, inputSource=inputState.ArrowKeys)
            inputState.set("slideRight", turnRightWASDSet, inputSource=inputState.ArrowKeys)

            inputState.set("turnLeft", False, inputSource=inputState.ArrowKeys)
            inputState.set("turnRight", False, inputSource=inputState.ArrowKeys)

    def enableCraneControls(self):
        """
        This function should only be called for when our controls are disabled,
        but we need to map our movement keys to functions. (i.e. on a crane, on a banquet table, etc.)
        This serves as an improved implementation of 'passMessagesThrough'.
        """

        if self.isEnabled and self.craneControlsEnabled:
            return

        controls = base.controls

        self.inputStateTokens.extend((
            inputState.watchWithModifiers("forward", controls.MOVE_UP, inputSource=inputState.ArrowKeys),
            inputState.watchWithModifiers("reverse", controls.MOVE_DOWN, inputSource=inputState.ArrowKeys),
            inputState.watchWithModifiers("turnLeft", controls.MOVE_LEFT, inputSource=inputState.ArrowKeys),
            inputState.watchWithModifiers("turnRight", controls.MOVE_RIGHT, inputSource=inputState.ArrowKeys)
        ))

    def disableCraneControls(self):
        """
        Disables crane controls.
        """

        if not self.isEnabled and not self.craneControlsEnabled:
            return

        for token in self.inputStateTokens:
            token.release()
        self.inputStateTokens = []
