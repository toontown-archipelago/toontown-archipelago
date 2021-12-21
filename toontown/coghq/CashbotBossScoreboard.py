from datetime import datetime

from direct.gui.DirectGui import *
from panda3d.core import *
from toontown.suit.Suit import *
from direct.task.Task import Task
from direct.interval.IntervalGlobal import *

from toontown.toon.ToonHead import ToonHead

import random

POINTS_TEXT_SCALE = .09

LABEL_Y_POS = .55

# TEXT COLORS
RED = (1, 0, 0, 1)
GREEN = (0, 1, 0, 1)
GOLD = (1, float(225) / float(255), float(128) / float(255), 1)
WHITE = (1, 1, 1, 1)

def doGainAnimation(pointText, amount, reason='', localAvFlag=False):
    reasonFlag = True if reason == '' else False

    pointTextColor = GOLD if localAvFlag else WHITE

    randomRoll = random.randint(5, 15) + 10 if not reason else 5

    textToShow = '+' + str(amount) + ' ' + reason
    popup = OnscreenText(parent=pointText, text=textToShow, style=3, fg=GREEN if reasonFlag else GOLD, align=TextNode.ACenter, scale=.042, pos=(.03, .03), roll=-randomRoll)

    def cleanup():
        popup.cleanup()

    xOffset = .065 if reasonFlag else .015

    targetPos = Point3(pointText.getX()+xOffset, 0, pointText.getZ()+.055)
    startPos = Point3(popup.getX(), popup.getY(), popup.getZ())
    Sequence(
        Parallel(
            LerpColorScaleInterval(popup, duration=.5, colorScale=(0, 1, 0, 0), startColorScale=GREEN, blendType='easeInOut'),
            LerpPosInterval(popup, duration=.5, pos=targetPos, startPos=startPos, blendType='easeInOut'),
            Sequence(
                Parallel(
                    LerpScaleInterval(pointText, duration=.25, scale=1 + .15,
                                      startScale=1, blendType='easeInOut'),
                    LerpColorScaleInterval(pointText, duration=.25, colorScale=GREEN, startColorScale=GOLD if localAvFlag else WHITE,
                                           blendType='easeInOut'),
                ),
                Parallel(
                    LerpScaleInterval(pointText, duration=.25, startScale=1 + .15,
                                      scale=1, blendType='easeInOut'),
                    LerpColorScaleInterval(pointText, duration=.25, startColorScale=GREEN, colorScale=GOLD if localAvFlag else WHITE,
                                           blendType='easeInOut')
                )


            )
        ),
        Func(cleanup)
    ).start()


def doLossAnimation(pointText, amount, reason='', localAvFlag=False):

    pointTextColor = GOLD if localAvFlag else WHITE
    randomRoll = random.randint(5, 15) + 10

    textToShow = str(amount) + ' ' + reason
    popup = OnscreenText(parent=pointText, text=textToShow, style=3, fg=RED, align=TextNode.ACenter, scale=.042, pos=(.03, .03), roll=-randomRoll)

    def cleanup():
        popup.cleanup()

    targetPos = Point3(pointText.getX()+.065, 0, pointText.getZ()+.055)
    startPos = Point3(popup.getX(), popup.getY(), popup.getZ())
    Sequence(
        Parallel(
            LerpColorScaleInterval(popup, duration=.5, colorScale=(0, 1, 0, 0), startColorScale=RED, blendType='easeInOut'),
            LerpPosInterval(popup, duration=.5, pos=targetPos, startPos=startPos, blendType='easeInOut'),
            Sequence(
                Parallel(
                    LerpScaleInterval(pointText, duration=.25, scale=1 - .15,
                                      startScale=1, blendType='easeInOut'),
                    LerpColorScaleInterval(pointText, duration=.25, colorScale=RED, startColorScale=GOLD if localAvFlag else WHITE,
                                           blendType='easeInOut'),
                ),
                Parallel(
                    LerpScaleInterval(pointText, duration=.25, startScale=1 - .15,
                                      scale=1, blendType='easeInOut'),
                    LerpColorScaleInterval(pointText, duration=.25, startColorScale=RED, colorScale=GOLD if localAvFlag else WHITE,
                                           blendType='easeInOut')
                )


            )
        ),
        Func(cleanup)
    ).start()

class CashbotBossScoreboardToonRow:

    FIRST_PLACE_HEAD_X = -.28
    FIRST_PLACE_HEAD_Y = LABEL_Y_POS-.15
    FIRST_PLACE_TEXT_X = 0

    FRAME_Y_FIRST_PLACE = .4

    PLACE_Y_OFFSET = .15



    def __init__(self, scoreboard_frame, avId, place=0):

        # 0 based index based on what place they are in, y should be adjusted downwards
        self.place = place
        self.avId = avId
        self.points = 0

        self.toon_head = self.createToonHead(avId)
        self.frame = DirectFrame(parent=scoreboard_frame)
        self.frame.setX(-1.30)
        self.frame.setZ(self.getYFromPlaceOffset(self.FRAME_Y_FIRST_PLACE))
        self.toon_head.reparentTo(self.frame)
        self.toon_head.setPos(self.FIRST_PLACE_HEAD_X, 0, 0)
        self.toon_head.setScale(.1)
        self.toon_head.setH(180)
        self.points_text = OnscreenText(parent=self.frame, text=str(self.points), style=3, fg=GOLD if base.localAvatar.doId == self.avId else WHITE, align=TextNode.ACenter, scale=.09, pos=(self.FIRST_PLACE_TEXT_X, 0))

        self.currHeadAnim = None
        self.currTextAnim = None

    def getYFromPlaceOffset(self, y):
        return y - (self.PLACE_Y_OFFSET*self.place)

    def createToonHead(self, avId):
        head = ToonHead()
        av = base.cr.doId2do[avId]
        head.setupHead(av.style, forGui=1)
        return head

    def addScore(self, amount, reason=''):

        # First update the amount
        old = self.points
        self.points += amount
        self.points_text.setText(str(self.points))

        # find the difference
        diff = self.points - old

        # if we lost points make a red popup, if we gained green popup
        if diff > 0:
            doGainAnimation(self.points_text, diff, localAvFlag=self.avId == base.localAvatar.doId, reason=reason)
        elif diff < 0:
            doLossAnimation(self.points_text, diff, localAvFlag=self.avId == base.localAvatar.doId, reason=reason)

    def updatePosition(self):
        # Move to new position based on place
        oldPos = Point3(self.frame.getX(), self.frame.getY(), self.frame.getZ())
        newPos = Point3(self.frame.getX(), self.frame.getY(), self.getYFromPlaceOffset(self.FRAME_Y_FIRST_PLACE))
        LerpPosInterval(self.frame, duration=1.0, pos=newPos, startPos=oldPos, blendType='easeInOut').start()

    def reset(self):
        self.points = 0
        self.points_text.setText('0')

    def cleanup(self):
        self.toon_head.cleanup()
        del self.toon_head
        self.points_text.cleanup()
        del self.points_text

    def show(self):
        self.points_text.show()
        self.toon_head.show()

    def hide(self):
        self.points_text.hide()
        self.toon_head.hide()



class CashbotBossScoreboard:

    def __init__(self):

        self.frame = DirectFrame()

        self.toon_text = OnscreenText(parent=self.frame, text='Toon', style=3, fg=(1, 1, 1, 1), align=TextNode.ALeft, scale=0.1, pos=(-1.7, LABEL_Y_POS))
        self.pts_text = OnscreenText(parent=self.frame, text='Pts.', style=3, fg=(1, 1, 1, 1), align=TextNode.ALeft,
                                      scale=0.1, pos=(-1.4, LABEL_Y_POS))
        self.h_divider = OnscreenText(parent=self.frame, text='|', style=3, fg=(1, 1, 1, 1), align=TextNode.ALeft, scale=(.1, .5), pos=(-1.35, .5), roll=90)
        self.v_divider = OnscreenText(parent=self.frame, text='|', style=3, fg=(1, 1, 1, 1), align=TextNode.ALeft, scale=(.1, 1), pos=(-1.45, -0.1))

        self.rows = {}   # maps avId -> ScoreboardToonRow object

    def addToon(self, avId):
        if avId not in self.rows:
            self.rows[avId] = CashbotBossScoreboardToonRow(self.frame, avId, len(self.rows))

        if len(self.rows) > 1:
            self.show()

    def clearToons(self):
        for row in self.rows.values():
            row.cleanup()
            del self.rows[row.avId]

        self.hide()

    # Positive/negative amount of points to add to a player
    def addScore(self, avId, amount, reason=''):
        if avId in self.rows:
            self.rows[avId].addScore(amount, reason=reason)
            self.updatePlacements()

    def updatePlacements(self):
        # make a list of all the objects
        rows = [r for r in self.rows.values()]
        # sort it based on how many points they have in descending order
        rows.sort(key=lambda x: x.points, reverse=True)
        # set place
        i = 0
        for r in rows:
            r.place = i
            r.updatePosition()
            i += 1

    def getToons(self):
        return [avId for avId in self.rows.keys()]

    def cleanup(self):

        self.clearToons()

        self.toon_text.cleanup()
        self.pts_text.cleanup()
        self.h_divider.cleanup()
        self.v_divider.cleanup()

    def reset(self):
        for row in self.rows.values():
            row.reset()

        self.updatePlacements()

    def show(self):
        if len(self.rows) > 1:
            self.toon_text.show()
            self.pts_text.show()
            self.h_divider.show()
            self.v_divider.show()
        for row in self.rows.values():
            row.show()

    def hide(self):
        self.toon_text.hide()
        self.pts_text.hide()
        self.h_divider.hide()
        self.v_divider.hide()
        for row in self.rows.values():
            row.hide()

