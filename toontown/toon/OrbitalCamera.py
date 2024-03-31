from panda3d.core import (BitMask32, CollisionHandlerFloor,
                          CollisionHandlerQueue, CollisionNode, CollisionRay,
                          CollisionSegment, CollisionTraverser, NodePath,
                          Vec3, WindowProperties)
from direct.directnotify import DirectNotifyGlobal
from direct.fsm.FSM import FSM
from direct.showbase.InputStateGlobal import inputState
from direct.showbase.PythonUtil import fitSrcAngle2Dest, lerp, reduceAngle
from direct.task import Task
from direct.task.TaskManagerGlobal import taskMgr

from otp.otpbase import OTPGlobals
from toontown.toon.ParamObj import ParamObj


class OrbitalCamera(FSM, NodePath, ParamObj):
    notify = DirectNotifyGlobal.directNotify.newCategory("OrbitalCamera")

    class ParamSet(ParamObj.ParamSet):
        Params = {"camOffset": Vec3(0, -9, 5.5)}

    UpdateTaskName = "OrbitCamUpdateTask"
    ReadMouseTaskName = "OrbitCamReadMouseTask"
    CollisionCheckTaskName = "OrbitCamCollisionTask"
    MinP = -50
    MaxP = 20
    baseH = None
    minH = None
    maxH = None
    presets = [[-9, 0, 0], [-24, 0, -10], [-12, 0, -15]]

    TopNodeName = "OrbitCam"

    def __init__(self, subject):
        ParamObj.__init__(self)
        NodePath.__init__(self, self.TopNodeName)
        FSM.__init__(self, "OrbitalCamera")

        self.mouseControl = False
        self.mouseDelta = (0, 0)
        self.lastMousePos = (0, 0)
        self.origMousePos = (0, 0)
        self.request("Off")
        self.__inputEnabled = False
        self.subject = subject
        self.mouseX = 0.0
        self.mouseY = 0.0
        self._paramStack = []
        self.setDefaultParams()
        self.presetPos = 0
        self.collisionTaskCount = 0
        self._rmbToken = inputState.watchWithModifiers("RMB", "mouse3")
        self.initializeCollisions()
        self.firstPerson = False
        self.ignoreRMB = False

    def destroy(self):
        self.destroyCollisions()
        self._rmbToken.release()
        del self._rmbToken
        del self.subject
        FSM.cleanup(self)
        NodePath.removeNode(self)
        ParamObj.destroy(self)
        self.ignoreAll()
    
    def initializeCollisions(self):
        self.cTravOnFloor = CollisionTraverser("CamMode.cTravOnFloor")
        self.camFloorRayNode = self.attachNewNode("camFloorRayNode")
        self.ccRay2 = CollisionRay(0.0, 0.0, 0.0, 0.0, 0.0, -1.0)
        self.ccRay2Node = CollisionNode("ccRay2Node")
        self.ccRay2Node.addSolid(self.ccRay2)
        self.ccRay2NodePath = self.camFloorRayNode.attachNewNode(self.ccRay2Node)
        self.ccRay2BitMask = OTPGlobals.FloorBitmask
        self.ccRay2Node.setFromCollideMask(self.ccRay2BitMask)
        self.ccRay2Node.setIntoCollideMask(BitMask32.allOff())
        self.ccRay2MoveNodePath = hidden.attachNewNode("ccRay2MoveNode")
        self.camFloorCollisionBroadcaster = CollisionHandlerFloor()
        self.camFloorCollisionBroadcaster.setInPattern("zone_on-floor")
        self.camFloorCollisionBroadcaster.setOutPattern("zone_off-floor")
        self.camFloorCollisionBroadcaster.addCollider(
            self.ccRay2NodePath, self.ccRay2MoveNodePath
        )
        self.cTravOnFloor.addCollider(
            self.ccRay2NodePath, self.camFloorCollisionBroadcaster
        )
    
    def destroyCollisions(self):
        del self.cTravOnFloor
        del self.ccRay2
        del self.ccRay2Node
        self.ccRay2NodePath.remove_node()
        del self.ccRay2NodePath
        self.ccRay2MoveNodePath.remove_node()
        del self.ccRay2MoveNodePath
        self.camFloorRayNode.remove_node()
        del self.camFloorRayNode

    def enterActive(self):
        self.enableInput()

        base.camNode.setLodCenter(self.subject)

        self._initMaxDistance()
        self._startCollisionCheck()
        if not self.firstPerson:
            self.acceptWheel()
        self.acceptTab()
        self.reparentTo(self.subject)
        base.camera.reparentTo(self)
        self.setPos(0, 0, self.subject.getHeight())
        camera.setPosHpr(self.camOffset[0], self.camOffset[1], 10, 0, 0, 0)

    def _initMaxDistance(self):
        self._maxDistance = abs(self.camOffset[1])

    def exitActive(self):
        self._stopCollisionCheck()
        base.camNode.setLodCenter(NodePath())
        self.ignoreWheel()
        self.ignoreTab()

        self.disableInput()

    def enableMouseControl(self, pressed):
        if not pressed or self.ignoreRMB:
            return

        if not base.CAM_TOGGLE_LOCK:
            # FIXME: Unless the user interacts with anything that untoggles mouse control
            # (i.e. hopping onto a crane, taking damage, opening book), 
            # the user is permanently stuck in this state            
            self.ignore("InputState-RMB")
            self.accept("InputState-RMB", self.disableMouseControl)

        if self.oobeEnabled():
            return

        self.mouseControl = True
        mouseData = base.win.getPointer(0)
        self.origMousePos = (mouseData.getX(), mouseData.getY())

        base.win.movePointer(0, base.win.getXSize() // 2, base.win.getYSize() // 2)
        self.lastMousePos = (base.win.getXSize() / 2, base.win.getYSize() / 2)

        if self.getCurrentOrNextState() == "Active":
            self._startMouseControlTasks()
        
        self.setCursor(True)

        self.subject.controlManager.setTurn(0)

    def disableMouseControl(self, pressed, disabledByMouse=True):
        self.ignore("InputState-RMB")
        self.accept("InputState-RMB", self.enableMouseControl)

        if self.oobeEnabled():
            return

        if self.mouseControl:
            self.mouseControl = False
            self._stopMouseControlTasks()

            base.win.movePointer(
                0, int(self.origMousePos[0]), int(self.origMousePos[1])
            )

            base.win.movePointer(
                0, int(self.origMousePos[0]), int(self.origMousePos[1])
            )
            self.setCursor(False)

        self.subject.controlManager.setTurn(1)
    
    def setCursor(self, cursor):
        wp = WindowProperties()
        wp.setCursorHidden(cursor)
        base.win.requestProperties(wp)

    def enableInput(self):
        self.__inputEnabled = True
        self.accept("InputState-RMB", self.enableMouseControl)
        if inputState.isSet("RMB"):
            self.enableMouseControl(True)

    def disableInput(self):
        self.__inputEnabled = False
        self.disableMouseControl(False, False)
        self.ignore("InputState-RMB")

    def isInputEnabled(self):
        return self.__inputEnabled

    def isSubjectMoving(self):
        return any([inputState.isSet(movement) for movement in 
                    ("forward", "reverse", "turnRight", "turnLeft", "slideRight", "slideLeft")])

    def _avatarFacingTask(self, task):
        if self.oobeEnabled():
            return task.cont

        if self.isSubjectMoving():  # or self.subject.isAimingPie:
            camH = self.getH(render)
            subjectH = self.subject.getH(render)
            if abs(camH - subjectH) > 0.01:
                self.subject.setH(render, camH)
                self.setH(0)
        return task.cont

    def _mouseUpdateTask(self, task):
        if self.oobeEnabled():
            return task.cont

        subjectMoving = self.isSubjectMoving()
        subjectTurning = subjectMoving

        if subjectMoving:  # or self.subject.isAimingPie:
            hNode = self.subject
        else:
            hNode = self
        
        camSensitivityX = base.settings.get("camSensitivityX")
        camSensitivityY = base.settings.get("camSensitivityY")

        if self.mouseDelta[0] or self.mouseDelta[1]:
            (dx, dy) = self.mouseDelta
            if subjectTurning:
                dx = +dx
            hNode.setH(hNode, -dx * camSensitivityX)
            curP = self.getP()
            newP = curP + -dy * camSensitivityY
            newP = min(max(newP, self.MinP), self.MaxP)
            self.setP(newP)
            if self.baseH:
                self._checkHBounds(hNode)

            self.setR(render, 0)

        return task.cont

    def _checkHBounds(self, hNode):
        currH = fitSrcAngle2Dest(hNode.getH(), 180)
        if currH < self.minH:
            hNode.setH(reduceAngle(self.minH))
        elif currH > self.maxH:
            hNode.setH(reduceAngle(self.maxH))

    def acceptWheel(self):
        self.accept("wheel_up", self._handleWheelUp)
        self.accept("wheel_down", self._handleWheelDown)
        self.accept("page_up", self._handleWheelUp)
        self.accept("page_down", self._handleWheelDown)
        self._resetWheel()

    def ignoreWheel(self):
        self.ignore("wheel_up")
        self.ignore("wheel_down")
        self.ignore("page_up")
        self.ignore("page_down")
        self._resetWheel()
    
    def acceptTab(self):
        self.accept("tab", self.toggleFirstPerson)
    
    def ignoreTab(self):
        self.ignore("tab")
    
    def toggleFirstPerson(self):
        # self.firstPerson = not self.firstPerson
        # if self.firstPerson:
        #     self._handleSetWheel(0)
        #     self.ignoreWheel()
        #     # self.enableMouseControl(True)
        #     # self.ignore("InputState-RMB")
        # else:
        #     self.setPresetPos(0, transition=False)
        #     self.acceptWheel()
        #     # self.disableMouseControl(True)
        self.presetPos += 1
        if self.presetPos >= len(self.presets):
            self.presetPos = 0
        self.setPresetPos(self.presetPos)
    
    def _handleSetWheel(self, y):
        self._collSolid.setPointB(0, y + 1, 0)
        self.camOffset.setY(y)
        t = (-14 - y) / -12
        height = self.subject.getHeight()
        z = lerp(height, height, t)
        self.setZ(z)

    def _handleWheelUp(self):
        y = max(-25, min(-2, self.camOffset[1] + 1.0))
        self._handleSetWheel(y)

    def _handleWheelDown(self):
        y = max(-25, min(-2, self.camOffset[1] - 1.0))
        self._handleSetWheel(y)

    def _resetWheel(self):
        if not self.isActive():
            return

        self.camOffset = Vec3(0, -14, 5.5)
        y = self.camOffset[1]
        z = self.camOffset[2]
        self._collSolid.setPointB(0, y + 1, 0)
        self.setZ(z)

    def getCamOffset(self):
        return self.camOffset

    def setCamOffset(self, camOffset):
        self.camOffset = Vec3(camOffset)

    def applyCamOffset(self):
        if self.isActive():
            camera.setPos(self.camOffset)

    def _setCamDistance(self, distance):
        offset = camera.getPos(self)
        offset.normalize()
        camera.setPos(self, offset * distance)

    def _getCamDistance(self):
        return camera.getPos(self).length()

    def _startCollisionCheck(self):
        self._collSolid = CollisionSegment(0, 0, 0, 0, -(self._maxDistance + 1.0), 0)
        collSolidNode = CollisionNode("OrbitCam.CollSolid")
        collSolidNode.addSolid(self._collSolid)
        collSolidNode.setFromCollideMask(
            OTPGlobals.CameraBitmask
            | OTPGlobals.CameraTransparentBitmask
            | OTPGlobals.FloorBitmask
        )
        collSolidNode.setIntoCollideMask(BitMask32.allOff())
        self._collSolidNp = self.attachNewNode(collSolidNode)
        self._cHandlerQueue = CollisionHandlerQueue()
        self._cTrav = CollisionTraverser("OrbitCam.cTrav")
        self._cTrav.addCollider(self._collSolidNp, self._cHandlerQueue)
        taskMgr.add(
            self._collisionCheckTask, OrbitalCamera.CollisionCheckTaskName, priority=45
        )

    def _collisionCheckTask(self, task=None):
        self.collisionTaskCount = (self.collisionTaskCount + 1) % 5

        if self.oobeEnabled():
            return Task.cont

        self._cTrav.traverse(self.subject.getGeom())

        if self.firstPerson or self.subject.isDisguised:
            self.subject.getGeomNode().hide()
        else:
            self.subject.getGeomNode().show()

        if self._cHandlerQueue.getNumEntries() == 0:
            for i in range(self._cHandlerQueue.getNumEntries()):
                if not self._cHandlerQueue.getEntry(i).hasSurfacePoint():
                    return Task.cont

        self._cHandlerQueue.sortEntries()

        cNormal = (0, -1, 0)
        collEntry = None
        numEntries = self._cHandlerQueue.getNumEntries()

        if numEntries > 0:
            collEntry = self._cHandlerQueue.getEntry(0)
            cNormal = collEntry.getSurfaceNormal(self)

        if not (collEntry and collEntry.hasSurfacePoint()):
            camera.setPos(self.camOffset)
            camera.setZ(0)

            if not self.firstPerson:
                if self.subject.isDisguised:
                    self.subject.getGeomNode().hide()
                else:
                    self.subject.getGeomNode().show()

            return task.cont

        cPoint = collEntry.getSurfacePoint(self)
        offset = 0.9
        camera.setPos(cPoint + cNormal * offset)
        distance = camera.getDistance(self)
        if not self.firstPerson:
            if distance < 1.8 or self.subject.isDisguised:
                self.subject.getGeomNode().hide()
            else:
                self.subject.getGeomNode().show()
        self.subject.ccPusherTrav.traverse(render)
        return Task.cont

    def _stopCollisionCheck(self):
        taskMgr.remove(OrbitalCamera.CollisionCheckTaskName)
        self._cTrav.removeCollider(self._collSolidNp)
        del self._cHandlerQueue
        del self._cTrav
        self._collSolidNp.detachNode()
        del self._collSolidNp
        if self.subject:
            if self.subject.isDisguised:
                self.subject.getGeomNode().hide()
            else:
                self.subject.getGeomNode().show()

    def setPresetPos(self, presetIndex, transition=True):
        self.presetPos = presetIndex

        self.setCameraPos(
            self.presets[self.presetPos][0],
            self.presets[self.presetPos][1],
            self.presets[self.presetPos][2],
            transition=transition,
        )

    def setCameraPos(self, y, h, p, transition=True):
        t = (-14 - y) / -12
        z = lerp(self.subject.getHeight(), self.subject.getHeight(), t)
        self._collSolid.setPointB(0, y + 1, 0)
        self.camOffset.setY(y)
        self.setPos(self.getX(), self.getY(), z)
        self.setHpr(h, p, 0)

    def _startMouseControlTasks(self):
        if self.mouseControl:
            properties = WindowProperties()
            properties.setMouseMode(properties.MRelative)
            base.win.requestProperties(properties)
            self._startMouseReadTask()
            self._startMouseUpdateTask()

    def _stopMouseControlTasks(self):
        properties = WindowProperties()
        properties.setMouseMode(properties.MAbsolute)
        base.win.requestProperties(properties)
        self._stopMouseReadTask()
        self._stopMouseUpdateTask()

    def _startMouseReadTask(self):
        self._stopMouseReadTask()
        taskMgr.add(
            self._mouseReadTask, self.TopNodeName + "-MouseRead", priority=-29
        )

    def _mouseReadTask(self, task):
        if (self.oobeEnabled()) or not base.mouseWatcherNode.hasMouse():
            self.mouseDelta = (0, 0)
        else:
            winSize = (base.win.getXSize(), base.win.getYSize())
            mouseData = base.win.getPointer(0)
            if mouseData.getX() > winSize[0] or mouseData.getY() > winSize[1]:
                self.mouseDelta = (0, 0)
            else:
                self.mouseDelta = (
                    mouseData.getX() - self.lastMousePos[0],
                    mouseData.getY() - self.lastMousePos[1],
                )
                base.win.movePointer(0, winSize[0] // 2, winSize[1] // 2)

                mouseData = base.win.getPointer(0)
                self.lastMousePos = (mouseData.getX(), mouseData.getY())

        return task.cont

    def _stopMouseReadTask(self):
        taskMgr.remove(self.TopNodeName + "-MouseRead")

    def _startMouseUpdateTask(self):
        self._stopMouseUpdateTask()
        taskMgr.add(
            self._avatarFacingTask,
            self.TopNodeName + "-AvatarFacing",
            priority=23,
        )
        taskMgr.add(
            self._mouseUpdateTask,
            self.TopNodeName + "-MouseUpdate",
            priority=40,
        )

    def _stopMouseUpdateTask(self):
        taskMgr.remove(self.TopNodeName + "-MouseUpdate")
        taskMgr.remove(self.TopNodeName + "-AvatarFacing")

    def start(self):
        if not self.isActive():
            self.request("Active")

    def stop(self):
        if self.isActive():
            self.request("Off")
            self.subject.setSpeed(0, 0, 0)

    def isActive(self):
        return self.state == "Active"
    
    def oobeEnabled(self):
        return hasattr(base, "oobeMode") and base.oobeMode
