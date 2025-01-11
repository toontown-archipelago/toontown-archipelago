import random

from direct.distributed.ClockDelta import globalClockDelta
from direct.fsm import ClassicFSM
from direct.fsm import State
from direct.interval.ActorInterval import ActorInterval
from direct.interval.FunctionInterval import Func, Wait
from direct.interval.LerpInterval import LerpPosInterval, LerpScaleInterval, \
    LerpPosHprInterval, LerpPosQuatInterval
from direct.interval.MetaInterval import Sequence, Parallel
from direct.task.Task import Task
from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import NodePath, Vec4, CompassEffect, Texture, CardMaker, Quat
from panda3d.ode import OdeGeom, OdeBody

from toontown.hood import SkyUtil
from toontown.minigame.ArrowKeys import ArrowKeys
from toontown.minigame.DistributedMinigame import DistributedMinigame
from toontown.minigame.MinigameAvatarScorePanel import MinigameAvatarScorePanel
from toontown.minigame.crashball.CrashBallConstants import CrashBallNPCChoices, CrashBallSkyFiles, InitialScore, \
    GolfBallRadius, GolfBallDensity
from toontown.minigame.crashball.CrashBallGamePhysicsWorld import CrashBallGamePhysicsWorld
from toontown.suit.Suit import Suit
from toontown.suit.SuitDNA import SuitDNA
from toontown.toonbase import TTLocalizer, ToontownGlobals


class DistributedCrashBallGame(DistributedMinigame, CrashBallGamePhysicsWorld):
    # define constants that you won't want to tweak here
    CameraPosHpr = (0, -14, 14, 0, -30, 0)

    CloudPositions = {
        0: (-5, 5, -2),
        1: (5, -5, -2),
        2: (-5, -5, -2),
        3: (5, 5, -2)
    }

    ArrowPositions = {
        0: (6, 6, 0, 135, -90, 0),  # near right
        1: (-6, 6, 0, -135, -90, 0),  # far right
        2: (6, -6, 0, 45, -90, 0),  # near left
        3: (-6, -6, 0, 315, -90, 0)  # far left
    }

    Arrow_Black = (0.2, 0.2, 0.2, 1.0)
    Arrow_Green = (0.55, 0.95, 0.55, 1.0)

    def __init__(self, cr):
        DistributedMinigame.__init__(self, cr)
        CrashBallGamePhysicsWorld.__init__(self, canRender=True)

        self.gameFSM = ClassicFSM.ClassicFSM('DistributedMinigameTemplate',
                                             [
                                                 State.State('off',
                                                             self.enterOff,
                                                             self.exitOff,
                                                             ['play']),
                                                 State.State('play',
                                                             self.enterPlay,
                                                             self.exitPlay,
                                                             ['WinMovie', 'cleanup']),
                                                 State.State('WinMovie',
                                                             self.enterWinMovie,
                                                             self.exitWinMovie,
                                                             ['cleanup']),
                                                 State.State('cleanup',
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

        self.notify.setDebug(True)

        self.lastForceArrowUpdateTime = 0
        self.npcPlayerIds = []
        self.npcPlayers = {}
        self.vehicles = {}
        self.golfBalls = {}
        self.golfBallSpawnTracks = {}

    def getTitle(self):
        return TTLocalizer.CrashBallGameTitle

    def getInstructions(self):
        return TTLocalizer.CrashBallGameInstructions

    def getMaxDuration(self):
        # how many seconds can this minigame possibly last (within reason)?
        # this is for debugging only
        return 0

    def setNpcPlayerIds(self, npcIds: list[int]) -> None:
        self.npcPlayerIds = npcIds

    @property
    def totalPlayerIdList(self) -> list[int]:
        return self.avIdList + self.npcPlayerIds

    def load(self):
        self.notify.debug("load")
        DistributedMinigame.load(self)
        # load resources and create objects here
        self.music = base.loader.loadMusic("phase_4/audio/bgm/MG_CrashBall.ogg")
        self.winSting = base.loader.loadSfx("phase_4/audio/sfx/MG_win.ogg")
        self.loseSting = base.loader.loadSfx("phase_4/audio/sfx/MG_lose.ogg")
        self.tireHit = loader.loadSfx("phase_4/audio/sfx/Golf_Hit_Barrier_1.ogg")
        self.wallHit = loader.loadSfx("phase_4/audio/sfx/MG_maze_pickup.ogg")

        self.arrowKeys = ArrowKeys()

        # Load the environment
        cloudModel = loader.loadModel("phase_5.5/models/estate/bumper_cloud")
        cloudModel.setScale(12, 12, 1)

        self.clouds = []
        for i in self.CloudPositions:
            cloud = cloudModel.copyTo(NodePath())
            cloud.setPos(*self.CloudPositions[i])
            cloud.setColorScale(0.8, 0.8, 0.8, 1)
            self.clouds.append(cloud)

        windmillModel = loader.loadModel("phase_6/models/golf/windmill")
        # windmillModel.find("**/windmillFan0").setHpr(0, -45, 0)

        self.windmills = []
        for i in self.WindmillPositions:
            windmill = windmillModel.copyTo(NodePath())
            windmill.setPosHpr(*self.WindmillPositions[i])
            self.windmills.append(windmill)

        self.boostArrowTexture = loader.loadTexture("phase_4/maps/greyscale_arrow.png")
        self.boostArrowTexture.setMinfilter(Texture.FTLinear)

        self.arrows = {}
        for i in self.ArrowPositions:
            arrowParent, arrow, arrow2, arrow3 = self.genArrow()
            arrowParent.setPosHpr(*self.ArrowPositions[i])
            arrowParent.setScale(1.5)
            self.arrows[i] = (arrowParent, arrow, arrow2, arrow3)

        self.toonNodes = {}
        for i in self.ToonNodePosHprs:
            node = render.attachNewNode(f"crashBallNode-{i}")
            node.setPosHpr(*self.ToonNodePosHprs[i])
            self.toonNodes[i] = node

        cloudModel.removeNode()

        self.sky = loader.loadModel(CrashBallSkyFiles[self.getSafezoneId()])
        self.sky.setZ(-300)
        self.sky.setScale(2.0)

        self.setupSimulation()

        self.dropShadowModel = loader.loadModel(
            "phase_3/models/props/drop_shadow")
        self.dropShadowModel.setColor(0, 0, 0, 0.5)
        self.dropShadowModel.flattenMedium()
        self.dropShadowModel.hide()

        self.golfBalls = {}
        self.scorePanels = {}

    def unload(self):
        self.notify.debug("unload")
        DistributedMinigame.unload(self)
        # unload resources and delete objects from load() here
        # remove our game ClassicFSM from the framework ClassicFSM
        self.removeChildGameFSM(self.gameFSM)
        del self.gameFSM

    def skyTrack(self, task):
        return SkyUtil.cloudSkyTrack(task)

    def onstage(self):
        self.notify.debug("onstage")
        DistributedMinigame.onstage(self)
        # start up the minigame; parent things to render, start playing
        # music...
        # at this point we cannot yet show the remote players' toons
        [cloud.reparentTo(render) for cloud in self.clouds]
        [windmill.reparentTo(render) for windmill in self.windmills]
        [arrow[0].reparentTo(render) for arrow in self.arrows.values()]

        self.startSky()

        base.setBackgroundColor(Vec4(0.6, 0.77, 0.94, 1))

        self.moveCameraToTop()

        # Start music
        base.playMusic(self.music, looping = 1, volume = 0.8)

    def offstage(self):
        self.notify.debug("offstage")
        # stop the minigame; parent things to hidden, stop the
        # music...

        taskMgr.remove("skyTrack")

        for panel in self.scorePanels.values():
            panel.cleanup()
        del self.scorePanels

        self.sky.removeNode()
        del self.sky

        # Stop music
        self.music.stop()
        del self.music

        del self.winSting
        del self.loseSting
        del self.tireHit
        del self.wallHit

        for cloud in self.clouds:
            cloud.removeNode()
        self.clouds = []

        for windmill in self.windmills:
            windmill.removeNode()
        self.windmills = []

        for arrow in self.arrows.values():
            arrow[0].removeNode()
        self.arrows = {}

        for wall in self.walls.values():
            wall["wall"].destroy()
            wall["wallNode"].removeNode()

        self.walls = {}

        base.setBackgroundColor(ToontownGlobals.DefaultBackgroundColor)

        # the base class parents the toons to hidden, so consider
        # calling it last
        DistributedMinigame.offstage(self)

    def handleDisabledAvatar(self, avId):
        """This will be called if an avatar exits unexpectedly"""
        self.notify.debug("handleDisabledAvatar")
        self.notify.debug("avatar " + str(avId) + " disabled")
        # clean up any references to the disabled avatar before he disappears

        # then call the base class
        DistributedMinigame.handleDisabledAvatar(self, avId)

    def setGameReady(self):
        if not self.hasLocalToon: return
        self.notify.debug("setGameReady")
        if DistributedMinigame.setGameReady(self):
            return
        # all of the remote toons have joined the game;
        # it's safe to show them now.
        for index, avId in enumerate(self.avIdList):
            # Find the actual avatar in the cr
            toon = self.getAvatar(avId)
            if toon is None:
                continue
            toon.reparentTo(render)
            toon.forwardSpeed = 0
            toon.rotateSpeed = False
            # toon.setAnimState('Happy', 1.0)
            # Start the smoothing task.
            # toon.startSmooth()
            # hide their dropshadows again
            toon.dropShadow.hide()
            toon.setAnimState('Sit')
            if avId in self.vehicles:
                toon.reparentTo(self.vehicles[avId].getNode())
                toon.setPosHpr(0, 1.0, -2.5, 0, 0, 0)
            toon.stopLookAround()

        npcRng = random.Random()
        npcRng.seed(self.getDoId())

        choices = list(CrashBallNPCChoices[self.getSafezoneId()])
        npcRng.shuffle(choices)

        self.npcPlayers = {}
        for index, npcId in enumerate(self.npcPlayerIds, start=len(self.avIdList)):
            suit = Suit()
            dna = SuitDNA()
            dna.newSuit(choices[index])
            suit.setDNA(dna)
            suit.loop("sit")
            self.npcPlayers[npcId] = suit

            if npcId in self.vehicles:
                suit.reparentTo(self.vehicles[npcId].getNode())
                suit.setPosHpr(0.25, 1.0, -3.0, 0, 0, 0)

    def setGameStart(self, timestamp):
        if not self.hasLocalToon: return
        self.notify.debug("setGameStart")
        # base class will cause gameFSM to enter initial state
        DistributedMinigame.setGameStart(self, timestamp)
        # all players have finished reading the rules,
        # and are ready to start playing.
        # transition to the appropriate state
        self.gameFSM.request("play")

    def getAvatar(self, avId):
        if avId in self.npcPlayers:
            return self.npcPlayers[avId]
        return super().getAvatar(avId)

    def moveCameraToTop(self):
        myPos = self.avIdList.index(self.localAvId)
        toonNode = self.toonNodes[myPos]
        camera.reparentTo(toonNode)
        camera.setPosHpr(*self.CameraPosHpr)
        # base.localAvatar.setPosHpr(*toonNode.getPos(), *toonNode.getHpr())
        # base.localAvatar.reparentTo(render)
        base.camLens.setFar(1200)

    def startSky(self):
        # Turn off depth tests on the sky because as the cloud layers interpenetrate
        # we do not want to see the polys cutoff. Since there is nothing behing them
        # we can get away with this.
        self.sky.setDepthTest(0)
        self.sky.setDepthWrite(0)
        self.sky.setBin("background", 100)
        # Make sure they are drawn in the correct order in the hierarchy
        # The sky should be first, then the clouds
        self.sky.find("**/Sky").reparentTo(self.sky, -1)

        # Nowadays we use a CompassEffect to counter-rotate the sky
        # automatically at render time, rather than depending on a
        # task to do this just before the scene is rendered.
        self.sky.reparentTo(render)
        self.sky.setHpr(0.0, 0.0, 0.0)
        ce = CompassEffect.make(NodePath(), CompassEffect.PRot | CompassEffect.PZ)
        self.sky.node().setEffect(ce)

        # Even with the CompassEffect, we still need the task to spin
        # the clouds.

        skyTrackTask = Task(self.skyTrack)
        # Store the clouds and h value so the task has access to it
        skyTrackTask.h = 0
        skyTrackTask.cloud1 = self.sky.find("**/cloud1")
        skyTrackTask.cloud2 = self.sky.find("**/cloud2")

        if (not skyTrackTask.cloud1.isEmpty()) and (not skyTrackTask.cloud2.isEmpty()):
            taskMgr.add(skyTrackTask, "skyTrack")
        else:
            self.notify.warning("Couldn't find clouds!")

    def genArrow(self):
        factory = CardMaker("factory")
        factory.setFrame(-1.0, 1.0, -.5, .5)
        arrowRoot = render.attachNewNode("CrashBallArrow")

        arrows = []
        for i in range(3):
            arrow = arrowRoot.attachNewNode(factory.generate())
            arrow.setTransparency(1)
            arrow.setTexture(self.boostArrowTexture)
            arrow.setPos(0, 0, i)
            arrow.setColorScale(self.Arrow_Black)
            arrows.append(arrow)

        return arrowRoot, *arrows

    def spawnGolfBall(self, timestamp: int, windmillIdx: int, hVariance: float, ballId: int) -> None:
        """
        Respond to a request from the server to create a new golf ball from the specified windmill index.
        """
        if self.gameFSM.getCurrentState().getName() != "play":
            return

        ts = globalClockDelta.localElapsedTime(timestamp)

        arrows = self.arrows[windmillIdx]

        def cleanupTrack():
            self.golfBallSpawnTracks[ballId].finish()
            del self.golfBallSpawnTracks[ballId]
        
        colorWaitTime = 0.2
        arrowColorTrack = Sequence(
            Func(arrows[1].clearColorScale),
            Func(arrows[1].setColorScale, self.Arrow_Green),
            Wait(colorWaitTime),

            Func(arrows[2].clearColorScale),
            Func(arrows[2].setColorScale, self.Arrow_Green),
            Wait(colorWaitTime),

            Func(arrows[3].clearColorScale),
            Func(arrows[3].setColorScale, self.Arrow_Green),
            Wait(colorWaitTime),
        )
        self.golfBallSpawnTracks[ballId] = Sequence(
            arrowColorTrack,
            Func(self.setupBall, windmillIdx, hVariance, ballId),

            Func(arrows[1].setColorScale, self.Arrow_Black),
            Func(arrows[2].setColorScale, self.Arrow_Black),
            Func(arrows[3].setColorScale, self.Arrow_Black),

            Func(cleanupTrack)
        )
        self.golfBallSpawnTracks[ballId].start(ts)

    def setupBall(self, windmillIdx: int, hVariance: float, ballId: int) -> None:
        golfBallGeom, golfBall, odeGeom = self.createSphere(GolfBallDensity, GolfBallRadius, windmillIdx, hVariance)
        self.setupInitialBallForce(golfBall, windmillIdx, hVariance)

        shadow = self.dropShadowModel.copyTo(golfBallGeom)
        shadow.setBin('shadow', 100)
        shadow.setScale(0.09)
        shadow.setDepthWrite(False)
        shadow.setDepthTest(True)
        shadow.hide()

        golfBallGeom.setName(f'golfBallGeom-{ballId}')
        golfBallGeom.setColor(1.0, 1.0, 1.0, 1)

        self.golfBalls[ballId] = {
            'golfBall': golfBall,
            'golfBallGeom': golfBallGeom,
            'golfBallOdeGeom': odeGeom,
            'golfBallShadow': shadow,
        }

    def deductScore(self, ballId: int, avId: int, scoreVal: int) -> None:
        if avId != 0 and self.scores[avId] > 0:
            # Kill them.
            if not scoreVal:
                # Kill their controls if the local toon was the one that lost.
                if avId == self.localAvId:
                    self.getLocalVehicle().disableControls()
                    camera.wrtReparentTo(render)
                else:
                    self.vehicles[avId].stopSmooth()

                avatar = self.getAvatar(avId)
                np = self.vehicles[avId].tireNodePath
                self.vehicles[avId].disappearTrack = Sequence(
                    Parallel(
                        LerpScaleInterval(np, 0.7, 0.01),
                        LerpScaleInterval(avatar, 0.7, 0.01),
                    ),
                    Func(avatar.hide),
                    Func(avatar.setScale, 1.0)
                )
                self.vehicles[avId].disappearTrack.start()

                # Enable their respective wall.
                index = self.totalPlayerIdList.index(avId)
                self.walls[index]["wall"].enable()
                self.walls[index]["wallNode"].show()

            self.scores[avId] = scoreVal
            self.scorePanels[avId].setScore(self.scores[avId])

        ballDict = [(b, bDict) for b, bDict in self.golfBalls.items() if b == ballId]
        if not ballDict:
            return

        ballId, ballDesc = ballDict[0]

        ballDesc["golfBallOdeGeom"].destroy()
        ballDesc["golfBallGeom"].removeNode()
        del self.golfBalls[ballId]

    def setWinner(self, winnerId: int) -> None:
        self.gameFSM.request("WinMovie", [winnerId])

    def sendBallData(self, ballData) -> None:
        for ballId, x, y, z, xVel, yVel, zVel in ballData:
            if ballId not in self.golfBalls:
                continue

            ballDesc = self.golfBalls[ballId]
            ae: OdeGeom = ballDesc["golfBallOdeGeom"]
            ae.setPosition(float(x), float(y), float(z))
            aoe: OdeBody = ballDesc["golfBall"]
            aoe.setLinearVel(float(xVel), float(yVel), float(zVel))

    def getLocalVehicle(self):
        return self.vehicles[self.localAvId]

    def postStep(self):
        """Play sounds as needed after one simulation step."""
        super().postStep()

        # self.notify.debug('in post step --------------------------')
        for entry in self.colEntries:
            c0, c1 = self.getOrderedContacts(entry)
            if c1 == self.ballCollideId:
                if c0 in (self.ballCollideId, self.tireCollideId, self.extraKickCollideId):
                    self.tireHit.play()
                elif c0 == self.windmillCollideId or c0 in self.wallCollideIds:
                    self.wallHit.play()
            elif c0 == self.ballCollideId:
                if c1 in (self.ballCollideId, self.tireCollideId, self.extraKickCollideId):
                    self.tireHit.play()
                elif c1 == self.windmillCollideId or c1 in self.wallCollideIds:
                    self.wallHit.play()

    # these are enter and exit functions for the game's
    # fsm (finite state machine)

    def enterOff(self):
        self.notify.debug("enterOff")

    def exitOff(self):
        pass

    def enterPlay(self):
        self.notify.debug("enterPlay")

        # Initialize the scoreboard w/ 15 score per player.
        self.scores = {avId: InitialScore for avId in self.totalPlayerIdList}
        spacing = .4
        for i, avId in enumerate(self.totalPlayerIdList):
            avName = self.getAvatarName(avId)
            scorePanel = MinigameAvatarScorePanel(avId, avName,
                                                  avatar=self.npcPlayers[avId] if avId in self.npcPlayerIds else None)
            scorePanel.setScore(self.scores[avId])
            scorePanel.setScale(.9)
            scorePanel.setPos(.75 - spacing * ((len(self.totalPlayerIdList) - 1) - i), 0.0, .875)
            # make the panels slightly transparent
            scorePanel.makeTransparent(.75)
            self.scorePanels[avId] = scorePanel

        # Enable controls for the local avatar.
        self.getLocalVehicle().enableControls()

        # Begin smoothing for other vehicles.
        for avId, vehicle in self.vehicles.items():
            if avId == self.localAvId:
                continue

            vehicle.startSmooth()

        # Begin the physics simulation. This should persist through the entire game.
        self.startSim()

    def exitPlay(self):
        # End the physics simulation now that the game is done.
        self.stopSim()

        # Stop the local toon movement.
        if self.vehicles:
            self.getLocalVehicle().disableControls()

        for track in list(self.golfBallSpawnTracks.values()):
            track.finish()
        self.golfBallSpawnTracks = {}

        for ballDict in self.golfBalls.values():
            ballDict["golfBallOdeGeom"].destroy()
            ballDict["golfBallGeom"].removeNode()
            ballDict["golfBallShadow"].removeNode()

        self.golfBalls = {}

    def enterWinMovie(self, winnerId: int):
        winner = self.getAvatar(winnerId)
        if winnerId == self.localAvId:
            base.playSfx(self.winSting)
        else:
            base.playSfx(self.loseSting)

        camera.wrtReparentTo(render)

        self.winSequence = Parallel()
        if winner is not None:
            winner.wrtReparentTo(render)
            np = self.vehicles[winnerId].getNode()
            np.wrtReparentTo(render)
            cQuat = Quat()
            cQuat.setHpr((180, -30, 0))
            self.winSequence.append(
                Parallel(
                    ActorInterval(actor=winner, animName='victory', duration=5.5),
                    LerpPosHprInterval(winner, 1.0, (0, 0, 0), (0, 0, 0)),
                    LerpPosInterval(np, 1.0, (0, 0, np.getZ())),
                    LerpPosQuatInterval(camera, 1.0, (0, 10, 7), cQuat)
                )
            )

        self.winSequence.append(Sequence(Wait(5.0), Func(self.gameOver)))
        self.winSequence.start()

    def exitWinMovie(self):
        self.winSequence.finish()
        del self.winSequence

    def enterCleanup(self):
        self.notify.debug("enterCleanup")

        for suit in self.npcPlayers.values():
            suit.delete()
        self.npcPlayers = {}

    def exitCleanup(self):
        pass
