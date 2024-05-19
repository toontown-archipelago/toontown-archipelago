import random
import traceback
from dataclasses import dataclass

from toontown.toonbase import ToontownGlobals
from . import DistributedMinigameTemplateAI
from . import DistributedRaceGameAI
from . import DistributedCannonGameAI
from . import DistributedTagGameAI
from . import DistributedPatternGameAI
from . import DistributedRingGameAI
from . import DistributedMazeGameAI
from . import DistributedTugOfWarGameAI
from . import DistributedCatchGameAI
from . import DistributedDivingGameAI
from . import DistributedTargetGameAI
from . import DistributedPairingGameAI
from . import DistributedPhotoGameAI
from . import DistributedVineGameAI
from . import DistributedIceGameAI
from . import DistributedCogThiefGameAI
from . import DistributedTwoDGameAI
from . import DistributedTravelGameAI
from . import TravelGameGlobals
from .DistributedMinigameAI import DistributedMinigameAI


@dataclass
class GeneratedMinigame:
    minigame: DistributedMinigameAI
    zone: int
    gameId: int


class MinigameCreatorAI:

    MINIGAME_ID_TO_CLASS = {
            ToontownGlobals.RaceGameId: DistributedRaceGameAI.DistributedRaceGameAI,
            ToontownGlobals.CannonGameId: DistributedCannonGameAI.DistributedCannonGameAI,
            ToontownGlobals.TagGameId: DistributedTagGameAI.DistributedTagGameAI,
            ToontownGlobals.PatternGameId: DistributedPatternGameAI.DistributedPatternGameAI,
            ToontownGlobals.RingGameId: DistributedRingGameAI.DistributedRingGameAI,
            ToontownGlobals.MazeGameId: DistributedMazeGameAI.DistributedMazeGameAI,
            ToontownGlobals.TugOfWarGameId: DistributedTugOfWarGameAI.DistributedTugOfWarGameAI,
            ToontownGlobals.CatchGameId: DistributedCatchGameAI.DistributedCatchGameAI,
            ToontownGlobals.DivingGameId: DistributedDivingGameAI.DistributedDivingGameAI,
            ToontownGlobals.TargetGameId: DistributedTargetGameAI.DistributedTargetGameAI,
            ToontownGlobals.MinigameTemplateId: DistributedMinigameTemplateAI.DistributedMinigameTemplateAI,
            ToontownGlobals.PairingGameId: DistributedPairingGameAI.DistributedPairingGameAI,
            ToontownGlobals.VineGameId: DistributedVineGameAI.DistributedVineGameAI,
            ToontownGlobals.IceGameId: DistributedIceGameAI.DistributedIceGameAI,
            ToontownGlobals.CogThiefGameId: DistributedCogThiefGameAI.DistributedCogThiefGameAI,
            ToontownGlobals.TwoDGameId: DistributedTwoDGameAI.DistributedTwoDGameAI,
            ToontownGlobals.TravelGameId: DistributedTravelGameAI.DistributedTravelGameAI,
            ToontownGlobals.PhotoGameId: DistributedPhotoGameAI.DistributedPhotoGameAI
        }

    def __init__(self, air):
        self.air = air
        self.minigameZoneReferences = {}
        self.minigameRequests = {}

    def acquireMinigameZone(self, zoneId):
        if zoneId not in self.minigameZoneReferences:
            self.minigameZoneReferences[zoneId] = 0
        self.minigameZoneReferences[zoneId] += 1

    def releaseMinigameZone(self, zoneId):
        self.minigameZoneReferences[zoneId] -= 1
        if self.minigameZoneReferences[zoneId] <= 0:
            del self.minigameZoneReferences[zoneId]
            self.air.deallocateZone(zoneId)

    def getMinigameChoices(self, numPlayers: int, previousGameId=ToontownGlobals.NoPreviousGameId, allowTrolleyTracks=False) -> list[int]:
        choices = list(ToontownGlobals.MinigameIDs)

        # Remove trolley tracks if we don't want to consider it
        if not allowTrolleyTracks and ToontownGlobals.TravelGameId in choices:
            choices.remove(ToontownGlobals.TravelGameId)

        # Remove previous game from the pool
        if previousGameId in choices:
            choices.remove(previousGameId)

        # If a player is solo filter out multiplayer games
        if numPlayers <= 1:
            for multiplayerGame in ToontownGlobals.MultiplayerMinigames:
                if multiplayerGame in choices:
                    choices.remove(multiplayerGame)

        return choices

    def createMinigame(self, playerArray, trolleyZone, minigameZone=None, previousGameId=ToontownGlobals.NoPreviousGameId, newbieIds=None, startingVotes=None, metagameRound=-1, desiredNextGame=None) -> GeneratedMinigame:
        if newbieIds is None:
            newbieIds = []

        if minigameZone is None:
            minigameZone = self.air.allocateZone()

        self.acquireMinigameZone(minigameZone)

        minigameChoices = self.getMinigameChoices(len(playerArray), previousGameId=previousGameId, allowTrolleyTracks=False)
        mgId = random.choice(minigameChoices)

        if metagameRound > -1:
            if metagameRound % 2 == 0:
                mgId = ToontownGlobals.TravelGameId
            elif desiredNextGame:
                mgId = desiredNextGame

        # Check for requested minigames via commands, clear request if one was found
        for toonId in playerArray:
            if toonId in self.minigameRequests:
                mgId = self.minigameRequests[toonId]
                self.clearRequest(toonId)
                break

        if mgId not in self.MINIGAME_ID_TO_CLASS:
            print(f"Unable to find minigame constructor matching minigame id: {mgId}, defaulting to cannon game")
            traceback.print_exc()
            mg = DistributedCannonGameAI.DistributedCannonGameAI(self.air, ToontownGlobals.CannonGameId)
        else:
            mg = self.MINIGAME_ID_TO_CLASS[mgId](self.air, mgId)

        mg.setExpectedAvatars(playerArray)
        mg.setNewbieIds(newbieIds)
        mg.setTrolleyZone(trolleyZone)
        if startingVotes is None:
            for avId in playerArray:
                mg.setStartingVote(avId, TravelGameGlobals.DefaultStartingVotes)

        else:
            for index in range(len(startingVotes)):
                avId = playerArray[index]
                votes = startingVotes[index]
                if votes < 0:
                    print('createMinigame negative votes, avId=%s votes=%s' % (avId, votes))
                    votes = 0
                mg.setStartingVote(avId, votes)

        mg.setMetagameRound(metagameRound)
        mg.generateWithRequired(minigameZone)

        for avId in playerArray:
            toon = self.air.doId2do.get(avId)
            if toon is not None:
                self.air.questManager.toonPlayedMinigame(toon)

        return GeneratedMinigame(mg, minigameZone, mgId)

    def storeRequest(self, avId, minigameId):
        self.minigameRequests[avId] = minigameId

    def clearRequest(self, avId):
        if avId in self.minigameRequests:
            del self.minigameRequests[avId]