from direct.distributed.DistributedObjectAI import DistributedObjectAI

from toontown.groups.DistributedGroupAI import DistributedGroupAI
from toontown.toon.DistributedToonAI import DistributedToonAI


class DistributedGroupManagerAI(DistributedObjectAI):
    """
    An instance on the district that is responsible for managing separate groups.
    A "group" can be thought of as a "party" on other games, or even a "lobby".

    Toons will be in a group with other toons while a leader/host sets up game rules and eventually
    sends the entire group into some instance. (In our case, the trolley with specific settings.)

    This class is responsible for creating, destroying, and managing groups.
    Only one of these instances should exist per zone, or this could even be a singleton global object.
    """

    def __init__(self, air):
        super().__init__(air)
        self.groups: list[DistributedGroupAI] = []

    def delete(self):
        DistributedObjectAI.delete(self)

        for group in self.groups:
            group.delete()

        self.groups.clear()

    def getGroup(self, toon: DistributedToonAI) -> DistributedGroupAI | None:
        """
        Gets the current group this toon is in. Returns None if this toon is not in the group.
        """
        for group in self.groups:
            if toon.getDoId() in group.getMembers():
                return group

        return None

    def createGroup(self, leader: DistributedToonAI) -> DistributedGroupAI:
        """
        Creates a new group on the toon. Returns the new group.
        If this toon is already in a group, the old one will be returned.
        This toon cannot be in two different groups.
        """

        group = self.getGroup(leader)
        if group is not None:
            return group

        # Create a new group!
        group = DistributedGroupAI(self.air, leader)
        group.generateWithRequired(self.zoneId)
        self.groups.append(group)

        # Setup the required state.
        group.b_setLeader(leader.getDoId())
        group.b_setMembers(group.getMembers())
        group.b_setCapacity(group.DefaultCapacity)
        self.d_setCurrentGroup(leader.getDoId(), group.getDoId())
        return group

    """
    Astron Methods (Outgoing)
    """

    def d_setCurrentGroup(self, avId: int, groupId: int):
        self.sendUpdateToAvatarId(avId, "setCurrentGroup", [groupId])

    """
    Astron Methods (Incoming)
    """
    def requestKick(self, toKickId: int):

        leaderId: int = self.air.getAvatarIdFromSender()
        leader = self.air.getDo(leaderId)
        if leader is None:
            return

        # Is the leader in a group?
        group = self.getGroup(leader)
        if group is None:
            return

        # Is the leader actually a leader?
        if group.getLeader() != leader.getDoId():
            return

        # Is the leader in the same group as the other toon?
        if toKickId not in group.getMembers():
            return

        # This is a valid operation.
        group.removeMember(toKickId)
        group.b_setMembers(group.getMembers())
        print(f"{leader.getName()} has kicked {toKickId}. The updated roster is now {group.getMembers()}")

    def invitePlayer(self, toInviteId: int):

        inviterId: int = self.air.getAvatarIdFromSender()
        inviter = self.air.getDo(inviterId)
        otherToon = self.air.getDo(toInviteId)
        if inviter is None:
            return

        otherGroup = self.getGroup(otherToon)
        # Is the other toon already in a group?
        if otherGroup is not None:
            return

        # Is the inviter in a group?
        group = self.getGroup(inviter)
        if group is None:
            # Are both players not in a group? This is valid. Create a new group.
            if otherGroup is None:
                group = self.createGroup(inviter)
                group.addMember(otherToon.getDoId())
                group.b_setMembers(group.getMembers())
                self.d_setCurrentGroup(toInviteId, group.getDoId())
            return

        # Is the group already full?
        if group.isFull():
            return

        # This is a valid operation.
        group.addMember(toInviteId)
        group.b_setMembers(group.getMembers())
        self.d_setCurrentGroup(toInviteId, group.getDoId())
        print(f"{inviter.getName()} has invited {toInviteId}. The updated roster is now {group.getMembers()}")
