from typing import Any, Dict, List

from toontown.archipelago.packets.serverbound.serverbound_packet_base import ServerBoundPacketBase


# Requests the data package from the server. Does not require client authentication.
class GetDataPackagePacket(ServerBoundPacketBase):

    def __init__(self):
        super().__init__()
        self.cmd = "GetDataPackage"

        # Optional. If specified, will only send back the specified data. Such as, ["Factorio"] -> Datapackage
        # with only Factorio data.
        self.games: List[str] = []

    def build(self) -> Dict[str, Any]:
        # Return all attributes
        return {
            'cmd': self.cmd,
            'games': self.games
        }

# Example of using this packet

# get_data_pkg_packet = GetDataPackagePacket()
# get_data_pkg_packet.games.append(["Kingdom Hearts 2"])  # ONLY get kh2 data
# await client.send_packet(get_data_pkg_packet)
