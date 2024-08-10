import math
from panda3d.core import CardMaker, TransparencyAttrib
from direct.gui.DirectGui import DirectFrame, DirectLabel, DirectButton, OnscreenImage, DGG
from direct.task import Task
from toontown.toon import NPCToons
from toontown.hood import ZoneUtil
from toontown.toonbase import ToontownGlobals
from toontown.quest import Quests
from toontown.suit import SuitPlannerBase
from toontown.suit import SuitDNA
from . import QuestMapGlobals

class QuestMap(DirectFrame):

    def __init__(self, av, **kw):
        DirectFrame.__init__(self, relief=None, sortOrder=50)
        self.initialiseoptions(QuestMap)
        self.setBin('fixed', 0)
        self.container = DirectFrame(parent=self, relief=None)
        self.marker = DirectFrame(parent=self.container, relief=None)
        self.cogInfoFrame = DirectFrame(parent=self.container, relief=None)
        cm = CardMaker('bg')
        cm.setFrame(-0.5, 0.5, -0.5, 0.5)
        bg = self.cogInfoFrame.attachNewNode(cm.generate())
        bg.setTransparency(1)
        bg.setColor(0.5, 0.5, 0.5, 0.5)
        bg.setBin('fixed', 0)
        self.cogInfoFrame['geom'] = bg
        self.cogInfoFrame['geom_pos'] = (0, 0, 0)
        self.cogInfoFrame['geom_scale'] = (6, 1, 2)
        self.cogInfoFrame.setScale(0.05)
        self.cogInfoFrame.setPos(0, 0, 0.6)
        self.buildingMarkers = []
        self.av = av
        self.wantToggle = False
        if base.config.GetBool('want-toggle-quest-map', True):
            self.wantToggle = True
        self.updateMarker = True
        self.cornerPosInfo = None
        self.hqPosInfo = None
        self.fishingSpotInfo = None
        self.load()
        self.setScale(1.5)
        bg.removeNode()
        self.hoodId = None
        self.zoneId = None
        self.suitPercentage = {}
        for currHoodInfo in SuitPlannerBase.SuitPlannerBase.SuitHoodInfo:
            tracks = currHoodInfo[SuitPlannerBase.SuitPlannerBase.SUIT_HOOD_INFO_TRACK]
            self.suitPercentage[currHoodInfo[SuitPlannerBase.SuitPlannerBase.SUIT_HOOD_INFO_ZONE]] = tracks

        return

    def load(self):
        gui = loader.loadModel('phase_4/models/questmap/questmap_gui')
        icon = gui.find('**/tt_t_gui_qst_arrow')
        iconNP = aspect2d.attachNewNode('iconNP')
        icon.reparentTo(iconNP)
        icon.setR(90)
        self.marker['geom'] = iconNP
        self.marker['image'] = iconNP
        self.marker.setScale(0.05)
        iconNP.removeNode()
        self.mapOpenButton = DirectButton(image=(gui.find('**/tt_t_gui_qst_mapClose'), gui.find('**/tt_t_gui_qst_mapClose'), gui.find('**/tt_t_gui_qst_mapTryToOpen')), relief=None, pos=(-0.084, 0, 0.37), parent=base.a2dBottomRight, scale=0.205, command=self.show)
        self.mapCloseButton = DirectButton(image=(gui.find('**/tt_t_gui_qst_mapOpen'), gui.find('**/tt_t_gui_qst_mapOpen'), gui.find('**/tt_t_gui_qst_mapTryToClose')), relief=None, pos=(-0.084, 0, 0.37), parent=base.a2dBottomRight, scale=0.205, command=self.hide)
        self.mapOpenButton.hide()
        self.mapCloseButton.hide()
        gui.removeNode()
        icons = loader.loadModel('phase_3/models/gui/cog_icons')
        cIcon = icons.find('**/CorpIcon')
        lIcon = icons.find('**/LegalIcon')
        mIcon = icons.find('**/MoneyIcon')
        sIcon = icons.find('**/SalesIcon')
        cogInfoTextColor = (0.2, 0.2, 0.2, 1)
        textPos = (1.2, -0.2)
        textScale = 0.8
        self.cInfo = DirectLabel(parent=self.cogInfoFrame, text='', text_fg=cogInfoTextColor, text_pos=textPos, text_scale=textScale, geom=cIcon, geom_pos=(-0.2, 0, 0), geom_scale=0.8, relief=None)
        self.cInfo.setPos(-2.2, 0, 0.5)
        self.lInfo = DirectLabel(parent=self.cogInfoFrame, text_fg=cogInfoTextColor, text='', text_pos=textPos, text_scale=textScale, geom=lIcon, geom_pos=(-0.2, 0, 0), geom_scale=0.8, relief=None)
        self.lInfo.setPos(-2.2, 0, -0.5)
        self.mInfo = DirectLabel(parent=self.cogInfoFrame, text_fg=cogInfoTextColor, text='', text_pos=textPos, text_scale=textScale, geom=mIcon, geom_pos=(-0.2, 0, 0), geom_scale=0.8, relief=None)
        self.mInfo.setPos(0.8, 0, 0.5)
        self.sInfo = DirectLabel(parent=self.cogInfoFrame, text_fg=cogInfoTextColor, text='', text_pos=textPos, text_scale=textScale, geom=sIcon, geom_pos=(-0.2, 0, 0), geom_scale=0.8, relief=None)
        self.sInfo.setPos(0.8, 0, -0.5)
        icons.removeNode()
        return

    def updateCogInfo(self):
        currPercentage = self.suitPercentage.get(self.zoneId)
        if currPercentage is None:
            return
        self.cInfo['text'] = '%s%%' % currPercentage[0]
        self.lInfo['text'] = '%s%%' % currPercentage[1]
        self.mInfo['text'] = '%s%%' % currPercentage[2]
        self.sInfo['text'] = '%s%%' % currPercentage[3]
        return

    def destroy(self):
        self.ignore('questPageUpdated')
        self.mapOpenButton.destroy()
        self.mapCloseButton.destroy()
        del self.mapOpenButton
        del self.mapCloseButton
        DirectFrame.destroy(self)
        
    def putBuildingMarker(self, pos, blockNumber=None, track=None, index=None, floorNumber=None):
        if track:
            marker = DirectButton(parent=self.container, text_pos=(-0.05, -0.65), text_fg=(1, 1, 1, 1), text_scale=0.50, relief=None, clickSound=None, sortOrder=52)
            cm = CardMaker('bg')
            cm.setFrame(-0.05, 0.025, -0.05, 0.05)
            bg = marker.attachNewNode(cm.generate())
            bg.setTransparency(1)
            bg.setColor(0.1, 0.1, 0.1, 0.7)
            bg.setBin('fixed', 1)
            marker.setBin('fixed', 2)
            floorCounter = DirectLabel(parent=marker, relief=None, pos=(0.5, 0.5, -0.25), scale=(1, 1, 1), geom=bg, geom_pos=(0, 0, 0.23), geom_scale=(24.5, 1, 12), text=f'{floorNumber}', textMayChange=0, text_pos=(0.18, 0), text_fg=(1, 1, 1, 1), text_scale=0.75, sortOrder=51)
            icon = self.getIcon(track)
            iconNP = aspect2d.attachNewNode('buildingBlock-%s' % blockNumber)
            icon.reparentTo(iconNP)
            marker['image'] = iconNP
            marker['image_scale'] = 1
            marker.setScale(0.05)
            # Calculate the bounds of the iconNP
            bounds = iconNP.getTightBounds()
            min_bound = bounds[0]
            max_bound = bounds[1]
            # Set the frameSize of the marker to match the bounds of the iconNP
            marker['frameSize'] = (min_bound[0], max_bound[0], min_bound[2], max_bound[2])
            floorCounter.hide()
            marker.bind(DGG.WITHIN, lambda x: floorCounter.show())
            marker.bind(DGG.WITHOUT, lambda x: floorCounter.hide())
            
            relX, relY = self.transformAvPos(pos)
            marker.setPos(relX, 0, relY)
            self.buildingMarkers.append(marker)
            iconNP.removeNode()
        elif index == 'hq':
            marker = DirectLabel(parent=self.container, text='', text_pos=(-0.05, -0.15), text_fg=(1, 1, 1, 1), relief=None)
            icon = self.getIcon(index)
            iconNP = aspect2d.attachNewNode('hq')
            icon.reparentTo(iconNP)
            marker['image'] = iconNP
            marker['image_scale'] = 1
            marker.setScale(0.05)
            relX, relY = self.transformAvPos(pos)
            marker.setPos(relX, 0, relY)
            self.buildingMarkers.append(marker)
            iconNP.removeNode()
        else:
            pass

    def getIcon(self, index):
        icons = loader.loadModel('phase_3/models/gui/cog_icons')
        if index == 'c':
            icon = icons.find('**/CorpIcon')
        elif index == 's':
            icon = icons.find('**/SalesIcon')
        elif index == 'l':
            icon = icons.find('**/LegalIcon')
        elif index == 'm':
            icon = icons.find('**/MoneyIcon')
        elif index == 'hq':
            image = OnscreenImage(image='phase_4/maps/Fire_hat.png', pos=(0, 0, 0))
            image.setScale(0.75)
            image.setTransparency(TransparencyAttrib.MAlpha)
            icon = image
        icons.removeNode()
        return icon

    def updateBuildingInfo(self):
        for marker in self.buildingMarkers:
            marker.destroy()
        for marker in self.buildingMarkers:
            marker.destroy()

        self.buildingMarkers = []
        dnaStore = base.cr.playGame.dnaStore

        self.putBuildingMarker(self.hqPosInfo, index='hq')

        for blockIndex in range(dnaStore.getNumBlockNumbers()):
            blockNumber = dnaStore.getBlockNumberAt(blockIndex)
            blockZoneId = dnaStore.getZoneFromBlockNumber(blockNumber)
            streetId = ZoneUtil.getCanonicalBranchZone(self.av.getLocation()[1])
            zoneIdBlock = blockZoneId + blockNumber
            if dnaStore.isSuitBlock(zoneIdBlock) and (zoneIdBlock in range(streetId, streetId+99)):
                # grab the number of floors for the building
                numFloors = dnaStore.getNumFloors(zoneIdBlock)
                
                self.putBuildingMarker(
                    dnaStore.getDoorPosHprFromBlockNumber(blockNumber).getPos(),
                    zoneIdBlock,
                    track=dnaStore.getSuitBlockTrack(zoneIdBlock),
                    floorNumber=numFloors)
                continue

    def transformAvPos(self, pos):
        if self.cornerPosInfo is None:
            return (0, 0)
        topRight = self.cornerPosInfo[0]
        bottomLeft = self.cornerPosInfo[1]
        relativeX = (pos.getX() - bottomLeft.getX()) / (topRight.getX() - bottomLeft.getX()) - 0.5
        relativeY = (pos.getY() - bottomLeft.getY()) / (topRight.getY() - bottomLeft.getY()) - 0.5
        return (relativeX, relativeY)

    def update(self, task):
        if self.av:
            if self.updateMarker:
                relX, relY = self.transformAvPos(self.av.getPos())
                self.marker.setPos(relX, 0, relY)
                self.marker.setHpr(0, 0, -180 - self.av.getH())

        for buildingMarker in self.buildingMarkers:
            i = self.buildingMarkers.index(buildingMarker)
            if not buildingMarker.isEmpty():
                buildingMarker.setScale((math.sin(task.time + i * math.pi / 3.0) + 1) * 0.005 + 0.04)
        return Task.cont

    def updateMap(self):
        if self.av:
            try:
                hoodId = ZoneUtil.getCanonicalHoodId(self.av.getLocation()[1])
                zoneId = ZoneUtil.getCanonicalBranchZone(self.av.getLocation()[1])
                if hoodId in ToontownGlobals.dnaPGMap:
                    mapsGeom = loader.loadModel('phase_4/models/questmap/%s_maps' % ToontownGlobals.dnaPGMap[hoodId])
                    mapImage = mapsGeom.find('**/%s_%s_english' % (ToontownGlobals.dnaMap[hoodId], zoneId))
                else:
                    self.stop()
                    return
                if not mapImage.isEmpty():
                    self.container['image'] = mapImage
                    self.resetFrameSize()
                    self.cornerPosInfo = QuestMapGlobals.CornerPosTable.get('%s_%s_english' % (ToontownGlobals.dnaMap[hoodId], zoneId))
                    self.hqPosInfo = QuestMapGlobals.HQPosTable.get('%s_%s_english' % (ToontownGlobals.dnaMap[hoodId], zoneId))
                    self.fishingSpotInfo = QuestMapGlobals.FishingSpotPosTable.get('%s_%s_english' % (ToontownGlobals.dnaMap[hoodId], zoneId))
                    self.cogInfoPos = QuestMapGlobals.CogInfoPosTable.get('%s_%s_english' % (ToontownGlobals.dnaMap[hoodId], zoneId))
                    self.cogInfoFrame.setPos(self.cogInfoPos)
                    self.hide()
                    self.hoodId = hoodId
                    self.zoneId = zoneId
                    self.updateBuildingInfo()
                    self.updateCogInfo()
                    taskMgr.add(self.update, 'questMapUpdate')
                else:
                    self.stop()
                mapsGeom.removeNode()
            except OSError:
                self.stop()
                return

    def start(self):
        self.container.show()
        self.accept('questPageUpdated', self.updateMap)
        self.handleMarker()

    def initMarker(self, task):
        if self.av:
            if not hasattr(base.cr.playGame.getPlace(), 'isInterior') or not base.cr.playGame.getPlace().isInterior:
                relX, relY = self.transformAvPos(self.av.getPos())
                self.marker.setPos(relX, 0, relY)
                self.marker.setHpr(0, 0, -180 - self.av.getH())
            self.marker['geom_scale'] = 1.4 * task.time % 0.5 * 10 + 1
            self.marker['geom_color'] = (1,
             1,
             1,
             0.8 - 1.4 * task.time % 0.5 * 2 / 0.8 + 0.2)
        if task.time < 1:
            return Task.cont
        else:
            self.marker['geom_color'] = (1, 1, 1, 0)
            return Task.done

    def show(self):
        taskMgr.add(self.initMarker, 'questMapInit')
        DirectFrame.show(self)
        self.mapOpenButton.hide()
        if self.container['image']:
            self.mapCloseButton.show()

    def hide(self):
        taskMgr.remove('questMapInit')
        DirectFrame.hide(self)
        if self.container['image']:
            self.mapOpenButton.show()
        self.mapCloseButton.hide()

    def toggle(self):
        if self.isHidden():
            self.show()
        else:
            self.hide()

    def obscureButton(self):
        self.mapOpenButton.hide()
        self.mapCloseButton.hide()

    def stop(self):
        self.container['image'] = None

        for marker in self.buildingMarkers:
            marker.destroy()
        for marker in self.buildingMarkers:
            marker.destroy()

        self.buildingMarkers = []
        self.container.hide()
        self.hide()
        self.obscureButton()
        self.ignore('questPageUpdated')
        taskMgr.remove('questMapUpdate')
        return

    def handleMarker(self):
        if hasattr(base.cr.playGame.getPlace(), 'isInterior') and base.cr.playGame.getPlace().isInterior:
            self.updateMarker = False
        else:
            self.updateMarker = True

    def acceptOnscreenHooks(self):
        self.accept(ToontownGlobals.MapHotkey, self.toggle)
        self.updateMap()

    def ignoreOnscreenHooks(self):
        self.ignore(ToontownGlobals.MapHotkey)
        self.obscureButton()
