import functools

from direct.distributed import DistributedSmoothNode
from direct.fsm.ClassicFSM import ClassicFSM
from direct.fsm.State import State
from direct.gui.DirectLabel import DirectLabel
from direct.interval.FunctionInterval import Func
from direct.interval.LerpInterval import LerpScaleInterval
from direct.interval.MetaInterval import Sequence
from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import Fog, CollisionPlane, Plane, Vec3, Point3, CollisionNode, BitMask32, CollisionPolygon, NodePath, \
    VBase4, TextNode, Vec4

from libotp import NametagGroup, CFSpeech, CFTimeout
from libotp.nametag import NametagGlobals
from toontown.building import ElevatorUtils
from toontown.building.ElevatorConstants import ELEVATOR_CJ
from toontown.coghq import ScaleLeagueGlobals
from toontown.coghq.BossSpeedrunTimer import BossSpeedrunTimer
from toontown.coghq.CogBossScoreboard import CogBossScoreboard
from toontown.minigame.DistributedMinigame import DistributedMinigame
from toontown.minigame.craning.CraneWalk import CraneWalk
from toontown.suit import BossCogGlobals
from toontown.toon.Toon import Toon
from toontown.toon.ToonDNA import ToonDNA
from toontown.toonbase import TTLocalizer, ToontownGlobals
from toontown.toonbase.ToontownTimer import ToontownTimer


class DistributedScaleGame(DistributedMinigame):
    # define constants that you won't want to tweak here
    stunTextColor = (0, 0.3, 1.0, 1)

    def __init__(self, cr):
        super().__init__(cr)

        self.walkStateData = CraneWalk('walkDone')

        self.bossSpeedrunTimer = BossSpeedrunTimer()
        self.bossSpeedrunTimer.hide()

        self.scoreboard = CogBossScoreboard()
        self.scoreboard.hide()

        self.boss = None
        self.ruleset = ScaleLeagueGlobals.CJRuleset()
        self.weightPerToon = 1
        self.baseColStashed = False
        self.bonusTimer = None
        self.cooldownTimer = None
        self.witnessToonOnstage = False
        self.everThrownPie = False
        self.onscreenMessage = None
        self.lawyerRequest = None
        self.lawyers = []
        self.chairs = {}
        self.gavels = {}
        self.panFlashInterval = None

        self.gameFSM = ClassicFSM(self.__class__.__name__,
                                  [
                                      State('off',
                                            self.enterOff,
                                            self.exitOff,
                                            ['play']),
                                      State('play',
                                            self.enterPlay,
                                            self.exitPlay,
                                            ['victory', 'defeat', 'cleanup']),
                                      State('victory',
                                            self.enterVictory,
                                            self.exitVictory,
                                            ['cleanup']),
                                      State('defeat',
                                            self.enterDefeat,
                                            self.exitDefeat,
                                            ['cleanup']),
                                      State('cleanup',
                                            self.enterCleanup,
                                            self.exitCleanup,
                                            []),
                                  ],
                                  # Initial State
                                  'off',
                                  # Final State
                                  'cleanup',
                                  )

        # it's important for the final state to do cleanup;
        # on disconnect, the ClassicFSM will be forced into the
        # final state. All states (except 'off') should
        # be prepared to transition to 'cleanup' at any time.

        # Add our game ClassicFSM to the framework ClassicFSM
        self.addChildGameFSM(self.gameFSM)

    def getTitle(self):
        return TTLocalizer.ScaleGameTitle

    def getInstructions(self):
        return TTLocalizer.ScaleGameInstructions

    def getMaxDuration(self):
        # how many seconds can this minigame possibly last (within reason)?
        # this is for debugging only
        return 0

    def load(self):
        self.notify.debug("load")
        super().load()
        # load resources and create objects here
        self.music = base.loader.loadMusic('phase_7/audio/bgm/encntr_suit_winning_indoor.ogg')
        self.winSting = base.loader.loadSfx("phase_4/audio/sfx/MG_win.ogg")
        self.loseSting = base.loader.loadSfx("phase_4/audio/sfx/MG_lose.ogg")
        self.piesRestockSfx = loader.loadSfx('phase_5/audio/sfx/LB_receive_evidence.ogg')
        self.toonUpSfx = loader.loadSfx('phase_11/audio/sfx/LB_toonup.ogg')
        self.evidenceHitSfx = loader.loadSfx('phase_11/audio/sfx/LB_evidence_hit.ogg')

        self.geom = loader.loadModel('phase_11/models/lawbotHQ/LawbotCourtroom3')
        self.geom.setPos(0, 0, -71.601)
        self.geom.setScale(1)
        self.elevatorEntrance = self.geom.find('**/elevator_origin')
        self.elevatorEntrance.getChildren().detach()
        self.elevatorEntrance.setScale(1)
        self.elevatorModel = loader.loadModel('phase_11/models/lawbotHQ/LB_Elevator')
        self.elevatorModel.reparentTo(self.elevatorEntrance)
        leftDoor = self.elevatorModel.find('**/left-door')
        if leftDoor.isEmpty():
            leftDoor = self.elevatorModel.find('**/left_door')
        leftDoor.setPos(ElevatorUtils.getLeftClosePoint(ELEVATOR_CJ))
        rightDoor = self.elevatorModel.find('**/right-door')
        if rightDoor.isEmpty():
            rightDoor = self.elevatorModel.find('**/right_door')
        rightDoor.setPos(ElevatorUtils.getRightClosePoint(ELEVATOR_CJ))

        floor = self.geom.find('**/MidVaultFloor1')
        if floor.isEmpty():
            floor = self.geom.find('**/CR3_Floor')
        self.evFloor = self.replaceCollisionPolysWithPlanes(floor)
        self.evFloor.reparentTo(self.geom)
        self.evFloor.setName('floor')
        plane = CollisionPlane(Plane(Vec3(0, 0, 1), Point3(0, 0, -50)))
        planeNode = CollisionNode('dropPlane')
        planeNode.addSolid(plane)
        planeNode.setCollideMask(ToontownGlobals.PieBitmask)
        self.geom.attachNewNode(planeNode)
        self.door3 = self.geom.find('**/SlidingDoor1/')
        if self.door3.isEmpty():
            self.door3 = self.geom.find('**/interior/CR3_Door')
        self.mainDoor = self.geom.find('**/Door_1')
        if not self.mainDoor.isEmpty():
            itemsToHide = ['interior/Door_1']
            for str in itemsToHide:
                stuffToHide = self.geom.find('**/%s' % str)
                if not stuffToHide.isEmpty():
                    self.notify.debug('found %s' % stuffToHide)
                    stuffToHide.wrtReparentTo(self.mainDoor)
                else:
                    self.notify.debug('not found %s' % stuffToHide)

        self.reflectedMainDoor = self.geom.find('**/interiorrefl/CR3_Door')
        if not self.reflectedMainDoor.isEmpty():
            itemsToHide = ['Reflections/Door_1']
            for str in itemsToHide:
                stuffToHide = self.geom.find('**/%s' % str)
                if not stuffToHide.isEmpty():
                    self.notify.debug('found %s' % stuffToHide)
                    stuffToHide.wrtReparentTo(self.reflectedMainDoor)
                else:
                    self.notify.debug('not found %s' % stuffToHide)

        self.geom.reparentTo(render)
        self.loadWitnessStand()
        self.loadScale()
        self.loadJuryBox()
        self.loadPodium()

        buildings = self.geom.findAllMatches('**/LB_BGBuildings*')
        sky = self.geom.findAllMatches('**/LB_Sky*')

        fog = Fog('LBHQLobby')
        fog.setColor(.12, .15, .23)
        fog.setExpDensity(0.0005)
        for node in sky:
            node.setColorScale(0.88, 0.92, .96, 1)
            node.setFog(fog)

        for node in buildings:
            node.setColorScale(0.88, 0.92, .96, 1)
            node.setFog(fog)

        ug = self.geom.find('**/Reflections')
        ug.setBin('ground', -10)

        self.__makeWitnessToon()
        self.__showWitnessToon()

    def unload(self):
        self.notify.debug("unload")
        super().unload()
        # unload resources and delete objects from load() here
        # remove our game ClassicFSM from the framework ClassicFSM
        self.removeChildGameFSM(self.gameFSM)
        del self.gameFSM

        self.__cleanupWitnessToon()
        self.__cleanupJuryBox()

        self.geom.removeNode()
        del self.geom

        self.music.stop()
        del self.music

        self.scoreboard.cleanup()
        del self.scoreboard

        self.bossSpeedrunTimer.cleanup()
        del self.bossSpeedrunTimer

        if self.bonusTimer:
            self.bonusTimer.destroy()
        del self.bonusTimer
        if self.cooldownTimer:
            self.cooldownTimer.destroy()
        del self.cooldownTimer

        localAvatar.chatMgr.chatInputSpeedChat.removeCJMenu()

    def onstage(self):
        self.notify.debug("onstage")
        super().onstage()
        # start up the minigame; parent things to render, start playing
        # music...
        # at this point we cannot yet show the remote players' toons

        base.localAvatar.reparentTo(render)
        base.localAvatar.setPos(-3, 0, 0)
        base.localAvatar.loop('neutral')
        localAvatar.setCameraFov(ToontownGlobals.CogHQCameraFov)
        base.camLens.setNearFar(ToontownGlobals.CogHQCameraNear, ToontownGlobals.CogHQCameraFar)
        base.transitions.irisIn(0.4)
        NametagGlobals.setMasterArrowsOn(1)
        camera.reparentTo(render)

        camera.setPosHpr(-3, 45, 30, 0, 0, 0)

        DistributedSmoothNode.activateSmoothing(1, 1)

    def offstage(self):
        self.notify.debug("offstage")
        # stop the minigame; parent things to hidden, stop the
        # music...
        DistributedSmoothNode.activateSmoothing(1, 0)
        NametagGlobals.setMasterArrowsOn(0)
        base.camLens.setFar(ToontownGlobals.DefaultCameraFar)

        # the base class parents the toons to hidden, so consider
        # calling it last
        super().offstage()

    def handleDisabledAvatar(self, avId):
        """This will be called if an avatar exits unexpectedly"""
        self.notify.debug("handleDisabledAvatar")
        self.notify.debug("avatar " + str(avId) + " disabled")
        # clean up any references to the disabled avatar before he disappears

        # then call the base class
        super().handleDisabledAvatar(avId)

    def setGameReady(self):
        if not self.hasLocalToon: return
        self.notify.debug("setGameReady")
        if super().setGameReady():
            return
        # all of the remote toons have joined the game;
        # it's safe to show them now.
        self.weightPerToon = self.ruleset.JURORS_SEATED // len(self.avIdList)
        localAvatar.chatMgr.chatInputSpeedChat.addCJMenu(self.weightPerToon)

    def setGameStart(self, timestamp):
        if not self.hasLocalToon: return
        self.notify.debug("setGameStart")
        # base class will cause gameFSM to enter initial state
        super().setGameStart(timestamp)
        # all players have finished reading the rules,
        # and are ready to start playing.
        # transition to the appropriate state
        self.gameFSM.request("play")

    # these are enter and exit functions for the game's
    # fsm (finite state machine)

    def enterOff(self):
        self.notify.debug("enterOff")

    def exitOff(self):
        pass

    def enterPlay(self):
        self.notify.debug("enterPlay")

        self.walkStateData.enter()

        base.playMusic(self.music, looping=1, volume=0.9)

        self.accept("LocalSetFinalBattleMode", self.toFinalBattleMode)
        self.accept("LocalSetOuchMode", self.toOuchMode)
        self.accept("ChatMgr-enterMainMenu", self.chatClosed)

        self.accept('enterWitnessStand', self.__touchedWitnessStand)
        self.accept('outOfPies', self.__outOfPies)
        self.accept('begin-pie', self.__foundPieButton)
        self.accept('pieSplat', self.__pieSplat)
        self.accept('localPieSplat', self.__localPieSplat)

        localAvatar.setCameraFov(ToontownGlobals.BossBattleCameraFov)

        # Display Boss Timer
        self.bossSpeedrunTimer.reset()
        self.bossSpeedrunTimer.start_updating()
        self.bossSpeedrunTimer.show()

        # Setup the scoreboard
        self.scoreboard.clearToons()
        for avId in self.avIdList:
            if avId in base.cr.doId2do:
                self.scoreboard.addToon(avId)

    def exitPlay(self):
        if self.boss is not None:
            self.boss.cleanupBossBattle()

        self.__clearOnscreenMessage()
        self.walkStateData.exit()
        self.ignoreAll()
        taskMgr.remove(self.uniqueName('PieAdvice'))
        localAvatar.setCameraFov(ToontownGlobals.CogHQCameraFov)

        self.cr.relatedObjectMgr.abortRequest(self.lawyerRequest)
        self.lawyerRequest = None

        render.clearTag('pieCode')

    def enterVictory(self):
        if self.victor == 0:
            return

        victor = base.cr.getDo(self.victor)
        if self.victor == self.localAvId:
            base.playSfx(self.winSting)
        else:
            base.playSfx(self.loseSting)
        camera.reparentTo(victor)
        camera.setPosHpr(0, 8, victor.getHeight() / 2.0, 180, 0, 0)

        victor.setAnimState("victory")

        taskMgr.doMethodLater(5, self.gameOver, self.uniqueName("scaleGameVictory"), extraArgs=[])

    def exitVictory(self):
        taskMgr.remove(self.uniqueName("scaleGameVictory"))
        camera.reparentTo(render)

    def enterDefeat(self):
        self.defeatTrack = Sequence(self.boss.makeDefeatMovie(), Func(self.gameOver))
        self.defeatTrack.start()

    def exitDefeat(self):
        self.defeatTrack.finish()
        del self.defeatTrack

    def enterCleanup(self):
        self.notify.debug("enterCleanup")

    def exitCleanup(self):
        pass

    """
    yeah
    """

    def loadJuryBox(self):
        self.juryBox = self.geom.find('**/JuryBox')
        self.reflectedJuryBox = self.geom.find('**/JuryBox_Geo_Reflect')

    def loadPodium(self):
        self.podium = self.geom.find('**/Podium')
        self.reflectedPodium = self.geom.find('**/Podium_Geo1_Refl')

    def loadWitnessStand(self):
        self.realWitnessStand = self.geom.find('**/WitnessStand')
        if not self.realWitnessStand.isEmpty():
            pass
        self.reflectedWitnessStand = self.geom.find('**/Witnessstand_Geo_Reflect')
        if not self.reflectedWitnessStand.isEmpty():
            pass
        colNode = self.realWitnessStand.find('**/witnessStandCollisions/Witnessstand_Collision')
        colNode.setName('WitnessStand')

    def loadScale(self):
        self.scaleNodePath = loader.loadModel('phase_11/models/lawbotHQ/scale')
        self.beamNodePath = self.scaleNodePath.find('**/scaleBeam')
        self.defensePanNodePath = self.scaleNodePath.find('**/defensePan')
        self.prosecutionPanNodePath = self.scaleNodePath.find('**/prosecutionPan')
        self.defenseColNodePath = self.scaleNodePath.find('**/DefenseCol')
        self.defenseColNodePath.setTag('pieCode', str(ToontownGlobals.PieCodeDefensePan))
        self.prosecutionColNodePath = self.scaleNodePath.find('**/ProsecutionCol')
        self.prosecutionColNodePath.setTag('pieCode', str(ToontownGlobals.PieCodeProsecutionPan))
        self.standNodePath = self.scaleNodePath.find('**/scaleStand')
        self.scaleNodePath.setPosHpr(*ToontownGlobals.LawbotBossInjusticePosHpr)
        self.defenseLocator = self.scaleNodePath.find('**/DefenseLocator')
        defenseLocBounds = self.defenseLocator.getBounds()
        defenseLocPos = defenseLocBounds.getCenter()
        self.notify.debug('defenseLocatorPos = %s' % defenseLocPos)
        self.defensePanNodePath.setPos(defenseLocPos)
        self.defensePanNodePath.reparentTo(self.beamNodePath)
        self.notify.debug('defensePanNodePath.getPos()=%s' % self.defensePanNodePath.getPos())
        self.prosecutionLocator = self.scaleNodePath.find('**/ProsecutionLocator')
        prosecutionLocBounds = self.prosecutionLocator.getBounds()
        prosecutionLocPos = prosecutionLocBounds.getCenter()
        self.notify.debug('prosecutionLocatorPos = %s' % prosecutionLocPos)
        self.prosecutionPanNodePath.setPos(prosecutionLocPos)
        self.prosecutionPanNodePath.reparentTo(self.beamNodePath)
        self.beamLocator = self.scaleNodePath.find('**/StandLocator1')
        beamLocatorBounds = self.beamLocator.getBounds()
        beamLocatorPos = beamLocatorBounds.getCenter()
        negBeamLocatorPos = -beamLocatorPos
        self.notify.debug('beamLocatorPos = %s' % beamLocatorPos)
        self.notify.debug('negBeamLocatorPos = %s' % negBeamLocatorPos)
        self.beamNodePath.setPos(beamLocatorPos)
        self.scaleNodePath.setScale(*ToontownGlobals.LawbotBossInjusticeScale)
        self.scaleNodePath.wrtReparentTo(self.geom)
        self.baseHighCol = self.scaleNodePath.find('**/BaseHighCol')
        oldBitMask = self.baseHighCol.getCollideMask()
        newBitMask = oldBitMask & ~ToontownGlobals.PieBitmask
        newBitMask = newBitMask & ~ToontownGlobals.CameraBitmask
        self.baseHighCol.setCollideMask(newBitMask)
        self.defenseHighCol = self.scaleNodePath.find('**/DefenseHighCol')
        self.defenseHighCol.stash()
        self.defenseHighCol.setCollideMask(newBitMask)
        self.baseTopCol = self.scaleNodePath.find('**/Scale_base_top_collision')
        self.baseSideCol = self.scaleNodePath.find('**/Scale_base_side_col')
        self.defenseLocator.hide()
        self.prosecutionLocator.hide()
        self.beamLocator.hide()

    def __makeWitnessToon(self):
        npc = Toon()
        npc.setName("Kitt Kitt Lou")
        npc.setPickable(0)
        npc.setPlayerType(NametagGroup.CCNonPlayer)
        dna = ToonDNA()
        dna.newToonFromProperties('css', 'ms', 'm', 'm', 8, 0, 8, 8,
                                  1,
                                  21,
                                  1,
                                  21,
                                  1,
                                  24
                                  )
        npc.setDNAString(dna.makeNetString())
        npc.animFSM.request('Sit')
        self.witnessToon = npc
        self.witnessToon.setPosHpr(*ToontownGlobals.LawbotBossWitnessStandPosHpr)

    def __cleanupWitnessToon(self):
        self.__hideWitnessToon()
        if self.witnessToon:
            self.witnessToon.removeActive()
            self.witnessToon.delete()
            self.witnessToon = None
        return

    def __showWitnessToon(self):
        if not self.witnessToonOnstage:
            self.witnessToon.addActive()
            self.witnessToon.reparentTo(self.geom)
            seatCenter = self.realWitnessStand.find('**/witnessStandSeatEdge')
            center = seatCenter.getPos()
            self.notify.debug('center = %s' % center)
            self.witnessToon.setPos(center)
            self.witnessToon.setH(180)
            self.witnessToon.setZ(self.witnessToon.getZ() - 1.5)
            self.witnessToon.setY(self.witnessToon.getY() - 1.15)
            self.witnessToonOnstage = 1

    def __hideWitnessToon(self):
        if self.witnessToonOnstage:
            self.witnessToon.removeActive()
            self.witnessToon.detachNode()
            self.witnessToonOnstage = 0

    def replaceCollisionPolysWithPlanes(self, model):
        newCollisionNode = CollisionNode('collisions')
        newCollideMask = BitMask32(0)
        planes = []
        collList = model.findAllMatches('**/+CollisionNode')
        if not collList:
            collList = [model]
        for cnp in collList:
            cn = cnp.node()
            if not isinstance(cn, CollisionNode):
                self.notify.warning('Not a collision node: %s' % repr(cnp))
                break
            newCollideMask = newCollideMask | cn.getIntoCollideMask()
            for i in range(cn.getNumSolids()):
                solid = cn.getSolid(i)
                if isinstance(solid, CollisionPolygon):
                    plane = Plane(solid.getPlane())
                    planes.append(plane)
                else:
                    self.notify.warning('Unexpected collision solid: %s' % repr(solid))
                    newCollisionNode.addSolid(plane)

        newCollisionNode.setIntoCollideMask(newCollideMask)
        threshold = 0.1
        planes.sort(key=functools.cmp_to_key(lambda p1, p2: p1.compareTo(p2, threshold)))
        lastPlane = None
        for plane in planes:
            if lastPlane == None or plane.compareTo(lastPlane, threshold) != 0:
                cp = CollisionPlane(plane)
                newCollisionNode.addSolid(cp)
                lastPlane = plane

        return NodePath(newCollisionNode)

    def declareVictor(self, avId: int) -> None:
        self.victor = avId
        self.gameFSM.request("victory")

    def setBossCogId(self, bossCogId: int) -> None:
        self.boss = base.cr.getDo(bossCogId)
        self.boss.game = self
        self.boss.prepareBossForBattle()

    def __outOfPies(self):
        self.notify.debug('----- outOfPies')
        self.__showOnscreenMessage(TTLocalizer.LawbotBossNeedMoreEvidence)
        taskMgr.doMethodLater(20, self.__howToGetPies, self.uniqueName('PieAdvice'))

    def __howToGetPies(self, task):
        self.notify.debug('----- __howToGetPies')
        self.__showOnscreenMessage(TTLocalizer.LawbotBossHowToGetEvidence)

    def __howToThrowPies(self, task):
        self.notify.debug('----- __howToThrowPies')
        self.__showOnscreenMessage(TTLocalizer.LawbotBossHowToThrowPies)

    def __foundPieButton(self):
        self.everThrownPie = True
        self.__clearOnscreenMessage()
        taskMgr.remove(self.uniqueName('PieAdvice'))

    def __touchedWitnessStand(self, entry):
        self.sendUpdate('touchWitnessStand', [])
        self.__clearOnscreenMessage()
        taskMgr.remove(self.uniqueName('PieAdvice'))
        base.playSfx(self.piesRestockSfx)
        if not self.everThrownPie:
            taskMgr.doMethodLater(30, self.__howToThrowPies, self.uniqueName('PieAdvice'))

    def __showOnscreenMessage(self, text):
        self.notify.debug('----- __showOnscreenmessage')
        if self.onscreenMessage:
            self.onscreenMessage.destroy()
            self.onscreenMessage = None
        self.onscreenMessage = DirectLabel(text=text, text_fg=VBase4(1, 1, 1, 1), text_align=TextNode.ACenter,
                                           relief=None, pos=(0, 0, 0.35), scale=0.1)
        return

    def __clearOnscreenMessage(self):
        if self.onscreenMessage:
            self.onscreenMessage.destroy()
            self.onscreenMessage = None
        return

    def touchedGavel(self, gavel, entry):
        self.notify.debug('touchedGavel')
        attackCodeStr = entry.getIntoNodePath().getNetTag('attackCode')
        if attackCodeStr == '':
            self.notify.warning('Node %s has no attackCode tag.' % repr(entry.getIntoNodePath()))
            return
        attackCode = int(attackCodeStr)
        into = entry.getIntoNodePath()
        self.boss.zapLocalToon(attackCode, into)

    def touchedGavelHandle(self, gavel, entry):
        attackCodeStr = entry.getIntoNodePath().getNetTag('attackCode')
        if attackCodeStr == '':
            self.notify.warning('Node %s has no attackCode tag.' % repr(entry.getIntoNodePath()))
            return
        attackCode = int(attackCodeStr)
        into = entry.getIntoNodePath()
        self.boss.zapLocalToon(attackCode, into)

    def toFinalBattleMode(self):
        self.walkStateData.fsm.request('walking')

    def toOuchMode(self):
        self.walkStateData.fsm.request('ouch')

    def chatClosed(self):
        if self.walkStateData.fsm.getCurrentState().getName() == "walking":
            base.localAvatar.enableAvatarControls()

    def setScaleTilt(self, tilt):
        self.beamNodePath.setP(tilt)
        self.defensePanNodePath.setP(-tilt)
        self.prosecutionPanNodePath.setP(-tilt)

    def stashBaseCol(self):
        if not self.baseColStashed:
            self.notify.debug('stashBaseCol')
            self.baseTopCol.stash()
            self.baseSideCol.stash()
            self.baseColStashed = True

    def unstashBaseCol(self):
        if self.baseColStashed:
            self.notify.debug('unstashBaseCol')
            self.baseTopCol.unstash()
            self.baseSideCol.unstash()
            self.baseColStashed = False

    def makeScaleReflectDamage(self):
        diffDamage = self.boss.bossDamage - ToontownGlobals.LawbotBossInitialDamage
        diffDamage *= 1.0
        if diffDamage >= 0:
            percentDamaged = diffDamage / (
                    ToontownGlobals.LawbotBossMaxDamage - ToontownGlobals.LawbotBossInitialDamage)
            tilt = percentDamaged * ToontownGlobals.LawbotBossWinningTilt
        else:
            percentDamaged = diffDamage / (ToontownGlobals.LawbotBossInitialDamage - 0)
            tilt = percentDamaged * ToontownGlobals.LawbotBossWinningTilt
        self.setScaleTilt(tilt)
        if self.boss.bossDamage < ToontownGlobals.LawbotBossMaxDamage * 0.85:
            self.unstashBaseCol()
        else:
            self.stashBaseCol()

    def hideBonusTimer(self):
        base.localAvatar.showHpString(TTLocalizer.StunBonusOver, color=self.stunTextColor)

        #self.witnessToon.clearChat()
        #text = TTLocalizer.WitnessToonBonusOver
        #self.witnessToon.setChatAbsolute(text, CFSpeech | CFTimeout)
        if self.bonusTimer:
            Sequence(LerpScaleInterval(self.bonusTimer, 0.09, .45, blendType='easeInOut'),
                     LerpScaleInterval(self.bonusTimer, 0.2, 0, blendType='easeInOut'),
                     Func(self.bonusTimer.hide),
                     Func(self.showCooldownTimer)).start()

    def hideCooldownTimer(self):
        base.localAvatar.showHpString(TTLocalizer.StunBonusAvailable, color=self.stunTextColor)

        if self.cooldownTimer:
            Sequence(LerpScaleInterval(self.cooldownTimer, 0.09, .45, blendType='easeInOut'),
                     LerpScaleInterval(self.cooldownTimer, 0.2, 0, blendType='easeInOut'),
                     Func(self.cooldownTimer.hide)).start()

    def showCooldownTimer(self):
        if not self.cooldownTimer:
            self.cooldownTimer = ToontownTimer()
            self.cooldownTimer.posInTopRightBelowHealthBar()
            self.cooldownTimer.setFontColor(Vec4(0, 0.65, 1, 1))
        Sequence(Func(self.cooldownTimer.show),
                 LerpScaleInterval(self.cooldownTimer, 0.2, 0.45, 0, blendType='easeInOut'),
                 LerpScaleInterval(self.cooldownTimer, 0.09, 0.4, blendType='easeInOut')).start()
        self.cooldownTimer.countdown(ToontownGlobals.LawbotBossBonusWaitTime, self.hideCooldownTimer)

    def enteredBonusState(self):
        base.localAvatar.showHpString(TTLocalizer.StunBonus, color=self.stunTextColor)
        self.witnessToon.clearChat()
        text = TTLocalizer.WitnessToonBonus % (
            ToontownGlobals.LawbotBossBonusWeightMultiplier, ToontownGlobals.LawbotBossBonusDuration)
        self.witnessToon.setChatAbsolute(text, CFSpeech | CFTimeout)
        base.playSfx(self.toonUpSfx)
        if not self.bonusTimer:
            self.bonusTimer = ToontownTimer()
            self.bonusTimer.posInTopRightBelowHealthBar()
        Sequence(Func(self.bonusTimer.show),
                 LerpScaleInterval(self.bonusTimer, 0.2, 0.45, 0, blendType='easeInOut'),
                 LerpScaleInterval(self.bonusTimer, 0.09, 0.4, blendType='easeInOut')).start()
        self.bonusTimer.countdown(ToontownGlobals.LawbotBossBonusDuration, self.hideBonusTimer)

    def __cleanupJuryBox(self):
        self.notify.debug('----- __cleanupJuryBox')
        if self.juryBox:
            self.juryBox.removeNode()

    def updateRequiredElements(self):
        if self.bossSpeedrunTimer:
            self.bossSpeedrunTimer.cleanup()

        self.bossSpeedrunTimer = BossSpeedrunTimer()
        self.bossSpeedrunTimer.hide()
        # self.heatDisplay.update(self.calculateHeat(), self.modifiers)

    def setRawRuleset(self, attrs):
        self.ruleset = ScaleLeagueGlobals.CJRuleset.fromStruct(attrs)
        self.updateRequiredElements()
        print(('ruleset updated: ' + str(self.ruleset)))

    def getRawRuleset(self):
        return self.ruleset.asStruct()

    def getRuleset(self):
        return self.ruleset

    def lawyerDisabled(self, avId):
        self.scoreboard.addScore(avId, 3, reason='LAWYER!')

    def updateTimer(self, secs):
        self.bossSpeedrunTimer.override_time(secs)
        self.bossSpeedrunTimer.update_time()

    def updateDamageDealt(self, avId, damageDealt):
        self.scoreboard.addScore(avId, damageDealt)
        self.scoreboard.addDamage(avId, damageDealt)

    def updateStunCount(self, avId, pointBonus):
        self.scoreboard.addScore(avId, pointBonus, reason='STUN!')
        self.scoreboard.addStun(avId)

    def avHealed(self, avId, hp):
        self.scoreboard.addScore(avId, hp, reason='HEAL!')
        self.scoreboard.addHealing(avId, hp)

    def toonDied(self, avId):
        self.scoreboard.addScore(avId, BossCogGlobals.POINTS_PENALTY_SAD, BossCogGlobals.PENALTY_GO_SAD_TEXT)
        self.scoreboard.toonDied(avId)

    def revivedToon(self, avId):
        self.scoreboard.toonRevived(avId)
        if avId == base.localAvatar.doId:
            self.boss.localToonIsSafe = False
            base.localAvatar.stunToon()

    def cleanupPanFlash(self):
        if self.panFlashInterval:
            self.panFlashInterval.finish()
            self.panFlashInterval = None
        return

    def flashPanBlue(self):
        self.cleanupPanFlash()
        intervalName = 'FlashPanBlue'
        self.defensePanNodePath.setColorScale(1, 1, 1, 1)
        seq = Sequence(self.defensePanNodePath.colorScaleInterval(0.1, colorScale=VBase4(0, 0, 1, 1)),
                       self.defensePanNodePath.colorScaleInterval(0.3, colorScale=VBase4(1, 1, 1, 1)),
                       name=intervalName)
        self.panFlashInterval = seq
        seq.start()

    def __pieSplat(self, toon, pieCode):
        if pieCode == ToontownGlobals.PieCodeDefensePan:
            self.boss.flashRed()
            self.flashPanBlue()
            base.playSfx(self.evidenceHitSfx, node=self.defensePanNodePath, volume=0.25)
        elif pieCode == ToontownGlobals.PieCodeProsecutionPan:
            self.boss.flashGreen()

    def __localPieSplat(self, pieCode, entry):
        if pieCode == ToontownGlobals.PieCodeDefensePan:
            self.d_hitBoss()
        if pieCode == ToontownGlobals.PieCodeLawyer:
            self.__lawyerGotHit(entry)
        if pieCode != ToontownGlobals.PieCodeToon:
            return
        avatarDoId = entry.getIntoNodePath().getNetTag('avatarDoId')
        if avatarDoId == '':
            self.notify.warning('Toon %s has no avatarDoId tag.' % repr(entry.getIntoNodePath()))
            return
        doId = int(avatarDoId)
        if doId != localAvatar.doId:
            self.d_hitToon(doId)

    def __lawyerGotHit(self, entry):
        lawyerCol = entry.getIntoNodePath()
        names = lawyerCol.getName().split('-')
        lawyerDoId = int(names[1])
        for lawyer in self.lawyers:
            if lawyerDoId == lawyer.doId:
                lawyer.sendUpdate('hitByToon', [])

    def d_hitBoss(self):
        self.notify.debug('----- d_hitBoss')
        self.sendUpdate('hitBoss', [])

    def d_hitToon(self, toonId):
        self.notify.debug('----- d_hitToon')
        self.sendUpdate('hitToon', [toonId])

    def setLawyerIds(self, lawyerIds):
        self.lawyers = []
        self.cr.relatedObjectMgr.abortRequest(self.lawyerRequest)
        self.lawyerRequest = self.cr.relatedObjectMgr.requestObjects(lawyerIds, allCallback=self.__gotLawyers)

    def __gotLawyers(self, lawyers):
        self.lawyerRequest = None
        self.lawyers = lawyers
        for i in range(len(self.lawyers)):
            suit = self.lawyers[i]
            suit.fsm.request('neutral')
            suit.loop('neutral')
            suit.setBossCogId(self.doId)

    def toonGotHealed(self, toonId):
        toon = base.cr.doId2do.get(toonId)
        if toon:
            base.playSfx(self.toonUpSfx, node=toon)

    def getChairParent(self):
        return self.juryBox
