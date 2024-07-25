from direct.directnotify import DirectNotifyGlobal
from direct.gui.DirectGui import *
from direct.task.Task import Task
from direct.task.TaskManagerGlobal import taskMgr

from toontown.battle import BattleProps
from toontown.suit.Suit import Suit
from toontown.suit.SuitAvatarPanel import SuitAvatarPanel
from toontown.battle.SuitBattleGlobals import *
from toontown.toonbase.ToontownBattleGlobals import *


class TownBattleSuitPanel(DirectFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory('TownBattleSuitPanel')

    def __init__(self, id):
        gui = loader.loadModel('phase_3.5/models/gui/battle_gui')
        DirectFrame.__init__(self, relief=None, image=gui.find('**/ToonBtl_Status_BG'),
                             image_color=Vec4(0.7, 0.7, 0.7, 0.8))
        self.hpText = DirectLabel(parent=self, text='', pos=(-0.06, 0, -0.0325), text_scale=0.045)
        self.setScale(0.8)
        self.initialiseoptions(TownBattleSuitPanel)

        if not base.colorBlindMode:
            self.healthColors = Suit.healthColors
            self.healthGlowColors = Suit.healthGlowColors
        else:
            self.healthColors = Suit.healthColorsAccess
            self.healthGlowColors = Suit.healthGlowColorsAccess

        self.hidden = False
        self.cog = None
        self.isLoaded = 0
        self.notify.info("Loading Suit Battle Panel!")
        self.healthText = DirectLabel(parent=self, text='', pos=(0, 0, -0.075), text_scale=0.05)
        healthGui = loader.loadModel('phase_3.5/models/gui/matching_game_gui')
        button = healthGui.find('**/minnieCircle')
        button.setScale(0.5)
        button.setH(180)
        if not base.colorBlindMode:
            button.setColor(Vec4(0.2, 1, 0, 1))
        else:
            button.setColor(Vec4(0, 0.8, 0, 1))
        self.accept('inventory-levels', self.__handleToggle)
        self.healthNode = self.attachNewNode('health')
        self.healthNode.setPos(-0.06, 0, 0.05)
        button.reparentTo(self.healthNode)
        glow = BattleProps.globalPropPool.getProp('glow')
        glow.reparentTo(button)
        glow.setScale(0.28)
        glow.setPos(-0.005, 0.01, 0.015)
        if not base.colorBlindMode:
            glow.setColor(Vec4(0.25, 1, 0.25, 0.5))
        else:
            glow.setColor(Vec4(0.2, 0.8, 0, 1))
        self.button = button
        self.glow = glow
        self.head = None
        self.hide()
        healthGui.removeNode()
        gui.removeNode()

    def setCogInformation(self, cog):
        self.cog = cog
        self.updateHealthBar()
        if self.head:
            self.head.removeNode()

        self.head = self.attachNewNode('head')
        for part in cog.headParts:
            copyPart = part.copyTo(self.head)
            copyPart.setDepthTest(1)
            copyPart.setDepthWrite(1)

        p1, p2 = Point3(), Point3()
        self.head.calcTightBounds(p1, p2)
        d = p2 - p1
        biggest = max(d[0], d[1], d[2])
        s = 0.1 / biggest
        self.head.setPosHprScale(0.1, 0, 0.01, 180, 0, 0, s, s, s)
        self.setLevelText(cog)

    def setLevelText(self, cog):
        if cog.getSkeleRevives() > 0:
            self.healthText['text'] = TTLocalizer.TownBattleSuitLevelAndRevive % {
                'level': (self.cog.getActualLevel()),
                'revives': SuitAvatarPanel.getRevives(self.cog) + 1
            }
        else:
            self.healthText['text'] = TTLocalizer.TownBattleSuitLevel % {
                'level': (self.cog.getActualLevel()),
            }

    def updateHealthBar(self):

        condition = self.cog.healthCondition
        taskMgr.remove(self.uniqueName('blink-task'))

        if condition == 4:
            blinkTask = Task.loop(Task(self.__blinkRed), Task.pause(0.75), Task(self.__blinkGray), Task.pause(0.1))
            taskMgr.add(blinkTask, self.uniqueName('blink-task'))

        elif condition == 5:
            taskMgr.remove(self.uniqueName('blink-task'))
            blinkTask = Task.loop(Task(self.__blinkRed), Task.pause(0.25), Task(self.__blinkGray), Task.pause(0.1))
            taskMgr.add(blinkTask, self.uniqueName('blink-task'))
        else:
            if not self.button.isEmpty():
                self.button.setColor(self.healthColors[condition], 1)

            if not self.glow.isEmpty():
                self.glow.setColor(self.healthGlowColors[condition], 1)

        self.hp = self.cog.getHP()
        self.maxHp = self.cog.getMaxHP()
        self.hpText['text'] = str(self.hp) + '/' + str(self.maxHp)

    def show(self):
        if self.cog:
            try:
                self.updateHealthBar()
            except:
                pass
        self.hidden = False
        self.healthNode.show()
        self.button.show()
        self.glow.show()
        DirectFrame.show(self)

    def __handleToggle(self):
        if self.cog:
            if self.hidden:
                self.show()
            else:
                self.hide()

    def __blinkRed(self, task):
        if not self.button.isEmpty():
            self.button.setColor(self.healthColors[3], 1)

        if not self.glow.isEmpty():
            self.glow.setColor(self.healthGlowColors[3], 1)

        return Task.done

    def __blinkGray(self, task):
        if not self.button.isEmpty():
            self.button.setColor(self.healthColors[4], 1)

        if not self.glow.isEmpty():
            self.glow.setColor(self.healthGlowColors[4], 1)

        return Task.done

    def hide(self):
        taskMgr.remove(self.uniqueName('blink-task'))

        self.hidden = True
        self.healthNode.hide()
        self.button.hide()
        self.glow.hide()
        DirectFrame.hide(self)

    def unload(self):
        if self.isLoaded == 0:
            return
        self.isLoaded = 0
        self.exit()
        del self.glow
        del self.cog
        del self.button
        del self.hpText
        DirectFrame.destroy(self)

    def cleanup(self):
        self.ignoreAll()
        if self.head:
            self.head.removeNode()
            del self.head

        taskMgr.remove(self.uniqueName('blink-task'))

        self.healthNode.removeNode()
        self.button.removeNode()
        self.glow.removeNode()
        DirectFrame.destroy(self)
