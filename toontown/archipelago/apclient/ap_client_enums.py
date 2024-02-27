from enum import Enum


class APClientEnums(Enum):

    # Enums to determine the state of our client's connection
    DISCONNECTED = 1  # Server loop is not running, we cannot send/receive packets, self.socket is None
    CONNECTING = 2  # Server loop is running, and trying to connect
    CONNECTED = 3  # Connection to archipelago is established, we can receive RoomInfo and send Connect packet
    PLAYING = 4  # Same as CONNECTED, but we have a valid slot after a good ConnectPacket has been sent
