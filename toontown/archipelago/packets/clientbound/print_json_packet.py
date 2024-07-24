from copy import deepcopy
from typing import List

from toontown.archipelago.util import global_text_properties
from toontown.archipelago.util.net_utils import JSONMessagePart, JSONtoTextParser, JSONPartFormatter
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

        # Parser for outputting to console if we want debug
        self.debug(JSONtoTextParser(client).parse(deepcopy(self.data)))

        # Our parser that is Panda3D friendly
        parser = JSONPartFormatter(deepcopy(self.data), client)
        formatted_parts = parser.get_formatted_parts()

        # Loop through all the parts and build a string
        ret = ''
        for part in formatted_parts:
            color = part['color']
            text = part['text']
            p3dcolor = global_text_properties.get_property_code_from_json_code(color)
            ret += f"\1{p3dcolor}\1{text}\2"

        client.av.queueArchipelagoMessage(ret)
        client.av.archipelago_session.datastore.parsePrintJSON(self._raw_data)
