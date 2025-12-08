from typing import Dict, Any, List

from BaseClasses import Tutorial, Region, ItemClassification, CollectionState, Location, LocationProgressType
from worlds.AutoWorld import World, WebWorld
import random
import logging
from . import regions, consts
from .consts import ToontownItem, ToontownLocation, ToontownWinCondition
from .items import ITEM_DESCRIPTIONS, ITEM_DEFINITIONS, ToontownItemDefinition, get_item_def_from_id, ToontownItemName, \
    ITEM_NAME_TO_ID, FISHING_LICENSES, TELEPORT_ACCESS_ITEMS, FACILITY_KEY_ITEMS, get_item_groups, DISGUISE_ITEMS
from .locations import LOCATION_DESCRIPTIONS, LOCATION_DEFINITIONS, EVENT_DEFINITIONS, ToontownLocationName, \
    ToontownLocationType, ALL_TASK_LOCATIONS_SPLIT, LOCATION_NAME_TO_ID, ToontownLocationDefinition, \
    TREASURE_LOCATION_TYPES, KNOCK_KNOCK_LOCATION_TYPES, BOSS_LOCATION_TYPES, BOSS_EVENT_DEFINITIONS, get_location_groups
from .options import ToontownOptions, TPSanity, StartingTaskOption, GagTrainingCheckBehavior, FacilityLocking, toontown_option_groups, \
    GagTrainingFrameBehavior
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
    option_groups = toontown_option_groups


class ToontownWorld(World):
    """
    Toontown is a now defunct classic Disney MMORPG where you play as "toons" to fend off evil robots from invading
    the tooniverse with the use of "gags" since they mean business and cannot take a joke.
    """

    game = "Toontown"
    web = ToontownWeb()

    required_client_version = (0, 6, 3)
    options_dataclass = ToontownOptions
    options: ToontownOptions

    item_name_to_id = ITEM_NAME_TO_ID
    location_name_to_id = LOCATION_NAME_TO_ID

    location_descriptions = LOCATION_DESCRIPTIONS
    location_name_groups = get_location_groups()
    item_descriptions = ITEM_DESCRIPTIONS
    item_name_groups = get_item_groups()

    def __init__(self, world, player):
        super(ToontownWorld, self).__init__(world, player)
        self.created_locations: list[ToontownLocationDefinition] = []
        self.valid_bounties = list()
        self.inserted_bounties = list()

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

    def create_progression_deprioritized_skip_balancing(self, name: str) -> ToontownItem:
        item_id: int = self.item_name_to_id[name]
        return ToontownItem(name, ItemClassification.progression_deprioritized_skip_balancing, item_id, self.player)

    def create_progression_item(self, name: str) -> ToontownItem:
        item_id: int = self.item_name_to_id[name]
        return ToontownItem(name, ItemClassification.progression, item_id, self.player)

    def create_useful_item(self, name: str) -> ToontownItem:
        item_id: int = self.item_name_to_id[name]
        return ToontownItem(name, ItemClassification.useful, item_id, self.player)

    def create_event(self, event: str) -> ToontownItem:
        return ToontownItem(event, ItemClassification.progression_skip_balancing, None, self.player)

    def generate_early(self) -> None:
        # Convert web options to standard options, if the relevant standard option is still the default.
        # The default between web options and standard options should result in the same settings,
        # so that we don't accidentally change something unintentionally
        if self.options.starting_gags.value == self.options.starting_gags.default:
            self.options.starting_gags.value = list(self.options.web_starting_gags.value) + ["randomized"] * self.options.web_random_gags.value
        if self.options.win_condition.value == self.options.win_condition.default:
            self.options.win_condition.value = self.convert_web_win_conditions()
            
        # We picked a randomized omitted gag, set to something new
        if self.options.omit_gag.value == 6:
            self.options.omit_gag.value = random.randint(1, 5)
        # We picked a random single target gag to omit, set to something new
        elif self.options.omit_gag.value == 7:
            self.options.omit_gag.value = random.choice([1, 3, 4, 5])

        # Calculate what our starting gag tracks should be
        startingTracks = self.calculate_starting_tracks(self.options.starting_gags.value)

        # Save as attributes so we can reference this later in fill_slot_data()
        self.startingTracks = startingTracks

        #Randomize win conditions
        if "randomized" in self.options.win_condition.value:
            self.options.win_condition.value = self.randomize_win_condition(self.options.win_condition.value)

        startingOptionToAccess = {
            StartingTaskOption.option_ttc: ToontownItemName.TTC_ACCESS,
            StartingTaskOption.option_dd: ToontownItemName.DD_ACCESS,
            StartingTaskOption.option_dg: ToontownItemName.DG_ACCESS,
            StartingTaskOption.option_mml: ToontownItemName.MML_ACCESS,
            StartingTaskOption.option_tb: ToontownItemName.TB_ACCESS,
            StartingTaskOption.option_ddl: ToontownItemName.DDL_ACCESS
        }
        self.startingAccess = startingOptionToAccess.get(self.options.starting_task_playground.value, StartingTaskOption.option_ttc)
        # If our starting PG is random, figure out which one to use
        if self.options.starting_task_playground.value == StartingTaskOption.option_randomized:
            self.startingAccess = startingOptionToAccess.get(random.choice(list(startingOptionToAccess.keys())), StartingTaskOption.option_ttc)

    def calculate_bounties(self):
        required_bounties = self.options.bounties_required.value
        total_bounties = self.options.total_bounties.value
        self.valid_bounties.extend(locations.BOUNTY_LOCATIONS)

        # Fishing settings to remove specific bounties
        # Non-species logic
        if self.options.fish_checks.value in [1, 2]:
            for bounty in locations.FISH_SPECIES_BOUNTIES:
                self.valid_bounties.remove(bounty)
        # Species logic
        if self.options.fish_checks.value == 0:
            for bounty in locations.FISH_ALBUM_BOUNTIES:
                self.valid_bounties.remove(bounty)
        # No fishing
        if self.options.fish_checks.value == 3:
            for bounty in locations.ALL_FISH_BOUNTIES:
                self.valid_bounties.remove(bounty)

        # No racing
        if not self.options.racing_logic.value:
            for bounty in locations.RACE_BOUNTIES:
                self.valid_bounties.remove(bounty)

        # No golfing
        if not self.options.minigolf_logic.value:
            for bounty in locations.GOLF_BOUNTIES:
                self.valid_bounties.remove(bounty)

        # No boss checks
        if self.options.checks_per_boss.value == 0:
            for bounty in locations.BOSS_BOUNTIES:
                self.valid_bounties.remove(bounty)

        # No gag checks
        if self.options.gag_training_check_behavior.value == 2:
            for bounty in locations.GAG_BOUNTIES:
                self.valid_bounties.remove(bounty)

        # We omitted a gag track, remove its respective bounty from the pool
        OMITTABLE_BOUNTIES = [
            "NONE",
            ToontownLocationName.TRAP_TRAIN_UNLOCKED,
            ToontownLocationName.SOUND_OPERA_UNLOCKED,
            ToontownLocationName.THROW_WEDDING_UNLOCKED,
            ToontownLocationName.SQUIRT_GEYSER_UNLOCKED,
            ToontownLocationName.DROP_BOAT_UNLOCKED
        ]
        if self.options.omit_gag.value != 0:
            # Have to check just in the edge case it was removed above
            if OMITTABLE_BOUNTIES[self.options.omit_gag.value] in self.valid_bounties:
                self.valid_bounties.remove(OMITTABLE_BOUNTIES[self.options.omit_gag.value])

        # Remove bounties that are excluded
        valid_copy = self.valid_bounties.copy()
        for bounty in valid_copy:
            if bounty.value in self.options.exclude_locations.value:
                self.valid_bounties.remove(bounty)
        gen_bounties = len(self.valid_bounties)

        # If we want more bounties than our settings allow, overwrite values to prevent errors
        if total_bounties > gen_bounties:
            logging.warning(f"WARNING: [{self.multiworld.player_name[self.player]}] had too many bounties ({total_bounties}). Setting to {gen_bounties}.")
            self.options.total_bounties.value = gen_bounties
            total_bounties = self.options.total_bounties.value

        # If we want more bounties required than we have, overwrite values to prevent errors
        if required_bounties > total_bounties:
            logging.warning(
                f"WARNING: [{self.multiworld.player_name[self.player]}] had too many bounties required ({required_bounties}). Setting to {total_bounties}.")
            self.options.bounties_required.value = total_bounties

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

        # Now create locations.
        for i, location_data in enumerate(LOCATION_DEFINITIONS):
            # Do we skip this location generation?
            if location_data.type in forbidden_location_types:
                continue

            if location_data.region == ToontownRegionName.LOGIN:
                if location_data.name in [ToontownLocationName.STARTING_TRACK_ONE, ToontownLocationName.STARTING_TRACK_TWO] and not len(self.startingTracks) == 2:
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

        for location_data in EVENT_DEFINITIONS:
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
        self._force_item_placement(ToontownLocationName.STARTING_NEW_GAME,  ToontownItemName.TTC_ACCESS)
        if len(self.startingTracks) == 2:
            self._force_item_placement(ToontownLocationName.STARTING_TRACK_ONE, self.startingTracks[0])
            self._force_item_placement(ToontownLocationName.STARTING_TRACK_TWO, self.startingTracks[1])

        if self.options.omit_gag.value != 0 and self.options.gag_tracks_required.value >= 7:
            self.options.gag_tracks_required.value = 6
            logging.warning("Required Gag Tracks for goal is 7, but we omitted a Gag. Setting to 6.")

        # Force bounty placements
        if "bounties" in self.options.win_condition.value:
            self.calculate_bounties()

            # These bounties are priority placements, guaranteed to have bounties if we have enough room
            priority_bounties = []
            for bounty in self.valid_bounties:
                if bounty.value in self.options.priority_locations.value:
                    priority_bounties.append(bounty)

            # Finally place our bounties
            for created_bounty in range(self.options.total_bounties.value):
                if priority_bounties:
                    bounty_choice = random.choice(priority_bounties)
                    priority_bounties.remove(bounty_choice)
                else:
                    bounty_choice = random.choice(self.valid_bounties)
                self.valid_bounties.remove(bounty_choice)
                self.inserted_bounties.append(bounty_choice)

            for bounty in self.inserted_bounties:
                self._force_item_placement(bounty, ToontownItemName.BOUNTY)

            if self.options.hint_bounties.value:
                self.options.start_hints.value.add(ToontownItemName.BOUNTY.value)

        # only populate these locations if there's a reason to go there.
        if self.options.checks_per_boss.value > 0 or "cog-bosses" in self.options.win_condition.value:
            self._force_item_placement(ToontownLocationName.FIGHT_VP,  ToontownItemName.VP)
            self._force_item_placement(ToontownLocationName.FIGHT_CFO,  ToontownItemName.CFO)
            self._force_item_placement(ToontownLocationName.FIGHT_CJ,  ToontownItemName.CJ)
            self._force_item_placement(ToontownLocationName.FIGHT_CEO,  ToontownItemName.CEO)

        # Do we have force teleport access? if so place our tps
        if self.options.tpsanity.value == TPSanity.option_treasure:
            if self.startingAccess != ToontownItemName.TTC_ACCESS:
                self._force_item_placement(ToontownLocationName.TTC_TREASURE_1, ToontownItemName.TTC_ACCESS)
            if self.startingAccess != ToontownItemName.DD_ACCESS:
                self._force_item_placement(ToontownLocationName.DD_TREASURE_1, ToontownItemName.DD_ACCESS)
            if self.startingAccess != ToontownItemName.DG_ACCESS:
                self._force_item_placement(ToontownLocationName.DG_TREASURE_1, ToontownItemName.DG_ACCESS)
            if self.startingAccess != ToontownItemName.MML_ACCESS:
                self._force_item_placement(ToontownLocationName.MML_TREASURE_1, ToontownItemName.MML_ACCESS)
            if self.startingAccess != ToontownItemName.TB_ACCESS:
                self._force_item_placement(ToontownLocationName.TB_TREASURE_1, ToontownItemName.TB_ACCESS)
            if self.startingAccess != ToontownItemName.DDL_ACCESS:
                self._force_item_placement(ToontownLocationName.DDL_TREASURE_1, ToontownItemName.DDL_ACCESS)
            self._force_item_placement(ToontownLocationName.SBHQ_TREASURE_1, ToontownItemName.SBHQ_ACCESS)
            self._force_item_placement(ToontownLocationName.CBHQ_TREASURE_1, ToontownItemName.CBHQ_ACCESS)
            self._force_item_placement(ToontownLocationName.LBHQ_TREASURE_1, ToontownItemName.LBHQ_ACCESS)
            self._force_item_placement(ToontownLocationName.BBHQ_TREASURE_1, ToontownItemName.BBHQ_ACCESS)
            self._force_item_placement(ToontownLocationName.AA_TREASURE_1, ToontownItemName.AA_ACCESS)
            self._force_item_placement(ToontownLocationName.GS_TREASURE_1, ToontownItemName.GS_ACCESS)

        # Debug, use this to print a pretty picture to make sure our regions are set up correctly
        if DEBUG_MODE:
            from Utils import visualize_regions
            visualize_regions(self.multiworld.get_region("Menu", self.player), "toontown.puml")

    def create_items(self) -> None:
        pool = []

        # Spawn each defined item.
        for item in ITEM_DEFINITIONS:
            for _ in range(item.quantity):
                # we don't need to make the access key items for our starting PG
                if item.name == self.startingAccess:
                    continue
                pool.append(self.create_item(item.name.value))

        # Handle Cog Disguise generation
        bosses_condition = "cog-bosses" in self.options.win_condition.value
        if not bosses_condition and self.options.checks_per_boss.value == 0:
            # Bosses aren't relevant to the seed, we don't want disguises to be on priority and
            # not progression balanced.
            for itemName in DISGUISE_ITEMS:
                pool.append(self.create_progression_deprioritized_skip_balancing(itemName.value))
        else:
            # Bosses are relevant to the seed, make them progression as normal
            for itemName in DISGUISE_ITEMS:
                pool.append(self.create_item(itemName.value))

        # Handle facility key generation
        if self.options.facility_locking.value == FacilityLocking.option_keys:
            for itemName in FACILITY_KEY_ITEMS:
                pool.append(self.create_item(itemName.value))

        # Handle teleport access item generation.
        if self.options.tpsanity.value in (TPSanity.option_keys, TPSanity.option_shuffle):
            for itemName in TELEPORT_ACCESS_ITEMS:
                # Handle giving out access based on our starting PG
                if itemName == self.startingAccess:
                    if self.startingAccess == ToontownItemName.TTC_ACCESS:
                        self.multiworld.push_precollected(self.create_item(itemName.value))
                    else:
                        for _ in range(2):
                            self.multiworld.push_precollected(self.create_item(itemName.value))
                else:
                    # We have our facility keys set to access, make 2 of each of those
                    if itemName in (ToontownItemName.SBHQ_ACCESS, ToontownItemName.CBHQ_ACCESS, ToontownItemName.LBHQ_ACCESS, ToontownItemName.BBHQ_ACCESS) \
                                and self.options.facility_locking.value == FacilityLocking.option_access:
                        for _ in range(2):
                            pool.append(self.create_item(itemName.value))
                    else:
                        pool.append(self.create_item(itemName.value))
        # handle task carry capacity item generation.
        # the amount to give will be based on the starting capacity defined by the yaml
        for _ in range(max(0, self.options.max_task_capacity.value - self.options.starting_task_capacity.value)):
            pool.append(self.create_item(ToontownItemName.TASK_CAPACITY.value))

        # handle joke book item generation
        joke_books = [
            ToontownItemName.TTC_JOKE_BOOK.value,
            ToontownItemName.DD_JOKE_BOOK.value,
            ToontownItemName.DG_JOKE_BOOK.value,
            ToontownItemName.MML_JOKE_BOOK.value,
            ToontownItemName.TB_JOKE_BOOK.value,
            ToontownItemName.DDL_JOKE_BOOK.value
        ]
        # we only want joke books if we have jokes on
        if self.options.jokes_per_street.value > 0 and self.options.joke_books.value:
            for book in joke_books:
                pool.append(self.create_item(book))

        # Automatically apply teleport access across the board so hq access can be gotten from an item
        if self.options.tpsanity.value == TPSanity.option_none:
            for itemName in TELEPORT_ACCESS_ITEMS:
                # Our starting HQ isn't TTC, don't make an extra TTC access and actually add one to the pool
                if self.startingAccess != ToontownItemName.TTC_ACCESS and itemName == ToontownItemName.TTC_ACCESS:
                    pool.append(self.create_item(itemName.value))
                    continue
                # Make 2 for any starting access that isn't TTC
                if itemName == self.startingAccess and self.startingAccess != ToontownItemName.TTC_ACCESS:
                    for _ in range(2):
                        self.multiworld.push_precollected(self.create_item(itemName.value))
                else:
                    # We have our facility keys set to access, make an extra of each
                    if itemName in (ToontownItemName.SBHQ_ACCESS, ToontownItemName.CBHQ_ACCESS, ToontownItemName.LBHQ_ACCESS, ToontownItemName.BBHQ_ACCESS) \
                                and self.options.facility_locking.value == FacilityLocking.option_access:
                        pool.append(self.create_item(itemName.value))
                    self.multiworld.push_precollected(self.create_item(itemName.value))

        # Automatically give both keys at the start for treasure TP sanity
        if self.options.tpsanity.value == TPSanity.option_treasure:
            if self.startingAccess == ToontownItemName.TTC_ACCESS:
                self.multiworld.push_precollected(self.create_item(self.startingAccess.value))
            else:
                for _ in range(2):
                    self.multiworld.push_precollected(self.create_item(self.startingAccess.value))
            # We have our facility keys set to access, make an extra of each
            if self.options.facility_locking.value == FacilityLocking.option_access:
                for itemName in TELEPORT_ACCESS_ITEMS:
                    if itemName in (ToontownItemName.SBHQ_ACCESS, ToontownItemName.CBHQ_ACCESS, ToontownItemName.LBHQ_ACCESS, ToontownItemName.BBHQ_ACCESS):
                        pool.append(self.create_item(itemName.value))

        # Dynamically generate laff boosts.
        max_laff = self.options.max_laff.value
        start_laff = self.options.starting_laff.value
        if start_laff > max_laff:
            self.options.max_laff.value = start_laff
            max_laff = self.options.max_laff.value
        if "laff-o-lympics" in self.options.win_condition.value:  # Our goal is laff-o-lympics, only progressive +1 Boost items
            # Lets make sure our goal isn't more than our max_laff
            # If it is, make our max the same as our goal
            required_laff = self.options.laff_points_required.value
            if required_laff > max_laff:
                self.options.max_laff.value = required_laff
                max_laff = self.options.max_laff.value

            LAFF_TO_GIVE = max_laff - start_laff

            for _ in range(LAFF_TO_GIVE):
                pool.append(self.create_item(ToontownItemName.LAFF_BOOST_1.value))
        else:  # If our goal isn't laff-o-lypics, generate laff items normally
            LAFF_TO_GIVE = max_laff - start_laff
            if LAFF_TO_GIVE < 0:
                logging.warning(f"[{self.multiworld.player_name[self.player]}] Too low max HP. Setting max HP to starting HP.")
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
        OMITTABLE_ITEMS = [
            "NONE",
            ToontownItemName.TRAP_FRAME,
            ToontownItemName.SOUND_FRAME,
            ToontownItemName.THROW_FRAME,
            ToontownItemName.SQUIRT_FRAME,
            ToontownItemName.DROP_FRAME
        ]
        for frame in items.GAG_TRAINING_FRAMES:
            # Skip the frame generation for our omitted track
            if self.options.omit_gag.value != 0:
                if frame == OMITTABLE_ITEMS[self.options.omit_gag.value]:
                    continue
            quantity = 8 if frame not in self.startingTracks else 7
            for _ in range(quantity):
                pool.append(self.create_item(frame.value))
        if len(self.startingTracks) != 2:  # we're not generating starting tracks...
            for frame in self.startingTracks:
                self.multiworld.push_precollected(self.create_item(frame.value))

        # Dynamically generate gag upgrades.
        OMIT_VALUE_TO_GAG_UPGRADES = {
            1: ToontownItemName.TRAP_UPGRADE,
            2: ToontownItemName.SOUND_UPGRADE,
            3: ToontownItemName.THROW_UPGRADE,
            4: ToontownItemName.SQUIRT_UPGRADE,
            5: ToontownItemName.DROP_UPGRADE
        }
        for upgrade in items.GAG_UPGRADES:
            if self.options.omit_gag.value != 0:
                if upgrade == OMIT_VALUE_TO_GAG_UPGRADES[self.options.omit_gag.value]:
                    continue
            pool.append(self.create_item(upgrade.value))

        # Dynamically generate training multipliers.
        GAG_MULTI_TO_GIVE = self.options.max_global_gag_xp.value - self.options.base_global_gag_xp.value
        gag_training_item = self.options.gag_frame_item_behavior.value
        gag_training_check = self.options.gag_training_check_behavior.value
        gags_pretrained = gag_training_item == GagTrainingFrameBehavior.option_trained
        gags_unlocked = gag_training_item == GagTrainingFrameBehavior.option_unlock
        checks_not_normal = gag_training_check != GagTrainingCheckBehavior.option_trained
        if GAG_MULTI_TO_GIVE < 0:
            logging.warning(f"[{self.multiworld.player_name[self.player]}] Too low max global gag XP. Setting max global gag XP to base global gag XP.")
            GAG_MULTI_TO_GIVE = 0
        TWO_GAG_MULTI_BOOSTS = round(consts.TWO_XP_BOOST_RATIO * GAG_MULTI_TO_GIVE)
        while TWO_GAG_MULTI_BOOSTS > 0 and GAG_MULTI_TO_GIVE > 2:
            TWO_GAG_MULTI_BOOSTS -= 1
            GAG_MULTI_TO_GIVE -= 2
            # Settings mean we don't have any logical reason for training, make items useful bc overflow
            if gags_pretrained or (gags_unlocked and checks_not_normal):
                pool.append(self.create_useful_item(ToontownItemName.GAG_MULTIPLIER_2.value))
            else:
                pool.append(self.create_item(ToontownItemName.GAG_MULTIPLIER_2.value))
        for _ in range(GAG_MULTI_TO_GIVE):
            # Settings mean we don't have any logical reason for training, make items useful bc overflow
            if gags_pretrained or (gags_unlocked and checks_not_normal):
                pool.append(self.create_useful_item(ToontownItemName.GAG_MULTIPLIER_1.value))
            else:
                pool.append(self.create_item(ToontownItemName.GAG_MULTIPLIER_1.value))

        # Create fishing licenses.
        if self.options.fish_progression.value in (FishProgression.LicensesAndRods, FishProgression.Licenses):
            for fishLicense in FISHING_LICENSES:
                pool.append(self.create_item(fishLicense.value))

        # Create fishing rods.
        if self.options.fish_progression.value in (FishProgression.LicensesAndRods, FishProgression.Rods):
            for _ in range(4):
                pool.append(self.create_item(ToontownItemName.FISHING_ROD_UPGRADE.value))

        # racing item logic
        item = self.create_item(ToontownItemName.GO_KART.value)
        if self.options.racing_logic.value:
            pool.append(item)
        else:
            self.multiworld.push_precollected(item)

        # golfing item logic
        item = self.create_item(ToontownItemName.GOLF_PUTTER.value)
        if self.options.minigolf_logic.value:
            pool.append(item)
        else:
            self.multiworld.push_precollected(item)


        # Fill the rest of the room with junk.
        junk: int = len(self.multiworld.get_unfilled_locations(self.player)) - len(pool)
        if junk < 0:
            raise Exception(f"[Toontown - {self.multiworld.get_player_name(self.player)}] "
                            f"Generated with too many items ({-junk}). Please tweak settings.")

        trap: int = round(junk * (self.options.trap_percent / 100))
        filler: int = junk - trap
        for i in range(trap):
            pool.append(self.create_item(self.get_trap_item_name()))
        for i in range(filler):
            pool.append(self.create_item(self.get_filler_item_name()))

        # Finalize item pool.
        self.multiworld.itempool += pool

    def get_trap_item_name(self):
        trap_weights = {
            ToontownItemName.UBER_TRAP.value: self.options.uber_trap_weight,
            ToontownItemName.DRIP_TRAP.value: self.options.drip_trap_weight,
            ToontownItemName.BEAN_TAX_TRAP_750.value: (self.options.bean_tax_weight/3),
            ToontownItemName.BEAN_TAX_TRAP_1000.value: (self.options.bean_tax_weight/3),
            ToontownItemName.BEAN_TAX_TRAP_1250.value: (self.options.bean_tax_weight/3),
            ToontownItemName.GAG_SHUFFLE_TRAP.value: self.options.gag_shuffle_weight,
            ToontownItemName.DAMAGE_15.value: (self.options.damage_trap_weight/2),
            ToontownItemName.DAMAGE_25.value: (self.options.damage_trap_weight/2),
        }
        trap_items = list(trap_weights.keys())
        return random.choices(trap_items, weights=[trap_weights[i] for i in trap_items])[0]

    def get_filler_item_name(self):
        junk_weights = {
            ToontownItemName.MONEY_150.value: (self.options.bean_weight/4),
            ToontownItemName.MONEY_400.value: (self.options.bean_weight/4),
            ToontownItemName.MONEY_700.value: (self.options.bean_weight/4),
            ToontownItemName.MONEY_1000.value: (self.options.bean_weight/4),

            ToontownItemName.XP_10.value: (self.options.exp_weight*0.47),
            ToontownItemName.XP_15.value: (self.options.exp_weight*0.33),
            ToontownItemName.XP_20.value: (self.options.exp_weight*0.2),

            ToontownItemName.SOS_REWARD_3.value: (self.options.sos_weight*0.4),
            ToontownItemName.SOS_REWARD_4.value: (self.options.sos_weight*0.3),
            ToontownItemName.SOS_REWARD_5.value: (self.options.sos_weight*0.3),
            ToontownItemName.UNITE_REWARD_GAG.value: (self.options.unite_weight/2),
            ToontownItemName.UNITE_REWARD_TOONUP.value: (self.options.unite_weight/2),
            ToontownItemName.PINK_SLIP_REWARD.value: self.options.fire_weight,
            ToontownItemName.HEAL_10.value: (self.options.heal_weight/2),
            ToontownItemName.HEAL_20.value: (self.options.heal_weight/2),
            ToontownItemName.FISH.value: self.options.fish_weight,
        }
        junk_items = list(junk_weights.keys())
        return random.choices(junk_items, weights=[junk_weights[i] for i in junk_items])[0]

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
        # Check for our item links as well
        if self.options.item_links.value:
            for link in self.options.item_links.value:
                for item in link["item_pool"]:
                    local_itempool.append(self.item_name_to_id[item])

        local_locations = [
            [location.unique_id, location.name.value]
            for location in self.created_locations
        ]

        win_condition = ToontownWinCondition.from_options(self.options)

        # TODO: if actually removing tasks becomes implemented,
        #       check if there are still enough tasks to complete

        # If win condition is total_tasks, make sure that the player can actually complete them.
        # if self.options.win_condition_total_tasks.value and self.options.total_tasks_required.value > 6*self.options.logical_tasks_per_playground.value:
        #     raise Exception(f"[Toontown - {self.multiworld.get_player_name(self.player)}] "
        #                     f"Too many total tasks required (max is 6*logical_tasks: {6*self.options.logical_tasks_per_playground.value}), please tweak settings.")

        # If win condition is hood_tasks, make sure that the player can actually complete them.
        # if self.options.win_condition_hood_tasks.value and self.options.hood_tasks_required.value > self.options.logical_tasks_per_playground.value:
        #     raise Exception(f"[Toontown - {self.multiworld.get_player_name(self.player)}] "
        #                     f"Too many hood tasks required (max is logical_tasks: {self.options.logical_tasks_per_playground.value}), please tweak settings.")

        # Return the result.
        return {
            "seed": self.multiworld.seed,
            "team": self.options.team.value,
            "game_version": "v0.18.4",
            "seed_generation_type": self.options.seed_generation_type.value,
            "starting_laff": self.options.starting_laff.value,
            "max_laff": self.options.max_laff.value,
            "omit_gag": self.options.omit_gag.value,
            "starting_money": self.options.starting_money.value,
            "starting_task_capacity": self.options.starting_task_capacity.value,
            "max_task_capacity": self.options.max_task_capacity.value,
            "base_global_gag_xp": self.options.base_global_gag_xp.value,
            "damage_multiplier": self.options.damage_multiplier.value,
            "overflow_mod": self.options.overflow_mod.value,
            "win_condition": int(win_condition),
            "cog_bosses_required": self.options.cog_bosses_required.value,
            "total_tasks_required": self.options.total_tasks_required.value,
            "hood_tasks_required": self.options.hood_tasks_required.value,
            "gag_tracks_required": self.options.gag_tracks_required.value,
            "starting_task_playground": self.options.starting_task_playground.value,
            "fish_species_required": self.options.fish_species_required.value,
            "laff_points_required": self.options.laff_points_required.value,
            "bounties_required": self.options.bounties_required.value,
            "total_bounties": self.options.total_bounties.value,
            "hint_bounties": self.options.hint_bounties.value,
            "gag_training_check_behavior": self.options.gag_training_check_behavior.value,
            "gag_frame_item_behavior": self.options.gag_frame_item_behavior.value,
            "fish_locations": self.options.fish_locations.value,
            "fish_checks": self.options.fish_checks.value,
            "uber_trap_weight": self.options.uber_trap_weight.value,
            "drip_trap_weight": self.options.drip_trap_weight.value,
            "bean_tax_weight": self.options.bean_tax_weight.value,
            "gag_shuffle_weight": self.options.gag_shuffle_weight.value,
            "bean_weight": self.options.bean_weight.value,
            "exp_weight": self.options.exp_weight.value,
            "sos_weight": self.options.sos_weight.value,
            "unite_weight": self.options.unite_weight.value,
            "fire_weight": self.options.fire_weight.value,
            "fish_progression": self.options.fish_progression.value,
            "racing_logic": self.options.racing_logic.value,
            "golfing_logic": self.options.minigolf_logic.value,
            "maxed_cog_gallery_quota": self.options.maxed_cog_gallery_quota.value,
            "facility_locking": self.options.facility_locking.value,
            "death_link": self.options.death_link.value,
            "ring_link": self.options.ring_link.value,
            "slot_sync_jellybeans": self.options.slot_sync_jellybeans.value,
            "slot_sync_gag_experience": self.options.slot_sync_gag_experience.value,
            "pet_shop_display": self.options.pet_shop_display.value,
            "task_reward_display": self.options.task_reward_display.value,
            "local_itempool": local_itempool,
            "local_locations": local_locations,
            "tpsanity": self.options.tpsanity.value,
            "treasures_per_location": self.options.treasures_per_location.value,
            "checks_per_boss": self.options.checks_per_boss.value,
            "jokes_per_street": self.options.jokes_per_street.value,
            "joke_books": self.options.joke_books.value,
            "start_gag_xp": self.options.base_global_gag_xp.value,
            "max_gag_xp": self.options.max_global_gag_xp.value,
            "damage_trap_weight": self.options.damage_trap_weight.value,
            "heal_weight": self.options.heal_weight.value,
            "fish_weight": self.options.fish_weight.value,
            "random_prices": self.options.random_prices.value,
            "item_links": self.options.item_links.value,
            "fish_pity": self.options.fish_pity.value,
        }

    def calculate_starting_tracks(self, starting_gags: list):
        gag_to_item = {
            "toonup": ToontownItemName.TOONUP_FRAME,
            "trap": ToontownItemName.TRAP_FRAME,
            "lure": ToontownItemName.LURE_FRAME,
            "sound": ToontownItemName.SOUND_FRAME,
            "throw": ToontownItemName.THROW_FRAME,
            "squirt": ToontownItemName.SQUIRT_FRAME,
            "drop": ToontownItemName.DROP_FRAME
        }
        option_to_track = {
            1: "trap",
            2: "sound",
            3: "throw",
            4: "squirt",
            5: "drop"
        }
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
        rng = self.multiworld.random
        choices = ALL.copy()

        # Checking if the track we're wanting is in the starting list
        # Then also removing it from our options
        omitted_gag = self.options.omit_gag.value != 0
        omitted_track = self.options.omit_gag.value
        # If our omitted track is in our starting, randomize it
        if omitted_gag:
            if option_to_track[omitted_track] in set(starting_gags):
                starting_gags.remove(option_to_track[omitted_track])
                starting_gags.append("randomized")
            choices.remove(gag_to_item[option_to_track[omitted_track]])

        starting_random_gags = starting_gags.count("randomized")
        starting_gag_items = [gag_to_item[item] for item in set(starting_gags) if item in gag_to_item]
        wild_random = "wild" in set(starting_gags)


        for i in starting_gag_items:
            choices.remove(i)
        for i in range(starting_random_gags):
            if len(choices) == 0:
                break

            if wild_random:  # We don't consider any logic for our starting tracks
                chosen = rng.choice(choices)
                starting_gag_items.append(chosen)
                choices.remove(chosen)
            else:
                offensive_choices = OFFENSIVE.copy()
                if omitted_gag:
                    # Remove our omitted gag from our possible choices
                    if gag_to_item[option_to_track[omitted_track]] in offensive_choices:
                        offensive_choices.remove(gag_to_item[option_to_track[omitted_track]])
                if len(starting_gag_items) == 0:  # first gag always should be offensive.
                    chosen = rng.choice(offensive_choices)
                    starting_gag_items.append(chosen)
                    choices.remove(chosen)
                elif len(starting_gag_items) == 1:
                    first_track = starting_gag_items[0]
                    if first_track == ToontownItemName.TRAP_FRAME:
                        chosen = ToontownItemName.LURE_FRAME
                    elif first_track in SUPPORT:  # ensure an offensive gag if the first track was support
                        if first_track == ToontownItemName.TOONUP_FRAME:
                            if ToontownItemName.TRAP_FRAME in offensive_choices:
                                offensive_choices.remove(ToontownItemName.TRAP_FRAME)
                        chosen = rng.choice(offensive_choices)
                    else:
                        chosen = rng.choice(choices)
                    starting_gag_items.append(chosen)
                    choices.remove(chosen)
                else:
                    chosen = rng.choice(choices)
                    starting_gag_items.append(chosen)
                    choices.remove(chosen)


        ## Check to ensure sphere 1 isn't very likely to be empty.
        if (not any([gag in starting_gag_items for gag in OFFENSIVE])
            and self.options.treasures_per_location.value <= 1  # This is one to handle the edge case where our tpsanity is treasures
            and (self.options.fish_checks.value == self.options.fish_checks.option_none
                    or self.options.fish_progression.value in [
                    self.options.fish_progression.option_licenses,
                    self.options.fish_progression.option_licenses_and_rods
                ])
            ):
            logging.warning("[{self.multiworld.player_name[self.player]}] Sphere 1 likely contains very few checks, adding an offensive gag to starting gags to avoid this.")
            if ToontownItemName.LURE_FRAME in starting_gags:
                starting_gag_items.append(rng.choice(OFFENSIVE))
            else:
                choices = OFFENSIVE.copy()
                if omitted_gag:
                    # Remove our omitted gag from our possible choices
                    if gag_to_item[option_to_track[omitted_track]] in choices:
                        choices.remove(gag_to_item[option_to_track[omitted_track]])
                if ToontownItemName.TRAP_FRAME in choices:
                    choices.remove(ToontownItemName.TRAP_FRAME)
                starting_gag_items.append(rng.choice(choices))

        # Update the option to use the randomized values so that it outputs to spoiler log.
        item_to_gag = {v:k for k,v in gag_to_item.items()}
        self.options.starting_gags.value = [item_to_gag[i] for i in starting_gag_items]

        return starting_gag_items

    def convert_web_win_conditions(self) -> list:
        """
        Convert between web specific win condition options and the actual win condition option.
        """
        conditions = ["randomized"] * self.options.web_win_condition_randomized.value
        for toggled,condition in (
        (self.options.web_win_condition_bounty.value, "bounties"),
        (self.options.web_win_condition_cog_bosses.value, "cog-bosses"),
        (self.options.web_win_condition_fish_species.value, "fish-species"),
        (self.options.web_win_condition_gag_tracks.value, "gag-tracks"),
        (self.options.web_win_condition_hood_tasks.value, "hood-tasks"),
        (self.options.web_win_condition_laff_o_lympics.value, "laff-o-lympics"),
        (self.options.web_win_condition_total_tasks.value, "total-tasks")
        ):
            if toggled:
                conditions.append(condition)
        return conditions
    
    def randomize_win_condition(self, win_conditions: list) -> list:
        randomized = win_conditions.count("randomized")
        choices = list(self.options.win_condition.valid_keys)
        choices.remove("randomized")  # not a valid random choice
        for omitted_choice in self.options.conditions_omitted_when_randomized.value:
            choices.remove(omitted_choice)
        result = [i for i in set(win_conditions) if i != "randomized"]
        rng = self.multiworld.random
        for i in result:
            choices.remove(i)
        result += rng.sample(choices, k=min(randomized, len(choices)))
        return result

    def get_disabled_location_types(self) -> set[ToontownLocationType]:
        """
        Returns a set of disabled location types.
        These location types are removed from logic generation.
        """
        forbidden_location_types: set[ToontownLocationType] = set()
        fish_checks = FishChecks(self.options.fish_checks.value)
        if fish_checks == FishChecks.AllSpecies:
            forbidden_location_types.add(ToontownLocationType.FISHING_GENUS)
            forbidden_location_types.add(ToontownLocationType.FISHING_GALLERY)
        elif fish_checks == FishChecks.AllGalleryAndGenus:
            forbidden_location_types.add(ToontownLocationType.FISHING)
        elif fish_checks == FishChecks.AllGallery:
            forbidden_location_types.add(ToontownLocationType.FISHING)
            forbidden_location_types.add(ToontownLocationType.FISHING_GENUS)
        elif fish_checks == FishChecks.Nonne:
            forbidden_location_types.add(ToontownLocationType.FISHING)
            forbidden_location_types.add(ToontownLocationType.FISHING_GENUS)
            forbidden_location_types.add(ToontownLocationType.FISHING_GALLERY)

        tpl = self.options.treasures_per_location.value
        # If treasures are 0, but our tp sanity is treasures; let's make it one to avoid crashes on gen
        if tpl == 0 and self.options.tpsanity.value == TPSanity.option_treasure:
            self.options.treasures_per_location.value = 1
            tpl = self.options.treasures_per_location.value
        rev_locs = TREASURE_LOCATION_TYPES[::-1]
        for i in range(len(rev_locs) - tpl):
            forbidden_location_types.add(rev_locs[i])

        kkps = self.options.jokes_per_street.value
        rev_locs = KNOCK_KNOCK_LOCATION_TYPES[::-1]
        for i in range(len(rev_locs) - kkps):
            forbidden_location_types.add(rev_locs[i])

        cpb = self.options.checks_per_boss.value
        rev_locs = BOSS_LOCATION_TYPES[::-1]
        for i in range(len(rev_locs) - cpb):
            forbidden_location_types.add(rev_locs[i])
        wcb = "cog-bosses" in self.options.win_condition.value
        if cpb <= 0 and not wcb:
            forbidden_location_types.add(ToontownLocationType.BOSS_META)

        racing = self.options.racing_logic.value
        if not racing:
            forbidden_location_types.add(ToontownLocationType.RACING)

        golf = self.options.minigolf_logic.value
        if not golf:
            forbidden_location_types.add(ToontownLocationType.GOLF)

        GAG_LOCATION_TYPES = [
            ToontownLocationType.SUPPORT_GAG_TRAINING,
            ToontownLocationType.TRAP_GAG_TRAINING,
            ToontownLocationType.SOUND_GAG_TRAINING,
            ToontownLocationType.THROW_GAG_TRAINING,
            ToontownLocationType.SQUIRT_GAG_TRAINING,
            ToontownLocationType.DROP_GAG_TRAINING,
        ]

        gags = self.options.gag_training_check_behavior.value
        if gags == GagTrainingCheckBehavior.option_disabled:
            for type in GAG_LOCATION_TYPES:
                forbidden_location_types.add(type)

        omitted_track = self.options.omit_gag.value
        if omitted_track != 0:
            forbidden_location_types.add(GAG_LOCATION_TYPES[omitted_track])

        return forbidden_location_types

    def _force_item_placement(self, location: ToontownLocationName, item: ToontownItemName) -> None:
        self.multiworld.get_location(location.value, self.player).place_locked_item(self.create_item(item.value))
