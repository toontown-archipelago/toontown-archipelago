from typing import Any, Dict

from toontown.archipelago.packets.serverbound.serverbound_packet_base import ServerBoundPacketBase


# Basic chat command which sends text to the server to be distributed to other clients.
class SayPacket(ServerBoundPacketBase):

    def __init__(self):
        super().__init__()
        self.cmd = "Say"

        self.text: str = ''

    def build(self) -> Dict[str, Any]:
        # Return all attributes
        return {
            'cmd': self.cmd,
            'text': self.text
        }

# Example of using this packet

# say_packet = SayPacket()
# say_packet.text = "Hello guys :)"
# await client.send_packet(say_packet)
