from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import DirectFrame, DirectButton
import direct.gui.DirectGuiGlobals as DGG
from toontown.parties import PartyUtils

class CannonGui(DirectObject):
    notify = directNotify.newCategory('CannonGui')
    FIRE_PRESSED = 'cannongui_fire_pressed'

    def __init__(self):
        self.__loaded = False
        self.leftPressed = 0
        self.rightPressed = 0
        self.upPressed = 0
        self.downPressed = 0
        self.__aimPad = None
        self.__timerPad = None
        return

    def load(self):
        if self.__loaded:
            return
        self.__timerPad = PartyUtils.getNewToontownTimer()
        guiModel = 'phase_4/models/gui/cannon_game_gui'
        guiNode = loader.loadModel(guiModel)
        self.__aimPad = DirectFrame(image=guiNode.find('**/CannonFire_PAD'), relief=None, pos=(0.7, 0, -0.553333), scale=0.8)
        guiNode.removeNode()
        self.fireButton = DirectButton(parent=self.__aimPad, image=((guiModel, '**/Fire_Btn_UP'), (guiModel, '**/Fire_Btn_DN'), (guiModel, '**/Fire_Btn_RLVR')), relief=None, pos=(0.0115741, 0, 0.00505051), scale=1.0, command=self.__firePressed)
        self.upButton = DirectButton(parent=self.__aimPad, image=((guiModel, '**/Cannon_Arrow_UP'), (guiModel, '**/Cannon_Arrow_DN'), (guiModel, '**/Cannon_Arrow_RLVR')), relief=None, pos=(0.0115741, 0, 0.221717))
        self.downButton = DirectButton(parent=self.__aimPad, image=((guiModel, '**/Cannon_Arrow_UP'), (guiModel, '**/Cannon_Arrow_DN'), (guiModel, '**/Cannon_Arrow_RLVR')), relief=None, pos=(0.0136112, 0, -0.210101), image_hpr=(0, 0, 180))
        self.leftButton = DirectButton(parent=self.__aimPad, image=((guiModel, '**/Cannon_Arrow_UP'), (guiModel, '**/Cannon_Arrow_DN'), (guiModel, '**/Cannon_Arrow_RLVR')), relief=None, pos=(-0.199352, 0, -0.000505269), image_hpr=(0, 0, -90))
        self.rightButton = DirectButton(parent=self.__aimPad, image=((guiModel, '**/Cannon_Arrow_UP'), (guiModel, '**/Cannon_Arrow_DN'), (guiModel, '**/Cannon_Arrow_RLVR')), relief=None, pos=(0.219167, 0, -0.00101024), image_hpr=(0, 0, 90))
        self.__aimPad.setColor(1, 1, 1, 0.9)

        def bindButton(button, upHandler, downHandler):
            button.bind(DGG.B1PRESS, lambda x, handler = upHandler: handler())
            button.bind(DGG.B1RELEASE, lambda x, handler = downHandler: handler())

        bindButton(self.upButton, self.__upPressed, self.__upReleased)
        bindButton(self.downButton, self.__downPressed, self.__downReleased)
        bindButton(self.leftButton, self.__leftPressed, self.__leftReleased)
        bindButton(self.rightButton, self.__rightPressed, self.__rightReleased)
        self.__loaded = True
        return

    def unload(self):
        self.ignoreAll()
        if not self.__loaded:
            return
        self.disable()
        self.upButton.unbind(DGG.B1PRESS)
        self.upButton.unbind(DGG.B1RELEASE)
        self.downButton.unbind(DGG.B1PRESS)
        self.downButton.unbind(DGG.B1RELEASE)
        self.leftButton.unbind(DGG.B1PRESS)
        self.leftButton.unbind(DGG.B1RELEASE)
        self.rightButton.unbind(DGG.B1PRESS)
        self.rightButton.unbind(DGG.B1RELEASE)
        self.fireButton.destroy()
        self.__aimPad.destroy()
        del self.__aimPad
        del self.fireButton
        del self.upButton
        del self.downButton
        del self.leftButton
        del self.rightButton
        self.__timerPad.destroy()
        del self.__timerPad
        self.__loaded = False

    def enable(self, timer = 0):
        self.__aimPad.show()
        base.setCellsAvailable([base.bottomCells[3], base.bottomCells[4]], 0)
        base.setCellsAvailable([base.rightCells[1]], 0)
        if timer > 0:
            self.__timerPad.setTime(timer)
            self.__timerPad.countdown(timer)
            self.__timerPad.show()
        self.enableKeys()

    def disable(self):
        self.__aimPad.hide()
        base.setCellsAvailable([base.bottomCells[3], base.bottomCells[4]], 1)
        base.setCellsAvailable([base.rightCells[1]], 1)
        self.__timerPad.hide()
        self.disableKeys()

    def enableKeys(self):
        self.enableAimKeys()
        self.enableFireKey()

    def disableKeys(self):
        self.__aimPad.hide()
        self.disableAimKeys()
        self.disableFireKey()

    def enableAimKeys(self):
        self.leftPressed = 0
        self.rightPressed = 0
        self.upPressed = 0
        self.downPressed = 0
        self.accept(base.controls.MOVE_UP, self.__upKeyPressed)
        self.accept(base.controls.MOVE_DOWN, self.__downKeyPressed)
        self.accept(base.controls.MOVE_LEFT, self.__leftKeyPressed)
        self.accept(base.controls.MOVE_RIGHT, self.__rightKeyPressed)

    def disableAimKeys(self):
        self.ignore(base.controls.MOVE_UP)
        self.ignore(base.controls.MOVE_DOWN)
        self.ignore(base.controls.MOVE_LEFT)
        self.ignore(base.controls.MOVE_RIGHT)
        messenger.send(base.controls.MOVE_UP + '-up')
        messenger.send(base.controls.MOVE_DOWN + '-up')
        messenger.send(base.controls.MOVE_LEFT + '-up')
        messenger.send(base.controls.MOVE_RIGHT + '-up')
        self.ignore(base.controls.MOVE_UP + "-up")
        self.ignore(base.controls.MOVE_DOWN + "-up")
        self.ignore(base.controls.MOVE_LEFT + "-up")
        self.ignore(base.controls.MOVE_RIGHT + "-up")

    def enableFireKey(self):
        self.accept(base.controls.JUMP, self.__fireKeyPressed)

    def disableFireKey(self):
        self.ignore(base.controls.JUMP)
        self.ignore(base.controls.JUMP + '-up')

    def __fireKeyPressed(self):
        self.ignore(base.controls.JUMP)
        self.accept(base.controls.JUMP + '-up', self.__fireKeyReleased)
        self.__firePressed()

    def __upKeyPressed(self):
        self.ignore(base.controls.MOVE_UP)
        self.accept(base.controls.MOVE_UP + '-up', self.__upKeyReleased)
        self.__upPressed()

    def __downKeyPressed(self):
        self.ignore(base.controls.MOVE_DOWN)
        self.accept(base.controls.MOVE_DOWN + '-up', self.__downKeyReleased)
        self.__downPressed()

    def __leftKeyPressed(self):
        self.ignore(base.controls.MOVE_LEFT)
        self.accept(base.controls.MOVE_LEFT + '-up', self.__leftKeyReleased)
        self.__leftPressed()

    def __rightKeyPressed(self):
        self.ignore(base.controls.MOVE_RIGHT)
        self.accept(base.controls.MOVE_RIGHT + '-up', self.__rightKeyReleased)
        self.__rightPressed()

    def __fireKeyReleased(self):
        self.ignore(base.controls.JUMP + '-up')
        self.accept(base.controls.JUMP, self.__fireKeyPressed)

    def __leftKeyReleased(self):
        self.ignore(base.controls.MOVE_LEFT + '-up')
        self.accept(base.controls.MOVE_LEFT, self.__leftKeyPressed)
        self.__leftReleased()

    def __rightKeyReleased(self):
        self.ignore(base.controls.MOVE_RIGHT + '-up')
        self.accept(base.controls.MOVE_RIGHT, self.__rightKeyPressed)
        self.__rightReleased()

    def __upKeyReleased(self):
        self.ignore(base.controls.MOVE_UP + '-up')
        self.accept(base.controls.MOVE_UP, self.__upKeyPressed)
        self.__upReleased()

    def __downKeyReleased(self):
        self.ignore(base.controls.MOVE_DOWN + '-up')
        self.accept(base.controls.MOVE_DOWN, self.__downKeyPressed)
        self.__downReleased()

    def __upPressed(self):
        self.notify.debug('up pressed')
        self.upPressed = self.__enterControlActive(self.upPressed)

    def __downPressed(self):
        self.notify.debug('down pressed')
        self.downPressed = self.__enterControlActive(self.downPressed)

    def __leftPressed(self):
        self.notify.debug('left pressed')
        self.leftPressed = self.__enterControlActive(self.leftPressed)

    def __rightPressed(self):
        self.notify.debug('right pressed')
        self.rightPressed = self.__enterControlActive(self.rightPressed)

    def __upReleased(self):
        self.notify.debug('up released')
        self.upPressed = self.__exitControlActive(self.upPressed)

    def __downReleased(self):
        self.notify.debug('down released')
        self.downPressed = self.__exitControlActive(self.downPressed)

    def __leftReleased(self):
        self.notify.debug('left released')
        self.leftPressed = self.__exitControlActive(self.leftPressed)

    def __rightReleased(self):
        self.notify.debug('right released')
        self.rightPressed = self.__exitControlActive(self.rightPressed)

    def __firePressed(self):
        self.notify.debug('fire pressed')
        messenger.send(CannonGui.FIRE_PRESSED)

    def __enterControlActive(self, control):
        return control + 1

    def __exitControlActive(self, control):
        return max(0, control - 1)
