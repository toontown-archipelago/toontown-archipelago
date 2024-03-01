from typing import List

from toontown.archipelago.packets.clientbound.clientbound_packet_base import ClientBoundPacketBase


# Sent to clients when the server refuses connection. This is sent during the initial connection handshake.
class ConnectionRefusedPacket(ClientBoundPacketBase):

    ERROR_INVALID_SLOT = "InvalidSlot"
    ERROR_INVALID_GAME = "InvalidGame"
    ERROR_INCOMPATIBLE_VERSION = "IncompatibleVersion"
    ERROR_INVALID_PASSWORD = "InvalidPassword"
    ERROR_INVALID_ITEMS_HANDLING = "InvalidItemsHandling"

    def __init__(self, json_data):
        super().__init__(json_data)

        # Optional. When provided, should contain any one of:
        # InvalidSlot, InvalidGame, IncompatibleVersion, InvalidPassword, or InvalidItemsHandling
        self.errors: List[str] = self.read_raw_field('errors')

    def handle(self, client):
        self.debug("Handling packet")

        for error in self.errors:

            if error == self.ERROR_INVALID_SLOT:
                self.debug(f"Slot {client.slot_name} is invalid for this multiworld!")
                client.av.d_sendArchipelagoMessage(f"Invalid slot! Please use !slot to correct your slot.")

            elif error == self.ERROR_INVALID_GAME:
                self.debug("Invalid game provided!")
                client.av.d_sendArchipelagoMessage("Invalid game provided!")

            elif error == self.ERROR_INCOMPATIBLE_VERSION:
                self.debug("Incompatible version detected!")
                client.av.d_sendArchipelagoMessage("Incompatible version detected!")

            elif error == self.ERROR_INVALID_PASSWORD:
                self.debug("Invalid password provided!")
                client.av.d_sendArchipelagoMessage("Invalid password provided! Please use !password to correct your password.")

            elif error == self.ERROR_INVALID_ITEMS_HANDLING:
                self.debug("Invalid item sent to server!")
                client.av.d_sendArchipelagoMessage("Invalid item sent to server!")

            else:
                self.debug(f"Unknown error: {error}")
                client.av.d_sendArchipelagoMessage(f"Unknown error: {error}")
