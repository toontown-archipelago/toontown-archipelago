from datetime import datetime

from direct.gui.DirectGui import *
from panda3d.core import *

from direct.showbase.DirectObject import DirectObject
from toontown.coghq import CraneLeagueGlobals
from toontown.suit.Suit import *
from direct.task.Task import Task
from direct.interval.IntervalGlobal import *
from toontown.toon import ToonDNA, AccessoryGlobals

from toontown.toon.ToonHead import ToonHead

import random

POINTS_TEXT_SCALE = .09

LABEL_Y_POS = .55

# TEXT COLORS
RED = (1, 0, 0, 1)
GREEN = (0, 1, 0, 1)
GOLD = (1, 235.0 / 255.0, 165.0 / 255.0, 1)
WHITE = (.9, .9, .9, .85)
CYAN = (0, 1, 240.0 / 255.0, 1)


def doGainAnimation(pointText, amount, reason='', localAvFlag=False):
    reasonFlag = len(reason) > 0  # reason flag is true if there is a reason
    pointTextColor = GOLD if localAvFlag else WHITE
    randomRoll = random.randint(5, 15) + 10 if reasonFlag else 5
    textToShow = '+' + str(amount) + ' ' + reason
    popup = OnscreenText(parent=pointText, text=textToShow, style=3, fg=GOLD if reasonFlag else GREEN,
                         align=TextNode.ACenter, scale=.05, pos=(.03, .03), roll=-randomRoll, font=ToontownGlobals.getCompetitionFont())

    def cleanup():
        popup.cleanup()

    # points with a reason go towards the right to see easier
    xOffset = .125 if reasonFlag else .01
    zOffset = .02 if reasonFlag else .055
    reasonTimeAdd = .85 if reasonFlag else 0
    popupStartColor = CYAN if reasonFlag else GREEN
    popupFadedColor = (CYAN[0], CYAN[1], CYAN[2], 0) if reasonFlag else (GREEN[0], GREEN[1], GREEN[2], 0)

    targetPos = Point3(pointText.getX() + xOffset, 0, pointText.getZ() + zOffset)
    startPos = Point3(popup.getX(), popup.getY(), popup.getZ())
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
                    LerpColorScaleInterval(pointText, duration=.25, colorScale=GREEN, startColorScale=pointTextColor,
                                           blendType='easeInOut'),
                ),
                Parallel(
                    LerpScaleInterval(pointText, duration=.25, startScale=1 + .2,
                                      scale=1, blendType='easeInOut'),
                    LerpColorScaleInterval(pointText, duration=.25, startColorScale=GREEN, colorScale=pointTextColor,
                                           blendType='easeInOut')
                )

            )
        ),
        Func(cleanup)
    ).start()


def doLossAnimation(pointText, amount, reason='', localAvFlag=False):
    reasonFlag = True if len(reason) > 0 else False  # reason flag is true if there is a reason
    pointTextColor = GOLD if localAvFlag else WHITE
    randomRoll = random.randint(5, 15) + 15 if reasonFlag else 5
    # points with a reason go towards the right to see easier
    xOffset = .125 if not reasonFlag else .01
    zOffset = .02 if not reasonFlag else .055

    textToShow = str(amount) + ' ' + reason
    popup = OnscreenText(parent=pointText, text=textToShow, style=3, fg=RED, align=TextNode.ACenter, scale=.05,
                         pos=(.03, .03), roll=-randomRoll, font=ToontownGlobals.getCompetitionFont())

    def cleanup():
        popup.cleanup()

    targetPos = Point3(pointText.getX() + xOffset, 0, pointText.getZ() + zOffset)
    startPos = Point3(popup.getX(), popup.getY(), popup.getZ())
    Sequence(
        Parallel(
            LerpColorScaleInterval(popup, duration=2, colorScale=(1, 0, 0, 0), startColorScale=RED,
                                   blendType='easeInOut'),
            LerpPosInterval(popup, duration=2, pos=targetPos, startPos=startPos, blendType='easeInOut'),
            Sequence(
                Parallel(
                    LerpScaleInterval(pointText, duration=.25, scale=1 - .2,
                                      startScale=1, blendType='easeInOut'),
                    LerpColorScaleInterval(pointText, duration=.25, colorScale=RED, startColorScale=pointTextColor,
                                           blendType='easeInOut'),
                ),
                Parallel(
                    LerpScaleInterval(pointText, duration=.25, startScale=1 - .2,
                                      scale=1, blendType='easeInOut'),
                    LerpColorScaleInterval(pointText, duration=.25, startColorScale=RED, colorScale=pointTextColor,
                                           blendType='easeInOut')
                )

            )
        ),
        Func(cleanup)
    ).start()


class CashbotBossScoreboardToonRow(DirectObject):
    INSTANCES = []

    FIRST_PLACE_HEAD_X = -.28
    FIRST_PLACE_HEAD_Y = LABEL_Y_POS - .15
    FIRST_PLACE_TEXT_X = 0

    FRAME_Y_FIRST_PLACE = .4

    PLACE_Y_OFFSET = .15

    # Called when a button on a row is clicked, instance is the actual instance that clicked this
    @classmethod
    def _clicked(cls, instance, _=None):

        # Loop through all instances
        for ins in cls.INSTANCES:
            # Skip the instance that clicked
            if ins is instance:
                continue

            # Another thing was clicked, force spectate to be false
            ins.isBeingSpectated = False

        # Spec
        instance.__attempt_spectate()

    def __init__(self, scoreboard_frame, avId, place=0):

        self.INSTANCES.append(self)

        # 0 based index based on what place they are in, y should be adjusted downwards
        self.place = place
        self.avId = avId
        self.points = 0
        self.frame = DirectFrame(parent=scoreboard_frame)
        self.toon_head = self.createToonHead(avId)
        self.toon_head_button = DirectButton(parent=self.frame, pos=(self.FIRST_PLACE_HEAD_X, 0, .035), scale=.6,
                                             command=CashbotBossScoreboardToonRow._clicked, extraArgs=[self])
        self.toon_head_button.setTransparency(TransparencyAttrib.MAlpha)
        self.toon_head_button.setColorScale(1, 1, 1, 0)
        self.frame.setX(-1.30)
        self.frame.setZ(self.getYFromPlaceOffset(self.FRAME_Y_FIRST_PLACE))
        self.toon_head.reparentTo(self.frame)
        self.toon_head.setPos(self.FIRST_PLACE_HEAD_X, 0, 0)
        self.toon_head.setH(180)
        self.toon_head.startBlink()
        self.points_text = OnscreenText(parent=self.frame, text=str(self.points), style=3, fg=WHITE,
                                        align=TextNode.ACenter, scale=.09, pos=(self.FIRST_PLACE_TEXT_X, 0), font=ToontownGlobals.getCompetitionFont())
        self.combo_text = OnscreenText(parent=self.frame, text='x' + '0', style=3, fg=CYAN, align=TextNode.ACenter,
                                       scale=.055, pos=(self.FIRST_PLACE_HEAD_X + .1, +.06), font=ToontownGlobals.getCompetitionFont())
        self.sad_text = OnscreenText(parent=self.frame, text='SAD!', style=3, fg=RED, align=TextNode.ACenter,
                                     scale=.065, pos=(self.FIRST_PLACE_HEAD_X, 0), roll=-15, font=ToontownGlobals.getCompetitionFont())
        self.combo_text.hide()
        self.sad_text.hide()
        if self.avId == base.localAvatar.doId:
            self.points_text.setColorScale(*GOLD)

        self.sadSecondsLeft = base.boss.ruleset.REVIVE_TOONS_TIME

        self.isBeingSpectated = False

    def __attempt_spectate(self):
        # Is the toon spectating?
        if not base.boss.localToonSpectating:
            return

        # Toon exists?
        t = base.cr.doId2do.get(self.avId)
        if not t:
            return

        # Already spectating?
        if self.isBeingSpectated:
            self.__stop_spectating()
            return

        # Check all the cranes
        crane = None
        for c in base.boss.cranes.values():
            # Our toon is on a crane
            if c.avId == self.avId:
                crane = c
                break

        # Spectate them
        self.__change_camera_angle(t, crane)
        self.isBeingSpectated = True

        # Listen for when the toon hops on/off the crane
        self.accept('crane-enter-exit', self.__change_camera_angle)

    def __change_camera_angle(self, toon, crane, _=None):
        base.localAvatar.stopUpdateSmartCamera()
        base.camera.reparentTo(render)
        # if crane is not None, then parent the camera to the crane, otherwise the toon
        if not crane:

            # Fallback, if toon does not exist then just exit spectate
            if not toon:
                self.__stop_spectating()
                return

            base.camera.reparentTo(toon)
            base.camera.setY(-12)
            base.camera.setZ(5)
            base.camera.setP(-5)
        else:
            base.camera.reparentTo(crane.hinge)
            camera.setPosHpr(0, -20, -5, 0, -20, 0)

    def __stop_spectating(self):
        localAvatar.attachCamera()
        localAvatar.orbitalCamera.start()
        localAvatar.setCameraFov(ToontownGlobals.BossBattleCameraFov)
        base.localAvatar.startUpdateSmartCamera()
        self.isBeingSpectated = False
        # Not spectating anymore, no need to watch for crane events any more
        self.ignore('crane-enter-exit')

    def getYFromPlaceOffset(self, y):
        return y - (self.PLACE_Y_OFFSET * self.place)

    def createToonHead(self, avId):
        head = ToonHead()
        av = base.cr.doId2do[avId]

        head.setupHead(av.style, forGui=1)

        head.setupToonHeadHat(av.getHat(), av.style.head)
        head.setupToonHeadGlasses(av.getGlasses(), av.style.head)

        head.fitAndCenterHead(.15, forGui=1)
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
        self.combo_text.setText('COMBO x0')
        self.combo_text.hide()
        taskMgr.remove('sadtimer-' + str(self.avId))
        self.sad_text.hide()
        self.sad_text.setText('SAD!')

    def cleanup(self):
        self.toon_head.cleanup()
        del self.toon_head
        self.points_text.cleanup()
        del self.points_text
        self.combo_text.cleanup()
        del self.combo_text
        taskMgr.remove('sadtimer-' + str(self.avId))
        self.sad_text.cleanup()
        del self.sad_text
        self.toon_head_button.destroy()
        del self.toon_head_button
        self.INSTANCES.remove(self)

    def show(self):
        self.points_text.show()
        self.toon_head.show()

    def hide(self):
        self.points_text.hide()
        self.toon_head.hide()
        self.combo_text.hide()
        self.sad_text.hide()

    def toonDied(self):
        self.toon_head.sadEyes()
        self.sad_text.show()
        self.sadSecondsLeft = base.boss.ruleset.REVIVE_TOONS_TIME

        if base.boss.ruleset.REVIVE_TOONS_UPON_DEATH:
            taskMgr.remove('sadtimer-' + str(self.avId))
            taskMgr.add(self.__updateSadTimeLeft, 'sadtimer-' + str(self.avId))

    def toonRevived(self):
        self.toon_head.normalEyes()
        self.sad_text.hide()

    def __updateSadTimeLeft(self, task):

        if self.sadSecondsLeft < 0:
            return Task.done

        self.sad_text.setText(str(self.sadSecondsLeft))
        self.sadSecondsLeft -= 1
        task.delayTime = 1
        return Task.again


class CashbotBossScoreboard:

    def __init__(self):

        self.frame = DirectFrame()

        self.toon_text = OnscreenText(parent=self.frame, text='Toon', style=3, fg=(.9, .9, .9, .85),
                                      align=TextNode.ALeft, scale=0.1, pos=(-1.7, LABEL_Y_POS),
                                      font=ToontownGlobals.getCompetitionFont())
        self.pts_text = OnscreenText(parent=self.frame, text='Pts.', style=3, fg=(.9, .9, .9, .85),
                                     align=TextNode.ALeft,
                                     scale=0.1, pos=(-1.4, LABEL_Y_POS), font=ToontownGlobals.getCompetitionFont())
        self.h_divider = OnscreenText(parent=self.frame, text='|', style=3, fg=(.9, .9, .9, .85), align=TextNode.ALeft,
                                      scale=(.1, .5), pos=(-1.35, .5), roll=90)
        self.v_divider = OnscreenText(parent=self.frame, text='|', style=3, fg=(.9, .9, .9, .85), align=TextNode.ALeft,
                                      scale=(.1, 1), pos=(-1.45, -0.1))

        self.rows = {}  # maps avId -> ScoreboardToonRow object

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

    def __addScoreLater(self, avId, amount, task=None):
        self.addScore(avId, amount, reason=CraneLeagueGlobals.LOW_LAFF_BONUS_TEXT, ignoreLaff=True)

    # Positive/negative amount of points to add to a player
    def addScore(self, avId, amount, reason='', ignoreLaff=False):

        # If we don't want to include penalties for low laff bonuses and the amount is negative ignore laff
        if not base.boss.ruleset.LOW_LAFF_BONUS_INCLUDE_PENALTIES and amount <= 0:
            ignoreLaff = True

        # Should we consider a low laff bonus?
        if not ignoreLaff and base.boss.ruleset.WANT_LOW_LAFF_BONUS:
            av = base.cr.doId2do.get(avId)
            if av and av.getHp() <= base.boss.ruleset.LOW_LAFF_BONUS_THRESHOLD:
                taskMgr.doMethodLater(.75, self.__addScoreLater, 'delayedScore',
                                      extraArgs=[avId, int(amount * base.boss.ruleset.LOW_LAFF_BONUS)])

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
            LerpColorScaleInterval(row.combo_text, duration=base.boss.ruleset.COMBO_DURATION, colorScale=(1, 1, 1, 0),
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
