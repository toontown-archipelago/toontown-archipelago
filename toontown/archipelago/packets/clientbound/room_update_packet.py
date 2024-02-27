from typing import List

from toontown.archipelago.util.net_utils import NetworkPlayer
from toontown.archipelago.packets.clientbound.connected_packet import ConnectedPacket
from toontown.archipelago.packets.clientbound.room_info_packet import RoomInfoPacket


# RoomUpdate may contain the same arguments from RoomInfo and, once authenticated, arguments
# from Connected with the following exceptions:
# - players
# - checked_locations
# - missing_locations

# All arguments for this packet are optional, only changes are sent.
class RoomUpdatePacket(RoomInfoPacket, ConnectedPacket):

    def __init__(self, json_data):

        # Initialize all the fields within RoomInfo and Connected if present
        RoomInfoPacket.__init__(self, json_data)
        ConnectedPacket.__init__(self, json_data)

        # Sent in the event of an alias rename. Always sends all players, whether connected or not.
        self.players: List[NetworkPlayer] = self.read_raw_field('players', ignore_missing=True)

        # May be a partial update, containing new locations that were checked,
        # especially from a coop partner in the same slot.
        self.checked_locations: List[int] = self.read_raw_field('checked_locations', ignore_missing=True)

    def handle(self, client):
        self.debug(f"[AP Client] Handling RoomUpdate packet")
