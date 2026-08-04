from panda3d.core import TextNode
from direct.gui.DirectGui import DirectFrame, DGG, DirectButton, DirectEntry

from decimal import *
import re

from panda3d.core import TextNode
from direct.gui.DirectGui import DirectLabel


class TTLabel(DirectLabel):
    TitleSize = 5
    GiantSize = 4
    LargeSize = 3
    MediumSize = 2
    NormalSize = 1
    SmallSize = 0
    Scales = {
        TitleSize: 0.12,
        GiantSize: 0.1,
        LargeSize: 0.072,
        MediumSize: 0.062,
        NormalSize: 0.052,
        SmallSize: 0.035
    }

    def __init__(self, parent=None, text_size=1, pos=(0.0, 0.0, 0.0), text_align=TextNode.ACenter, text_wordwrap=16, text='', **kw):
        scale = self.Scales.get(text_size, self.Scales[self.NormalSize])

        optiondefs = (
            ('relief', None, None),
            ('pos', pos, None),
            ('text_scale', scale, None),
            ('text_wordwrap', text_wordwrap, None),
            ('text', text, None),
            ('text_align', text_align, TextNode.ACenter)
        )

        self.defineoptions(kw, optiondefs)
        DirectLabel.__init__(self, parent or aspect2d)
        self.initialiseoptions(TTLabel)



class PlacerTool3D(DirectFrame):
    ORIGINAL_SCALE = (1.0, 1.0, 1.0)
    MINIMIZED_SCALE = (0.85, 1.0, 0.15)
    ORIG_DRAG_BUTTON_POS = (0.37, 0.0, 0.37)
    MINI_DRAG_BUTTON_POS = (0.37, 0.0, 0.03)
    ORIG_MINI_BUTTON_POS = (0.29, 0.0, 0.37)
    MINI_MINI_BUTTON_POS = (0.29, 0.0, 0.03)
    ORIG_NAME_POS = (-0.39, 0.0, 0.27)
    MINI_NAME_POS = (-0.39, 0.0, 0.0)

    def __init__(self, target, increment=0.01, hprIncrement=1.0, parent=None, pos=(0.0, 0.0, 0.0)):
        DirectFrame.__init__(self, parent or aspect2d)
        self.target = target
        self.increment = increment
        self.minimized = False
        self.mainFrame = DirectFrame(
            parent=self,
            relief=None,
            geom=DGG.getDefaultDialogGeom(),
            geom_color=(1, 1, 0.75, 1),
            geom_scale=self.ORIGINAL_SCALE,
            pos=pos,
        )
        # Arrow gui (preload)
        gui = loader.loadModel('phase_3/models/gui/tt_m_gui_mat_mainGui.bam')
        # Set Bins
        self.mainFrame.setBin('gui-popup', 0)
        # Name
        name = self.target.getName()
        self.nameLabel = TTLabel(
            self.mainFrame, text='Target: %s' % name, pos=self.ORIG_NAME_POS, text_align=TextNode.ALeft, text_wordwrap=13)
        # Pos
        pos = self.target.getPos()
        self.posLabel = TTLabel(
            self.mainFrame, text='Position: ', pos=(-0.39, 0.0, 0.055), text_align=TextNode.ALeft)
        self.xPosSpinner = PlacerToolSpinner(
            self.mainFrame, value=pos[0], pos=(-0.085, 0.0, 0.06), increment=increment, callback=self.handleXChange)
        self.yPosSpinner = PlacerToolSpinner(
            self.mainFrame, value=pos[1], pos=(0.1, 0.0, 0.06), increment=increment, callback=self.handleYChange)
        self.zPosSpinner = PlacerToolSpinner(
            self.mainFrame, value=pos[2], pos=(0.28, 0.0, 0.06), increment=increment, callback=self.handleZChange)
        # hpr
        hpr = self.target.getHpr()
        self.hprLabel = TTLabel(
            self.mainFrame, text='HPR: ', pos=(-0.39, 0.0, -0.19), text_align=TextNode.ALeft)
        self.hSpinner = PlacerToolSpinner(
            self.mainFrame, value=hpr[0], pos=(-0.085, 0.0, -0.195), increment=hprIncrement, callback=self.handleHChange)
        self.pSpinner = PlacerToolSpinner(
            self.mainFrame, value=hpr[1], pos=(0.1, 0.0, -0.195), increment=hprIncrement, callback=self.handlePChange)
        self.rSpinner = PlacerToolSpinner(
            self.mainFrame, value=hpr[2], pos=(0.28, 0.0, -0.195), increment=hprIncrement, callback=self.handleRChange)
        # scale
        scale = [round(s, 3) for s in self.target.getScale()]
        self.scaleLabel = TTLabel(
            self.mainFrame, text='Scale: ', pos=(-0.39, 0.0, -0.4), text_align=TextNode.ALeft)

        self.sxSpinner = PlacerToolSpinner(
            self.mainFrame, value=hpr[0], pos=(-0.085, 0.0, -0.4), increment=increment, callback=self.handleSxChange)
        self.sySpinner = PlacerToolSpinner(
            self.mainFrame, value=hpr[1], pos=(0.1, 0.0, -0.4), increment=increment, callback=self.handleSyChange)
        self.szSpinner = PlacerToolSpinner(
            self.mainFrame, value=hpr[2], pos=(0.28, 0.0, -0.4), increment=increment, callback=self.handleSzChange)

        gui.removeNode()
        gui = loader.loadModel('phase_3/models/gui/tt_m_gui_mat_nameShop')
        thumb = gui.find('**/tt_t_gui_mat_namePanelCircle')
        self.dragButton = DirectButton(
            self.mainFrame,
            relief=None,
            image=thumb,
            image_scale=(0.5, 0.5, 0.5),
            pos=self.ORIG_DRAG_BUTTON_POS
        )
        self.minimizeButton = DirectButton(
            self.mainFrame,
            relief=None,
            image=thumb,
            image_scale=(0.5, 0.5, 0.5),
            image_color=(0.0, 0.0, 0.65, 1.0),
            pos=self.ORIG_MINI_BUTTON_POS,
            command=self.toggleMinimize,
            extraArgs=[]
        )
        self.dragButton.bind(DGG.B1PRESS, self.onPress)
        self.dragButton.bind(DGG.B1RELEASE, self.onRelease)
        if target is not None:
            self.setTarget(target)

    def destroy(self):
        self.target = None
        messenger.send('placer-destroyed', [self])
        DirectFrame.destroy(self)

    def setTarget(self, target):
        self.target = target
        name = self.target.getName()
        scale = [round(s, 3) for s in self.target.getScale()]
        x, y, z = self.target.getPos()
        h, p, r = self.target.getHpr()
        sx, sy, sz = self.target.getScale()
        self.nameLabel['text'] = 'Target: %s' % name
        self.xPosSpinner.setValue(x)
        self.yPosSpinner.setValue(y)
        self.zPosSpinner.setValue(z)
        self.hSpinner.setValue(h)
        self.pSpinner.setValue(p)
        self.rSpinner.setValue(r)
        self.sxSpinner.setValue(sx)
        self.sySpinner.setValue(sy)
        self.szSpinner.setValue(sz)

    def handleXChange(self, value):
        self.changeTargetPos(0, value)

    def handleYChange(self, value):
        self.changeTargetPos(1, value)

    def handleZChange(self, value):
        self.changeTargetPos(2, value)

    def handleHChange(self, value):
        self.changeTargetHpr(0, value)

    def handlePChange(self, value):
        self.changeTargetHpr(1, value)

    def handleRChange(self, value):
        self.changeTargetHpr(2, value)

    def handleSxChange(self, value):
        self.changeTargetScale(0, value)

    def handleSyChange(self, value):
        self.changeTargetScale(1, value)

    def handleSzChange(self, value):
        self.changeTargetScale(2, value)

    def changeTargetPos(self, index, value):
        pos = self.target.getPos()
        pos[index] = float(value)
        self.target.setPos(pos)

    def changeTargetHpr(self, index, value):
        hpr = self.target.getHpr()
        hpr[index] = float(value)
        self.target.setHpr(hpr)

    def changeTargetScale(self, index, value):
        pos = self.target.getScale()
        pos[index] = float(value)
        self.target.setScale(pos)

    def toggleMinimize(self):
        if self.minimized:
            self.maximize()
        else:
            self.minimize()

    def minimize(self):
        self.minimized = True
        self.mainFrame['geom_scale'] = self.MINIMIZED_SCALE
        self.nameLabel.setPos(self.MINI_NAME_POS)
        self.dragButton.setPos(self.MINI_DRAG_BUTTON_POS)
        self.minimizeButton.setPos(self.MINI_MINI_BUTTON_POS)
        self.posLabel.hide()
        self.xPosSpinner.hide()
        self.yPosSpinner.hide()
        self.zPosSpinner.hide()
        self.hprLabel.hide()
        self.hSpinner.hide()
        self.pSpinner.hide()
        self.rSpinner.hide()
        self.scaleLabel.hide()
        self.setPos(0, 0, 0)

    def maximize(self):
        self.minimized = False
        self.mainFrame['geom_scale'] = self.ORIGINAL_SCALE
        self.nameLabel.setPos(self.ORIG_NAME_POS)
        self.dragButton.setPos(self.ORIG_DRAG_BUTTON_POS)
        self.minimizeButton.setPos(self.ORIG_MINI_BUTTON_POS)
        self.posLabel.show()
        self.xPosSpinner.show()
        self.yPosSpinner.show()
        self.zPosSpinner.show()
        self.hprLabel.show()
        self.hSpinner.show()
        self.pSpinner.show()
        self.rSpinner.show()
        self.scaleLabel.show()
        self.setPos(0, 0, 0)

    def onPress(self, *args):
        taskMgr.add(self.mouseMoverTask, '%s-mouseMoverTask' % self.id)

    def onRelease(self, *args):
        taskMgr.remove('%s-mouseMoverTask' % self.id)

    def mouseMoverTask(self, task):
        if base.mouseWatcherNode.hasMouse():
            mpos = base.mouseWatcherNode.getMouse()
            buttonPos = self.dragButton.getPos()
            newPos = (mpos[0] - buttonPos[0]/2 - 0.02, 0, mpos[1] - buttonPos[2])
            self.setPos(render2d, newPos)
        return task.cont


class PlacerToolSpinner(DirectFrame):
    def __init__(self, parent=None, pos=(0.0, 0.0, 0.0), scale=1.0, value=0, callback=None, increment=0.01):
        DirectFrame.__init__(self, parent or render2d, pos=pos, scale=1.0)
        self.increment = increment
        self.value = Decimal(value)
        self.callback = callback

        self.display = DirectEntry(
            parent=self,
            relief=None,
            initialText="%.2f" % value,
            scale=1,
            text_scale=0.055,
            text_align=TextNode.ACenter,
            pos=(0.0, 0.0, 0.0),
            frameColor=(0.8, 0.8, 0.5, 1),
            borderWidth=(0.1, 0.1),
            numLines=1,
            width=6,
            frameSize=(-0.1, 0.1, -0.1, 0.1),
            cursorKeys=1
        )
        self.display.bind(DGG.TYPE, self.typeCallback)
        # This allows the text box to handle mouse events
        self.display.guiItem.setActive(True)

        gui = loader.loadModel('phase_3/models/gui/tt_m_gui_mat_mainGui.bam')
        image = (
            gui.find('**/tt_t_gui_mat_shuffleArrowUp'),
            gui.find('**/tt_t_gui_mat_shuffleArrowDown'),
            gui.find('**/tt_t_gui_mat_shuffleArrowUp'),
            gui.find('**/tt_t_gui_mat_shuffleArrowDisabled')
        )
        self.upArrow = DirectButton(self,
            relief=None,
            image=image,
            image_scale=(0.6, 0.6, 0.6),
            image1_scale=(0.7, 0.7, 0.7),
            image2_scale=(0.7, 0.7, 0.7),
            pos=(0.0, 0.0, 0.08),
            command=self.__handleUpClicked
        )
        self.upArrow.setR(90)
        self.downArrow = DirectButton(
            self,
            relief=None,
            image=image,
            image_scale=(0.6, 0.6, 0.6),
            image1_scale=(0.7, 0.7, 0.7),
            image2_scale=(0.7, 0.7, 0.7),
            pos=(0.0, 0.0, -0.05),
            command=self.__handleDownClicked
        )
        self.downArrow.setR(-90)

    def typeCallback(self, e):
        if self.display is None:
            return
        value = self.display.get()
        value = re.sub("[^0-9\.-]", "", value)
        if value == '':
            value = '000.00'
        elif value == '-':
            return
        if '.' not in value:
            try:
                value = int(value)
            except:
                return
        else:
            try:
                value = '%.2f' % float(value)
            except:
                return
        self.setValue(value)

    def setValue(self, value):
        getcontext().prec = 2
        self.value = Decimal(value)
        self.display.enterText('%.2f' % float(value))
        if self.callback:
            self.callback(self.value)

    def __handleUpClicked(self):
        getcontext().prec = 2
        self.setValue(float(self.value) + float(self.increment))

    def __handleDownClicked(self):
        getcontext().prec = 2
        self.setValue(float(self.value) - float(self.increment))
