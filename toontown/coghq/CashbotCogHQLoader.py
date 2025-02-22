from direct.directnotify import DirectNotifyGlobal
from direct.fsm import StateData
from . import CogHQLoader, MintInterior
from toontown.toonbase import ToontownGlobals
from direct.gui import DirectGui
from toontown.toonbase import TTLocalizer
from toontown.toon import Toon
from direct.fsm import State
from . import CashbotHQExterior
from . import CashbotHQBossBattle
from panda3d.core import DecalEffect, Fog, VirtualFileSystem
from toontown.content_pack import MusicManagerGlobals

class CashbotCogHQLoader(CogHQLoader.CogHQLoader):
    notify = DirectNotifyGlobal.directNotify.newCategory('CashbotCogHQLoader')

    def __init__(self, hood, parentFSMState, doneEvent):
        CogHQLoader.CogHQLoader.__init__(self, hood, parentFSMState, doneEvent)
        self.fsm.addState(State.State('mintInterior', self.enterMintInterior, self.exitMintInterior, ['quietZone', 'cogHQExterior']))
        for stateName in ['start', 'cogHQExterior', 'quietZone']:
            state = self.fsm.getStateNamed(stateName)
            state.addTransition('mintInterior')

        self.cogHQExteriorModelPath = 'phase_10/models/cogHQ/CashBotShippingStation'
        self.cogHQLobbyModelPath = 'phase_10/models/cogHQ/VaultLobby'
        self.geom = None
        return

    def load(self, zoneId):
        CogHQLoader.CogHQLoader.load(self, zoneId)
        Toon.loadCashbotHQAnims()

    def unloadPlaceGeom(self):
        if self.geom:
            self.geom.removeNode()
            self.geom = None
        CogHQLoader.CogHQLoader.unloadPlaceGeom(self)
        return

    def loadPlaceGeom(self, zoneId):
        self.notify.info('loadPlaceGeom: %s' % zoneId)
        zoneId = zoneId - zoneId % 100
        if zoneId == ToontownGlobals.CashbotHQ:
            self.geom = loader.loadModel(self.cogHQExteriorModelPath)

            self.music = MusicManagerGlobals.GLOBALS[zoneId]['music']
            self.battleMusic = MusicManagerGlobals.GLOBALS[zoneId]['battleMusic']

            ddLinkTunnel = self.geom.find('**/LinkTunnel1')
            ddLinkTunnel.setName('linktunnel_dl_9252_DNARoot')
            locator = self.geom.find('**/sign_origin')
            backgroundGeom = self.geom.find('**/EntranceFrameFront')
            backgroundGeom.node().setEffect(DecalEffect.make())
            signText = DirectGui.OnscreenText(text=TTLocalizer.DonaldsDreamland[-1], font=ToontownGlobals.getSuitFont(), scale=3, fg=(0.87, 0.87, 0.87, 1), mayChange=False, parent=backgroundGeom)
            signText.setPosHpr(locator, 0, 0, 0, 0, 0, 0)
            signText.setDepthWrite(0)
        elif zoneId == ToontownGlobals.CashbotLobby:
            if base.config.GetBool('want-qa-regression', 0):
                self.notify.info('QA-REGRESSION: COGHQ: Visit CashbotLobby')
            self.geom = loader.loadModel(self.cogHQLobbyModelPath)

            self.music = MusicManagerGlobals.GLOBALS[zoneId]['music']
            self.battleMusic = MusicManagerGlobals.GLOBALS[zoneId]['music']

            buildings = self.geom.findAllMatches('**/BGBuildings2')
            sky = self.geom.find('**/SkyBox')

            fog = Fog('CBHQLobby')
            fog.setColor(.15, .17, .15)
            fog.setExpDensity(0.00125)

            sky.setColorScale(0.61, 0.65, 0.62, 1)
            sky.setFog(fog)

            for building in buildings:
                building.setColorScale(0.61, 0.65, 0.62, 1)
                building.setFog(fog)
        else:
            self.notify.warning('loadPlaceGeom: unclassified zone %s' % zoneId)
        CogHQLoader.CogHQLoader.loadPlaceGeom(self, zoneId)

    def unload(self):
        CogHQLoader.CogHQLoader.unload(self)
        Toon.unloadCashbotHQAnims()

    def enterMintInterior(self, requestStatus):
        self.placeClass = MintInterior.MintInterior
        self.mintId = requestStatus['mintId']
        self.enterPlace(requestStatus)

    def exitMintInterior(self):
        self.exitPlace()
        self.placeClass = None
        del self.mintId
        return

    def getExteriorPlaceClass(self):
        return CashbotHQExterior.CashbotHQExterior

    def getBossPlaceClass(self):
        return CashbotHQBossBattle.CashbotHQBossBattle
