# Astron struct dataclass to be sent to clients to cache currently online toons.
# Contains minimal information that clients need to construct AvatarHandles.
import dataclasses
from dataclasses import dataclass
from typing import List

from toontown.friends.FriendHandle import FriendHandle
from toontown.toon.ToonDNA import ToonDNA

NO_PET = 0


@dataclass
class OnlineToon:
    avId: int  # Toon ID
    name: str  # Current Name
    dna:  bytes  # DNA String

    def struct(self) -> List[int]:
        fields = dataclasses.asdict(self).values()
        return list(fields)

    def make_dna(self) -> ToonDNA:
        return ToonDNA(dnastring=self.dna)

    # Constructs a FriendHandle instance from this instance to be used for the friends list.
    def handle(self) -> FriendHandle:
        return FriendHandle(self.avId, self.name, self.make_dna(), NO_PET)

    @classmethod
    def from_struct(cls, info_array: List[int]):
        return cls(*info_array)
