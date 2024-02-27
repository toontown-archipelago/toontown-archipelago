# Represents a gameplay session attached to toon players, handles rewarding and sending items through the multiworld
from toontown.archipelago.apclient.ap_client_enums import APClientEnums
from toontown.archipelago.apclient.archipelago_client import ArchipelagoClient
from toontown.archipelago.packets.serverbound.say_packet import SayPacket


class ArchipelagoSession:

    def __init__(self, avatar):
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

    def cleanup(self):
        self.client.stop()

