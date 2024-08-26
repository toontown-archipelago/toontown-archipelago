from typing import Any

from toontown.archipelago.packets.clientbound.clientbound_packet_base import ClientBoundPacketBase


# Sent to clients in response to a Set package if you want_reply was set to true, or if the client has registered to
# receive updates for a certain key using the SetNotify package.
# SetReply packages are sent even if a Set package did not alter the value for the key.
class SetReplyPacket(ClientBoundPacketBase):

    def __init__(self, json_data):
        super().__init__(json_data)

        # The key that was updated.
        self.key: str = self.read_raw_field('key')

        # The new value for the key.
        self.value: Any = self.read_raw_field('value')

        # The value the key had before it was updated. Not present on "_read" prefixed special keys.
        self.original_value: Any = self.read_raw_field('original_value')

    def handle(self, client):
        self.debug("Handling packet")

        if self.key.startswith(f'slot{client.slot}:'):
            client.av.handle_ap_data_update({self.key.split(':')[1]: self.value})
