from toontown.archipelago.packets.clientbound.clientbound_packet_base import ClientBoundPacketBase


# Sent to clients if the server caught a problem with a packet. This only occurs for errors that are explicitly
# checked for.
class InvalidPacket(ClientBoundPacketBase):

    def __init__(self, json_data):
        super().__init__(json_data)

        # The PacketProblemType that was detected in the packet.
        self.type: str = self.read_raw_field('type')

        # The cmd argument of the faulty packet, will be None if the cmd failed to be parsed.
        self.original_cmd: str = self.read_raw_field('original_cmd')

        # A descriptive message of the problem at hand.
        self.text: str = self.read_raw_field('text')

    def handle(self, client):
        self.debug(f"Invalid packet received:\n<{self.original_cmd}>: {self.type}: {self.text}")
