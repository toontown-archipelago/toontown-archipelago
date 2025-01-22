from direct.distributed.DistributedObject import DistributedObject

from toontown.groups.GroupBase import GroupBase


class DistributedGroup(DistributedObject, GroupBase):

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        GroupBase.__init__(self, GroupBase.NoLeader)

    def generate(self):
        DistributedObject.generate(self)

    def __localToonInGroup(self) -> bool:
        return base.localAvatar.getDoId() in self.getMembers()

    """
    Methods used for GUI management.
    """

    def render(self):
        if not self.__localToonInGroup():
            return

        print(f'Rendering Group GUI: {self.getMembers()}')

    def cleanup(self):
        print(f'Cleaning up Group GUI: {self.getMembers()}')

    """
    Methods called from the AI over astron.
    """
    def setLeader(self, leader: int):
        super().setLeader(leader)
        self.render()

    def setMembers(self, members: list[int]):
        super().setMembers(members)
        self.render()
