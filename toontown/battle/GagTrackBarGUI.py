from direct.gui import DirectGuiGlobals
from direct.gui.DirectWaitBar import DirectWaitBar
from panda3d.core import TextNode

from toontown.archipelago.util.global_text_properties import get_raw_formatted_string, MinimalJsonMessagePart
from toontown.toon.Experience import Experience
from toontown.toonbase import ToontownBattleGlobals, TTLocalizer


def getTrackColor(track, multiplier=1.0):
    r, g, b = ToontownBattleGlobals.TrackColors[track]
    r *= multiplier
    g *= multiplier
    b *= multiplier
    return r, g, b


class GagTrackBarGUI(DirectWaitBar):

    DEFAULT_TRACK_FRAME_ALPHA = 0.7
    DEFAULT_TRACK_BAR_ALPHA = 0.8

    LOCKED_BAR_COLOR = (.9, .1, .1, 1)

    DEFAULT_BORDER_WIDTH = (0.02, 0.02)

    DEFAULT_TEXT_POS = (0, -0.05)

    DEFAULT_FRAME_SIZE = (-0.6, 0.6, -0.1, 0.1)

    DEFAULT_TEXT_SCALE = 0.16
    DEFAULT_TEXT_COLOR = (0, 0, 0, 0.8)

    SKINNY_FRAME_SIZE = (-1, 1, -0.15, 0.15)

    SKINNY_TEXT_SCALE = 0.18
    SKINNY_TEXT_COLOR = (0, 0, 0, .8)

    def __init__(self, track: int, **kw):
        super().__init__(**kw)
        self.initialiseoptions(GagTrackBarGUI)

        self.track: int = track
        self.setTrack(self.track)
        self.makeThick()

    def makeThick(self):
        self['frameSize'] = self.DEFAULT_FRAME_SIZE
        self['text_scale'] = self.DEFAULT_TEXT_SCALE
        self['text_fg'] = self.DEFAULT_TEXT_COLOR

    def makeSkinny(self):
        self['frameSize'] = self.SKINNY_FRAME_SIZE
        self['text_scale'] = self.SKINNY_TEXT_SCALE
        self['text_fg'] = self.SKINNY_TEXT_COLOR

    def reset(self):
        self['relief'] = DirectGuiGlobals.SUNKEN
        self['borderWidth'] = self.DEFAULT_BORDER_WIDTH

        # Set the colors
        self.resetBarColorAndFrameColor()

        self['text'] = '0/0'
        self['text_align'] = TextNode.ACenter
        self['text_pos'] = self.DEFAULT_TEXT_POS

    def resetBarColorAndFrameColor(self):
        self.resetBarColor()
        self.resetFrameColor()

    def resetBarColor(self, multiplier=0.8):
        self['barColor'] = self.getTrackBarColor(multiplier)

    def resetFrameColor(self):
        self['frameColor'] = self.getTrackFrameColor()

    def makeBarRed(self):
        self['barColor'] = self.LOCKED_BAR_COLOR

    def makeBarBright(self):
        self['barColor'] = self.getTrackBarColor(multiplier=1.0)

    def makeFrameRed(self):
        self['frameColor'] = self.LOCKED_BAR_COLOR

    def getTrackFrameColor(self):
        r, g, b = getTrackColor(self.track, multiplier=self.DEFAULT_TRACK_FRAME_ALPHA)
        return r, g, b, 1

    def getTrackBarColor(self, multiplier=0.8):
        r, g, b = getTrackColor(self.track, multiplier)
        return r, g, b, 1

    # Sets this gag track bar GUI element to appear in the default state to represent a specific gag track
    def setTrack(self, track):
        self.track = track
        self.reset()

    # Sets this bar to display the string for when a toon has gags over the normal gag cap
    def showExperienceOverflowText(self, currentExp: int, track: int):

        CAP: int = ToontownBattleGlobals.MaxSkill
        boost = ToontownBattleGlobals.getUberDamageBonusString(currentExp, track)
        xp = TTLocalizer.InventoryUberTrackMaxed if currentExp >= CAP else currentExp

        self['text'] = TTLocalizer.InventoryUberTrackExp % {'curExp': xp, 'boost': boost}
        self['value'] = CAP
        self['range'] = CAP

    def showExperienceDefaultText(self, currentExp: int, expCap: int):

        # Update to show experience, if current exp == exp cap, the cap will be red
        text = f"{currentExp} / {expCap}"

        # We are capped. Make the frame red
        if currentExp >= expCap:
            self.makeFrameRed()
            text = TTLocalizer.InventoryTrackLocked % {'exp': expCap}

        self['text'] = text
        self['value'] = currentExp
        self['range'] = expCap

    def forceShowExperience(self, currentExp: int, expCap: int, track: int):

        # If the currentExp is over the normal gag limit, we can safely assume that this is overflow
        if currentExp >= ToontownBattleGlobals.regMaxSkill:
            self.showExperienceOverflowText(currentExp, track)
            return

        self.showExperienceDefaultText(currentExp, expCap)

    # Given an experience instance, display this gag track bar
    def showExperience(self, experience: Experience, track: int):
        self.setTrack(track)

        nextGagExp = experience.getNextExpValue(track, experience.getExp(track))
        # Edge case, if we are able to overflow but haven't reached that part yet, display regmaxskill
        if ToontownBattleGlobals.regMaxSkill > experience.getExp(track) >= ToontownBattleGlobals.Levels[track][-1]:
            nextGagExp = ToontownBattleGlobals.regMaxSkill

        cap = min(experience.getExperienceCapForTrack(track), nextGagExp)
        self.forceShowExperience(experience.getExp(track), cap, track)

        if experience.getExperienceCapForTrack(track) < nextGagExp:
            self.makeFrameRed()