from direct.fsm.FSM import FSM
from direct.interval.MetaInterval import Parallel
from direct.interval.SoundInterval import SoundInterval
from panda3d.core import Point3, NodePath


class PieGameRampFSM(FSM):

    def __init__(self, rampNode: NodePath) -> None:
        super().__init__("PieGameRampFSM")
        self.rampNode = rampNode
        self.activeIntervals = {}

        self.rampSlideSfx = loader.loadSfx('phase_9/audio/sfx/CHQ_VP_ramp_slide.ogg')

    def cleanup(self) -> None:
        super().cleanup()
        self.cleanupIntervals()
        del self.activeIntervals
        del self.rampSlideSfx

    def storeInterval(self, interval, name):
        self.activeIntervals[name] = interval

    def cleanupIntervals(self):
        # Copy the current intervals into a local list
        intervals = list(self.activeIntervals.values())

        # Iterate over that list
        for interval in intervals:
            interval.finish()

        # Clear the dictionary once you’re done
        self.activeIntervals.clear()

    def clearInterval(self, name, finish=1):
        if name in self.activeIntervals:
            ival = self.activeIntervals[name]
            if finish:
                ival.finish()
            else:
                ival.pause()
            if name in self.activeIntervals:
                del self.activeIntervals[name]
        else:
            self.notify.debug('interval: %s already cleared' % name)

    def finishInterval(self, name):
        if name in self.activeIntervals:
            interval = self.activeIntervals[name]
            interval.finish()

    """
    FSM states
    """

    def enterExtend(self):
        intervalName = 'extend-%s' % self.rampNode.getName()
        adjustTime = 2.0 * self.rampNode.getX() / 18.0
        ival = Parallel(SoundInterval(self.rampSlideSfx, node=self.rampNode),
                        self.rampNode.posInterval(adjustTime, Point3(0, 0, 0), blendType='easeInOut', name=intervalName))
        ival.start()
        self.storeInterval(ival, intervalName)

    def exitExtend(self):
        intervalName = 'extend-%s' % self.rampNode.getName()
        self.clearInterval(intervalName)

    def enterExtended(self):
        self.rampNode.setPos(0, 0, 0)

    def enterRetract(self):
        intervalName = 'retract-%s' % self.rampNode.getName()
        adjustTime = 2.0 * (18 - self.rampNode.getX()) / 18.0
        ival = Parallel(SoundInterval(self.rampSlideSfx, node=self.rampNode),
                        self.rampNode.posInterval(adjustTime, Point3(18, 0, 0), blendType='easeInOut', name=intervalName))
        ival.start()
        self.storeInterval(ival, intervalName)

    def exitRetract(self):
        intervalName = 'retract-%s' % self.rampNode.getName()
        self.clearInterval(intervalName)

    def enterRetracted(self):
        self.rampNode.setPos(18, 0, 0)
