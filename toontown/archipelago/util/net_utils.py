# I did not write this
# Taken from https://github.com/ArchipelagoMW/Archipelago/blob/main/NetUtils.py
from __future__ import annotations

import typing
import enum
from copy import deepcopy

from json import JSONEncoder, JSONDecoder

from toontown.archipelago.util.utils import Version, ByValue

ARCHIPELAGO_GAME_NAME = "Toontown"
ARCHIPELAGO_CLIENT_VERSION = Version(0, 4, 4)


class JSONMessagePart(typing.TypedDict, total=False):
    text: str
    # optional
    type: str
    color: str
    # owning player for location/item
    player: int
    # if type == item indicates item flags
    flags: int


class ClientStatus(ByValue, enum.IntEnum):
    CLIENT_UNKNOWN = 0
    CLIENT_CONNECTED = 5
    CLIENT_READY = 10
    CLIENT_PLAYING = 20
    CLIENT_GOAL = 30


class SlotType(ByValue, enum.IntFlag):
    spectator = 0b00
    player = 0b01
    group = 0b10

    @property
    def always_goal(self) -> bool:
        """Mark this slot as having reached its goal instantly."""
        return self.value != 0b01


class Permission(ByValue, enum.IntFlag):
    disabled = 0b000  # 0, completely disables access
    enabled = 0b001  # 1, allows manual use
    goal = 0b010  # 2, allows manual use after goal completion
    auto = 0b110  # 6, forces use after goal completion, only works for release
    auto_enabled = 0b111  # 7, forces use after goal completion, allows manual use any time

    @staticmethod
    def from_text(text: str):
        data = 0
        if "auto" in text:
            data |= 0b110
        elif "goal" in text:
            data |= 0b010
        if "enabled" in text:
            data |= 0b001
        return Permission(data)


class NetworkPlayer(typing.NamedTuple):
    """Represents a particular player on a particular team."""
    team: int
    slot: int
    alias: str
    name: str


class NetworkSlot(typing.NamedTuple):
    """Represents a particular slot across teams."""
    name: str
    game: str
    type: SlotType
    group_members: typing.Union[typing.List[int], typing.Tuple] = ()  # only populated if type == group


class NetworkItem(typing.NamedTuple):
    item: int
    location: int
    player: int
    flags: int = 0


def _scan_for_TypedTuples(obj: typing.Any) -> typing.Any:
    if isinstance(obj, tuple) and hasattr(obj, "_fields"):  # NamedTuple is not actually a parent class
        data = obj._asdict()
        data["class"] = obj.__class__.__name__
        return data
    if isinstance(obj, (tuple, list, set, frozenset)):
        return tuple(_scan_for_TypedTuples(o) for o in obj)
    if isinstance(obj, dict):
        return {key: _scan_for_TypedTuples(value) for key, value in obj.items()}
    return obj


_encode = JSONEncoder(
    ensure_ascii=False,
    check_circular=False,
    separators=(',', ':'),
).encode


def encode(obj: typing.Any) -> str:
    return _encode(_scan_for_TypedTuples(obj))


def get_any_version(data: dict) -> Version:
    data = {key.lower(): value for key, value in data.items()}  # .NET version classes have capitalized keys
    return Version(int(data["major"]), int(data["minor"]), int(data["build"]))


allowlist = {
    "NetworkPlayer": NetworkPlayer,
    "NetworkItem": NetworkItem,
    "NetworkSlot": NetworkSlot
}

custom_hooks = {
    "Version": get_any_version
}


def _object_hook(o: typing.Any) -> typing.Any:
    if isinstance(o, dict):
        hook = custom_hooks.get(o.get("class", None), None)
        if hook:
            return hook(o)
        cls = allowlist.get(o.get("class", None), None)
        if cls:
            for key in tuple(o):
                if key not in cls._fields:
                    del (o[key])
            return cls(**o)

    return o


decode = JSONDecoder(object_hook=_object_hook).decode


class HandlerMeta(type):
    def __new__(mcs, name, bases, attrs):
        handlers = attrs["handlers"] = {}
        trigger: str = "_handle_"
        for base in bases:
            handlers.update(base.handlers)
        handlers.update({handler_name[len(trigger):]: method for handler_name, method in attrs.items() if
                         handler_name.startswith(trigger)})

        orig_init = attrs.get('__init__', None)
        if not orig_init:
            for base in bases:
                orig_init = getattr(base, '__init__', None)
                if orig_init:
                    break

        def __init__(self, *args, **kwargs):
            if orig_init:
                orig_init(self, *args, **kwargs)
            # turn functions into bound methods
            self.handlers = {name: method.__get__(self, type(self)) for name, method in
                             handlers.items()}

        attrs['__init__'] = __init__
        return super(HandlerMeta, mcs).__new__(mcs, name, bases, attrs)


class JSONTypes(str, enum.Enum):
    color = "color"
    text = "text"
    player_id = "player_id"
    player_name = "player_name"
    item_name = "item_name"
    item_id = "item_id"
    location_name = "location_name"
    location_id = "location_id"
    entrance_name = "entrance_name"


# A class that parses a list of JSONMessagePart instances and modifies them to have colors defined and IDs replaced
def item_flag_to_color(flag: int):
    # 0b001 = logical advancement, 0b010 = useful, 0b100 = trap
    if flag & 0b001:
        return 'plum'

    if flag & 0b010:
        return 'slateblue'

    if flag & 0b100:
        return 'salmon'

    return 'cyan'


class JSONPartFormatter:

    COLOR_BLACK = (0, 0, 0, 1)
    COLOR_RED = (.93, 0, 0, 1)
    COLOR_GREEN = (0, 1, .5, 1)
    COLOR_YELLOW = (.98, .98, .82, 1)
    COLOR_BLUE = (.4, .58, .93, 1)
    COLOR_MAGENTA = (.93, 0, .93, 1)
    COLOR_CYAN = (0, .93, .93, 1)
    COLOR_WHITE = (1, 1, 1, 1)

    COLOR_PLUM = (.69, .6, .93, 1)
    COLOR_SLATEBLUE = (.43, .54, .9, 1)
    COLOR_SALMON = (.97, .5, .45, 1)

    COLOR_MAP = {
        'black': COLOR_BLACK,
        'red': COLOR_RED,
        'green': COLOR_GREEN,
        'yellow': COLOR_YELLOW,
        'blue': COLOR_BLUE,
        'magenta': COLOR_MAGENTA,
        'cyan': COLOR_CYAN,
        'white': COLOR_WHITE,
        'plum': COLOR_PLUM,
        'slateblue': COLOR_SLATEBLUE,
        'salmon': COLOR_SALMON
    }

    def __init__(self, parts: typing.List[JSONMessagePart], client):
        self.parts = parts
        self.client = client

    def is_local_player(self, slot_num: int) -> bool:
        return slot_num == self.client.slot

    # Returns a new list of JSONMessagePart instances with replaced IDs and colors ALWAYS defined
    def get_formatted_parts(self) -> typing.List[JSONMessagePart]:

        new_parts: typing.List[JSONMessagePart] = []

        for part in self.parts:

            new_part: JSONMessagePart = deepcopy(part)

            # What type of part is this?
            part_type = part['type'] if 'type' in part else 'default'

            # Switch statement basically on how we should handle the types of parts
            if part_type in ('player_id', 'player_name'):
                self.handle_player_part(new_part)
            elif part_type in ('item_id', 'item_name'):
                self.handle_item_part(new_part)
            elif part_type in ('location_id', 'location_name'):
                self.handle_location_part(new_part)
            elif part_type == 'entrance_name':
                self.handle_entrance_part(new_part)
            elif part_type in ('default', 'text'):
                self.handle_default_part(new_part)
            elif part_type == 'color':  # No need to do anything, color is already defined
                pass
            else:
                print(f"Unknown JSONMessagePart type: {part_type}, reverting to default part behavior")
                self.handle_default_part(new_part)

            new_parts.append(new_part)

        return new_parts

    # Modifies a JSONMessagePart assuming it is a player type
    def handle_player_part(self, part: JSONMessagePart) -> None:

        # If we were given the ID, compare it against our client and override the text
        if part['type'] == 'player_id':
            pid = int(part['text'])
            # If this is us, set color to magenta otherwise yellow
            part['color'] = 'magenta' if pid == self.client.slot else 'yellow'
            part['text'] = self.client.get_slot_info(pid).name

        # If we were given name, instead of ID, do same thing basically
        elif part['type'] == 'player_name':
            part['color'] = 'magenta' if self.client.slot_name == part['text'] else 'yellow'

        else:
            print(f"Unknown JSONMessagePart type for player part: {part['type']}")
            part['color'] = 'white'

    # Modifies a JSONMessagePart assuming it is an item type
    def handle_item_part(self, part: JSONMessagePart) -> None:
        color = item_flag_to_color(part['flags'])
        part['color'] = color
        item = part['text']

        # If we were given the ID, override the text
        if part['type'] == 'item_id':
            part['text'] = self.client.get_item_name(item)

        # If we were given name, instead of ID, do same thing basically
        elif part['type'] == 'item_name':
            pass  # Do nothing

        else:
            print(f"Unknown JSONMessagePart type for item part: {part['type']}")

    # Modifies a JSONMessagePart assuming it is a location type
    def handle_location_part(self, part: JSONMessagePart) -> None:
        part['color'] = 'green'
        location = part['text']

        # If we were given the ID, override the text
        if part['type'] == 'location_id':
            part['text'] = self.client.get_location_name(location)

        # If we were given name, instead of ID, do same thing basically
        elif part['type'] == 'location_name':
            pass  # Do nothing

        else:
            print(f"Unknown JSONMessagePart type for location part: {part['type']}")

    # Modifies a JSONMessagePart assuming it is an entrance type
    def handle_entrance_part(self, part: JSONMessagePart) -> None:
        part['color'] = 'blue'

    # Modifies a JSONMessagePart assuming it is a default type (no type specified)
    def handle_default_part(self, part: JSONMessagePart) -> None:
        part['color'] = 'white'


class JSONtoTextParser(metaclass=HandlerMeta):
    color_codes = {
        # not exact color names, close enough but decent looking
        "black": "000000",
        "red": "EE0000",
        "green": "00FF7F",
        "yellow": "FAFAD2",
        "blue": "6495ED",
        "magenta": "EE00EE",
        "cyan": "00EEEE",
        "slateblue": "6D8BE8",
        "plum": "AF99EF",
        "salmon": "FA8072",
        "white": "FFFFFF"
    }

    def __init__(self, client):
        self.client = client

    def parse(self, input: typing.List[JSONMessagePart]) -> str:
        return "".join(self.handle_node(section) for section in input)

    def handle_node(self, node: JSONMessagePart):
        node_type = node.get("type", None)
        handler = self.handlers.get(node_type, self.handlers["text"])
        return handler(node)

    def _handle_color(self, node: JSONMessagePart):
        codes = node["color"].split(";")
        buffer = "".join(color_code(code) for code in codes if code in color_codes)
        return buffer + self._handle_text(node) + color_code("reset")

    def _handle_text(self, node: JSONMessagePart):
        return node.get("text", "")

    def _handle_player_id(self, node: JSONMessagePart):
        player = int(node["text"])
        node["color"] = 'magenta' if player == self.client.slot else 'yellow'
        node["text"] = self.client.get_slot_info(player).name
        return self._handle_color(node)

    # for other teams, spectators etc.? Only useful if player isn't in the clientside mapping
    def _handle_player_name(self, node: JSONMessagePart):
        node["color"] = 'yellow'
        return self._handle_color(node)

    def _handle_item_name(self, node: JSONMessagePart):
        flags = node.get("flags", 0)
        if flags == 0:
            node["color"] = 'cyan'
        elif flags & 0b001:  # advancement
            node["color"] = 'plum'
        elif flags & 0b010:  # useful
            node["color"] = 'slateblue'
        elif flags & 0b100:  # trap
            node["color"] = 'salmon'
        else:
            node["color"] = 'cyan'
        return self._handle_color(node)

    def _handle_item_id(self, node: JSONMessagePart):
        item_id = int(node["text"])
        node["text"] = self.client.get_item_name(item_id)
        return self._handle_item_name(node)

    def _handle_location_name(self, node: JSONMessagePart):
        node["color"] = 'green'
        return self._handle_color(node)

    def _handle_location_id(self, node: JSONMessagePart):
        item_id = int(node["text"])
        node["text"] = self.client.get_location_name(item_id)
        return self._handle_location_name(node)

    def _handle_entrance_name(self, node: JSONMessagePart):
        node["color"] = 'blue'
        return self._handle_color(node)


class RawJSONtoTextParser(JSONtoTextParser):
    def _handle_color(self, node: JSONMessagePart):
        return self._handle_text(node)


color_codes = {'reset': 0, 'bold': 1, 'underline': 4, 'black': 30, 'red': 31, 'green': 32, 'yellow': 33, 'blue': 34,
               'magenta': 35, 'cyan': 36, 'white': 37, 'black_bg': 40, 'red_bg': 41, 'green_bg': 42, 'yellow_bg': 43,
               'blue_bg': 44, 'magenta_bg': 45, 'cyan_bg': 46, 'white_bg': 47}


def color_code(*args):
    return '\033[' + ';'.join([str(color_codes[arg]) for arg in args]) + 'm'


def color(text, *args):
    return color_code(*args) + text + color_code('reset')


def add_json_text(parts: list, text: typing.Any, **kwargs) -> None:
    parts.append({"text": str(text), **kwargs})


def add_json_item(parts: list, item_id: int, player: int = 0, item_flags: int = 0, **kwargs) -> None:
    parts.append({"text": str(item_id), "player": player, "flags": item_flags, "type": JSONTypes.item_id, **kwargs})


def add_json_location(parts: list, item_id: int, player: int = 0, **kwargs) -> None:
    parts.append({"text": str(item_id), "player": player, "type": JSONTypes.location_id, **kwargs})


class Hint(typing.NamedTuple):
    receiving_player: int
    finding_player: int
    location: int
    item: int
    found: bool
    entrance: str = ""
    item_flags: int = 0

    def re_check(self, ctx, team) -> Hint:
        if self.found:
            return self
        found = self.location in ctx.location_checks[team, self.finding_player]
        if found:
            return Hint(self.receiving_player, self.finding_player, self.location, self.item, found, self.entrance,
                        self.item_flags)
        return self

    def __hash__(self):
        return hash((self.receiving_player, self.finding_player, self.location, self.item, self.entrance))

    def as_network_message(self) -> dict:
        parts = []
        add_json_text(parts, "[Hint]: ")
        add_json_text(parts, self.receiving_player, type="player_id")
        add_json_text(parts, "'s ")
        add_json_item(parts, self.item, self.receiving_player, self.item_flags)
        add_json_text(parts, " is at ")
        add_json_location(parts, self.location, self.finding_player)
        add_json_text(parts, " in ")
        add_json_text(parts, self.finding_player, type="player_id")
        if self.entrance:
            add_json_text(parts, "'s World at ")
            add_json_text(parts, self.entrance, type="entrance_name")
        else:
            add_json_text(parts, "'s World")
        add_json_text(parts, ". ")
        if self.found:
            add_json_text(parts, "(found)", type="color", color="green")
        else:
            add_json_text(parts, "(not found)", type="color", color="red")

        return {"cmd": "PrintJSON", "data": parts, "type": "Hint",
                "receiving": self.receiving_player,
                "item": NetworkItem(self.item, self.location, self.finding_player, self.item_flags),
                "found": self.found}

    @property
    def local(self):
        return self.receiving_player == self.finding_player