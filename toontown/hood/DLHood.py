from panda3d.core import *
from . import ToonHood
from toontown.town import DLTownLoader
from toontown.safezone import DLSafeZoneLoader
from toontown.toonbase.ToontownGlobals import *

class DLHood(ToonHood.ToonHood):

    def __init__(self, parentFSM, doneEvent, dnaStore, hoodId):
        ToonHood.ToonHood.__init__(self, parentFSM, doneEvent, dnaStore, hoodId)
        self.id = DonaldsDreamland
        self.townLoaderClass = DLTownLoader.DLTownLoader
        self.safeZoneLoaderClass = DLSafeZoneLoader.DLSafeZoneLoader
        self.storageDNAFile = 'phase_8/dna/storage_DL.dna'
        self.holidayStorageDNADict = {WINTER_DECORATIONS: ['phase_8/dna/winter_storage_DL.dna'],
         WACKY_WINTER_DECORATIONS: ['phase_8/dna/winter_storage_DL.dna'],
         HALLOWEEN_PROPS: ['phase_8/dna/halloween_props_storage_DL.dna'],
         SPOOKY_PROPS: ['phase_8/dna/halloween_props_storage_DL.dna']}
        self.skyFile = 'phase_8/models/props/DL_sky'
        self.titleColor = (1.0, 0.9, 0.5, 1.0)
        self.colorScale = (0.55, 0.55, 0.65, 1)

    def load(self):
        ToonHood.ToonHood.load(self)
        self.parentFSM.getStateNamed('DLHood').addChild(self.fsm)

        self.fog = Fog('DLFog')

    def setFog(self):
        if base.wantFog:
            self.fog.setColor(0.35, 0.35, 0.45)
            self.fog.setExpDensity(0.00125)
            render.clearFog()
            render.setFog(self.fog)
            self.sky.clearFog()
            self.sky.setFog(self.fog)

    def setColorScale(self):
        render.setColorScale(self.colorScale)

    def unload(self):
        self.parentFSM.getStateNamed('DLHood').removeChild(self.fsm)
        ToonHood.ToonHood.unload(self)

    def enter(self, *args):
        ToonHood.ToonHood.enter(self, *args)

    def exit(self):
        ToonHood.ToonHood.exit(self)
