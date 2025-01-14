import random
from operator import itemgetter

from direct.distributed.ClockDelta import globalClockDelta
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.interval.FunctionInterval import Func
from direct.interval.LerpInterval import LerpFunctionInterval
from direct.interval.MetaInterval import Sequence
from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import Vec3, NodePath
from panda3d.ode import OdeBody

from toontown.minigame import IceGameGlobals


class DistributedCrashBallVehicleAI(DistributedObjectAI):
    # Store which index moves against which axis.
    PlayerAxis = {
        0: 1,  # y
        1: 1,  # y
        2: 0,  # x
        3: 0   # x
    }

    PlayerMovementLine = {
        0: ((10, -5.5), (10, 5.5)),
        1: ((-10, -5.5), (-10, 5.5)),
        2: ((-5.5, -10), (5.5, -10)),
        3: ((-5.5, 10), (5.5, 10))
    }
    ToonNodePosHprs = {
        0: (10, 0, 2, 90, 0, 0),
        1: (-10, 0, 2, -90, 0, 0),
        2: (0, -10, 2, 0, 0, 0),
        3: (0, 10, 2, 180, 0, 0)
    }

    def __init__(self, air, minigame, minigameId: int, controllerId: int, tireOdeGeom, extraKickOdeGeom) -> None:
        super().__init__(air)

        self.minigame = minigame
        self.minigameId = minigameId
        self.controllerId = controllerId
        self.tireOdeGeom = tireOdeGeom
        self.extraKickOdeGeom = extraKickOdeGeom

        self.node = None

        self.destinationX = 0.0
        self.isFastMoving = False
        self.useExtraKick = False
        self.lastUsedExtraKick = 0.0

        self.deleted = False

    def announceGenerate(self):
        super().announceGenerate()

        self.node = NodePath(self.uniqueName("CrashBallVehicle"))
        self.node.setPosHpr(*self.ToonNodePosHprs[self.getControllerIndex()])
        self.tireOdeGeom.setPosition(*self.node.getPos())
        self.extraKickOdeGeom.setPosition(*self.node.getPos())

    def delete(self) -> None:
        self.stopNpcMovement()
        taskMgr.remove(self.uniqueName("crashBallVehicleDelete"))

        self.node.removeNode()
        del self.node
        self.tireOdeGeom.destroy()
        del self.tireOdeGeom
        self.extraKickOdeGeom.destroy()
        del self.extraKickOdeGeom

        del self.minigame

        self.deleted = True

        super().delete()

    def getMinigameId(self) -> int:
        return self.minigameId

    def getControllerId(self) -> int:
        return self.controllerId

    def getPlayerAxis(self):
        return self.PlayerAxis[self.getControllerIndex()]

    def getControllerIndex(self) -> int:
        return self.minigame.totalPlayerIdList.index(self.controllerId)

    def startNpcMovement(self) -> None:
        # Task for the movement tick.
        taskMgr.doMethodLater(random.random(), self.__npcDetermineNextMove,
                              self.uniqueName(f"crashBallNpc-{self.controllerId}"))

        # Task for adjusting the npc's x value.
        taskMgr.add(self.__npcMoveTask, self.uniqueName(f"crashBallMoveNpc-{self.controllerId}"))

    def stopNpcMovement(self) -> None:
        taskMgr.remove(self.uniqueName(f"crashBallNpc-{self.controllerId}"))
        taskMgr.remove(self.uniqueName(f"crashBallMoveNpc-{self.controllerId}"))

    def waitToDelete(self) -> None:
        taskMgr.doMethodLater(1.0, self.requestDelete, self.uniqueName("crashBallVehicleDelete"), extraArgs=[])

    def setVehicleX(self, x: float, timestamp: int) -> None:
        if self.deleted:
            return

        if self.getPlayerAxis() == 1:
            self.node.setY(x)
        else:
            self.node.setX(x)

        self.tireOdeGeom.setPosition(*self.node.getPos())
        self.extraKickOdeGeom.setPosition(*self.node.getPos())

    def __localShowExtraKick(self) -> None:
        # Send to the clients.
        serverTime = globalClock.getRealTime()
        timestamp = globalClockDelta.localToNetworkTime(serverTime)
        self.sendUpdate("showExtraKick", [timestamp])
        # Process the extra kick locally.
        self.showExtraKick()

    def __calculateLineIntersection(self, targetAxis: int, pointA: tuple[float, float], pointB: tuple[float, float],
                                    pointC: tuple[float, float], pointD: tuple[float, float],
                                    ) -> tuple[float, float] | None:
        # Line AB represented as a1x + b1y = c1
        a1 = pointB[1] - pointA[1]
        b1 = pointA[0] - pointB[0]
        c1 = (a1 * pointA[0]) + (b1 * pointA[1])

        # Line CD represented as a2x + b2y = c2
        a2 = pointD[1] - pointC[1]
        b2 = pointC[0] - pointD[0]
        c2 = (a2 * pointC[0]) + (b2 * pointC[1])

        determinant = (a1 * b2) - (a2 * b1)
        if determinant == 0:
            return

        x = (b2 * c1 - b1 * c2) / determinant
        y = (a1 * c2 - a2 * c1) / determinant
        intersection = (x, y)

        # The line segment does not intersect with the target's movement axis.
        if not pointC[targetAxis] <= intersection[targetAxis] <= pointD[targetAxis]:
            return

        return intersection

    def __npcDetermineNextMove(self, task):
        playerPos = self.node.getPos()
        playerAxis = self.getPlayerAxis()

        now = globalClock.getRealTime()

        if self.useExtraKick:
            self.__localShowExtraKick()
            self.lastUsedExtraKick = now
            self.useExtraKick = False

        xValues = []
        for ballId, ball in self.minigame.golfBalls.items():
            odeGeomBody: OdeBody = ball["golfBall"]
            pos = odeGeomBody.getPosition()
            lVel = odeGeomBody.getLinearVel()
            xVel, yVel = lVel[0] / 5, lVel[1] / 5
            if not xVel or not yVel:
                continue

            slope = yVel / xVel
            nextPos = Vec3(playerPos[0] + lVel[0], playerPos[1] + lVel[1], 0)
            # Calculate the point of intersection between the ball's movement trajectory and
            # the npc player's movement axis.
            intersectPoint = self.__calculateLineIntersection(
                playerAxis, (pos[0], pos[1]), (nextPos[0], nextPos[1]),
                *self.PlayerMovementLine[self.getControllerIndex()]
            )
            # If there is an intersection, add the point's x value to the list along with the ball's linear velocity.
            if intersectPoint is not None:
                xValues.append((intersectPoint[playerAxis], slope))

        # Choose the x value of one with the highest slope.
        if xValues:
            xVal = max(xValues, key=itemgetter(1))[0]
            if now - self.lastUsedExtraKick > 5.0:
                # 50/50 to use the extra kick.
                self.useExtraKick = bool(random.randint(0, 1))
        # Choose a random X value to move to. Make sure it isn't too small.
        elif random.random() <= 0.33:
            xVal = 0.0
            while abs(self.destinationX - xVal) < 0.3:
                xVal = random.random() * 5.5 * random.choice([-1, 1])
            # Don't use the extra kick for random movements.
            self.useExtraKick = False
        # Try again in 1/10 seconds.
        else:
            task.delayTime = 0.1
            self.useExtraKick = False
            self.notify.info(f"Doing next NPC movement for npc {self.controllerId} in {task.delayTime} seconds...")
            return task.again

        # Random chance for the movement to use faster movement.
        self.isFastMoving = random.random() <= 0.33

        # Send the new x value.
        self.destinationX = xVal

        t = abs(playerPos[playerAxis] - xVal) / (6.0 if self.isFastMoving else 4.0)

        # Set a random delay time.
        task.delayTime = t
        self.notify.info(f"Doing next NPC movement for npc {self.controllerId} in {task.delayTime} seconds...")
        return task.again

    def __npcMoveTask(self, task):
        dt = globalClock.getDt()
        curPos = self.node.getPos()
        oldXValue = curPos[self.getPlayerAxis()]
        xChange = dt * (12.0 if self.isFastMoving else 8.0)

        if oldXValue < self.destinationX:
            newXValue = min(oldXValue + xChange, self.destinationX)
            curPos[self.getPlayerAxis()] = newXValue
            self.node.setPos(curPos)
            self.updateSendVehicleX()

        elif oldXValue > self.destinationX:
            newXValue = max(oldXValue - xChange, self.destinationX)
            curPos[self.getPlayerAxis()] = newXValue
            self.node.setPos(curPos)
            self.updateSendVehicleX()

        return task.cont

    def updateSendVehicleX(self) -> None:
        self.tireOdeGeom.setPosition(*self.node.getPos())
        self.extraKickOdeGeom.setPosition(*self.node.getPos())

        serverTime = globalClock.getRealTime()
        timestamp = globalClockDelta.localToNetworkTime(serverTime)
        self.sendUpdate("sendVehicleX", [self.node.getPos()[self.getPlayerAxis()], timestamp])

    def requestExtraKick(self) -> None:
        avId = self.air.getAvatarIdFromSender()
        if avId != self.controllerId:
            return

        self.showExtraKick()

        # Send change to others.
        serverTime = globalClock.getRealTime()
        timestamp = globalClockDelta.localToNetworkTime(serverTime)
        self.sendUpdate("showExtraKick", [timestamp])

    def showExtraKick(self) -> None:
        # Enable the extra kick ode geom.
        self.extraKickOdeGeom.enable()
        radius = IceGameGlobals.TireRadius
        scaleMulti = 3.0

        def increaseRadius(t):
            self.extraKickOdeGeom.setRadius(radius * t)

        Sequence(
            # Increase radius of the tire physics collision.
            LerpFunctionInterval(increaseRadius, 0.1, fromData=1.0, toData=scaleMulti),
            # Restore radius to normal.
            Func(self.extraKickOdeGeom.setRadius, radius),
            # Disable the ode geom.
            Func(self.extraKickOdeGeom.disable),
        ).start()
