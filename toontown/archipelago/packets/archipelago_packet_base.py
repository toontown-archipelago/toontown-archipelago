import json
from enum import IntEnum
from typing import Any


class ArchipelagoPacketBase:

    DEBUG = False  # Enable to have the AI spit out a bunch of information about packets

    class PacketType(IntEnum):
        UNDEFINED = -1  # This packet was not defined correctly, an error will be thrown
        SERVER_BOUND = 0  # This packet is to be sent to the server from our client only
        CLIENT_BOUND = 1  # This packet is to be received by the client from the server only

    packet_type = PacketType.UNDEFINED

    def __init__(self):
        self._raw_data = {}

    @property
    def raw_data(self):
        return self._raw_data

    # Reads a field given from the raw packet (json_data from constructor)
    # :param field - the key to index in the json object read from the raw packet
    # :param ignore_missing - when False, throw an exception if the field is missing (KeyError), when True, use default
    # :param default - Use this as the return value when ignore_missing is True and the field is not present in raw data
    def read_raw_field(self, field: str, ignore_missing=False, default=None) -> Any:

        # Is the key missing, and we aren't ignoring it?
        if field not in self.raw_data and not ignore_missing:
            raise KeyError(f"{field} is not present in the raw JSON data within this packet")

        # Is the key missing, but we want to safely ignore it? If so, return default we were given
        if field not in self.raw_data and ignore_missing:
            return default

        # Safely give the data
        return self.raw_data[field]

    # Determine whether this packet is valid
    def valid(self) -> bool:
        return self.packet_type != self.PacketType.UNDEFINED

    # String representation of this instance
    def __repr__(self):
        return f"[{self.__class__.__name__}]=<{','.join(self.raw_data)}>"

    # Used for debugging, dump the entire content of the raw packet data
    def dump(self):
        formatted_msg = json.dumps(self.raw_data, indent=4)
        print(formatted_msg)

    # Prints a message if debug flag is on
    def debug(self, message: str) -> None:
        if not self.DEBUG:
            return

        print(f"[{self.__class__.__name__}]: {message}")
