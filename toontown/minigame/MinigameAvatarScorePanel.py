from direct.gui.DirectGui import *

from toontown.toon import LaffMeter
from toontown.toonbase.ToontownGlobals import *


class MinigameAvatarScorePanel(DirectFrame):
    def __init__(self, avId, avName, avatar=None):
        self.avId = avId

        if avatar is None:
            if self.avId in base.cr.doId2do:
                self.avatar = base.cr.doId2do[self.avId]
            else:
                # Must be a suit
                self.avatar = None
        else:
            self.avatar = avatar

        # initialize our base class.
        DirectFrame.__init__(self,
                             relief=None,
                             image_color=GlobalDialogColor,
                             image_scale=(0.4, 1.0, 0.24),
                             image_pos=(0.0, 0.1, 0.0),
                             )

        # For some reason, we need to set this after construction to
        # get it to work properly.
        self['image'] = DGG.getDefaultDialogGeom()

        # Make a label for showing the score.
        self.scoreText = DirectLabel(self,
                                     relief=None,
                                     text="0",
                                     text_scale=TTLocalizer.MASPscoreText,
                                     pos=(0.1, 0.0, -0.09))

        self.laffMeter = None
        self.suitHead = None

        if avatar is None:
            self.laffMeter = LaffMeter.LaffMeter(self.avatar.style,
                                                 self.avatar.hp,
                                                 self.avatar.maxHp)
            self.laffMeter.reparentTo(self)
            self.laffMeter.setPos(-0.085, 0, -0.035)
            self.laffMeter.setScale(0.05)
            self.laffMeter.start()
        else:
            # Now put the avatar's head in the panel.
            self.suitHead = self.attachNewNode('head')
            for part in avatar.headParts:
                copyPart = part.copyTo(self.suitHead)
                # Turn on depth write and test.
                copyPart.setDepthTest(1)
                copyPart.setDepthWrite(1)
            p1 = Point3()
            p2 = Point3()
            self.suitHead.calcTightBounds(p1, p2)
            d = p2 - p1
            biggest = max(d[0], d[1], d[2])
            s = 0.1 / biggest
            self.suitHead.setPosHprScale(
                -0.085, 0, -0.085,
                180, 0, 0,
                s, s, s)

        # Make a label for showing the avatar's name.  This goes down
        # here at the end, so the name will be on top of the other
        # stuff.
        self.nameText = DirectLabel(self,
                                    relief=None,
                                    text=avName,
                                    text_scale=TTLocalizer.MASPnameText,
                                    text_pos=(0.0, 0.06),
                                    text_wordwrap=7.5,
                                    text_shadow=(1, 1, 1, 1))

        self.show()

    def cleanup(self):
        if self.laffMeter:
            self.laffMeter.destroy()
            del self.laffMeter
        if self.suitHead:
            self.suitHead.removeNode()
            del self.suitHead
        del self.scoreText
        del self.nameText
        self.destroy()

    def setScore(self, score):
        self.scoreText['text'] = str(score)

    def getScore(self):
        return int(self.scoreText['text'])

    def makeTransparent(self, alpha):
        self.setTransparency(1)
        self.setColorScale(1, 1, 1, alpha)
