# Represents a gameplay session attached to toon players, handles rewarding and sending items through the multiworld
import asyncio
from threading import Thread

from toontown.archipelago.archipelago_client import ArchipelagoClient
from toontown.archipelago.packets.serverbound.say_packet import SayPacket


class ArchipelagoSession:

    def __init__(self, avatar):
        self.avatar = avatar  # The avatar that owns this session, DistributedToonAI
        self.client = ArchipelagoClient(self.avatar, self.avatar.getName())  # The client responsible for socket communication

    # Called from DisToonAI when this toon sends a chat message
    def handle_chat(self, message: str):

        # Handle the case where they want to change their slot name
        if message.startswith('!slot'):
            new_slot = message.removeprefix('!slot').lstrip()
            self.client.update_identification(new_slot)
            self.avatar.d_setSystemMessage(0, f"Updated slot name to {new_slot}")
            return

        if message.startswith('!password'):
            new_pass = message.removeprefix('!password').lstrip()
            self.client.update_identification(self.client.slot_name, new_pass)
            self.avatar.d_setSystemMessage(0, f"Updated password")
            return

        # Handle the case where they are trying to connect
        if message.startswith('!connect'):
            try:
                self.client.connect()
            except Exception as e:
                self.avatar.d_setSystemMessage(0, f"{e}")

            return

        # Below we are only gonna consider the case we have a valid connection
        if self.client.state == ArchipelagoClient.DISCONNECTED:
            return

        # Anything else just send as an archipelago message
        packet = SayPacket()
        packet.text = message
        self.client.send_packet(packet)

    def cleanup(self):
        self.client.stop()

