# Astron struct wrapper class for communicating information between the AI and the client.
# See DistributedArchipelagoManager.sync() in ttap.dc
import dataclasses
from dataclasses import dataclass
from typing import List


@dataclass
class ArchipelagoInformation:
    avId: int
    slotId: int
    teamId: int

    def struct(self) -> List[int]:
        fields = dataclasses.asdict(self).values()
        return list(fields)

    @classmethod
    def from_struct(cls, info_array: List[int]):
        return cls(*info_array)
