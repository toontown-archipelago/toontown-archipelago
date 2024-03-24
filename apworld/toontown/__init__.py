from typing import Dict, Any, List

from BaseClasses import Tutorial, Region, ItemClassification, CollectionState, Location, LocationProgressType
from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import set_rule

from . import regions, consts
from .consts import ToontownItem, ToontownLocation
from .items import ITEM_DESCRIPTIONS, ITEM_DEFINITIONS, ToontownItemDefinition, get_item_def_from_id, ToontownItemName, ITEM_NAME_TO_ID, FISHING_LICENSES
from .locations import LOCATION_DESCRIPTIONS, LOCATION_DEFINITIONS, EVENT_DEFINITIONS, ToontownLocationName, \
    ToontownLocationType, ALL_TASK_LOCATIONS_SPLIT, LOCATION_NAME_TO_ID, ToontownLocationDefinition
from .options import ToontownOptions
from .regions import REGION_DEFINITIONS, ToontownRegionName
from .ruledefs import test_location, test_entrance, test_item_location
from .fish import FishProgression, FishChecks

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

    required_client_version = (0, 4, 4)
    options_dataclass = ToontownOptions
    options: ToontownOptions

    item_name_to_id = ITEM_NAME_TO_ID
    location_name_to_id = LOCATION_NAME_TO_ID

    location_descriptions = LOCATION_DESCRIPTIONS
    item_descriptions = ITEM_DESCRIPTIONS

    def __init__(self, world, player):
        super(ToontownWorld, self).__init__(world, player)
        self.created_locations: list[ToontownLocationDefinition] = []

    def set_rules(self):
        # Add location rules.
        for i, location_data in enumerate(self.created_locations):
            location: Location = self.multiworld.get_location(location_data.name.value, self.player)
            location.access_rule = lambda state, i=i: test_location(
                self.created_locations[i], state, self.multiworld, self.player, self.options)
            location.item_rule = lambda item, i=i: test_item_location(
                self.created_locations[i], item, self.multiworld, self.player, self.options)

        # Add entrance rules.
        for i, region_data in enumerate(REGION_DEFINITIONS):
            for o, entrance_data in enumerate(region_data.connects_to):
                entrance_name = f"{region_data.name.value} -> {entrance_data.connects_to.value}"
                entrance = self.multiworld.get_entrance(entrance_name, self.player)
                entrance.access_rule = lambda state, i=i, o=o: test_entrance(
                    REGION_DEFINITIONS[i].connects_to[o], state, self.multiworld, self.player, self.options)

    def create_item(self, name: str) -> ToontownItem:
        item_id: int = self.item_name_to_id[name]
        item_def: ToontownItemDefinition = get_item_def_from_id(item_id)
        return ToontownItem(name, item_def.classification, item_id, self.player)

    def create_event(self, event: str) -> ToontownItem:
        return ToontownItem(event, ItemClassification.progression_skip_balancing, None, self.player)

    def generate_early(self) -> None:
        # Calculate what our starting gag tracks should be
        first_track, second_track = self.calculate_starting_tracks()

        # Save as attributes so we can reference this later in fill_slot_data()
        self.first_track = first_track
        self.second_track = second_track

    def create_regions(self) -> None:
        player = self.player

        # Create all regions.
        regions: Dict[ToontownRegionName, Region] = {}
        for region_data in REGION_DEFINITIONS:
            region = Region(region_data.name.value, player, self.multiworld)
            regions[region_data.name] = region
            self.multiworld.regions.append(region)

        # Create all entrances.
        for region_data in REGION_DEFINITIONS:
            parent_region = regions[region_data.name]
            for entrance_data in region_data.connects_to:
                entrance_name = f"{region_data.name.value} -> {entrance_data.connects_to.value}"
                child_region = regions[entrance_data.connects_to]
                parent_region.connect(child_region, entrance_name)

        # Determine forbidden location types.
        forbidden_location_types: set[ToontownLocationType] = self.get_disabled_location_types()

        # Noe create locations.
        for i, location_data in enumerate(LOCATION_DEFINITIONS):
            # Do we skip this location generation?
            if location_data.type in forbidden_location_types:
                continue

            # Now create the location.
            region = regions[location_data.region]
            location = ToontownLocation(player, location_data.name.value, self.location_name_to_id[location_data.name.value], region)
            location.progress_type = location_data.progress_type
            region.locations.append(location)
            self.created_locations.append(location_data)

            # Do some progress type overrides as necessary.
            logical_tasks_per_pg = self.options.logical_tasks_per_playground.value
            for loc_list in ALL_TASK_LOCATIONS_SPLIT:
                if location_data.name in loc_list[logical_tasks_per_pg:]:
                    location.progress_type = LocationProgressType.EXCLUDED

            if not self.options.logical_maxed_cog_gallery.value:
                if location_data.type == ToontownLocationType.GALLERY_MAX:
                    location.progress_type = LocationProgressType.EXCLUDED

        for i, location_data in enumerate(EVENT_DEFINITIONS):
            region = regions[location_data.region]
            location = ToontownLocation(player, location_data.name.value, None, region)
            region.locations.append(location)
            self.created_locations.append(location_data)

            if location_data.name == ToontownLocationName.SAVED_TOONTOWN:
                location.place_locked_item(self.create_event("Saved Toontown"))
                self.multiworld.completion_condition[player] = lambda state: state.has("Saved Toontown", player)
            else:
                location.place_locked_item(self.create_event(location_data.name.value))

        # Force various item placements.
        self._force_item_placement(ToontownLocationName.STARTING_NEW_GAME,  ToontownItemName.TTC_HQ_ACCESS)
        self._force_item_placement(ToontownLocationName.STARTING_TRACK_ONE, self.first_track)
        self._force_item_placement(ToontownLocationName.STARTING_TRACK_TWO, self.second_track)

        # Do we have force teleport access? if so place our tps
        if self.options.force_playground_treasure_teleport_access_unlocks.value:
            self._force_item_placement(ToontownLocationName.TTC_TREASURE_1, ToontownItemName.TTC_TELEPORT)
            self._force_item_placement(ToontownLocationName.DD_TREASURE_1,  ToontownItemName.DD_TELEPORT)
            self._force_item_placement(ToontownLocationName.DG_TREASURE_1,  ToontownItemName.DG_TELEPORT)
            self._force_item_placement(ToontownLocationName.MML_TREASURE_1, ToontownItemName.MML_TELEPORT)
            self._force_item_placement(ToontownLocationName.TB_TREASURE_1,  ToontownItemName.TB_TELEPORT)
            self._force_item_placement(ToontownLocationName.DDL_TREASURE_1, ToontownItemName.DDL_TELEPORT)

        # Same for cog hqs
        if self.options.force_coghq_treasure_teleport_access_unlocks.value:
            self._force_item_placement(ToontownLocationName.SBHQ_TREASURE_1, ToontownItemName.SBHQ_TELEPORT)
            self._force_item_placement(ToontownLocationName.CBHQ_TREASURE_1, ToontownItemName.CBHQ_TELEPORT)
            self._force_item_placement(ToontownLocationName.LBHQ_TREASURE_1, ToontownItemName.LBHQ_TELEPORT)
            self._force_item_placement(ToontownLocationName.BBHQ_TREASURE_1, ToontownItemName.BBHQ_TELEPORT)

        # Debug, use this to print a pretty picture to make sure our regions are set up correctly
        if DEBUG_MODE:
            from Utils import visualize_regions
            visualize_regions(self.multiworld.get_region("Menu", self.player), "toontown.puml")

    def create_items(self) -> None:
        pool = []
        exclude_items: List[ToontownItemName] = self._get_excluded_items()

        # Spawn each defined item.
        for item in ITEM_DEFINITIONS:
            for _ in range(item.quantity):
                if item.name in exclude_items:
                    continue
                pool.append(self.create_item(item.name.value))

        # Dynamically generate laff boosts.
        LAFF_TO_GIVE = self.options.max_laff.value - self.options.starting_laff.value
        if LAFF_TO_GIVE < 0:
            print(f"[Toontown - {self.multiworld.get_player_name(self.player)}] "
                  f"WARNING: Too low max HP. Setting max HP to starting HP.")
            LAFF_TO_GIVE = 0
        FIVE_LAFF_BOOSTS = round(consts.FIVE_LAFF_BOOST_RATIO * LAFF_TO_GIVE)
        while FIVE_LAFF_BOOSTS > 0 and LAFF_TO_GIVE > 5:
            FIVE_LAFF_BOOSTS -= 1
            LAFF_TO_GIVE -= 5
            pool.append(self.create_item(ToontownItemName.LAFF_BOOST_5.value))
        FOUR_LAFF_BOOSTS = round(consts.FOUR_LAFF_BOOST_RATIO * LAFF_TO_GIVE)
        while FOUR_LAFF_BOOSTS > 0 and LAFF_TO_GIVE > 4:
            FOUR_LAFF_BOOSTS -= 1
            LAFF_TO_GIVE -= 4
            pool.append(self.create_item(ToontownItemName.LAFF_BOOST_4.value))
        THREE_LAFF_BOOSTS = round(consts.THREE_LAFF_BOOST_RATIO * LAFF_TO_GIVE)
        while THREE_LAFF_BOOSTS > 0 and LAFF_TO_GIVE > 3:
            THREE_LAFF_BOOSTS -= 1
            LAFF_TO_GIVE -= 3
            pool.append(self.create_item(ToontownItemName.LAFF_BOOST_3.value))
        TWO_LAFF_BOOSTS = round(consts.TWO_LAFF_BOOST_RATIO * LAFF_TO_GIVE)
        while TWO_LAFF_BOOSTS > 0 and LAFF_TO_GIVE > 2:
            TWO_LAFF_BOOSTS -= 1
            LAFF_TO_GIVE -= 2
            pool.append(self.create_item(ToontownItemName.LAFF_BOOST_2.value))

        for _ in range(LAFF_TO_GIVE):
            pool.append(self.create_item(ToontownItemName.LAFF_BOOST_1.value))

        # Dynamically generate training frames.
        for frame in items.GAG_TRAINING_FRAMES:
            quantity = 9 if frame not in (self.first_track, self.second_track) else 8
            for _ in range(quantity):
                pool.append(self.create_item(frame.value))

        # Dynamically generate training multipliers.
        GAG_MULTI_TO_GIVE = self.options.max_global_gag_xp.value - self.options.base_global_gag_xp.value
        if GAG_MULTI_TO_GIVE < 0:
            print(f"[Toontown - {self.multiworld.get_player_name(self.player)}] "
                  f"WARNING: Too low max global gag XP. Setting max global gag XP to base global gag XP.")
            GAG_MULTI_TO_GIVE = 0
        TWO_GAG_MULTI_BOOSTS = round(consts.TWO_XP_BOOST_RATIO * GAG_MULTI_TO_GIVE)
        while TWO_GAG_MULTI_BOOSTS > 0 and GAG_MULTI_TO_GIVE > 2:
            TWO_GAG_MULTI_BOOSTS -= 1
            GAG_MULTI_TO_GIVE -= 2
            pool.append(self.create_item(ToontownItemName.GAG_MULTIPLIER_2.value))
        for _ in range(GAG_MULTI_TO_GIVE):
            pool.append(self.create_item(ToontownItemName.GAG_MULTIPLIER_1.value))

        # Create fishing licenses.
        if self.options.fish_progression.value in (FishProgression.LicensesAndRods, FishProgression.Licenses):
            for fishLicense in FISHING_LICENSES:
                pool.append(self.create_item(fishLicense.value))

        # Create fishing rods.
        if self.options.fish_progression.value in (FishProgression.LicensesAndRods, FishProgression.Rods):
            for _ in range(4):
                pool.append(self.create_item(ToontownItemName.FISHING_ROD_UPGRADE.value))

        # Fill the rest of the room with junk.
        junk: int = len(self.multiworld.get_unfilled_locations(self.player)) - len(pool)
        if junk < 0:
            raise Exception(f"[Toontown - {self.multiworld.get_player_name(self.player)}] "
                            f"Generated with too many items ({-junk}). Please tweak settings.")

        trap: int = round(junk * (self.options.trap_percent / 100))
        filler: int = junk - trap
        for i in range(trap):
            pool.append(self.create_item(items.random_trap().value))
        for i in range(filler):
            pool.append(self.create_item(items.random_junk().value))

        # Finalize item pool.
        self.multiworld.itempool += pool

    def fill_slot_data(self) -> Dict[str, Any]:
        """
        Returns any information that the client/AI is going to need from generation.
        """
        # Determine some special slot data args.
        local_itempool = [
            location.item.code
            for location in self.multiworld.get_locations()
            if location.address and location.item and location.item.code and location.item.player == self.player
        ]

        # Return the result.
        return {
            "seed": self.multiworld.seed,
            "seed_generation_type": self.options.seed_generation_type.value,
            "starting_laff": self.options.starting_laff.value,
            "starting_money": self.options.starting_money.value,
            "base_global_gag_xp": self.options.base_global_gag_xp.value,
            "first_track": self.first_track.value,
            "second_track": self.second_track.value,
            "cog_bosses_required": self.options.cog_bosses_required.value,
            "fish_locations": self.options.fish_locations.value,
            "fish_checks": self.options.fish_checks.value,
            "fish_progression": self.options.fish_progression.value,
            "maxed_cog_gallery_quota": self.options.maxed_cog_gallery_quota.value,
            "death_link": self.options.death_link.value,
            "local_itempool": local_itempool,
        }

    def calculate_starting_tracks(self):
        # Define lists to pull gags from so we don't give two support tracks
        OFFENSIVE: List[ToontownItemName] = [
            ToontownItemName.TRAP_FRAME,
            ToontownItemName.SOUND_FRAME,
            ToontownItemName.THROW_FRAME,
            ToontownItemName.SQUIRT_FRAME,
            ToontownItemName.DROP_FRAME,
        ]
        SUPPORT: List[ToontownItemName] = [
            ToontownItemName.TOONUP_FRAME,
            ToontownItemName.LURE_FRAME,
        ]
        ALL: List[ToontownItemName] = OFFENSIVE + SUPPORT

        # First force pick an offensive track
        rng = self.multiworld.random
        first_track = rng.choice(OFFENSIVE)

        # Edge case, if we got trap then second track MUST be lure
        if first_track == ToontownItemName.TRAP_FRAME:
            second_track = ToontownItemName.LURE_FRAME
            return first_track, second_track

        # Otherwise we can choose any track that isn't the first one
        choices = ALL.copy()
        choices.remove(first_track)
        second_track = rng.choice(choices)

        return first_track, second_track

    def get_disabled_location_types(self) -> set[ToontownLocationType]:
        """
        Returns a set of disabled location types.
        These location types are removed from logic generation.
        """
        forbidden_location_types: set[ToontownLocationType] = set()
        fish_checks = FishChecks(self.options.fish_checks.value)
        if fish_checks == FishChecks.AllSpecies:
            forbidden_location_types.add(ToontownLocationType.FISHING_GENUS)
            forbidden_location_types.add(ToontownLocationType.GALLERY)
        elif fish_checks == FishChecks.AllGalleryAndGenus:
            forbidden_location_types.add(ToontownLocationType.FISHING)
        elif fish_checks == FishChecks.AllGallery:
            forbidden_location_types.add(ToontownLocationType.FISHING)
            forbidden_location_types.add(ToontownLocationType.FISHING_GENUS)
        elif fish_checks == FishChecks.Nonne:
            forbidden_location_types.add(ToontownLocationType.FISHING)
            forbidden_location_types.add(ToontownLocationType.FISHING_GENUS)
            forbidden_location_types.add(ToontownLocationType.GALLERY)
        return forbidden_location_types

    def _get_excluded_items(self) -> List[ToontownItemName]:
        items_to_exclude: List[ToontownItemName] = []

        # If we have the force tp access setting...
        if self.options.force_playground_treasure_teleport_access_unlocks.value:
            # Add all teleport access
            items_to_exclude.append(ToontownItemName.TTC_TELEPORT)
            items_to_exclude.append(ToontownItemName.DD_TELEPORT)
            items_to_exclude.append(ToontownItemName.DG_TELEPORT)
            items_to_exclude.append(ToontownItemName.MML_TELEPORT)
            items_to_exclude.append(ToontownItemName.TB_TELEPORT)
            items_to_exclude.append(ToontownItemName.DDL_TELEPORT)

        if self.options.force_coghq_treasure_teleport_access_unlocks.value:
            items_to_exclude.append(ToontownItemName.SBHQ_TELEPORT)
            items_to_exclude.append(ToontownItemName.CBHQ_TELEPORT)
            items_to_exclude.append(ToontownItemName.LBHQ_TELEPORT)
            items_to_exclude.append(ToontownItemName.BBHQ_TELEPORT)

        # Done return our items
        return items_to_exclude

    def _force_item_placement(self, location: ToontownLocationName, item: ToontownItemName) -> None:
        self.multiworld.get_location(location.value, self.player).place_locked_item(self.create_item(item.value))
