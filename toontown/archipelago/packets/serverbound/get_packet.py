from typing import Any, Dict, List

from toontown.archipelago.packets.serverbound.serverbound_packet_base import ServerBoundPacketBase


# Used to request a single or multiple values from the server's data storage, see the Set package for how to write
# values to the data storage. A Get package will be answered with a Retrieved package.
class GetPacket(ServerBoundPacketBase):

    def __init__(self):
        super().__init__()
        self.cmd = "Get"

        # Keys to retrieve the values for.
        self.keys: List[str] = []

    def build(self) -> Dict[str, Any]:
        # Return all attributes
        return {
            'cmd': self.cmd,
            'keys': self.keys
        }

# Example of using this packet

# get_packet = GetPacket()
# get_packet.keys.append('some_data')
# await client.send_packet(get_packet)
