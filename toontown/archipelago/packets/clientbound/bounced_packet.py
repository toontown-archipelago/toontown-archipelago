from typing import List, Dict, Any

from toontown.archipelago.packets.clientbound.clientbound_packet_base import ClientBoundPacketBase


# Sent to clients after a client requested this message be sent to them, more info in the Bounce package.
class BouncedPacket(ClientBoundPacketBase):

    def __init__(self, json_data):
        super().__init__(json_data)

        # Optional. Game names this message is targeting
        self.games: List[str] = self.read_raw_field("games", ignore_missing=True)

        # Optional. Player slot IDs that this message is targeting
        self.slots: List[int] = self.read_raw_field('slots', ignore_missing=True)

        # Optional. Client Tags this message is targeting
        self.tags: List[str] = self.read_raw_field('tags', ignore_missing=True)

        # The data in the Bounce package copied
        self.data: Dict[Any, Any] = self.read_raw_field('data')

    def handle(self, client):
        print("[AP Client] Received Bounced packet")
