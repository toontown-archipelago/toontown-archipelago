import random

from direct.fsm import State
from panda3d.core import Point3

from toontown.battle.DistributedBattleBaseAI import DistributedBattleBaseAI
from toontown.suit.DistributedSuitAI import DistributedSuitAI
from toontown.suit.SuitDNA import SuitDNA, getRandomSuitType

from toontown.battle.BattleBase import *
from toontown.toon.DistributedToonAI import DistributedToonAI


# Astron command #s
SET_MIN_LEVEL = 1
SET_MAX_LEVEL = 2


class DistributedBattleSandboxAI(DistributedBattleBaseAI):
    def __init__(self, air, zoneId):
        super().__init__(air, zoneId)

        self.pos = Point3(0, 0, 50)

        self.minLevel: int = 50
        self.maxLevel: int = 50

        self.notify.setDebug(True)

    def __generateSuit(self) -> DistributedSuitAI:
        suit = DistributedSuitAI(self.air, None)

        dna: SuitDNA = SuitDNA()

        # Assert that start level is non zero and that end level is not less than the start level.
        startLevel = self.minLevel
        endLevel = self.maxLevel
        if startLevel < 1:
            startLevel = 1
        if endLevel < startLevel:
            endLevel = startLevel

        suitLevel = random.randint(startLevel, endLevel)
        randomSuitType = getRandomSuitType(suitLevel)
        dna.newSuitRandom(level=randomSuitType)
        suit.dna = dna
        suit.setLevel(suitLevel)

        suit.generateWithRequired(self.zoneId)
        return suit

    def start(self, invoker: int, otherToons=None):

        if otherToons is None:
            otherToons = []

        self.joinableFsm.request('Joinable')
        if self.addToon(invoker):
            self.activeToons.append(invoker)
        else:
            self.end()
            return

        for toon in otherToons:
            self.addToon(toon)
            self.activeToons.append(toon)

        self.suitRequestJoin(self.__generateSuit())
        self.suitRequestJoin(self.__generateSuit())
        self.suitRequestJoin(self.__generateSuit())
        self.suitRequestJoin(self.__generateSuit())

        self.b_setState('FaceOff')

    def end(self):
        self.b_setState('Resume')

    # Called from clients participating in this battle. Update a setting we have
    def updateSetting(self, command: int, value: int):
        if command == SET_MIN_LEVEL:
            self.minLevel = value
            self.broadcast(f"Set min level to {self.minLevel}")
        elif command == SET_MAX_LEVEL:
            self.maxLevel = value
            self.broadcast(f"Set max level to {self.maxLevel}")

    # Send a message to active toons
    def broadcast(self, msg: str):
        for toonId in self.activeToons:
            toon = self.air.getDo(toonId)
            if isinstance(toon, DistributedToonAI):
                toon.d_sendArchipelagoMessage(msg)

    """
    Boilerplate FSM code, this pretty much just makes the battle function correctly
    """
    def faceOffDone(self):
        toonId = self.air.getAvatarIdFromSender()
        if self.ignoreResponses == 1:
            self.notify.debug('faceOffDone() - ignoring toon: %d' % toonId)
            return
        elif self.fsm.getCurrentState().getName() != 'FaceOff':
            self.notify.warning('faceOffDone() - in state: %s' % self.fsm.getCurrentState().getName())
            return
        elif self.toons.count(toonId) == 0:
            self.notify.warning('faceOffDone() - toon: %d not in toon list' % toonId)
            return
        self.responses[toonId] += 1
        self.notify.debug('toon: %d done facing off' % toonId)
        if not self.ignoreFaceOffDone:
            if self.allToonsResponded():
                self.handleFaceOffDone()
            else:
                self.timer.stop()
                self.timer.startCallback(TIMEOUT_PER_USER, self.__serverFaceOffDone)

    def enterFaceOff(self):
        self.notify.debug('enterFaceOff()')
        self.joinableFsm.request('Joinable')
        self.runableFsm.request('Unrunable')
        self.timer.startCallback(5.0, self.__serverFaceOffDone)
        return None

    def __serverFaceOffDone(self):
        self.notify.debug('faceoff timed out on server')
        self.ignoreFaceOffDone = 1
        self.handleFaceOffDone()

    def exitFaceOff(self):
        self.timer.stop()
        self.resetResponses()
        return None

    def handleFaceOffDone(self):
        self.d_setMembers()
        self.b_setState('WaitForInput')

    def enterResume(self):
        DistributedBattleBaseAI.enterResume(self)
        self.delete()

    def exitResume(self):
        DistributedBattleBaseAI.exitResume(self)
        taskName = self.taskName('finish')
        taskMgr.remove(taskName)

    def enterReward(self):
        self.ignoreResponses = 0
        super().enterReward()
        self.joinableFsm.request('Unjoinable')
        self.reviveDeadToons()

    def toonRequestJoin(self, x, y, z):

        if not self.air:
            return

        super().toonRequestJoin(x, y, z)

    def rewardDone(self):

        if not self.air:
            return

        super().rewardDone()

    def movieDone(self):
        if not self.air:
            return

        super().movieDone()

    def localMovieDone(self, needUpdate, deadToons, deadSuits, lastActiveSuitDied):

        spots = 4 - len(self.activeSuits)
        for _ in range(spots):
            self.suitRequestJoin(self.__generateSuit())

        super().localMovieDone(needUpdate, deadToons, deadSuits, lastActiveSuitDied)


