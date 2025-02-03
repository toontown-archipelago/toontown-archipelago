from direct.distributed.DistributedObject import DistributedObject

from libotp.nametag.WhisperGlobals import WhisperType
from toontown.groups import GroupGlobals
from toontown.groups.GroupBase import GroupBase
from toontown.groups.GroupInterface import GroupInterface
from toontown.groups.GroupMemberStruct import GroupMemberStruct


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

        # If we are in the group and this group is deleting, send an update to mark us as not ready.
        # This probably means we are leaving the area and are unable to respond to the group sending us to game.
        if self.__localToonInGroup() and base.localAvatar.getGroupManager() is not None:
            base.localAvatar.getGroupManager().updateStatus(GroupGlobals.STATUS_UNREADY)

        DistributedObject.delete(self)
        self.cleanup()

    def __localToonInGroup(self) -> bool:
        return base.localAvatar.getDoId() in self.getMemberIds()

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
    def setMembers(self, members: list[list[int, int, bool]]):

        formattedMembers: list[GroupMemberStruct] = []
        leader = None
        weAreNotInThisGroup = self.__localToonInGroup()

        for entry in members:
            member = GroupMemberStruct.from_struct(entry)
            if member.leader:
                leader = member
            formattedMembers.append(member)

        super().setMembers(formattedMembers)
        self.setLeader(leader.avId if leader is not None else GroupBase.NoLeader)

        # If we are a newcomer to this group, analyze the state of this group.
        # If we are in the walk state, we are considered ready to go.
        weJoined = not weAreNotInThisGroup and self.__localToonInGroup()
        if weJoined:
            if base.cr.playGame.getPlace() is not None and base.cr.playGame.getPlace().getState() == 'walk' and base.localAvatar.getGroupManager() is not None:
                base.localAvatar.getGroupManager().updateStatus(GroupGlobals.STATUS_READY)

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
