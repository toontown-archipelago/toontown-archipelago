from typing import List

from direct.directnotify import DirectNotifyGlobal
from . import HoodDataAI
from toontown.toonbase import ToontownGlobals
from toontown.safezone import DistributedTrolleyAI
from toontown.safezone import MMTreasurePlannerAI
from toontown.safezone import ArchipelagoTreasurePlannerAI
from toontown.safezone import DistributedArchiTreasureAI
from toontown.safezone import DistributedMMPianoAI

class MMHoodDataAI(HoodDataAI.HoodDataAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('MMHoodDataAI')

    def __init__(self, air, zoneId=None):
        hoodId = ToontownGlobals.MinniesMelodyland
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
                                MMTreasurePlannerAI.MMTreasurePlannerAI(self.zoneId)
                                ]
        for planner in self.treasurePlanner:
            planner.start()

    def getStreetClerkZoneIds(self) -> List[int]:
        return [4115, 4214, 4343]  # Alto, Baritone, Tenor
