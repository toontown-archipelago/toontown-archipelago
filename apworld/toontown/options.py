from dataclasses import dataclass

from Options import PerGameCommonOptions, StartInventoryPool, Range, Choice, Toggle


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


class MaxLaffOption(Range):
    """
    The max laff you can get from items throughout the run.
    Must be above or equal to the starting_laff.
    """
    display_name = "Max Laff"
    range_start = 1
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
    default = 2


class MaxGlobalGagXPRange(Range):
    """
    Additional global gag experience that can be obtained from items.
    Stacks additively onto the base value above.
    Must be above or equal to the base_global_gag_xp.
    """
    display_name = "Max Global Gag XP"
    range_start = 0
    range_end = 30
    default = 15


class GlobalDamageMultiplierRange(Range):
    """
    The numerator of the global damage multiplier for all gags, with a denominator of 10:
    If you set this to x, the multiplier will actually be x/10.
    This applies to all players in the server.
    """
    display_name = "Global Damage Multiplier"
    range_start = 0
    range_end = 160
    default = 10


class StartMoneyOption(Range):
    """
    The starting amount of jellybeans to have when starting a new game.
    """
    display_name = "Starting Jellybeans"
    range_start = 0
    range_end = 9999
    default = 50


class CogBossesRequired(Range):
    """
    How many cog bosses must be defeated before being able to talk to Flippy to complete the game.
    """
    display_name = "Cog Bosses Required"
    range_start = 0
    range_end = 4
    default = 4


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
    default = 3


class TreasuresPerLocation(Range):
    """
    The amount of archipelago treasures that'll have items in each location
    """
    display_name = "AP Treasures Per Location"
    range_start = 0
    range_end = 6
    default = 4


class GagTrainingCheckBehavior(Choice):
    """
    Behavior of how gag experience check locations are handled.

    unlock: When unlocking a new gag, you get its respective check.
    trained: When earning all available experience for a specific gag level, you get its respective check.
    """
    option_unlock = 0
    option_trained = 1

    display_name = "Gag Training Check Behavior"


class LogicalTasksPerPlayground(Range):
    """
    Determines the amount of tasks per playground that are in logic.
    """
    display_name = "Logical Tasks Per Playground"
    range_start = 0
    range_end = 12
    default = 12


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
    range_start = 0
    range_end = 10
    default = 3


class FishLocations(Choice):
    """
    Determines where fish can spawn.
    - playgrounds: Fish spawn in their vanilla locations. Street-exclusive fish can be found anywhere in their playgrounds.
    - vanilla: Fish spawn in their vanilla locations. Street-exclusive fish remain in their vanilla locations.
    - global: Fish can spawn anywhere.
    """
    display_name = "fish_locations"
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
    display_name = "fish_checks"
    option_all_species = 0
    option_all_gallery_and_genus = 1
    option_all_gallery = 2
    option_none = 3
    default = 1


class FishProgression(Choice):
    """
    Determines the progression for fishing.
    - licenses_and_rods: Both 'licenses' and 'rods' progression are active.
    - licenses: Playground fishing is restricted until their respective Fishing License is obtained. The player starts with a Gold Rod.
    - rods: Progressive fishing rod items are added to the pool.
    - none: All fishing areas are available. The player starts with a Gold Rod.
    """
    display_name = "fish_progression"
    option_licenses_and_rods = 0
    option_licenses = 1
    option_rods = 2
    option_none = 3
    default = 0


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
    range_start = 1
    range_end = 100
    default = 20


class DeathLinkOption(Toggle):
    """
    Enable to turn on the "DeathLink" mechanic in Archipelago.
    """

    display_name = "Death Link"
    default = False


@dataclass
class ToontownOptions(PerGameCommonOptions):
    team: TeamOption
    max_laff: MaxLaffOption
    starting_laff: StartLaffOption
    base_global_gag_xp: BaseGlobalGagXPRange
    max_global_gag_xp: MaxGlobalGagXPRange
    global_damage_multiplier: GlobalDamageMultiplierRange
    starting_money: StartMoneyOption
    cog_bosses_required: CogBossesRequired
    tpsanity: TPSanity
    treasures_per_location: TreasuresPerLocation
    gag_training_check_behavior: GagTrainingCheckBehavior
    logical_tasks_per_playground: LogicalTasksPerPlayground
    logical_maxed_cog_gallery: LogicalMaxedCogGallery
    maxed_cog_gallery_quota: MaxedCogGalleryQuota
    fish_locations: FishLocations
    fish_checks: FishChecks
    fish_progression: FishProgression
    seed_generation_type: SeedGenerationTypeOption
    trap_percent: TrapPercentOption
    death_link: DeathLinkOption
