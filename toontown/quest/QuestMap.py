import math
from panda3d.core import CardMaker, TextNode, Point3
from direct.gui.DirectGui import DirectFrame, DirectLabel, DirectButton
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
        self.suitBuildingMarkers = []
        self.questBlocks = []
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

    def putBuildingMarker(self, pos, mapIndex = None, isSuitBlock = False):
        marker = DirectLabel(parent=self.container, text='', text_pos=(-0.05, -0.15), text_fg=(1, 1, 1, 1), relief=None)
        gui = loader.loadModel('phase_4/models/parties/schtickerbookHostingGUI')
        icon = gui.find('**/startPartyButton_inactive')
        iconNP = aspect2d.attachNewNode('iconNP')
        icon.reparentTo(iconNP)
        icon.setX(-12.0792 / 30.48)
        icon.setZ(-9.7404 / 30.48)
        marker['text'] = '%s' % mapIndex
        marker['text_scale'] = 0.7
        marker['image'] = iconNP
        if isSuitBlock: # Make the bubble appear gray if a cog took over a task building
            marker['image_color'] = (0.5, 0.5, 0.5, 1)
        else:
            marker['image_color'] = (1, 0, 0, 1)
        marker['image_scale'] = 6
        marker.setScale(0.05)
        relX, relY = self.transformAvPos(pos)
        marker.setPos(relX, 0, relY)
        self.buildingMarkers.append(marker)
        iconNP.removeNode()
        gui.removeNode()

    def putSuitBuildingMarker(self, pos, blockNumber = None, track = None):
        if base.localAvatar.buildingRadar[SuitDNA.suitDepts.index(track)]:
            marker = DirectLabel(parent = self.container, text = '', text_pos = (-0.05, -0.15), text_fg = (1, 1, 1, 1),  relief = None)
            icon = self.getSuitIcon(track)
            iconNP = aspect2d.attachNewNode('suitBlock-%s' % blockNumber)
            icon.reparentTo(iconNP)
            marker['image'] = iconNP
            marker['image_scale'] = 1
            marker.setScale(0.05)
            relX, relY = self.transformAvPos(pos)
            marker.setPos(relX, 0, relY)
            self.suitBuildingMarkers.append(marker)
            iconNP.removeNode()
        else:
            pass

    def getSuitIcon(self, dept):
        icons = loader.loadModel('phase_3/models/gui/cog_icons')
        if dept == 'c':
            corpIcon = icons.find('**/CorpIcon')
        elif dept == 's':
            corpIcon = icons.find('**/SalesIcon')
        elif dept == 'l':
            corpIcon = icons.find('**/LegalIcon')
        elif dept == 'm':
            corpIcon = icons.find('**/MoneyIcon')
        else:
            corpIcon = None
        icons.removeNode()
        return corpIcon

    def updateQuestInfo(self):
        for marker in self.buildingMarkers:
            marker.destroy()

        self.buildingMarkers = []
        self.questBlocks = []
        zoneIdList = []
        streetIdList = []
        dnaStore = base.cr.playGame.dnaStore

        for zoneId, streetId in ToontownGlobals.HoodHierarchy.items():
            zoneIdList.append(zoneId)
            streetIdList.append(streetId)

        for (i, questDesc) in enumerate(self.av.quests):
            i += 1
            quest = Quests.getQuest(questDesc[0])
            toNpcId = questDesc[2]
            if quest is None:
                return

            completed = quest.getCompletionStatus(self.av, questDesc) == Quests.COMPLETE
            if not completed:
                if quest.getType() == Quests.RecoverItemQuest:
                    if quest.getHolder() == Quests.AnyFish:
                        self.putBuildingMarker(self.fishingSpotInfo, mapIndex=i)
                    continue
                elif quest.getType() not in (
                    Quests.DeliverGagQuest, Quests.DeliverItemQuest,
                    Quests.VisitQuest, Quests.TrackChoiceQuest):
                    continue

            if toNpcId == Quests.ToonHQ:
                self.putBuildingMarker(self.hqPosInfo, mapIndex=i)

            npcZoneId = NPCToons.getNPCZone(toNpcId)
            hoodId = ZoneUtil.getCanonicalHoodId(npcZoneId)
            branchId = ZoneUtil.getCanonicalBranchZone(npcZoneId)

            if self.hoodId == hoodId and self.zoneId == branchId:
                for blockIndex in range(dnaStore.getNumBlockNumbers()):
                    blockNumber = dnaStore.getBlockNumberAt(blockIndex)
                    zoneId = dnaStore.getZoneFromBlockNumber(blockNumber)
                    zoneIdBlock = zoneId + blockNumber
                    interiorZoneId = (zoneId - (zoneId%100)) + 500 + blockNumber
                    if npcZoneId == interiorZoneId:
                        self.questBlocks.append(zoneIdBlock)
                        self.putBuildingMarker(
                            dnaStore.getDoorPosHprFromBlockNumber(zoneIdBlock).getPos(),
                            mapIndex=i,
                            isSuitBlock=dnaStore.isSuitBlock(zoneIdBlock))
                        continue

        for blockIndex in range(dnaStore.getNumBlockNumbers()):
            blockNumber = dnaStore.getBlockNumberAt(blockIndex)
            blockZoneId = dnaStore.getZoneFromBlockNumber(blockNumber)
            streetId = ZoneUtil.getCanonicalBranchZone(self.av.getLocation()[1])
            zoneIdBlock = blockZoneId + blockNumber
            print(streetId)
            if dnaStore.isSuitBlock(zoneIdBlock) and (zoneIdBlock in range(streetId, streetId+99)) and blockNumber not in self.questBlocks:
                print(zoneIdBlock)
                self.putSuitBuildingMarker(
                    dnaStore.getDoorPosHprFromBlockNumber(blockNumber).getPos(),
                    zoneIdBlock,
                    dnaStore.getSuitBlockTrack(zoneIdBlock))
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
                buildingMarker.setScale((math.sin(task.time * 6.0 + i * math.pi / 3.0) + 1) * 0.005 + 0.04)
        for buildingMarker in self.suitBuildingMarkers:
            i = self.suitBuildingMarkers.index(buildingMarker)
            if not buildingMarker.isEmpty():
                buildingMarker.setScale((math.sin(task.time + i * math.pi / 3.0) + 1) * 0.005 + 0.04)
        return Task.cont

    def updateMap(self):
        if self.av:
            try:
                hoodId = ZoneUtil.getCanonicalHoodId(self.av.getLocation()[1])
                zoneId = ZoneUtil.getCanonicalBranchZone(self.av.getLocation()[1])
                mapsGeom = loader.loadModel('phase_4/models/questmap/%s_maps' % ToontownGlobals.dnaMap[hoodId])
                mapImage = mapsGeom.find('**/%s_%s_english' % (ToontownGlobals.dnaMap[hoodId], zoneId))
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
                    self.updateQuestInfo()
                    self.updateCogInfo()
                    taskMgr.add(self.update, 'questMapUpdate')
                else:
                    self.stop()
                mapsGeom.removeNode()
            except:
                self.stop()
                raise

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
        for marker in self.suitBuildingMarkers:
            marker.destroy()

        self.buildingMarkers = []
        self.suitBuildingMarkers = []
        self.questBlocks = []
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
