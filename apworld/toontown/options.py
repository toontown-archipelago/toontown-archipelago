from dataclasses import dataclass

from Options import PerGameCommonOptions, StartInventoryPool, Range, Choice, Toggle


class StartHPOption(Range):
    """
    The starting amount of max Laff Points (HP) to have when starting a new game.
    """
    display_name = "Starting Laff"
    range_start = 1
    range_end = 80
    default = 20


class MaxHPOption(Range):
    """
    The max HP you can get from items throughout the run.
    """
    display_name = "Max Laff"
    range_start = 1
    range_end = 137
    default = 137


class StartMoneyOption(Range):
    """
    The starting amount of jellybeans to have when starting a new game.
    """
    display_name = "Starting Jellybeans"
    range_start = 0
    range_end = 9999
    default = 50


class BaseGagXPMultiplierOption(Range):
    """
    The starting base gag experience multiplier when starting a new game.
    This multiplier will multiplicatively stack with other gag experience bonuses throughout the game
    """
    display_name = "Starting Base Gag XP Multiplier"
    range_start = 1
    range_end = 10
    default = 2


class MaxGagXPMultiplierFromItems(Range):
    """
    The max gag multiplier that can be obtained from items.
    """
    display_name = "Max Gag XP Multiplier From Items"
    range_start = 0
    range_end = 30
    default = 15


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


class ForcePlaygroundVisitTeleportAccessUnlocksOption(Toggle):
    """
    Enable to force your playground teleport access to be on its corresponding "Visit Location" check
    """
    display_name = "Force Visit Playground Teleport Access Unlocks"
    default = True


class ForceCogHQVisitTeleportAccessUnlocksOption(Toggle):
    """
    Enable to force your Cog HQ teleport access to be on its corresponding "Visit Location" check
    """
    display_name = "Force Visit Cog HQ Teleport Access Unlocks"


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
    default = 10


@dataclass
class ToontownOptions(PerGameCommonOptions):
    max_hp: MaxHPOption
    starting_hp: StartHPOption
    starting_money: StartMoneyOption
    starting_base_gag_xp_multiplier: BaseGagXPMultiplierOption
    max_gag_xp_multiplier_from_items: MaxGagXPMultiplierFromItems
    logical_tasks_per_playground: LogicalTasksPerPlayground
    logical_maxed_cog_gallery: LogicalMaxedCogGallery
    force_playground_visit_teleport_access_unlocks: ForcePlaygroundVisitTeleportAccessUnlocksOption
    force_coghq_visit_teleport_access_unlocks: ForceCogHQVisitTeleportAccessUnlocksOption
    seed_generation_type: SeedGenerationTypeOption
    trap_percent: TrapPercentOption
