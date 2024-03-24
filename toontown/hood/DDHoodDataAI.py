from typing import List

from direct.directnotify import DirectNotifyGlobal
from . import HoodDataAI
from toontown.toonbase import ToontownGlobals
from toontown.safezone import DistributedTrolleyAI
from toontown.safezone import DDTreasurePlannerAI
from toontown.safezone import DistributedBoatAI
from toontown.safezone import ArchipelagoTreasurePlannerAI
from toontown.safezone import DistributedArchiTreasureAI

class DDHoodDataAI(HoodDataAI.HoodDataAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DDHoodDataAI')

    def __init__(self, air, zoneId=None):
        hoodId = ToontownGlobals.DonaldsDock
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
                                DDTreasurePlannerAI.DDTreasurePlannerAI(self.zoneId)
                                ]
        for planner in self.treasurePlanner:
            planner.start()
        boat = DistributedBoatAI.DistributedBoatAI(self.air)
        boat.generateWithRequired(self.zoneId)
        boat.start()
        self.addDistObj(boat)

    def getStreetClerkZoneIds(self) -> List[int]:
        return [1128, 1218, 1309]  # Barnacle, Seaweed, Lighthouse
