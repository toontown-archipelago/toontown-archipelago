import random
from typing import List, Any, Dict

from apworld.toontown import locations, TPSanity
from apworld.toontown.fish import FishProgression

from toontown.archipelago.apclient.ap_client_enums import APClientEnums
from toontown.archipelago.definitions.util import ap_location_name_to_id
from toontown.archipelago.packets.serverbound.status_update_packet import StatusUpdatePacket
from toontown.archipelago.packets.serverbound.connect_packet import ConnectPacket
from toontown.archipelago.packets.serverbound.connect_update_packet import ConnectUpdatePacket
from toontown.archipelago.util.net_utils import NetworkPlayer, NetworkSlot, ClientStatus, SlotType
from toontown.archipelago.packets.clientbound.clientbound_packet_base import ClientBoundPacketBase
from toontown.fishing import FishGlobals
from otp.otpbase import OTPGlobals
from toontown.toonbase import ToontownGlobals


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
        # client.team = self.team  # todo when AP releases actual team functionality use this
        client.team = self.slot_data.get('team', 0)  # temp fix to allow team functionality
        client.slot_id_to_slot_name.clear()
        for id_string, network_slot in self.slot_info.items():
            client.slot_id_to_slot_name[int(id_string)] = network_slot

        # If there wasn't a "console player", add it, this is so when we cheat items in we don't crash the socket thread
        if 0 not in client.slot_id_to_slot_name:
            client.slot_id_to_slot_name[0] = NetworkSlot("Console", "No game", SlotType.spectator, [])

        # Cache this successful connection on the ai
        slot_info = self.get_slot_info(self.slot)
        simbase.air.cacheArchipelagoConnectInformation(client.av.doId, slot_info.name, client.address)

    def handle_first_time_player(self, av):

        #  Reset stats
        av.newToon()

        # Set their max HP
        av.b_setMaxHp(self.slot_data.get('starting_laff', 15))
        av.b_setHp(av.getMaxHp())

        # Set their starting money
        av.b_setMoney(self.slot_data.get('starting_money', 50))

        # Set their starting task capacity

        av.b_setQuestCarryLimit(self.slot_data.get('starting_task_capacity', 4))

        # Set their starting gag xp multiplier
        av.b_setBaseGagSkillMultiplier(self.slot_data.get('base_global_gag_xp', 2))

        # Give them gold rod if set in yaml
        fish_progression = FishProgression(self.slot_data.get('fish_progression', 3))
        need_gold_rod = fish_progression in (FishProgression.Licenses, FishProgression.Nonne)
        if need_gold_rod:
            av.b_setFishingRod(FishGlobals.MaxRodId)

    # Given the option defined in the YAML for RNG generation and the seed of the AP playthrough
    # Return a new modified seed based on what option was chosen in the YAML
    #     option_global = 0
    #     option_slot_name = 1
    #     option_unique = 2
    #     option_wild = 3
    def handle_seed_generation_type(self, av, seed, option):

        option_global = 0
        option_slot_name = 1
        option_unique = 2
        option_wild = 3

        # No change
        if option == option_global:
            return seed

        # Use slot name
        if option == option_slot_name:
            return f"{seed}-{self.get_slot_info(self.slot).name}"

        # Use Toon ID
        if option == option_unique:
            return f"{seed}-{av.doId}"

        # Make something up
        if option == option_wild:
            return random.randint(1, 2**32)

        # An incorrect value was given, default to global
        return self.handle_seed_generation_type(av, seed, option_global)

    def handle_yaml_settings(self, av):

        # Update the value used for seeding any RNG elements that we want to be consistent based on this AP seed
        new_seed = self.slot_data.get('seed', random.randint(1, 2**32))
        rng_option = self.slot_data.get('seed_generation_type', 'global')
        new_seed = self.handle_seed_generation_type(av, new_seed, rng_option)
        av.setSeed(new_seed)
        
        # Get damage multiplier
        damageMultiplier = self.slot_data.get('damage_multiplier', 100)
        av.b_setDamageMultiplier(damageMultiplier)

        # Get overflow modifier
        overflowMod = self.slot_data.get('overflow_mod', 100)
        av.b_setOverflowMod(overflowMod)

    def handle(self, client):
        self.debug(f"Successfully connected to the Archipelago server as {self.get_slot_info(self.slot).name}"
              f" playing {self.get_slot_info(self.slot).game}")

        # Store any information in the cache that we may need later
        self.update_client_slot_cache(client)

        # We have a valid connection, set client state to connected
        client.state = APClientEnums.CONNECTED

        client.av.b_setName(client.slot_name)

        # Is this this slot's first toon? If so reset the toon's stats and initialize their settings from their YAML
        if len(self.checked_locations) == 0:
            self.handle_first_time_player(client.av)
        # Is this this specific toon's first slot? if so, reset this toon's stats and initialize from YAML. 
        if len(client.av.checkedLocations) == 0:
            self.handle_first_time_player(client.av)


        self.debug(f"Detected slot data: {self.slot_data}")
        client.av.b_setSlotData(self.slot_data)
        client.av.updateWinCondition()

        self.handle_yaml_settings(client.av)

        # Send all checks that may have been obtained while disconnected
        toonCheckedLocations = client.av.getCheckedLocations()
        if len(toonCheckedLocations) > 0:
            client.av.archipelago_session.sync()

        # Receive all checks that were collected from our slot while disconnected
        client.av.receiveCheckedLocations(self.checked_locations)

        # Reset cheat access (also check if restricted and keep that value)
        if client.av.getAccessLevel() != OTPGlobals.AccessLevelName2Int.get('RESTRICTED', 0):
            client.av.b_setAccessLevel(OTPGlobals.AccessLevelName2Int.get('NO_ACCESS', 0))

        # Tell AP we are playing
        won_id = ap_location_name_to_id(locations.ToontownLocationName.SAVED_TOONTOWN.value)
        status_packet = StatusUpdatePacket()
        status_packet.status = ClientStatus.CLIENT_GOAL if (client.av.hasCheckedLocation(won_id)) else ClientStatus.CLIENT_PLAYING
        client.send_packet(status_packet)

        # Scout some locations that we need to display
        client.av.scoutLocations(locations.SCOUTING_REQUIRED_LOCATIONS)

        # Login location rewarding
        new_game = ap_location_name_to_id(locations.ToontownLocationName.STARTING_NEW_GAME.value)
        track_one_check = ap_location_name_to_id(locations.ToontownLocationName.STARTING_TRACK_ONE.value)
        track_two_check = ap_location_name_to_id(locations.ToontownLocationName.STARTING_TRACK_TWO.value)
        client.av.addCheckedLocation(new_game)
        client.av.addCheckedLocation(track_one_check)
        client.av.addCheckedLocation(track_two_check)

        # Checks Page Variables
        client.av.hintPoints = self.hint_points
        client.av.totalChecks = len(self.missing_locations) + len(self.checked_locations)

        # Request synced data and subscribe to changes.
        client.av.request_default_ap_data()
        # Update Deathlink Tag.
        if self.slot_data.get('death_link', False):
            update_packet = ConnectUpdatePacket()
            update_packet.tags = [ConnectPacket.TAG_DEATHLINK]
            client.send_packet(update_packet)

        # Finally at the very send, tell the AP DOG that there is some info to sync
        simbase.air.archipelagoManager.updateToonInfo(client.av.doId, client.slot, client.team)
