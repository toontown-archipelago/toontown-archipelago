from datetime import datetime, timedelta

from direct.gui.DirectGui import *
from panda3d.core import *

from toontown.coghq import CraneLeagueGlobals
from toontown.suit.Suit import *
from direct.task.Task import Task
from direct.interval.IntervalGlobal import *


class BossSpeedrunTimer:

    TIMER = 0
    STOPWATCH = 1
    MODE = STOPWATCH

    def __init__(self):

        self.frame = DirectFrame(pos=(-0.22, 0, .9))
        self.ot_frame = DirectFrame(pos=(0, 0, .9))
        self.time_text = OnscreenText(parent=self.frame, text='00:00.00', style=3, fg=(.9, .9, .9, .85), align=TextNode.ALeft, scale=0.1, font=ToontownGlobals.getCompetitionFont())
        self.overtime_text = OnscreenText(parent=self.ot_frame, text='OVERTIME!', style=3, fg=(.9, .75, .4, .85), align=TextNode.ABoxedCenter, scale=0.1, font=ToontownGlobals.getCompetitionFont())
        self.overtime_text_sequence = Sequence(LerpScaleInterval(self.overtime_text, scale=1.2, blendType='easeInOut', duration=2), LerpScaleInterval(self.overtime_text, scale=1, blendType='easeInOut', duration=2))
        self.overtime_text_sequence.loop()
        self.reset()
        self.overridden_time = None
        self.start_updating()

    def reset(self):
        self.started = datetime.now()
        self.overridden_time = None

    def set_pos(self, pos):
        self.frame.setPos(pos)

    def stop_updating(self):
        taskMgr.remove('boss-timer-update-time')

    def start_updating(self):
        self.stop_updating()
        taskMgr.add(self._update_time_task, "boss-timer-update-time")

    def _update_time_task(self, task):
        self.update_time()
        return Task.cont

    def _get_formatted_time(self, total_seconds):
        min = total_seconds // 60
        sec = total_seconds % 60
        frac = int((total_seconds - int(total_seconds)) * 100)
        return '{:02}:{:02}.{:02}'.format(int(min), int(sec), frac)

    def update_time(self):
        now = datetime.now()
        difference = now - self.started
        total_secs = difference.total_seconds() if not self.overridden_time else self.overridden_time
        self.time_text.setText(self._get_formatted_time(total_secs))

    def override_time(self, secs):
        self.overridden_time = secs

    def show_overtime(self):
        self.overtime_text.show()

    def hide_overtime(self):
        self.overtime_text.hide()

    def cleanup(self):
        self.overtime_text_sequence.finish()
        self.overtime_text.cleanup()
        self.stop_updating()
        self.time_text.cleanup()
        self.ot_frame.destroy()
        self.frame.destroy()

    def show(self):
        self.frame.show()
        self.ot_frame.show()

    def hide(self):
        self.frame.hide()
        self.ot_frame.hide()

# Same thing as the other timer, but counts down instead
class BossSpeedrunTimedTimer(BossSpeedrunTimer):

    MODE = BossSpeedrunTimer.TIMER

    def __init__(self, time_limit):
        BossSpeedrunTimer.__init__(self)
        self.time_limit = time_limit
        self.want_overtime = False

    def reset(self):
        BossSpeedrunTimer.reset(self)
        self.time_text['fg'] = (.9, .9, .9, .85)

    def update_time(self):
        now = datetime.now()
        end = self.started + timedelta(seconds=self.time_limit)
        time_left = end - now
        total_secs = time_left.total_seconds()
        if total_secs < 0:
            total_secs = 0

        if self.overridden_time is not None:
            self.time_text['fg'] = (0, .7, 0, 1) if self.overridden_time > 0.0 else (.7, 0, 0, 1)
            if self.overridden_time <= 0.0:
                self.time_text.setText('00:00.00')
            else:
                self.time_text.setText(self._get_formatted_time(self.overridden_time))
            return

        if self.want_overtime:
            self.time_text.hide()
            super().show_overtime()
        else:
            self.time_text.show()
            super().hide_overtime()

        if total_secs <= 10:
            frac_secs = int((total_secs - int(total_secs))*100)
            self.time_text['fg'] = (.7, 0, 0, 1) if frac_secs < 50 else (.9, .9, .9, .85)
        elif total_secs <= 31:
            self.time_text['fg'] = (.7, 0, 0, 1) if int(total_secs) % 2 == 0 else (.9, .9, .9, .85)

        self.time_text.setText(self._get_formatted_time(total_secs))

    def show_overtime(self):
        self.want_overtime = True

    def hide_overtime(self):
        self.want_overtime = False
