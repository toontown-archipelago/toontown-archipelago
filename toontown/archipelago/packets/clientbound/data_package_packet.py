from typing import TypedDict, Dict

from toontown.archipelago.util.data_package import DataPackage
from toontown.archipelago.packets.clientbound.clientbound_packet_base import ClientBoundPacketBase


# GameData is a dict but contains these keys and values. It's broken out into another "type" for ease of documentation.
class GameData(TypedDict):
    item_name_to_id: Dict[str, int]  # Mapping of all item names to their respective ID.
    location_name_to_id: Dict[str, int]  # Mapping of all location names to their respective ID.
    version: int  # Version number of this game's data. Deprecated. Used by older clients to request an updated
    # datapackage if cache is outdated.
    checksum: str  # A checksum hash of this game's data.


# A data package is a JSON object which may contain arbitrary metadata to enable a client to interact with the
# Archipelago server most easily. Currently, this package is used to send ID to name mappings so that clients need not
# maintain their own mappings.
#
# We encourage clients to cache the data package they receive on disk, or otherwise not tied to a session.
# You will know when your cache is outdated if the RoomInfo packet or the datapackage itself denote a different version.
# A special case is datapackage version 0, where it is expected the package is custom and should not be cached.
#
# Note:
#
# Any ID is unique to its type across AP: Item 56 only exists once and Location 56 only exists once.
# Any Name is unique to its type across its own Game only: Single Arrow can exist in two games.
# The IDs from the game "Archipelago" may be used in any other game.
# Especially Location ID -1: Cheat Console and -2: Server (typically Remote Start Inventory)
class DataPackageObject(TypedDict):
    games: Dict[str, GameData]  # Mapping of all Games and their respective data


# Sent to clients to provide what is known as a 'data package' which contains information to enable a client to most
# easily communicate with the Archipelago server. Contents include things like location id to name mappings,
# among others; see Data Package Contents for more info.
class DataPackagePacket(ClientBoundPacketBase):

    def __init__(self, json_data):
        super().__init__(json_data)

        # The data package as a JSON object.
        self.data: DataPackageObject = self.read_raw_field('data')

    def handle(self, client):
        self.debug(f"Received data package from server, storing information for {len(self.data['games'])} games")

        # Loop through all games and their data
        for game_name, game_data in self.data['games'].items():
            game_name: str
            game_data: GameData

            # Construct an actual game_data packet
            package = DataPackage()
            package.game = game_name
            package.checksum = game_data['checksum']

            # Our datapackage is stored in reverse order for our location/item keys
            package.id_to_item_name = {int(v): k for k, v in game_data['item_name_to_id'].items()}
            package.id_to_location_name = {int(v): k for k, v in game_data['location_name_to_id'].items()}

            # Cache this package, and have our client store it
            package.cache()
            client.data_packages[game_name] = package
            client.global_data_package.merge(package)


