from . import CogHood
from toontown.toonbase import ToontownGlobals
from toontown.coghq import LawbotCogHQLoader
from panda3d.core import Fog

class LawbotHQ(CogHood.CogHood):

    def __init__(self, parentFSM, doneEvent, dnaStore, hoodId):
        CogHood.CogHood.__init__(self, parentFSM, doneEvent, dnaStore, hoodId)
        self.id = ToontownGlobals.LawbotHQ
        self.cogHQLoaderClass = LawbotCogHQLoader.LawbotCogHQLoader
        self.storageDNAFile = None
        self.skyFile = 'phase_9/models/cogHQ/cog_sky'
        self.titleColor = (0.6, 0.65, 0.75, 1.0)
        self.colorScale = (0.88, 0.92, .96, 1)
        return

    def load(self):
        CogHood.CogHood.load(self)
        self.sky.hide()
        self.parentFSM.getStateNamed('LawbotHQ').addChild(self.fsm)
        self.fog = Fog("LBHQ")

    def unload(self):
        self.parentFSM.getStateNamed('LawbotHQ').removeChild(self.fsm)
        del self.cogHQLoaderClass
        CogHood.CogHood.unload(self)

    def enter(self, *args):
        CogHood.CogHood.enter(self, *args)
        localAvatar.setCameraFov(ToontownGlobals.CogHQCameraFov)
        base.camLens.setNearFar(ToontownGlobals.LawbotHQCameraNear, ToontownGlobals.LawbotHQCameraFar)

    def exit(self):
        localAvatar.setCameraFov(ToontownGlobals.DefaultCameraFov)
        base.camLens.setNearFar(ToontownGlobals.DefaultCameraNear, ToontownGlobals.DefaultCameraFar)
        CogHood.CogHood.exit(self)

    def setColorScale(self):
        # colouring render didn't look too great tbh
        # just set it on the skybox
        self.sky.setColorScale(self.colorScale)

    def setFog(self):
        if base.wantFog:
            self.fog.setColor(.15, .18, .26)
            self.fog.setExpDensity(0.0005)
            render.clearFog()
            render.setFog(self.fog)
            self.sky.clearFog()
            self.sky.setFog(self.fog)
