from direct.directnotify import DirectNotifyGlobal
from toontown.battle import BattlePlace
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from toontown.toonbase import ToontownGlobals
from toontown.building import Elevator
from panda3d.core import *
from toontown.coghq import CogHQExterior

class LawbotHQExterior(CogHQExterior.CogHQExterior):
    notify = DirectNotifyGlobal.directNotify.newCategory('LawbotHQExterior')

    def enter(self, requestStatus):
        CogHQExterior.CogHQExterior.enter(self, requestStatus)
        self.loader.hood.setColorScale()
        self.loader.hood.setFog()

    def exit(self):
        CogHQExterior.CogHQExterior.exit(self)
        self.loader.hood.setNoColorScale()
        self.loader.hood.setNoFog()
