# Represents a gameplay session attached to toon players, handles rewarding and sending items through the multiworld
from typing import List

from toontown.archipelago.apclient.ap_client_enums import APClientEnums
from toontown.archipelago.apclient.archipelago_client import ArchipelagoClient
from toontown.archipelago.packets.serverbound.location_checks_packet import LocationChecksPacket
from toontown.archipelago.packets.serverbound.say_packet import SayPacket
from toontown.archipelago.packets.serverbound.status_update_packet import StatusUpdatePacket
from toontown.archipelago.util.net_utils import ClientStatus

# Typing hack, delete later #todo
if False:
    from toontown.toon.DistributedToonAI import DistributedToonAI


class ArchipelagoSession:

    def __init__(self, avatar: "DistributedToonAI"):
        self.avatar = avatar  # The avatar that owns this session, DistributedToonAI
        self.client = ArchipelagoClient(self.avatar, self.avatar.getName())  # The client responsible for socket communication

    def handle_connect(self):
        try:
            self.client.connect()
        except Exception as e:
            self.avatar.d_setSystemMessage(0, f"{e}")

    def handle_disconnect(self):
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
            return self.handle_connect()

        # Handle the case where they are trying to disconnect
        if message.startswith('!disconnect'):
            return self.handle_disconnect()

        # Below we are only gonna consider the case we have a valid connection
        if self.client.state in (APClientEnums.DISCONNECTED, APClientEnums.CONNECTING):
            return

        # Anything else just send as an archipelago message
        packet = SayPacket()
        packet.text = message
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

