from typing import List

from toontown.archipelago.util.net_utils import JSONMessagePart, JSONtoTextParser
from toontown.archipelago.packets.clientbound.clientbound_packet_base import ClientBoundPacketBase


# Sent to clients purely to display a message to the player. While various message types provide additional arguments,
# clients only need to evaluate the data argument to construct the human-readable message text.
# All other arguments may be ignored safely.
class PrintJSONPacket(ClientBoundPacketBase):

    def __init__(self, json_data):
        super().__init__(json_data)

        # Textual content of this message
        self.data: List[JSONMessagePart] = self.read_raw_field('data')

        # There are a lot more fields in this packet that I am ignoring as they are basically optional
        # type, receiving, item, found, team, slot, message, tags, countdown

    def handle(self, client):

        parser = JSONtoTextParser(client)
        self.debug(parser.parse(self.data))
        client.av.d_sendArchipelagoMessage(parser.parse(self.data))
