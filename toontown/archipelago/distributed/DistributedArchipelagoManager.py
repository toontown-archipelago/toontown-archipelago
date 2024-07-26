from typing import List, Dict, Union

from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObject import DistributedObject

from toontown.archipelago.definitions import color_profile
from toontown.archipelago.definitions.color_profile import ColorProfile
from toontown.archipelago.util.HintContainer import HintContainer, HintedItem
from toontown.archipelago.util.archipelago_information import ArchipelagoInformation
from toontown.toon.DistributedToon import DistributedToon

# An array of default defined team colors to use.
# Feel free to dynamically adjust this array however you please
TEAM_COLORS = (
    color_profile.BLUE,
    color_profile.RED,
    color_profile.GREEN,
    color_profile.YELLOW,
    color_profile.CYAN,
    color_profile.MAGENTA,
    color_profile.ORANGE,
    color_profile.PURPLE,
    color_profile.PINK,
    color_profile.MINT_GREEN,
    color_profile.MIDNIGHT_BLUE,
    color_profile.BURGUNDY,
    color_profile.MAUVE,
)

# The color to use when a toon is not on a team. (Not connected to AP)
NO_TEAM_COLOR = color_profile.GRAY


# Basically the "None" to check for when team checking
NO_TEAM = 999

class DistributedArchipelagoManager(DistributedObject):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedArchipelagoManager")
    neverDisable = 1

    def __init__(self, cr):
        super().__init__(cr)
        self.notify.debug("DistributedArchipelagoManager starting up....")

        self._ap_info_cache: Dict[int, ArchipelagoInformation] = {}

    def generate(self):
        self.notify.debug("DistributedArchipelagoManager generate()")
        base.cr.archipelagoManager = self

    def announceGenerate(self):
        self.notify.debug("DistributedArchipelagoManager announceGenerate()")

    def delete(self):
        self.notify.debug("DistributedArchipelagoManager delete()")
        base.cr.archipelagoManager = None

    # Called from the AI. Used to update information that we need to know about toons and their sessions.
    # As the client, we are unaware of most Archipelago things being done on the AI so whatever we need to know
    # We receive here.

    # This can probably be improved, but for now we just get something to work.
    # Only called when information updates on the AI that we need to know.
    def sync(self, info_array: List[List[int]]):

        # First convert our astron data back into our dataclass
        tempInfo: List[ArchipelagoInformation] = []
        for info in info_array:
            tempInfo.append(ArchipelagoInformation.from_struct(info))

        # Clear our cache and add the new data we received
        self._ap_info_cache.clear()
        for info in tempInfo:
            self._ap_info_cache[info.avId] = info

        # Now update everyone's colors
        self.syncToonColorProfiles()

        # Debug
        self.notify.debug(f"DistributedArchipelagoManager sync(): {self._ap_info_cache}")

    # Loops through every DistributedToon in the base.cr repository and sets a color profile for them
    # (If we have one)
    def syncToonColorProfiles(self):

        toons: Dict[int, DistributedToon] = base.cr.getObjectsOfExactClass(DistributedToon)
        self.notify.debug(f"Syncing {len(toons)+1} toons color profiles")

        # Loop through every toon in our DO repository and update their color profile.
        # (If they exist)
        for toonId, toon in toons.items():
            newColorProfile = self.getToonColorProfile(toonId)
            toon.setColorProfile(newColorProfile)

        # Now update ours.
        base.localAvatar.setColorProfile(self.getToonColorProfile(base.localAvatar.getDoId()))

    # Given an avId, attempt to find information related to this toon.
    # Returns ArchipelagoInformation dataclass if exists, None otherwise.
    def getInformation(self, avId) -> Union[ArchipelagoInformation, None]:
        return self._ap_info_cache.get(avId, None)

    def getLocalInformation(self) -> ArchipelagoInformation | None:
        """
        Returns the local toon's information. Returns None if local toon is not currently in an Archipelago session
        """
        return self.getInformation(base.localAvatar.getDoId())

    """
    Helper methods to be called throughout the client for game code
    
    Most of these methods are just dupes of the AI versions, but they work with our ArchipelagoInformation
    dataclasses instead of the raw session on the AI.
    """

    # Given an toon ID, return the ID of the team they are on.
    # Returns None if they are either not on a team, or not connected to Archipelago.
    def getToonTeam(self, avId) -> int:

        # See if we have information about this toon
        info = self.getInformation(avId)
        if info is None:
            return NO_TEAM

        # See if we are on a valid team
        teamId = info.teamId
        if teamId == NO_TEAM:
            return NO_TEAM

        # We have a team!
        return teamId

    # Given two toon IDs, return whether or not they are on the same team.
    # This case is ONLY True when both toons are connected to archipelago and have a similar team slot.
    def onSameTeam(self, avId1, avId2) -> bool:
        team1 = self.getToonTeam(avId1)
        team2 = self.getToonTeam(avId2)

        # If either team1 or team2 is not on a team, they cannot be on the same team.
        if NO_TEAM in (team1, team2):
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
        if NO_TEAM in (toon1Team, toon2Team):
            return False

        # If the teams are not equal, they are enemies.
        return toon1Team != toon2Team

    # Returns a list of all toon IDs we are enemies with.
    def getAllEnemies(self) -> List[int]:
        enemies: List[int] = []

        # Loop through all of our information, if the two avIds are enemies then add it
        for info in self._ap_info_cache.values():
            if self.onEnemyTeams(info.avId, base.localAvatar.getDoId()):
                enemies.append(info.avId)

        return enemies

    # Given a team ID, (from self.getToonTeam()) return a ColorProfile.
    def getTeamColorProfile(self, teamId: int) -> ColorProfile:

        # If not on a valid team then return gray.
        # This toon is either "spectating" or is not connected to Archipelago currently.
        if teamId < 0 or teamId is None:
            return NO_TEAM_COLOR

        # If on a team that is within bounds return that color
        if teamId < len(TEAM_COLORS):
            return TEAM_COLORS[teamId]

        # Out of bounds color, make a randomly seeded one (lol)
        return color_profile.getRandomColorProfile(teamId)

    # Given a Toon ID, return a color profile we should use for this toon.
    def getToonColorProfile(self, toonId: int) -> ColorProfile:

        info = self.getInformation(toonId)

        # If we don't have information for this toon, we can safely assume they are not on a team.
        if info is None:
            return NO_TEAM_COLOR

        # Extract the toon's team information and find the team's corresponding color.
        teamID = info.teamId
        return self.getTeamColorProfile(teamID)


    """
    Code related to hint management
    """

    def d_requestHints(self):
        self.sendUpdate('requestHints')

    def setHints(self, primitiveHintContainer):
        """
        Called from the AI, updates hint container stored locally
        """
        container = HintContainer.from_struct(base.localAvatar.getDoId(), primitiveHintContainer)
        base.localAvatar.setHintContainer(container)
        messenger.send('archipelago-hint-update')

    def addHint(self, primitiveHint, silent=False) -> bool:
        """
        Called from the AI, contains a single hint to add to our container
        returns true if the hint made a modification
        """
        hint: HintedItem = HintedItem.from_struct(primitiveHint)
        newHint = base.localAvatar.getHintContainer().addHint(hint)
        if not silent and newHint:
            messenger.send('archipelago-hints-updated')
        return newHint

    def addHints(self, primitiveHintList, silent=False):
        """
        Called from the AI, contains a multiple hints to add to our container
        """
        foundNewHint = False
        for hint in primitiveHintList:
            new = self.addHint(hint, silent=True)
            if new:
                foundNewHint = True

        if not silent and foundNewHint:
            messenger.send('archipelago-hints-updated')

