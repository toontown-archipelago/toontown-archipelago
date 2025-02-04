from direct.distributed.DistributedObjectAI import DistributedObjectAI

from toontown.groups import GroupGlobals
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

    def announceGenerate(self):
        super().announceGenerate()
        self.accept('avatarExited', self.__handleUnexpectedExit)

    def delete(self):
        DistributedObjectAI.delete(self)
        self.ignore('avatarExited')

        for group in self.groups:
            group.delete()

        self.groups.clear()

    def getGroup(self, toon: DistributedToonAI) -> DistributedGroupAI | None:
        """
        Gets the current group this toon is in. Returns None if this toon is not in the group.
        """
        for group in self.groups:
            if toon.getDoId() in group.getMemberIds():
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
        group.b_setCapacity(group.DefaultCapacity)
        group.b_setMembers(group.getMembers())
        self.d_setCurrentGroup(leader.getDoId(), group.getDoId())
        return group

    def deleteGroup(self, group: DistributedGroupAI):
        group.requestDelete()
        if group in self.groups:
            self.groups.remove(group)

    def __handleUnexpectedExit(self, toon):
        group = self.getGroup(toon)
        if group is None:
            return

        removed = group.removeMember(toon.getDoId())
        group.b_setMembers(group.getMembers())
        if removed:
            group.announce(f"{toon.getName()} has logged out. Removing them from the group.")
            if len(group.getMembers()) == 0:
                self.deleteGroup(group)

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

        # Is the leader in the same group as the other toon?
        if toKickId not in group.getMemberIds():
            return

        # Is the leader actually a leader? Only check this if the person is not kicking themselves.
        if leaderId != toKickId and group.getLeader() != leader.getDoId():
            return

        if group.onCooldown():
            return

        if toKickId == leaderId:
            group.announce(f"{leader.getName()} has chose to leave the group.")
        else:
            name = toKickId
            if self.air.getDo(toKickId) is not None:
                name = self.air.getDo(toKickId).getName()
            group.announce(f"{leader.getName()} has kicked {name} from the group.")

        # This is a valid operation.
        group.removeMember(toKickId)
        group.b_setMembers(group.getMembers())

        # Is this group empty? If so, delete it.
        if len(group.getMembers()) == 0:
            self.deleteGroup(group)

    def invitePlayer(self, toInviteId: int):

        inviterId: int = self.air.getAvatarIdFromSender()
        inviter = self.air.getDo(inviterId)
        otherToon = self.air.getDo(toInviteId)
        if inviter is None:
            return

        otherGroup = self.getGroup(otherToon)
        group = self.getGroup(inviter)

        # Is the other toon already in a group?
        if otherGroup is not None:
            group.announce(f"{inviter.getName()} tried to invite {otherToon.getName()}, but they are already in a group!")
            return

        # Is the inviter in a group?

        if group is None:
            # Are both players not in a group? This is valid. Create a new group.
            if otherGroup is None:
                group = self.createGroup(inviter)
                group.addMember(otherToon.getDoId())
                group.b_setMembers(group.getMembers())
                self.d_setCurrentGroup(toInviteId, group.getDoId())
                group.announce(f"{inviter.getName()} has started a group with {otherToon.getName()}")
            return

        # Is the group already full?
        if group.isFull():
            group.announce(f"{inviter.getName()} tried to invite {otherToon.getName()} but the group is full!")
            return

        if group.onCooldown():
            return

        # This is a valid operation.
        group.addMember(toInviteId)
        group.b_setMembers(group.getMembers())
        self.d_setCurrentGroup(toInviteId, group.getDoId())
        group.announce(f"{inviter.getName()} has added {otherToon.getName()} to the group!")

    def requestPromote(self, toPromoteId: int):

        leaderId: int = self.air.getAvatarIdFromSender()
        leader = self.air.getDo(leaderId)
        if leader is None:
            return

        toPromote = self.air.getDo(toPromoteId)
        if toPromote is None:
            return

        # Are the two users in the same group?
        leadersGroup = self.getGroup(leader)
        if leadersGroup is None or toPromoteId not in leadersGroup.getMemberIds():
            return

        # Is the leader actually the leader?
        if leadersGroup.getLeader() != leaderId:
            return

        if leadersGroup.onCooldown():
            return

        # This is a valid operation. Swap the two members places and update their statuses and leader variable.
        memberIds = leadersGroup.getMemberIds()
        members = leadersGroup.getMembers()
        oldToPromoteIndex = memberIds.index(toPromoteId)
        oldLeaderIndex = memberIds.index(leaderId)
        oldLeader = members[oldLeaderIndex]
        newLeader = members[oldToPromoteIndex]
        newLeader.status = GroupGlobals.STATUS_LEADER
        newLeader.leader = True
        oldLeader.status = GroupGlobals.STATUS_READY
        oldLeader.leader = False
        members[oldLeaderIndex] = newLeader
        members[oldToPromoteIndex] = oldLeader
        leadersGroup.setLeader(toPromoteId)
        leadersGroup.b_setMembers(members)
        leadersGroup.announce(f"{leader.getName()} has promoted {toPromote.getName()} to the group leader!")

    def requestTeamSwap(self, avId: int):

        requester: int = self.air.getAvatarIdFromSender()
        leader = self.air.getDo(requester)
        if leader is None:
            return

        toSwap = self.air.getDo(avId)
        if toSwap is None:
            return

        # Are the two users in the same group?
        leadersGroup = self.getGroup(leader)
        if leadersGroup is None or avId not in leadersGroup.getMemberIds():
            return

        # We can only allow this operation if the user is the leader or they are acting on themselves.
        selfSwap = avId == requester
        isLeader = leadersGroup.getLeader() == requester
        if not (selfSwap or isLeader):
            return

        if leadersGroup.onCooldown():
            return

        # Allow this operation.
        teamCycle = (GroupGlobals.TEAM_SPECTATOR, GroupGlobals.TEAM_FFA)
        memberIndex = leadersGroup.getMemberIds().index(avId)
        oldTeam = leadersGroup.members[memberIndex].team
        oldTeamIndex = teamCycle.index(oldTeam)
        newTeamIndex = oldTeamIndex + 1
        if newTeamIndex >= len(teamCycle):
            newTeamIndex = 0
        leadersGroup.members[memberIndex].team = teamCycle[newTeamIndex]

        leadersGroup.b_setMembers(leadersGroup.getMembers())

    def requestStart(self):
        requesterId = self.air.getAvatarIdFromSender()
        requester = self.air.getDo(requesterId)
        if requester is None:
            return

        group = self.getGroup(requester)
        if group is None:
            return

        # Is this the group leader?
        if group.getLeader() != requesterId:
            return

        # Is everyone ready?
        notReady = 0
        for member in group.getMembers():
            if member.status == GroupGlobals.STATUS_UNREADY:
                notReady += 1
        if notReady > 0:
            group.announce(f"{requester.getName()} wants to start the activity but {notReady} toon{'s' if notReady > 1 else ''} {'are' if notReady > 1 else 'is'} not ready!")
            return

        if len(group.getSpectators()) >= len(group.getMembers()):
            group.announce(f"{requester.getName()} wants to start the activity but everyone is spectating!")
            return

        group.startActivity()

    def updateStatus(self, code):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.getDo(avId)
        if av is None:
            return

        group = self.getGroup(av)
        if group is None:
            return

        # Don't update statuses unless they are ready/unready codes.
        if code not in (GroupGlobals.STATUS_UNREADY, GroupGlobals.STATUS_READY):
            return

        # Don't update the status if it's the leader. It doesn't matter.
        if avId == group.getLeader():
            return

        # Update the status and re update the members.
        member = group.getMember(avId)
        shouldUpdate = member.status != code
        member.status = code

        if shouldUpdate:
            group.d_setMembers(group.getMembers())
