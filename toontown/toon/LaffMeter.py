import random

from panda3d.core import *
from direct.gui.DirectGui import DirectFrame, DirectLabel
from direct.interval.FunctionInterval import Func
from direct.interval.MetaInterval import Sequence, Parallel
from otp.otpbase import OTPGlobals
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import ToontownIntervals


class LaffMeter(DirectFrame):
    deathColor = Vec4(0.58039216, 0.80392157, 0.34117647, 1.0)
    flyoutLabelGenerator = TextNode('flyoutLabelGenerator')

    FRACTIONS = [0.0, 0.166666, 0.333333, 0.5, 0.666666, 0.833333]

    gui = base.loader.loadModel("phase_3/models/gui/laff_o_meter")
    headModels = {
        "dog": gui.find("**/laffMeter_dog"),
        "cat": gui.find("**/laffMeter_cat"),
        "mouse": gui.find("**/laffMeter_mouse"),
        "horse": gui.find("**/laffMeter_horse"),
        "rabbit": gui.find("**/laffMeter_rabbit"),
        "duck": gui.find("**/laffMeter_duck"),
        "monkey": gui.find("**/laffMeter_monkey"),
        "bear": gui.find("**/laffMeter_bear"),
        "pig": gui.find("**/laffMeter_pig"),
        "deer": gui.find("**/laffMeter_deer"),
        "beaver": gui.find("**/laffMeter_beaver"),
        "alligator": gui.find("**/laffMeter_alligator"),
        "fox": gui.find("**/laffMeter_fox"),
        "bat": gui.find("**/laffMeter_bat"),
        "raccoon": gui.find("**/laffMeter_raccoon"),
        "turkey": gui.find("**/laffMeter_turkey"),
        "koala": gui.find("**/laffMeter_koala"),
        "kangaroo": gui.find("**/laffMeter_kangaroo"),
        "kiwi": gui.find("**/laffMeter_kiwi"),
        "armadillo": gui.find("**/laffMeter_armadillo"),
    }
    gui.removeNode()

    def __init__(self, avdna, hp, maxHp):
        DirectFrame.__init__(self, relief=None, sortOrder=50)
        self.teeth = None
        self.hpLabel = None
        self.maxLabel = None
        self.openSmile = None
        self.eyes = None
        self.smile = None
        self.frown = None
        self.initialiseoptions(LaffMeter)
        self.container = DirectFrame(parent=self, relief=None)
        self.style = avdna
        self.av = None
        self.hp = hp
        self.maxHp = maxHp
        self.color = None
        self.__obscured = 0
        if self.style.type == 't':
            self.isToon = 1
        else:
            self.isToon = 0
        self.load()
        self.flashName = None
        self.flashIval = None
        self.flashThreshold = None  # The laff at which the laff meter starts flashing
        self.overhead = False
        return

    def fixOverhead(self):
        self.container.setDepthTest(1)
        self.container.setDepthWrite(1)
        self.container.setY(.01)
        self.frown.setY(-.02)
        self.smile.setY(-.01)
        self.eyes.setY(-.01)
        self.openSmile.setY(-.02)
        self.maxLabel.setY(-.01)
        self.hpLabel.setY(-.01)
        for t in self.teeth:
            t.setY(-.01)

        self.overhead = True

    # Called when we take damage or get laff, makes a number fly out of the meter
    def makeDeltaNumber(self, delta):

        def cleanup(_node):
            _node.removeNode()

        if delta == 0:
            return

        numString = '+' if delta > 0 else ''
        numColor = (0, .9, 0, 1) if delta > 0 else (.9, 0, 0, 1)
        numString += str(delta)

        self.flyoutLabelGenerator.setFont(OTPGlobals.getSignFont())
        self.flyoutLabelGenerator.setText(numString)
        self.flyoutLabelGenerator.clearShadow()
        self.flyoutLabelGenerator.setAlign(TextNode.ACenter)
        self.flyoutLabelGenerator.setTextColor(numColor)
        node = self.flyoutLabelGenerator.generate()
        hptextnode = self.attachNewNode(node)
        hptextnode.setScale(.1)
        hptextnode.setBillboardPointEye()
        if self.overhead:
            hptextnode.setBin('fixed', 100)
        ypos = -1.01 + random.random()  # Used to mitigate z fighting
        hptextnode.setPos(0, ypos, 0)
        hptextnode.setR(9)
        xgoal = random.random() + 1.4
        zgoal = random.random() + 1.4
        sgoal = 1.4
        if self.overhead:
            sgoal *= 1.5
        Sequence(
            Parallel(
                hptextnode.scaleInterval(.2, sgoal),
                hptextnode.posInterval(1.3, Point3(xgoal, ypos, zgoal), blendType='easeInOut'),
                hptextnode.colorScaleInterval(1.3, Vec4(numColor[0], numColor[1], numColor[2], 0))
            ),
            Func(cleanup, hptextnode)
        ).start()

    def setFlashThreshold(self, num):
        self.flashThreshold = num

    def obscure(self, obscured):
        self.__obscured = obscured
        if self.__obscured:
            self.hide()

    def isObscured(self):
        return self.__obscured

    def load(self):

        if not self.isToon:
            return

        gui = loader.loadModel('phase_3/models/gui/laff_o_meter')

        hType = self.style.getType()
        headModel = self.headModels.get(hType)
        if headModel is None:
            raise Exception('unknown toon species: ', hType)

        self.color = self.style.getHeadColor()
        self.container['image'] = headModel
        self.container['image_color'] = self.color
        self.resetFrameSize()
        self.setScale(0.1)
        self.frown = DirectFrame(parent=self.container, relief=None, image=gui.find('**/frown'))
        self.smile = DirectFrame(parent=self.container, relief=None, image=gui.find('**/smile'))
        self.eyes = DirectFrame(parent=self.container, relief=None, image=gui.find('**/eyes'))
        toothScale = (.92, .92, 0.87)
        toothPos = (-0.03, 0.0, -0.33)
        self.openSmile = DirectFrame(parent=self.container, relief=None, image=gui.find('**/open_smile'),
                                     image_pos=(0.0, 0.0, -0.65), image_scale=toothScale)
        tooth1 = DirectFrame(parent=self.openSmile, relief=None, image=gui.find('**/tooth_1'),
                                  image_pos=toothPos, image_scale=toothScale)
        tooth2 = DirectFrame(parent=self.openSmile, relief=None, image=gui.find('**/tooth_2'),
                                  image_pos=toothPos, image_scale=toothScale)
        tooth3 = DirectFrame(parent=self.openSmile, relief=None, image=gui.find('**/tooth_3'),
                                  image_pos=toothPos, image_scale=toothScale)
        tooth4 = DirectFrame(parent=self.openSmile, relief=None, image=gui.find('**/tooth_4'),
                                  image_pos=toothPos, image_scale=toothScale)
        tooth5 = DirectFrame(parent=self.openSmile, relief=None, image=gui.find('**/tooth_5'),
                                  image_pos=toothPos, image_scale=toothScale)
        tooth6 = DirectFrame(parent=self.openSmile, relief=None, image=gui.find('**/tooth_6'),
                                  image_pos=toothPos, image_scale=toothScale)
        self.maxLabel = DirectLabel(parent=self.eyes, relief=None, pos=(0.442, 0, 0.051), text='120',
                                    text_scale=0.4, text_font=ToontownGlobals.getInterfaceFont())
        self.hpLabel = DirectLabel(parent=self.eyes, relief=None, pos=(-0.398, 0, 0.051), text='120',
                                   text_scale=0.4, text_font=ToontownGlobals.getInterfaceFont())

        self.teeth = [tooth6, tooth5, tooth4, tooth3, tooth2, tooth1]

        gui.removeNode()

    def destroy(self):

        if self.av:
            ToontownIntervals.cleanup(self.av.uniqueName('laffMeterBoing') + '-' + str(self.this))
            ToontownIntervals.cleanup(self.av.uniqueName('laffMeterBoing') + '-' + str(self.this) + '-play')
            self.stopFlash()
            self.ignore(self.av.uniqueName('hpChange'))

        del self.style
        del self.av
        del self.hp
        del self.maxHp

        for tooth in self.teeth:
            tooth.destroy()

        if self.isToon:
            del self.frown
            del self.smile
            del self.openSmile
            del self.teeth
            del self.maxLabel
            del self.hpLabel

        super().destroy()

    def adjustTeeth(self):

        if not self.isToon:
            return

        for i, tooth in enumerate(self.teeth):
            if self.hp > self.maxHp * self.FRACTIONS[i]:
                tooth.show()
            else:
                tooth.hide()

    def adjustText(self):

        if not self.isToon:
            return

        if self.maxLabel['text'] != str(self.maxHp) or self.hpLabel['text'] != str(self.hp):
            self.maxLabel['text'] = str(self.maxHp)
            self.hpLabel['text'] = str(self.hp)

    def animatedEffect(self, delta):
        if delta == 0 or self.av is None:
            return

        name = self.av.uniqueName('laffMeterBoing') + '-' + str(self.this)
        ToontownIntervals.cleanup(name)

        if delta > 0:
            ToontownIntervals.start(ToontownIntervals.getPulseLargerIval(self, name))
        else:
            ToontownIntervals.start(ToontownIntervals.getPulseSmallerIval(self, name))

    def startFlash(self):

        if not self.av:
            return

        self.stopFlash()
        self.flashName = self.av.uniqueName('laffMeterFlash')
        self.flashIval = ToontownIntervals.getFlashIval(self, self.flashName)
        ToontownIntervals.loop(self.flashIval)

    def stopFlash(self):

        if not self.flashIval:
            return

        self.flashIval.finish()
        ToontownIntervals.cleanup(self.flashName)
        self.flashIval = None

    def adjustFace(self, hp, maxHp, quietly=0):

        self.stopFlash()
        if self.isToon and self.hp != None:
            self.frown.hide()
            self.smile.hide()
            self.openSmile.hide()
            self.eyes.hide()
            for tooth in self.teeth:
                tooth.hide()

            delta = hp - self.hp
            deltaIgnoringNegative = hp - max(0, self.hp)
            numToShow = deltaIgnoringNegative

            # If laff is negative, and new laff is also negative dont show
            if hp < 0 and self.hp < 0:
                numToShow = 0

            self.makeDeltaNumber(numToShow)

            self.hp = hp
            self.maxHp = maxHp
            if self.hp < 1:
                self.frown.show()
                self.container['image_color'] = self.deathColor
            elif self.hp >= self.maxHp:
                self.smile.show()
                self.eyes.show()
                self.container['image_color'] = self.color
            else:
                self.openSmile.show()
                self.eyes.show()
                self.maxLabel.show()
                self.hpLabel.show()
                self.container['image_color'] = self.color
                self.adjustTeeth()
            self.adjustText()
            if not quietly:
                self.animatedEffect(delta)

            # Flash when low hp but not when dead
            # If there isn't a custom flash threshold set, then use the red teeth as one
            shouldFlash = False
            if self.flashThreshold is not None and self.hp <= self.flashThreshold:
                shouldFlash = True
            elif self.flashThreshold is None and self.hp <= self.maxHp * self.FRACTIONS[1]:
                shouldFlash = True

            # If we are dead we do not flash
            if self.hp <= 0:
                shouldFlash = False

            if shouldFlash:
                self.startFlash()

    def start(self):
        if self.av:
            self.hp = self.av.hp
            self.maxHp = self.av.maxHp
            # self.flashThreshold = self.av.maxHp * .166666
        if self.isToon:
            if not self.__obscured:
                self.show()
            self.adjustFace(self.hp, self.maxHp, 1)
            if self.av:
                self.accept(self.av.uniqueName('hpChange'), self.adjustFace)
                self.accept('uberThreshold', self.setFlashThreshold)

    def stop(self):

        if not self.isToon:
            return

        self.hide()

        if self.av:
            self.ignore(self.av.uniqueName('hpChange'))

    def setAvatar(self, av):

        if self.av:
            self.ignore(self.av.uniqueName('hpChange'))

        self.av = av
        self.flashName = self.av.uniqueName('laffMeterFlash') + '-' + str(self.this)
