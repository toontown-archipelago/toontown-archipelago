# Astron struct dataclass to be sent to clients to cache currently online toons.
# Contains minimal information that clients need to construct AvatarHandles.
import dataclasses
from dataclasses import dataclass
from typing import List


@dataclass
class OnlineToon:
    avId: int  # Toon ID
    name: str  # Current Name

    def struct(self) -> List[int]:
        fields = dataclasses.asdict(self).values()
        return list(fields)

    @classmethod
    def from_struct(cls, info_array: List[int]):
        return cls(*info_array)
