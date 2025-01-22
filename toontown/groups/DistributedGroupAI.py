from direct.distributed.DistributedObjectAI import DistributedObjectAI

from toontown.groups.GroupBase import GroupBase
from toontown.toon.DistributedToonAI import DistributedToonAI


class DistributedGroupAI(DistributedObjectAI, GroupBase):

    def __init__(self, air, leader: DistributedToonAI):
        DistributedObjectAI.__init__(self, air)
        GroupBase.__init__(self, leader.getDoId())

    def getToons(self):
        """
        Returns a list of DistributedToonAI instances in this group.
        """
        dos = []
        for doId in self.getMembers():
            toon = self.air.getDo(doId)
            if toon is None:
                continue

            dos.append(toon)

        return dos

    """
    Astron Methods (Outgoing)
    """

    def b_setLeader(self, leader: int):
        self.setLeader(leader)
        self.d_SetLeader(leader)

    def d_SetLeader(self, leader: int):
        self.sendUpdate('setLeader', [leader])

    def b_setMembers(self, members: list[int]):
        self.setMembers(members)
        self.d_setMembers(self.getMembers())

    def d_setMembers(self, members: list[int]):
        self.sendUpdate('setMembers', [members])

    def b_setCapacity(self, capacity: int):
        self.setCapacity(capacity)
        self.d_setCapacity(capacity)

    def d_setCapacity(self, capacity: int):
        self.sendUpdate('setCapacity', [capacity])
