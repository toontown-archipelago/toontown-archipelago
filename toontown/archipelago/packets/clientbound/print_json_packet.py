from copy import deepcopy
from typing import List

from toontown.archipelago.util import global_text_properties
from toontown.archipelago.util.HintContainer import HintedItem
from toontown.archipelago.util.net_utils import JSONMessagePart, JSONtoTextParser, JSONPartFormatter, NetworkItem
from toontown.archipelago.packets.clientbound.clientbound_packet_base import ClientBoundPacketBase


# Sent to clients purely to display a message to the player. While various message types provide additional arguments,
# clients only need to evaluate the data argument to construct the human-readable message text.
# All other arguments may be ignored safely.
class PrintJSONPacket(ClientBoundPacketBase):

    def __init__(self, json_data):
        super().__init__(json_data)

        # Textual content of this message
        self.data: List[JSONMessagePart] = self.read_raw_field('data')

        # PrintJsonType of this message (optional)
        self.type: str = self.read_raw_field('type', ignore_missing=True)

        # Destination Player's ID
        self.receiving: int = self.read_raw_field('receiving', ignore_missing=True)

        # Source player's ID location ID item ID and item flags
        self.item: NetworkItem = self.read_raw_field('item', ignore_missing=True)

        # Whether the location hinted for was checked
        self.found: bool = self.read_raw_field('found', ignore_missing=True)

        # There are a lot more fields in this packet that I am ignoring as they are basically optional
        # team, slot, message, tags, countdown

    def is_hint_packet(self) -> bool:
        return self.type == 'Hint'

    def parse_hint(self, client) -> HintedItem:
        """
        Reads this packet when we know for sure it is a hint packet. Will cause errors if this packet is not a hint
        packet, use self.is_hint_packet() before calling this
        """
        location_name = client.get_location_name(self.item.location)
        player_name = client.get_player_name(self.item.player)
        return HintedItem(self.receiving, self.item, player_name, location_name, self.found)

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

        # If this is a hint packet, go ahead and add the hint to the hint cache
        if self.is_hint_packet():
            hint = self.parse_hint(client)
            client.av.archipelago_session.getHintContainer().addHint(hint)
            client.av.sendHint(hint)
