from panda3d.core import *
from . import Playground
import random

class DLPlayground(Playground.Playground):

    def __init__(self, loader, parentFSM, doneEvent):
        Playground.Playground.__init__(self, loader, parentFSM, doneEvent)
        
    def enter(self, requestStatus):
        self.loader.hood.setColorScale()
        self.loader.hood.setFog()
        Playground.Playground.enter(self, requestStatus)

    def exit(self):
        self.loader.hood.setNoColorScale()
        self.loader.hood.setNoFog()
        Playground.Playground.exit(self)

    def showPaths(self):
        from toontown.toonbase import TTLocalizer
