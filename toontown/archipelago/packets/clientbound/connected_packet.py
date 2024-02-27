from typing import List, Any, Dict

from toontown.archipelago.apclient.ap_client_enums import APClientEnums
from toontown.archipelago.util.net_utils import NetworkPlayer, NetworkSlot
from toontown.archipelago.packets.clientbound.clientbound_packet_base import ClientBoundPacketBase


# Sent to clients when the connection handshake is successfully completed.
class ConnectedPacket(ClientBoundPacketBase):

    def __init__(self, json_data):
        super().__init__(json_data)

        # Your team number. See NetworkPlayer for more info on team number.
        self.team: int = self.read_raw_field('team', ignore_missing=True)

        # Your slot number on your team. See NetworkPlayer for more info on the slot number.
        self.slot: int = self.read_raw_field('slot', ignore_missing=True)

        # List denoting other players in the multiworld, whether connected or not.
        self.players: List[NetworkPlayer] = self.read_raw_field('players', ignore_missing=True)

        # Contains ids of remaining locations that need to be checked. Useful for trackers, among other things.
        self.missing_locations: List[int] = self.read_raw_field('missing_locations', ignore_missing=True)

        # Contains ids of all locations that have been checked. Useful for trackers, among other things.
        # Location ids are in the range of ± 2^53-1.
        self.checked_locations: List[int] = self.read_raw_field('checked_locations', ignore_missing=True)

        # Contains a json object for slot related data, differs per game. Empty if not required.
        # Not present if slot_data in Connect is false.
        self.slot_data: Dict[str, Any] = self.read_raw_field('slot_data', ignore_missing=True)

        # maps each slot to a NetworkSlot information.
        self.slot_info: Dict[str, NetworkSlot] = self.read_raw_field('slot_info', ignore_missing=True)

        # Number of hint points that the current player has.
        self.hint_points: int = self.read_raw_field('hint_points', ignore_missing=True)

    def get_slot_info(self, slot: int) -> NetworkSlot:
        return self.slot_info[str(slot)]

    # Creates a dict mapping slot ID -> network slot object for later retrieval
    def update_client_slot_cache(self, client):

        # Clear the cache, and populate it
        client.slot = self.slot
        client.slot_id_to_slot_name.clear()
        for id_string, network_slot in self.slot_info.items():
            client.slot_id_to_slot_name[int(id_string)] = network_slot

    def handle(self, client):
        self.debug(f"[AP Client] Successfully connected to the Archipelago server as {self.get_slot_info(self.slot).name}"
              f" playing {self.get_slot_info(self.slot).game}")

        # Store any information in the cache that we may need later
        self.update_client_slot_cache(client)

        # We have a valid connection, set client state to connected
        client.state = APClientEnums.CONNECTED

        # todo ew ew ew ew this is so gross fix later pls
        client.av.archipelago_session.sync()
