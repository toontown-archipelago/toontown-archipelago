from typing import Any, Dict, List

from toontown.archipelago.packets.serverbound.serverbound_packet_base import ServerBoundPacketBase


# Sent to server to inform it of locations that the client has checked. Used to inform the server of new checks
# that are made, as well as to sync state.
class LocationChecksPacket(ServerBoundPacketBase):

    def __init__(self):
        super().__init__()
        self.cmd = "LocationChecks"

        # The ids of the locations checked by the client. May contain any number of checks, even ones sent before;
        # duplicates do not cause issues with the Archipelago server.
        self.locations: List[int] = []

    def build(self) -> Dict[str, Any]:
        # Return all attributes
        return {
            'cmd': self.cmd,
            'locations': self.locations
        }

# Example of using this packet

# location_checks_packet = LocationChecksPacket()
# location_checks_packet.locations.append(some_location_id)
# await client.send_packet(location_checks_packet)
