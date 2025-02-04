import dataclasses


@dataclasses.dataclass
class GroupMemberStruct:
    """
    Directly mirrors the GroupMember struct contained in the astron file.
    Provides an easy way to communicate group member information over the network.
    """
    avId: int
    team: int
    status: int
    leader: bool

    def to_struct(self):
        return [self.avId, self.team, self.status, self.leader]

    @classmethod
    def from_struct(cls, entry):
        return cls(*entry)
