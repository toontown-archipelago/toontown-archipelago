from typing import List, Any, Dict

from toontown.archipelago.apclient.ap_client_enums import APClientEnums
from toontown.archipelago.definitions import locations
from toontown.archipelago.definitions.util import ap_location_name_to_id, get_zone_discovery_id
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

        client.av.b_setName(client.slot_name)

        # Is this this toon's first time? If so reset the toon's stats and initialize their settings from their YAML
        if len(self.checked_locations) == 0:

            #  Reset stats
            client.av.newToon()

            # Set their max HP
            client.av.b_setMaxHp(self.slot_info.get('starting_hp', 15))
            client.av.b_setHp(client.av.getMaxHp())

            # Set their starting money
            client.av.b_setMoney(50)

            # Set their starting gag xp multiplier
            client.av.b_setBaseGagSkillMultiplier(self.slot_info.get('starting_gag_xp_multiplier', 2))

        # Login location rewarding
        track_one_check = ap_location_name_to_id(locations.STARTING_TRACK_ONE_LOCATION)
        track_two_check = ap_location_name_to_id(locations.STARTING_TRACK_TWO_LOCATION)
        client.av.addCheckedLocation(track_one_check)
        client.av.addCheckedLocation(track_two_check)