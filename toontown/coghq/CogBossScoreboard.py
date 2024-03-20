
from direct.gui.DirectGui import *
from panda3d.core import *

from direct.showbase.DirectObject import DirectObject
from toontown.coghq import CraneLeagueGlobals
from toontown.suit.Suit import *
from direct.task.Task import Task
from direct.interval.IntervalGlobal import *

from toontown.toon.ToonHead import ToonHead

import random
import math

POINTS_TEXT_SCALE = .09

LABEL_Y_POS = .55

# TEXT COLORS
RED = (1, 0, 0, 1)
GREEN = (0, 1, 0, 1)
GOLD = (1, 235.0 / 255.0, 165.0 / 255.0, 1)
WHITE = (.9, .9, .9, .85)
CYAN = (0, 1, 240.0 / 255.0, 1)


def doGainAnimation(label, amount, old_amount, new_amount, reason='', localAvFlag=False):
    pointText = label.points_text
    reasonFlag = len(reason) > 0  # reason flag is true if there is a reason
    randomRoll = random.randint(1, 20) + 10 if reasonFlag else 5
    textToShow = '+' + str(amount) + ' ' + reason
    popup = OnscreenText(parent=pointText, text=textToShow, style=3, fg=GOLD if reasonFlag else GREEN,
                         align=TextNode.ACenter, scale=.05, pos=(.03, .03), roll=-randomRoll, font=ToontownGlobals.getCompetitionFont())

    def cleanup():
        popup.cleanup()

    def doTextUpdate(n):
        try:
            pointText.setText(str(int(math.ceil(n))))
        except AttributeError:
            pass  # Monkey fix until i find exact cause

    # points with a reason go towards the right to see easier
    rx = random.random() / 5.0 - .1  # -.1-.1
    rz = random.random() / 10.0  # 0-.1
    xOffset = .125+rx if reasonFlag else .01+(rx/5.0)
    zOffset = .02+rz if reasonFlag else .055+(rz/5.0)
    reasonTimeAdd = .85 if reasonFlag else 0
    popupStartColor = CYAN if reasonFlag else GREEN
    popupFadedColor = (CYAN[0], CYAN[1], CYAN[2], 0) if reasonFlag else (GREEN[0], GREEN[1], GREEN[2], 0)

    targetPos = Point3(pointText.getX() + xOffset, 0, pointText.getZ() + zOffset)
    startPos = Point3(popup.getX(), popup.getY(), popup.getZ())
    label.cancel_inc_ival()

    label.inc_ival = Sequence(
        LerpFunctionInterval(doTextUpdate, fromData=old_amount, toData=new_amount, duration=.5, blendType='easeOut')
    )
    label.inc_ival.start()

    Sequence(
        Parallel(
            LerpColorScaleInterval(popup, duration=.95 + reasonTimeAdd, colorScale=popupFadedColor,
                                   startColorScale=popupStartColor, blendType='easeInOut'),
            LerpPosInterval(popup, duration=.95 + reasonTimeAdd, pos=targetPos, startPos=startPos,
                            blendType='easeInOut'),
            Sequence(
                Parallel(
                    LerpScaleInterval(pointText, duration=.25, scale=1 + .2,
                                      startScale=1, blendType='easeInOut'),
                    LerpColorScaleInterval(pointText, duration=.25, colorScale=GREEN, startColorScale=(1, 1, 1, 1),
                                           blendType='easeInOut'),
                ),
                Parallel(
                    LerpScaleInterval(pointText, duration=.25, startScale=1 + .2,
                                      scale=1, blendType='easeInOut'),
                    LerpColorScaleInterval(pointText, duration=.25, startColorScale=GREEN, colorScale=(1, 1, 1, 1),
                                           blendType='easeInOut')
                )

            )
        ),
        Func(cleanup)
    ).start()


def doLossAnimation(label, amount, old_amount, new_amount, reason='', localAvFlag=False):
    pointText = label.points_text
    reasonFlag = True if len(reason) > 0 else False  # reason flag is true if there is a reason
    randomRoll = random.randint(5, 15) + 15 if reasonFlag else 5

    textToShow = str(amount) + ' ' + reason
    popup = OnscreenText(parent=pointText, text=textToShow, style=3, fg=RED, align=TextNode.ACenter, scale=.05,
                         pos=(.03, .03), roll=-randomRoll, font=ToontownGlobals.getCompetitionFont())

    def cleanup():
        popup.cleanup()

    def doTextUpdate(n):
        try:
            pointText.setText(str(int(n)))
        except AttributeError:
            pass  # Monkey fix until i find out exact cause

    rx = random.random() / 5.0 - .1  # -.1-.1
    rz = random.random() / 10.0  # 0-.1
    xOffset = .125 + rx if reasonFlag else .01 + (rx / 5.0)
    zOffset = .02 + rz if reasonFlag else .055 + (rz / 5.0)
    targetPos = Point3(pointText.getX() + xOffset, 0, pointText.getZ() + zOffset)
    startPos = Point3(popup.getX(), popup.getY(), popup.getZ())
    label.cancel_inc_ival()

    label.inc_ival = Sequence(
        LerpFunctionInterval(doTextUpdate, fromData=old_amount, toData=new_amount, duration=.5, blendType='easeOut')
    )
    label.inc_ival.start()
    Sequence(
        Parallel(
            LerpFunc(doTextUpdate, fromData=old_amount, toData=new_amount, duration=.5, blendType='easeInOut'),
            LerpColorScaleInterval(popup, duration=2, colorScale=(1, 0, 0, 0), startColorScale=RED,
                                   blendType='easeInOut'),
            LerpPosInterval(popup, duration=2, pos=targetPos, startPos=startPos, blendType='easeInOut'),
            Sequence(
                Parallel(
                    LerpScaleInterval(pointText, duration=.25, scale=1 - .2,
                                      startScale=1, blendType='easeInOut'),
                    LerpColorScaleInterval(pointText, duration=.25, colorScale=RED, startColorScale=(1, 1, 1, 1),
                                           blendType='easeInOut'),
                ),
                Parallel(
                    LerpScaleInterval(pointText, duration=.25, startScale=1 - .2,
                                      scale=1, blendType='easeInOut'),
                    LerpColorScaleInterval(pointText, duration=.25, startColorScale=RED, colorScale=(1, 1, 1, 1),
                                           blendType='easeInOut')
                )

            )
        ),
        Func(cleanup)
    ).start()


def getScoreboardTextRow(scoreboard_frame, unique_id, default_text='', frame_color=(.5, .5, .5, .75), isToon=False):
    n = TextNode(unique_id)
    n.setText(default_text)
    n.setAlign(TextNode.ALeft)
    n.setFrameColor(frame_color)
    y_margin_addition = .4 if isToon else 0
    n.setFrameAsMargin(0.4, 0.4, 0.2+y_margin_addition, 0.2+y_margin_addition)
    n.setCardColor(.2, .2, .2, .75)
    n.setCardAsMargin(0.38, 0.38, 0.19, 0.19)
    n.setCardDecal(True)
    n.setShadow(0.05, 0.05)
    n.setShadowColor(0, 0, 0, 1)
    n.setTextColor(.7, .7, .7, 1)
    n.setTextScale(1)
    n.setFont(ToontownGlobals.getCompetitionFont())
    p = scoreboard_frame.attachNewNode(n)
    p.setScale(.05)
    return n, p  # Modify n for actual text properties, p for scale/pos


class CashbotBossScoreboardToonRow(DirectObject):

    FIRST_PLACE_HEAD_X = -.24
    FIRST_PLACE_HEAD_Y = 0.013
    FIRST_PLACE_TEXT_X = 0

    FRAME_X = .31
    FRAME_Y_FIRST_PLACE = -.12

    PLACE_Y_OFFSET = .125

    def __init__(self, scoreboard_frame, avId, place=0):

        DirectObject.__init__(self)

        # 0 based index based on what place they are in, y should be adjusted downwards
        self.place = place
        self.avId = avId
        self.points = 0
        self.damage, self.stuns, self.healing = 0, 0, 0
        self.frame = DirectFrame(parent=scoreboard_frame)
        self.toon_head = self.createToonHead(avId, scale=.125)
        self.frame.setX(self.FRAME_X)
        self.frame.setZ(self.getYFromPlaceOffset(self.FRAME_Y_FIRST_PLACE))
        self.toon_head.reparentTo(self.frame)
        self.toon_head.setPos(self.FIRST_PLACE_HEAD_X, 0, self.FIRST_PLACE_HEAD_Y)
        self.toon_head.setH(180)
        self.toon_head.startBlink()
        self.points_text = OnscreenText(parent=self.frame, text=str(self.points), style=3, fg=WHITE,
                                        align=TextNode.ABoxedCenter, scale=.09, pos=(self.FIRST_PLACE_TEXT_X, 0), font=ToontownGlobals.getCompetitionFont())
        self.combo_text = OnscreenText(parent=self.frame, text='x' + '0', style=3, fg=CYAN, align=TextNode.ACenter,
                                       scale=.055, pos=(self.FIRST_PLACE_HEAD_X + .1, +.055), font=ToontownGlobals.getCompetitionFont())
        self.sad_text = OnscreenText(parent=self.frame, text='SAD!', style=3, fg=RED, align=TextNode.ACenter,
                                     scale=.065, pos=(self.FIRST_PLACE_HEAD_X, 0), roll=-15, font=ToontownGlobals.getCompetitionFont())

        self.extra_stats_text = OnscreenText(parent=self.frame, text='', style=3, fg=WHITE, align=TextNode.ABoxedCenter, scale=.09, pos=(self.FIRST_PLACE_TEXT_X+.47, 0), font=ToontownGlobals.getCompetitionFont())


        self.combo_text.hide()
        self.sad_text.hide()
        if self.avId == base.localAvatar.doId:
            self.points_text['fg'] = GOLD
            self.extra_stats_text['fg'] = GOLD

        self.extra_stats_text.hide()

        self.inc_ival = None

    def getYFromPlaceOffset(self, y):
        return y - (self.PLACE_Y_OFFSET * self.place)

    def createToonHead(self, avId, scale=.15):
        head = ToonHead()
        av = base.cr.doId2do[avId]

        head.setupHead(av.style, forGui=1)

        head.setupToonHeadHat(av.getHat(), av.style.head)
        head.setupToonHeadGlasses(av.getGlasses(), av.style.head)

        head.fitAndCenterHead(scale, forGui=1)
        return head

    def cancel_inc_ival(self):
        if self.inc_ival:
            self.inc_ival.finish()

        self.inc_ival = None

    def addScore(self, amount, reason=''):

        # First update the amount
        old = self.points
        self.points += amount

        # find the difference
        diff = self.points - old

        # if we lost points make a red popup, if we gained green popup
        if diff > 0:
            doGainAnimation(self, diff, old, self.points, localAvFlag=self.avId == base.localAvatar.doId, reason=reason)
        elif diff < 0:
            doLossAnimation(self, diff, old, self.points, localAvFlag=self.avId == base.localAvatar.doId, reason=reason)

    def updatePosition(self):
        # Move to new position based on place
        oldPos = Point3(self.frame.getX(), self.frame.getY(), self.frame.getZ())
        newPos = Point3(self.frame.getX(), self.frame.getY(), self.getYFromPlaceOffset(self.FRAME_Y_FIRST_PLACE))
        LerpPosInterval(self.frame, duration=.5, pos=newPos, startPos=oldPos, blendType='easeInOut').start()

    def updateExtraStatsLabel(self):
        s = '%-7s %-7s %-7s' % (self.damage, self.stuns, self.healing)
        self.extra_stats_text.setText(s)

    def addDamage(self, n):
        self.damage += n
        self.updateExtraStatsLabel()

    def addStun(self):
        self.stuns += 1
        self.updateExtraStatsLabel()

    def addHealing(self, hp):
        self.healing += hp
        self.updateExtraStatsLabel()

    def expand(self):
        self.updateExtraStatsLabel()
        self.extra_stats_text.show()

    def collapse(self):
        self.extra_stats_text.hide()

    def reset(self):
        self.points = 0
        self.damage = 0
        self.stuns = 0
        self.healing = 0
        self.updateExtraStatsLabel()
        self.points_text.setText('0')
        self.combo_text.setText('COMBO x0')
        self.combo_text.hide()
        self.sad_text.hide()
        self.sad_text.setText('SAD!')
        self.cancel_inc_ival()

    def cleanup(self):
        self.toon_head.cleanup()
        del self.toon_head
        self.points_text.cleanup()
        del self.points_text
        self.combo_text.cleanup()
        del self.combo_text
        self.sad_text.cleanup()
        del self.sad_text
        self.extra_stats_text.cleanup()
        del self.extra_stats_text
        self.cancel_inc_ival()
        del self.inc_ival

    def show(self):
        self.frame.show()
        self.points_text.show()
        self.toon_head.show()

    def hide(self):
        self.frame.hide()
        self.extra_stats_text.hide()
        self.points_text.hide()
        self.toon_head.hide()
        self.combo_text.hide()
        self.sad_text.hide()

    def toonDied(self):
        self.toon_head.sadEyes()
        self.sad_text.show()

    def toonRevived(self):
        self.toon_head.normalEyes()
        self.sad_text.hide()


class CogBossScoreboard(DirectObject):

    def __init__(self):
        DirectObject.__init__(self)
        self.frame = DirectFrame(parent=base.a2dLeftCenter)
        self.frame.setPos(.2, 0, .5)

        self.default_row, self.default_row_path = getScoreboardTextRow(self.frame, 'master-row', default_text='%-10s %-7s\0' % ('Toon', 'Pts'))
        self.default_row_path.setScale(.06)

        self.rows = {}  # maps avId -> ScoreboardToonRow object
        self.accept('f1', self._consider_expand)

        self.is_expanded = False

        self.expand_tip = OnscreenText(parent=self.frame, text="Press F1 to show more stats", style=3, fg=WHITE, align=TextNode.ACenter, scale=.05, pos=(0.22, 0.1), font=ToontownGlobals.getCompetitionFont())
        self.expand_tip.hide()

        self.combo_duration = 2.0

    def _consider_expand(self):

        if self.is_expanded:
            self.collapse()
        else:
            self.expand()

    def expand(self):
        self.is_expanded = True
        self.default_row.setText('%-10s %-9s %-7s %-7s %-8s\0' % ('Toon', 'Pts', 'Dmg', 'Stuns', 'Healing'))
        for r in list(self.rows.values()):
            r.expand()

    def collapse(self):
        self.is_expanded = False
        self.default_row.setText('%-10s %-7s\0' % ('Toon', 'Pts'))
        for r in list(self.rows.values()):
            r.collapse()

    def addToon(self, avId):
        if avId not in self.rows:
            self.rows[avId] = CashbotBossScoreboardToonRow(self.frame, avId, len(self.rows))

    def clearToons(self):
        for row in list(self.rows.values()):
            row.cleanup()
            del self.rows[row.avId]

        self.hide()

    # Positive/negative amount of points to add to a player
    def addScore(self, avId, amount, reason=''):

        # If we don't get an integer
        if not isinstance(amount, int):
            raise Exception("amount should be an int! got " + type(amount))

        # If it is 0 (could be set by developer) don't do anything
        if amount == 0:
            return

        if avId in self.rows:
            self.rows[avId].addScore(amount, reason=reason)
            self.updatePlacements()

    def updatePlacements(self):
        # make a list of all the objects
        rows = [r for r in list(self.rows.values())]
        # sort it based on how many points they have in descending order
        rows.sort(key=lambda x: x.points, reverse=True)
        # set place
        i = 0
        for r in rows:
            r.place = i
            r.updatePosition()
            i += 1

    def getToons(self):
        return [avId for avId in list(self.rows.keys())]

    def cleanup(self):

        self.clearToons()

        self.default_row_path.removeNode()
        self.ignore('f1')

    def hide_tip_later(self):
        taskMgr.remove('expand-tip')
        taskMgr.doMethodLater(5.0, self.__hide_tip, 'expand-tip')

    def __hide_tip(self, _=None):
        taskMgr.remove('expand-tip')
        LerpColorScaleInterval(self.expand_tip, 1.0, colorScale=(1, 1, 1, 0), startColorScale=(1, 1, 1, 1), blendType='easeInOut').start()

    def reset(self):
        self.expand_tip.show()
        self.expand_tip.setColorScale(1, 1, 1, 1)
        self.hide_tip_later()
        taskMgr.remove('expand-tip')
        for row in list(self.rows.values()):
            row.reset()

        self.updatePlacements()
        self.collapse()

    def show(self):
        self.frame.show()
        self.expand_tip.show()
        self.expand_tip.setColorScale(1, 1, 1, 1)
        self.hide_tip_later()
        self.default_row_path.show()
        for row in list(self.rows.values()):
            row.show()

        self.collapse()

    def hide(self):
        self.frame.hide()
        self.expand_tip.hide()
        self.default_row_path.hide()
        for row in list(self.rows.values()):
            row.hide()

    # updates combo text
    def setCombo(self, avId, amount):

        row = self.rows.get(avId)
        if not row:
            return

        row.combo_text.setText('x' + str(amount))

        if amount < 2:
            row.combo_text.hide()
            return

        row.combo_text['fg'] = CYAN
        row.combo_text.show()

        Parallel(
            Sequence(
                LerpScaleInterval(row.combo_text, duration=.25, scale=1.07, startScale=1, blendType='easeInOut'),
                LerpScaleInterval(row.combo_text, duration=.25, startScale=1.07, scale=1, blendType='easeInOut')
            ),
            LerpColorScaleInterval(row.combo_text, duration=self.combo_duration, colorScale=(1, 1, 1, 0),
                                   startColorScale=(1, 1, 1, 1))
        ).start()

    def toonDied(self, avId):
        row = self.rows.get(avId)
        if not row:
            return

        row.toonDied()

    def toonRevived(self, avId):
        row = self.rows.get(avId)
        if not row:
            return

        row.toonRevived()

    def addDamage(self, avId, n):
        row = self.rows.get(avId)
        if row:
            row.addDamage(n)

    def addStun(self, avId):
        row = self.rows.get(avId)
        if row:
            row.addStun()

    def addHealing(self, avId, hp):
        row = self.rows.get(avId)
        if row:
            row.addHealing(hp)
