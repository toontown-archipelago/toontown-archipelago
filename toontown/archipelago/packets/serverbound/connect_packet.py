from typing import Any, Dict, List

from toontown.archipelago.packets.serverbound.serverbound_packet_base import ServerBoundPacketBase
from toontown.archipelago.util.utils import Version


# Sent by the client to initiate a connection to an Archipelago game session.
class ConnectPacket(ServerBoundPacketBase):
    ITEMS_HANDLING_FLAG_SEND_ITEMS = 0b001  # Send items to other worlds
    ITEMS_HANDLING_FLAG_RECEIVE_ITEMS = 0b010  # Receive items from other worlds
    ITEMS_HANDLING_FLAG_GET_SENT_STARTING_ITEMS = 0b100  # Have our starting inventory sent

    # Default behavior, send, receive items and get sent starting inventory
    ITEMS_HANDLING_ALL_FLAGS = ITEMS_HANDLING_FLAG_SEND_ITEMS | ITEMS_HANDLING_FLAG_RECEIVE_ITEMS | ITEMS_HANDLING_FLAG_GET_SENT_STARTING_ITEMS

    # Signifies that this client is a reference client, its usefulness is mostly in debugging to compare client
    # behaviours more easily.
    TAG_AP = "AP"
    # Client participates in the DeathLink mechanic, therefore will send and receive DeathLink bounce packets
    TAG_DEATHLINK = "DeathLink"
    # Tells the server that this client will not send locations and is actually a Tracker. When specified and used with
    # empty or null game in Connect, game and game's version validation will be skipped.
    TAG_TRACKER = "Tracker"
    # Tells the server that this client will not send locations and is intended for chat. When specified and used with
    # empty or null game in Connect, game and game's version validation will be skipped.
    TAG_TEXTONLY = "TextOnly"

    def __init__(self):
        super().__init__()

        self.cmd = "Connect"

        # If the game session requires a password, it should be passed here.
        self.password: str = ''
        # The name of the game the client is playing. Example: A Link to the Past
        self.game: str = 'Toontown'
        # The player name for this client.
        self.name: str = 'Unnamed Player'
        # Unique identifier for player client.
        self.uuid: str = 'Undefined UUID'
        # An object representing the Archipelago version this client supports.
        self.version: Version = None
        # Flags configuring which items should be sent by the server. Read below for individual flags.
        self.items_handling: int = 0
        # Denotes special features or capabilities that the sender is capable of. Tags
        self.tags: List[str] = []
        # If true, the Connect answer will contain slot_data
        self.slot_data: bool = False

    def build(self) -> Dict[str, Any]:
        # Return all attributes
        return {
            'cmd': self.cmd,
            'password': self.password,
            'name': self.name,
            'game': self.game,
            'uuid': self.uuid,
            'version': self.version,
            'items_handling': self.items_handling,
            'tags': self.tags,
            'slot_data': self.slot_data,
        }

# Example of using this packet

# connect_packet = ConnectPacket()
# connect_packet.game = "Toontown"
# connect_packet.name = "devvydontTT"
# connect_packet.uuid = 'blabhlablhba'
# connect_packet.version = Version(0, 4, 4)
# connect_packet.items_handling = ConnectPacket.ITEMS_HANDLING_ALL_FLAGS
# connect_packet.tags = [ConnectPacket.TAG_DEATHLINK]
# connect_packet.slot_data = True
# await client.send_packet(connect_packet)
