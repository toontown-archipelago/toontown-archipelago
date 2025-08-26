# Contains data that maps IDs to item names and location names
from sys import platform
from typing import Dict, Union

import json
from pathlib import Path


class DataPackage:
    def __init__(self):
        self.game = ''
        self.version = -1
        self.checksum = ''
        self.id_to_item_name: Dict[int, str] = {}
        self.id_to_location_name: Dict[int, str] = {}

    #encode names to ascii on platforms other than windows, due to astron causing crashes.
    if platform == 'win32':
        def get_item_from_id(self, item_id: Union[int, str]) -> str:
            return self.id_to_item_name.get(int(item_id), f'Unknown Item[{item_id}]')

        def get_location_from_id(self, location_id: Union[int, str]) -> str:
            return self.id_to_location_name.get(int(location_id), f'Unknown Location[{location_id}]')

    else:
        def get_item_from_id(self, item_id: Union[int, str]) -> str:
            return self.id_to_item_name.get(int(item_id), f'Unknown Item[{item_id}]').encode('ascii', 'replace').decode()

        def get_location_from_id(self, location_id: Union[int, str]) -> str:
            return self.id_to_location_name.get(int(location_id), f'Unknown Location[{location_id}]').encode('ascii', 'replace').decode()

    @classmethod
    def load(cls, name: str, data: Dict[str, any]):
        """
        Load and cache a game's datapackage to disk.
        """
        instance = cls()

        instance.game = name
        instance.version = data.get('version', -1)
        instance.checksum = data['checksum']
        instance.id_to_item_name = {int(v): k for k, v in data['item_name_to_id'].items()}
        instance.id_to_location_name = {int(v): k for k, v in data['location_name_to_id'].items()}

        # Create a python dict version of this object that can be read later via json
        data = {
            'game': instance.game,
            'version': instance.version,
            'checksum': instance.checksum,
            'items': instance.id_to_item_name,
            'locations': instance.id_to_location_name
        }

        Path('output/datapackages').mkdir(parents=True, exist_ok=True)
        with open(f'output/datapackages/{instance.checksum}.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

        return instance

    @classmethod
    def from_cache(cls, checksum: str):
        """
        Given a checksum, load up a new DataPackage instance.
        Raises FileNotFoundException if it doesn't exist, OSError with any error opening it.
        """

        with open(f'output/datapackages/{checksum}.json', encoding='utf-8') as f:
            instance = cls()
            data = json.load(f)

            instance.game = data['game']
            instance.version = data['version']
            instance.checksum = data['checksum']
            instance.id_to_item_name = {int(k): v for k, v in data['items'].items()}
            instance.id_to_location_name = {int(k): v for k, v in data['locations'].items()}
            return instance

class GlobalDataPackage:
    def __init__(self):
        self._games: Dict[DataPackage] = {}

    def add_datapackage(self, data: DataPackage):
        """
        Add a datapackage to this.
        """
        self._games.update({data.game: data})

    def get_item_from_id(self, item_id: Union[int, str]) -> str:
        """
        Get an item with a given id, provided for compatibility with existing code.
        please use get_item instead.
        """
        item_id = int(item_id)
        for game in self._games.values():
            try:
                return game.id_to_item_name[item_id]
            except KeyError:
                continue
        return f'Unknown Item[{item_id}]'

    def get_location_from_id(self, location_id: Union[int, str]) -> str:
        """
        Get a location with a given id, provided for compatibility with existing code.
        please use get_location instead.
        """
        location_id = int(location_id)
        for game in self._games.values():
            try:
                return game.locations[location_id]
            except KeyError:
                continue
        return f'Unknown Location[{location_id}]'

    def get_item(self, game: str, item_id: Union[int, str]) -> str:
        """
        Get an item from a given game.
        Raises KeyError if the game doesn't exist.
        """
        return self._games[game].get_item_from_id(int(item_id))

    def get_location(self, game: str, location_id: Union[int, str]) -> str:
        """
        Get a location from a given game.
        Raises KeyError if the game doesn't exist.
        """
        return self._games[game].get_location_from_id(int(location_id))
