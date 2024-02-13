from typing import List

from toontown.archipelago.net_utils import JSONMessagePart
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

    # Returns a clean string safe to display that replaces IDs with what they should display to the player as
    def parse_json_message_part(self, client, part: JSONMessagePart) -> str:

        # If this part has no type, then it is meant to be a simple string
        if 'type' not in part:
            return part['text']

        _type = part['type']

        # Handle the case this part is a player ID
        if _type == 'player_id':
            return client.get_slot_info(part['text']).name

        # Handle the case where this is an item ID
        if _type == 'item_id':
            return client.get_item_info(part['text'])

        # Handle the case where this is a location ID
        if _type == 'location_id':
            return client.get_location_info(part['text'])

        # Not sure what other case we could have here
        return f'unknown text type [{_type}]'

    def handle(self, client):
        msg = '[AP Message] '
        for part in self.data:
            msg += self.parse_json_message_part(client, part)

        print(msg)
