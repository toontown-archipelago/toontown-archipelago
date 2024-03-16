from panda3d.core import *
from direct.interval.IntervalGlobal import *
from toontown.toonbase.ToontownGlobals import *
from direct.directnotify import DirectNotifyGlobal
from . import DistributedBarrelBase


class DistributedAPCheckBarrel(DistributedBarrelBase.DistributedBarrelBase):

    def __init__(self, cr):
        DistributedBarrelBase.DistributedBarrelBase.__init__(self, cr)
        self.locationCheckId = 0

    def loadModel(self):
        super().loadModel()
        self.updateBarrelVisual()

    def updateBarrelVisual(self):

        if self.barrel is None:
            return

        # If we already have the check, make it gray otherwise full color
        if self.getLocationCheckId() in base.localAvatar.getCheckedLocations():
            # This is the code that runs in super().setGrab() to "disable" this barrel for collision checks
            self.ignore(self.uniqueName('entertreasureSphere'))
            self.barrel.setColorScale(0.5, 0.5, 0.5, 1)
        else:
            self.barrel.setColorScale(1, 1, 1, 1)

    def setLocationCheckId(self, locationCheckId):
        self.locationCheckId = locationCheckId
        self.updateBarrelVisual()

    def getLocationCheckId(self):
        return self.locationCheckId

    def applyLabel(self):

        cm = CardMaker('ap-logo-card')
        card = self.gagNode.attachNewNode(cm.generate())

        # (LOOKING AT IT) +RIGHT/-LEFT +BACKINTO/-FORWARDOUT +UP/-DOWN
        card.setPos(-0.9, -.02, -.75)
        card.setScale(1.7)
        card.setTransparency(TransparencyAttrib.MAlpha)
        tex = loader.loadTexture('phase_14/maps/ap_icon.png')
        card.setTexture(tex)

    def setGrab(self, avId):
        DistributedBarrelBase.DistributedBarrelBase.setGrab(self, avId)
