from typing import Dict, Any

from toontown.archipelago.packets.archipelago_packet_base import ArchipelagoPacketBase


# Abstraction for all possible packets we can receive from the server
# Classes that extend this one should be instantied by the client to be sent to the server
class ServerBoundPacketBase(ArchipelagoPacketBase):
    packet_type = ArchipelagoPacketBase.PacketType.SERVER_BOUND

    def __init__(self):
        super().__init__()
        self.cmd: str = 'Undefined'

    def valid(self):
        return self.packet_type == ArchipelagoPacketBase.PacketType.SERVER_BOUND

    # A method for child classes to override, build a json serializable dict that is safe to send
    def build(self) -> Dict[str, Any]:
        raise NotImplementedError

    # Override the behavior of the raw_data attribute to just build the packet
    @property
    def raw_data(self):
        return self.build()
