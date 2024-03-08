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
            ToontownEntranceDefinition(ToontownRegionName.GALLERY),
            ToontownEntranceDefinition(ToontownRegionName.FISHING),
            ToontownEntranceDefinition(ToontownRegionName.TRAINING),
        ]
    ),
    ToontownRegionDefinition(ToontownRegionName.GALLERY),
    ToontownRegionDefinition(ToontownRegionName.FISHING),
    ToontownRegionDefinition(ToontownRegionName.TRAINING),
    ToontownRegionDefinition(
        ToontownRegionName.TTC,
        [
            ToontownEntranceDefinition(ToontownRegionName.MML, [Rule.LoopyLane]),
            ToontownEntranceDefinition(ToontownRegionName.DD, [Rule.PunchlinePlace]),
            ToontownEntranceDefinition(ToontownRegionName.DG, [Rule.SillyStreet]),
            ToontownEntranceDefinition(ToontownRegionName.GS),
        ]
    ),
    ToontownRegionDefinition(
        ToontownRegionName.DD,
        [
            ToontownEntranceDefinition(ToontownRegionName.TTC, [Rule.BarnacleBoulevard]),
            ToontownEntranceDefinition(ToontownRegionName.DG, [Rule.SeaweedStreet]),
            ToontownEntranceDefinition(ToontownRegionName.TB, [Rule.LighthouseLane]),
            ToontownEntranceDefinition(ToontownRegionName.AA, [Rule.AATunnel]),
        ]
    ),
    ToontownRegionDefinition(
        ToontownRegionName.DG,
        [
            ToontownEntranceDefinition(ToontownRegionName.TTC, [Rule.ElmStreet]),
            ToontownEntranceDefinition(ToontownRegionName.DD, [Rule.MapleStreet]),
            ToontownEntranceDefinition(ToontownRegionName.SBHQ, [Rule.OakStreet]),
        ]
    ),
    ToontownRegionDefinition(
        ToontownRegionName.MML,
        [
            ToontownEntranceDefinition(ToontownRegionName.TTC, [Rule.AltoAvenue]),
            ToontownEntranceDefinition(ToontownRegionName.TB, [Rule.BaritoneBoulevard]),
            ToontownEntranceDefinition(ToontownRegionName.DDL, [Rule.TenorTerrace]),
        ]
    ),
    ToontownRegionDefinition(
        ToontownRegionName.TB,
        [
            ToontownEntranceDefinition(ToontownRegionName.MML, [Rule.SleetStreet]),
            ToontownEntranceDefinition(ToontownRegionName.DD, [Rule.WalrusWay]),
            ToontownEntranceDefinition(ToontownRegionName.LBHQ, [Rule.PolarPlace]),
        ]
    ),
    ToontownRegionDefinition(
        ToontownRegionName.DDL,
        [
            ToontownEntranceDefinition(ToontownRegionName.MML, [Rule.LullabyLane]),
            ToontownEntranceDefinition(ToontownRegionName.CBHQ, [Rule.PajamaPlace]),
        ]
    ),
    ToontownRegionDefinition(ToontownRegionName.GS),
    ToontownRegionDefinition(
        ToontownRegionName.AA,
        [
            ToontownEntranceDefinition(ToontownRegionName.BBHQ),
        ]
    ),
    ToontownRegionDefinition(ToontownRegionName.SBHQ),
    ToontownRegionDefinition(ToontownRegionName.CBHQ),
    ToontownRegionDefinition(ToontownRegionName.LBHQ),
    ToontownRegionDefinition(ToontownRegionName.BBHQ),
)
