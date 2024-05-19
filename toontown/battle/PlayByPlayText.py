from panda3d.core import *
from toontown.toonbase import TTLocalizer
from toontown.toonbase.ToontownBattleGlobals import *
from toontown.toonbase.ToontownGlobals import *
from .SuitBattleGlobals import *
from direct.interval.IntervalGlobal import *
from direct.directnotify import DirectNotifyGlobal
import string
from direct.gui import OnscreenText
from . import BattleBase

class PlayByPlayText(OnscreenText.OnscreenText):
    notify = DirectNotifyGlobal.directNotify.newCategory('PlayByPlayText')

    def __init__(self):
        OnscreenText.OnscreenText.__init__(self, mayChange=1, scale=TTLocalizer.PBPTonscreenText, fg=(1, 0, 0, 1), font=getSignFont(), wordwrap=13)
        self.setZ(0.75)

    def getShowInterval(self, text, duration):
        color = (1, 0, 0, 1)
        track = Sequence(
            Func(self.hide),
            Wait(duration * 0.3),
            Func(self.setColorScale, color),
            Func(self.setText, text),
            Func(self.show),
            LerpScaleInterval(self, 0.2, (1.2), startScale=(0), blendType='easeInOut'),
            LerpScaleInterval(self, 0.09, (1.0), blendType='easeInOut'),
            Wait(duration * 0.7),
            LerpColorScaleInterval(self, 0.25, (1, 0, 0, 0)), Func(self.hide))
        return track

    def getToonsDiedInterval(self, textList, duration):
        track = Sequence(Func(self.hide), Wait(duration * 0.3))
        waitGap = 0.6 / len(textList) * duration
        for text in textList:
            newList = [Func(self.setText, text),
             Func(self.show),
             Wait(waitGap),
             Func(self.hide)]
            track += newList

        track.append(Wait(duration * 0.1))
        return track
