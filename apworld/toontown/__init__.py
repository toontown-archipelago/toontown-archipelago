from typing import Dict, Any, List

from BaseClasses import Tutorial, Region, ItemClassification, CollectionState, Location, LocationProgressType
from worlds.AutoWorld import World, WebWorld
import random
from worlds.generic.Rules import set_rule

from . import regions, consts
from .consts import ToontownItem, ToontownLocation, ToontownWinCondition
from .items import ITEM_DESCRIPTIONS, ITEM_DEFINITIONS, ToontownItemDefinition, get_item_def_from_id, ToontownItemName, \
    ITEM_NAME_TO_ID, FISHING_LICENSES, TELEPORT_ACCESS_ITEMS, FACILITY_KEY_ITEMS
from .locations import LOCATION_DESCRIPTIONS, LOCATION_DEFINITIONS, EVENT_DEFINITIONS, ToontownLocationName, \
    ToontownLocationType, ALL_TASK_LOCATIONS_SPLIT, LOCATION_NAME_TO_ID, ToontownLocationDefinition, \
    TREASURE_LOCATION_TYPES, BOSS_LOCATION_TYPES
from .options import ToontownOptions, TPSanity, StartingTaskOption, GagTrainingCheckBehavior, FacilityLocking, toontown_option_groups
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

    def create_progression_item(self, name: str) -> ToontownItem:
        item_id: int = self.item_name_to_id[name]
        item_def: ToontownItemDefinition = get_item_def_from_id(item_id)
        return ToontownItem(name, ItemClassification.progression, item_id, self.player)

    def create_event(self, event: str) -> ToontownItem:
        return ToontownItem(event, ItemClassification.progression_skip_balancing, None, self.player)

    def generate_early(self) -> None:
        # Calculate what our starting gag tracks should be
        first_track, second_track = self.calculate_starting_tracks()

        # Save as attributes so we can reference this later in fill_slot_data()
        self.first_track = first_track
        self.second_track = second_track

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
        self._force_item_placement(ToontownLocationName.STARTING_NEW_GAME,  ToontownItemName.TTC_ACCESS)
        self._force_item_placement(ToontownLocationName.STARTING_TRACK_ONE, self.first_track)
        self._force_item_placement(ToontownLocationName.STARTING_TRACK_TWO, self.second_track)

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

        # Handle facility key generation
        if self.options.facility_locking == FacilityLocking.option_keys:
            for itemName in FACILITY_KEY_ITEMS:
                item = self.create_item(itemName.value)
                pool.append(item)

        # Handle teleport access item generation.
        if self.options.tpsanity.value in (TPSanity.option_keys, TPSanity.option_shuffle):
            for itemName in TELEPORT_ACCESS_ITEMS:
                item = self.create_item(itemName.value)
                # Handle giving out access based on our starting PG
                if itemName == self.startingAccess:
                    if self.startingAccess == ToontownItemName.TTC_ACCESS:
                        self.multiworld.push_precollected(item)
                    else:
                        for _ in range(2):
                            self.multiworld.push_precollected(item)
                else:
                    # We have our facility keys set to access, make 2 of each of those
                    if itemName in (ToontownItemName.SBHQ_ACCESS, ToontownItemName.CBHQ_ACCESS, ToontownItemName.LBHQ_ACCESS, ToontownItemName.BBHQ_ACCESS) \
                                and self.options.facility_locking == FacilityLocking.option_access:
                        for _ in range(2):
                            pool.append(item)
                    else:
                        pool.append(item)
        # handle task carry capacity item generation.
        # the amount to give will be based on the starting capacity defined by the yaml
        item = self.create_item(ToontownItemName.TASK_CAPACITY.value)
        for _ in range(max(0, self.options.max_task_capacity.value - self.options.starting_task_capacity.value)):
            pool.append(item)

        # Automatically apply teleport access across the board so hq access can be gotten from an item
        if self.options.tpsanity.value == TPSanity.option_none:
            for itemName in TELEPORT_ACCESS_ITEMS:
                item = self.create_item(itemName.value)
                # Our starting HQ isn't TTC, don't make an extra TTC access and actually add one to the pool
                if self.startingAccess != ToontownItemName.TTC_ACCESS and itemName == ToontownItemName.TTC_ACCESS:
                    pool.append(item)
                    continue
                # Make 2 for any starting access that isn't TTC
                if itemName == self.startingAccess and self.startingAccess != ToontownItemName.TTC_ACCESS:
                    for _ in range(2):
                        self.multiworld.push_precollected(item)
                else:
                    # We have our facility keys set to access, make an extra of each
                    if itemName in (ToontownItemName.SBHQ_ACCESS, ToontownItemName.CBHQ_ACCESS, ToontownItemName.LBHQ_ACCESS, ToontownItemName.BBHQ_ACCESS) \
                                and self.options.facility_locking == FacilityLocking.option_access:
                        pool.append(item)
                    self.multiworld.push_precollected(item)

        # Automatically give both keys at the start for treasure TP sanity
        if self.options.tpsanity.value == TPSanity.option_treasure:
            item = self.create_item(self.startingAccess.value)
            if self.startingAccess == ToontownItemName.TTC_ACCESS:
                self.multiworld.push_precollected(item)
            else:
                for _ in range(2):
                    self.multiworld.push_precollected(item)
            # We have our facility keys set to access, make an extra of each
            if self.options.facility_locking == FacilityLocking.option_access:
                for itemName in TELEPORT_ACCESS_ITEMS:
                    item = self.create_item(itemName.value)
                    if itemName in (ToontownItemName.SBHQ_ACCESS, ToontownItemName.CBHQ_ACCESS, ToontownItemName.LBHQ_ACCESS, ToontownItemName.BBHQ_ACCESS):
                        pool.append(item)

        # Dynamically generate laff boosts.
        if self.options.win_condition_laff_o_lympics:  # Our goal is laff-o-lympics, only progressive +1 Boost items
            # Lets make sure our goal isn't more than our max_laff
            # If it is, make our max laff the same as our goal
            LAFF_TO_GIVE = max(self.options.laff_points_required, self.options.max_laff.value) - self.options.starting_laff.value

            for _ in range(LAFF_TO_GIVE):
                pool.append(self.create_item(ToontownItemName.LAFF_BOOST_1.value))
        else:  # If our goal isn't laff-o-lypics, generate laff items normally
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
            quantity = 8 if frame not in (self.first_track, self.second_track) else 7
            for _ in range(quantity):
                pool.append(self.create_item(frame.value))

        # Dynamically generate gag upgrades.
        for upgrade in items.GAG_UPGRADES:
            pool.append(self.create_item(upgrade.value))

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
            pool.append(self.create_item(self.make_random_trap()))
        for i in range(filler):
            pool.append(self.create_item(self.make_random_junk()))

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

        # Finalize item pool.
        self.multiworld.itempool += pool

    def make_random_trap(self):
        trap_weights = {
            ToontownItemName.UBER_TRAP.value: self.options.uber_trap_weight,
            ToontownItemName.DRIP_TRAP.value: self.options.drip_trap_weight,
            ToontownItemName.BEAN_TAX_TRAP_750.value: (self.options.bean_tax_weight/3),
            ToontownItemName.BEAN_TAX_TRAP_1000.value: (self.options.bean_tax_weight/3),
            ToontownItemName.BEAN_TAX_TRAP_1250.value: (self.options.bean_tax_weight/3),
            ToontownItemName.GAG_SHUFFLE_TRAP.value: self.options.gag_shuffle_weight
        }
        trap_items = list(trap_weights.keys())
        return random.choices(trap_items, weights=[trap_weights[i] for i in trap_items])[0]

    def make_random_junk(self):
        junk_weights = {
            ToontownItemName.MONEY_150.value: (self.options.bean_weight/4),
            ToontownItemName.MONEY_400.value: (self.options.bean_weight/4),
            ToontownItemName.MONEY_700.value: (self.options.bean_weight/4),
            ToontownItemName.MONEY_1000.value: (self.options.bean_weight/4),
            # money_weight = 100

            ToontownItemName.XP_10.value: (self.options.exp_weight*0.47),
            ToontownItemName.XP_15.value: (self.options.exp_weight*0.33),
            ToontownItemName.XP_20.value: (self.options.exp_weight*0.2),

            ToontownItemName.SOS_REWARD.value: self.options.sos_weight,
            ToontownItemName.UNITE_REWARD.value: self.options.unite_weight,
            ToontownItemName.PINK_SLIP_REWARD.value: self.options.fire_weight,
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
            "seed_generation_type": self.options.seed_generation_type.value,
            "starting_laff": self.options.starting_laff.value,
            "max_laff": self.options.max_laff.value,
            "starting_money": self.options.starting_money.value,
            "starting_task_capacity": self.options.starting_task_capacity.value,
            "max_task_capacity": self.options.max_task_capacity.value,
            "base_global_gag_xp": self.options.base_global_gag_xp.value,
            "damage_multiplier": self.options.damage_multiplier.value,
            "overflow_mod": self.options.overflow_mod.value,
            "first_track": self.first_track.value,
            "second_track": self.second_track.value,
            "win_condition": int(win_condition),
            "cog_bosses_required": self.options.cog_bosses_required.value,
            "total_tasks_required": self.options.total_tasks_required.value,
            "hood_tasks_required": self.options.hood_tasks_required.value,
            "gag_tracks_required": self.options.gag_tracks_required.value,
            "starting_task_playground": self.options.starting_task_playground.value,
            "fish_species_required": self.options.fish_species_required.value,
            "laff_points_required": self.options.laff_points_required.value,
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
            "slot_sync_jellybeans": self.options.slot_sync_jellybeans.value,
            "slot_sync_gag_experience": self.options.slot_sync_gag_experience.value,
            "local_itempool": local_itempool,
            "tpsanity": self.options.tpsanity.value,
            "treasures_per_location": self.options.treasures_per_location.value,
            "checks_per_boss": self.options.checks_per_boss.value,
            "start_gag_xp": self.options.base_global_gag_xp.value,
            "max_gag_xp": self.options.max_global_gag_xp.value
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
            tpl = 1
        rev_locs = TREASURE_LOCATION_TYPES[::-1]
        for i in range(len(rev_locs) - tpl):
            forbidden_location_types.add(rev_locs[i])

        cpb = self.options.checks_per_boss.value
        rev_locs = BOSS_LOCATION_TYPES[::-1]
        for i in range(len(rev_locs) - cpb):
            forbidden_location_types.add(rev_locs[i])

        racing = self.options.racing_logic.value
        if not racing:
            forbidden_location_types.add(ToontownLocationType.RACING)

        golf = self.options.minigolf_logic.value
        if not golf:
            forbidden_location_types.add(ToontownLocationType.GOLF)

        gags = self.options.gag_training_check_behavior.value
        if gags == GagTrainingCheckBehavior.option_disabled:
            forbidden_location_types.add(ToontownLocationType.GAG_TRAINING)

        return forbidden_location_types

    def _force_item_placement(self, location: ToontownLocationName, item: ToontownItemName) -> None:
        self.multiworld.get_location(location.value, self.player).place_locked_item(self.create_item(item.value))
