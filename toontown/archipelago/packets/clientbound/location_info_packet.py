from typing import List

from toontown.archipelago.util.net_utils import NetworkItem
from toontown.archipelago.packets.clientbound.clientbound_packet_base import ClientBoundPacketBase


# Sent to clients to acknowledge a received LocationScouts packet
# and responds with the item in the location(s) being scouted.
class LocationInfoPacket(ClientBoundPacketBase):

    def __init__(self, json_data):
        super().__init__(json_data)

        # Contains list of item(s) in the location(s) scouted.
        self.locations: List[NetworkItem] = json_data['locations']

    def handle(self, client):

        for location in self.locations:
            self.debug(f"{location.player}'s {location.item} is at {location.location}")
