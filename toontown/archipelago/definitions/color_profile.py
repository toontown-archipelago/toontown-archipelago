import random
from dataclasses import dataclass

from panda3d.core import PGButton, Vec4


# A class used for groupings of colors to use for Nametag colors
# similarly to libotp.nametag.NametagGlobals.getNameFg()
#
# These definitions are put into its own dataclass to provide simple definitions but also have some utility.
# These definitions can be used for things such as: Nametags, Labels for the friends list, and misc UI elements
# with Archipelago teams being its main purpose.
@dataclass
class ColorProfile:

    # The color meant to be used when clickable. (i.e. you can click your friend's nametag)
    clickable: Vec4

    # The color meant to be used when currently pressed on the element.
    pressed: Vec4

    # The color meant to be used when hovering your cursor over the element.
    hover: Vec4

    # The color meant to be used when the element is disabled. (unable to be clicked)
    disabled: Vec4

    # Given a ColorProfile, return the color that is considered the "main" color.
    # In most circumstances, this is just the color that shows up when a UI element is clickable.
    def getPrimaryColor(self) -> Vec4:
        return self.clickable

    # Given a state (from PGButton), return the corresponding color we should use for its state.
    # See Nametag2d.getState()
    def getColorFromState(self, state: int) -> Vec4:
        color = {
            PGButton.SReady:     self.clickable,
            PGButton.SDepressed: self.pressed,
            PGButton.SRollover:  self.hover,
            PGButton.SInactive:  self.disabled,
        }.get(state)

        if color is not None:
            return color

        # We were given an invalid state, ideally this should never happen
        raise KeyError(f"ColorProfile: Unknown state: {state}. You must provide a state defined in panda3d.core.PGButton!")

    # Helper method that leaves alpha unchanged and bounds color values between 0 and 1 when performing
    # multiplication on Vec4 objects.
    def _multiply(self, color: Vec4, multiplier: float) -> Vec4:
        a = color[3]
        r, g, b, _ = color * multiplier
        r = min(max(r, 0), 1)
        g = min(max(g, 0), 1)
        b = min(max(b, 0), 1)
        return Vec4(r, g, b, a)

    # Returns a copy of this instance so you can modify it without messing with the original definition.
    def copy(self):
        return ColorProfile(Vec4(*self.clickable), Vec4(*self.pressed), Vec4(*self.hover), Vec4(*self.disabled))


# Uses one color to dynamically generate a pressed/hover/disabled state color.
class AutoColorProfile(ColorProfile):
    def __init__(self, primary: Vec4):
        self._primary: Vec4 = primary

    """
    Property definitions that act as overrides for ColorProfile attributes
    """

    # Original color passed in to __init__()
    @property
    def clickable(self) -> Vec4:
        return self._primary

    # When hovering, the color typically tends to be slightly brighter than the original color
    @property
    def hover(self) -> Vec4:
        return self._multiply(self.getPrimaryColor(), 1.25)

    # Disabled colors are typically just darker versions of the primary colors.
    @property
    def disabled(self) -> Vec4:
        return self._multiply(self.getPrimaryColor(), 0.75)

    # For pressed, we can just use the same as disabled.
    @property
    def pressed(self) -> Vec4:
        return self.disabled


# Define some ColorProfile constants to use throughout the codebase :3
# Local Toon blue:
BLUE = ColorProfile(
    Vec4(0.3, 0.3, 0.7, 1),
    Vec4(0.5, 0.5, 1, 1),
    Vec4(0.5, 0.5, 1, 1),
    Vec4(0.3, 0.3, 0.7, 1),
)

# Other player Toon green:
GREEN = ColorProfile(
    Vec4(0, 0.6, 0.2, 1),
    Vec4(0, 0.6, 0.2, 1),
    Vec4(0, 1, 0.5, 1),
    Vec4(0.1, 0.4, 0.2, 1),
)

# Red
RED = AutoColorProfile(Vec4(.85, .35, .35, 1))

# Yellow
YELLOW = AutoColorProfile(Vec4(.8, .8, .15, 1))

# Cyan
CYAN = AutoColorProfile(Vec4(.15, .8, .8, 1))

# Magenta
MAGENTA = AutoColorProfile(Vec4(.8, .15, .8, 1))

# Orange
ORANGE = AutoColorProfile(Vec4(.9, .65, .22, 1))

# Purple
PURPLE = AutoColorProfile(Vec4(.47, .15, .8, 1))

# Pink
PINK = AutoColorProfile(Vec4(.9, .5, .77, 1))

# Mint Green
MINT_GREEN = AutoColorProfile(Vec4(.56, .87, .6, 1))

# Midnight Blue
MIDNIGHT_BLUE = AutoColorProfile(Vec4(.3, .32, .52, 1))

# Burgundy
BURGUNDY = AutoColorProfile(Vec4(.55, .09, .22, 1))

# Mauve (washed out purple
MAUVE = AutoColorProfile(Vec4(.64, .46, .65, 1))

# Gray
GRAY = AutoColorProfile(Vec4(.55, .55, .55, 1))


# Use the power of RNG to generate a completely random color profile.
# Pass in a seed for consistent ID -> Color profiles.
def getRandomColorProfile(seed=None) -> AutoColorProfile:
    rng = random.Random()
    if seed is not None:
        rng.seed(seed)

    return AutoColorProfile(Vec4(rng.random(), rng.random(), rng.random(), 1))
