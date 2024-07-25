import typing

from panda3d.core import *
from . import ShtikerPage
from direct.gui.DirectGui import *
from toontown.quest import Quests
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from toontown.quest import QuestBookPoster
from direct.directnotify import DirectNotifyGlobal

if typing.TYPE_CHECKING:
    from toontown.toonbase.ToonBaseGlobals import *

class QuestPage(ShtikerPage.ShtikerPage):
    notify = DirectNotifyGlobal.directNotify.newCategory('QuestPage')

    def __init__(self):
        ShtikerPage.ShtikerPage.__init__(self)
        self.quests = {0: None,
         1: None,
         2: None,
         3: None,
         4: None,
         5: None,
        }
        self.textRolloverColor = Vec4(1, 1, 0, 1)
        self.textDownColor = Vec4(0.5, 0.9, 1, 1)
        self.textDisabledColor = Vec4(0.4, 0.8, 0.4, 1)
        self.questFrames = []
        return

    def load(self):
        self.title = DirectLabel(parent=self, relief=None, text=TTLocalizer.QuestPageToonTasks, text_scale=0.12, textMayChange=0, pos=(0, 0, 0.6))
        self.loadQuestFrames()
        self.accept('questsChanged', self.updatePage)
        return
    
    def loadQuestFrames(self):
        if base.localAvatar.getQuestCarryLimit() <= 4:
            questFramePlaceList = (
            (-0.45, 0, 0.25, 0, 0, 0),
            (-0.45, 0, -0.35, 0, 0, 0),
            (0.45, 0, 0.25, 0, 0, 0),
            (0.45, 0, -0.35, 0, 0, 0),
            # these are here just to make python happy
            (0, 0, 0, 0, 0, 0), 
            (0, 0, 0, 0, 0, 0)
)
        else:
            questFramePlaceList = (
            (-0.45, 0, 0.35, 0, 0, 0),
            (-0.45, 0, -0.075, 0, 0, 0),
            (0.45, 0, 0.35, 0, 0, 0),
            (0.45, 0, -0.075, 0, 0, 0),
            (-0.45, 0, -0.50, 0, 0, 0),
            (0.45, 0, -0.50, 0, 0, 0),
            )
            
        # clear any existing frames before creating new ones
        for frame in self.questFrames:
            frame.destroy()
        self.questFrames = []

        for i in range(ToontownGlobals.MaxQuestCarryLimit):
            frame = QuestBookPoster.QuestBookPoster(reverse=i in (2, 3, 5), mapIndex=i + 1)
            frame.reparentTo(self)
            frame.setPosHpr(*questFramePlaceList[i])
            if base.localAvatar.getQuestCarryLimit() <= 4:
                frame.setScale(1.06)
            else:
                frame.setScale(0.7)
            self.questFrames.append(frame)

    def acceptOnscreenHooks(self):
        self.accept(ToontownGlobals.QuestsHotkeyOn, self.showQuestsOnscreen)
        self.accept(ToontownGlobals.QuestsHotkeyOff, self.hideQuestsOnscreen)

    def ignoreOnscreenHooks(self):
        self.ignore(ToontownGlobals.QuestsHotkeyOn)
        self.ignore(ToontownGlobals.QuestsHotkeyOff)

    def unload(self):
        self.ignore('questsChanged')
        del self.title
        del self.quests
        del self.questFrames
        loader.unloadModel('phase_3.5/models/gui/stickerbook_gui')
        ShtikerPage.ShtikerPage.unload(self)

    def clearQuestFrame(self, index):
        self.questFrames[index].clear()
        self.quests[index] = None
        return

    def fillQuestFrame(self, questDesc, index):
        self.questFrames[index].update(questDesc)
        self.quests[index] = questDesc

    def getLowestUnusedIndex(self):
        for i in range(ToontownGlobals.MaxQuestCarryLimit):
            if self.quests[i] == None:
                return i

        return -1

    def updatePage(self):
        self.notify.debug('updatePage()')
        newQuests = base.localAvatar.quests
        carryLimit = base.localAvatar.getQuestCarryLimit()
        self.loadQuestFrames()
        for i in range(ToontownGlobals.MaxQuestCarryLimit):
            if i < carryLimit:
                self.questFrames[i].show()
            else:
                self.questFrames[i].hide()

        for index, questDesc in list(self.quests.items()):
            if questDesc is not None and list(questDesc) not in newQuests:
                self.clearQuestFrame(index)

        for questDesc in newQuests:
            newQuestDesc = tuple(questDesc)
            if newQuestDesc not in list(self.quests.values()):
                index = self.getLowestUnusedIndex()
                self.fillQuestFrame(newQuestDesc, index)

        for i, questDesc in self.quests.items():
            if questDesc:
                if self.canDeleteQuest(questDesc):
                    self.questFrames[i].setDeleteCallback(self.__deleteQuest)
                else:
                    self.questFrames[i].setDeleteCallback(None)
                self.questFrames[i].update(questDesc)
            else:
                self.questFrames[i].unbindMouseEnter()
        messenger.send('questPageUpdated')
        return

    def enter(self):
        self.updatePage()
        ShtikerPage.ShtikerPage.enter(self)

    def exit(self):
        ShtikerPage.ShtikerPage.exit(self)

    def showQuestsOnscreenTutorial(self):
        self.setPos(0, 0, -0.2)
        self.showQuestsOnscreen()

    def showQuestsOnscreen(self):

        # Check if there is currently something already displaying in the hotkey interface slot
        if not base.localAvatar.allowOnscreenInterface():
            return

        # We can now own the slot
        base.localAvatar.setCurrentOnscreenInterface(self)
        messenger.send('wakeup')

        for i in range(ToontownGlobals.MaxQuestCarryLimit):
            if hasattr(self.questFrames[i], 'mapIndex'):
                self.questFrames[i].mapIndex.show()

        self.updatePage()
        self.reparentTo(aspect2d)
        self.title.hide()
        self.show()

    def hideQuestsOnscreenTutorial(self):
        self.setPos(0, 0, 0)
        self.hideQuestsOnscreen()

    def hideQuestsOnscreen(self):

        # If the current onscreen interface is not us, don't do anything
        if base.localAvatar.getCurrentOnscreenInterface() is not self:
            return

        base.localAvatar.setCurrentOnscreenInterface(None)  # Free up the on screen interface slot
        for i in range(ToontownGlobals.MaxQuestCarryLimit):
            if hasattr(self.questFrames[i], 'mapIndex'):
                self.questFrames[i].mapIndex.hide()

        self.reparentTo(self.book)
        self.title.show()
        self.hide()

    def canDeleteQuest(self, questDesc):
        return Quests.isQuestJustForFun(questDesc[0], questDesc[3])

    def __deleteQuest(self, questDesc):
        base.localAvatar.d_requestDeleteQuest(questDesc)
