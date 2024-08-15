from typing import Any, Dict

from toontown.archipelago.packets.clientbound.clientbound_packet_base import ClientBoundPacketBase


# Sent to clients as a response the Get package.
class RetrievedPacket(ClientBoundPacketBase):

    def __init__(self, json_data):
        super().__init__(json_data)

        # A key-value collection containing all the values for the keys requested in the Get package.
        # If a requested key was not present in the server's data, the associated value will be null.
        # Additional arguments added to the Get package that triggered this Retrieved will also be passed along.
        self.keys: Dict[str, Any] = self.read_raw_field('keys')

    def handle(self, client):
        self.debug("Handling packet")

        # Filter the dict for only our private keys specifically,
        # and pass them how the handler expects.
        realKeys = {i.split(':')[1]:v
                    for i, v in self.keys.items()
                    if i.startswith(f'slot{client.slot}:')}
        client.av.handle_ap_data_update(realKeys)
