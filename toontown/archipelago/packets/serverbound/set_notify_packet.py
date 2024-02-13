from typing import Any, Dict, List

from toontown.archipelago.packets.serverbound.serverbound_packet_base import ServerBoundPacketBase


# Used to register your current session for receiving all SetReply packages of certain keys to allow your
# client to keep track of changes.
class SetNotifyPacket(ServerBoundPacketBase):

    def __init__(self):
        super().__init__()
        self.cmd = "SetNotify"

        # Keys to receive all SetReply packages for.
        self.keys: List[str] = []

    def build(self) -> Dict[str, Any]:
        # Return all attributes
        return {
            'cmd': self.cmd,
            'keys': self.keys
        }

# Example of using this packet

# set_notify_packet = SetNotifyPacket()
# set_notify_packet.keys.append('some_key')
# await client.send_packet(set_notify_packet)
