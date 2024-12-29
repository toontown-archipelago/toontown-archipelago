from typing import Union, List

from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

from toontown.archipelago.util.HintContainer import HintContainer, HintedItem
from toontown.archipelago.util.archipelago_information import ArchipelagoInformation


class DistributedArchipelagoManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedArchipelagoManagerAI")

    def __init__(self, air):
        super().__init__(air)
        self.notify.debug("DistributedArchipelagoManager starting up....")

        # A cache of the last astron update sent, no need to use
        self.__previousSyncedInformation = []

    def announceGenerate(self):
        self.notify.debug(f"DistributedArchipelagoManager announceGenerate() with doId: {self.doId}")

    """
    Internal methods to make management easier
    """

    def __getToon(self, avId) -> None:
        return self.air.doId2do.get(avId)

    def __getSession(self, avId) -> None:
        return None

    # Returns a list of all Archipelago Sessions that are defined on any DistributedToonAI instances.
    def __getAllArchipelagoSessions(self):
        return []


    """
    Public methods to be called for logic throughout the game's codebase
    """

    # Called when we need to make clients aware of information updates regarding slot/team IDs
    # todo In the future, we should refactor this to update specific toons dynamically but for now
    # todo we just want something to work
    def updateToonInfo(self, avId, slotId, teamId):
        infoToSend: List[ArchipelagoInformation] = []
        allApSessions = self.__getAllArchipelagoSessions()
        for session in allApSessions:
            infoToSend.append(ArchipelagoInformation(session.avatar.doId, 0, 0))

        self.d_sync(infoToSend)

    # Given an toon ID, return the ID of the team they are on.
    # Returns None if they are either not on a team, or not connected to Archipelago.
    def getToonTeam(self, avId) -> Union[int, None]:

        # See if we have a session
        return None

    # Given two toon IDs, return whether or not they are on the same team.
    # This case is ONLY True when both toons are connected to archipelago and have a similar team slot.
    def onSameTeam(self, avId1, avId2) -> bool:
        team1 = self.getToonTeam(avId1)
        team2 = self.getToonTeam(avId2)

        # If either team1 or team2 is not on a team, they cannot be on the same team.
        if None in (team1, team2):
            return False

        # If the teams are equal, they are on the same team
        return team1 == team2

    # Given two toon IDs, return whether or not they are on enemy teams.
    # We define enemy teams as two opposing teams that does not include spectators.
    # This means that if either toon is not on a team, they will not be considered enemies.
    def onEnemyTeams(self, avId1, avId2) -> bool:
        toon1Team = self.getToonTeam(avId1)
        toon2Team = self.getToonTeam(avId2)

        # If either toon1 or toon2 is not on a team, they cannot be enemies.
        if None in (toon1Team, toon2Team):
            return False

        # If the teams are not equal, they are enemies.
        return toon1Team != toon2Team


    """
    Code related to hint management
    """
    def requestHints(self):
        """
        Called via an astron update when a client requests their full hint container.
        """

        pass

    def d_setHints(self, avId, hint_container: HintContainer):
        """
        Send the full hint container to a certain client for sync purposes.
        """
        pass

    def d_sendHint(self, avId, hint: HintedItem):
        """
        Send a singular hint to a player for them to additively cache it locally
        """
        pass

    def d_sendHints(self, avId, hints: List[HintedItem]):
        """
        Send multiple hints to a player for them to additively cache them locally
        """
        pass


    """
    Boilerplate astron code throw up emoji
    """

    # No need to use, boilerplate for ram astron field
    def getSync(self):
        return self.__previousSyncedInformation

    # No need to use, boilerplate for ram astron field
    def setSync(self, infoArray: List[ArchipelagoInformation]):
        self.__previousSyncedInformation = infoArray

    # Call to sync the client with information that they need from the AI to display information correctly.
    # This can probably be optimized later but this is just to get something to work :3
    def d_sync(self, infoArray: List[ArchipelagoInformation]):
        structList: List[List[int]] = [info.struct() for info in infoArray]
        self.sendUpdate('sync', [structList])
