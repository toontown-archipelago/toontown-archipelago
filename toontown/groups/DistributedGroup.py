from direct.distributed.DistributedObject import DistributedObject

from libotp.nametag.WhisperGlobals import WhisperType
from toontown.groups.GroupBase import GroupBase
from toontown.groups.GroupInterface import GroupInterface
from toontown.toonbase import ToontownGlobals


class DistributedGroup(DistributedObject, GroupBase):

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        GroupBase.__init__(self, GroupBase.NoLeader)

        self.interface: GroupInterface | None = None

    def announceGenerate(self):
        DistributedObject.announceGenerate(self)
        if self.__localToonInGroup():
            base.localAvatar.getGroupManager().setCurrentGroup(self.getDoId())

        self.render()

    def delete(self):
        DistributedObject.delete(self)
        self.cleanup()

    def __localToonInGroup(self) -> bool:
        return base.localAvatar.getDoId() in self.getMembers()

    """
    Methods used for GUI management.
    """

    def render(self):

        # No need to render the group if we aren't in it.
        if not self.__localToonInGroup():
            self.__deleteInterface()
            return

        if self.interface is None:
            self.__makeNewInterface()

        self.interface.updateMembers(self.getMembers())

    def cleanup(self):
        self.__deleteInterface()

    def __makeNewInterface(self):
        self.__deleteInterface()
        self.interface = GroupInterface(self)

    def __deleteInterface(self):
        if self.interface is not None:
            self.interface.destroy()
            self.interface = None

    """
    Methods called from the AI over astron.
    """
    def setLeader(self, leader: int):
        super().setLeader(leader)
        self.render()

    def setMembers(self, members: list[int]):
        super().setMembers(members)
        self.render()

    def announce(self, message: str):
        if self.__localToonInGroup():
            base.localAvatar.setSystemMessage(0, message, whisperType=WhisperType.WTToontownBoardingGroup)

    def setMinigameZone(self, minigameZone, minigameGameId):
        playground = base.cr.playGame.getPlace()
        doneStatus = {
            'loader': 'minigame',
            'where': 'minigame',
            'hoodId': playground.loader.hood.id,
            'zoneId': minigameZone,
            'shardId': None,
            'minigameId': minigameGameId,
            'avId': None,
        }
        playground.doneStatus = doneStatus
        playground.fsm.forceTransition('teleportOut', [doneStatus])
