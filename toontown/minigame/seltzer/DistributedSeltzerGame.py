from direct.distributed import DistributedSmoothNode
from direct.fsm.ClassicFSM import ClassicFSM
from direct.fsm.State import State
from direct.interval.FunctionInterval import Func, Wait
from direct.interval.MetaInterval import Sequence
from panda3d.core import CollisionPlane, Plane, Vec3, Point3, CollisionNode

from libotp.nametag import NametagGlobals
from toontown.coghq import SeltzerLeagueGlobals
from toontown.coghq.BossSpeedrunTimer import BossSpeedrunTimer
from toontown.coghq.CogBossScoreboard import CogBossScoreboard
from toontown.minigame.DistributedMinigame import DistributedMinigame
from toontown.minigame.craning.CraneWalk import CraneWalk
from toontown.suit import BossCogGlobals
from toontown.toonbase import TTLocalizer, ToontownGlobals


class DistributedSeltzerGame(DistributedMinigame):

    # define constants that you won't want to tweak here

    def __init__(self, cr):
        super().__init__(cr)

        self.walkStateData = CraneWalk('walkDone')

        self.bossSpeedrunTimer = BossSpeedrunTimer()
        self.bossSpeedrunTimer.hide()

        self.scoreboard = CogBossScoreboard()
        self.scoreboard.hide()

        self.boss = None
        self.belts = [None, None]
        self.tables = {}
        self.golfSpots = {}

        self.victor = 0

        self.gameFSM = ClassicFSM(self.__class__.__name__,
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
        return TTLocalizer.SeltzerGameTitle

    def getInstructions(self):
        return TTLocalizer.SeltzerGameInstructions

    def getMaxDuration(self):
        # how many seconds can this minigame possibly last (within reason)?
        # this is for debugging only
        return 0

    def load(self):
        self.notify.debug("load")
        super().load()
        # load resources and create objects here
        self.music = base.loader.loadMusic('phase_12/audio/bgm/BossBot_CEO_v2.ogg')
        self.winSting = base.loader.loadSfx("phase_4/audio/sfx/MG_win.ogg")
        self.loseSting = base.loader.loadSfx("phase_4/audio/sfx/MG_lose.ogg")
        self.pickupFoodSfx = loader.loadSfx('phase_6/audio/sfx/SZ_MM_gliss.ogg')

        self.geom = loader.loadModel('phase_12/models/bossbotHQ/BanquetInterior_1')
        self.banquetDoor = self.geom.find('**/door3')
        plane = CollisionPlane(Plane(Vec3(0, 0, 1), Point3(0, 0, -50)))
        planeNode = CollisionNode('dropPlane')
        planeNode.addSolid(plane)
        planeNode.setCollideMask(ToontownGlobals.PieBitmask)
        self.geom.attachNewNode(planeNode)
        self.geom.reparentTo(render)

    def unload(self):
        self.notify.debug("unload")
        super().unload()
        # unload resources and delete objects from load() here
        # remove our game ClassicFSM from the framework ClassicFSM
        self.removeChildGameFSM(self.gameFSM)
        del self.gameFSM

        self.music.stop()
        del self.music

        for belt in self.belts:
            if belt:
                belt.cleanup()

        for spot in self.golfSpots.values():
            if spot:
                spot.cleanup()

        self.golfSpots = {}
        self.geom.removeNode()
        del self.geom

        self.scoreboard.cleanup()
        del self.scoreboard

        self.bossSpeedrunTimer.cleanup()
        del self.bossSpeedrunTimer

        localAvatar.chatMgr.chatInputSpeedChat.removeCEOMenu()

    def onstage(self):
        self.notify.debug("onstage")
        super().onstage()
        # start up the minigame; parent things to render, start playing
        # music...
        # at this point we cannot yet show the remote players' toons
        base.localAvatar.reparentTo(render)
        base.localAvatar.setPosHpr(0, 90, 0, 0, 0, 0)
        base.localAvatar.loop('neutral')
        localAvatar.setCameraFov(ToontownGlobals.CogHQCameraFov)
        base.camLens.setNearFar(ToontownGlobals.CogHQCameraNear, ToontownGlobals.CogHQCameraFar)
        base.transitions.irisIn(0.4)
        NametagGlobals.setMasterArrowsOn(1)
        camera.reparentTo(render)

        camera.setPosHpr(0, 90, 15, 0, 0, 0)

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

        # Enable the special CEO chat menu.
        localAvatar.chatMgr.chatInputSpeedChat.addCEOMenu()

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

        self.accept("LocalSetFinalBattleMode", self.toFinalBattleMode)
        self.accept("LocalSetOuchMode", self.toOuchMode)
        self.accept("LocalSetSquishedMode", self.toSquishedMode)
        self.accept("ChatMgr-enterMainMenu", self.chatClosed)

        base.playMusic(self.music, looping=1, volume=0.9)
        localAvatar.setCameraFov(ToontownGlobals.BossBattleCameraFov)

        # Display Boss Timer
        self.bossSpeedrunTimer.reset()
        self.bossSpeedrunTimer.start_updating()
        self.bossSpeedrunTimer.show()

        # Setup the scoreboard
        self.scoreboard.clearToons()
        self.scoreboard.show()
        for avId in self.avIdList:
            if avId in base.cr.doId2do:
                self.scoreboard.addToon(avId)

    def exitPlay(self):
        if self.boss is not None:
            self.boss.cleanupBossBattle()

        self.walkStateData.exit()

        self.ignoreAll()
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

        self.victoryTrack = Sequence(
            self.boss.makeVictoryMovie(),
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
    Misc
    """

    def setBossCogId(self, bossCogId: int) -> None:
        self.boss = base.cr.getDo(bossCogId)
        self.boss.game = self
        self.boss.prepareBossForBattle()

    def declareVictor(self, avId: int) -> None:
        self.victor = avId
        self.gameFSM.request("victory")

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

    def toCraneMode(self):
        if self.gameFSM.getCurrentState().getName() != "play":
            return
        self.walkStateData.fsm.request('crane')

    def toMovieMode(self):
        if self.gameFSM.getCurrentState().getName() != "play":
            return
        self.walkStateData.fsm.request('movie')

    def toFinalBattleMode(self, checkForOuch: bool = False):
        if self.gameFSM.getCurrentState().getName() != "play":
            return
        if not checkForOuch or self.walkStateData.fsm.getCurrentState().getName() != 'ouch':
            self.walkStateData.fsm.request('walking')

    def toOuchMode(self):
        if self.gameFSM.getCurrentState().getName() != "play":
            return
        self.walkStateData.fsm.request('ouch')

    def toSquishedMode(self):
        if self.gameFSM.getCurrentState().getName() != "play":
            return
        self.walkStateData.fsm.request('squished')

    def chatClosed(self):
        if self.walkStateData.fsm.getCurrentState().getName() == "walking":
            base.localAvatar.enableAvatarControls()

    def updateRequiredElements(self):
        if self.bossSpeedrunTimer:
            self.bossSpeedrunTimer.cleanup()

        self.bossSpeedrunTimer = BossSpeedrunTimer()
        self.bossSpeedrunTimer.hide()
        # self.heatDisplay.update(self.calculateHeat(), self.modifiers)

    def setRawRuleset(self, attrs):
        self.ruleset = SeltzerLeagueGlobals.CEORuleset.fromStruct(attrs)
        self.updateRequiredElements()
        print(('ruleset updated: ' + str(self.ruleset)))

    def getRawRuleset(self):
        return self.ruleset.asStruct()

    def getRuleset(self):
        return self.ruleset

    def setBelt(self, belt, beltIndex):
        if beltIndex < len(self.belts):
            self.belts[beltIndex] = belt

    def setTable(self, table, tableIndex):
        self.tables[tableIndex] = table

    def setGolfSpot(self, golfSpot, golfSpotIndex):
        self.golfSpots[golfSpotIndex] = golfSpot

    def localToonTouchedBeltToonup(self, beltIndex, toonupIndex, toonupNum):
        self.sendUpdate('requestGetToonup', [beltIndex, toonupIndex, toonupNum])

    def getBoss(self):
        return self.boss
