from typing import Any, Dict, List

from toontown.archipelago.packets.serverbound.serverbound_packet_base import ServerBoundPacketBase


# Sent to the server to inform it of locations the client has seen, but not checked. Useful in cases in which the
# item may appear in the game world, such as 'ledge items' in A Link to the Past.
# The server will always respond with a LocationInfo packet with the items located in the scouted location.
class LocationScoutsPacket(ServerBoundPacketBase):

    def __init__(self):
        super().__init__()
        self.cmd = "LocationScouts"

        # The ids of the locations seen by the client. May contain any number of locations, even ones sent before; \
        # duplicates do not cause issues with the Archipelago server.
        self.locations: List[int] = []

        # If non-zero, the scouted locations get created and broadcast as a player-visible hint.
        # If 2 only new hints are broadcast, however this does not remove them from the LocationInfo reply.
        self.create_as_hint: int = 0

    def build(self) -> Dict[str, Any]:
        # Return all attributes
        return {
            'cmd': self.cmd,
            'locations': self.locations,
            'create_as_hint': self.create_as_hint
        }

# Example of using this packet

# location_scouts_packet = LocationScoutsPacket()
# location_scouts_packet.locations.append(some_location_id)
# location_scouts_packet.create_as_hint = 2  # only broadcast if this is new
# await client.send_packet(location_scouts_packet)
