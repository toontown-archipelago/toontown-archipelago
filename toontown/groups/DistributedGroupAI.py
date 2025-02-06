import time

from direct.distributed.DistributedObjectAI import DistributedObjectAI

from toontown.groups import GroupGlobals
from toontown.groups.GroupBase import GroupBase
from toontown.groups.GroupMemberStruct import GroupMemberStruct
from toontown.toon.DistributedToonAI import DistributedToonAI


class DistributedGroupAI(DistributedObjectAI, GroupBase):

    def __init__(self, air, leader: DistributedToonAI):
        DistributedObjectAI.__init__(self, air)
        GroupBase.__init__(self, leader.getDoId())
        self.activityStartCooldown = 0

    def getToons(self):
        """
        Returns a list of DistributedToonAI instances in this group.
        """
        dos = []
        for doId in self.getMemberIds():
            toon = self.air.getDo(doId)
            if toon is None:
                continue

            dos.append(toon)

        return dos

    def getSpectators(self) -> list[int]:
        return [member.avId for member in self.getMembers() if member.team == GroupGlobals.TEAM_SPECTATOR]

    def announce(self, message: str) -> None:
        """
        Announces a message to the toons in the group.
        """
        self.d_announce(message)

    def onCooldown(self) -> bool:
        if self.activityStartCooldown > time.time():
            return True
        return False

    def startActivity(self) -> None:

        if self.onCooldown():
            return

        self.announce("Activity starting...")
        self.activityStartCooldown = time.time() + 6
        minigame = self.air.minigameMgr.createMinigame(self.getMemberIds(), self.zoneId, newbieIds=[], spectatorIds=self.getSpectators(), startingVotes=None, metagameRound=-1)
        self.d_setMinigameZone(minigame)

    """
    Astron Methods (Outgoing)
    """

    def b_setMembers(self, members: list[GroupMemberStruct]):
        self.setMembers(members)
        self.d_setMembers(members)

    def d_setMembers(self, members: list[GroupMemberStruct]):
        self.sendUpdate('setMembers', [[member.to_struct() for member in members]])

    def b_setCapacity(self, capacity: int):
        self.setCapacity(capacity)
        self.d_setCapacity(capacity)

    def d_setCapacity(self, capacity: int):
        self.sendUpdate('setCapacity', [capacity])

    def d_announce(self, message: str):
        """
        Sends a message to all members in the group. It is probably ideal if this isn't just sending raw strings over
        the network for localizing purposes, but this is fine for now.
        """
        self.sendUpdate('announce', [message])

    def d_setMinigameZone(self, minigame):
        """
        Forces all members to teleport to a newly created minigame.
        """
        for avId in self.getMemberIds():
            self.sendUpdateToAvatarId(avId, 'setMinigameZone', [minigame.zone, minigame.gameId])
