import math

from direct.showbase.EventManagerGlobal import eventMgr
from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import BitMask32, Vec4, Point3, Vec3, deg2Rad
from panda3d.ode import OdePlaneGeom, OdeUtil, OdeBody, OdeMass, OdeSphereGeom, OdeCylinderGeom

from toontown.minigame import IceGameGlobals
from toontown.minigame.MinigamePhysicsWorldBase import MinigamePhysicsWorldBase
from toontown.minigame.crashball.CrashBallConstants import MetersToFeet, GolfBallInitialForce


class CrashBallGamePhysicsWorld(MinigamePhysicsWorldBase):
    ToonNodePosHprs = {
        0: (10, 0, 2, 90, 0, 0),
        1: (-10, 0, 2, -90, 0, 0),
        2: (0, -10, 2, 0, 0, 0),
        3: (0, 10, 2, 180, 0, 0)
    }

    WallPosHprData = {
        0: (10, 7.5, 0, -90),
        1: (-10, -7.5, 0, 90),
        2: (7.5, -10, 0, 180),
        3: (-7.5, 10, 0, 0)
    }

    # ODE Collision bits
    # 0 - floor
    # 1 - windmill
    # 2 - obstacle
    # 3 - ball
    # 4 - tire
    # 5 - wall 1
    # 6 - wall 2
    # 7 - wall 3
    # 8 - wall 4
    floorCollideId = 1
    floorMask = BitMask32(floorCollideId)
    windmillCollideId = 1 << 1
    windmillMask = BitMask32(windmillCollideId)
    obstacleCollideId = 1 << 2
    obstacleMask = BitMask32(obstacleCollideId)
    ballCollideId = 1 << 3
    ballMask = BitMask32(ballCollideId)
    tireCollideId = 1 << 4
    tireMask = BitMask32(tireCollideId)

    wallCollideIds = [1 << 5, 1 << 6, 1 << 7, 1 << 8]
    wall0Mask = BitMask32(wallCollideIds[0])
    wall1Mask = BitMask32(wallCollideIds[1])
    wall2Mask = BitMask32(wallCollideIds[2])
    wall3Mask = BitMask32(wallCollideIds[3])

    allWallsMask = wall0Mask | wall1Mask | wall2Mask | wall3Mask
    wallMasks = (wall0Mask, wall1Mask, wall2Mask, wall3Mask)

    scoreCollideIds = [1 << 9, 1 << 10, 1 << 11, 1 << 12]
    score0Mask = BitMask32(scoreCollideIds[0])
    score1Mask = BitMask32(scoreCollideIds[1])
    score2Mask = BitMask32(scoreCollideIds[2])
    score3Mask = BitMask32(scoreCollideIds[3])

    allScoresMask = score0Mask | score1Mask | score2Mask | score3Mask
    scoreMasks = (score0Mask, score1Mask, score2Mask, score3Mask)

    extraKickCollideId = 1 << 13
    extraKickMask = BitMask32(extraKickCollideId)

    tireSurfaceType = 0
    iceSurfaceType = 1
    fenceSurfaceType = 2
    ballSurfaceType = 3
    scoreSurfaceType = 4
    extraKickSurfaceType = 5
    allSurfaces = (0, 1, 2, 3, 4, 5)

    windmillXY = {
        0: (12, 12),   # near right
        1: (-12, 12),  # far right
        2: (12, -12),  # near left
        3: (-12, -12)  # far left
    }

    WindmillPositions = {
        0: (10, 10, 0, 45, 0, 0),  # near right
        1: (-10, 10, 0, -225, 0, 0),  # far right
        2: (10, -10, 0, -45, 0, 0),  # near left
        3: (-10, -10, 0, 225, 0, 0)  # far left
    }

    BallSpawnPoints = {
        0: (6, 6, 0),
        1: (-6, 6, 0),
        2: (6, -6, 0),
        3: (-6, -6, 0)
    }

    def setupSimulation(self):
        """Setup the ice game specific parameters."""
        super().setupSimulation()
        # toontown uses feet, 1 meter = 3.2808399 feet
        # for this game lets express mass in kilograms
        # so gravity at 9.8 meters per seconds squared becomes
        self.world.setGravity(0, 0, -32.174)

        # ODE's default is meter, kilograms, seconds, let's change the defaults
        # do we need to change global ERP value,
        # that controls how much error correction is performed in each time step
        # default is 0.2
        self.world.setAutoDisableFlag(1)  # lets try auto disable
        self.world.setAutoDisableLinearThreshold(0.5 * MetersToFeet)
        # skipping AutoDisableAngularThreshold as that is radians per second
        # self.world.setAutoDisableAngularThreshold(0.01)
        # don't consider rotation for auto disable
        self.world.setAutoDisableAngularThreshold(OdeUtil.getInfinity())
        self.world.setAutoDisableSteps(10)

        # Set and the global CFM (constraint force mixing) value.
        # Typical values are in the range 10-9 -- 1.
        # The default is 10-5 if single precision is being used
        self.world.setCfm(1E-5 * MetersToFeet)

        # Our surfaces
        # 0 = tire
        # 1 = ice
        # 2 = fence
        # 3 = ball
        self.world.initSurfaceTable(len(self.allSurfaces))  # 3 types of surfaces

        # PN_uint8 pos1, PN_uint8 pos2,  - surface0, surface1
        #            dReal mu, - 0 frictionless, 1 infinite friction
        #            dReal bounce, # Restitution parameter 0 not bouncy, 1 max bouncy
        #            NOTE: 1 is NOT max bouncy, you can make it more bouncy by increasing it above 1
        #            dReal bounce_vel, #The minimum incoming velocity necessary for bounce.
        #                              Incoming velocities below this will
        #                              effectively have a bounce parameter of 0.
        #            dReal soft_erp, # Contact normal "softness" parameter.
        #            dReal soft_cfm, # Contact normal "softness" paramete
        #            dReal slip,     # The coefficients of force-dependent-slip (FDS)
        #            dReal dampen   # dampening constant

        # the most usual collision, ball against ice
        self.world.setSurfaceEntry(self.ballSurfaceType, self.iceSurfaceType,
                                   0.01,  # near frictionless
                                   0,  # not bouncy
                                   0,  # bounce_vel
                                   0,  # soft_erp
                                   0,  # soft_cfm
                                   0,  # slip
                                   0.1,  # dampen
                                   )
        # ball against ball
        self.world.setSurfaceEntry(self.ballSurfaceType, self.ballSurfaceType,
                                   0.1,  # friction
                                   1.0,  # bounciness
                                   0.1,  # bounce_vel
                                   0,  # soft_erp
                                   0,  # soft_cfm
                                   0,  # slip
                                   0,  # dampen
                                   )

        # ball against tire
        self.world.setSurfaceEntry(self.ballSurfaceType, self.tireSurfaceType,
                                   0.1,  # friction
                                   1.0,  # bounciness
                                   0.3,  # bounce_vel
                                   0,  # soft_erp
                                   0,  # soft_cfm
                                   0,  # slip
                                   0,  # dampen
                                   )

        # ball against extra kick collider
        self.world.setSurfaceEntry(self.ballSurfaceType, self.extraKickSurfaceType,
                                   0.1,  # friction
                                   2.25,  # bounciness
                                   0.0,  # bounce_vel
                                   0,  # soft_erp
                                   0,  # soft_cfm
                                   0,  # slip
                                   0.2,  # dampen
                                   )

        # ball against fence
        self.world.setSurfaceEntry(self.ballSurfaceType, self.fenceSurfaceType,
                                   0.1,  # friction
                                   1.0,  # bounciness
                                   0.2,  # bounce_vel
                                   0,  # soft_erp
                                   0,  # soft_cfm
                                   0,  # slip
                                   0,  # dampen
                                   )

        # ball against score wall
        self.world.setSurfaceEntry(self.ballSurfaceType, self.scoreSurfaceType,
                                   1.0,  # friction
                                   0,  # bounciness
                                   0,  # bounce_vel
                                   0,  # soft_erp
                                   0,  # soft_cfm
                                   0,  # slip
                                   0,  # dampen
                                   )

        # Create a plane geom which prevent the objects from falling forever
        self.floor = OdePlaneGeom(self.space, Vec4(0.0, 0.0, 1.0, -10.0))
        self.floor.setCollideBits(self.ballMask)  # we only collide against balls
        self.floor.setCategoryBits(self.floorMask)

        # Wall collisions
        self.walls = {} # order: e/w/s/n
        for i, (x, y) in enumerate(((-1.0, 0.0), (1.0, 0.0), (0.0, 1.0), (0.0, -1.0))):
            wallNode, wall = self.createWall(x, y, i)
            self.walls[i] = {
                "wallNode": wallNode,
                "wall": wall
            }
            # Disable the wall until it's needed.
            self.walls[i]["wall"].disable()

        # Score collisions
        self.scoreWalls = {} # order: e/w/s/n
        for i, (x, y) in enumerate(((-1.0, 0.0), (1.0, 0.0), (0.0, 1.0), (0.0, -1.0))):
            self.scoreWalls[i] = self.createScoreWall(x, y, i)

        # a temporary floor at z=0, until we implement ice with holes
        self.floorTemp = OdePlaneGeom(self.space, Vec4(0.0, 0.0, 1.0, 0.0))
        self.floorTemp.setCollideBits(self.ballMask)  # we only collide against balls
        self.floorTemp.setCategoryBits(self.floorMask)
        self.space.setSurfaceType(self.floorTemp, self.iceSurfaceType)
        self.space.setCollideId(self.floorTemp, self.floorCollideId)

        self.windmillColliders = [self.createWindmill(*self.windmillXY[i]) for i in range(4)]

        self.space.setAutoCollideWorld(self.world)
        self.space.setAutoCollideJointGroup(self.contactgroup)
        self.world.setQuickStepNumIterations(8)
        self.DTA = 0.0

        self.frameCounter = 0

    def simulate(self):
        """Do one physics step."""
        self.colEntries = []
        self.space.autoCollide()
        eventMgr.doEvents()
        self.colCount = len(self.colEntries)
        if self.maxColCount < self.colCount:
            self.maxColCount = self.colCount
            self.notify.debug("New Max Collision Count %s" % (self.maxColCount))
        if self.useQuickStep:
            self.world.quickStep(self.DTAStep)  # Simulate
        else:
            self.world.step(self.DTAStep)  # Simulate

        # Disable body dampening as it seems to improve the feel of the ball physics.
        # for bodyPair in self.bodyList:
        #     self.world.applyDampening(self.DTAStep, bodyPair[1])

        self.contactgroup.empty()  # Remove all contact joints
        # self.commonObjectControl()
        self.timingSimTime = self.timingSimTime + self.DTAStep

    def startSim(self):
        """Start the real time physics simulation."""
        taskMgr.add(self.__simulationTask, "simulation task")

    def stopSim(self):
        """Stop the real time physics simulation."""
        taskMgr.remove("simulation task")

    def __simulationTask(self, task):
        """Simulate the world, multiple steps if needed."""
        self.DTA += globalClock.getDt()
        self.frameCounter += 1
        if self.frameCounter >= 10:
            self.frameCounter = 0

        startTime = globalClock.getRealTime()

        while self.DTA >= self.DTAStep:
            if self.deterministic:
                OdeUtil.randSetSeed(0)
            self.DTA -= self.DTAStep
            self.preStep()
            self.simulate()
            self.postStep()

        if self.canRender:
            self.placeBodies()

        return task.cont

    def createTire(self, tireIndex):
        """Create one physics tire. Returns a (nodePath, OdeBody, OdeGeom) tuple"""
        self.notify.debug("create tireindex %s" % (tireIndex))

        geom = OdeSphereGeom(self.space, IceGameGlobals.TireRadius)
        self.space.setSurfaceType(geom, self.tireSurfaceType)
        self.space.setCollideId(geom, self.tireCollideId)#self.tireCollideIds[tireIndex])

        self.geomList.append(geom)

        # A tire collides against balls... teehee...
        # geom.setCollideBits(self.allTiresMask | self.wallMask | self.floorMask | self.obstacleMask)
        geom.setCollideBits(self.ballMask)
        geom.setCategoryBits(self.tireMask)

        # Create a second physics object relative to the tire which handles the "extra kick" command.
        geom2 = OdeSphereGeom(self.space, IceGameGlobals.TireRadius)
        self.space.setSurfaceType(geom2, self.extraKickSurfaceType)
        self.space.setCollideId(geom2, self.extraKickCollideId)  # self.tireCollideIds[tireIndex])

        self.geomList.append(geom2)

        # A tire collides against balls... teehee...
        # geom.setCollideBits(self.allTiresMask | self.wallMask | self.floorMask | self.obstacleMask)
        geom2.setCollideBits(self.ballMask)
        geom2.setCategoryBits(self.extraKickMask)
        # Disable for now.
        geom2.disable()

        if self.canRender:
            testTire = render.attachNewNode("tire holder %d" % tireIndex)
            # lets create a black tire
            tireModel = loader.loadModel("phase_4/models/minigames/ice_game_tire")
            tireModel.setZ(-IceGameGlobals.TireRadius + 0.01)
            tireModel.reparentTo(testTire)

            testTire2 = testTire.attachNewNode("tire holder 2 %d" % tireIndex)
            tire2 = tireModel.copyTo(testTire2)
            tire2.setZ(-IceGameGlobals.TireRadius + 0.01)
            testTire2.setColorScale(1, 1, 1, 0.3)
            testTire2.setTransparency(1)
            testTire2.hide()
        else:
            testTire, testTire2 = None, None
        return testTire, testTire2, geom, geom2

    def createSphere(self, density: float, radius: float, windmillIdx: int, hVariance: float):
        body = OdeBody(self.world)
        M = OdeMass()
        M.setSphere(density, radius)
        body.setMass(M)
        body.setPosition(Point3(*self.BallSpawnPoints[windmillIdx]))

        # Disable the ball for now.
        body.disable()

        geom = OdeSphereGeom(self.space, radius)
        self.space.setSurfaceType(geom, self.ballSurfaceType)
        self.space.setCollideId(geom, self.ballCollideId)#self.tireCollideIds[tireIndex])

        self.massList.append(M)
        self.geomList.append(geom)

        # Balls collide against the floor, walls, tires, and other balls
        geom.setCollideBits(self.ballMask | self.tireMask | self.allScoresMask | self.allWallsMask | self.floorMask |
                            self.windmillMask)
        geom.setCategoryBits(self.ballMask)
        geom.setBody(body)

        if self.canRender:
            testball = render.attachNewNode("Ball Holder")
            ballmodel = loader.loadModel('phase_6/models/golf/golf_ball')
            ballmodel.reparentTo(testball)
            testball.setScale(radius * 4)
            self.odePandaRelationList.append((testball, body))
        else:
            testball = None
            self.bodyList.append((None, body))
        return testball, body, geom

    def setupInitialBallForce(self, golfBall: OdeBody, windmillIdx: int, hVariance: float):
        golfBall.setAngularVel(0, 0, 0)  # make sure it's not spinning when it starts
        golfBall.setLinearVel(0, 0, 0)  # make sure it's not moving  when it starts

        # Set up the initial force of the body.
        degs = self.WindmillPositions[windmillIdx][3] - 180 + hVariance
        radAngle = deg2Rad(degs)
        dirVector = Vec3(math.cos(radAngle), math.sin(radAngle), 0)
        inputForce = GolfBallInitialForce / 100 * 25000
        force = dirVector * inputForce
        golfBall.addForce(force)

        # Enable the golf ball.
        golfBall.enable()

    def createWindmill(self, x: float, y: float):
        # args: space, radius, length
        windmill = OdeCylinderGeom(self.space, 5.0, 5.0)
        windmill.setCollideBits(self.ballMask)  # we only collide against balls
        windmill.setCategoryBits(self.windmillMask)
        windmill.setPosition(x, y, 0)
        self.space.setSurfaceType(windmill, self.fenceSurfaceType)
        self.space.setCollideId(windmill, self.windmillCollideId)
        return windmill

    def createWall(self, x: float, y: float, index: int):
        wall = OdePlaneGeom(self.space, Vec4(x, y, 0.0, -10.0))
        wall.setCollideBits(self.ballMask)  # we only collide against balls
        wall.setCategoryBits(self.wallMasks[index])
        self.space.setSurfaceType(wall, self.fenceSurfaceType)
        self.space.setCollideId(wall, self.wallCollideIds[index])

        if self.canRender:
            wallNode = render.attachNewNode(f"wall holder {index}")
            wallModel = loader.loadModel('phase_3.5/models/modules/wood_fence')
            wallModel.reparentTo(wallNode)

            x, y, z, h = self.WallPosHprData[index]
            wallNode.setPos(x, y, z)
            wallNode.setH(h)
            wallNode.setScale(1.5, 1, 1)
            wallNode.setTwoSided(1)
            wallNode.hide()
        else:
            wallNode = None

        return wallNode, wall

    def createScoreWall(self, x: float, y: float, index: int):
        scoreWall = OdePlaneGeom(self.space, Vec4(x, y, 0.0, -13.0))
        scoreWall.setCollideBits(self.ballMask)  # we only collide against balls
        scoreWall.setCategoryBits(self.scoreMasks[index])
        self.space.setSurfaceType(scoreWall, self.scoreSurfaceType)
        self.space.setCollideId(scoreWall, self.scoreCollideIds[index])
        return scoreWall
