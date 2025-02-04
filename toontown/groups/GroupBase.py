from toontown.groups import GroupGlobals
from toontown.groups.GroupMemberStruct import GroupMemberStruct


class GroupBase:
    """
    Holds a collection of IDs. Provides basic functionality for having a list of members
    and a "leader".
    """

    # A flag that can be used to send over astron that represents a "null" group.
    NoGroup = -1
    NoLeader = -2

    DefaultCapacity = 16

    def __init__(self, leader: int):
        self.leader: int = leader
        self.members: list[GroupMemberStruct] = []

        if self.leader != GroupBase.NoLeader:
            self.members.append(GroupMemberStruct(self.leader, GroupGlobals.TEAM_FFA, GroupGlobals.STATUS_LEADER, True))

        self.capacity = GroupBase.DefaultCapacity

    def getLeader(self) -> int:
        """
        Returns the ID of the leader of the group.
        If the leader is NoLeader (-2), that means the group is empty and should be destroyed.
        The consumer needs to check for this.
        """
        return self.leader

    def setLeader(self, leader: int):
        """
        Sets the leader of the group. If the given parameter is not present in the group already,
        this does nothing.
        """
        if leader not in self.getMemberIds():
            return
        self.leader = leader

    def hasLeader(self) -> bool:
        return self.leader != GroupBase.NoLeader

    def getMembers(self) -> list[GroupMemberStruct]:
        """
        Returns a list of members in this group. The returned list is a list of their IDs.
        """
        return self.members

    def getMemberIds(self) -> list[int]:
        """
        Returns a list of integers representing IDs of members in this group.
        """
        return [member.avId for member in self.members]

    def isInGroup(self, avId: int) -> bool:
        """
        Checks if a toon with the given avId is in the group. Returns False if they are not.
        """
        return avId in self.getMemberIds()

    def setMembers(self, members: list[GroupMemberStruct]):
        """
        Sets the members of the group. If the leader is not present in the group already,
        the leader is set to whoever is first.
        """
        self.members = members
        if self.leader not in self.getMemberIds() and self.getMemberCount() > 0:
            self.leader = members[0].avId

    def getMemberCount(self) -> int:
        """
        Returns how many members are currently in this group.
        """
        return len(self.members)

    def addMember(self, member: int) -> bool:
        """
        Attempts to add a member to the group.
        Returns True if the member was successfully added.
        """
        if member in self.getMemberIds():
            return False

        self.members.append(GroupMemberStruct(member, GroupGlobals.TEAM_FFA, GroupGlobals.STATUS_UNREADY, False))
        return True

    def getMember(self, avId: int) -> GroupMemberStruct | None:
        """
        Queries this group for a member. Returns None if there is not a member with the given ID.
        """
        for member in self.members:
            if member.avId == avId:
                return member

        return None

    def removeMember(self, memberId: int) -> bool:
        """
        Attempts to remove a member from the group.
        Returns True if the member was successfully removed.
        """
        member = self.getMember(memberId)
        if member is None:
            return False

        self.members.remove(member)

        # If the member that is being removed was the leader, we should make the leader the first person.
        if memberId == self.leader:
            self.leader = self.members[0].avId if self.getMemberCount() > 0 else GroupBase.NoLeader

        return True

    def getCapacity(self) -> int:
        return self.capacity

    def setCapacity(self, capacity: int):
        self.capacity = capacity

    def isFull(self):
        return self.getMemberCount() >= self.getCapacity()
