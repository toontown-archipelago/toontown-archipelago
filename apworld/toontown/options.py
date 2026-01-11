from dataclasses import dataclass
from Options import PerGameCommonOptions, Range, Choice, Toggle, OptionGroup, ProgressionBalancing, Accessibility, OptionList, OptionSet, StartInventoryPool, Visibility


class TeamOption(Range):
    """
    Experimental option to set what team you are on. Do not use unless you are admin'ing a race.
    """
    display_name = "Team"
    range_start = 0
    range_end = 20
    default = 0


class StartLaffOption(Range):
    """
    The starting amount of max Laff Points to have when starting a new game.
    """
    display_name = "Starting Laff"
    range_start = 1
    range_end = 80
    default = 20


class StartGagOption(OptionList):
    """
    The gags to have when starting a new game. "randomized" will be replaced with a valid track.
    you cannot start with gags above level 1, duplicate values other than "randomized" will be ignored.

    valid keys: {"randomized", "toonup", "trap", "lure", "sound", "throw", "squirt", "drop"}
    ex. ["toonup, "sound"] will start you with toonup and sound as starting tracks.
    ex. ["sound"] will start you with only sound as a starting track.
    Note: You can add "wild" to this list in order to remove any sanity/logic behind randomized gag choices (being able to do damage)
    (cont.) This will allow for gag combinations such as ["trap", "toonup"] to be possible with randomization
    ex. ['wild', 'randomized', 'randomized'] will roll two random tracks with no consideration
    An empty list will start you with no gag tracks.
    """
    display_name = "Starting Gags"
    valid_keys = {
        "randomized",
        "toonup",
        "trap",
        "lure",
        "sound",
        "throw",
        "squirt",
        "drop",
        "wild"
    }
    default = ["randomized", "randomized"]
    visibility = ~(Visibility.simple_ui|Visibility.complex_ui)


class StartGagOptionWeb(OptionSet):
    """
    The gags to have when starting a new game.
    """
    display_name = "Starting Gags"
    valid_keys = {
        "toonup",
        "trap",
        "lure",
        "sound",
        "throw",
        "squirt",
        "drop"
    }
    default = []
    visibility = Visibility.simple_ui|Visibility.complex_ui


class StartGagRandomWeb(Range):
    """
    Randomized starting gag count, this will add to the list of starting gags above.
    """
    display_name = "Starting Gags"
    range_start = 0
    range_end = 7
    default = 2
    visibility = Visibility.simple_ui|Visibility.complex_ui


class OmitGagOption(Choice):
    """
    Choose an offensive gag track to not receive during the seed.
    none (default): Receive all Gag tracks
    trap: Never receive Trap Gags
    sound: Never receive Sound Gags
    throw: Never receive Throw Gags
    squirt: Never receive Squirt Gags
    drop: Never receive Drop Gags
    randomized: Pick a random Gag track to not receive during the seed
    randomsingle: Pick a random single target Gag track to not receive during the seed
    """
    display_name = "Omit Offensive Gag Track"
    option_none = 0
    option_trap = 1
    option_sound = 2
    option_throw = 3
    option_squirt = 4
    option_drop = 5
    option_randomized = 6
    option_randomsingle = 7
    default = 0


class MaxLaffOption(Range):
    """
    The max laff you can get from items throughout the run.
    Must be above or equal to the starting_laff.
    """
    display_name = "Max Laff"
    range_start = 34
    range_end = 150
    default = 150


class BaseGlobalGagXPRange(Range):
    """
    The base global gag experience multiplier when starting a new game.
    This multiplier is globally multiplicative on top of in-game boosts.
    """
    display_name = "Base Global Gag XP"
    range_start = 1
    range_end = 10
    default = 5


class MaxGlobalGagXPRange(Range):
    """
    Additional global gag experience that can be obtained from items.
    Stacks additively onto the base value above.
    Must be above or equal to the base_global_gag_xp.
    """
    display_name = "Max Global Gag XP"
    range_start = 0
    range_end = 30
    default = 30


class StartDamageMultiplierRange(Range):
    """
    The percentage of damage that will be done when battling Cogs at the start of the run.
    75 -> 75%/0.75x damage, 200 -> 200%/2x damage, etc.
    """
    display_name = "Starting Damage Percentage"
    range_start = 50
    range_end = 200
    default = 100


class MaxDamageMultiplierRange(Range):
    """
    The percentage of damage that can be reached at max.
    75 -> 75%/0.75x damage, 200 -> 200%/2x damage, etc.
    """
    display_name = "Maximum Damage Percentage"
    range_start = 70
    range_end = 200
    default = 100


class OverflowModRange(Range):
    """
    The percentage multiplier that will given with exp overflow.
    50 -> 50%/Half overflow rate, 200 -> 200%/2x overflow rate, etc.
    """
    display_name = "Overflow Rate Modifier"
    range_start = 25
    range_end = 300
    default = 100


class StartMoneyOption(Range):
    """
    The starting amount of jellybeans to have when starting a new game.
    """
    display_name = "Starting Jellybeans"
    range_start = 0
    range_end = 1000
    default = 1000


class StartingTaskCapacityOption(Range):
    """
    The starting amount of tasks a toon can hold when starting a new game.
    """
    display_name = "Starting Task Capacity"
    range_start = 1
    range_end = 6
    default = 4


class MaxTaskCapacityOption(Range):
    """
    The max amount of tasks a toon can hold.
    """
    display_name = "Max Task Capacity"
    range_start = 1
    range_end = 6
    default = 6


class WinConditions(OptionList):
    """
    Determines the condition required before being able to talk to Flippy to complete the game.
    At least one of these should be enabled.

    valid keys: ["cog-bosses", "bounties", "total-tasks", "hood-tasks", "gag-tracks",
                 "fish-species", "laff-o-lympics", "randomized"]

    "cog-bosses" - Player must defeat enough bosses (determined by cog_bosses_required)
    "bounties" - Player must collect enough bounties in their own world (determined by bounties_required, total_bounties)
    "total-tasks" - Player must complete enough ToonTasks (determined by total_tasks_required)
    "hood-tasks" - Player must complete enough ToonTasks in each Playground (determined by hood_tasks_required)
    "gag-tracks" - Player must max enough Gag Tracks (determined by gag_tracks_required)
    "fish-species" - Player must catch enough fish species (determined by fish_species_required)
    "laff-o-lympics" - Player must reach a certain amount of laff (determined by laff_points_required)
                       NOTE: Replaces ALL Laff Boosts with +1 Laff Boosts
    "randomized" - Will choose a random not-yet chosen goal as one of your goals.
                   NOTE: Can be input into the below list multiple times for multiple random goals
    Examples: ["cog-bosses", "hood-tasks"] | ["randomized", "randomized", "gag-tracks"]
    """
    display_name = "Win Conditions"
    valid_keys = {
        "randomized",
        "cog-bosses",
        "total-tasks",
        "hood-tasks",
        "gag-tracks",
        "fish-species",
        "laff-o-lympics",
        "bounties"
    }
    default = ["cog-bosses"]
    visibility = ~(Visibility.simple_ui|Visibility.complex_ui)


class OmitRandomWinConditions(OptionList):
    """
    Allows for the selected win conditions to be omitted when randomizing a win condition.
    Example: Adding "bounties" to this option will ensure bounties can't be rolled when you roll for a randomized win condition

    valid keys: ["cog-bosses", "bounties", "total-tasks", "hood-tasks", "gag-tracks",
                 "fish-species", "laff-o-lympics"]

    Examples: ["cog-bosses", "hood-tasks"] | ["randomized", "randomized", "gag-tracks"]
    """
    display_name = "Win Conditions Omitted when Randomized"
    valid_keys = {
        "cog-bosses",
        "total-tasks",
        "hood-tasks",
        "gag-tracks",
        "fish-species",
        "laff-o-lympics",
        "bounties"
    }
    default = []
    visibility = ~(Visibility.simple_ui|Visibility.complex_ui)


class WinConditionCogBossesWeb(Toggle):
    """Defeat a number of cog bosses to complete the game (determined by cog_bosses_required)."""
    display_name = "Cog Bosses"
    default = True
    visibility = Visibility.simple_ui|Visibility.complex_ui


class CogBossesRequired(Range):
    """
    How many cog bosses must be defeated before being able to talk to Flippy to complete the game.
    Unused if win_condition is not cog_bosses.
    """
    display_name = "Bosses Required"
    range_start = 0
    range_end = 4
    default = 3


class WinConditionTotalTasksWeb(Toggle):
    """Complete a total number of tasks to complete the game (determined by total_tasks_required)."""
    display_name = "Total Tasks"
    default = False
    visibility = Visibility.simple_ui|Visibility.complex_ui


class TotalTasksRequired(Range):
    """
    How many total tasks must be finished before being able to talk to Flippy to complete the game.
    Must be less than total tasks in game (6 zones times logical_tasks_per_playground tasks).
    Unused if win_condition is not total_tasks.
    """
    display_name = "Tasks Required"
    range_start = 0
    range_end = 72
    default = 48


class WinConditionHoodTasksWeb(Toggle):
    """Complete a number of tasks from each neighborhood to complete the game (determined by hood_tasks_required)."""
    display_name = "Hood Tasks"
    default = False
    visibility = Visibility.simple_ui|Visibility.complex_ui


class HoodTasksRequired(Range):
    """
    How many tasks must be finished in each neighborhood before being able to talk to Flippy to complete the game.
    Must be less than logical_tasks_per_playground.
    Unused if win_condition is not hood_tasks.
    """
    display_name = "Hood Tasks Count"
    range_start = 0
    range_end = 12
    default = 8


class WinConditionTotalGagTracksWeb(Toggle):
    """Max a certain number of gag tracks to complete the game (determined by gag_tracks_required)."""
    display_name = "Gag Tracks Maxed"
    default = False
    visibility = Visibility.simple_ui|Visibility.complex_ui


class GagTracksRequired(Range):
    """
    How many gag tracks must be maxxed before being able to talk to Flippy to complete the game.
    Must be less than or equal to total number of gag tracks a toon can obtain.
    Unused if win_condition is not total_gag_tracks
    """
    display_name = "Tracks Required"
    range_start = 0
    range_end = 7
    default = 5


class WinConditionFishSpeciesWeb(Toggle):
    """Catch a certain amount of fish species to complete the game (determined by fish_species_required)."""
    display_name = "Fish Species"
    default = False
    visibility = Visibility.simple_ui|Visibility.complex_ui


class FishSpeciesRequired(Range):
    """
    How many fish species must be caught before being able to talk to Flippy to complete the game.
    Must be less than or equal to total number of fish species a toon can obtain.
    Unused if win_condition is not total_fish_species
    """
    display_name = "Fish Required"
    range_start = 0
    range_end = 70
    default = 60


class WinConditionLaffOLympicsWeb(Toggle):
    """Reach a certain amount of laff to complete the game (determined by laff_points_required)."""
    display_name = "Laff o lympics"
    default = False
    visibility = Visibility.simple_ui|Visibility.complex_ui


class LaffPointsRequired(Range):
    """
    How many laff points we must have before being able to talk to Flippy to complete the game.
    Setting must be below or equal to max_laff setting
    Unused if win_condition is not laff_o_lympics
    """
    display_name = "Laff Required"
    range_start = 0
    range_end = 150
    default = 120


class WinConditionBountyWeb(Toggle):
    """Player must reach a certain number of bounty checks to complete the game (determined by bounties_required, total_bounties)"""
    display_name = "Bounty"
    default = False
    visibility = Visibility.simple_ui|Visibility.complex_ui


class BountiesRequired(Range):
    """
    How many bounties we must have before being able to talk to Flippy to complete the game
    Unused if win_condition is not bounty
    Range 0 to 34
    """
    display_name = "Bounties Required"
    range_start = 0
    range_end = 34
    default = 7


class TotalBounties(Range):
    """
    How many bounties are in the pool.
    Unused if win_condition is not bounty
    Must be equal to or above bounties_required
    Range 1 to 34
    """
    display_name = "Total Bounties"
    range_start = 1
    range_end = 34
    default = 15


class BountiesHinted(Toggle):
    """Should bounties be hinted from the beginning of the run?"""
    display_name = "Hinted Bounties"
    default = False


class WinConditionRandomizedWeb(Range):
    """
    How many additional random Win Conditions will be selected for goal?
    """
    display_name = "Randomized Win Conditions"
    range_start = 0
    range_end = len(WinConditions.valid_keys)
    default = 0
    visibility = Visibility.simple_ui|Visibility.complex_ui


class TPSanity(Choice):
    """
    Determines how Teleport Access is shuffled in the Item Pool for all Playgrounds/HQs.
    - keys: Playgrounds and HQs are locked until their respective Teleport Access is found.
    - treasure: All areas are accessible. Teleport Access items are guaranteed to spawn in their area treasure.
    - shuffle: All areas are accessible. Teleport Access items are shuffled in the pool.
    - none: All areas are accessible. You start with global teleport access.
    """
    display_name = "tpsanity"
    option_keys = 0
    option_treasure = 1
    option_shuffle = 2
    option_none = 3
    default = 0


class TreasuresPerLocation(Range):
    """
    The amount of archipelago treasures that'll have items in each location
    """
    display_name = "Treasures Per Location"
    range_start = 0
    range_end = 6
    default = 4


class JokeBookToggle(Toggle):
    """
    Add joke books to the item pool to lock knock knock jokes behind them
    NOTE: If jokes_per_street is set to 0 books will not be added to the pool
    """
    display_name = "Joke Book Toggle"
    default = True


class JokesPerStreet(Range):
    """
    The amount of knock knock doors that'll have checks on each street
    A setting above 0 will add per-playground joke books to the item pool, if enabled
    """
    display_name = "Knock Knock Jokes Per Street"
    range_start = 0
    range_end = 10
    default = 3


class ChecksPerBoss(Range):
    """
    How many checks you will receive from a cog boss upon completion.
    """
    display_name = "Checks Per Boss"
    range_start = 0
    range_end = 5
    default = 4


class GagTrainingCheckBehavior(Choice):
    """
    Behavior of how gag experience check locations are handled.

    unlock: When unlocking a new gag, you get its respective check.
    trained: When earning all available experience for a specific gag level, you get its respective check.
    disabled: Does not give checks for gags.
    """
    option_unlock = 0
    option_trained = 1
    option_disabled = 2
    default = 1

    display_name = "Gag Training Behavior"


class GagTrainingFrameBehavior(Choice):
    """
    Behavior of how gag frame items are handled

    vanilla: unlocks the gag when you get the exp required.
    unlock: unlocks the gag immediately, giving you the required exp directly.
    trained: maxes your experience in the track immediately, effectively disabling exp entirely until overcapped.
    """

    option_vanilla = 0
    option_unlock = 1
    option_trained = 2
    default = 0

    display_name = "Gag Frame Behavior"


class LogicalTasksPerPlayground(Range):
    """
    Determines the amount of tasks per playground that are in logic.
    """
    display_name = "Logical Tasks Per Playground"
    range_start = 0
    range_end = 12
    default = 12


class StartingTaskOption(Choice):
    """
    Determines what the starting playground is for quests (includes TP access)
    ttc: start with TTC access
    dd: start with DD access
    dg: start with DG access
    mml: start with MML access
    tb: start with TB access
    ddl: start with DDL access
    randomized: start with a randomized task access
    """
    display_name = "Starting Task Playground"
    option_ttc = 0
    option_dd = 1
    option_dg = 2
    option_mml = 3
    option_tb = 4
    option_ddl = 5
    option_randomized = 6
    default = 0


class LogicalMaxedCogGallery(Toggle):
    """
    Enable to make Cog Gallery Maxed checks be in logic.
    """
    display_name = "Logical Maxed Cog Gallery"
    default = True


class MaxedCogGalleryQuota(Range):
    """
    The amount of Cogs required to reach its maxed Cog Gallery.
    """
    display_name = "Maxed Cog Gallery Quota"
    range_start = 1
    range_end = 10
    default = 2


class FacilityLocking(Choice):
    """
    Determines how facilities are locked within a run.
    - keys: Default, each facility has its own key.
    - access: Adds a second area access key for each cog HQ to the pool that unlocks all facilities within.
    - unlocked: Facilities are unlocked from the start of the run.
    """
    display_name = "Facility Locking"
    option_keys = 0
    option_access = 1
    option_unlocked = 2
    default = 0


class FishLocations(Choice):
    """
    Determines where fish can spawn.
    - playgrounds: Fish spawn in their vanilla locations. Street-exclusive fish can be found anywhere in their playgrounds.
    - vanilla: Fish spawn in their vanilla locations. Street-exclusive fish remain in their vanilla locations.
    - global: Fish can spawn anywhere.
    """
    display_name = "Fish Locations"
    option_playgrounds = 0
    option_vanilla = 1
    option_global = 2
    default = 0


class FishChecks(Choice):
    """
    Determines the amount of items that can be found from fishing.
    - all_species: All 70 species will have an item.
    - all_gallery_and_genus: Every 10 species and unique genus will have an item.
    - all_gallery: Every 10 species will have an item.
    - none: There are no items in fishing.
    """
    display_name = "Fish Checks"
    option_all_species = 0
    option_all_gallery_and_genus = 1
    option_all_gallery = 2
    option_none = 3
    default = 0


class FishProgression(Choice):
    """
    Determines the progression for fishing.
    - licenses_and_rods: Both 'licenses' and 'rods' progression are active.
    - licenses: Playground fishing is restricted until their respective Fishing License is obtained. The player starts with a Gold Rod.
    - rods: Progressive fishing rod items are added to the pool.
    - none: All fishing areas are available. The player starts with a Gold Rod.
    """
    display_name = "Fish Progression"
    option_licenses_and_rods = 0
    option_licenses = 1
    option_rods = 2
    option_none = 3
    default = 2


class FishPity(Range):
    """
    The amount of pity (% chance of a guarantee) gained towards a new species per catch.
    """
    display_name = "Fishing Pity Per Catch"
    range_start = 0
    range_end = 100
    default = 25


class RacingOption(Toggle):
    """
    Enable to turn on racing checks.
    """

    display_name = "Racing Logic"
    default = False


class GolfingOption(Toggle):
    """
    Enable to turn on the minigolf checks.
    """

    display_name = "Golfing Logic"
    default = False


class SyncJellybeans(Toggle):
    """
    Enable to sync Jellybeans between toons on the same slot.
    Even if you aren't using multiple toons,
    leaving this on will retain your jellybeans if you need to make a new toon to reconnect.
    If this is 'false', the data will still be sent, but your toon will not sync with it.
    """
    display_name = "Sync Jellybeans"
    default = True


class SyncGagExp(Toggle):
    """
    Enable to sync Gag Experience between toons on the same slot.
    Even if you aren't using multiple toons,
    leaving this on will retain your gag experience if you need to make a new toon to reconnect.
    If this is 'false', the data will still be sent, but your toon will not sync with it.
    """
    display_name = "Sync Gag Exp"
    default = True


class RewardDisplayOption(Choice):
    """
    Controls display of rewards from something. intended to be subclassed.
    "hidden": hides what a multiworld reward will be, instead it'll name the check as the reward.
    "owner": hides what the item is, but shows who it's for.
    "class": hides what the item is, but shows who it's for, and what classification it has.
    "shown": (default) Tells you what the reward will be when you're looking at the check.
    "auto_hint": As shown, but also sends a hint out to the multiworld when you would be shown the reward.
    """
    option_hidden = 0
    option_owner = 1
    option_class = 2
    option_shown = 3
    option_auto_hint = 4
    default = 3


class TaskRewardDisplayOption(RewardDisplayOption):
    """
    Controls Display of ToonTask rewards.
    "hidden": hides what a multiworld reward will be, instead it'll name the check as the reward.
    "owner": hides what the item is, but shows who it's for.
    "class": hides what the item is, but shows who it's for, and what classification it has.
    "shown": (default) Tells you what the reward will be when you're looking at the check.
    "auto hint": As shown, but also sends a hint out to the multiworld when you would be shown the reward.
    """
    display_name = "Task Rewards"
    

class PetShopRewardDisplayOption(RewardDisplayOption):
    """
    Controls Display of Pet Shop Rewards.
    "hidden": hides what a multiworld reward will be, instead it'll name the check as the reward.
    "owner": hides what the item is, but shows who it's for.
    "class": hides what the item is, but shows who it's for, and what classification it has.
    "shown": (default) Tells you what the reward will be when you're looking at the check.
    "auto hint": As shown, but also sends a hint out to the multiworld when you would be shown the reward.
    """
    display_name = "Pet Shop Rewards"


class RandomShopCostToggle(Toggle):
    """
    Enable to turn on the pet shop price randomization.
    Logic accounts for the random price range if enabled.
    """

    display_name = "Randomize Pet Shop Prices"
    default = False


class SeedGenerationTypeOption(Choice):
    """
    Type of seeding to use when RNG checks happen in game.

    Global: RNG elements are determined solely by the AP seed
    Per Slot: RNG elements are determined by AP seed and Slot Name
    Per Toon: RNG elements are determined by AP seed and internal toon ID
    Wild: RNG elements are completely random and will shuffle upon relogging
    """
    option_global = 0
    option_slot_name = 1
    option_unique = 2
    option_wild = 3

    display_name = "Seed Generation Type"


class TrapPercentOption(Range):
    """
    Percentage of junk items to be replaced with traps
    """

    display_name = "Trap Percentage"
    range_start = 0
    range_end = 100
    default = 20


class UberWeightOption(Range):
    """
    Weight of uber traps in the trap pool.
    """

    display_name = "Uber Trap Weight"
    range_start = 0
    range_end = 100
    default = 80


class DripWeightOption(Range):
    """
    Weight of drip traps in the trap pool.
    """

    display_name = "Drip Trap Weight"
    range_start = 0
    range_end = 100
    default = 50


class TaxWeightOption(Range):
    """
    Weight of bean taxes in the trap pool.
    """

    display_name = "Bean Tax Weight"
    range_start = 0
    range_end = 100
    default = 36


class ShuffleWeightOption(Range):
    """
    Weight of gag shuffles in the trap pool.
    """

    display_name = "Gag Shuffle Weight"
    range_start = 0
    range_end = 100
    default = 80


class DamageWeightOption(Range):
    """
    Weight of damage items in the trap pool.
    """

    display_name = "Damage Trap Weight"
    range_start = 0
    range_end = 100
    default = 80


class BeanWeightOption(Range):
    """
    Weight of bean items in the junk pool.
    """

    display_name = "Bean Junk Weight"
    range_start = 0
    range_end = 100
    default = 100


class GagExpWeightOption(Range):
    """
    Weight of gag exp items in the junk pool.
    """

    display_name = "Exp Bundle Weight"
    range_start = 0
    range_end = 100
    default = 100


class SOSWeightOption(Range):
    """
    Weight of SOS card items in the junk pool.
    """

    display_name = "SOS Card Weight"
    range_start = 0
    range_end = 100
    default = 60


class UniteWeightOption(Range):
    """
    Weight of unite items in the junk pool.
    """

    display_name = "Unite Weight"
    range_start = 0
    range_end = 100
    default = 60


class FireWeightOption(Range):
    """
    Weight of Pink Slip items in the junk pool.
    """

    display_name = "Pink Slip Weight"
    range_start = 0
    range_end = 100
    default = 60


class SummonWeightOption(Range):
    """
    Weight of Cog Summon items in the junk pool.
    """

    display_name = "Cog Summon Weight"
    range_start = 0
    range_end = 100
    default = 50


class HealWeightOption(Range):
    """
    Weight of healing items in the junk pool.
    """

    display_name = "Healing Junk Weight"
    range_start = 0
    range_end = 100
    default = 75


class FishWeightOption(Range):
    """
    Weight of Fish items in the junk pool.
    """

    display_name = "Fish Junk Weight"
    range_start = 0
    range_end = 100
    default = 65


class DeathLinkOption(Choice):
    """
    Enable to turn on the "DeathLink" mechanic in Archipelago.
    "full": You die when someone else dies, simple.
    "drain": Laff drains over time from your current amount to 0, potentially recoverable.
    "one": Laff is set to 1 when someone else dies, potentially recoverable.
    "off": (default) Deathlink is disabled.
    """

    display_name = "Death Link"
    option_full = 0
    option_drain = 1
    option_one = 2
    option_off = 3
    default = 3


class RingLinkOption(Toggle):
    """
    Enable to turn on the "RingLink" mechanic in Archipelago.
    """

    display_name = "Ring Link"
    default = False

@dataclass
class ToontownOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    team: TeamOption
    max_laff: MaxLaffOption
    starting_laff: StartLaffOption
    starting_gags: StartGagOption
    omit_gag: OmitGagOption
    web_starting_gags: StartGagOptionWeb
    web_random_gags: StartGagRandomWeb
    base_global_gag_xp: BaseGlobalGagXPRange
    max_global_gag_xp: MaxGlobalGagXPRange
    start_damage_multiplier: StartDamageMultiplierRange
    max_damage_multiplier: MaxDamageMultiplierRange
    overflow_mod: OverflowModRange
    starting_money: StartMoneyOption
    starting_task_capacity: StartingTaskCapacityOption
    max_task_capacity: MaxTaskCapacityOption
    win_condition: WinConditions
    conditions_omitted_when_randomized: OmitRandomWinConditions
    web_win_condition_cog_bosses: WinConditionCogBossesWeb
    web_win_condition_total_tasks: WinConditionTotalTasksWeb
    web_win_condition_hood_tasks: WinConditionHoodTasksWeb
    web_win_condition_gag_tracks: WinConditionTotalGagTracksWeb
    web_win_condition_fish_species: WinConditionFishSpeciesWeb
    web_win_condition_laff_o_lympics: WinConditionLaffOLympicsWeb
    web_win_condition_bounty: WinConditionBountyWeb
    web_win_condition_randomized: WinConditionRandomizedWeb
    cog_bosses_required: CogBossesRequired
    total_tasks_required: TotalTasksRequired
    hood_tasks_required: HoodTasksRequired
    gag_tracks_required: GagTracksRequired
    fish_species_required: FishSpeciesRequired
    laff_points_required: LaffPointsRequired
    bounties_required: BountiesRequired
    total_bounties: TotalBounties
    hint_bounties: BountiesHinted
    tpsanity: TPSanity
    treasures_per_location: TreasuresPerLocation
    jokes_per_street: JokesPerStreet
    joke_books: JokeBookToggle
    checks_per_boss: ChecksPerBoss
    gag_training_check_behavior: GagTrainingCheckBehavior
    gag_frame_item_behavior: GagTrainingFrameBehavior
    logical_tasks_per_playground: LogicalTasksPerPlayground
    starting_task_playground: StartingTaskOption
    logical_maxed_cog_gallery: LogicalMaxedCogGallery
    maxed_cog_gallery_quota: MaxedCogGalleryQuota
    facility_locking: FacilityLocking
    fish_locations: FishLocations
    fish_checks: FishChecks
    fish_progression: FishProgression
    fish_pity: FishPity
    slot_sync_jellybeans: SyncJellybeans
    slot_sync_gag_experience: SyncGagExp
    racing_logic: RacingOption
    minigolf_logic: GolfingOption
    seed_generation_type: SeedGenerationTypeOption
    trap_percent: TrapPercentOption
    uber_trap_weight: UberWeightOption
    drip_trap_weight: DripWeightOption
    bean_tax_weight: TaxWeightOption
    gag_shuffle_weight: ShuffleWeightOption
    damage_trap_weight: DamageWeightOption
    bean_weight: BeanWeightOption
    exp_weight: GagExpWeightOption
    sos_weight: SOSWeightOption
    unite_weight: UniteWeightOption
    fire_weight: FireWeightOption
    summon_weight: SummonWeightOption
    heal_weight: HealWeightOption
    fish_weight: FishWeightOption
    death_link: DeathLinkOption
    ring_link: RingLinkOption
    pet_shop_display: PetShopRewardDisplayOption
    task_reward_display: TaskRewardDisplayOption
    random_prices: RandomShopCostToggle

toontown_option_groups: list[OptionGroup] = [
    OptionGroup("Archipelago Settings", [
        ProgressionBalancing, Accessibility, SyncJellybeans, 
        SyncGagExp, PetShopRewardDisplayOption, TaskRewardDisplayOption,
        TrapPercentOption
    ]),
    OptionGroup("Toon Settings", [
        TeamOption, MaxLaffOption, StartLaffOption, StartingTaskOption,
        StartGagOption, StartGagOptionWeb, StartGagRandomWeb, OmitGagOption,
        BaseGlobalGagXPRange, MaxGlobalGagXPRange, 
        StartDamageMultiplierRange, MaxDamageMultiplierRange, OverflowModRange, StartMoneyOption,
        StartingTaskCapacityOption, MaxTaskCapacityOption, DeathLinkOption,
        RingLinkOption, RandomShopCostToggle
    ]),
    OptionGroup("Win Condition", [
        WinConditions, WinConditionRandomizedWeb, OmitRandomWinConditions,
        WinConditionCogBossesWeb, CogBossesRequired,
        WinConditionTotalTasksWeb, TotalTasksRequired,
        WinConditionHoodTasksWeb, HoodTasksRequired,
        WinConditionTotalGagTracksWeb, GagTracksRequired,
        WinConditionFishSpeciesWeb, FishSpeciesRequired,
        WinConditionLaffOLympicsWeb, LaffPointsRequired,
        WinConditionBountyWeb, BountiesRequired, TotalBounties, BountiesHinted
        ], False),
    OptionGroup("Check/Item Behavior", [
        TPSanity, TreasuresPerLocation, ChecksPerBoss, GagTrainingCheckBehavior,
        GagTrainingFrameBehavior, LogicalTasksPerPlayground, LogicalMaxedCogGallery,
        MaxedCogGalleryQuota, FacilityLocking, FishChecks, FishLocations,
        FishProgression, FishPity, RacingOption, GolfingOption, SeedGenerationTypeOption,
        JokesPerStreet, JokeBookToggle
    ], False),
    OptionGroup("Junk Weights", [
        BeanWeightOption, GagExpWeightOption, SOSWeightOption, UniteWeightOption, SummonWeightOption, FireWeightOption, HealWeightOption, FishWeightOption
    ], True),
    OptionGroup("Trap Weights", [
        UberWeightOption, DripWeightOption, TaxWeightOption, ShuffleWeightOption, DamageWeightOption
    ], True)
]
