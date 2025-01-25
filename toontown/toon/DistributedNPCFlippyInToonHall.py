import typing

from panda3d.core import *
from .DistributedNPCToon import *
from .NPCToons import QUEST_MOVIE_AP_WIN_CONDITION_NOT_MET

if typing.TYPE_CHECKING:
    from toontown.toonbase.ToonBaseGlobals import *


class DistributedNPCFlippyInToonHall(DistributedNPCToon):

    def __init__(self, client_repo):
        DistributedNPCToon.__init__(self, client_repo)

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

        fullString = toon.winCondition.generate_npc_victory_dialogue(delimiter='\x07')
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

    def doVictoryConditionNotMetMovie(self, toon: DistributedToon.DistributedToon):
        isLocalToon = toon.doId == base.localAvatar.doId
        npcDialogue = toon.getWinCondition().generate_npc_dialogue(delimiter='\x07') + '\x07When you finish, come back and see me!\x07Good luck!'
        if isLocalToon:
            self.setupCamera(None)

        self.setupAvatars(toon)
        self.acceptOnce(self.uniqueName('doneChatPage'), self.finishMovie, extraArgs=[toon, isLocalToon])
        self.clearChat()
        self.setPageChat(toon.doId, 0, npcDialogue, 1)
