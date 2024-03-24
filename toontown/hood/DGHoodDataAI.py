from typing import List

from direct.directnotify import DirectNotifyGlobal
from . import HoodDataAI
from toontown.toonbase import ToontownGlobals
from toontown.safezone import DistributedTrolleyAI
from toontown.safezone import DGTreasurePlannerAI
from toontown.safezone import DistributedDGFlowerAI
from toontown.safezone import ButterflyGlobals
from toontown.safezone import ArchipelagoTreasurePlannerAI
from toontown.safezone import DistributedArchiTreasureAI

class DGHoodDataAI(HoodDataAI.HoodDataAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DGHoodDataAI')

    def __init__(self, air, zoneId=None):
        hoodId = ToontownGlobals.DaisyGardens
        if zoneId == None:
            zoneId = hoodId
        HoodDataAI.HoodDataAI.__init__(self, air, zoneId, hoodId)
        return

    def startup(self):
        HoodDataAI.HoodDataAI.startup(self)
        trolley = DistributedTrolleyAI.DistributedTrolleyAI(self.air)
        trolley.generateWithRequired(self.zoneId)
        trolley.start()
        self.addDistObj(trolley)
        self.treasurePlanner = [ArchipelagoTreasurePlannerAI.ArchipelagoTreasurePlannerAI(self.zoneId, DistributedArchiTreasureAI.DistributedArchiTreasureAI, 0),
                                DGTreasurePlannerAI.DGTreasurePlannerAI(self.zoneId)
                                ]
        for planner in self.treasurePlanner:
            planner.start()
        flower = DistributedDGFlowerAI.DistributedDGFlowerAI(self.air)
        flower.generateWithRequired(self.zoneId)
        flower.start()
        self.addDistObj(flower)
        self.createButterflies(ButterflyGlobals.DG)

    def getStreetClerkZoneIds(self) -> List[int]:
        return [5123, 5243, 5320]  # Elm, Maple, Oak
