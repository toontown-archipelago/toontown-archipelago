from typing import Any, Dict

from toontown.archipelago.util.net_utils import ClientStatus
from toontown.archipelago.packets.serverbound.serverbound_packet_base import ServerBoundPacketBase


# Sent to the server to update on the sender's status. Examples include readiness or goal completion.
# (Example: defeated Ganon in A Link to the Past)
class StatusUpdatePacket(ServerBoundPacketBase):

    def __init__(self):
        super().__init__()
        self.cmd = "StatusUpdate"

        # One of Client States. Send as int. Follow the link for more information. (ClientStatus class enum)
        self.status: ClientStatus = ClientStatus.CLIENT_UNKNOWN

    def build(self) -> Dict[str, Any]:
        # Return all attributes
        return {
            'cmd': self.cmd,
            'status': self.status
        }

# Example of using this packet

# status_update_packet = StatusUpdatePacket()
# status_update_packet.status = ClientStatus.CLIENT_CONNECTED
# await client.send_packet(status_update_packet)
