from typing import List

from toontown.archipelago.packets.clientbound.clientbound_packet_base import ClientBoundPacketBase
from toontown.archipelago.utils import InvalidSlotException


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
        print("[AP Client] Handling Connection Refused packet")

        for error in self.errors:

            if error == self.ERROR_INVALID_SLOT:
                print(f"Slot {client.slot_name} is invalid for this multiworld!")

            elif error == self.ERROR_INVALID_GAME:
                print("[AP Client] Invalid game provided!")

            elif error == self.ERROR_INCOMPATIBLE_VERSION:
                print("[AP Client] Incompatible version detected!")

            elif error == self.ERROR_INVALID_PASSWORD:
                print("[AP Client] Invalid password provided!")

            elif error == self.ERROR_INVALID_ITEMS_HANDLING:
                print("[AP Client] Invalid item sent to server!")

            else:
                print(f"[AP Client] Unknown error: {error}")
