from direct.distributed import DistributedSmoothNode
from direct.fsm.ClassicFSM import ClassicFSM
from direct.fsm.State import State
from direct.gui.DirectLabel import DirectLabel
from direct.interval.ActorInterval import ActorInterval
from direct.interval.FunctionInterval import Func, Wait
from direct.interval.MetaInterval import Sequence, Parallel
from direct.interval.SoundInterval import SoundInterval
from direct.showutil.Rope import Rope
from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import Point3, RopeNode, CollisionPolygon, CollisionNode, VBase4, TextNode, CompassEffect, NodePath

from libotp import NametagGroup, CFSpeech, CFTimeout
from libotp.nametag import NametagGlobals
from toontown.building import ElevatorUtils
from toontown.building.ElevatorConstants import ELEVATOR_VP
from toontown.coghq.BossSpeedrunTimer import BossSpeedrunTimer
from toontown.coghq.CogBossScoreboard import CogBossScoreboard
from toontown.minigame.DistributedMinigame import DistributedMinigame
from toontown.minigame.craning.CraneWalk import CraneWalk
from toontown.minigame.pie.PieGameRampFSM import PieGameRampFSM
from toontown.suit import BossCogGlobals
from toontown.toon.Toon import Toon
from toontown.toon.ToonDNA import ToonDNA
from toontown.toonbase import TTLocalizer, ToontownGlobals


class DistributedPieGame(DistributedMinigame):

    # define constants that you won't want to tweak here

    def __init__(self, cr):
        super().__init__(cr)

        self.walkStateData = CraneWalk('walkDone')

        self.bossSpeedrunTimer = BossSpeedrunTimer()
        self.bossSpeedrunTimer.hide()

        self.scoreboard = CogBossScoreboard()
        self.scoreboard.hide()

        self.boss = None
        self.cagedToon = None
        self.cageShadow = None
        self.onscreenMessage = None
        self.everThrownPie = False

        self.gameFSM = ClassicFSM('DistributedPieGame',
                                  [
                                      State('off',
                                            self.enterOff,
                                            self.exitOff,
                                            ['play']),
                                      State('play',
                                            self.enterPlay,
                                            self.exitPlay,
                                            ['victory', 'cleanup']),
                                      State('victory',
                                            self.enterVictory,
                                            self.exitVictory,
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
        return TTLocalizer.PieGameTitle

    def getInstructions(self):
        return TTLocalizer.PieGameInstructions

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
        self.piesRestockSfx = loader.loadSfx('phase_9/audio/sfx/CHQ_SOS_pies_restock.ogg')

        self.geom = loader.loadModel('phase_9/models/cogHQ/BossRoomHQ')
        self.rampA = self.__findRamp('rampA', '**/west_ramp2')
        self.rampB = self.__findRamp('rampB', '**/west_ramp')
        self.rampC = self.__findRamp('rampC', '**/west_ramp1')

        self.rampA.request('Retract')
        self.rampB.request('Retract')
        self.rampC.request('Extend')

        # Setup elevator
        elevatorEntrance = self.geom.find('**/elevatorEntrance')
        elevatorEntrance.getChildren().detach()
        elevatorEntrance.setScale(1)
        self.elevatorModel = loader.loadModel('phase_9/models/cogHQ/cogHQ_elevator')
        self.elevatorModel.reparentTo(elevatorEntrance)
        leftDoor = self.elevatorModel.find('**/left-door')
        if leftDoor.isEmpty():
            leftDoor = self.elevatorModel.find('**/left_door')
        leftDoor.setPos(ElevatorUtils.getLeftClosePoint(ELEVATOR_VP))
        rightDoor = self.elevatorModel.find('**/right-door')
        if rightDoor.isEmpty():
            rightDoor = self.elevatorModel.find('**/right_door')
        rightDoor.setPos(ElevatorUtils.getRightClosePoint(ELEVATOR_VP))
        # self.setupElevator(elevatorModel)

        self.cage = self.geom.find('**/cage')
        pos = self.cage.getPos()
        self.cage.setPos(Point3(pos[0], pos[1], 25))

        self.cageDoor = self.geom.find('**/cage_door')
        self.cage.setScale(1)
        self.rope = Rope(name='supportChain')
        self.rope.reparentTo(self.cage)
        self.rope.setup(2, ((self.cage, (0.15, 0.13, 16)), (self.geom, (0.23, 78, 120))))
        self.rope.ropeNode.setRenderMode(RopeNode.RMBillboard)
        self.rope.ropeNode.setUvMode(RopeNode.UVDistance)
        self.rope.ropeNode.setUvDirection(0)
        self.rope.ropeNode.setUvScale(0.8)
        self.rope.setTexture(self.cage.findTexture('hq_chain'))
        self.rope.setTransparency(1)

        self.geom.reparentTo(render)

        self.sky = loader.loadModel('phase_9/models/cogHQ/cog_sky')
        self.sky.setTag('sky', 'Regular')
        self.sky.setScale(2.0)
        self.sky.setFogOff()
        self.sky.setH(150)
        self.sky.setZ(-100)

        self.__makeCagedToon()
        self.__placeCageShadow()

    def __findRamp(self, name, path):
        ramp = self.geom.find(path)
        children = ramp.getChildren()
        animate = ramp.attachNewNode(name)
        children.reparentTo(animate)
        return PieGameRampFSM(animate)

    def __makeCagedToon(self):
        if self.cagedToon:
            return
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
        npc.animFSM.request('neutral')
        self.cagedToon = npc
        self.cagedToon.addActive()
        self.cagedToon.reparentTo(self.cage)
        self.cagedToon.setPosHpr(0, -2, 0, 180, 0, 0)
        self.cagedToon.loop('neutral')
        touch = CollisionPolygon(Point3(-3.0382, 3.0382, -1), Point3(3.0382, 3.0382, -1), Point3(3.0382, -3.0382, -1),
                                 Point3(-3.0382, -3.0382, -1))
        touchNode = CollisionNode('Cage')
        touchNode.setCollideMask(ToontownGlobals.WallBitmask)
        touchNode.addSolid(touch)
        self.cage.attachNewNode(touchNode)

    def __cleanupCagedToon(self):
        if self.cagedToon:
            self.cagedToon.removeActive()
            self.cagedToon.delete()
            self.cagedToon = None
        return

    def __placeCageShadow(self):
        if self.cageShadow is None:
            self.cageShadow = loader.loadModel('phase_3/models/props/drop_shadow')
            self.cageShadow.setPos(0, 77.9, 18)
            self.cageShadow.setColorScale(1, 1, 1, 0.6)
        self.cageShadow.reparentTo(render)

    def __removeCageShadow(self):
        if self.cageShadow is not None:
            self.cageShadow.detachNode()

    def unload(self):
        self.notify.debug("unload")
        super().unload()

        self.music.stop()
        del self.music

        self.scoreboard.cleanup()
        del self.scoreboard

        self.__cleanupCagedToon()
        self.__removeCageShadow()

        self.bossSpeedrunTimer.cleanup()
        del self.bossSpeedrunTimer

        self.geom.removeNode()
        del self.geom
        del self.cage
        self.rampA.cleanup()
        self.rampB.cleanup()
        self.rampC.cleanup()
        del self.rampA
        del self.rampB
        del self.rampC

        self.sky.removeNode()
        del self.sky

        # unload resources and delete objects from load() here
        # remove our game ClassicFSM from the framework ClassicFSM
        self.removeChildGameFSM(self.gameFSM)
        del self.gameFSM

    def onstage(self):
        self.notify.debug("onstage")
        super().onstage()
        # start up the minigame; parent things to render, start playing
        # music...
        # at this point we cannot yet show the remote players' toons
        self.startSky()

        base.localAvatar.reparentTo(render)
        base.localAvatar.loop('neutral')
        localAvatar.setCameraFov(ToontownGlobals.CogHQCameraFov)
        base.camLens.setNearFar(ToontownGlobals.CogHQCameraNear, ToontownGlobals.CogHQCameraFar)
        base.transitions.irisIn(0.4)
        NametagGlobals.setMasterArrowsOn(1)
        camera.reparentTo(render)
        camera.setPosHpr(0, -150, 8, 0, 0, 0)
        # camera.setPosHpr(-15 - 25, 60, 55, -90, -30, 0)

        self.setToonsToBattleThreePos()

        DistributedSmoothNode.activateSmoothing(1, 1)

    def startSky(self):
        self.sky.reparentTo(camera)
        self.sky.setZ(0.0)
        self.sky.setHpr(0.0, 0.0, 0.0)
        ce = CompassEffect.make(NodePath(), CompassEffect.PRot | CompassEffect.PZ)
        self.sky.node().setEffect(ce)

    def stopSky(self):
        taskMgr.remove('skyTrack')
        self.sky.reparentTo(hidden)

    def offstage(self):
        self.notify.debug("offstage")
        # stop the minigame; parent things to hidden, stop the
        # music...
        DistributedSmoothNode.activateSmoothing(1, 0)
        NametagGlobals.setMasterArrowsOn(0)
        localAvatar.setCameraFov(ToontownGlobals.DefaultCameraFov)
        base.camLens.setNearFar(ToontownGlobals.DefaultCameraNear, ToontownGlobals.DefaultCameraFar)

        self.stopSky()

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
        for i in range(self.numPlayers):
            avId = self.avIdList[i]
            avatar = self.getAvatar(avId)
            if avatar:
                avatar.startSmooth()

        self.setToonsToBattleThreePos()

        base.localAvatar.d_clearSmoothing()
        base.localAvatar.sendCurrentPosition()
        base.localAvatar.b_setAnimState('neutral', 1)
        base.localAvatar.b_setParent(ToontownGlobals.SPRender)

    def setToonsToBattleThreePos(self):
        """
        Places each toon at the desired position and orientation without creating
        or returning any animation tracks. The position and orientation are
        applied immediately.
        """
        TOON_SPAWN_POSITIONS = [
            [-25, 65, 18, -90, 0, 0],
            [-25, 55, 18, -90, 0, 0],
            [25, 65, 18, 90, 0, 0],
            [25, 55, 18, 90, 0, 0],
        ]
        for i, toonId in enumerate(self.avIdList):
            toon = base.cr.doId2do.get(toonId)
            if toon:
                toon.setPosHpr(*TOON_SPAWN_POSITIONS[i])

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

        self.accept('enterCage', self.__touchedCage)
        self.accept('begin-pie', self.__foundPieButton)
        self.accept('outOfPies', self.__outOfPies)
        taskMgr.doMethodLater(30, self.__howToGetPies, self.uniqueName('PieAdvice'))

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

        self.walkStateData.exit()

        self.__clearOnscreenMessage()
        self.ignore('begin-pie')
        localAvatar.setCameraFov(ToontownGlobals.CogHQCameraFov)

    def enterVictory(self):
        if self.victor == 0:
            return

        victor = base.cr.getDo(self.victor)

        def doSfx():
            if self.victor == self.localAvId:
                base.playSfx(self.winSting)
            else:
                base.playSfx(self.loseSting)

        camera.reparentTo(render)
        camera.setPosHpr(0, -125, 8, 180, 0, 0)

        self.victoryTrack = Sequence(
            Parallel(
                ActorInterval(self.boss, "Fb_fall"),
                Sequence(SoundInterval(self.boss.reelSfx, node=self.boss), SoundInterval(self.boss.deathSfx)),
            ),
            Func(camera.reparentTo, victor),
            Func(camera.setPosHpr, 0, 8, victor.getHeight() / 2.0, 180, 0, 0),
            Func(victor.setAnimState, "victory"),
            Func(doSfx),
            Wait(5.0),
            Func(self.gameOver)
        )
        self.victoryTrack.start()

    def exitVictory(self):
        self.victoryTrack.finish()
        del self.victoryTrack
        camera.reparentTo(render)

    def enterCleanup(self):
        self.notify.debug("enterCleanup")

    def exitCleanup(self):
        pass

    """
    Updates sent from server
    """

    def declareVictor(self, avId: int) -> None:
        self.victor = avId
        self.gameFSM.request("victory")

    def setBossCogId(self, bossCogId: int) -> None:
        self.boss = base.cr.getDo(bossCogId)
        self.boss.prepareBossForBattle()

    def cagedToonBattleThree(self, index, avId):
        str = TTLocalizer.CagedToonBattleThree.get(index)
        if str:
            toonName = ''
            if avId:
                toon = self.cr.doId2do.get(avId)
                if not toon:
                    self.cagedToon.clearChat()
                    return
                toonName = toon.getName()
            text = str % {'toon': toonName}
            self.cagedToon.setChatAbsolute(text, CFSpeech | CFTimeout)
        else:
            self.cagedToon.clearChat()

    """
    Misc shit
    """

    def toFinalBattleMode(self):
        self.walkStateData.fsm.request('walking')

    def toOuchMode(self):
        self.walkStateData.fsm.request('ouch')

    def chatClosed(self):
        if self.walkStateData.fsm.getCurrentState().getName() == "walking":
            base.localAvatar.enableAvatarControls()

    def __touchedCage(self, entry):
        self.sendUpdate('touchCage', [])
        self.__clearOnscreenMessage()
        taskMgr.remove(self.uniqueName('PieAdvice'))
        base.playSfx(self.piesRestockSfx)
        if not self.everThrownPie:
            taskMgr.doMethodLater(30, self.__howToThrowPies, self.uniqueName('PieAdvice'))

    def __outOfPies(self):
        self.__showOnscreenMessage(TTLocalizer.BossBattleNeedMorePies)
        taskMgr.doMethodLater(20, self.__howToGetPies, self.uniqueName('PieAdvice'))

    def __howToGetPies(self, task):
        self.__showOnscreenMessage(TTLocalizer.BossBattleHowToGetPies)

    def __howToThrowPies(self, task):
        self.__showOnscreenMessage(TTLocalizer.BossBattleHowToThrowPies)

    def __foundPieButton(self):
        self.everThrownPie = True
        self.__clearOnscreenMessage()
        taskMgr.remove(self.uniqueName('PieAdvice'))

    def __showOnscreenMessage(self, text):
        if self.onscreenMessage:
            self.onscreenMessage.destroy()
            self.onscreenMessage = None
        self.onscreenMessage = DirectLabel(text=text, text_fg=VBase4(1, 1, 1, 1), text_align=TextNode.ACenter,
                                           relief=None, pos=(0, 0, 0.35), scale=0.1)

    def __clearOnscreenMessage(self):
        if self.onscreenMessage:
            self.onscreenMessage.destroy()
            self.onscreenMessage = None

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
