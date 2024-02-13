from typing import Any, Dict

from toontown.archipelago.packets.serverbound.serverbound_packet_base import ServerBoundPacketBase


# Sent to server to request a ReceivedItems packet to synchronize items.
class SyncPacket(ServerBoundPacketBase):

    def __init__(self):
        super().__init__()
        self.cmd = "Sync"

        # No arguments for this packet

    def build(self) -> Dict[str, Any]:
        # Return all attributes
        return {'cmd': self.cmd}

# Example of using this packet

# sync_packet = SyncPacket()
# await client.send_packet(sync_packet)
