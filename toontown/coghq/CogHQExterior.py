from direct.directnotify import DirectNotifyGlobal
from toontown.battle import BattlePlace
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from toontown.toonbase import ToontownGlobals
from toontown.hood import ZoneUtil
from panda3d.core import *
from panda3d.toontown import *
from libotp import *
from otp.distributed.TelemetryLimiter import RotationLimitToH, TLGatherAllAvs
from toontown.content_pack import MusicManagerGlobals

class CogHQExterior(BattlePlace.BattlePlace):
    notify = DirectNotifyGlobal.directNotify.newCategory('CogHQExterior')

    def __init__(self, loader, parentFSM, doneEvent):
        BattlePlace.BattlePlace.__init__(self, loader, doneEvent)
        self.parentFSM = parentFSM
        self.fsm = ClassicFSM.ClassicFSM('CogHQExterior', [State.State('start', self.enterStart, self.exitStart, ['walk',
          'tunnelIn',
          'teleportIn',
          'doorIn']),
         State.State('walk', self.enterWalk, self.exitWalk, ['stickerBook',
          'teleportOut',
          'tunnelOut',
          'DFA',
          'doorOut',
          'died',
          'stopped',
          'WaitForBattle',
          'battle',
          'squished',
          'purchase',
          'stopped']),
         State.State('stopped', self.enterStopped, self.exitStopped, ['walk', 'teleportOut', 'stickerBook']),
         State.State('doorIn', self.enterDoorIn, self.exitDoorIn, ['walk', 'stopped']),
         State.State('doorOut', self.enterDoorOut, self.exitDoorOut, ['walk', 'stopped']),
         State.State('stickerBook', self.enterStickerBook, self.exitStickerBook, ['walk',
          'DFA',
          'WaitForBattle',
          'battle',
          'tunnelOut',
          'doorOut',
          'squished',
          'purchase',
          'died']),
         State.State('WaitForBattle', self.enterWaitForBattle, self.exitWaitForBattle, ['battle', 'walk']),
         State.State('battle', self.enterBattle, self.exitBattle, ['walk', 'teleportOut', 'died']),
         State.State('DFA', self.enterDFA, self.exitDFA, ['DFAReject', 'teleportOut', 'tunnelOut']),
         State.State('DFAReject', self.enterDFAReject, self.exitDFAReject, ['walk']),
         State.State('squished', self.enterSquished, self.exitSquished, ['walk', 'died', 'teleportOut']),
         State.State('teleportIn', self.enterTeleportIn, self.exitTeleportIn, ['walk', 'WaitForBattle', 'battle']),
         State.State('teleportOut', self.enterTeleportOut, self.exitTeleportOut, ['teleportIn', 'final', 'WaitForBattle']),
         State.State('died', self.enterDied, self.exitDied, ['quietZone']),
         State.State('tunnelIn', self.enterTunnelIn, self.exitTunnelIn, ['walk', 'WaitForBattle', 'battle']),
         State.State('tunnelOut', self.enterTunnelOut, self.exitTunnelOut, ['final']),
         State.State('purchase', self.enterPurchase, self.exitPurchase, ['walk']),
         State.State('final', self.enterFinal, self.exitFinal, ['start'])], 'start', 'final')

    def load(self):
        self.parentFSM.getStateNamed('cogHQExterior').addChild(self.fsm)
        BattlePlace.BattlePlace.load(self)

    def unload(self):
        self.parentFSM.getStateNamed('cogHQExterior').removeChild(self.fsm)
        del self.fsm
        BattlePlace.BattlePlace.unload(self)

    def enter(self, requestStatus):
        self.zoneId = requestStatus['zoneId']
        base.discord.setZone(self.zoneId)
        BattlePlace.BattlePlace.enter(self)
        self.fsm.enterInitialState()
        if not hasattr(self.loader, "music"):
            self.loader.music = MusicManagerGlobals.GLOBALS[self.zoneId]['music']
            self.loader.battleMusic = MusicManagerGlobals.GLOBALS[self.zoneId]['battleMusic']
        base.contentPackMusicManager.playMusic(self.loader.music, looping=1, volume=0.8)
        self.loader.geom.reparentTo(render)
        self.nodeList = [self.loader.geom]
        self._telemLimiter = TLGatherAllAvs('CogHQExterior', RotationLimitToH)
        self.accept('doorDoneEvent', self.handleDoorDoneEvent)
        self.accept('DistributedDoor_doorTrigger', self.handleDoorTrigger)
        NametagGlobals.setMasterArrowsOn(1)
        self.tunnelOriginList = base.cr.hoodMgr.addLinkTunnelHooks(self, self.nodeList, self.zoneId)
        how = requestStatus['how']
        self.fsm.request(how, [requestStatus])
        self.handleInterests()

    def exit(self):
        self.fsm.requestFinalState()
        self._telemLimiter.destroy()
        del self._telemLimiter
        for node in self.tunnelOriginList:
            node.removeNode()

        del self.tunnelOriginList
        if self.loader.geom:
            self.loader.geom.reparentTo(hidden)
        self.ignoreAll()
        BattlePlace.BattlePlace.exit(self)

    def enterTunnelOut(self, requestStatus):
        fromZoneId = self.zoneId - self.zoneId % 100
        tunnelName = base.cr.hoodMgr.makeLinkTunnelName(self.loader.hood.id, fromZoneId)
        requestStatus['tunnelName'] = tunnelName
        BattlePlace.BattlePlace.enterTunnelOut(self, requestStatus)

    def enterTeleportIn(self, requestStatus):
        x, y, z, h, p, r = base.cr.hoodMgr.getPlaygroundCenterFromId(self.loader.hood.id)
        base.localAvatar.setPosHpr(render, x, y, z, h, p, r)
        BattlePlace.BattlePlace.enterTeleportIn(self, requestStatus)

    def enterTeleportOut(self, requestStatus, callback = None):
        if 'battle' in requestStatus:
            self.__teleportOutDone(requestStatus)
        else:
            BattlePlace.BattlePlace.enterTeleportOut(self, requestStatus, self.__teleportOutDone)

    def __teleportOutDone(self, requestStatus):
        hoodId = requestStatus['hoodId']
        zoneId = requestStatus['zoneId']
        avId = requestStatus['avId']
        shardId = requestStatus['shardId']
        if hoodId == self.loader.hood.hoodId and zoneId == self.loader.hood.hoodId and shardId == None:
            self.fsm.request('teleportIn', [requestStatus])
        elif hoodId == ToontownGlobals.MyEstate:
            self.getEstateZoneAndGoHome(requestStatus)
        else:
            self.doneStatus = requestStatus
            messenger.send(self.doneEvent)
        return

    def exitTeleportOut(self):
        BattlePlace.BattlePlace.exitTeleportOut(self)

    def enterSquished(self):
        base.localAvatar.laffMeter.start()
        base.localAvatar.b_setAnimState('Squish')
        taskMgr.doMethodLater(2.0, self.handleSquishDone, base.localAvatar.uniqueName('finishSquishTask'))

    def handleSquishDone(self, extraArgs = []):
        base.cr.playGame.getPlace().setState('walk')

    def exitSquished(self):
        taskMgr.remove(base.localAvatar.uniqueName('finishSquishTask'))
        base.localAvatar.laffMeter.stop()

    def handleInterests(self):

        # Grab the "starting" zone ID for this zone
        branchZone = ZoneUtil.getBranchZone(self.zoneId)

        # First, we need to load the DNA file for this Cog HQ.
        dnaStore = DNAStorage()
        dnaFileName = self.genDNAFileName(branchZone)
        loadDNAFile(dnaStore, dnaFileName)

        # Next, we need to collect all of the visgroup zone IDs.
        self.zoneVisDict = {}
        for i in range(dnaStore.getNumDNAVisGroups()):
            groupFullName = dnaStore.getDNAVisGroupName(i)
            visGroup = dnaStore.getDNAVisGroup(i)
            visZoneId = int(base.cr.hoodMgr.extractGroupName(groupFullName))
            visZoneId = ZoneUtil.getTrueZoneId(visZoneId, branchZone)
            visibles = []
            for i in range(visGroup.getNumVisibles()):
                visibles.append(int(visGroup.getVisibleName(i)))

            visibles.append(ZoneUtil.getBranchZone(visZoneId))
            self.zoneVisDict[visZoneId] = visibles

        # Finally, we want interest in all visgroups due to this being a Cog HQ.
        visibleZoneIds = set()
        visibleZoneIds.add(self.zoneId)  # Of course make sure we can at least see our zone
        for connectingZones in list(self.zoneVisDict.values()):
            for zone in connectingZones:
                visibleZoneIds.add(zone)

        base.cr.sendSetZoneMsg(self.zoneId, list(visibleZoneIds))
