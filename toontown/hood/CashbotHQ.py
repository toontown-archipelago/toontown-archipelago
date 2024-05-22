from panda3d.core import *
from direct.directnotify import DirectNotifyGlobal
from . import CogHood
from toontown.toonbase import ToontownGlobals, TTLocalizer
from toontown.hood import ZoneUtil
from toontown.coghq import CashbotCogHQLoader

class CashbotHQ(CogHood.CogHood):
    notify = DirectNotifyGlobal.directNotify.newCategory('CashbotHQ')

    def __init__(self, parentFSM, doneEvent, dnaStore, hoodId):
        CogHood.CogHood.__init__(self, parentFSM, doneEvent, dnaStore, hoodId)
        self.id = ToontownGlobals.CashbotHQ
        self.cogHQLoaderClass = CashbotCogHQLoader.CashbotCogHQLoader
        self.storageDNAFile = None
        self.skyFile = 'phase_3.5/models/props/TT_sky'
        self.titleColor = (0.79, 0.94, 0.87, 1.0)
        self.colorScale = (0.61, 0.65, 0.62, 1)
        return

    def load(self):
        CogHood.CogHood.load(self)
        self.parentFSM.getStateNamed('CashbotHQ').addChild(self.fsm)
        self.fog = Fog('CBHQ')

    def unload(self):
        self.parentFSM.getStateNamed('CashbotHQ').removeChild(self.fsm)
        del self.cogHQLoaderClass
        CogHood.CogHood.unload(self)

    def enter(self, *args):
        CogHood.CogHood.enter(self, *args)
        localAvatar.setCameraFov(ToontownGlobals.CogHQCameraFov)
        base.camLens.setNearFar(ToontownGlobals.CashbotHQCameraNear, ToontownGlobals.CashbotHQCameraFar)

    def exit(self):
        localAvatar.setCameraFov(ToontownGlobals.DefaultCameraFov)
        base.camLens.setNearFar(ToontownGlobals.DefaultCameraNear, ToontownGlobals.DefaultCameraFar)
        CogHood.CogHood.exit(self)

    def spawnTitleText(self, zoneId, floorNum = None):
        if ZoneUtil.isMintInteriorZone(zoneId):
            text = '%s\n%s' % (ToontownGlobals.StreetNames[zoneId][-1], TTLocalizer.MintFloorTitle % (floorNum + 1))
            self.doSpawnTitleText(text)
        else:
            CogHood.CogHood.spawnTitleText(self, zoneId)

    def setFog(self):
        if base.wantFog:
            self.fog.setColor(.22, .26, .22)
            self.fog.setExpDensity(0.0003)
            render.clearFog()
            render.setFog(self.fog)
            self.sky.clearFog()
            self.sky.setFog(self.fog)

    def setColorScale(self):
        base.render.setColorScale(self.colorScale)
