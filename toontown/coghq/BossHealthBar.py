from direct.gui.DirectGui import *
from panda3d.core import *

from otp.otpbase import OTPGlobals
from toontown.suit.Suit import *
from direct.task.Task import Task
from direct.interval.IntervalGlobal import *


class BossHealthBar:

    bossBarColors = (
        Vec4(.25, .7, .25, 0.9),
        Vec4(.7, .7, .4, 0.9),
        Vec4(.8, 0.65, 0.2, 0.9),
        Vec4(.65, .2, .2, 0.9),
        Vec4(0.2, 0.2, 0.2, 0.9)
        )

    colorThresholds = (0.75, 0.5, 0.25, 0.1, 0.05)
    bossBarStartPosZ = 1.5
    bossBarEndPosZ = 0.88
    bossBarIncrementAmt = 2

    def __init__(self, dept):
        self.dept = dept
        self.bossBarFrameBg = loader.loadTexture('phase_9/maps/HealthBarBosses.png')
        self.bossBarFrame = DirectFrame(pos=(1, 0, self.bossBarEndPosZ), scale=1.8*0.8, sortOrder=20)
        self.gui = loader.loadModel('phase_9/models/gui/HealthBarBosses')
        self.gui.setScale(1, 1, .75)
        self.gui.setColorScale(.4, .4, .4, 1)
        self.gui.setTexture(self.bossBarFrameBg)
        self.gui.setTransparency(1)
        self.damageBar = DirectWaitBar(relief=None, scale=(0.195, 0, 0.077), value=100, pos=(-0.005, 0, 0.0015), frameSize=(-2.0, 2.0, -0.2, 0.2), borderWidth=(0.005, 0.005), range=100, sortOrder=50, frameColor=(0.1, 0.1, 0.1, .9), barColor=(0.5, 0.5, .5, 0.6))
        self.bossBar = DirectWaitBar(relief=None, scale=(0.195, 0, 0.077), value=100, pos=(-0.005, 0, 0.0015), frameSize=(-2.0, 2.0, -0.2, 0.2), borderWidth=(0.005, 0.005), range=100, sortOrder=100, frameColor=(0.1, 0.1, 0.1, .9), barColor=(0.2, 0.2, .9, 0.95), text='0 / 0', text_scale=(0.14, 0.30), text_fg=(.9, .9, .9, 1), text_align=TextNode.ACenter, text_pos=(0, -0.12), text_shadow=(0, 0, 0, 1), text_font=ToontownGlobals.getMinnieFont())
        self.gui.hide()
        self.bossBar.hide()
        self.damageBar.hide()
        self.gui.reparentTo(self.bossBarFrame)
        self.bossBar.reparentTo(self.bossBarFrame)
        self.damageBar.reparentTo(self.bossBarFrame)

        self.healthCondition = 0
        self.currHp = 0
        self.newHp = 0
        self.maxHp = 0
        self.healthRatio = 0
        self.isUpdating = False
        self.isBlinking = False
        
        self.stunCountText = None
        self.damageDealtText = None
        self.speedDamageDealtText = None
        self.goonsStompedText = None
        self.damageDealt = 0
        self.speedDamageDealt = 0
        self.stunCount = 0
        self.goonsStomped = 0

        self.drainIval = None


    def initialize(self, hp, maxhp):
        self.maxHp = maxhp
        self.newHp = hp
        self.currHp = hp
        self.bossBar['text'] = ('%s / %s' % (str(hp), str(maxhp)))
        self.bossBar['range'] = maxhp
        self.bossBar['value'] = hp
        self.damageBar['range'] = maxhp
        self.damageBar['value'] = hp
        self.__checkUpdateColor(self.__updateCondition(hp, maxhp))
        self.bossBar.show()
        self.damageBar.show()
        self.gui.show()
        self.damageDealtText = OnscreenText(parent=self.bossBarFrame, text='Damage Dealt: ' + str(self.damageDealt), style=3, fg=(.9, .9, .9, .85), align=TextNode.ARight, scale=0.04, pos=(0.40, -0.19))
        self.stunCountText = OnscreenText(parent=self.bossBarFrame, text='Stuns: ' + str(self.stunCount), style=3, fg=(.9, .9, .9, .85), align=TextNode.ARight, scale=0.04, pos=(0.40, -0.24))
        if self.dept == 'c':
            self.speedDamageDealtText = OnscreenText(parent=self.bossBarFrame, text='Golf: ' + str(self.speedDamageDealt), style=3, fg=(.9, .9, .9, .85), align=TextNode.ARight, scale=0.04, pos=(0.40, -0.29))
        if self.dept == 'm':
            self.goonsStompedText = OnscreenText(parent=self.bossBarFrame, text='Goons Stomped: ' + str(self.speedDamageDealt), style=3, fg=(.9, .9, .9, .85), align=TextNode.ARight, scale=0.04, pos=(0.40, -0.29))
        Sequence(self.bossBarFrame.posInterval(1.0, Point3(1, 0, self.bossBarEndPosZ), blendType='easeOut')).start()

    def update(self, hp, maxHp):

        if not self.bossBar:
            return

        taskMgr.remove('drain-damage-bar-task')
        # Instantly set the hp bar, but queue up the damage bar to go down
        self.bossBar['value'] = hp
        self.bossBar['text'] = '%s / %s' % (str(hp), str(maxHp))
        cond = self.__updateCondition(hp, maxHp)

        self.__checkUpdateColor(cond)

        # Now handle the bar drain
        if hp < maxHp:
            taskMgr.doMethodLater(2, self.__drainDamageBar, 'drain-damage-bar-task')

    def __updateDrainBar(self, value):
        self.damageBar['value'] = value

    def __finishUpdateDrainBar(self, task=None):
        if self.drainIval:
            self.drainIval.finish()
            self.drainIval = None

    def __drainDamageBar(self, task=None):

        self.__finishUpdateDrainBar()

        start = self.damageBar['value']
        goal = self.bossBar['value']

        # Make the damage bar catch up to the actual bar
        self.drainIval = Sequence(
            LerpFunctionInterval(self.__updateDrainBar, fromData=start, toData=goal, duration=.5),
            Func(self.__finishUpdateDrainBar)
        )
        self.drainIval.start()

    def __updateCondition(self, hp, maxHp):
        self.healthRatio = float(hp) / float(maxHp)
        if self.healthRatio > self.colorThresholds[0]:
            condition = 0
        elif self.healthRatio > self.colorThresholds[1]:
            condition = 1
        elif self.healthRatio > self.colorThresholds[2]:
            condition = 2
        elif self.healthRatio > self.colorThresholds[3]:
            condition = 3
        elif self.healthRatio > self.colorThresholds[4]:
            condition = 4
        else:
            condition = 5

        return condition

    def __checkUpdateColor(self, condition):
            self.__applyNewColor(condition, condition)
            if self.healthCondition != condition:
                if condition == 4:
                    if self.healthCondition == 5:
                        taskMgr.remove('bar-blink-task')
                        self.isBlinking = False
                    blinkTask = Task.loop(Task(self.__blinkRed), Task.pause(0.75), Task(self.__blinkGray), Task.pause(0.1))
                    taskMgr.add(blinkTask, 'bar-blink-task')
                    self.isBlinking = True
                elif condition == 5:
                    if self.healthCondition == 4:
                        taskMgr.remove('bar-blink-task')
                        self.isBlinking = False
                    blinkTask = Task.loop(Task(self.__blinkRed), Task.pause(0.25), Task(self.__blinkGray), Task.pause(0.1))
                    taskMgr.add(blinkTask, 'bar-blink-task')
                    self.isBlinking = True
                else:
                    if self.isBlinking:
                        taskMgr.remove('bar-blink-task')
                        self.isBlinking = False
                self.healthCondition = condition

    def __applyNewColor(self, currColor, condition):
        if self.bossBar:
            if currColor != 3 and currColor != 4 and currColor != 5:
                if self.healthRatio > self.colorThresholds[0]:
                    condition = 0
                elif self.healthRatio > self.colorThresholds[1]:
                    condition = 1
                elif self.healthRatio > self.colorThresholds[2]:
                    condition = 2

                if condition > 0:
                    numeratorRatioAmt = self.colorThresholds[condition - 1]
                else:
                    numeratorRatioAmt = 1
                denominatorRatioAmt = self.colorThresholds[condition]
                numeratorColorAmt = self.bossBarColors[condition]
                denominatorColorAmt = self.bossBarColors[condition + 1]
                currentRatioAmt = numeratorRatioAmt - self.healthRatio
                totalRatioAmt = numeratorRatioAmt - denominatorRatioAmt
                ratioRatio = currentRatioAmt / totalRatioAmt
                differenceColorAmt = denominatorColorAmt - numeratorColorAmt
                ratioColorToAdd = differenceColorAmt * ratioRatio
                totalColorAmt = self.bossBarColors[condition] + ratioColorToAdd
                self.bossBar['barColor'] = totalColorAmt

    def __blinkRed(self, task):
        if self.bossBar:
            self.bossBar['barColor'] = self.bossBarColors[3]
            return Task.done
        else:
            taskMgr.remove('bar-blink-task')

    def __blinkGray(self, task):
        if self.bossBar:
            self.bossBar['barColor'] = self.bossBarColors[4]
            return Task.done
        else:
            taskMgr.remove('bar-blink-task')

    def deinitialize(self):
        pass

    def cleanup(self):
        if self.bossBarFrame:
            self.bossBarFrame.destroy()
            del self.bossBarFrame
            if self.bossBar:
                if self.isUpdating:
                    taskMgr.remove('bar-smooth-update-task')
                self.bossBar.destroy()
                del self.bossBar
                if self.isBlinking:
                    taskMgr.remove('bar-blink-task')
                self.healthCondition = None
            if self.damageBar:
                self.__finishUpdateDrainBar()
                self.damageBar.destroy()
                del self.damageBar
                
    def updateDamageDealt(self, avId, damageDealt):
        if avId == base.localAvatar.doId:
            self.damageDealt += damageDealt
            self.damageDealtText.setText('Damage Dealt: ' + str(self.damageDealt))

    def updateSpeedDamageDealt(self, avId, speedDamageDealt):
        if avId == base.localAvatar.doId:
            self.speedDamageDealt += speedDamageDealt
            self.speedDamageDealtText.setText('Golf: ' + str(self.speedDamageDealt))

    def updateGoonsStomped(self, avId):
        if avId == base.localAvatar.doId:
            self.goonsStomped += 1
            self.goonsStompedText.setText('Goons Stomped: ' + str(self.goonsStomped))

    def updateStunCount(self, avId):
        if avId == base.localAvatar.doId:
            self.stunCount += 1
            self.stunCountText.setText('Stuns: ' + str(self.stunCount))
