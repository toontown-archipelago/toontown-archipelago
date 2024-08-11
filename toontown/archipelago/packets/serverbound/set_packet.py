from typing import Any, Dict, List, TypedDict

from toontown.archipelago.packets.serverbound.serverbound_packet_base import ServerBoundPacketBase


class DataStorageOperation(TypedDict):
    operation: str
    value: Any


# Used to write data to the server's data storage, that data can then be shared across worlds or just saved for later.
# Values for keys in the data storage can be retrieved with a Get package, or monitored with a SetNotify package.
# Keys that start with _read_ cannot be set.
class SetPacket(ServerBoundPacketBase):

    def __init__(self):
        super().__init__()
        self.cmd = "Set"

        # The key to manipulate. Can never start with "_read".
        self.key: str = ''

        # The default value to use in case the key has no value on the server.
        self.default: Any = None

        # If true, the server will send a SetReply response back to the client.
        self.want_reply: bool = False

        # Operations to apply to the value, multiple operations can be present,
        # and they will be executed in order of appearance.
        self.operations: List[DataStorageOperation] = []

    def build(self) -> Dict[str, Any]:
        # Return all attributes
        return {
            'cmd': self.cmd,
            'key': self.key,
            'default': self.default,
            'want_reply': self.want_reply,
            'operations': self.operations,
        }

# Example of using this packet

# set_packet = SetPacket()
# set_packet.key = 'some_key'
# set_packet.default = 123
# await client.send_packet(set_packet)
