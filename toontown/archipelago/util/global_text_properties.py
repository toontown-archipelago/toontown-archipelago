# Add text properties to satisfy the following colors for json strings
# COLOR_BLACK = (0, 0, 0, 1)
# COLOR_RED = (.93, 0, 0, 1)
# COLOR_GREEN = (0, 1, .5, 1)
# COLOR_YELLOW = (.98, .98, .82, 1)
# COLOR_BLUE = (.4, .58, .93, 1)
# COLOR_MAGENTA = (.93, 0, .93, 1)
# COLOR_CYAN = (0, .93, .93, 1)
# COLOR_WHITE = (1, 1, 1, 1)
#
# COLOR_PLUM = (.69, .6, .93, 1)
# COLOR_SLATEBLUE = (.43, .54, .9, 1)
# COLOR_SALMON = (.97, .5, .45, 1)
#
# COLOR_MAP = {
#     'black': COLOR_BLACK,
#     'red': COLOR_RED,
#     'green': COLOR_GREEN,
#     'yellow': COLOR_YELLOW,
#     'blue': COLOR_BLUE,
#     'magenta': COLOR_MAGENTA,
#     'cyan': COLOR_CYAN,
#     'white': COLOR_WHITE,
#     'plum': COLOR_PLUM,
#     'slateblue': COLOR_SLATEBLUE,
#     'salmon': COLOR_SALMON
# }
from typing import List, NamedTuple

from panda3d.core import TextProperties, TextPropertiesManager

from toontown.archipelago.util.net_utils import JSONPartFormatter, JSONMessagePart

__TEXT_PROPERTIES_MANAGER = TextPropertiesManager.getGlobalPtr()

__JSON_COLOR_CODE_TO_TEXT_PROPERTY = {}


# Called locally to register a new constant TextProperties
def __register_property(json_color_code: str, text_property_code: str, properties: TextProperties):
    __JSON_COLOR_CODE_TO_TEXT_PROPERTY[json_color_code] = text_property_code
    __TEXT_PROPERTIES_MANAGER.setProperties(text_property_code, properties)


# Now define all our TextProperty instances, first define what the code is for Panda3D, this isn't important
# Instantiate a TextProperties instance and tweak the settings desired
# Register it using __register_property() and provide the Panda3D code, the JSON code, then the TextProperties instance


# Black text
TEXT_PROPERTIES_CODE_BLACK = "json_black"
__TEXT_PROPERTIES_BLACK = TextProperties()
__TEXT_PROPERTIES_BLACK.setTextColor(*JSONPartFormatter.COLOR_BLACK)
__register_property('black', TEXT_PROPERTIES_CODE_BLACK, __TEXT_PROPERTIES_BLACK)


# Red text
TEXT_PROPERTIES_CODE_RED = "json_red"
__TEXT_PROPERTIES_RED = TextProperties()
__TEXT_PROPERTIES_RED.setTextColor(*JSONPartFormatter.COLOR_RED)
__register_property('red', TEXT_PROPERTIES_CODE_RED, __TEXT_PROPERTIES_RED)


# Green text
TEXT_PROPERTIES_CODE_GREEN = "json_green"
__TEXT_PROPERTIES_GREEN = TextProperties()
__TEXT_PROPERTIES_GREEN.setTextColor(*JSONPartFormatter.COLOR_GREEN)
__register_property('green', TEXT_PROPERTIES_CODE_GREEN, __TEXT_PROPERTIES_GREEN)


# Yellow text
TEXT_PROPERTIES_CODE_YELLOW = "json_yellow"
__TEXT_PROPERTIES_YELLOW = TextProperties()
__TEXT_PROPERTIES_YELLOW.setTextColor(*JSONPartFormatter.COLOR_YELLOW)
__register_property('yellow', TEXT_PROPERTIES_CODE_YELLOW, __TEXT_PROPERTIES_YELLOW)


# Blue text
TEXT_PROPERTIES_CODE_BLUE = "json_blue"
__TEXT_PROPERTIES_BLUE = TextProperties()
__TEXT_PROPERTIES_BLUE.setTextColor(*JSONPartFormatter.COLOR_BLUE)
__register_property('blue', TEXT_PROPERTIES_CODE_BLUE, __TEXT_PROPERTIES_BLUE)


# Magenta text
TEXT_PROPERTIES_CODE_MAGENTA = "json_magenta"
__TEXT_PROPERTIES_MAGENTA = TextProperties()
__TEXT_PROPERTIES_MAGENTA.setTextColor(*JSONPartFormatter.COLOR_MAGENTA)
__register_property('magenta', TEXT_PROPERTIES_CODE_MAGENTA, __TEXT_PROPERTIES_MAGENTA)


# Cyan text
TEXT_PROPERTIES_CODE_CYAN = "json_cyan"
__TEXT_PROPERTIES_CYAN = TextProperties()
__TEXT_PROPERTIES_CYAN.setTextColor(*JSONPartFormatter.COLOR_CYAN)
__register_property('cyan', TEXT_PROPERTIES_CODE_CYAN, __TEXT_PROPERTIES_CYAN)


# White text
TEXT_PROPERTIES_CODE_WHITE = "json_white"
__TEXT_PROPERTIES_WHITE = TextProperties()
__TEXT_PROPERTIES_WHITE.setTextColor(*JSONPartFormatter.COLOR_WHITE)
__register_property('white', TEXT_PROPERTIES_CODE_WHITE, __TEXT_PROPERTIES_WHITE)


# Plum text
TEXT_PROPERTIES_CODE_PLUM = "json_plum"
__TEXT_PROPERTIES_PLUM = TextProperties()
__TEXT_PROPERTIES_PLUM.setTextColor(*JSONPartFormatter.COLOR_PLUM)
__register_property('plum', TEXT_PROPERTIES_CODE_PLUM, __TEXT_PROPERTIES_PLUM)


# slateblue text
TEXT_PROPERTIES_CODE_SLATEBLUE = "json_slateblue"
__TEXT_PROPERTIES_SLATEBLUE = TextProperties()
__TEXT_PROPERTIES_SLATEBLUE.setTextColor(*JSONPartFormatter.COLOR_SLATEBLUE)
__register_property('slateblue', TEXT_PROPERTIES_CODE_SLATEBLUE, __TEXT_PROPERTIES_SLATEBLUE)


# salmon text
TEXT_PROPERTIES_CODE_SALMON = "json_salmon"
__TEXT_PROPERTIES_SALMON = TextProperties()
__TEXT_PROPERTIES_SALMON.setTextColor(*JSONPartFormatter.COLOR_SALMON)
__register_property('salmon', TEXT_PROPERTIES_CODE_SALMON, __TEXT_PROPERTIES_SALMON)


# Bold text (ideally use a diff font but too much work rn so i am making bold actually italics)
TEXT_PROPERTIES_CODE_BOLD = "json_bold"
__TEXT_PROPERTIES_BOLD = TextProperties()
__TEXT_PROPERTIES_BOLD.setSlant(.30)
__register_property('bold', TEXT_PROPERTIES_CODE_BOLD, __TEXT_PROPERTIES_BOLD)


# Underline text
TEXT_PROPERTIES_CODE_UNDERLINE = "json_underline"
__TEXT_PROPERTIES_UNDERLINE = TextProperties()
__TEXT_PROPERTIES_UNDERLINE.setUnderscore(True)
__register_property('underline', TEXT_PROPERTIES_CODE_UNDERLINE, __TEXT_PROPERTIES_UNDERLINE)


# salmon text
TEXT_PROPERTIES_CODE_FISH_SUBTEXT = "json_fish_subtext"
__TEXT_PROPERTIES_FISH = TextProperties()
__TEXT_PROPERTIES_FISH.setSlant(0.25)
__TEXT_PROPERTIES_FISH.setTextScale(0.73)
__register_property('fishSubtext', TEXT_PROPERTIES_CODE_FISH_SUBTEXT, __TEXT_PROPERTIES_FISH)


# Called publically to get the TextProperties property code from a json color code
def get_property_code_from_json_code(json_color_code: str) -> str:
    return __JSON_COLOR_CODE_TO_TEXT_PROPERTY.get(json_color_code, TEXT_PROPERTIES_CODE_WHITE)


class MinimalJsonMessagePart(NamedTuple):
    message: str
    color: str = 'white'  # Use a json color code, 'red' 'blue' 'salmon' etc.


# Use this is you want to use the JSONMessagePart system to create strings to display in game. This method will skip
# all the special formatting that AP messages need however, and will only utilize the 'text' and 'color' fields
# There is no error checking for this method so be wary of the color ur passing in

# Example usage:
# msg = get_raw_formatted_string([
#   MinimalJsonMessagePart(message='this is a '),
#   MinimalJsonMessagePart(message='colorful', color='red'),
#   MinimalJsonMessagePart(message='message ', color='blue'),
#   MinimalJsonMessagePart(message=' :)', color='green'),
# ])
def get_raw_formatted_string(parts: List[MinimalJsonMessagePart]) -> str:
    msg = ''
    for part in parts:
        msg += f"\1{get_property_code_from_json_code(part.color)}\1{part.message}\2"
    return msg
