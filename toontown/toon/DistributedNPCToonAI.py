from otp.ai.AIBaseGlobal import *
from direct.task.Task import Task
from panda3d.core import *
from .DistributedNPCToonBaseAI import *
from toontown.quest import Quests

class DistributedNPCToonAI(DistributedNPCToonBaseAI):
    FourthGagVelvetRopeBan = config.GetBool('want-ban-fourth-gag-velvet-rope', 0)

    def __init__(self, air, npcId, questCallback = None, hq = 0):
        DistributedNPCToonBaseAI.__init__(self, air, npcId, questCallback)
        self.hq = hq
        self.tutorial = 0
        return

    def getTutorial(self):
        return self.tutorial

    def setTutorial(self, val):
        self.tutorial = val

    def getHq(self):
        return self.hq

    def avatarEnter(self):
        avId = self.air.getAvatarIdFromSender()
        self.notify.debug('avatar enter ' + str(avId))
        self.air.questManager.requestInteract(avId, self)
        DistributedNPCToonBaseAI.avatarEnter(self)

    def chooseQuest(self, questId):
        avId = self.air.getAvatarIdFromSender()
        self.notify.debug('chooseQuest: avatar %s choseQuest %s' % (avId, questId))

        if questId <= 0:
            self.air.questManager.avatarCancelled(avId)
            self.cancelChoseQuest(avId)
            return

        self.air.questManager.avatarChoseQuest(avId, self, questId)

    def sendTimeoutMovie(self, avId, task):
        self.sendUpdate('setMovie', [NPCToons.QUEST_MOVIE_TIMEOUT,
         self.npcId,
         avId,
         [],
         ClockDelta.globalClockDelta.getRealNetworkTime()])
        self.sendClearMovie(avId, None)
        return Task.done

    def sendClearMovie(self, avId, task):
        self.sendUpdate('setMovie', [NPCToons.QUEST_MOVIE_CLEAR,
         self.npcId,
         0,
         [],
         ClockDelta.globalClockDelta.getRealNetworkTime()])
        return Task.done

    def rejectAvatar(self, avId):
        self.sendUpdate('setMovie', [NPCToons.QUEST_MOVIE_REJECT,
         self.npcId,
         avId,
         [],
         ClockDelta.globalClockDelta.getRealNetworkTime()])
        if not self.tutorial:
            taskMgr.doMethodLater(5.5, self.sendClearMovie, self.uniqueName('clearMovie'), extraArgs=[avId])

    def completeQuest(self, avId, questId, rewardId):
        self.sendUpdate('setMovie', [NPCToons.QUEST_MOVIE_COMPLETE,
         self.npcId,
         avId,
         [questId, rewardId, 0],
         ClockDelta.globalClockDelta.getRealNetworkTime()])
        if not self.tutorial:
            taskMgr.doMethodLater(60.0, self.sendTimeoutMovie, self.uniqueName('clearMovie'), extraArgs=[avId])

    def incompleteQuest(self, avId, questId, completeStatus, toNpcId):
        self.sendUpdate('setMovie', [NPCToons.QUEST_MOVIE_INCOMPLETE,
         self.npcId,
         avId,
         [questId, completeStatus, toNpcId],
         ClockDelta.globalClockDelta.getRealNetworkTime()])
        if not self.tutorial:
            taskMgr.doMethodLater(60.0, self.sendTimeoutMovie, self.uniqueName('clearMovie'), extraArgs=[avId])

    def assignQuest(self, avId, questId, rewardId, toNpcId):
        if self.questCallback:
            self.questCallback()
        self.sendUpdate('setMovie', [NPCToons.QUEST_MOVIE_ASSIGN,
         self.npcId,
         avId,
         [questId, rewardId, toNpcId],
         ClockDelta.globalClockDelta.getRealNetworkTime()])
        if not self.tutorial:
            taskMgr.doMethodLater(60.0, self.sendTimeoutMovie, self.uniqueName('clearMovie'), extraArgs=[avId])

    def presentQuestChoice(self, avId, quests):
        flatQuests = []
        for quest in quests:
            flatQuests.extend(quest)

        self.sendUpdate('setMovie', [NPCToons.QUEST_MOVIE_QUEST_CHOICE,
         self.npcId,
         avId,
         flatQuests,
         ClockDelta.globalClockDelta.getRealNetworkTime()])
        if not self.tutorial:
            taskMgr.doMethodLater(60.0, self.sendTimeoutMovie, self.uniqueName('clearMovie'), extraArgs=[avId])

    def presentTrackChoice(self, avId, questId, tracks):
        self.sendUpdate('setMovie', [NPCToons.QUEST_MOVIE_TRACK_CHOICE,
         self.npcId,
         avId,
         tracks,
         ClockDelta.globalClockDelta.getRealNetworkTime()])
        if not self.tutorial:
            taskMgr.doMethodLater(60.0, self.sendTimeoutMovie, self.uniqueName('clearMovie'), extraArgs=[avId])

    def cancelChoseQuest(self, avId):
        self.sendUpdate('setMovie', [NPCToons.QUEST_MOVIE_QUEST_CHOICE_CANCEL,
         self.npcId,
         avId,
         [],
         ClockDelta.globalClockDelta.getRealNetworkTime()])
        if not self.tutorial:
            taskMgr.doMethodLater(60.0, self.sendTimeoutMovie, self.uniqueName('clearMovie'), extraArgs=[avId])

    def cancelChoseTrack(self, avId):
        self.sendUpdate('setMovie', [NPCToons.QUEST_MOVIE_TRACK_CHOICE_CANCEL,
         self.npcId,
         avId,
         [],
         ClockDelta.globalClockDelta.getRealNetworkTime()])
        if not self.tutorial:
            taskMgr.doMethodLater(60.0, self.sendTimeoutMovie, self.uniqueName('clearMovie'), extraArgs=[avId])

    def setMovieDone(self):
        avId = self.air.getAvatarIdFromSender()
        self.notify.debug('setMovieDone busy: avId: %s' % avId)
        taskMgr.remove(self.uniqueName('clearMovie'))
        self.sendClearMovie(avId, None)