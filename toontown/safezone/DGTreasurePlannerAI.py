from toontown.toonbase.ToontownGlobals import *
from . import RegenTreasurePlannerAI
from . import DistributedDGTreasureAI

class DGTreasurePlannerAI(RegenTreasurePlannerAI.RegenTreasurePlannerAI):

    def __init__(self, zoneId):
        RegenTreasurePlannerAI.RegenTreasurePlannerAI.__init__(self, zoneId, DistributedDGTreasureAI.DistributedDGTreasureAI, 'DGTreasurePlanner', 15, 2)
        return None