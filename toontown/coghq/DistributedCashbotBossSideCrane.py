from direct.distributed.ClockDelta import *
from direct.fsm import FSM
from toontown.coghq import DistributedCashbotBossCrane
from toontown.coghq import DistributedCashbotBossSafe
from panda3d.core import *

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
        
    def grabObject(self, obj):
        if isinstance(obj, DistributedCashbotBossSafe.DistributedCashbotBossSafe):
            return
        else:
            DistributedCashbotBossCrane.DistributedCashbotBossCrane.grabObject(self, obj)
