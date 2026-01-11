import math
from typing import Dict, Callable, Any, Tuple, Union

from BaseClasses import CollectionState, MultiWorld
from .consts import XP_RATIO_FOR_GAG_LEVEL, ToontownItem, CAP_RATIO_FOR_GAG_LEVEL, ToontownWinCondition
from .fish import LOCATION_TO_GENUS_SPECIES, FISH_DICT, FishProgression, FishLocation, get_catchable_fish, \
    LOCATION_TO_GENUS, FISH_ZONE_TO_LICENSE, FishZone, FISH_ZONE_TO_REGION, PlaygroundFishZoneGroups
from .items import ToontownItemName
from .options import ToontownOptions, TPSanity, FacilityLocking, GagTrainingFrameBehavior, \
    GagTrainingCheckBehavior
from .locations import ToontownLocationDefinition, ToontownLocationName, LOCATION_NAME_TO_ID, FISH_LOCATIONS, \
    get_location_def_from_name
from .regions import ToontownEntranceDefinition, ToontownRegionName
from .rules import Rule, ItemRule

LocEntrDef = Union[ToontownLocationDefinition, ToontownEntranceDefinition]
rules_to_func: Dict[Union[Rule, ItemRule], Callable] = {}


def rule(rule: Union[Rule, ItemRule], *argument: Any):
    def decorator(f):
        def wrapper(*args, **kwargs):
            kwargs['argument'] = kwargs.get('argument') or argument
            return f(*args, **kwargs)
        rules_to_func[rule] = wrapper
        return wrapper
    return decorator


def has_collected_items_for_gag_level(state: CollectionState, player: int, options, level: int) -> bool:
    if isinstance(options, ToontownOptions):
        max_xp = options.max_global_gag_xp.value
        start_xp = options.base_global_gag_xp.value
        gag_training_item = options.gag_frame_item_behavior.value
        gag_training_check = options.gag_training_check_behavior.value
    else:
        max_xp = options.get("max_gag_xp", 30)
        start_xp = options.get("start_gag_xp", 5)
        gag_training_item = options.get("gag_frame_item_behavior", 0)
        gag_training_check = options.get("gag_training_check_behavior", 0)
    # Determines if a given player has collected a sufficient amount of the XP items in the run.
    # Always returns True if the player has a difference of less than 10 mult between start and max (aka, assumes they don't care)
    xp = state.count(ToontownItemName.GAG_MULTIPLIER_1.value, player) + (2 * state.count(ToontownItemName.GAG_MULTIPLIER_2.value, player))
    sufficient_xp = XP_RATIO_FOR_GAG_LEVEL.get(level) <= (xp / max_xp) if (max_xp - start_xp) >= 10 else True
    # We aren't even training gags this seed, return true
    gags_pretrained = gag_training_item == GagTrainingFrameBehavior.option_trained
    gags_unlocked = gag_training_item == GagTrainingFrameBehavior.option_unlock
    checks_not_normal = gag_training_check != GagTrainingCheckBehavior.option_trained
    if gags_pretrained or (gags_unlocked and checks_not_normal):
        sufficient_xp = True

    # Check collected gag capacity items too.
    cap = state.count(ToontownItemName.GAG_CAPACITY_5.value, player) + (
                2 * state.count(ToontownItemName.GAG_CAPACITY_10.value, player)) + (
                      2 * state.count(ToontownItemName.GAG_CAPACITY_15.value, player))
    max_cap = 12 + (2 * 2)  # TODO - have this be dynamic to gag capacity items in pool
    sufficient_cap = CAP_RATIO_FOR_GAG_LEVEL.get(level) <= (cap / max_cap)

    # Return TRUE if we have enough xp and cap.
    return sufficient_xp and sufficient_cap


@rule(Rule.LoopyLane)          # NOTE - Streets are always enabled for now.
@rule(Rule.PunchlinePlace)     # If some kind of logic changes this (i.e. Street items getting added),
@rule(Rule.SillyStreet)        # they'll need to be moved down to a different rule group
@rule(Rule.BarnacleBoulevard)  # (AKA, probably HasItemRule)
@rule(Rule.SeaweedStreet)
@rule(Rule.LighthouseLane)
@rule(Rule.AATunnel)
@rule(Rule.ElmStreet)
@rule(Rule.MapleStreet)
@rule(Rule.OakStreet)
@rule(Rule.AltoAvenue)
@rule(Rule.BaritoneBoulevard)
@rule(Rule.TenorTerrace)
@rule(Rule.SleetStreet)
@rule(Rule.WalrusWay)
@rule(Rule.PolarPlace)
@rule(Rule.LullabyLane)
@rule(Rule.PajamaPlace)
def AlwaysTrueRule(state: CollectionState, locentr: LocEntrDef, world: MultiWorld, player: int, options, argument: Tuple = None):
    return True


@rule(Rule.SellbotDisguise, ToontownItemName.SELLBOT_DISGUISE)
@rule(Rule.CashbotDisguise, ToontownItemName.CASHBOT_DISGUISE)
@rule(Rule.LawbotDisguise,  ToontownItemName.LAWBOT_DISGUISE)
@rule(Rule.BossbotDisguise, ToontownItemName.BOSSBOT_DISGUISE)
@rule(Rule.Golfing,         ToontownItemName.GOLF_PUTTER)
@rule(Rule.Racing,          ToontownItemName.GO_KART)
def HasItemRule(state: CollectionState, locentr: LocEntrDef, world: MultiWorld, player: int, options, argument: Tuple = None):
    if len(argument) == 2:
        return state.has(argument[0].value, player, argument[1])
    return state.has(argument[0].value, player)


@rule(Rule.FrontFactoryKey, ToontownItemName.FRONT_FACTORY_ACCESS, Rule.Has40PercentMax)
@rule(Rule.SideFactoryKey,  ToontownItemName.SIDE_FACTORY_ACCESS, Rule.Has40PercentMax)
@rule(Rule.CoinMintKey,     ToontownItemName.COIN_MINT_ACCESS, Rule.Has40PercentMax)
@rule(Rule.DollarMintKey,   ToontownItemName.DOLLAR_MINT_ACCESS, Rule.Has60PercentMax)
@rule(Rule.BullionMintKey,  ToontownItemName.BULLION_MINT_ACCESS, Rule.Has60PercentMax)
@rule(Rule.OfficeAKey,      ToontownItemName.A_OFFICE_ACCESS, Rule.Has60PercentMax)
@rule(Rule.OfficeBKey,      ToontownItemName.B_OFFICE_ACCESS, Rule.Has60PercentMax)
@rule(Rule.OfficeCKey,      ToontownItemName.C_OFFICE_ACCESS, Rule.Has60PercentMax)
@rule(Rule.OfficeDKey,      ToontownItemName.D_OFFICE_ACCESS, Rule.Has80PercentMax)
@rule(Rule.FrontOneKey,     ToontownItemName.FRONT_ONE_ACCESS, Rule.Has60PercentMax)
@rule(Rule.MiddleTwoKey,    ToontownItemName.MIDDLE_TWO_ACCESS, Rule.Has60PercentMax)
@rule(Rule.BackThreeKey,    ToontownItemName.BACK_THREE_ACCESS, Rule.Has80PercentMax)
def CanEnterFacility(state: CollectionState, locentr: LocEntrDef, world: MultiWorld, player: int, options, argument: Tuple = None):
    args = (state, locentr, world, player, options)
    itemToHQAccessRule = {
        ToontownItemName.FRONT_FACTORY_ACCESS: Rule.CanReachSBHQ,
        ToontownItemName.SIDE_FACTORY_ACCESS: Rule.CanReachSBHQ,
        ToontownItemName.COIN_MINT_ACCESS: Rule.CanReachCBHQ,
        ToontownItemName.DOLLAR_MINT_ACCESS: Rule.CanReachCBHQ,
        ToontownItemName.BULLION_MINT_ACCESS: Rule.CanReachCBHQ,
        ToontownItemName.A_OFFICE_ACCESS: Rule.CanReachLBHQ,
        ToontownItemName.B_OFFICE_ACCESS: Rule.CanReachLBHQ,
        ToontownItemName.C_OFFICE_ACCESS: Rule.CanReachLBHQ,
        ToontownItemName.D_OFFICE_ACCESS: Rule.CanReachLBHQ,
        ToontownItemName.FRONT_ONE_ACCESS: Rule.CanReachBBHQ,
        ToontownItemName.MIDDLE_TWO_ACCESS: Rule.CanReachBBHQ,
        ToontownItemName.BACK_THREE_ACCESS: Rule.CanReachBBHQ,
    }
    if isinstance(options, ToontownOptions):
        locking_method = options.facility_locking.value
    else:
        locking_method = options.get("facility_locking", 0)
    # Facilities have their own keys
    if locking_method == FacilityLocking.option_keys:
        return state.has(argument[0].value, player) \
               and passes_rule(itemToHQAccessRule[argument[0]], *args) \
               and passes_rule(argument[1], *args)
    # Facilities are locked by a second access key
    elif locking_method == FacilityLocking.option_access:
        key_to_access = {
            ToontownItemName.FRONT_FACTORY_ACCESS: ToontownItemName.SBHQ_ACCESS,
            ToontownItemName.SIDE_FACTORY_ACCESS: ToontownItemName.SBHQ_ACCESS,
            ToontownItemName.COIN_MINT_ACCESS: ToontownItemName.CBHQ_ACCESS,
            ToontownItemName.DOLLAR_MINT_ACCESS: ToontownItemName.CBHQ_ACCESS,
            ToontownItemName.BULLION_MINT_ACCESS: ToontownItemName.CBHQ_ACCESS,
            ToontownItemName.A_OFFICE_ACCESS: ToontownItemName.LBHQ_ACCESS,
            ToontownItemName.B_OFFICE_ACCESS: ToontownItemName.LBHQ_ACCESS,
            ToontownItemName.C_OFFICE_ACCESS: ToontownItemName.LBHQ_ACCESS,
            ToontownItemName.D_OFFICE_ACCESS: ToontownItemName.LBHQ_ACCESS,
            ToontownItemName.FRONT_ONE_ACCESS: ToontownItemName.BBHQ_ACCESS,
            ToontownItemName.MIDDLE_TWO_ACCESS: ToontownItemName.BBHQ_ACCESS,
            ToontownItemName.BACK_THREE_ACCESS: ToontownItemName.BBHQ_ACCESS,
        }
        return state.count(key_to_access[argument[0]].value, player) >= 2 \
               and passes_rule(itemToHQAccessRule[argument[0]], *args) \
               and passes_rule(argument[1], *args)
    # Facilities must be set to unlocked, access is true as long as we can reach the HQ
    else:
        return passes_rule(itemToHQAccessRule[argument[0]], *args) \
               and passes_rule(itemToHQAccessRule[argument[0]], *args) \
               and passes_rule(argument[1], *args)


@rule(Rule.Has20PercentMax, 0.2)
@rule(Rule.Has40PercentMax, 0.4)
@rule(Rule.Has60PercentMax, 0.6)
@rule(Rule.Has80PercentMax, 0.8)
def HasEnoughLaff(state: CollectionState, locentr: LocEntrDef, world: MultiWorld, player: int, options, argument: Tuple = None):
    if isinstance(options, ToontownOptions):
        base_hp = options.starting_laff.value
        max_hp = options.max_laff.value
        goal_laff = options.laff_points_required.value
        laff_o = "laff-o-lympics" in options.win_condition
        if laff_o:
            max_hp = max(max_hp, goal_laff)
    else:
        base_hp = options.get("starting_laff", 20)
        max_hp = options.get("max_laff", 150)
        goal_laff = options.get("laff_points_required", 120)
        laff_o = options.get("win_condition", 0) & ToontownWinCondition.laff_o_lympics
        if laff_o:
            max_hp = max(max_hp, goal_laff)
    hp_diff = max_hp - base_hp
    # Our difference in base and max HP is too low, always true
    if hp_diff < 10:
        return True

    # We need this so archipelago itself can calculate our current laff
    def calcLaff():
        laff = base_hp
        laff += state.count(ToontownItemName.LAFF_BOOST_1.value, player)
        laff += (2 * state.count(ToontownItemName.LAFF_BOOST_2.value, player))
        laff += (3 * state.count(ToontownItemName.LAFF_BOOST_3.value, player))
        laff += (4 * state.count(ToontownItemName.LAFF_BOOST_4.value, player))
        laff += (5 * state.count(ToontownItemName.LAFF_BOOST_5.value, player))
        return laff

    return calcLaff() >= round(max_hp*argument[0])


@rule(Rule.HasTTCHQAccess,  ToontownItemName.TTC_ACCESS)
@rule(Rule.HasDDHQAccess,   ToontownItemName.DD_ACCESS)
@rule(Rule.HasDGHQAccess,   ToontownItemName.DG_ACCESS)
@rule(Rule.HasMMLHQAccess,  ToontownItemName.MML_ACCESS)
@rule(Rule.HasTBHQAccess,   ToontownItemName.TB_ACCESS)
@rule(Rule.HasDDLHQAccess,  ToontownItemName.DDL_ACCESS)
def HasItemCountRule(state: CollectionState, locentr: LocEntrDef, world: MultiWorld, player: int, options, argument: Tuple = None):
    return state.count(argument[0].value, player) >= 2


@rule(Rule.CanBuyTTCDoodle, 1)
@rule(Rule.CanBuyDDDoodle, 2)
@rule(Rule.CanBuyDGDoodle, 3)
@rule(Rule.CanBuyMMLDoodle, 4)
@rule(Rule.CanBuyTBDoodle, 5)
@rule(Rule.CanBuyDDLDoodle, 6)
def HasEnoughBeanCapacity(state: CollectionState, locentr: LocEntrDef, world: MultiWorld, player: int, options, argument: Tuple = None):
    if isinstance(options, ToontownOptions):
        random_price = options.random_prices.value
    else:
        random_price = options.get("random_prices", False)
    # We expect one more jar boost logically just in-case we get a high-roll on increase
    if random_price:
        return (state.count(ToontownItemName.MONEY_CAP_1000.value, player) >= (argument[0] + 1))
    else:
        return (state.count(ToontownItemName.MONEY_CAP_1000.value, player) >= argument[0])


@rule(Rule.HasTTCBook, ToontownItemName.TTC_JOKE_BOOK)
@rule(Rule.HasDDBook, ToontownItemName.DD_JOKE_BOOK)
@rule(Rule.HasDGBook, ToontownItemName.DG_JOKE_BOOK)
@rule(Rule.HasMMLBook, ToontownItemName.MML_JOKE_BOOK)
@rule(Rule.HasTBBook, ToontownItemName.TB_JOKE_BOOK)
@rule(Rule.HasDDLBook, ToontownItemName.DDL_JOKE_BOOK)
def CanLaughAtJoke(state: CollectionState, locentr: LocEntrDef, world: MultiWorld, player: int, options, argument: Tuple = None):
    if isinstance(options, ToontownOptions):
        books = options.joke_books.value
    else:
        books = options.get("joke_books", True)
    if books:
        return state.has(argument[0].value, player)
    else:
        return True


@rule(Rule.TunnelCanBeUsed)
def TunnelCanBeUsed(state: CollectionState, locentr: LocEntrDef, world: MultiWorld, player: int, options, argument: Tuple = None):
    if isinstance(options, ToontownOptions):
        option = options.tpsanity.value
    else:
        option = options.get("tpsanity", 0)
    if option == TPSanity.option_keys:
        return passes_rule(Rule.HasTeleportAccess, state, locentr, world, player, options)
    return True


@rule(Rule.HasTeleportAccess)
def HasTeleportAccess(state: CollectionState, locentr: LocEntrDef, world: MultiWorld, player: int, options, argument: Tuple = None):
    region_to_tp_item = {
        ToontownRegionName.TTC: ToontownItemName.TTC_ACCESS,
        ToontownRegionName.DD: ToontownItemName.DD_ACCESS,
        ToontownRegionName.DG: ToontownItemName.DG_ACCESS,
        ToontownRegionName.MML: ToontownItemName.MML_ACCESS,
        ToontownRegionName.TB: ToontownItemName.TB_ACCESS,
        ToontownRegionName.DDL: ToontownItemName.DDL_ACCESS,
        ToontownRegionName.GS: ToontownItemName.GS_ACCESS,
        ToontownRegionName.AA: ToontownItemName.AA_ACCESS,
        ToontownRegionName.SBHQ: ToontownItemName.SBHQ_ACCESS,
        ToontownRegionName.CBHQ: ToontownItemName.CBHQ_ACCESS,
        ToontownRegionName.LBHQ: ToontownItemName.LBHQ_ACCESS,
        ToontownRegionName.BBHQ: ToontownItemName.BBHQ_ACCESS,
    }
    return state.has(region_to_tp_item[locentr.connects_to].value, player)


@rule(Rule.FishCatch)
def FishCatch(state: CollectionState, locentr: LocEntrDef, world: MultiWorld, player: int, options, argument: Tuple = None):
    if isinstance(options, ToontownOptions):
        fishLocation = FishLocation(options.fish_locations.value)
        fishProgression = FishProgression(options.fish_progression.value)
    else:
        fishLocation = FishLocation(options.get("fish_locations", 0))
        fishProgression = FishProgression(options.get("fish_progression", 2))

    # Determine if we can catch the fish of this location/entrance definition.
    fishGenus, speciesIndex = LOCATION_TO_GENUS_SPECIES[locentr.name]
    fishDef = FISH_DICT[fishGenus][speciesIndex]

    # Get our rod tier.
    hasMaxRod = fishProgression not in (FishProgression.Rods, FishProgression.LicensesAndRods)
    rodTier = 4 if hasMaxRod else min(state.count(ToontownItemName.FISHING_ROD_UPGRADE.value, player), 4)
    needsLicense = fishProgression in (FishProgression.Licenses, FishProgression.LicensesAndRods)
    hasAnyLicense = True

    # Check if we have any license.
    if needsLicense:
        hasAnyLicense = any(
            state.has(license.value, player)
            for license in [
                ToontownItemName.TTC_FISHING,
                ToontownItemName.DD_FISHING,
                ToontownItemName.DG_FISHING,
                ToontownItemName.MML_FISHING,
                ToontownItemName.TB_FISHING,
                ToontownItemName.DDL_FISHING,
            ]
        )

    # Figure out the zones we must scan.
    feasible_areas = set(fz for fz in fishDef.zone_list if fz != FishZone.Anywhere)
    if FishZone.Anywhere in fishDef.zone_list:
        for fz in PlaygroundFishZoneGroups.keys():
            feasible_areas.add(fz)

    # Attempt catching the fish in feasible areas.
    for zone in feasible_areas:
        # Estate fishing is disabled.
        if zone == FishZone.MyEstate:
            continue

        # If we don't have our license, skip this zone.
        if needsLicense:
            license = FISH_ZONE_TO_LICENSE.get(zone)
            if license:
                if not state.has(license.value, player):
                    continue

        # Ensure we can visit this region.
        region = FISH_ZONE_TO_REGION.get(zone)
        if region:
            if not state.can_reach(region.value, None, player):
                continue

        # Check the fish in this area.
        for _genus, _species, _rarity in get_catchable_fish(zone, rodTier, fishLocation):
            if _genus == fishGenus and _species == speciesIndex:
                return True

    # We cannot catch this fish anywhere.
    return False


@rule(Rule.FishGenus)
def FishGenus(state: CollectionState, locentr: LocEntrDef, world: MultiWorld, player: int, options, argument: Tuple = None):
    # See if we can reach the location for any valid genus.
    checkGenus = LOCATION_TO_GENUS[locentr.name]
    for locationName, fishData in LOCATION_TO_GENUS_SPECIES.items():
        if fishData[0] == checkGenus:
            fishLocationDef = get_location_def_from_name(locationName)
            if passes_rule(Rule.FishCatch, state, fishLocationDef, world, player, options):
                # We can catch a fish of this genus.
                return True

    # Could not catch this genus anywhere.
    return False


@rule(Rule.FishGallery)
def FishGallery(state: CollectionState, locentr: LocEntrDef, world: MultiWorld, player: int, options, argument: Tuple = None):
    # How many fish do we need?
    fishRequired = {
        ToontownLocationName.FISHING_10_SPECIES: 10,
        ToontownLocationName.FISHING_20_SPECIES: 20,
        ToontownLocationName.FISHING_30_SPECIES: 30,
        ToontownLocationName.FISHING_40_SPECIES: 40,
        ToontownLocationName.FISHING_50_SPECIES: 50,
        ToontownLocationName.FISHING_60_SPECIES: 60,
        ToontownLocationName.FISHING_COMPLETE_ALBUM: 70,
    }[locentr.name]

    # Count our fish!
    fishCount = sum(
        int(passes_rule(Rule.FishCatch, state, get_location_def_from_name(locationName), world, player, options))
        for locationName in FISH_LOCATIONS
    )

    # Check if we have enough.
    return fishCount >= fishRequired


@rule(Rule.ToonUpOne,       ToontownItemName.TOONUP_FRAME, 1)
@rule(Rule.ToonUpTwo,       ToontownItemName.TOONUP_FRAME, 2)
@rule(Rule.ToonUpThree,     ToontownItemName.TOONUP_FRAME, 3)
@rule(Rule.ToonUpFour,      ToontownItemName.TOONUP_FRAME, 4)
@rule(Rule.ToonUpFive,      ToontownItemName.TOONUP_FRAME, 5)
@rule(Rule.ToonUpSix,       ToontownItemName.TOONUP_FRAME, 6)
@rule(Rule.ToonUpSeven,     ToontownItemName.TOONUP_FRAME, 7)
@rule(Rule.TrapOne,         ToontownItemName.TRAP_FRAME, 1)
@rule(Rule.TrapTwo,         ToontownItemName.TRAP_FRAME, 2)
@rule(Rule.TrapThree,       ToontownItemName.TRAP_FRAME, 3)
@rule(Rule.TrapFour,        ToontownItemName.TRAP_FRAME, 4)
@rule(Rule.TrapFive,        ToontownItemName.TRAP_FRAME, 5)
@rule(Rule.TrapSix,         ToontownItemName.TRAP_FRAME, 6)
@rule(Rule.TrapSeven,       ToontownItemName.TRAP_FRAME, 7)
@rule(Rule.LureOne,         ToontownItemName.LURE_FRAME, 1)
@rule(Rule.LureTwo,         ToontownItemName.LURE_FRAME, 2)
@rule(Rule.LureThree,       ToontownItemName.LURE_FRAME, 3)
@rule(Rule.LureFour,        ToontownItemName.LURE_FRAME, 4)
@rule(Rule.LureFive,        ToontownItemName.LURE_FRAME, 5)
@rule(Rule.LureSix,         ToontownItemName.LURE_FRAME, 6)
@rule(Rule.LureSeven,       ToontownItemName.LURE_FRAME, 7)
@rule(Rule.SoundOne,        ToontownItemName.SOUND_FRAME, 1)
@rule(Rule.SoundTwo,        ToontownItemName.SOUND_FRAME, 2)
@rule(Rule.SoundThree,      ToontownItemName.SOUND_FRAME, 3)
@rule(Rule.SoundFour,       ToontownItemName.SOUND_FRAME, 4)
@rule(Rule.SoundFive,       ToontownItemName.SOUND_FRAME, 5)
@rule(Rule.SoundSix,        ToontownItemName.SOUND_FRAME, 6)
@rule(Rule.SoundSeven,      ToontownItemName.SOUND_FRAME, 7)
@rule(Rule.ThrowOne,        ToontownItemName.THROW_FRAME, 1)
@rule(Rule.ThrowTwo,        ToontownItemName.THROW_FRAME, 2)
@rule(Rule.ThrowThree,      ToontownItemName.THROW_FRAME, 3)
@rule(Rule.ThrowFour,       ToontownItemName.THROW_FRAME, 4)
@rule(Rule.ThrowFive,       ToontownItemName.THROW_FRAME, 5)
@rule(Rule.ThrowSix,        ToontownItemName.THROW_FRAME, 6)
@rule(Rule.ThrowSeven,      ToontownItemName.THROW_FRAME, 7)
@rule(Rule.SquirtOne,       ToontownItemName.SQUIRT_FRAME, 1)
@rule(Rule.SquirtTwo,       ToontownItemName.SQUIRT_FRAME, 2)
@rule(Rule.SquirtThree,     ToontownItemName.SQUIRT_FRAME, 3)
@rule(Rule.SquirtFour,      ToontownItemName.SQUIRT_FRAME, 4)
@rule(Rule.SquirtFive,      ToontownItemName.SQUIRT_FRAME, 5)
@rule(Rule.SquirtSix,       ToontownItemName.SQUIRT_FRAME, 6)
@rule(Rule.SquirtSeven,     ToontownItemName.SQUIRT_FRAME, 7)
@rule(Rule.DropOne,         ToontownItemName.DROP_FRAME, 1)
@rule(Rule.DropTwo,         ToontownItemName.DROP_FRAME, 2)
@rule(Rule.DropThree,       ToontownItemName.DROP_FRAME, 3)
@rule(Rule.DropFour,        ToontownItemName.DROP_FRAME, 4)
@rule(Rule.DropFive,        ToontownItemName.DROP_FRAME, 5)
@rule(Rule.DropSix,         ToontownItemName.DROP_FRAME, 6)
@rule(Rule.DropSeven,       ToontownItemName.DROP_FRAME, 7)
def GagTraining(state: CollectionState, locentr: LocEntrDef, world: MultiWorld, player: int, options, argument: Tuple = None):
    # We need lure to be able to train trap :3
    if argument[0] == ToontownItemName.TRAP_FRAME:
        return state.has(argument[0].value, player, argument[1]) \
               and has_collected_items_for_gag_level(state, player, options, argument[1]) \
               and state.has(ToontownItemName.LURE_FRAME.value, player)
    # We need a way to trigger an unlure for exp :3
    if argument[0] == ToontownItemName.LURE_FRAME:
        return state.has(argument[0].value, player, argument[1]) \
               and has_collected_items_for_gag_level(state, player, options, argument[1]) \
               and (state.has(ToontownItemName.TRAP_FRAME.value, player) or state.has(ToontownItemName.SQUIRT_FRAME.value, player) or state.has(ToontownItemName.THROW_FRAME.value, player) or state.has(ToontownItemName.SOUND_FRAME.value, player))
    return state.has(argument[0].value, player, argument[1]) \
           and has_collected_items_for_gag_level(state, player, options, argument[1])


@rule(Rule.CanReachTTC,  ToontownRegionName.TTC)
@rule(Rule.CanReachDD,   ToontownRegionName.DD)
@rule(Rule.CanReachDG,   ToontownRegionName.DG)
@rule(Rule.CanReachMML,  ToontownRegionName.MML)
@rule(Rule.CanReachTB,   ToontownRegionName.TB)
@rule(Rule.CanReachDDL,  ToontownRegionName.DDL)
@rule(Rule.CanReachAA,   ToontownRegionName.AA)
@rule(Rule.CanReachGS,   ToontownRegionName.GS)
@rule(Rule.CanReachSBHQ, ToontownRegionName.SBHQ)
@rule(Rule.CanReachCBHQ, ToontownRegionName.CBHQ)
@rule(Rule.CanReachLBHQ, ToontownRegionName.LBHQ)
@rule(Rule.CanReachBBHQ, ToontownRegionName.BBHQ)
def ReachLocationRule(state: CollectionState, locentr: LocEntrDef, world: MultiWorld, player: int, options, argument: Tuple = None):
    if type(argument[0]) is ToontownLocationName:
        return state.can_reach(argument[0].value, "Location", player)
    elif type(argument[0]) is ToontownRegionName:
        return state.can_reach(argument[0].value, None, player)
    else:
        raise NotImplementedError("ReachLocationRule does not know how to interpret %s" % repr(argument[0]))


@rule(Rule.OnePlaygroundAccessible,    1)
@rule(Rule.TwoPlaygroundsAccessible,   2)
@rule(Rule.ThreePlaygroundsAccessible, 3)
@rule(Rule.FourPlaygroundsAccessible,  4)
@rule(Rule.FivePlaygroundsAccessible,  5)
@rule(Rule.SixPlaygroundsAccessible,   6)
def PlaygroundCountRule(state: CollectionState, locentr: LocEntrDef, world: MultiWorld, player: int, options, argument: Tuple = None):
    pgs = [
        ToontownRegionName.TTC,
        ToontownRegionName.DD,
        ToontownRegionName.DG,
        ToontownRegionName.MML,
        ToontownRegionName.TB,
        ToontownRegionName.DDL,
        ToontownRegionName.AA,
    ]
    return sum(int(state.can_reach(pg.value, None, player)) for pg in pgs) >= argument[0]

@rule(Rule.TierOneCogs)
@rule(Rule.TierTwoCogs)
def TierOneCogs(state: CollectionState, locentr: LocEntrDef, world: MultiWorld, player: int, options, argument: Tuple = None):
    return passes_rule(Rule.HasLevelOneOffenseGag, state, locentr, world, player, options)

@rule(Rule.TierThreeCogs, 3, None)
@rule(Rule.TierFourCogs, 4, None)
@rule(Rule.TierFourSellbot, 4, ToontownRegionName.SBHQ)
@rule(Rule.TierFourCashbot, 4, ToontownRegionName.CBHQ)
@rule(Rule.TierFourLawbot,  4, None)
@rule(Rule.TierFourBossbot, 4, None)
@rule(Rule.TierFiveCogs, 5, None)
@rule(Rule.TierFiveSellbot, 5, ToontownRegionName.SBHQ)
@rule(Rule.TierFiveCashbot, 5, ToontownRegionName.CBHQ)
@rule(Rule.TierFiveLawbot,  5, ToontownRegionName.LBHQ)
@rule(Rule.TierFiveBossbot, 5, ToontownRegionName.BBHQ)
@rule(Rule.TierSixCogs, 6, None)
@rule(Rule.TierSixSellbot, 6, ToontownRegionName.SBHQ)
@rule(Rule.TierSixCashbot, 6, ToontownRegionName.CBHQ)
@rule(Rule.TierSixLawbot,  6, ToontownRegionName.LBHQ)
@rule(Rule.TierSixBossbot, 6, ToontownRegionName.BBHQ)
@rule(Rule.TierEightSellbot, 8, ToontownRegionName.SBHQ)
@rule(Rule.TierEightCashbot, 8, ToontownRegionName.CBHQ)
@rule(Rule.TierEightLawbot,  8, ToontownRegionName.LBHQ)
@rule(Rule.TierEightBossbot, 8, ToontownRegionName.BBHQ)
def CanReachCogTier(state: CollectionState, locentr: LocEntrDef, world: MultiWorld, player: int, options, argument: Tuple = None):
    tier_to_info = {
        3: {
            "pgs": [
                ToontownRegionName.DD,
                ToontownRegionName.DG,
                ToontownRegionName.MML,
                ToontownRegionName.TB
            ],
            "gag_rule": Rule.HasLevelTwoOffenseGag
        },
        4: {
            "pgs": [
                ToontownRegionName.DD,
                ToontownRegionName.DG,
                ToontownRegionName.MML,
                ToontownRegionName.TB,
                ToontownRegionName.DDL,
            ],
            "gag_rule": Rule.HasLevelThreeOffenseGag
        },
        5: {
            "pgs": [
                ToontownRegionName.DG,
                ToontownRegionName.MML,
                ToontownRegionName.TB,
                ToontownRegionName.DDL,
            ],
            "gag_rule": Rule.HasLevelThreeOffenseGag
        },
        6: {
            "pgs": [
                ToontownRegionName.MML,
                ToontownRegionName.TB,
                ToontownRegionName.DDL,
            ],
            "gag_rule": Rule.HasLevelFourOffenseGag
        },
        8: {
            "pgs": [  # We rely on tier 7s and 8s to be found in HQs only, added separately
            ],
            "gag_rule": Rule.HasLevelFourOffenseGag
        },
    }
    tier = argument[0]
    tier_info = tier_to_info[tier]
    pgs = tier_info["pgs"]
    gag_rule = tier_info["gag_rule"]
    # Add the respective cog HQ to logical areas to locate tier
    if argument[1] is not None:
        pgs.append(argument[1])
    if tier == 8:  # Tier is 7/8, need to check laff too
        return any(state.can_reach(pg.value, None, player) for pg in pgs) \
               and passes_rule(gag_rule, state, locentr, world, player, options) \
               and passes_rule(Rule.Has20PercentMax, state, locentr, world, player, options)
    return any(state.can_reach(pg.value, None, player) for pg in pgs) \
           and passes_rule(gag_rule, state, locentr, world, player, options)

@rule(Rule.LevelOneCogs, 1)
@rule(Rule.LevelTwoCogs, 2)
@rule(Rule.LevelThreeCogs, 3)
@rule(Rule.LevelFourCogs, 4)
@rule(Rule.LevelFiveCogs, 5)
@rule(Rule.LevelSixCogs, 6)
@rule(Rule.LevelSevenCogs, 7)
@rule(Rule.LevelEightCogs, 8)
@rule(Rule.LevelNineCogs, 9)
@rule(Rule.LevelTenCogs, 10)
@rule(Rule.LevelElevenCogs, 11)
@rule(Rule.LevelTwelveCogs, 12)
@rule(Rule.LevelThirteenCogs, 13)
@rule(Rule.LevelFourteenCogs, 14)
def CanReachHighCogTier(state: CollectionState, locentr: LocEntrDef, world: MultiWorld, player: int, options, argument: Tuple = None):
    args = (state, locentr, world, player, options)

    CanTier1 = passes_rule(Rule.TierOneCogs, *args)
    CanTier2 = passes_rule(Rule.TierTwoCogs, *args)
    CanTier3 = passes_rule(Rule.TierThreeCogs, *args)
    CanTier4 = passes_rule(Rule.TierFourCogs, *args)
    CanTier5 = passes_rule(Rule.TierFiveCogs, *args)
    CanTier6 = passes_rule(Rule.TierSixCogs, *args)
    CanTier8Boss = passes_rule(Rule.TierEightBossbot, *args)
    CanTier8Law =  passes_rule(Rule.TierEightLawbot,  *args)
    CanTier8Cash = passes_rule(Rule.TierEightCashbot, *args)
    CanTier8Sell = passes_rule(Rule.TierEightSellbot, *args)
    CanDDL = state.can_reach(ToontownRegionName.DDL.value, None, player)
    CanCBHQ = state.can_reach(ToontownRegionName.CBHQ.value, None, player)
    CanLBHQ = state.can_reach(ToontownRegionName.LBHQ.value, None, player)
    CanBBHQ = state.can_reach(ToontownRegionName.BBHQ.value, None, player)
    CanBullion = passes_rule(Rule.BullionMintKey, *args) \
                 and passes_rule(Rule.HasLevelSixOffenseGag, *args) \
                 and passes_rule(Rule.Has60PercentMax, *args)
    CanDOffice = passes_rule(Rule.OfficeDKey, *args) \
                 and passes_rule(Rule.HasLevelSevenOffenseGag, *args) \
                 and passes_rule(Rule.Has60PercentMax, *args)
    CanBackThree = passes_rule(Rule.BackThreeKey, *args) \
                   and passes_rule(Rule.HasLevelSevenOffenseGag, *args) \
                   and passes_rule(Rule.Has60PercentMax, *args)
    CanFiveStory = passes_rule(Rule.FiveStory, *args)
    CanCFO = passes_rule(Rule.CanFightCFO, *args)
    CanCJ = passes_rule(Rule.CanFightCJ, *args)
    CanCEO = passes_rule(Rule.CanFightCEO, *args)

    tier_to_info = {
        1: {
            "gags": None,
            "laff": None,
            "rules": [
                CanTier1,
            ]
        },
        2: {
            "gags": None,
            "laff": None,
            "rules": [
                CanTier2,
            ]
        },
        3: {
            "gags": None,
            "laff": None,
            "rules": [
                CanTier3,
            ]
        },
        4: {
            "gags": None,
            "laff": None,
            "rules": [
                CanTier4,
            ]
        },
        5: {
            "gags": None,
            "laff": None,
            "rules": [
                CanTier5,
            ]
        },
        6: {
            "gags": None,
            "laff": None,
            "rules": [
                CanTier6,
            ]
        },
        7: {
            "gags": Rule.HasLevelFourOffenseGag,
            "laff": Rule.Has20PercentMax,
            "rules": [
                CanTier8Boss,
                CanTier8Law,
                CanTier8Cash,
                CanTier8Sell,
            ]
        },
        8: {
            "gags": Rule.HasLevelFourOffenseGag,
            "laff": Rule.Has20PercentMax,
            "rules": [
                CanTier8Boss,
                CanTier8Law,
                CanTier8Cash,
                CanTier8Sell,
            ]
        },
        9: {
            "gags": Rule.HasLevelFiveOffenseGag,
            "laff": Rule.Has20PercentMax,
            "rules": [
                CanDDL,
                CanFiveStory,
                CanCBHQ,
                CanLBHQ,
                CanBBHQ,
            ]
        },
        10: {
            "gags": Rule.HasLevelFiveOffenseGag,
            "laff": Rule.Has40PercentMax,
            "rules": [
                CanFiveStory,
                CanBullion,
                CanCFO,
                CanLBHQ,
                CanBBHQ,
            ]
        },
        11: {
            "gags": Rule.HasLevelFiveOffenseGag,
            "laff": Rule.Has60PercentMax,
            "rules": [
                CanCJ,
                CanBBHQ,
            ]
        },
        12: {
            "gags": None,
            "laff": None,
            "rules": [
                CanDOffice,
                CanCJ,
                CanBackThree,
                CanCEO,
            ]
        },
        13: {
            "gags": None,
            "laff": None,
            "rules": [
                CanCEO,
            ]
        },
        14: {
            "gags": None,
            "laff": None,
            "rules": [
                CanCEO,
            ]
        },
    }

    tier = argument[0]
    tier_info = tier_to_info[tier]
    if tier_info["gags"] is not None:
        gag_rule = passes_rule(tier_info["gags"], *args)
    else:
        gag_rule = True
    if tier_info["laff"] is not None:
        laff_rule = passes_rule(tier_info["laff"], *args)
    else:
        laff_rule = True
    if len(tier_info["rules"]) >= 1:
        gen_rule = any(rule for rule in tier_info["rules"])
    else:
        gen_rule = True

    return gag_rule and laff_rule and gen_rule


@rule(Rule.CanMaxTierOneSellbot, 1, ToontownRegionName.SBHQ)
@rule(Rule.CanMaxTierOneCashbot, 1, ToontownRegionName.CBHQ)
@rule(Rule.CanMaxTierOneLawbot,  1, ToontownRegionName.LBHQ)
@rule(Rule.CanMaxTierOneBossbot, 1, ToontownRegionName.BBHQ)
@rule(Rule.CanMaxTierTwoSellbot, 2, ToontownRegionName.SBHQ)
@rule(Rule.CanMaxTierTwoCashbot, 2, ToontownRegionName.CBHQ)
@rule(Rule.CanMaxTierTwoLawbot,  2, ToontownRegionName.LBHQ)
@rule(Rule.CanMaxTierTwoBossbot, 2, ToontownRegionName.BBHQ)
@rule(Rule.CanMaxTierThreeSellbot, 3, ToontownRegionName.SBHQ)
@rule(Rule.CanMaxTierThreeCashbot, 3, ToontownRegionName.CBHQ)
@rule(Rule.CanMaxTierThreeLawbot,  3, ToontownRegionName.LBHQ)
@rule(Rule.CanMaxTierThreeBossbot, 3, ToontownRegionName.BBHQ)
@rule(Rule.CanMaxTierFourSellbot, 4, ToontownRegionName.SBHQ)
@rule(Rule.CanMaxTierFourCashbot, 4, ToontownRegionName.CBHQ)
@rule(Rule.CanMaxTierFourLawbot,  4, ToontownRegionName.LBHQ)
@rule(Rule.CanMaxTierFourBossbot, 4, ToontownRegionName.BBHQ)
@rule(Rule.CanMaxTierFiveSellbot, 5, ToontownRegionName.SBHQ)
@rule(Rule.CanMaxTierFiveCashbot, 5, ToontownRegionName.CBHQ)
@rule(Rule.CanMaxTierFiveLawbot,  5, ToontownRegionName.LBHQ)
@rule(Rule.CanMaxTierFiveBossbot, 5, ToontownRegionName.BBHQ)
@rule(Rule.CanMaxTierSixSellbot, 6, ToontownRegionName.SBHQ)
@rule(Rule.CanMaxTierSixCashbot, 6, ToontownRegionName.CBHQ)
@rule(Rule.CanMaxTierSixLawbot,  6, ToontownRegionName.LBHQ)
@rule(Rule.CanMaxTierSixBossbot, 6, ToontownRegionName.BBHQ)
@rule(Rule.CanMaxTierEightSellbot, 8, ToontownRegionName.SBHQ)
@rule(Rule.CanMaxTierEightCashbot, 8, ToontownRegionName.CBHQ)
@rule(Rule.CanMaxTierEightLawbot,  8, ToontownRegionName.LBHQ)
@rule(Rule.CanMaxTierEightBossbot, 8, ToontownRegionName.BBHQ)
def CanMaxCogTier(state: CollectionState, locentr: LocEntrDef, world: MultiWorld, player: int, options, argument: Tuple = None):
    if isinstance(options, ToontownOptions):
        max_gallery = options.maxed_cog_gallery_quota.value
    else:
        max_gallery = options.get("maxed_cog_gallery_quota", 3)

    # Our gallery is only one, we don't need special max gallery logic
    if max_gallery == 1:
        return True

    CanFrontFactory = passes_rule(Rule.FrontFactoryKey, state, locentr, world, player, options) \
                      and passes_rule(Rule.HasLevelFourOffenseGag, state, locentr, world, player, options) \
                      and passes_rule(Rule.Has40PercentMax, state, locentr, world, player, options)
    CanSideFactory = passes_rule(Rule.SideFactoryKey, state, locentr, world, player, options) \
                     and passes_rule(Rule.HasLevelFiveOffenseGag, state, locentr, world, player, options) \
                     and passes_rule(Rule.Has40PercentMax, state, locentr, world, player, options)
    CanCoin = passes_rule(Rule.CoinMintKey, state, locentr, world, player, options) \
              and passes_rule(Rule.HasLevelFourOffenseGag, state, locentr, world, player, options) \
              and passes_rule(Rule.Has40PercentMax, state, locentr, world, player, options)
    CanDollar = passes_rule(Rule.DollarMintKey, state, locentr, world, player, options) \
                and passes_rule(Rule.HasLevelFiveOffenseGag, state, locentr, world, player, options) \
                and passes_rule(Rule.Has40PercentMax, state, locentr, world, player, options)
    CanBullion = passes_rule(Rule.BullionMintKey, state, locentr, world, player, options) \
                 and passes_rule(Rule.HasLevelSixOffenseGag, state, locentr, world, player, options) \
                 and passes_rule(Rule.Has60PercentMax, state, locentr, world, player, options)
    CanAOffice = passes_rule(Rule.OfficeAKey, state, locentr, world, player, options) \
                 and passes_rule(Rule.HasLevelFourOffenseGag, state, locentr, world, player, options) \
                 and passes_rule(Rule.Has40PercentMax, state, locentr, world, player, options)
    CanBOffice = passes_rule(Rule.OfficeBKey, state, locentr, world, player, options) \
                 and passes_rule(Rule.HasLevelFiveOffenseGag, state, locentr, world, player, options) \
                 and passes_rule(Rule.Has40PercentMax, state, locentr, world, player, options)
    CanCOffice = passes_rule(Rule.OfficeCKey, state, locentr, world, player, options) \
                 and passes_rule(Rule.HasLevelSixOffenseGag, state, locentr, world, player, options) \
                 and passes_rule(Rule.Has60PercentMax, state, locentr, world, player, options)
    CanDOffice = passes_rule(Rule.OfficeDKey, state, locentr, world, player, options) \
                 and passes_rule(Rule.HasLevelSevenOffenseGag, state, locentr, world, player, options) \
                 and passes_rule(Rule.Has60PercentMax, state, locentr, world, player, options)
    CanFrontOne = passes_rule(Rule.FrontOneKey, state, locentr, world, player, options) \
                  and passes_rule(Rule.HasLevelFiveOffenseGag, state, locentr, world, player, options) \
                  and passes_rule(Rule.Has40PercentMax, state, locentr, world, player, options)
    CanMiddleTwo = passes_rule(Rule.MiddleTwoKey, state, locentr, world, player, options) \
                   and passes_rule(Rule.HasLevelSixOffenseGag, state, locentr, world, player, options) \
                   and passes_rule(Rule.Has60PercentMax, state, locentr, world, player, options)
    CanBackThree = passes_rule(Rule.BackThreeKey, state, locentr, world, player, options) \
                   and passes_rule(Rule.HasLevelSevenOffenseGag, state, locentr, world, player, options) \
                   and passes_rule(Rule.Has60PercentMax, state, locentr, world, player, options)
    CanOneStory = passes_rule(Rule.OneStory, state, locentr, world, player, options)
    CanTwoStory = passes_rule(Rule.TwoStory, state, locentr, world, player, options)
    CanThreeStory = passes_rule(Rule.ThreeStory, state, locentr, world, player, options)
    CanFourStory = passes_rule(Rule.FourStory, state, locentr, world, player, options)
    CanFiveStory = passes_rule(Rule.FiveStory, state, locentr, world, player, options)
    CanVP = passes_rule(Rule.CanFightVP, state, locentr, world, player, options)
    CanCFO = passes_rule(Rule.CanFightCFO, state, locentr, world, player, options)
    CanCJ = passes_rule(Rule.CanFightCJ, state, locentr, world, player, options)
    CanCEO = passes_rule(Rule.CanFightCEO, state, locentr, world, player, options)

    tier_to_info = {
        1: {
            "generic-rules": [
                CanOneStory,
                CanTwoStory,
                CanThreeStory
            ],
            ToontownRegionName.SBHQ: [
                CanFrontFactory,
                CanSideFactory,
                CanVP
            ],
            ToontownRegionName.CBHQ: [
                CanCoin,
                CanDollar,
            ],
            ToontownRegionName.LBHQ: [
                CanAOffice,
                CanBOffice,
            ],
            ToontownRegionName.BBHQ: [
            ],
        },
        2: {
            "generic-rules": [
                CanOneStory,
                CanTwoStory,
                CanThreeStory
            ],
            ToontownRegionName.SBHQ: [
                CanFrontFactory,
                CanSideFactory,
                CanVP
            ],
            ToontownRegionName.CBHQ: [
                CanCoin,
                CanDollar,
                CanBullion,
            ],
            ToontownRegionName.LBHQ: [
                CanAOffice,
                CanBOffice,
                CanCOffice
            ],
            ToontownRegionName.BBHQ: [
                CanFrontOne
            ],
        },
        3: {
            "generic-rules": [
                CanTwoStory,
                CanThreeStory,
                CanFourStory
            ],
            ToontownRegionName.SBHQ: [
                CanFrontFactory,
                CanSideFactory,
                CanVP
            ],
            ToontownRegionName.CBHQ: [
                CanCoin,
                CanDollar,
                CanBullion,
                CanCFO
            ],
            ToontownRegionName.LBHQ: [
                CanAOffice,
                CanBOffice,
                CanCOffice
            ],
            ToontownRegionName.BBHQ: [
                CanFrontOne
            ],
        },
        4: {
            "generic-rules": [
                CanThreeStory,
                CanFourStory,
                CanFiveStory
            ],
            ToontownRegionName.SBHQ: [
                CanSideFactory,
                CanVP
            ],
            ToontownRegionName.CBHQ: [
                CanDollar,
                CanBullion,
                CanCFO
            ],
            ToontownRegionName.LBHQ: [
                CanBOffice,
                CanCOffice,
                CanDOffice,
                CanCJ
            ],
            ToontownRegionName.BBHQ: [
                CanFrontOne,
                CanMiddleTwo
            ],
        },
        5: {
            "generic-rules": [
                CanThreeStory,
                CanFourStory,
                CanFiveStory
            ],
            ToontownRegionName.SBHQ: [
                CanVP
            ],
            ToontownRegionName.CBHQ: [
                CanBullion,
                CanCFO
            ],
            ToontownRegionName.LBHQ: [
                CanCOffice,
                CanDOffice,
                CanCJ
            ],
            ToontownRegionName.BBHQ: [
                CanFrontOne,
                CanMiddleTwo,
                CanBackThree,
                CanCEO
            ],
        },
        6: {
            "generic-rules": [
                CanFourStory,
                CanFiveStory
            ],
            ToontownRegionName.SBHQ: [
                CanVP
            ],
            ToontownRegionName.CBHQ: [
                CanBullion,
                CanCFO
            ],
            ToontownRegionName.LBHQ: [
                CanCOffice,
                CanDOffice,
                CanCJ
            ],
            ToontownRegionName.BBHQ: [
                CanMiddleTwo,
                CanBackThree,
                CanCEO
            ],
        },
        8: {
            "generic-rules": [
                CanFiveStory
            ],
            ToontownRegionName.SBHQ: [  # No good tier 7/8 sources in HQ, outside of factory areas
            ],
            ToontownRegionName.CBHQ: [
                CanBullion,
                CanCFO
            ],
            ToontownRegionName.LBHQ: [
                CanDOffice,
                CanCJ
            ],
            ToontownRegionName.BBHQ: [
                CanBackThree,
                CanCEO
            ],
        },
    }
    tier = argument[0]
    tier_info = tier_to_info[tier]
    rules = tier_info["generic-rules"]
    # Add area/dept specific rules
    if argument[1]:
        rules.extend(tier_info[argument[1]])
    return any(rules)

@rule(Rule.CanAnyFacility)
def CanDoAnyFacility(state: CollectionState, locentr: LocEntrDef, world: MultiWorld, player: int, options, argument: Tuple = None):
    CanFrontFactory = passes_rule(Rule.FrontFactoryKey, state, locentr, world, player, options) \
                      and passes_rule(Rule.HasLevelFourOffenseGag, state, locentr, world, player, options) \
                      and passes_rule(Rule.Has40PercentMax, state, locentr, world, player, options)
    CanSideFactory = passes_rule(Rule.SideFactoryKey, state, locentr, world, player, options) \
                     and passes_rule(Rule.HasLevelFiveOffenseGag, state, locentr, world, player, options) \
                     and passes_rule(Rule.Has40PercentMax, state, locentr, world, player, options)
    CanCoin = passes_rule(Rule.CoinMintKey, state, locentr, world, player, options) \
              and passes_rule(Rule.HasLevelFourOffenseGag, state, locentr, world, player, options) \
              and passes_rule(Rule.Has40PercentMax, state, locentr, world, player, options)
    CanDollar = passes_rule(Rule.DollarMintKey, state, locentr, world, player, options) \
                and passes_rule(Rule.HasLevelFiveOffenseGag, state, locentr, world, player, options) \
                and passes_rule(Rule.Has40PercentMax, state, locentr, world, player, options)
    CanBullion = passes_rule(Rule.BullionMintKey, state, locentr, world, player, options) \
                 and passes_rule(Rule.HasLevelSixOffenseGag, state, locentr, world, player, options) \
                 and passes_rule(Rule.Has60PercentMax, state, locentr, world, player, options)
    CanAOffice = passes_rule(Rule.OfficeAKey, state, locentr, world, player, options) \
                 and passes_rule(Rule.HasLevelFourOffenseGag, state, locentr, world, player, options) \
                 and passes_rule(Rule.Has40PercentMax, state, locentr, world, player, options)
    CanBOffice = passes_rule(Rule.OfficeBKey, state, locentr, world, player, options) \
                 and passes_rule(Rule.HasLevelFiveOffenseGag, state, locentr, world, player, options) \
                 and passes_rule(Rule.Has40PercentMax, state, locentr, world, player, options)
    CanCOffice = passes_rule(Rule.OfficeCKey, state, locentr, world, player, options) \
                 and passes_rule(Rule.HasLevelSixOffenseGag, state, locentr, world, player, options) \
                 and passes_rule(Rule.Has60PercentMax, state, locentr, world, player, options)
    CanDOffice = passes_rule(Rule.OfficeDKey, state, locentr, world, player, options) \
                 and passes_rule(Rule.HasLevelSevenOffenseGag, state, locentr, world, player, options) \
                 and passes_rule(Rule.Has60PercentMax, state, locentr, world, player, options)
    CanFrontOne = passes_rule(Rule.FrontOneKey, state, locentr, world, player, options) \
                  and passes_rule(Rule.HasLevelFiveOffenseGag, state, locentr, world, player, options) \
                  and passes_rule(Rule.Has40PercentMax, state, locentr, world, player, options)
    CanMiddleTwo = passes_rule(Rule.MiddleTwoKey, state, locentr, world, player, options) \
                   and passes_rule(Rule.HasLevelSixOffenseGag, state, locentr, world, player, options) \
                   and passes_rule(Rule.Has60PercentMax, state, locentr, world, player, options)
    CanBackThree = passes_rule(Rule.BackThreeKey, state, locentr, world, player, options) \
                   and passes_rule(Rule.HasLevelSevenOffenseGag, state, locentr, world, player, options) \
                   and passes_rule(Rule.Has60PercentMax, state, locentr, world, player, options)
    facilities = [CanFrontFactory, CanSideFactory,
                  CanCoin, CanDollar, CanBullion,
                  CanAOffice, CanBOffice, CanCOffice, CanDOffice,
                  CanFrontOne, CanMiddleTwo, CanBackThree]
    return any(facilities)

@rule(Rule.OneStory, 1)
@rule(Rule.TwoStory, 2)
@rule(Rule.ThreeStory, 3)
@rule(Rule.FourStory, 4)
@rule(Rule.FiveStory, 5)
def CanReachBldg(state: CollectionState, locentr: LocEntrDef, world: MultiWorld, player: int, options, argument: Tuple = None):
    args = (state, locentr, world, player, options)
    if argument[0] == 1:
        pgs = [
            ToontownRegionName.TTC,
            ToontownRegionName.DD,
        ]
        laff_rule = Rule.Has20PercentMax
    elif argument[0] == 2:
        pgs = [
            ToontownRegionName.TTC,
            ToontownRegionName.DD,
            ToontownRegionName.DG,
        ]
        laff_rule = Rule.Has20PercentMax
    elif argument[0] == 3:
        pgs = [
            ToontownRegionName.DD,
            ToontownRegionName.DG,
            ToontownRegionName.MML,
            ToontownRegionName.TB,
            ToontownRegionName.DDL
        ]
        laff_rule = Rule.Has40PercentMax
    elif argument[0] == 4:
        pgs = [
            ToontownRegionName.DG,
            ToontownRegionName.MML,
            ToontownRegionName.TB,
            ToontownRegionName.DDL,
        ]
        laff_rule = Rule.Has60PercentMax
    elif argument[0] == 5:
        pgs = [
            ToontownRegionName.MML,
            ToontownRegionName.TB,
            ToontownRegionName.DDL,
        ]
        laff_rule = Rule.Has60PercentMax
    return any(state.can_reach(pg.value, None, player) for pg in pgs) and passes_rule(laff_rule, *args)


@rule(Rule.HasLevelOneOffenseGag,   1)
def hasDamageGag(state: CollectionState, locentr: LocEntrDef, world: MultiWorld, player: int, options, argument: Tuple = None):
    OFFENSIVE: List[ToontownItemName] = [
            ToontownItemName.SOUND_FRAME,
            ToontownItemName.THROW_FRAME,
            ToontownItemName.SQUIRT_FRAME,
            ToontownItemName.DROP_FRAME
            ]
    if state.has(ToontownItemName.TRAP_FRAME.value, player) and state.has(ToontownItemName.LURE_FRAME.value, player):
        return True
    return any(state.has(gag.value, player) for gag in OFFENSIVE)


@rule(Rule.HasLevelTwoOffenseGag,   2)
@rule(Rule.HasLevelThreeOffenseGag, 3)
@rule(Rule.HasLevelFourOffenseGag,  4)
@rule(Rule.HasLevelFiveOffenseGag,  5)
@rule(Rule.HasLevelSixOffenseGag,   6)
@rule(Rule.HasLevelSevenOffenseGag, 7)
@rule(Rule.HasLevelEightOffenseGag, 7)
def HasOffensiveLevel(state: CollectionState, locentr: LocEntrDef, world: MultiWorld, player: int, options, argument: Tuple = None):
    if isinstance(options, ToontownOptions):
        start_dmg = options.start_damage_multiplier.value
        max_dmg = options.max_damage_multiplier.value
    else:
        start_dmg = options.get("start_damage_multiplier", 100)
        max_dmg = options.get("max_damage_multiplier", 100)
    LEVEL = argument[0]
    OVERLEVEL = min(argument[0] + 1, 8)
    UNDERLEVEL = max(0, argument[0] - 1)
    LUREMIN = max(0, argument[0] - 2)


    # The ratio of Gag Capacity items required to reach a given gag level.
    DMG_RATIOS_FOR_GAG_TRACKS = {
        ToontownItemName.TOONUP_FRAME.value: {
            1: 0.25,
            2: 0.30,
            3: 0.35,
            4: 0.45,
            5: 0.60,
            6: 0.75,
            7: 0.90,
            8: 0.90
        },
        ToontownItemName.TRAP_FRAME.value: {
            1: 0.25,
            2: 0.30,
            3: 0.35,
            4: 0.45,
            5: 0.55,
            6: 0.70,
            7: 0.80,
            8: 0.90
        },
        ToontownItemName.SOUND_FRAME.value: {
            1: 0.30,
            2: 0.40,
            3: 0.50,
            4: 0.60,
            5: 0.70,
            6: 0.80,
            7: 0.90,
            8: 0.90
        },
        ToontownItemName.THROW_FRAME.value: {
            1: 0.25,
            2: 0.30,
            3: 0.35,
            4: 0.45,
            5: 0.60,
            6: 0.75,
            7: 0.90,
            8: 0.90
        },
        ToontownItemName.SQUIRT_FRAME.value: {
            1: 0.25,
            2: 0.35,
            3: 0.45,
            4: 0.55,
            5: 0.65,
            6: 0.75,
            7: 0.90,
            8: 0.90
        },
        ToontownItemName.DROP_FRAME.value: {
            1: 0.25,
            2: 0.30,
            3: 0.35,
            4: 0.45,
            5: 0.55,
            6: 0.70,
            7: 0.80,
            8: 0.90
        },
    }

    # To pass the check, we must have:
    # - Two of the following methods of damage
    # - + Sufficient healing (Toon-up @ level - 1)
    # - + Sufficient Lure (Lure @ level - 2)
    # - + EXP + Capacity required at level

    def calc_wanted_damage_for_track(track, level):
        base_dmg_ratio = start_dmg / max_dmg
        # Our difference in base and max dmg mult is too low, always true
        if base_dmg_ratio >= 0.9:
            return True
        wanted_ratio = DMG_RATIOS_FOR_GAG_TRACKS[track][level]
        dmg = start_dmg
        dmg += state.count(ToontownItemName.DMG_BOOST_1.value, player)
        dmg += (2 * state.count(ToontownItemName.DMG_BOOST_2.value, player))
        dmg += (3 * state.count(ToontownItemName.DMG_BOOST_3.value, player))
        dmg += (4 * state.count(ToontownItemName.DMG_BOOST_4.value, player))
        final_ratio = dmg / max_dmg
        # Second case here is for the case of gags are just always going to be powerful enough anyways and we don't need to restrict logic
        return (final_ratio >= wanted_ratio) or (dmg >= 120)

    minimum_lure = state.has(ToontownItemName.LURE_FRAME.value, player, LUREMIN)
    powerful_squirt_knockback = state.has(ToontownItemName.SQUIRT_FRAME.value, player, LEVEL) \
                                and state.has(ToontownItemName.LURE_FRAME.value, player, LEVEL) \
                                and calc_wanted_damage_for_track(ToontownItemName.SQUIRT_FRAME.value, LEVEL)
    powerful_throw_knockback = state.has(ToontownItemName.THROW_FRAME.value, player, LEVEL) \
                               and state.has(ToontownItemName.LURE_FRAME.value, player, LEVEL) \
                               and calc_wanted_damage_for_track(ToontownItemName.THROW_FRAME.value, LEVEL)
    powerful_drop = state.has(ToontownItemName.DROP_FRAME.value, player, LEVEL) and calc_wanted_damage_for_track(ToontownItemName.DROP_FRAME.value, LEVEL)
    powerful_trap = state.has(ToontownItemName.TRAP_FRAME.value, player, LEVEL) \
                    and state.has(ToontownItemName.LURE_FRAME.value, player, UNDERLEVEL) \
                    and calc_wanted_damage_for_track(ToontownItemName.TRAP_FRAME.value, LEVEL)
    powerful_sound = state.has(ToontownItemName.SOUND_FRAME.value, player, OVERLEVEL) and calc_wanted_damage_for_track(ToontownItemName.SOUND_FRAME.value, OVERLEVEL)

    def two_powerful_tracks():
        powerful_tracks = 0
        for track in (powerful_drop, powerful_trap, powerful_sound, powerful_throw_knockback, powerful_squirt_knockback):
            if track:
                powerful_tracks += 1
        return powerful_tracks >= 2

    sufficient_healing = state.has(ToontownItemName.TOONUP_FRAME.value, player, UNDERLEVEL) and calc_wanted_damage_for_track(ToontownItemName.TOONUP_FRAME.value, UNDERLEVEL)
    can_obtain_exp_required = has_collected_items_for_gag_level(state, player, options, LEVEL)
    return two_powerful_tracks() and sufficient_healing and minimum_lure and can_obtain_exp_required


@rule(Rule.CanFightVP,  Rule.CanReachSBHQ, Rule.SellbotDisguise, Rule.HasLevelFiveOffenseGag,  Rule.Has40PercentMax)
@rule(Rule.CanFightCFO, Rule.CanReachCBHQ, Rule.CashbotDisguise, Rule.HasLevelSixOffenseGag,   Rule.Has60PercentMax)
@rule(Rule.CanFightCJ,  Rule.CanReachLBHQ, Rule.LawbotDisguise,  Rule.HasLevelSevenOffenseGag, Rule.Has60PercentMax)
@rule(Rule.CanFightCEO, Rule.CanReachBBHQ, Rule.BossbotDisguise, Rule.HasLevelEightOffenseGag, Rule.Has80PercentMax)
def CanFightBoss(state: CollectionState, locentr: LocEntrDef, world: MultiWorld, player: int, options, argument: Tuple = None):
    if isinstance(options, ToontownOptions):
        cpb = options.checks_per_boss.value
        bosses_on = "cog-bosses" in options.win_condition
    else:
        cpb = options.get("checks_per_boss", 4)
        bosses_on = options.get("win_condition", 0) & ToontownWinCondition.cog_bosses
    # Not normally necessary, but other rules that reference this one shouldn't consider bosses when checks are off
    # AND we're not wanting bosses for goal
    if cpb == 0 and not bosses_on:
        return False
    args = (state, locentr, world, player, options)
    return passes_rule(argument[0], *args) and passes_rule(argument[1], *args) \
           and passes_rule(argument[2], *args) and passes_rule(argument[3], *args)


@rule(Rule.AllBossesDefeated)
def AllBossesDefeated(state: CollectionState, locentr: LocEntrDef, world: MultiWorld, player: int, options, argument: Tuple = None):
    args = (state, locentr, world, player, options)
    boss_rules = [
        Rule.CanFightVP,
        Rule.CanFightCFO,
        Rule.CanFightCJ,
        Rule.CanFightCEO,
    ]
    bosses_defeated = sum(passes_rule(rule, *args) for rule in boss_rules)
    return bosses_defeated >= options.cog_bosses_required.value and passes_rule(Rule.CanReachTTC, *args)  # TECHNICALLY TRUE!


@rule(Rule.AllFishCaught)
def AllFishCaught(state: CollectionState, locentr: LocEntrDef, world: MultiWorld, player: int, options, argument: Tuple = None):
    args = (state, locentr, world, player, options)
    # Count our fish!
    fishCount = sum(
        int(passes_rule(Rule.FishCatch, state, get_location_def_from_name(locationName), world, player, options))
        for locationName in FISH_LOCATIONS
    )

    # Check if we have enough to win.
    return fishCount >= options.fish_species_required.value and passes_rule(Rule.CanReachTTC, *args)  # TECHNICALLY TRUE!


@rule(Rule.TaskedAllHoods)
def TaskedAllHoods(state: CollectionState, locentr: LocEntrDef, world: MultiWorld, player: int, options, argument: Tuple = None):
    if isinstance(options, ToontownOptions):
        total_tasks = "total-tasks" in options.win_condition
        hood_tasks = "hood-tasks" in options.win_condition
        tasks_required = options.total_tasks_required.value
    else:
        total_tasks = options.get("win_condition", 0) & ToontownWinCondition.total_tasks
        hood_tasks = options.get("win_condition", 0) & ToontownWinCondition.hood_tasks
        tasks_required = options.get("total_tasks_required", 48)
    args = (state, locentr, world, player, options)
    hq_access_to_gag_rule = {
        Rule.HasTTCHQAccess: Rule.HasLevelOneOffenseGag,
        Rule.HasDDHQAccess: Rule.HasLevelTwoOffenseGag,
        Rule.HasDGHQAccess: Rule.HasLevelThreeOffenseGag,
        Rule.HasMMLHQAccess: Rule.HasLevelFourOffenseGag,
        Rule.HasTBHQAccess: Rule.HasLevelFiveOffenseGag,
        Rule.HasDDLHQAccess: Rule.HasLevelSixOffenseGag
    }

    def CountAndGagRule():  # We're doing it this way so that we can grab the gag logic we want based on the highest task pg needed
        rule_list = list(hq_access_to_gag_rule.keys())
        access_count = 0
        gag_rule = Rule.HasLevelOneOffenseGag
        for rule in rule_list:
            if passes_rule(rule, *args):
                access_count += 1
                gag_rule = hq_access_to_gag_rule[rule]
        return access_count, gag_rule

    access_count, gag_rule = CountAndGagRule()

    if hood_tasks:  # Complete enough tasks in each hood
        hoods_required = len(list(hq_access_to_gag_rule.keys()))  # We need all of them to win!
    elif total_tasks:  # Complete enough total tasks
        hoods_required = math.ceil(tasks_required / 12)  # How many HQs we need minimum to win!
    # Check if we have enough to win.
    return access_count >= hoods_required and passes_rule(Rule.CanReachTTC, *args) and passes_rule(gag_rule, *args)  # TECHNICALLY TRUE!


@rule(Rule.GainedEnoughLaff)
def GainedEnoughLaff(state: CollectionState, locentr: LocEntrDef, world: MultiWorld, player: int, options, argument: Tuple = None):
    if isinstance(options, ToontownOptions):
        starting_laff = options.starting_laff.value
        goal_laff = options.laff_points_required.value
    else:
        starting_laff = options.get("starting_laff", 20)
        goal_laff = options.get("laff_points_required", 120)
    args = (state, locentr, world, player, options)
    laff_needed = max(0, (goal_laff - starting_laff))

    # Check if we have enough to win.
    return state.count(ToontownItemName.LAFF_BOOST_1.value, player) >= laff_needed and passes_rule(Rule.CanReachTTC, *args)  # TECHNICALLY TRUE!


@rule(Rule.MaxedAllGags)
def MaxedAllGags(state: CollectionState, locentr: LocEntrDef, world: MultiWorld, player: int, options, argument: Tuple = None):
    if isinstance(options, ToontownOptions):
        required_gags = options.gag_tracks_required.value
    else:
        required_gags = options.get("gag_tracks_required", 5)
    args = (state, locentr, world, player, options)
    gag_items = [
        ToontownItemName.TOONUP_FRAME.value,
        ToontownItemName.TRAP_FRAME.value,
        ToontownItemName.LURE_FRAME.value,
        ToontownItemName.SOUND_FRAME.value,
        ToontownItemName.THROW_FRAME.value,
        ToontownItemName.SQUIRT_FRAME.value,
        ToontownItemName.DROP_FRAME.value
    ]

    def HasLevelSeven(gag):
        return state.count(gag, player) >= 7

    maxed_gags = sum(HasLevelSeven(gag) for gag in gag_items)
    return maxed_gags >= required_gags and passes_rule(Rule.CanReachTTC, *args)  # TECHNICALLY TRUE!

@rule(Rule.CanReachBounties)
def CanReachBounties(state: CollectionState, locentr: LocEntrDef, world: MultiWorld, player: int, options, argument: Tuple = None):
    if isinstance(options, ToontownOptions):
        bounties_required = options.bounties_required.value
    else:
        bounties_required = options.get('bounties_required', 10)
    args = (state, locentr, world, player, options)

    return state.count(ToontownItemName.BOUNTY.value, player) >= bounties_required and passes_rule(Rule.CanReachTTC, *args)  # TECHNICALLY TRUE!


@rule(Rule.CanWinGame)
def CanWinGame(state: CollectionState, locentr: LocEntrDef, world: MultiWorld, player: int, options, argument: Tuple = None):
    if isinstance(options, ToontownOptions):
        win_condition = ToontownWinCondition.from_options(options)
    else:
        win_condition = ToontownWinCondition(options.get("win_condition", 0))
    args = (state, locentr, world, player, options)
    win_conditions = {
        ToontownWinCondition.cog_bosses: Rule.AllBossesDefeated,  # Cog Boss Goal
        ToontownWinCondition.total_tasks: Rule.TaskedAllHoods,  # Total Tasks Goal
        ToontownWinCondition.hood_tasks: Rule.TaskedAllHoods,  # Hood Tasks Goal
        ToontownWinCondition.gag_tracks: Rule.MaxedAllGags,  # Max Gags Goal
        ToontownWinCondition.fish_species: Rule.AllFishCaught,  # Fish Species Goal
        ToontownWinCondition.laff_o_lympics: Rule.GainedEnoughLaff,  # Laff-O-Lympics Goal
        ToontownWinCondition.bounty: Rule.CanReachBounties,  # Bounty Goal
    }
    # Return our goal rule, default to None if invalid
    return all(passes_rule(win_conditions.get(f), *args) for f in win_condition)


@rule(ItemRule.RestrictDisguises)
def RestrictDisguises(item: ToontownItem, locentr: LocEntrDef, world: MultiWorld, player: int, options, argument: Tuple = None):
    DISGUISE_ITEM_IDS = list(map(
        lambda name: LOCATION_NAME_TO_ID.get(name),
        [
            ToontownItemName.SELLBOT_DISGUISE.value,
            ToontownItemName.CASHBOT_DISGUISE.value,
            ToontownItemName.LAWBOT_DISGUISE.value,
            ToontownItemName.BOSSBOT_DISGUISE.value,
        ]
    ))
    return item.code not in DISGUISE_ITEM_IDS


"""
Meta location testing
"""


def passes_rule(rule: Rule, state_or_item: Union[CollectionState, ToontownItem], locentr: LocEntrDef,
                world: MultiWorld, player: int, options) -> bool:
    return rules_to_func[rule](state_or_item, locentr, world, player, options)


def test_location(location_def: ToontownLocationDefinition, state: CollectionState,
                  world: MultiWorld, player: int,
                  options) -> bool:
    if location_def.rules:
        return (any if location_def.rule_logic_or else all)(passes_rule(r, state, location_def, world, player, options) for r in location_def.rules)
    else:
        return True


def test_item_location(location_def: ToontownLocationDefinition, item: ToontownItem,
                       world: MultiWorld, player: int,
                       options) -> bool:
    if location_def.item_rules:
        return all(passes_rule(r, item, location_def, world, player, options) for r in location_def.item_rules)
    else:
        return True


def test_entrance(entrance_def: ToontownEntranceDefinition, state: CollectionState,
                  world: MultiWorld, player: int,
                  options) -> bool:
    if entrance_def.rules:
        return all(passes_rule(r, state, entrance_def, world, player, options) for r in entrance_def.rules)
    else:
        return True
