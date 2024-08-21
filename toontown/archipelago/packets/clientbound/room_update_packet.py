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

    def handle_hint_points_update(self, av):

        # This packet did not contain the hint_points field, nothing to update
        if self.hint_points is None:
            return

        new_hint_points = self.hint_points
        av.hintPoints = new_hint_points

    def handle_checked_locations_update(self, av):
        # Packet did not contain checked locations, nothing to update.
        if self.checked_locations is None:
            return
        
        av.receiveCheckedLocations(self.checked_locations)

    def handle(self, client):

        self.debug("Handling packet")

        # Attempt to handle a hint point update if this packet contains one
        self.handle_hint_points_update(client.av)
        self.handle_checked_locations_update(client.av)

