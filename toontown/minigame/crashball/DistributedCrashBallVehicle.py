from direct.distributed.ClockDelta import globalClockDelta
from direct.distributed.DistributedObject import DistributedObject
from direct.interval.FunctionInterval import Func
from direct.interval.LerpInterval import LerpFunctionInterval, LerpScaleInterval, LerpPosInterval
from direct.interval.MetaInterval import Sequence, Parallel
from direct.task.TaskManagerGlobal import taskMgr
from panda3d.direct import SmoothMover

from toontown.minigame import IceGameGlobals


class DistributedCrashBallVehicle(DistributedObject):
    # Store which index moves against which axis.
    PlayerAxis = {
        0: 1,  # y
        1: 1,  # y
        2: 0,  # x
        3: 0  # x
    }
    ToonNodePosHprs = {
        0: (10, 0, 2, 90, 0, 0),
        1: (-10, 0, 2, -90, 0, 0),
        2: (0, -10, 2, 0, 0, 0),
        3: (0, 10, 2, 180, 0, 0)
    }

    def __init__(self, cr) -> None:
        super().__init__(cr)

        self.minigameId = 0
        self.minigame = None
        self.controllerId = 0

        self.tireNodePath = None
        self.tireOdeGeom = None
        self.extraKickNodePath = None
        self.extraKickOdeGeom = None
        self.disappearTrack = None
        self.aimTaskName = ""

        self.__isExtraKickUp = False
        self.__isSprintHeld = False

        self.smoother = SmoothMover()
        self.smoother.setSmoothMode(SmoothMover.SMOn)

        self.smoothStarted = 0
        self.__broadcastPeriod = 0.2

    def announceGenerate(self) -> None:
        super().announceGenerate()

        self.smoothName = self.uniqueName('crashBallVehicleSmooth')
        self.posHprBroadcastName = self.uniqueName('crashBallVehicleBroadcast')

        self.minigame = base.cr.getDo(self.minigameId)
        self.minigame.vehicles[self.controllerId] = self

        index = self.minigame.totalPlayerIdList.index(self.controllerId)

        tireNp, extraKickNp, tireOdeGeom, extraKickOdeGeom = self.minigame.createTire(index)
        self.tireNodePath = tireNp
        self.tireNodePath.setPosHpr(*self.ToonNodePosHprs[self.getControllerIndex()])
        self.tireOdeGeom = tireOdeGeom
        self.extraKickNodePath = extraKickNp
        self.extraKickOdeGeom = extraKickOdeGeom

        self.tireOdeGeom.setPosition(*self.tireNodePath.getPos())
        self.extraKickOdeGeom.setPosition(*self.tireNodePath.getPos())

        self.reloadPosition()

    def delete(self) -> None:
        self.stopPosHprBroadcast()
        self.stopSmooth()
        self.disableControls()

        if self.disappearTrack is not None:
            self.disappearTrack.finish()
        del self.disappearTrack

        self.tireNodePath.removeNode()
        del self.tireNodePath
        self.tireOdeGeom.destroy()
        del self.tireOdeGeom
        self.extraKickNodePath.removeNode()
        del self.extraKickNodePath
        self.extraKickOdeGeom.destroy()
        del self.extraKickOdeGeom

        del self.minigame.vehicles[self.controllerId]
        del self.minigame
        super().delete()

    def setMinigameId(self, minigameId: int) -> None:
        self.minigameId = minigameId

    def setControllerId(self, controllerId: int) -> None:
        self.controllerId = controllerId

    def getControllerIndex(self) -> int:
        return self.minigame.totalPlayerIdList.index(self.controllerId)

    def getPlayerAxis(self):
        return self.PlayerAxis[self.getControllerIndex()]

    def getNode(self):
        return self.tireNodePath

    def enableControls(self) -> None:
        # Enable controls for the local avatar.
        self.aimTaskName = self.uniqueName("aimtask")
        taskMgr.add(self.__aimTask, self.aimTaskName)

        self.__isExtraKickUp = False
        self.accept(base.controls.JUMP, self.useExtraKick)
        self.accept(base.controls.SPRINT, self.__handleSprintPress)
        self.accept(base.controls.SPRINT + '-up', self.__handleSprintRelease)

        self.startPosHprBroadcast()

    def disableControls(self) -> None:
        taskMgr.remove(self.aimTaskName)
        self.ignore(base.controls.JUMP)
        self.ignore(base.controls.SPRINT)
        self.ignore(base.controls.SPRINT + '-up')

    def __handleSprintPress(self) -> None:
        self.__isSprintHeld = True

    def __handleSprintRelease(self) -> None:
        self.__isSprintHeld = False

    def __aimTask(self, task):
        """Handle input and other necessary stuff while in the Input Choice state."""
        dt = globalClock.getDt()
        arrowKeys = self.minigame.arrowKeys
        # Increase speed when sprint is held.
        xChange = dt * (12.0 if self.__isSprintHeld else 8.0)
        oldXValue = self.tireNodePath.getPos()[self.getPlayerAxis()]
        index = self.getControllerIndex()

        if arrowKeys.leftPressed() and not arrowKeys.rightPressed():
            if index in (0, 2):
                newX = min(max(oldXValue - xChange, -5.5), 5.5)
            else:
                newX = min(max(oldXValue + xChange, -5.5), 5.5)
        elif arrowKeys.rightPressed() and not arrowKeys.leftPressed():
            if index in (0, 2):
                newX = min(max(oldXValue + xChange, -5.5), 5.5)
            else:
                newX = min(max(oldXValue - xChange, -5.5), 5.5)
        else:
            return task.cont

        if newX != oldXValue:
            newPos = self.tireNodePath.getPos()
            newPos[self.getPlayerAxis()] = newX
            self.tireNodePath.setPos(newPos)

        return task.cont

    def useExtraKick(self) -> None:
        if self.__isExtraKickUp:
            return

        self.__isExtraKickUp = True
        self.b_showExtraKick()

    def b_showExtraKick(self) -> None:
        self.d_showExtraKick()
        self.showExtraKick(local=True)

    def d_showExtraKick(self) -> None:
        self.sendUpdate("requestExtraKick", [])

    def showExtraKick(self, timestamp: int = None, local: bool = False) -> None:
        if self.controllerId == base.localAvatar.doId and not local:
            return

        # Timestamp is sent by the server, not used locally.
        if timestamp is not None:
            ts = globalClockDelta.localElapsedTime(timestamp)
        else:
            ts = 0

        # Enable the extra kick ode geom.
        self.extraKickOdeGeom.enable()
        radius = IceGameGlobals.TireRadius
        scaleMulti = 3.0

        def increaseRadius(t):
            self.extraKickOdeGeom.setRadius(radius * t)

        def signalExtraKickDone():
            if self.controllerId == base.localAvatar.doId:
                self.__isExtraKickUp = False

        Sequence(
            Func(self.extraKickNodePath.show),
            # Increase radius of the tire physics collision.
            Parallel(
                LerpFunctionInterval(increaseRadius, 0.1, fromData=1.0, toData=scaleMulti),
                LerpScaleInterval(self.extraKickNodePath, 0.1, scaleMulti),
            ),
            # Restore radius to normal.
            Func(self.extraKickOdeGeom.setRadius, radius),
            # Disable the ode geom.
            Func(self.extraKickOdeGeom.disable),
            Func(self.extraKickNodePath.hide),
            Func(self.extraKickNodePath.setScale, 1.0),
            # Allow the local toon to input the extra kick command, if this is the local toon that we're dealing with.
            Func(signalExtraKickDone)
        ).start(ts)

    def sendVehicleX(self, x: float, timestamp: int) -> None:
        now = globalClock.getFrameTime()
        local = globalClockDelta.networkToLocalTime(timestamp, now)

        if self.getPlayerAxis() == 1:
            self.smoother.setY(x)
        else:
            self.smoother.setX(x)

        self.tireNodePath.setPos(self.smoother.getSmoothPos())
        self.tireOdeGeom.setPosition(*self.smoother.getSmoothPos())
        self.extraKickOdeGeom.setPosition(*self.smoother.getSmoothPos())

        self.smoother.setTimestamp(local)
        self.smoother.markPosition()

    ### Handle smoothing of distributed updates.  This is similar to
    ### code in DistributedSmoothNode, but streamlined for our
    ### purposes.

    def b_clearSmoothing(self):
        self.d_clearSmoothing()
        self.clearSmoothing()

    def d_clearSmoothing(self):
        self.sendUpdate("clearSmoothing", [0])

    def clearSmoothing(self, bogus=None):
        # Call this to invalidate all the old position reports
        # (e.g. just before popping to a new position).
        self.smoother.clearPositions(1)

    def reloadPosition(self):
        """reloadPosition(self)

        This function re-reads the position from the node itself and
        clears any old position reports for the node.  This should be
        used whenever show code bangs on the node position and expects
        it to stick.

        """
        self.smoother.clearPositions(0)
        self.smoother.setPos(self.tireNodePath.getPos())
        self.smoother.setHpr(self.tireNodePath.getHpr())
        self.smoother.setPhonyTimestamp()

    def doSmoothTask(self, task):
        """
        This function updates the position of the node to its computed
        smoothed position.  This may be overridden by a derived class
        to specialize the behavior.
        """
        self.smoother.computeAndApplySmoothPosHpr(self.tireNodePath, self.tireNodePath)
        return task.cont

    def startSmooth(self):
        """
        This function starts the task that ensures the node is
        positioned correctly every frame.  However, while the task is
        running, you won't be able to lerp the node or directly
        position it.
        """
        if not self.smoothStarted:
            taskName = self.smoothName
            taskMgr.remove(taskName)
            self.reloadPosition()
            taskMgr.add(self.doSmoothTask, taskName)
            self.smoothStarted = 1

    def stopSmooth(self):
        """
        This function stops the task spawned by startSmooth(), and
        allows show code to move the node around directly.
        """
        if self.smoothStarted:
            taskName = self.smoothName
            taskMgr.remove(taskName)
            self.forceToTruePosition()
            self.smoothStarted = 0

    def forceToTruePosition(self):
        """forceToTruePosition(self)

        This forces the node to reposition itself to its latest known
        position.  This may result in a pop as the node skips the last
        of its lerp points.

        """
        if self.smoother.getLatestPosition():
            self.smoother.applySmoothPos(self.tireNodePath)
            self.smoother.applySmoothHpr(self.tireNodePath)
        self.smoother.clearPositions(1)

    def setVehicleX(self, x, timestamp):
        if self.smoothStarted:
            now = globalClock.getFrameTime()
            local = globalClockDelta.networkToLocalTime(timestamp, now)

            if self.getPlayerAxis() == 1:
                self.smoother.setY(x)
            else:
                self.smoother.setX(x)

            self.tireOdeGeom.setPosition(*self.smoother.getSmoothPos())
            self.extraKickOdeGeom.setPosition(*self.smoother.getSmoothPos())

            self.smoother.setTimestamp(local)
            self.smoother.markPosition()
        else:
            if self.getPlayerAxis() == 1:
                self.tireNodePath.setY(x)
            else:
                self.tireNodePath.setX(x)

            self.tireOdeGeom.setPosition(*self.tireNodePath.getPos())
            self.extraKickOdeGeom.setPosition(*self.tireNodePath.getPos())

    def d_sendVehicleX(self):
        timestamp = globalClockDelta.getFrameNetworkTime()
        self.sendUpdate('setVehicleX', [self.tireNodePath.getPos()[self.getPlayerAxis()], timestamp])

    def stopPosHprBroadcast(self):
        taskName = self.posHprBroadcastName
        taskMgr.remove(taskName)

    def startPosHprBroadcast(self):
        taskName = self.posHprBroadcastName

        # Broadcast our initial position
        self.b_clearSmoothing()
        self.d_sendVehicleX()

        # remove any old tasks
        taskMgr.remove(taskName)
        taskMgr.doMethodLater(self.__broadcastPeriod,
                              self.__posHprBroadcast, taskName)

    def __posHprBroadcast(self, task):
        self.d_sendVehicleX()
        taskName = self.posHprBroadcastName
        taskMgr.doMethodLater(self.__broadcastPeriod,
                              self.__posHprBroadcast, taskName)
        return task.done
