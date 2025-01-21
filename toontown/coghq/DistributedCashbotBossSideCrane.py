from direct.distributed.ClockDelta import *
from direct.fsm import FSM
from toontown.coghq import DistributedCashbotBossCrane
from toontown.coghq import DistributedCashbotBossSafe
from panda3d.core import *
from panda3d.core import Point3
from panda3d.core import TextureStage
from panda3d.physics import PhysicsCollisionHandler
from panda3d.core import CollisionInvSphere, CollisionNode, CollisionCapsule, BitMask32, CollisionHandlerEvent

from toontown.suit import DistributedCashbotBossGoon
from toontown.toonbase import ToontownGlobals


class DistributedCashbotBossSideCrane(DistributedCashbotBossCrane.DistributedCashbotBossCrane, FSM.FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedCashbotBossCrane')
    firstMagnetBit = 21
    craneMinY = 8
    craneMaxY = 30
    armMinH = -12.5
    armMaxH = 12.5
    shadowOffset = 1
    emptyFrictionCoef = 0.1
    emptySlideSpeed = 15
    emptyRotateSpeed = 20
    lookAtPoint = Point3(0.3, 0, 0.1)
    lookAtUp = Vec3(0, -1, 0)
    neutralStickHinge = VBase3(0, 90, 0)
    magnetModel = loader.loadModel('phase_10/models/cogHQ/CBMagnet.bam')

    def __init__(self, cr):
        DistributedCashbotBossCrane.DistributedCashbotBossCrane.__init__(self, cr)
        FSM.FSM.__init__(self, 'DistributedCashbotBossSideCrane')

    def getName(self):
        return 'SideCrane-%s' % self.index
        
    def grabObject(self, obj):
        if isinstance(obj, DistributedCashbotBossSafe.DistributedCashbotBossSafe):
            return
        else:
            DistributedCashbotBossCrane.DistributedCashbotBossCrane.grabObject(self, obj)

    def getPointsForStun(self):
        return self.boss.ruleset.POINTS_SIDESTUN

    # Override base method, always wake up goons
    def considerObjectState(self, obj):
        if isinstance(obj, DistributedCashbotBossGoon.DistributedCashbotBossGoon):
            obj.d_requestWalk()
            obj.setObjectState('W', 0, obj.craneId)  # wake goon up

    def setupCable(self):
        activated = self.physicsActivated
        self.clearCable()
        
        self.handler = PhysicsCollisionHandler()
        self.handler.setStaticFrictionCoef(0.1)
        self.handler.setDynamicFrictionCoef(self.emptyFrictionCoef)
        
        linkWidth = float(self.cableLength) / float(self.numLinks)
        self.shell = CollisionInvSphere(0, 0, 0, linkWidth + 1)
        
        # The list of links is built up to pass to the Rope class, to
        # make a renderable spline for the cable.
        self.links = []
        self.links.append((self.topLink, Point3(0, 0, 0)))
        
        # Now that we've made a bunch of collisions, stash 'em all
        # (we're initially deactivated).
        anchor = self.topLink
        for linkNum in range(self.numLinks):
            anchor = self.makeLink(anchor, linkNum)

        # Make the magnet swing naturally on the end of the cable.
        self.collisions.stash()
        self.bottomLink = self.links[-1][0]
        self.middleLink = self.links[-2][0]
        self.magnet = self.bottomLink.attachNewNode('magnet')
        self.wiggleMagnet = self.magnet.attachNewNode('wiggleMagnet')
        taskMgr.add(self.rotateMagnet, self.rotateLinkName)
        
        magnetModel = self.boss.sideMagnet.copyTo(self.wiggleMagnet)
        magnetModel.setHpr(90, 45, 90)
        
        # And a node to hold stuff.
        self.gripper = magnetModel.attachNewNode('gripper')
        self.gripper.setPos(0, 0, -4)

        # Not to mention a bubble to detect stuff to grab.
        cn = CollisionNode('sniffer')
        self.sniffer = magnetModel.attachNewNode(cn)
        self.sniffer.stash()
        cs = CollisionCapsule(0, 0, -10, 0, 0, -13, 6)
        cs.setTangible(0)
        cn.addSolid(cs)
        cn.setIntoCollideMask(BitMask32(0))
        cn.setFromCollideMask(ToontownGlobals.CashbotBossObjectBitmask)
        self.snifferHandler = CollisionHandlerEvent()
        self.snifferHandler.addInPattern(self.snifferEvent)
        self.snifferHandler.addAgainPattern(self.snifferEvent)

        # Add a secondary smaller sniffer for dropped objects
        cn2 = CollisionNode('smallSniffer')
        self.smallSniffer = magnetModel.attachNewNode(cn2)
        self.smallSniffer.stash()
        cs2 = CollisionCapsule(0, 0, -1, 0, 0, -1, 1)  # Much smaller sniffer
        cs2.setTangible(0)
        cn2.addSolid(cs2)
        cn2.setIntoCollideMask(BitMask32(0))
        cn2.setFromCollideMask(ToontownGlobals.CashbotBossObjectBitmask)
        self.smallSnifferHandler = CollisionHandlerEvent()
        self.smallSnifferEvent = self.uniqueName('smallSniffer')
        self.smallSnifferHandler.addInPattern(self.smallSnifferEvent)
        self.smallSnifferHandler.addAgainPattern(self.smallSnifferEvent)
        
        rope = self.makeSpline()
        rope.reparentTo(self.cable)
        rope.setTexture(self.boss.cableTex)

        # Texture coordinates on the cable should be in the range
        # (0.83, 0.01) - (0.98, 0.14).
        ts = TextureStage.getDefault()
        rope.setTexScale(ts, 0.15, 0.13)
        rope.setTexOffset(ts, 0.83, 0.01)
        
        if activated:
            self.__activatePhysics()