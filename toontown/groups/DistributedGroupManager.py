from direct.distributed.DistributedObject import DistributedObject

from toontown.groups.DistributedGroup import DistributedGroup
from toontown.groups.GroupBase import GroupBase


class DistributedGroupManager(DistributedObject):
    """
    An instance on the client that is responsible for managing separate groups.
    A "group" can be thought of as a "party" on other games, or even a "lobby".

    Toons will be in a group with other toons while a leader/host sets up game rules and eventually
    sends the entire group into some instance. (In our case, the trolley with specific settings.)

    This class is responsible for communicating with the server's version of the group manager,
    and will tell our local client which group we are in.
    """

    def __init__(self, cr):
        super().__init__(cr)

        # The current group that our client is currently in.
        # Once we are in a group, we can actually properly render it.
        self.currentGroup: DistributedGroup | None = None

    def generate(self):
        """
        When a group manager comes into existence, we essentially just need to create a way to
        reference this object globally across the game so that our toon panels know to display
        an invite button.
        """
        super().generate()
        print("Generating DistributedGroupManager")
        base.localAvatar.setGroupManager(self)

    def delete(self):
        """
        When this group manager deletes, we need to make sure that we leave our current group.
        """
        super().delete()
        print("Deleting DistributedGroupManager")
        base.localAvatar.setGroupManager(None)

    def findGroupById(self, groupId: int) -> DistributedGroup | None:
        """
        Attempts to find the group in the client repository. Returns None if no such group exists.
        """
        if groupId == GroupBase.NoGroup:
            return None

        return self.cr.getDo(groupId)

    """
    Methods called from the codebase.
    """

    def attemptKick(self, avId: int):
        """
        Attempt to kick this toon from the boarding group we are currently in.
        """
        print(f'[DistributedGroupManager] attempting kick to {avId}')
        if self.getCurrentGroup() is None:
            return

        # Are we the leader of our group?
        if self.getCurrentGroup().getLeader() != base.localAvatar.doId:
            return

        self.d_requestKick(avId)

    def attemptInvite(self, avId: int):
        """
        Attempt to add this toon to the group we are currently in.
        """
        print(f'[DistributedGroupManager] attempting invite to {avId}')
        self.d_invitePlayer(avId)

    """
    Astron Methods
    """

    def d_requestKick(self, avId: int):
        self.sendUpdate('requestKick', [avId])

    def d_invitePlayer(self, avId: int):
        self.sendUpdate('invitePlayer', [avId])

    def setCurrentGroup(self, groupId: int):
        """
        Called from the AI when we are assigned to be in a new group.
        """

        # Cleanup the old group.
        if self.currentGroup is not None:
            self.currentGroup.cleanup()

        # Update to the new group.
        self.currentGroup = self.findGroupById(groupId)
        if self.currentGroup is None:
            return

        self.currentGroup.render()

    def getCurrentGroup(self) -> DistributedGroup | None:
        return self.currentGroup
