from typing import List, Dict

from toontown.archipelago.util.data_package import DataPackage
from toontown.archipelago.util.net_utils import Permission
from toontown.archipelago.packets.clientbound.clientbound_packet_base import ClientBoundPacketBase
from toontown.archipelago.packets.serverbound.get_data_package_packet import GetDataPackagePacket
from toontown.archipelago.util.utils import Version


class RoomInfoPacket(ClientBoundPacketBase):

    def __init__(self, json_data):
        super().__init__(json_data)

        # Denoted whether a password is required to join this room.
        self.password: bool = self.read_raw_field('password', ignore_missing=True)

        # List of games present in this multiworld.
        self.games: List[str] = self.read_raw_field('games', ignore_missing=True)

        # Denotes special features or capabilities that the sender is capable of. Example: WebHost
        self.tags: List[str] = self.read_raw_field('tags', ignore_missing=True)

        # Object denoting the version of Archipelago which the server is running.
        self.version: Version = self.read_raw_field('version', ignore_missing=True)

        # Object denoting the version of Archipelago which generated the multiworld.
        self.generator_version: Version = self.read_raw_field('generator_version', ignore_missing=True)

        # Mapping of permission name to Permission, keys are: "release", "collect" and "remaining".
        self.permissions: Dict[str, Permission] = self.read_raw_field('permissions', ignore_missing=True)

        # The percentage of total locations that need to be checked to receive a hint from the server.
        self.hint_cost: int = self.read_raw_field('hint_cost', ignore_missing=True)

        # The amount of hint points you receive per item/location check completed.
        self.location_check_points: int = self.read_raw_field('location_check_points', ignore_missing=True)

        # Deprecated
        self.datapackage_versions: dict[str, int] = self.read_raw_field('datapackage_versions', ignore_missing=True)

        # Checksum hash of the individual games' data packages the server will send. Used by newer clients to decide
        # which games' caches are outdated. See Data Package Contents for more information.
        self.datapackage_checksums: dict[str, str] = self.read_raw_field('datapackage_checksums', ignore_missing=True)

        # Uniquely identifying name of this generation
        self.seed_name: str = self.read_raw_field('seed_name', ignore_missing=True)

        # Unix time stamp of "now". Send for time synchronization if wanted for things like the DeathLink Bounce.
        self.time: float = self.read_raw_field('time', ignore_missing=True)

    def update_data_packages(self, client):

        data_package_packet = GetDataPackagePacket()

        for game_name, checksum in self.datapackage_checksums.items():

            # Attempt to load the package from the cache, if we fail then we need a new one
            package = None
            try:
                package = DataPackage.from_cache(checksum)

                # Otherwise, we can add this to the client
                client.data_packages[game_name] = package
                client.global_data_package.merge(package)
            except:
                pass

            if not package:
                data_package_packet.games.append(game_name)

        # Send the packet if we need to get some game info
        if len(data_package_packet.games) > 0:
            client.send_packet(data_package_packet)

    def handle(self, client):
        self.debug("[AP Client] Handling Room Info packet")

        # We should check in with our data packages
        self.update_data_packages(client)

        # When we are given this packet, we should attempt to connect this player to the room with their slot
        client.connect()
