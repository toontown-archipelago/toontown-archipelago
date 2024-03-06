from typing import Dict, Any, List

from BaseClasses import Tutorial, Region, ItemClassification, CollectionState
from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import set_rule

from . import regions
from .items import ITEM_DESCRIPTIONS, ITEM_DEFINITIONS, ToontownItemDefinition, ToontownItem
from .locations import LOCATION_DESCRIPTIONS, LOCATION_DEFINITIONS, ToontownLocation
from .options import ToontownOptions

DEBUG_MODE = False


class ToontownWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Toontown with Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["DevvyDont"]
    )]
    theme = "partyTime"


class ToontownWorld(World):
    """
    Toontown is a now defunct classic Disney MMORPG where you play as "toons" to fend off evil robots from invading
    the tooniverse with the use of "gags" since they mean business and cannot take a joke.
    """

    game = "Toontown"
    web = ToontownWeb()

    # v0.1.0
    required_client_version = (0, 1, 0)
    options_dataclass = ToontownOptions
    options: ToontownOptions

    item_name_to_id = {
        item.unique_name: item.unique_id for item in ITEM_DEFINITIONS.values()
    }

    location_name_to_id = {
        location.unique_name: location.unique_id for location in LOCATION_DEFINITIONS.values()
    }

    location_descriptions = LOCATION_DESCRIPTIONS
    item_descriptions = ITEM_DESCRIPTIONS

    # HELPER METHODS

    # Returns two items to be force added to the start inventory so we have two gag tracks on a new seed
    def calculate_starting_tracks(self):

        # Define lists to pull gags from so we don't give two support tracks
        OFFENSIVE: List[str] = [items.ITEM_TRAP_FRAME, items.ITEM_SOUND_FRAME, items.ITEM_THROW_FRAME,
                                items.ITEM_SQUIRT_FRAME, items.ITEM_DROP_FRAME]
        SUPPORT: List[str] = [items.ITEM_TOONUP_FRAME, items.ITEM_LURE_FRAME]
        ALL: List[str] = OFFENSIVE + SUPPORT

        # First force pick an offensive track
        rng = self.multiworld.random
        first_track = rng.choice(OFFENSIVE)

        # Edge case, if we got trap then second track MUST be lure
        if first_track == items.ITEM_TRAP_FRAME:
            second_track = items.ITEM_LURE_FRAME
            return first_track, second_track

        # Otherwise we can choose any track that isn't the first one
        choices = ALL.copy()
        choices.remove(first_track)
        second_track = rng.choice(choices)

        return first_track, second_track

    def create_and_place_event(self, region_name: str, location_name: str, event_name: str, locked_by: Dict[str, int]):

        def can_access(state: CollectionState) -> bool:
            requirement_satisfied = True
            for item_name, amount_needed in locked_by.items():
                if state.count(item_name, self.player) < amount_needed:
                    requirement_satisfied = False

            return requirement_satisfied

        event = self.create_event(event_name)
        region = self.multiworld.get_region(region_name, self.player)
        location = ToontownLocation(self.player, location_name, None, region)
        region.locations.append(location)
        location.place_locked_item(event)
        set_rule(location, can_access)

    # OVERRIDES

    def create_item(self, name: str) -> ToontownItem:
        item_definition: ToontownItemDefinition = ITEM_DEFINITIONS[name]
        item: ToontownItem = ToontownItem(item_definition.unique_name, item_definition.classification,
                                          self.item_name_to_id[name], self.player)
        return item

    def create_event(self, event: str) -> ToontownItem:
        return ToontownItem(event, ItemClassification.progression_skip_balancing, None, self.player)

    def generate_early(self) -> None:

        # Calculate what our starting gag tracks should be
        first_track, second_track = self.calculate_starting_tracks()

        # Save as attributes so we can reference this later in fill_slot_data()
        self.first_track = first_track
        self.second_track = second_track

    def fill_slot_data(self) -> Dict[str, Any]:

        # Return any information that the district is going to need from generation
        return {
            "seed": self.multiworld.seed,
            "seed_generation_type": self.options.seed_generation_type.value,
            "starting_hp": self.options.starting_hp.value,
            "starting_money": self.options.starting_money.value,
            "starting_gag_xp_multiplier": self.options.starting_base_gag_xp_multiplier.value,
            "first_track": self.first_track,
            "second_track": self.second_track
        }

    # Get what items we should exclude from the pool that is marked as required
    def _get_excluded_items(self) -> List[str]:

        items_to_exclude = []

        # Exclude our starting tracks
        items_to_exclude.append(self.first_track)
        items_to_exclude.append(self.second_track)

        # If we have the force tp access setting...
        if self.options.force_playground_visit_teleport_access_unlocks.value:

            # Add all teleport access
            items_to_exclude.append(items.ITEM_TTC_TELEPORT)
            items_to_exclude.append(items.ITEM_DD_TELEPORT)
            items_to_exclude.append(items.ITEM_DG_TELEPORT)
            items_to_exclude.append(items.ITEM_MML_TELEPORT)
            items_to_exclude.append(items.ITEM_TB_TELEPORT)
            items_to_exclude.append(items.ITEM_DDL_TELEPORT)

        if self.options.force_coghq_visit_teleport_access_unlocks.value:
            items_to_exclude.append(items.ITEM_SBHQ_TELEPORT)
            items_to_exclude.append(items.ITEM_CBHQ_TELEPORT)
            items_to_exclude.append(items.ITEM_LBHQ_TELEPORT)
            items_to_exclude.append(items.ITEM_BBHQ_TELEPORT)

        # Done return our items
        return items_to_exclude

    def create_items(self) -> None:

        num_items_in_pool = 0

        # todo calculate dynamically based on settings
        num_locations = len(LOCATION_DEFINITIONS)

        items_to_exclude = self._get_excluded_items()

        # Go through all the defined items and make sure the requirements are in
        for item in ITEM_DEFINITIONS.values():
            # Put as many as needed, most of these are 1
            for _ in range(item.quantity):

                # If this item needs to be excluded skip
                if item.unique_name in items_to_exclude:
                    items_to_exclude.remove(item.unique_name)
                    continue

                self.multiworld.itempool.append(self.create_item(item.unique_name))
                num_items_in_pool += 1

        # If there are fewer locations than items, we have a problem
        if num_locations < num_items_in_pool:
            raise Exception(f"Not enough locations for {num_items_in_pool} items ({num_locations} locations)")

        # Amount of things we need to fill in is the difference of total locations and number of items
        rng = self.multiworld.random
        num_junk = num_locations - num_items_in_pool
        for _ in range(num_junk):

            # Do a check for a trap...
            if self.options.trap_percent.value >= rng.randint(1, 100):
                item = items.random_trap()
            else:
                item = items.random_junk()

            item = item.unique_name
            self.multiworld.itempool.append(self.create_item(item))

    def _force_item_placement(self, location: str, item: str) -> None:
        self.multiworld.get_location(location, self.player).place_locked_item(self.create_item(item))

    def create_regions(self) -> None:

        all_regions: Dict[str, Region] = {}

        # Make all the regions
        for region_definition in regions.REGION_DEFINITIONS:
            new_region = Region(region_definition.unique_name, self.player, self.multiworld)
            all_regions[region_definition.unique_name] = new_region

            location_name_to_address_for_region = {}
            for location_name in region_definition.locations:
                location_name_to_address_for_region[location_name] = self.location_name_to_id[location_name]
            new_region.add_locations(location_name_to_address_for_region, ToontownLocation)

        # Make the connections and define any locks
        for region_definition in regions.REGION_DEFINITIONS:
            region = all_regions.get(region_definition.unique_name)

            # No connections, we can skip
            if len(region_definition.connects_to) <= 0:
                continue

            # Get all the regions that we connect to
            for connection in region_definition.connects_to:
                connecting_region = all_regions.get(connection)
                connecting_region_definition = regions.REGION_NAME_TO_REGION_DEFINITION[connection]

                # See if this region is locked behind an item
                if not connecting_region_definition.always_unlocked():
                    region.connect(connecting_region,
                                   rule=connecting_region_definition.lock.get_lock_function(self.player))
                else:
                    region.connect(connecting_region)

        self.multiworld.regions.extend(all_regions.values())

        # Place our starter items
        self._force_item_placement(locations.STARTING_NEW_GAME_LOCATION, items.ITEM_TTC_HQ_ACCESS)
        self._force_item_placement(locations.STARTING_TRACK_ONE_LOCATION, self.first_track)
        self._force_item_placement(locations.STARTING_TRACK_TWO_LOCATION, self.second_track)

        # Do we have force teleport access? if so place our tps
        if self.options.force_playground_visit_teleport_access_unlocks.value:
            self._force_item_placement(locations.DISCOVER_TTC, items.ITEM_TTC_TELEPORT)
            self._force_item_placement(locations.DISCOVER_DD, items.ITEM_DD_TELEPORT)
            self._force_item_placement(locations.DISCOVER_DG, items.ITEM_DG_TELEPORT)
            self._force_item_placement(locations.DISCOVER_MM, items.ITEM_MML_TELEPORT)
            self._force_item_placement(locations.DISCOVER_TB, items.ITEM_TB_TELEPORT)
            self._force_item_placement(locations.DISCOVER_DDL, items.ITEM_DDL_TELEPORT)

        # Same for cog hqs
        if self.options.force_coghq_visit_teleport_access_unlocks.value:
            self._force_item_placement(locations.DISCOVER_SBHQ, items.ITEM_SBHQ_TELEPORT)
            self._force_item_placement(locations.DISCOVER_CBHQ, items.ITEM_CBHQ_TELEPORT)
            self._force_item_placement(locations.DISCOVER_LBHQ, items.ITEM_LBHQ_TELEPORT)
            self._force_item_placement(locations.DISCOVER_BBHQ, items.ITEM_BBHQ_TELEPORT)

        # Place our proofs
        self._force_item_placement(locations.SELLBOT_PROOF, items.ITEM_SELLBOT_PROOF)
        self._force_item_placement(locations.CASHBOT_PROOF, items.ITEM_CASHBOT_PROOF)
        self._force_item_placement(locations.LAWBOT_PROOF, items.ITEM_LAWBOT_PROOF)
        self._force_item_placement(locations.BOSSBOT_PROOF, items.ITEM_BOSSBOT_PROOF)

        # Place our victory
        self._force_item_placement(locations.SAVED_TOONTOWN, items.ITEM_VICTORY)


        # Debug, use this to print a pretty picture to make sure our regions are set up correctly
        if DEBUG_MODE:
            from Utils import visualize_regions
            visualize_regions(self.multiworld.get_region("Menu", self.player), "toontown.puml")

    def generate_basic(self) -> None:
        # Set win condition
        self.multiworld.completion_condition[self.player] = lambda state: state.has(items.ITEM_VICTORY, self.player)
