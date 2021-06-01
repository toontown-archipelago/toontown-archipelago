from datetime import datetime

from direct.gui.DirectGui import *
from panda3d.core import *
from toontown.suit.Suit import *
from direct.task.Task import Task
from direct.interval.IntervalGlobal import *


class BossSpeedrunTimer:

    def __init__(self):
        self.time_text = OnscreenText(parent=aspect2d, text='0:00.00', style=3, fg=(1, 1, 1, 1), align=TextNode.ALeft, scale=0.1, pos=(-0.15, .9))
        self.reset()
        self.overridden_time = None
        self.start_updating()

    def reset(self):
        self.started = datetime.now()
        self.overridden_time = None

    def stop_updating(self):
        taskMgr.remove('boss-timer-update-time')

    def start_updating(self):
        self.stop_updating()
        taskMgr.add(self._update_time_task, "boss-timer-update-time")

    def _update_time_task(self, task):
        self.update_time()
        return Task.cont

    def update_time(self):
        now = datetime.now()
        difference = now - self.started
        total_secs = difference.total_seconds() if not self.overridden_time else self.overridden_time
        min = total_secs // 60
        sec = total_secs % 60
        frac = int((total_secs - int(total_secs)) * 100)
        new_time = '{:01}:{:02}.{:02}'.format(int(min), int(sec), frac)
        self.time_text.setText(new_time)

    def override_time(self, secs):
        self.overridden_time = secs

    def cleanup(self):
        self.stop_updating()
        self.time_text.cleanup()

    def show(self):
        self.time_text.show()

    def hide(self):
        self.time_text.hide()
