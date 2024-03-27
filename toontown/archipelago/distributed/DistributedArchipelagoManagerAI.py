from typing import Union, List

from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

from toontown.archipelago.apclient.ap_client_enums import APClientEnums
from toontown.archipelago.apclient.archipelago_session import ArchipelagoSession
from toontown.archipelago.util.archipelago_information import ArchipelagoInformation
from toontown.toon.DistributedToonAI import DistributedToonAI


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

    def __getToon(self, avId) -> Union[DistributedToonAI, None]:
        return self.air.doId2do.get(avId)

    def __getSession(self, avId) -> Union[ArchipelagoSession, None]:
        toon = self.__getToon(avId)
        if toon is None:
            return None

        # Is there a session defined?
        session = toon.archipelago_session
        if session is None:
            return None

        # If the toon is not connected to an AP server, then this should also be none.
        if session.client.state != APClientEnums.CONNECTED:
            return None

        return toon.archipelago_session

    # Returns a list of all Archipelago Sessions that are defined on any DistributedToonAI instances.
    def __getAllArchipelagoSessions(self) -> List[ArchipelagoSession]:
        sessions: List[ArchipelagoSession] = []

        # Loop through all online toons and extract the AP session if it exists.
        for toon in self.air.doFindAllInstances(DistributedToonAI):

            # Skip NPCs :3
            if not toon.isPlayerControlled():
                continue

            # If the toon has an AP session add it
            if toon.archipelago_session is not None:
                sessions.append(toon.archipelago_session)

        return sessions

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
            infoToSend.append(ArchipelagoInformation(session.avatar.doId, session.getSlotId(), session.getTeamId()))

        self.d_sync(infoToSend)

    # Given an toon ID, return the ID of the team they are on.
    # Returns None if they are either not on a team, or not connected to Archipelago.
    def getToonTeam(self, avId) -> Union[int, None]:

        # See if we have a session
        session = self.__getSession(avId)
        if session is None:
            return None

        # See if we are on a valid team
        teamId = session.getTeamId()
        if teamId < 0:
            return None

        # We have a team!
        return teamId

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
