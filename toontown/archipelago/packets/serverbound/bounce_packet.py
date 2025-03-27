from typing import Any, Dict, List

from toontown.archipelago.packets.serverbound.connect_packet import ConnectPacket
from toontown.archipelago.packets.serverbound.serverbound_packet_base import ServerBoundPacketBase


# Send this message to the server, tell it which clients should receive the message and the server will
# forward the message to all those targets to which any one requirement applies.
class BouncePacket(ServerBoundPacketBase):

    def __init__(self):
        super().__init__()
        self.cmd = "Bounce"

        # 	Optional. Game names that should receive this message
        self.games: List[str] = []

        # Optional. Player IDs that should receive this message
        self.slots: List[int] = []

        # Optional. Client tags that should receive this message
        self.tags: List[str] = []

        # Any data you want to send
        self.data: Dict[Any, Any] = {}

    # Call do add the deathlink data to send within this packet
    def add_deathlink_data(self, toon, cause=None):
        self.tags.append(ConnectPacket.TAG_DEATHLINK)
        self.data['time'] = globalClock.getRealTime()
        if toon.getDeathReason() is not None:
            self.data['cause'] = toon.getDeathReason().format(toon)

        # Documentation specifices this to either be slot name or name from a mp game.
        # Checking the AP discord confirms that in implementation, this is only used to verify if it was yourself.
        # Temporarily making this a string again to avoid issues with other games
        self.data['source'] = str(abs(int(hash(toon.getUUID())/10000000000)))

    def add_ringlink_data(self, toon, amount=0):
        self.tags.append(ConnectPacket.TAG_RINGLINK)
        self.data['time'] = globalClock.getRealTime()
        self.data['source'] = abs(int(hash(toon.getUUID())/10000000000))
        self.data['amount'] = amount

    def build(self) -> Dict[str, Any]:
        # Return all attributes
        return {
            'cmd': self.cmd,
            'games': self.games,
            'slots': self.slots,
            'tags': self.tags,
            'data': self.data,
        }

# Example of using this packet

# bounce_packet = BouncePacket()
# bounce_packet.tags.append("DeathLink")
# await client.send_packet(bounce_packet)
