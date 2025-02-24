from direct.interval.IntervalGlobal import *
from panda3d.core import *

from toontown.battle.BattlePlace import BattlePlace
from toontown.toonbase.ToonBaseGlobal import *
from direct.directnotify import DirectNotifyGlobal
from toontown.hood import Place
from direct.showbase import DirectObject
from direct.fsm import StateData
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from direct.task import Task
from toontown.toon import DeathForceAcknowledge
from toontown.toon import HealthForceAcknowledge
from toontown.tutorial import TutorialForceAcknowledge
from toontown.toon import NPCForceAcknowledge
from toontown.trolley import Trolley
from toontown.toontowngui import TTDialog
from toontown.toonbase import ToontownGlobals
from toontown.toon.Toon import teleportDebug
from toontown.toonbase import TTLocalizer
from direct.gui import DirectLabel
from otp.distributed.TelemetryLimiter import RotationLimitToH, TLGatherAllAvs

class Playground(BattlePlace):
    notify = DirectNotifyGlobal.directNotify.newCategory('Playground')

    def __init__(self, loader, parentFSM, doneEvent):
        super().__init__(loader, doneEvent)
        self.tfaDoneEvent = 'tfaDoneEvent'
        self.fsm = ClassicFSM.ClassicFSM('Playground', [
            State.State('start',
                        self.enterStart,
                        self.exitStart, [
                            'walk',
                            'deathAck',
                            'doorIn',
                            'tunnelIn']),
            State.State('walk',
                        self.enterWalk,
                        self.exitWalk, [
                            'drive',
                            'sit',
                            'stickerBook',
                            'TFA',
                            'DFA',
                            'trialerFA',
                            'trolley',
                            'final',
                            'doorOut',
                            'options',
                            'quest',
                            'purchase',
                            'stopped',
                            'fishing',
                            'battle',
                            'teleportOut']),
            State.State('stickerBook',
                        self.enterStickerBook,
                        self.exitStickerBook, [
                            'walk',
                            'DFA',
                            'TFA',
                            'trolley',
                            'final',
                            'doorOut',
                            'quest',
                            'purchase',
                            'stopped',
                            'fishing',
                            'trialerFA']),
            State.State('sit',
                        self.enterSit,
                        self.exitSit, [
                            'walk',
                            'DFA',
                            'trialerFA']),
            State.State('drive',
                        self.enterDrive,
                        self.exitDrive, [
                            'walk',
                            'DFA',
                            'trialerFA']),
            State.State('trolley',
                        self.enterTrolley,
                        self.exitTrolley, [
                            'walk']),
            State.State('doorIn',
                        self.enterDoorIn,
                        self.exitDoorIn, [
                            'walk']),
            State.State('doorOut',
                        self.enterDoorOut,
                        self.exitDoorOut, [
                            'walk']),
            State.State('TFA',
                        self.enterTFA,
                        self.exitTFA, [
                            'TFAReject',
                            'DFA']),
            State.State('TFAReject',
                        self.enterTFAReject,
                        self.exitTFAReject, [
                            'walk']),
            State.State('trialerFA',
                        self.enterTrialerFA,
                        self.exitTrialerFA, [
                            'trialerFAReject',
                            'DFA']),
            State.State('trialerFAReject',
                        self.enterTrialerFAReject,
                        self.exitTrialerFAReject, [
                            'walk']),
            State.State('DFA',
                        self.enterDFA,
                        self.exitDFA, [
                            'DFAReject',
                            'NPCFA',
                            'HFA']),
            State.State('DFAReject',
                        self.enterDFAReject,
                        self.exitDFAReject, [
                            'walk']),
            State.State('NPCFA',
                        self.enterNPCFA,
                        self.exitNPCFA, [
                            'NPCFAReject',
                            'HFA']),
            State.State('NPCFAReject',
                        self.enterNPCFAReject,
                        self.exitNPCFAReject, [
                            'walk']),
            State.State('HFA',
                        self.enterHFA,
                        self.exitHFA, [
                            'HFAReject',
                            'teleportOut',
                            'tunnelOut']),
            State.State('HFAReject',
                        self.enterHFAReject,
                        self.exitHFAReject, [
                            'walk']),
            State.State('deathAck',
                        self.enterDeathAck,
                        self.exitDeathAck, [
                            'teleportIn']),
            State.State('teleportIn',
                        self.enterTeleportIn,
                        self.exitTeleportIn, [
                            'walk',
                            'popup']),
            State.State('popup',
                        self.enterPopup,
                        self.exitPopup, [
                            'walk']),
            State.State('teleportOut',
                        self.enterTeleportOut,
                        self.exitTeleportOut, [
                            'deathAck',
                            'teleportIn']),
            State.State('died',
                        self.enterDied,
                        self.exitDied, [
                            'final']),
            State.State('tunnelIn',
                        self.enterTunnelIn,
                        self.exitTunnelIn, [
                            'walk']),
            State.State('tunnelOut',
                        self.enterTunnelOut,
                        self.exitTunnelOut, [
                            'final']),
            State.State('quest',
                        self.enterQuest,
                        self.exitQuest, [
                            'walk']),
            State.State('purchase',
                        self.enterPurchase,
                        self.exitPurchase, [
                            'walk']),
            State.State('stopped',
                        self.enterStopped,
                        self.exitStopped, [
                            'walk']),
            State.State('fishing',
                        self.enterFishing,
                        self.exitFishing, [
                            'walk']),
            State.State('battle', self.enterBattle, self.exitBattle, ['walk', 'teleportOut', 'died']),
            State.State('WaitForBattle', self.enterWaitForBattle, self.exitWaitForBattle, ['battle', 'walk']),
            State.State('final',
                        self.enterFinal,
                        self.exitFinal, [
                            'start'])],
            'start', 'final')
        self.parentFSM = parentFSM
        self.tunnelOriginList = []
        self.trolleyDoneEvent = 'trolleyDone'
        self.hfaDoneEvent = 'hfaDoneEvent'
        self.npcfaDoneEvent = 'npcfaDoneEvent'
        self.dialog = None
        self.deathAckBox = None
        return

    def enter(self, requestStatus):
        self.fsm.enterInitialState()
        messenger.send('enterPlayground')
        self.accept('doorDoneEvent', self.handleDoorDoneEvent)
        self.accept('DistributedDoor_doorTrigger', self.handleDoorTrigger)
        base.contentPackMusicManager.playMusic(self.loader.music, looping=True, interrupt=True, volume=0.8)
        self.loader.geom.reparentTo(render)
        for i in self.loader.nodeList:
            self.loader.enterAnimatedProps(i)

        self._telemLimiter = TLGatherAllAvs('Playground', RotationLimitToH)

        def __lightDecorationOn__():
            geom = base.cr.playGame.hood.loader.geom
            self.loader.hood.halloweenLights = geom.findAllMatches('**/*light*')
            self.loader.hood.halloweenLights += geom.findAllMatches('**/*lamp*')
            self.loader.hood.halloweenLights += geom.findAllMatches('**/prop_snow_tree*')
            for light in self.loader.hood.halloweenLights:
                light.setColorScaleOff(0)

        newsManager = base.cr.newsManager
        if newsManager:
            holidayIds = base.cr.newsManager.getDecorationHolidayId()
            if (ToontownGlobals.HALLOWEEN_COSTUMES in holidayIds or ToontownGlobals.SPOOKY_COSTUMES in holidayIds) and self.loader.hood.spookySkyFile:
                lightsOff = Sequence(LerpColorScaleInterval(base.cr.playGame.hood.loader.geom, 0.1, Vec4(0.55, 0.55, 0.65, 1)), Func(self.loader.hood.startSpookySky), Func(__lightDecorationOn__))
                lightsOff.start()
            else:
                self.loader.hood.startSky()
                lightsOn = LerpColorScaleInterval(base.cr.playGame.hood.loader.geom, 0.1, Vec4(1, 1, 1, 1))
                lightsOn.start()
        else:
            self.loader.hood.startSky()
            lightsOn = LerpColorScaleInterval(base.cr.playGame.hood.loader.geom, 0.1, Vec4(1, 1, 1, 1))
            lightsOn.start()
        NametagGlobals.setMasterArrowsOn(1)
        self.zoneId = requestStatus['zoneId']
        self.tunnelOriginList = base.cr.hoodMgr.addLinkTunnelHooks(self, self.loader.nodeList, self.zoneId)
        how = requestStatus['how']
        if how == 'teleportIn':
            how = 'deathAck'
        self.fsm.request(how, [requestStatus])

    def exit(self):
        self.ignoreAll()
        messenger.send('exitPlayground')
        self._telemLimiter.destroy()
        del self._telemLimiter
        for node in self.tunnelOriginList:
            node.removeNode()

        del self.tunnelOriginList
        self.loader.geom.reparentTo(hidden)

        def __lightDecorationOff__():
            for light in self.loader.hood.halloweenLights:
                light.reparentTo(hidden)

        newsManager = base.cr.newsManager
        NametagGlobals.setMasterArrowsOn(0)
        for i in self.loader.nodeList:
            self.loader.exitAnimatedProps(i)

        self.loader.hood.stopSky()
        base.contentPackMusicManager.stopMusic()

    def load(self):
        Place.Place.load(self)
        self.parentFSM.getStateNamed('playground').addChild(self.fsm)

    def unload(self):
        self.parentFSM.getStateNamed('playground').removeChild(self.fsm)
        del self.parentFSM
        del self.fsm
        if self.dialog:
            self.dialog.cleanup()
            self.dialog = None
        if self.deathAckBox:
            self.deathAckBox.cleanup()
            self.deathAckBox = None
        TTDialog.cleanupDialog('globalDialog')
        self.ignoreAll()
        Place.Place.unload(self)
        return

    def showTreasurePoints(self, points):
        self.hideDebugPointText()
        for i in range(len(points)):
            p = points[i]
            self.showDebugPointText(str(i), p)

    def showDropPoints(self, points):
        self.hideDebugPointText()
        for i in range(len(points)):
            p = points[i]
            self.showDebugPointText(str(i), p)

    def showPaths(self):
        pass

    def hidePaths(self):
        self.hideDebugPointText()

    def hideDebugPointText(self):
        if hasattr(self, 'debugText'):
            children = self.debugText.getChildren()
            for i in range(children.getNumPaths()):
                children[i].removeNode()

    def showDebugPointText(self, text, point):
        if not hasattr(self, 'debugText'):
            self.debugText = self.loader.geom.attachNewNode('debugText')
            self.debugTextNode = TextNode('debugTextNode')
            self.debugTextNode.setTextColor(1, 0, 0, 1)
            self.debugTextNode.setAlign(TextNode.ACenter)
            self.debugTextNode.setFont(ToontownGlobals.getSignFont())
        self.debugTextNode.setText(text)
        np = self.debugText.attachNewNode(self.debugTextNode.generate())
        np.setPos(point[0], point[1], point[2])
        np.setScale(4.0)
        np.setBillboardPointEye()

    def enterTrolley(self):
        base.localAvatar.laffMeter.start()
        base.localAvatar.b_setAnimState('off', 1)
        base.localAvatar.cantLeaveGame = 1
        self.accept(self.trolleyDoneEvent, self.handleTrolleyDone)
        self.trolley = Trolley.Trolley(self, self.fsm, self.trolleyDoneEvent)
        self.trolley.load()
        self.trolley.enter()

    def exitTrolley(self):
        base.localAvatar.laffMeter.stop()
        base.localAvatar.cantLeaveGame = 0
        self.ignore(self.trolleyDoneEvent)
        self.trolley.unload()
        self.trolley.exit()
        del self.trolley

    def detectedTrolleyCollision(self):
        self.fsm.request('trolley')

    def handleTrolleyDone(self, doneStatus):
        self.notify.debug('handling trolley done event')
        mode = doneStatus['mode']
        if mode == 'reject':
            self.fsm.request('walk')
        elif mode == 'exit':
            self.fsm.request('walk')
        elif mode == 'minigame':
            self.doneStatus = {'loader': 'minigame',
             'where': 'minigame',
             'hoodId': self.loader.hood.id,
             'zoneId': doneStatus['zoneId'],
             'shardId': None,
             'minigameId': doneStatus['minigameId']}
            messenger.send(self.doneEvent)
        else:
            self.notify.error('Unknown mode: ' + mode + ' in handleTrolleyDone')
        return

    def debugStartMinigame(self, zoneId, minigameId):
        self.doneStatus = {'loader': 'minigame',
         'where': 'minigame',
         'hoodId': self.loader.hood.id,
         'zoneId': zoneId,
         'shardId': None,
         'minigameId': minigameId}
        messenger.send(self.doneEvent)
        return

    def enterTFACallback(self, requestStatus, doneStatus):
        self.tfa.exit()
        del self.tfa
        doneStatusMode = doneStatus['mode']
        if doneStatusMode == 'complete':
            self.requestLeave(requestStatus)
        elif doneStatusMode == 'incomplete':
            self.fsm.request('TFAReject')
        else:
            self.notify.error('Unknown mode: %s' % doneStatusMode)

    def enterDFACallback(self, requestStatus, doneStatus):
        self.dfa.exit()
        del self.dfa
        ds = doneStatus['mode']
        if ds == 'complete':
            self.fsm.request('NPCFA', [requestStatus])
        elif ds == 'incomplete':
            self.fsm.request('DFAReject')
        else:
            self.notify.error('Unknown done status for DownloadForceAcknowledge: ' + repr(doneStatus))

    def enterHFA(self, requestStatus):
        self.acceptOnce(self.hfaDoneEvent, self.enterHFACallback, [requestStatus])
        self.hfa = HealthForceAcknowledge.HealthForceAcknowledge(self.hfaDoneEvent)
        self.hfa.enter(1)

    def exitHFA(self):
        self.ignore(self.hfaDoneEvent)

    def enterHFACallback(self, requestStatus, doneStatus):
        self.hfa.exit()
        del self.hfa
        if doneStatus['mode'] == 'complete':
            if requestStatus.get('partyHat', 0):
                outHow = {'teleportIn': 'tunnelOut'}
            else:
                outHow = {'teleportIn': 'teleportOut',
                 'tunnelIn': 'tunnelOut',
                 'doorIn': 'doorOut'}
            self.fsm.request(outHow[requestStatus['how']], [requestStatus])
        elif doneStatus['mode'] == 'incomplete':
            self.fsm.request('HFAReject')
        else:
            self.notify.error('Unknown done status for HealthForceAcknowledge: ' + repr(doneStatus))

    def enterHFAReject(self):
        self.fsm.request('walk')

    def exitHFAReject(self):
        pass

    def enterNPCFA(self, requestStatus):
        self.acceptOnce(self.npcfaDoneEvent, self.enterNPCFACallback, [requestStatus])
        self.npcfa = NPCForceAcknowledge.NPCForceAcknowledge(self.npcfaDoneEvent)
        self.npcfa.enter()

    def exitNPCFA(self):
        self.ignore(self.npcfaDoneEvent)

    def enterNPCFACallback(self, requestStatus, doneStatus):
        self.npcfa.exit()
        del self.npcfa
        if doneStatus['mode'] == 'complete':
            self.fsm.request('HFA', [requestStatus])
        elif doneStatus['mode'] == 'incomplete':
            self.fsm.request('NPCFAReject')
        else:
            self.notify.error('Unknown done status for NPCForceAcknowledge: ' + repr(doneStatus))

    def enterNPCFAReject(self):
        self.fsm.request('walk')

    def exitNPCFAReject(self):
        pass

    def enterWalk(self, teleportIn = 0):
        if self.deathAckBox:
            self.ignore('deathAck')
            self.deathAckBox.cleanup()
            self.deathAckBox = None
        Place.Place.enterWalk(self, teleportIn)
        return

    def enterDeathAck(self, requestStatus):
        self.deathAckBox = None
        self.fsm.request('teleportIn', [requestStatus])
        return

    def exitDeathAck(self):
        if self.deathAckBox:
            self.ignore('deathAck')
            self.deathAckBox.cleanup()
            self.deathAckBox = None
        return

    def enterTeleportIn(self, requestStatus):
        imgScale = 0.25
        x, y, z, h, p, r = base.cr.hoodMgr.getPlaygroundCenterFromId(self.loader.hood.id)

        if base.localAvatar.hp < 1:
            requestStatus['nextState'] = 'popup'
            self.accept('deathAck', self.__handleDeathAck, extraArgs=[requestStatus])
            self.deathAckBox = DeathForceAcknowledge.DeathForceAcknowledge(doneEvent='deathAck')
        else:
            requestStatus['nextState'] = 'walk'

        base.localAvatar.detachNode()
        base.localAvatar.setPosHpr(render, x, y, z, h, p, r)
        Place.Place.enterTeleportIn(self, requestStatus)
        return

    def __cleanupDialog(self, value):
        if self.dialog:
            self.dialog.cleanup()
            self.dialog = None
        if hasattr(self, 'fsm'):
            self.fsm.request('walk', [1])
        return

    def __handleDeathAck(self, requestStatus):
        if self.deathAckBox:
            self.ignore('deathAck')
            self.deathAckBox.cleanup()
            self.deathAckBox = None
        self.fsm.request('walk', [1])
        return

    def enterPopup(self, teleportIn = 0):
        if base.localAvatar.hp < 1:
            base.localAvatar.b_setAnimState('Sad', 1)
        else:
            base.localAvatar.b_setAnimState('neutral', 1.0)
        self.accept('teleportQuery', self.handleTeleportQuery)
        base.localAvatar.setTeleportAvailable(1)
        base.localAvatar.startSleepWatch(self.__handleFallingAsleepPopup)

    def exitPopup(self):
        base.localAvatar.stopSleepWatch()
        base.localAvatar.setTeleportAvailable(0)
        self.ignore('teleportQuery')

    def __handleFallingAsleepPopup(self, task):
        if hasattr(self, 'fsm'):
            self.fsm.request('walk')
            base.localAvatar.forceGotoSleep()
        return Task.done

    def enterTeleportOut(self, requestStatus):
        Place.Place.enterTeleportOut(self, requestStatus, self.__teleportOutDone)

    def __teleportOutDone(self, requestStatus):
        teleportDebug(requestStatus, 'Playground.__teleportOutDone(%s)' % (requestStatus,))
        if hasattr(self, 'activityFsm'):
            self.activityFsm.requestFinalState()
        hoodId = requestStatus['hoodId']
        zoneId = requestStatus['zoneId']
        avId = requestStatus['avId']
        shardId = requestStatus['shardId']
        if hoodId == self.loader.hood.hoodId and zoneId == self.loader.hood.hoodId and shardId == None:
            teleportDebug(requestStatus, 'same playground')
            self.fsm.request('deathAck', [requestStatus])
        elif hoodId == ToontownGlobals.MyEstate:
            teleportDebug(requestStatus, 'estate')
            self.getEstateZoneAndGoHome(requestStatus)
        else:
            teleportDebug(requestStatus, 'different hood/zone')
            self.doneStatus = requestStatus
            messenger.send(self.doneEvent)
        return

    def exitTeleportOut(self):
        Place.Place.exitTeleportOut(self)

    def createPlayground(self, dnaFile):
        loader.loadDNAFile(self.loader.dnaStore, self.safeZoneStorageDNAFile)
        node = loader.loadDNAFile(self.loader.dnaStore, dnaFile)
        if node.getNumParents() == 1:
            self.geom = NodePath(node.getParent(0))
            self.geom.reparentTo(hidden)
        else:
            self.geom = hidden.attachNewNode(node)
        self.makeDictionaries(self.loader.dnaStore)
        self.tunnelOriginList = base.cr.hoodMgr.addLinkTunnelHooks(self, self.nodeList, self.zoneId)
        self.geom.flattenMedium()
        gsg = base.win.getGsg()
        if gsg:
            self.geom.prepareScene(gsg)

    def makeDictionaries(self, dnaStore):
        self.nodeList = []
        for i in range(dnaStore.getNumDNAVisGroups()):
            groupFullName = dnaStore.getDNAVisGroupName(i)
            groupName = base.cr.hoodMgr.extractGroupName(groupFullName)
            groupNode = self.geom.find('**/' + groupFullName)
            if groupNode.isEmpty():
                self.notify.error('Could not find visgroup')
            self.nodeList.append(groupNode)

        self.removeLandmarkBlockNodes()
        self.loader.dnaStore.resetPlaceNodes()
        self.loader.dnaStore.resetDNAGroups()
        self.loader.dnaStore.resetDNAVisGroups()
        self.loader.dnaStore.resetDNAVisGroupsAI()

    def removeLandmarkBlockNodes(self):
        npc = self.geom.findAllMatches('**/suit_building_origin')
        for i in range(npc.getNumPaths()):
            npc.getPath(i).removeNode()

    def enterTFA(self, requestStatus):
        self.acceptOnce(self.tfaDoneEvent, self.enterTFACallback, [requestStatus])
        self.tfa = TutorialForceAcknowledge.TutorialForceAcknowledge(self.tfaDoneEvent)
        self.tfa.enter()

    def exitTFA(self):
        self.ignore(self.tfaDoneEvent)

    def enterTFAReject(self):
        self.fsm.request('walk')

    def exitTFAReject(self):
        pass
