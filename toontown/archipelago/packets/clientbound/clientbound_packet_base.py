from toontown.archipelago.packets.archipelago_packet_base import ArchipelagoPacketBase


class ClientBoundPacketBase(ArchipelagoPacketBase):
    packet_type = ArchipelagoPacketBase.PacketType.CLIENT_BOUND

    def __init__(self, json_data):
        super().__init__()
        self._raw_data = json_data
        self.command = self.read_raw_field("cmd")

    def handle(self, client):
        raise NotImplementedError

    def valid(self):
        return self.packet_type == ArchipelagoPacketBase.PacketType.CLIENT_BOUND
