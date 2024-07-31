from dataclasses import dataclass, field
from typing import List
from enum import Enum
from .rules import Rule


class ToontownRegionName(Enum):
    MENU = "Menu"

    # Non-physical regions. Accessible from anywhere in the game
    LOGIN    = "Login"
    GALLERY  = "Cog Gallery"
    FISHING  = "Fishing"
    TRAINING = "Gag Training"
    BUILDINGS = "Cog Buildings"

    # Playgrounds
    TTC  = "Toontown Central"
    DD   = "Donald's Dock"
    DG   = "Daisy Gardens"
    MML  = "Minnie's Melodyland"
    TB   = "The Brrrgh"
    DDL  = "Donald's Dreamland"
    GS   = "Goofy Speedway"
    AA   = "Acorn Acres"
    SBHQ = "Sellbot HQ"
    CBHQ = "Cashbot HQ"
    LBHQ = "Lawbot HQ"
    BBHQ = "Bossbot HQ"


@dataclass
class ToontownEntranceDefinition:
    connects_to: ToontownRegionName
    rules: List[Rule] = field(default_factory=list)


@dataclass
class ToontownRegionDefinition:
    name: ToontownRegionName
    connects_to: List[ToontownEntranceDefinition] = field(default_factory=list)


REGION_DEFINITIONS = (
    ToontownRegionDefinition(
        ToontownRegionName.MENU,
        [ToontownEntranceDefinition(ToontownRegionName.LOGIN)]
    ),
    ToontownRegionDefinition(
        ToontownRegionName.LOGIN,
        [
            ToontownEntranceDefinition(ToontownRegionName.TTC),
            ToontownEntranceDefinition(ToontownRegionName.DD,   [Rule.HasTeleportAccess]),
            ToontownEntranceDefinition(ToontownRegionName.DG,   [Rule.HasTeleportAccess]),
            ToontownEntranceDefinition(ToontownRegionName.MML,  [Rule.HasTeleportAccess]),
            ToontownEntranceDefinition(ToontownRegionName.TB,   [Rule.HasTeleportAccess]),
            ToontownEntranceDefinition(ToontownRegionName.DDL,  [Rule.HasTeleportAccess]),
            ToontownEntranceDefinition(ToontownRegionName.GS,   [Rule.HasTeleportAccess]),
            ToontownEntranceDefinition(ToontownRegionName.AA,   [Rule.HasTeleportAccess]),
            ToontownEntranceDefinition(ToontownRegionName.SBHQ, [Rule.HasTeleportAccess]),
            ToontownEntranceDefinition(ToontownRegionName.CBHQ, [Rule.HasTeleportAccess]),
            ToontownEntranceDefinition(ToontownRegionName.LBHQ, [Rule.HasTeleportAccess]),
            ToontownEntranceDefinition(ToontownRegionName.BBHQ, [Rule.HasTeleportAccess]),
            ToontownEntranceDefinition(ToontownRegionName.GALLERY),
            ToontownEntranceDefinition(ToontownRegionName.FISHING),
            ToontownEntranceDefinition(ToontownRegionName.TRAINING),
            ToontownEntranceDefinition(ToontownRegionName.BUILDINGS),
        ]
    ),
    ToontownRegionDefinition(ToontownRegionName.GALLERY),
    ToontownRegionDefinition(ToontownRegionName.FISHING),
    ToontownRegionDefinition(ToontownRegionName.TRAINING),
    ToontownRegionDefinition(ToontownRegionName.BUILDINGS),
    ToontownRegionDefinition(
        ToontownRegionName.TTC,
        [
            ToontownEntranceDefinition(ToontownRegionName.MML, [Rule.LoopyLane, Rule.TunnelCanBeUsed]),
            ToontownEntranceDefinition(ToontownRegionName.DD, [Rule.PunchlinePlace, Rule.TunnelCanBeUsed]),
            ToontownEntranceDefinition(ToontownRegionName.DG, [Rule.SillyStreet, Rule.TunnelCanBeUsed]),
            ToontownEntranceDefinition(ToontownRegionName.GS, [Rule.TunnelCanBeUsed]),
        ]
    ),
    ToontownRegionDefinition(
        ToontownRegionName.DD,
        [
            ToontownEntranceDefinition(ToontownRegionName.TTC, [Rule.BarnacleBoulevard, Rule.TunnelCanBeUsed]),
            ToontownEntranceDefinition(ToontownRegionName.DG, [Rule.SeaweedStreet, Rule.TunnelCanBeUsed]),
            ToontownEntranceDefinition(ToontownRegionName.TB, [Rule.LighthouseLane, Rule.TunnelCanBeUsed]),
            ToontownEntranceDefinition(ToontownRegionName.AA, [Rule.AATunnel, Rule.TunnelCanBeUsed]),
        ]
    ),
    ToontownRegionDefinition(
        ToontownRegionName.DG,
        [
            ToontownEntranceDefinition(ToontownRegionName.TTC,  [Rule.ElmStreet, Rule.TunnelCanBeUsed]),
            ToontownEntranceDefinition(ToontownRegionName.DD,   [Rule.MapleStreet, Rule.TunnelCanBeUsed]),
            ToontownEntranceDefinition(ToontownRegionName.SBHQ, [Rule.OakStreet, Rule.TunnelCanBeUsed]),
        ]
    ),
    ToontownRegionDefinition(
        ToontownRegionName.MML,
        [
            ToontownEntranceDefinition(ToontownRegionName.TTC, [Rule.AltoAvenue, Rule.TunnelCanBeUsed]),
            ToontownEntranceDefinition(ToontownRegionName.TB,  [Rule.BaritoneBoulevard, Rule.TunnelCanBeUsed]),
            ToontownEntranceDefinition(ToontownRegionName.DDL, [Rule.TenorTerrace, Rule.TunnelCanBeUsed]),
        ]
    ),
    ToontownRegionDefinition(
        ToontownRegionName.TB,
        [
            ToontownEntranceDefinition(ToontownRegionName.MML,  [Rule.SleetStreet, Rule.TunnelCanBeUsed]),
            ToontownEntranceDefinition(ToontownRegionName.DD,   [Rule.WalrusWay, Rule.TunnelCanBeUsed]),
            ToontownEntranceDefinition(ToontownRegionName.LBHQ, [Rule.PolarPlace, Rule.TunnelCanBeUsed]),
        ]
    ),
    ToontownRegionDefinition(
        ToontownRegionName.DDL,
        [
            ToontownEntranceDefinition(ToontownRegionName.MML, [Rule.LullabyLane, Rule.TunnelCanBeUsed]),
            ToontownEntranceDefinition(ToontownRegionName.CBHQ, [Rule.PajamaPlace, Rule.TunnelCanBeUsed]),
        ]
    ),
    ToontownRegionDefinition(ToontownRegionName.GS),
    ToontownRegionDefinition(
        ToontownRegionName.AA,
        [
            ToontownEntranceDefinition(ToontownRegionName.BBHQ, [Rule.TunnelCanBeUsed]),
        ]
    ),
    ToontownRegionDefinition(ToontownRegionName.SBHQ),
    ToontownRegionDefinition(ToontownRegionName.CBHQ),
    ToontownRegionDefinition(ToontownRegionName.LBHQ),
    ToontownRegionDefinition(ToontownRegionName.BBHQ),
)
