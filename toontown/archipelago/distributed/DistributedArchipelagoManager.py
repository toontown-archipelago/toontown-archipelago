from typing import List, Dict, Union

from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObject import DistributedObject

from toontown.archipelago.definitions import color_profile
from toontown.archipelago.definitions.color_profile import ColorProfile
from toontown.archipelago.util.archipelago_information import ArchipelagoInformation

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

        # Debug
        self.notify.debug(f"DistributedArchipelagoManager sync(): {self._ap_info_cache}")

    # Given an avId, attempt to find information related to this toon.
    # Returns ArchipelagoInformation dataclass if exists, None otherwise.
    def getInformation(self, avId) -> Union[ArchipelagoInformation, None]:
        return self._ap_info_cache.get(avId, None)

    """
    Helper methods to be called throughout the client for game code
    
    Most of these methods are just dupes of the AI versions, but they work with our ArchipelagoInformation
    dataclasses instead of the raw session on the AI.
    """

    # Given an toon ID, return the ID of the team they are on.
    # Returns None if they are either not on a team, or not connected to Archipelago.
    def getToonTeam(self, avId) -> Union[int, None]:

        # See if we have information about this toon
        info = self.getInformation(avId)
        if info is None:
            return None

        # See if we are on a valid team
        teamId = info.teamId
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
