# Represents a gameplay session attached to toon players, handles rewarding and sending items through the multiworld
from typing import List, TYPE_CHECKING

from toontown.archipelago.apclient.ap_client_enums import APClientEnums
from toontown.archipelago.apclient.archipelago_client import ArchipelagoClient
from toontown.archipelago.definitions import util
from toontown.archipelago.definitions.death_reason import DeathReason
from toontown.archipelago.packets.serverbound.bounce_packet import BouncePacket
from toontown.archipelago.packets.serverbound.location_checks_packet import LocationChecksPacket
from toontown.archipelago.packets.serverbound.location_scouts_packet import LocationScoutsPacket
from toontown.archipelago.packets.serverbound.say_packet import SayPacket
from toontown.archipelago.packets.serverbound.status_update_packet import StatusUpdatePacket
from toontown.archipelago.util import global_text_properties
from toontown.archipelago.util.global_text_properties import MinimalJsonMessagePart
from toontown.archipelago.util.net_utils import ClientStatus

if TYPE_CHECKING:
    from toontown.toon.DistributedToonAI import DistributedToonAI


class ArchipelagoSession:

    def __init__(self, avatar: "DistributedToonAI"):
        self.avatar = avatar  # The avatar that owns this session, DistributedToonAI
        self.client = ArchipelagoClient(self.avatar, self.avatar.getName())  # The client responsible for socket communication

    def handle_connect(self, server_url: str = None):

        if server_url:
            self.avatar.d_setSystemMessage(0, f"DEBUG: set AP server URL to {server_url}")
            self.client.set_connect_url(server_url)

        try:
            self.client.connect()
        except Exception as e:
            self.avatar.d_setSystemMessage(0, f"{e}")

    def handle_disconnect(self):
        self.client.team = 999
        self.client.stop()

    def handle_slot(self, new_slot):
        self.client.update_identification(new_slot)
        self.avatar.d_setSystemMessage(0, f"Updated slot name to {new_slot}")

    def handle_password(self, new_password):
        self.client.update_identification(self.client.slot_name, new_password)
        self.avatar.d_setSystemMessage(0, f"Updated password")

    # Called from DisToonAI when this toon sends a chat message
    def handle_chat(self, message: str):

        # Handle the case where they want to change their slot name
        if message.startswith('!slot'):
            return self.handle_slot(message.removeprefix('!slot').lstrip())

        # Handle the case where they want to input a password
        if message.startswith('!password'):
            return self.handle_password(message.removeprefix('!password').lstrip())

        # Handle the case where they are trying to connect
        if message.startswith('!connect'):
            # Attempt to extract an AP server URL and port
            ip = message.removeprefix('!connect').lstrip()
            if not ip:
                ip = None

            return self.handle_connect(server_url=ip)

        # Handle the case where they are trying to disconnect
        if message.startswith('!disconnect'):
            return self.handle_disconnect()

        # Below we are only gonna consider the case we have a valid connection
        if self.client.state in (APClientEnums.DISCONNECTED, APClientEnums.CONNECTING):
            return

        # Get a clean version of the message, if there is no useful content in this string skip it
        clean = message.strip()
        if len(clean) <= 0:
            return

        # Anything else just send as an archipelago message
        packet = SayPacket()
        packet.text = clean
        self.client.send_packet(packet)

    # Called right when we get connected to the server, makes sure our locations are synced in case we got stuff
    # while disconnected from AP
    def sync(self):
        self.complete_checks(self.avatar.getCheckedLocations())

    # Call to send a packet to AP that a location check was completed
    def complete_check(self, check: int):
        self.complete_checks([check])

    def complete_checks(self, checks: List[int]):
        if len(checks) == 0:
            return

        checks_packet = LocationChecksPacket()
        checks_packet.locations = list(checks)
        self.client.send_packet(checks_packet)

    def cleanup(self):
        self.client.stop()

    # Sends a status update to AP that we have completed our goal
    def victory(self):
        goal_complete_packet = StatusUpdatePacket()
        goal_complete_packet.status = ClientStatus.CLIENT_GOAL
        self.client.send_packet(goal_complete_packet)

    # Call to send a LocationScout packet to AP so we can receive information about items at specific locations
    def scout(self, locations: List[str], hint_item=False, force_broadcast=False):

        locationIDs = []
        for location in locations:
            locationIDs.append(util.ap_location_name_to_id(location))

        scout_packet = LocationScoutsPacket()
        scout_packet.locations = locationIDs

        # todo add setting in YAML for hinting the scout
        if hint_item and force_broadcast:
            scout_packet.hint_item = 2
        elif hint_item:
            scout_packet.hint_item = 1

        self.client.send_packet(scout_packet)

    # Called when the toon that owns this ap session dies. Mainly used for deathlink purposes
    def toon_died(self):

        # If deathlink is off don't do anything
        if not self.avatar.slotData.get('death_link', False):
            return

        # If our cause of death is a deathlink event from another player, don't continue
        if self.avatar.getDeathReason() == DeathReason.DEATHLINK:
            return

        # Create a deathlink packet
        deathlink_packet = BouncePacket()
        deathlink_packet.add_deathlink_data(self.avatar)
        self.client.send_packet(deathlink_packet)

        # Tell the person that they caused a death to happen
        death_component = self.avatar.getDeathReason().format(self.avatar)
        msg = global_text_properties.get_raw_formatted_string([
            MinimalJsonMessagePart("[DeathLink] ", color='red'),
            MinimalJsonMessagePart("Everyone died because "),
            MinimalJsonMessagePart(f"{death_component}", color='salmon')
        ])
        self.avatar.d_sendArchipelagoMessage(msg)

    """
    Methods to retrieve information about an Archipelago Session
    """

    def getSlotId(self) -> int:
        return self.client.slot

    def getTeamId(self) -> int:
        return self.client.team
