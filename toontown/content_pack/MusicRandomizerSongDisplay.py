from direct.gui import DirectGuiGlobals
from direct.gui.DirectLabel import DirectLabel
from direct.interval.FunctionInterval import Wait, Func
from direct.interval.LerpInterval import LerpPosInterval
from direct.interval.MetaInterval import Sequence
from panda3d.core import TextNode

class MusicRandomizerSongDisplay(DirectLabel):

    FRAME_COLOR = (0, 0, 0, 0.5)

    ONSCREEN_POS = (0.65, 0, -0.97)
    OFFSCREEN_POS = (0.65, 0, -1.1)

    TEXT_SCALE = .035
    TEXT_POS = (0, 0)
    TEXT_COLOR = (1, 1, 1, 1)
    TEXT_ALIGN = TextNode.ACenter

    SHOW_DURATION = 5
    SLIDE_DURATION = .5

    def __init__(self, **kw):
        super().__init__(**kw)
        self.initialiseoptions(MusicRandomizerSongDisplay)
        self._slide_sequence = None

    # Call to reset all options to default, ideally only need to do this once
    def set_default_options(self):

        # Setup the base frame
        self['pos'] = self.OFFSCREEN_POS  # todo change to offscreen

        # Setup the text
        self['text_scale'] = self.TEXT_SCALE
        self['text_pos'] = self.TEXT_POS
        self['text_fg'] = self.TEXT_COLOR
        self['text_align'] = self.TEXT_ALIGN

    # Given a song title, update the elements immediately to represent this
    def display_song(self, song_title=""):
        self.setScale(0.06)
        self.setText(song_title)
        self._do_slide_sequence()

    # Perform a slide transition into view on screen to show the display
    def _do_slide_sequence(self):
        self._cleanup_intervals()
        self['text_pos'] = self.TEXT_POS
        self['text_fg'] = self.TEXT_COLOR
        self['text_align'] = self.TEXT_ALIGN
        self['text_bg'] = self.FRAME_COLOR

        self._slide_sequence = Sequence(
            Func(self.show),
            LerpPosInterval(self, startPos=self.OFFSCREEN_POS, pos=self.ONSCREEN_POS, duration=self.SLIDE_DURATION, blendType='easeInOut'),
            Wait(self.SHOW_DURATION),
            LerpPosInterval(self, startPos=self.ONSCREEN_POS, pos=self.OFFSCREEN_POS, duration=self.SLIDE_DURATION, blendType='easeInOut'),
            Func(self.hide),
        )

        self._slide_sequence.start()

    # Perform a slide transition to immediately force this off screen
    def _do_hide_sequence(self):

        self._cleanup_intervals()

        self._slide_sequence = Sequence(
            Func(self.show),
            LerpPosInterval(self, startPos=self.ONSCREEN_POS, pos=self.OFFSCREEN_POS, duration=self.SLIDE_DURATION, blendType='easeInOut'),
            Func(self.hide),
        )
        self._slide_sequence.start()

    def _cleanup_intervals(self):
        if self._slide_sequence:
            self._slide_sequence.pause()
            self._slide_sequence = None

    def destroy(self):
        self.ignoreAll()
        self._cleanup_intervals()
        super().destroy()
