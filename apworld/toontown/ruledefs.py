from typing import Dict, Callable, Any, Tuple, Union

from BaseClasses import CollectionState, MultiWorld
from .consts import XP_RATIO_FOR_GAG_LEVEL, ToontownItem
from .fish import LOCATION_TO_GENUS_SPECIES, FISH_DICT, FishProgression, FishLocation, get_catchable_fish, LOCATION_TO_GENUS, FISH_ZONE_TO_LICENSE, FishZone, FISH_ZONE_TO_REGION
from .items import ToontownItemName
from .options import ToontownOptions
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


def has_collected_xp_for_gag_level(state: CollectionState, player: int, options: ToontownOptions, level: int) -> bool:
    # Determines if a given player has collected a sufficient amount of the XP items in the run.
    # always returns True if the player has 2 or less XP multis in the pool (aka, assumes they don't care)
    xp = state.count(ToontownItemName.GAG_MULTIPLIER_1.value, player) + (2 * state.count(ToontownItemName.GAG_MULTIPLIER_2.value, player))
    max_xp = options.max_global_gag_xp.value
    if max_xp <= 2:
        return True
    return XP_RATIO_FOR_GAG_LEVEL.get(level) <= (xp / max_xp)


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
@rule(Rule.TierOneCogs)
@rule(Rule.TierTwoCogs)
@rule(Rule.HasTTCHQAccess)
def AlwaysTrueRule(state: CollectionState, locentr: LocEntrDef, world: MultiWorld, player: int, options: ToontownOptions, argument: Tuple = None):
    return True


@rule(Rule.HasDDHQAccess,   ToontownItemName.DD_HQ_ACCESS)
@rule(Rule.HasDGHQAccess,   ToontownItemName.DG_HQ_ACCESS)
@rule(Rule.HasMMLHQAccess,  ToontownItemName.MML_HQ_ACCESS)
@rule(Rule.HasTBHQAccess,   ToontownItemName.TB_HQ_ACCESS)
@rule(Rule.HasDDLHQAccess,  ToontownItemName.DDL_HQ_ACCESS)
@rule(Rule.FrontFactoryKey, ToontownItemName.FRONT_FACTORY_ACCESS)
@rule(Rule.SideFactoryKey,  ToontownItemName.SIDE_FACTORY_ACCESS)
@rule(Rule.CoinMintKey,     ToontownItemName.COIN_MINT_ACCESS)
@rule(Rule.DollarMintKey,   ToontownItemName.DOLLAR_MINT_ACCESS)
@rule(Rule.BullionMintKey,  ToontownItemName.BULLION_MINT_ACCESS)
@rule(Rule.OfficeAKey,      ToontownItemName.A_OFFICE_ACCESS)
@rule(Rule.OfficeBKey,      ToontownItemName.B_OFFICE_ACCESS)
@rule(Rule.OfficeCKey,      ToontownItemName.C_OFFICE_ACCESS)
@rule(Rule.OfficeDKey,      ToontownItemName.D_OFFICE_ACCESS)
@rule(Rule.FrontOneKey,     ToontownItemName.FRONT_ONE_ACCESS)
@rule(Rule.MiddleTwoKey,    ToontownItemName.MIDDLE_TWO_ACCESS)
@rule(Rule.BackThreeKey,    ToontownItemName.BACK_THREE_ACCESS)
@rule(Rule.SellbotDisguise, ToontownItemName.SELLBOT_DISGUISE)
@rule(Rule.CashbotDisguise, ToontownItemName.CASHBOT_DISGUISE)
@rule(Rule.LawbotDisguise,  ToontownItemName.LAWBOT_DISGUISE)
@rule(Rule.BossbotDisguise, ToontownItemName.BOSSBOT_DISGUISE)
def HasItemRule(state: CollectionState, locentr: LocEntrDef, world: MultiWorld, player: int, options: ToontownOptions, argument: Tuple = None):
    if len(argument) == 2:
        return state.has(argument[0].value, player, argument[1])
    return state.has(argument[0].value, player)


@rule(Rule.FishCatch)
def FishCatch(state: CollectionState, locentr: LocEntrDef, world: MultiWorld, player: int, options: ToontownOptions, argument: Tuple = None):
    # Determine if we can catch the fish of this location/entrance definition.
    fishGenus, speciesIndex = LOCATION_TO_GENUS_SPECIES[locentr.name]
    fishDef = FISH_DICT[fishGenus][speciesIndex]
    fishLocation = FishLocation(options.fish_locations.value)
    fishProgression = FishProgression(options.fish_progression.value)

    # Get our rod tier.
    hasMaxRod = fishProgression not in (FishProgression.Rods, FishProgression.LicensesAndRods)
    rodTier = 4 if hasMaxRod else state.count(ToontownItemName.FISHING_ROD_UPGRADE.value, player)
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

    # Attempt catching the fish in feasible areas.
    for zone in fishDef.zone_list:
        # If we're fishing anywhere, ensure we can fish somewhere.
        if zone == FishZone.Anywhere and not hasAnyLicense:
            continue

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
def FishGenus(state: CollectionState, locentr: LocEntrDef, world: MultiWorld, player: int, options: ToontownOptions, argument: Tuple = None):
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
def FishGallery(state: CollectionState, locentr: LocEntrDef, world: MultiWorld, player: int, options: ToontownOptions, argument: Tuple = None):
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
def GagTraining(state: CollectionState, locentr: LocEntrDef, world: MultiWorld, player: int, options: ToontownOptions, argument: Tuple = None):
    return state.has(argument[0].value, player, argument[1]) \
            and has_collected_xp_for_gag_level(state, player, options, argument[1])


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
def ReachLocationRule(state: CollectionState, locentr: LocEntrDef, world: MultiWorld, player: int, options: ToontownOptions, argument: Tuple = None):
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
def PlaygroundCountRule(state: CollectionState, locentr: LocEntrDef, world: MultiWorld, player: int, options: ToontownOptions, argument: Tuple = None):
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


@rule(Rule.TierThreeCogs)
def TierThreeCogs(state: CollectionState, locentr: LocEntrDef, world: MultiWorld, player: int, options: ToontownOptions, argument: Tuple = None):
    return passes_rule(Rule.HasLevelTwoOffenseGag, state, locentr, world, player, options)


@rule(Rule.TierFourCogs)
@rule(Rule.TierFiveCogs)
def TierFiveCogs(state: CollectionState, locentr: LocEntrDef, world: MultiWorld, player: int, options: ToontownOptions, argument: Tuple = None):
    pgs = [
        ToontownRegionName.DD,
        ToontownRegionName.DG,
        ToontownRegionName.MML,
        ToontownRegionName.TB,
        ToontownRegionName.DDL,
    ]
    return any(state.can_reach(pg.value, None, player) for pg in pgs) \
           and passes_rule(Rule.HasLevelThreeOffenseGag, state, locentr, world, player, options)


@rule(Rule.TierSixCogs)
@rule(Rule.TierSevenCogs)
def ReachPastDD(state: CollectionState, locentr: LocEntrDef, world: MultiWorld, player: int, options: ToontownOptions, argument: Tuple = None):
    pgs = [
        ToontownRegionName.DG,
        ToontownRegionName.MML,
        ToontownRegionName.TB,
        ToontownRegionName.DDL,
    ]
    return any(state.can_reach(pg.value, None, player) for pg in pgs) \
           and passes_rule(Rule.HasLevelFourOffenseGag, state, locentr, world, player, options)


@rule(Rule.TierEightSellbot, ToontownRegionName.SBHQ)
@rule(Rule.TierEightCashbot, ToontownRegionName.CBHQ)
@rule(Rule.TierEightLawbot,  ToontownRegionName.LBHQ)
@rule(Rule.TierEightBossbot, ToontownRegionName.BBHQ)
def TierEightCogs(state: CollectionState, locentr: LocEntrDef, world: MultiWorld, player: int, options: ToontownOptions, argument: Tuple = None):
    pgs = [
        ToontownRegionName.MML,
        ToontownRegionName.TB,
        ToontownRegionName.DDL,
    ]
    if argument:
        pgs.append(argument[0])
    return any(state.can_reach(pg.value, None, player) for pg in pgs) \
           and passes_rule(Rule.HasLevelFourOffenseGag, state, locentr, world, player, options)


@rule(Rule.HasLevelOneOffenseGag,   1)
@rule(Rule.HasLevelTwoOffenseGag,   2)
@rule(Rule.HasLevelThreeOffenseGag, 3)
@rule(Rule.HasLevelFourOffenseGag,  4)
@rule(Rule.HasLevelFiveOffenseGag,  5)
@rule(Rule.HasLevelSixOffenseGag,   6)
@rule(Rule.HasLevelSevenOffenseGag, 7)
@rule(Rule.HasLevelEightOffenseGag, 8)
def HasOffensiveLevel(state: CollectionState, locentr: LocEntrDef, world: MultiWorld, player: int, options: ToontownOptions, argument: Tuple = None):
    LEVEL = argument[0]
    OVERLEVEL = min(argument[0] + 1, 7)
    UNDERLEVEL = max(0, argument[0] - 1)

    # To pass the check, we must have:
    # - A way to kill enemies (OR):
    #   - Throw or Squirt at-level and Lure at level
    #   - Drop level + 1
    #   - Trap level + 1 and Lure at level
    #   - Sound level + 1
    # - Sufficient healing (Toon-up level - 1)
    # - EXP required at level

    powerful_lure_knockback = any(
        state.has(offensive_frame.value, player, LEVEL)
        for offensive_frame in [
            ToontownItemName.THROW_FRAME,
            ToontownItemName.SQUIRT_FRAME,
        ]
    ) and state.has(ToontownItemName.LURE_FRAME.value, player, LEVEL)
    powerful_drop = state.has(ToontownItemName.DROP_FRAME.value, player, OVERLEVEL)
    powerful_trap = state.has(ToontownItemName.TRAP_FRAME.value, player, OVERLEVEL) \
                    and state.has(ToontownItemName.LURE_FRAME.value, player, LEVEL)
    powerful_sound = state.has(ToontownItemName.SOUND_FRAME.value, player, OVERLEVEL)
    sufficient_healing = state.has(ToontownItemName.TOONUP_FRAME.value, player, UNDERLEVEL)
    can_obtain_exp_required = has_collected_xp_for_gag_level(state, player, options, LEVEL)

    return (powerful_lure_knockback or powerful_sound or powerful_trap or powerful_drop) \
            and sufficient_healing and can_obtain_exp_required


@rule(Rule.CanFightVP)
def CanFightVP(state: CollectionState, locentr: LocEntrDef, world: MultiWorld, player: int, options: ToontownOptions, argument: Tuple = None):
    args = (state, locentr, world, player, options)
    return passes_rule(Rule.CanReachSBHQ, *args) and passes_rule(Rule.SellbotDisguise, *args) \
            and passes_rule(Rule.HasLevelSixOffenseGag, *args)


@rule(Rule.CanFightCFO)
def CanFightCFO(state: CollectionState, locentr: LocEntrDef, world: MultiWorld, player: int, options: ToontownOptions, argument: Tuple = None):
    args = (state, locentr, world, player, options)
    return passes_rule(Rule.CanReachCBHQ, *args) and passes_rule(Rule.CashbotDisguise, *args) \
            and passes_rule(Rule.HasLevelSixOffenseGag, *args)


@rule(Rule.CanFightCJ)
def CanFightCJ(state: CollectionState, locentr: LocEntrDef, world: MultiWorld, player: int, options: ToontownOptions, argument: Tuple = None):
    args = (state, locentr, world, player, options)
    return passes_rule(Rule.CanReachLBHQ, *args) and passes_rule(Rule.LawbotDisguise, *args) \
            and passes_rule(Rule.HasLevelSevenOffenseGag, *args)


@rule(Rule.CanFightCEO)
def CanFightCEO(state: CollectionState, locentr: LocEntrDef, world: MultiWorld, player: int, options: ToontownOptions, argument: Tuple = None):
    args = (state, locentr, world, player, options)
    return passes_rule(Rule.CanReachBBHQ, *args) and passes_rule(Rule.BossbotDisguise, *args) \
            and passes_rule(Rule.HasLevelSevenOffenseGag, *args)


@rule(Rule.AllBossesDefeated)
def AllBossesDefeated(state: CollectionState, locentr: LocEntrDef, world: MultiWorld, player: int, options: ToontownOptions, argument: Tuple = None):
    args = (state, locentr, world, player, options)
    boss_rules = [
        Rule.CanFightVP,
        Rule.CanFightCFO,
        Rule.CanFightCJ,
        Rule.CanFightCEO,
    ]
    bosses_defeated = sum(passes_rule(rule, *args) for rule in boss_rules)
    return bosses_defeated >= options.cog_bosses_required.value and passes_rule(Rule.CanReachTTC, *args)  # TECHNICALLY TRUE!


@rule(ItemRule.RestrictDisguises)
def RestrictDisguises(item: ToontownItem, locentr: LocEntrDef, world: MultiWorld, player: int, options: ToontownOptions, argument: Tuple = None):
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
                world: MultiWorld, player: int, options: ToontownOptions) -> bool:
    return rules_to_func[rule](state_or_item, locentr, world, player, options)


def test_location(location_def: ToontownLocationDefinition, state: CollectionState,
                  world: MultiWorld, player: int,
                  options: ToontownOptions) -> bool:
    if location_def.rules:
        return (any if location_def.rule_logic_or else all)(passes_rule(r, state, location_def, world, player, options) for r in location_def.rules)
    else:
        return True


def test_item_location(location_def: ToontownLocationDefinition, item: ToontownItem,
                       world: MultiWorld, player: int,
                       options: ToontownOptions) -> bool:
    if location_def.item_rules:
        return all(passes_rule(r, item, location_def, world, player, options) for r in location_def.item_rules)
    else:
        return True


def test_entrance(entrance_def: ToontownEntranceDefinition, state: CollectionState,
                  world: MultiWorld, player: int,
                  options: ToontownOptions) -> bool:
    if entrance_def.rules:
        return all(passes_rule(r, state, entrance_def, world, player, options) for r in entrance_def.rules)
    else:
        return True
