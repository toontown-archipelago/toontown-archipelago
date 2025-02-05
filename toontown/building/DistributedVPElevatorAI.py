from .ElevatorConstants import *
from . import DistributedBossElevatorAI
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownGlobals

class DistributedVPElevatorAI(DistributedBossElevatorAI.DistributedBossElevatorAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedVPElevatorAI')

    def __init__(self, air, bldg, zone, antiShuffle=0, minLaff=0):
        DistributedBossElevatorAI.DistributedBossElevatorAI.__init__(self, air, bldg, zone, antiShuffle=antiShuffle, minLaff=minLaff)
        self.type = ELEVATOR_VP
        self.countdownTime = ElevatorData[self.type]['countdown']
