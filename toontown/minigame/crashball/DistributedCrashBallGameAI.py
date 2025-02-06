import random
from decimal import Decimal, getcontext

from direct.distributed.ClockDelta import globalClockDelta
from direct.fsm import ClassicFSM, State
from direct.task.TaskManagerGlobal import taskMgr
from panda3d.ode import OdeCollisionEntry, OdeGeom

from toontown.golf import GolfGlobals
from toontown.minigame.DistributedMinigameAI import DistributedMinigameAI
from toontown.minigame.crashball.CrashBallConstants import InitialScore, GolfBallRadius, GolfBallDensity
from toontown.minigame.crashball.CrashBallGamePhysicsWorld import CrashBallGamePhysicsWorld
from toontown.minigame.crashball.DistributedCrashBallVehicleAI import DistributedCrashBallVehicleAI

# Set precision to be really high!
getcontext().prec = 49


class DistributedCrashBallGameAI(DistributedMinigameAI, CrashBallGamePhysicsWorld):
    # Rate of sending ball physics data (position and velocity) to the client.
    BallDataUpdateRate = 0.05

    def __init__(self, air, minigameId):
        DistributedMinigameAI.__init__(self, air, minigameId)
        CrashBallGamePhysicsWorld.__init__(self, canRender=False)

        self.gameFSM = ClassicFSM.ClassicFSM('DistributedMinigameTemplateAI',
                               [
                                State.State('inactive',
                                            self.enterInactive,
                                            self.exitInactive,
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
                                            ['inactive']),
                                ],
                               # Initial State
                               'inactive',
                               # Final State
                               'inactive',
                               )

        # Add our game ClassicFSM to the framework ClassicFSM
        self.addChildGameFSM(self.gameFSM)

        self.globalBallId = 0
        self.golfBalls = {}
        self.npcPlayerIds = []
        self.vehicles = {}

    def generate(self):
        self.notify.debug("generate")
        DistributedMinigameAI.generate(self)
        self.setupSimulation()

        eventName = self.uniqueName("crashBallCollision")
        self.space.setCollisionEvent(eventName)
        self.accept(eventName, self.handleOdeCollision)

        self.ballSpawnTask = self.uniqueName("crashBall-spawnBalls")

    def cleanup(self) -> None:
        for vehicle in self.vehicles.values():
            vehicle.requestDelete()
        self.vehicles = {}

        for ball in self.golfBalls.values():
            ball["golfBallOdeGeom"].destroy()
        self.golfBalls = {}

    def setExpectedAvatars(self, avIds):
        super().setExpectedAvatars(avIds)
        self.npcPlayerIds = [10 + i for i in range(4 - len(self.avIdList))]

    @property
    def totalPlayerIdList(self) -> list[int]:
        return self.avIdList + self.npcPlayerIds

    def getNpcPlayerIds(self) -> list[int]:
        return self.npcPlayerIds

    # Disable is never called on the AI so we do not define one

    def delete(self):
        self.notify.debug("delete")
        del self.gameFSM
        DistributedMinigameAI.delete(self)

    # override some network message handlers
    def setGameReady(self):
        self.notify.debug("setGameReady")
        DistributedMinigameAI.setGameReady(self)
        # all of the players have checked in
        # they will now be shown the rules

        self.vehicles = {}
        self.tireDict = {}
        for index, avId in enumerate(self.totalPlayerIdList):
            _, _, tireOdeGeom, tireOdeGeom2 = self.createTire(index)

            vehicle = DistributedCrashBallVehicleAI(self.air, self, self.getDoId(), avId, tireOdeGeom, tireOdeGeom2)
            vehicle.generateWithRequired(self.zoneId)
            self.vehicles[avId] = vehicle

    def setGameStart(self, timestamp):
        self.notify.debug("setGameStart")
        # base class will cause gameFSM to enter initial state
        DistributedMinigameAI.setGameStart(self, timestamp)
        # all of the players are ready to start playing the game
        # transition to the appropriate ClassicFSM state
        self.gameFSM.request('play')

    def __spawnBallTask(self, task):
        # Choose a random windmill to "spawn" from.
        windmillIdx = random.randint(0, 3)
        # Choose a random h delta to force the ball towards.
        hVariance = round(random.random() * 30 * random.choice([-1, 1]), 2)

        # Create the ball.
        _, golfBall, odeGeom = self.createSphere(GolfBallDensity, GolfBallRadius, windmillIdx, hVariance)
        self.golfBalls[self.globalBallId] = {
            'golfBall': golfBall,
            'golfBallOdeGeom': odeGeom,
        }
        # Spawn a task to enable the ball.
        taskMgr.doMethodLater(0.6, self.setupInitialBallForce, self.uniqueName(f"crashBallSetup-{self.globalBallId}"),
                              extraArgs=[golfBall, windmillIdx, hVariance])

        serverTime = globalClock.getRealTime() + 0.6
        timestamp = globalClockDelta.localToNetworkTime(serverTime)

        # Also create the ball on the clients.
        self.sendUpdate("spawnGolfBall", [timestamp, windmillIdx, hVariance, self.globalBallId])
        self.globalBallId += 1

        # Set a random delay time.
        task.delayTime = max(random.random() * 3.0, 1.0)
        self.notify.info(f"Spawning another ball in {task.delayTime} seconds...")
        # Repeat the task.
        return task.again

    def handleOdeCollision(self, entry: OdeCollisionEntry) -> None:
        geom1: OdeGeom = entry.getGeom1()
        geom2: OdeGeom = entry.getGeom2()
        if geom1 in self.scoreWalls.values() or geom2 in self.scoreWalls.values():
            ballDict = [ballId for ballId, ballDict in self.golfBalls.items()
                        if ballDict["golfBallOdeGeom"] in (geom1, geom2)]
            if not ballDict:
                return

            if geom1 in self.scoreWalls.values():
                index = list(self.scoreWalls.values()).index(geom1)
            else:
                index = list(self.scoreWalls.values()).index(geom2)
            self.handleScore(ballDict[0], index)
            return

    def handleScore(self, ballId: int, playerIndex: int) -> None:
        # Cleanup and remove the golf ball.
        golfBall = self.golfBalls[ballId]
        golfBall["golfBallOdeGeom"].destroy()
        del self.golfBalls[ballId]

        if playerIndex < len(self.totalPlayerIdList):
            avId = self.totalPlayerIdList[playerIndex]
            score = max(self.scoreDict[avId] - 1, 0)
            self.scoreDict[avId] = score

            # Remove the movement task.
            if score == 0:
                if avId in self.npcPlayerIds:
                    self.vehicles[avId].stopNpcMovement()

                # Enable their respective wall.
                index = self.totalPlayerIdList.index(avId)
                self.walls[index]["wall"].enable()

                # Queue up the wheel to be destroyed.
                self.vehicles[avId].waitToDelete()
        else:
            avId = 0
            score = 0

        self.sendUpdate("deductScore", [ballId, avId, score])

        # Handle lose condition for players.
        # This happens if there are Cogs with score left but all the player toons have been knocked out.
        if all(self.scoreDict[playerId] == 0 for playerId in self.avIdList):
            self.gameFSM.request("WinMovie", [0])
            return

        # Handle win condition for a single player.
        # This happens when the only one with a positive score amount is a player toon.
        playersStillIn = [playerId for playerId in self.totalPlayerIdList if self.scoreDict[playerId] > 0]
        if len(playersStillIn) == 1:
            self.gameFSM.request("WinMovie", [playersStillIn[0]])
            return

    def __sendBallData(self, task) -> None:
        ballData = []
        for ballId, ballDict in self.golfBalls.items():
            pos = ballDict["golfBallOdeGeom"].getPosition()
            vel = ballDict["golfBall"].getLinearVel()
            ballData.append([ballId, *[str(Decimal(item)) for item in (pos[0], pos[1], pos[2], vel[0], vel[1], vel[2])]])

        self.sendUpdate("sendBallData", [ballData])
        return task.again

    def setGameAbort(self):
        self.notify.debug("setGameAbort")
        # this is called when the minigame is unexpectedly
        # ended (a player got disconnected, etc.)
        if self.gameFSM.getCurrentState():
            self.gameFSM.request('cleanup')

        self.cleanup()

        DistributedMinigameAI.setGameAbort(self)

    def gameOver(self):
        self.notify.debug("gameOver")
        # call this when the game is done
        # clean things up in this class
        if hasattr(self, "gameFSM"):
            self.gameFSM.request('cleanup')
        # tell the base class to wrap things up
        DistributedMinigameAI.gameOver(self)

    def enterInactive(self):
        self.notify.debug("enterInactive")

    def exitInactive(self):
        pass

    def enterPlay(self):
        self.notify.debug("enterPlay")

        # reset scores
        self.scoreDict = {avId: InitialScore for avId in self.totalPlayerIdList}

        # Spin up a task which will spawn the golf balls.
        taskMgr.doMethodLater(random.random(), self.__spawnBallTask, self.ballSpawnTask)

        # Spawn a movement task for each npc player.
        for npcId in self.npcPlayerIds:
            self.vehicles[npcId].startNpcMovement()
            self.vehicles[npcId].updateSendVehicleX()

        # Begin the physics simulation. This should persist through the entire game.
        self.startSim()

        taskMgr.doMethodLater(self.BallDataUpdateRate, self.__sendBallData, self.uniqueName("crashBallSendData"))

    def exitPlay(self):
        # End the physics simulation now that the game is done.
        self.stopSim()

        # Cleanup spawn ball task.
        taskMgr.remove(self.ballSpawnTask)
        # Cleanup npc player tasks.
        for npcId in self.npcPlayerIds:
            self.vehicles[npcId].stopNpcMovement()

    def enterWinMovie(self, winnerId: int) -> None:
        self.sendUpdate("setWinner", [winnerId])
        # End the game when the win movie is over.
        taskMgr.doMethodLater(5, self.gameOver, self.uniqueName("crashBall-exitWinners"), extraArgs=[])

    def exitWinMovie(self) -> None:
        pass

    def enterCleanup(self):
        self.notify.debug("enterCleanup")
        self.cleanup()

        self.gameFSM.request('inactive')

    def exitCleanup(self):
        pass
