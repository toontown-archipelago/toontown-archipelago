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

        # Quest ID 0 means the toon wants to cancel their quest choice
        if questId == 0 or questId not in Quests.QuestDict.keys():
            self.air.questManager.avatarCancelled(avId)
            self.cancelChoseQuest(avId)
            return

        # Avatar wants to choose a quest of ID questID, let's verify it
        # We need the following attributes of the quest to assign it
        # questId, rewardId, toNpcId
        questToNpc = Quests.getQuestToNpcId(questId)
        rewardId = Quests.getQuestReward(questId)

        self.air.questManager.avatarChoseQuest(avId, self, questId, rewardId, questToNpc)

    def chooseTrack(self, trackId):
        avId = self.air.getAvatarIdFromSender()
        self.notify.debug('chooseTrack: avatar %s choseTrack %s' % (avId, trackId))

        # Currently, we do not support "choose track" quests in this source
        if trackId == -1 or True:
            self.air.questManager.avatarCancelled(avId)
            self.cancelChoseTrack(avId)
            return

    def sendTimeoutMovie(self, avId=0, task=None):
        self.sendUpdate('setMovie', [NPCToons.QUEST_MOVIE_TIMEOUT,
         self.npcId,
         avId,
         [],
         ClockDelta.globalClockDelta.getRealNetworkTime()])
        self.sendClearMovie(avId, task)
        return Task.done

    def sendClearMovie(self, avId=0, task=None):
        self.sendUpdate('setMovie', [NPCToons.QUEST_MOVIE_CLEAR,
         self.npcId,
         avId,
         [],
         ClockDelta.globalClockDelta.getRealNetworkTime()])
        return Task.done

    def rejectAvatar(self, avId):
        self.sendUpdate('setMovie', [NPCToons.QUEST_MOVIE_REJECT,
         self.npcId,
         avId,
         [],
         ClockDelta.globalClockDelta.getRealNetworkTime()])

    def rejectAvatarTierNotDone(self, avId):
        self.sendUpdate('setMovie', [NPCToons.QUEST_MOVIE_TIER_NOT_DONE,
         self.npcId,
         avId,
         [],
         ClockDelta.globalClockDelta.getRealNetworkTime()])

    def completeQuest(self, avId, questId, rewardId):
        self.sendUpdate('setMovie', [NPCToons.QUEST_MOVIE_COMPLETE,
         self.npcId,
         avId,
         [questId, rewardId, 0],
         ClockDelta.globalClockDelta.getRealNetworkTime()])

    def incompleteQuest(self, avId, questId, completeStatus, toNpcId):
        self.sendUpdate('setMovie', [NPCToons.QUEST_MOVIE_INCOMPLETE,
         self.npcId,
         avId,
         [questId, completeStatus, toNpcId],
         ClockDelta.globalClockDelta.getRealNetworkTime()])

    def assignQuest(self, avId, questId, rewardId, toNpcId):
        if self.questCallback:
            self.questCallback()
        self.sendUpdate('setMovie', [NPCToons.QUEST_MOVIE_ASSIGN,
         self.npcId,
         avId,
         [questId, rewardId, toNpcId],
         ClockDelta.globalClockDelta.getRealNetworkTime()])

    def presentQuestChoice(self, avId, quests):
        flatQuests = []
        for quest in quests:
            flatQuests.extend(quest)

        self.sendUpdate('setMovie', [NPCToons.QUEST_MOVIE_QUEST_CHOICE,
         self.npcId,
         avId,
         flatQuests,
         ClockDelta.globalClockDelta.getRealNetworkTime()])

    def presentTrackChoice(self, avId, questId, tracks):
        self.sendUpdate('setMovie', [NPCToons.QUEST_MOVIE_TRACK_CHOICE,
         self.npcId,
         avId,
         tracks,
         ClockDelta.globalClockDelta.getRealNetworkTime()])

    def cancelChoseQuest(self, avId):
        self.sendUpdate('setMovie', [NPCToons.QUEST_MOVIE_QUEST_CHOICE_CANCEL,
         self.npcId,
         avId,
         [],
         ClockDelta.globalClockDelta.getRealNetworkTime()])

    def cancelChoseTrack(self, avId):
        self.sendUpdate('setMovie', [NPCToons.QUEST_MOVIE_TRACK_CHOICE_CANCEL,
         self.npcId,
         avId,
         [],
         ClockDelta.globalClockDelta.getRealNetworkTime()])

    def setMovieDone(self):
        avId = self.air.getAvatarIdFromSender()
        self.sendClearMovie(avId)
