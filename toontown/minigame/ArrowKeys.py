from panda3d.core import ModifierButtons
from direct.showbase.DirectObject import DirectObject

class ArrowKeys(DirectObject):
    UP_INDEX = 0
    DOWN_INDEX = 1
    LEFT_INDEX = 2
    RIGHT_INDEX = 3
    JUMP_INDEX = 4
    NULL_HANDLERS = (None, None, None, None, None)

    def __init__(self):
        self.__jumpPost = 0
        self.setPressHandlers(self.NULL_HANDLERS)
        self.setReleaseHandlers(self.NULL_HANDLERS)
        self.origMb = base.buttonThrowers[0].node().getModifierButtons()
        base.buttonThrowers[0].node().setModifierButtons(ModifierButtons())
        self.enable()

    def enable(self):
        self.disable()
        self.accept(base.controls.MOVE_UP, self.__upKeyPressed)
        self.accept(base.controls.MOVE_DOWN, self.__downKeyPressed)
        self.accept(base.controls.MOVE_LEFT, self.__leftKeyPressed)
        self.accept(base.controls.MOVE_RIGHT, self.__rightKeyPressed)
        self.accept(base.controls.JUMP, self.__jumpKeyPressed)

    def disable(self):
        self.__upPressed = 0
        self.__downPressed = 0
        self.__leftPressed = 0
        self.__rightPressed = 0
        self.__jumpPressed = 0
        self.ignore(base.controls.MOVE_UP)
        self.ignore(base.controls.MOVE_DOWN)
        self.ignore(base.controls.MOVE_LEFT)
        self.ignore(base.controls.MOVE_RIGHT)
        self.ignore(base.controls.JUMP)
        self.ignore(base.controls.MOVE_UP + '-up')
        self.ignore(base.controls.MOVE_DOWN + '-up')
        self.ignore(base.controls.MOVE_LEFT + '-up')
        self.ignore(base.controls.MOVE_RIGHT + '-up')
        self.ignore(base.controls.JUMP + '-up')

    def destroy(self):
        base.buttonThrowers[0].node().setModifierButtons(self.origMb)
        events = [base.controls.MOVE_UP,
         base.controls.MOVE_DOWN,
         base.controls.MOVE_LEFT,
         base.controls.MOVE_RIGHT,
         base.controls.JUMP]
        for event in events:
            self.ignore(event)
            self.ignore(event + '-up')

    def upPressed(self):
        return self.__upPressed

    def downPressed(self):
        return self.__downPressed

    def leftPressed(self):
        return self.__leftPressed

    def rightPressed(self):
        return self.__rightPressed

    def jumpPressed(self):
        return self.__jumpPressed

    def jumpPost(self):
        jumpCache = self.__jumpPost
        self.__jumpPost = 0
        return jumpCache

    def setPressHandlers(self, handlers):
        if len(handlers) == 4:
            handlers.append(None)
        self.__checkCallbacks(handlers)
        self.__pressHandlers = handlers
        return

    def setReleaseHandlers(self, handlers):
        if len(handlers) == 4:
            handlers.append(None)
        self.__checkCallbacks(handlers)
        self.__releaseHandlers = handlers
        return

    def clearPressHandlers(self):
        self.setPressHandlers(self.NULL_HANDLERS)

    def clearReleaseHandlers(self):
        self.setReleaseHandlers(self.NULL_HANDLERS)

    def __checkCallbacks(self, callbacks):
        for callback in callbacks:
            pass

    def __doCallback(self, callback):
        if callback:
            callback()

    def __upKeyPressed(self):
        self.ignore(base.controls.MOVE_UP)
        self.accept(base.controls.MOVE_UP + '-up', self.__upKeyReleased)
        self.__upPressed = 1
        self.__doCallback(self.__pressHandlers[self.UP_INDEX])

    def __downKeyPressed(self):
        self.ignore(base.controls.MOVE_DOWN)
        self.accept(base.controls.MOVE_DOWN + '-up', self.__downKeyReleased)
        self.__downPressed = 1
        self.__doCallback(self.__pressHandlers[self.DOWN_INDEX])

    def __leftKeyPressed(self):
        self.ignore(base.controls.MOVE_LEFT)
        self.accept(base.controls.MOVE_LEFT + '-up', self.__leftKeyReleased)
        self.__leftPressed = 1
        self.__doCallback(self.__pressHandlers[self.LEFT_INDEX])

    def __rightKeyPressed(self):
        self.ignore(base.controls.MOVE_RIGHT)
        self.accept(base.controls.MOVE_RIGHT + '-up', self.__rightKeyReleased)
        self.__rightPressed = 1
        self.__doCallback(self.__pressHandlers[self.RIGHT_INDEX])

    def __jumpKeyPressed(self):
        self.ignore(base.controls.JUMP)
        self.accept(base.controls.JUMP + '-up', self.__jumpKeyReleased)
        self.__jumpPressed = 1
        self.__jumpPost = 1
        self.__doCallback(self.__pressHandlers[self.JUMP_INDEX])

    def __upKeyReleased(self):
        self.ignore(base.controls.MOVE_UP + '-up')
        self.accept(base.controls.MOVE_UP, self.__upKeyPressed)
        self.__upPressed = 0
        self.__doCallback(self.__releaseHandlers[self.UP_INDEX])

    def __downKeyReleased(self):
        self.ignore(base.controls.MOVE_DOWN + '-up')
        self.accept(base.controls.MOVE_DOWN, self.__downKeyPressed)
        self.__downPressed = 0
        self.__doCallback(self.__releaseHandlers[self.DOWN_INDEX])

    def __leftKeyReleased(self):
        self.ignore(base.controls.MOVE_LEFT + '-up')
        self.accept(base.controls.MOVE_LEFT, self.__leftKeyPressed)
        self.__leftPressed = 0
        self.__doCallback(self.__releaseHandlers[self.LEFT_INDEX])

    def __rightKeyReleased(self):
        self.ignore(base.controls.MOVE_RIGHT + '-up')
        self.accept(base.controls.MOVE_RIGHT, self.__rightKeyPressed)
        self.__rightPressed = 0
        self.__doCallback(self.__releaseHandlers[self.RIGHT_INDEX])

    def __jumpKeyReleased(self):
        self.ignore(base.controls.JUMP + '-up')
        self.accept(base.controls.JUMP, self.__jumpKeyPressed)
        self.__jumpPressed = 0
        self.__jumpPost = 0
        self.__doCallback(self.__releaseHandlers[self.JUMP_INDEX])
