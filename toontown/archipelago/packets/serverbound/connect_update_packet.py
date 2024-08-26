from typing import Any, Dict, List

from toontown.archipelago.packets.serverbound.serverbound_packet_base import ServerBoundPacketBase


# Sent by the client to initiate a connection to an Archipelago game session.
class ConnectUpdatePacket(ServerBoundPacketBase):
    def __init__(self):
        super().__init__()

        self.cmd = "ConnectUpdate"

        # Flags configuring which items should be sent by the server. Read below for individual flags.
        self.items_handling: int = None
        # Denotes special features or capabilities that the sender is capable of. Tags
        self.tags: List[str] = None

    def build(self) -> Dict[str, Any]:
        # Return all attributes
        return {
            'cmd': self.cmd,
            'items_handling': self.items_handling,
            'tags': self.tags
        }

# Example of using this packet

# connect_update_packet = ConnectPacket()
# connect_packet.items_handling = ConnectPacket.ITEMS_HANDLING_ALL_FLAGS
# connect_packet.tags = [ConnectPacket.TAG_DEATHLINK]
# client.send_packet(connect_packet)