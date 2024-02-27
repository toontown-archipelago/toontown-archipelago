# Contains data that maps IDs to item names and location names
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

    def get_item_from_id(self, item_id: Union[int, str]) -> str:
        return self.id_to_item_name.get(int(item_id), f'Unknown Item[{item_id}]')

    def get_location_from_id(self, location_id: Union[int, str]) -> str:
        return self.id_to_location_name.get(int(location_id), f'Unknown Location[{location_id}]')

    # Take in another datapackage, and merge all mappings from that one into this one THIS IS NOT OVERWRITE SAFE
    # Used to have a master package for all games where the instance calling merge() will have all keys
    def merge(self, other: "DataPackage") -> None:

        for item_id, name in other.id_to_item_name.items():
            self.id_to_item_name[item_id] = name

        for location_id, name in other.id_to_location_name.items():
            self.id_to_location_name[location_id] = name

    # Stores this datapackage on disk
    def cache(self):

        # Create a python dict version of this object that can be read later via json
        data = {
            'game': self.game,
            'version': self.version,
            'checksum': self.checksum,
            'items': self.id_to_item_name,
            'locations': self.id_to_location_name
        }

        Path(f'output/datapackages').mkdir(parents=True, exist_ok=True)
        with open(f'output/datapackages/{self.checksum}.json', 'w') as f:
            json.dump(data, f, indent=4)

    # Given a data package checksum, check if we already cached this data package earlier
    @classmethod
    def is_cached(cls, checksum: str) -> bool:

        try:
            f = open(f'output/datapackages/{checksum}.json')
            f.close()
            return True
        except FileNotFoundError:
            return False

    # Given a checksum, load up a new DataPackage instance, throws FileNotFoundException if it doesn't exist
    # Use is_cached() first to make sure
    @classmethod
    def from_cache(cls, checksum: str):
        instance = cls()

        with open(f'output/datapackages/{checksum}.json') as f:
            data = json.load(f)

            instance.game = data['game']
            instance.version = data['version']
            instance.checksum = data['checksum']
            instance.id_to_item_name = {int(k): v for k, v in data['items'].items()}
            instance.id_to_location_name = {int(k): v for k, v in data['locations'].items()}
            return instance
