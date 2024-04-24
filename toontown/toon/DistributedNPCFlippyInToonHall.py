from panda3d.core import *
from .DistributedNPCToon import *
from .NPCToons import QUEST_MOVIE_AP_WIN_CONDITION_NOT_MET


class DistributedNPCFlippyInToonHall(DistributedNPCToon):

    def __init__(self, cr):
        DistributedNPCToon.__init__(self, cr)

    def getCollSphereRadius(self):
        return 4

    def handleCollisionSphereEnter(self, collEntry):
        base.cr.playGame.getPlace().fsm.request('quest', [self])
        self.sendUpdate('avatarEnter', [])
        self.nametag3d.setDepthTest(0)
        self.nametag3d.setBin('fixed', 0)
        self.lookAt(base.localAvatar)

    def initPos(self):
        self.clearMat()
        self.setScale(1.25)

    # Called from the ai, the following avId has completed the game, do something for them
    def doToonVictory(self, avId):

        toon: DistributedToon.DistributedToon = base.cr.doId2do.get(avId)
        if not toon:
            return

        isLocalToon = avId == base.localAvatar.doId

        if avId == base.localAvatar.doId:
            self.__doLocalToonVictory()

        fullString = "You have completed your goal!\x07You may now use !release to give the other players in your multi-world the items that you haven't found yet.\x07Thank you for playing!"
        self.setupAvatars(toon)
        self.acceptOnce(self.uniqueName('doneChatPage'), self.finishMovie, extraArgs=[toon, isLocalToon])
        self.clearChat()
        self.setPageChat(toon.doId, 0, fullString, 1)

    def __doLocalToonVictory(self):
        self.setupCamera(None)

    def finishToonVictory(self, toon, isLocalToon, elapsed):
        self.finishMovie(toon, isLocalToon, elapsed)

        if isLocalToon:
            self.__doLocalToonVictory()

    def __doLocalToonRecap(self):
        base.localAvatar.setSystemMessage(0, "TODO add cutscene that shows ur stats or something")
        self.__finishLocalToonRecap()

    def __finishLocalToonRecap(self):
        base.cr.playGame.getPlace().fsm.request('walk')

    def setMovie(self, mode, npcId, avId, quests, timestamp):

        toon = base.cr.doId2do.get(avId)
        if not toon:
            return

        if mode == QUEST_MOVIE_AP_WIN_CONDITION_NOT_MET:
            return self.doVictoryConditionNotMetMovie(toon)

        super().setMovie(mode, npcId, avId, quests, timestamp)

    def doVictoryConditionNotMetMovie(self, toon):
        isLocalToon = toon.doId == base.localAvatar.doId

        win_condition = -1

        if toon.slotData != {}:
            win_condition = toon.slotData['win_condition']
            cog_bosses_required = toon.slotData['cog_bosses_required']
            total_tasks_required = toon.slotData['total_tasks_required']
            hood_tasks_required = toon.slotData['hood_tasks_required']

        fullString = 'It seems like you have not completed your goal yet.\x07'
        if win_condition == 0:
            fullString += 'Once you have defeated ' + str(cog_bosses_required) + ' of the boss cogs at least once'
        elif win_condition == 1:
            fullString += 'Once you have completed ' + str(total_tasks_required) + ' total Toontasks'
        elif win_condition == 2:
            fullString += 'Once you have completed ' + str(hood_tasks_required) + ' Toontasks in each neighborhood'
        else:
            fullString = 'You don\'t have a win condition!\x07Once you\'re connected to a server'

        fullString += ', please come talk to me.\x07Good luck!'

        if isLocalToon:
            self.setupCamera(None)

        self.setupAvatars(toon)
        self.acceptOnce(self.uniqueName('doneChatPage'), self.finishMovie, extraArgs=[toon, isLocalToon])
        self.clearChat()
        self.setPageChat(toon.doId, 0, fullString, 1)
