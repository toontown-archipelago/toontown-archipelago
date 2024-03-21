from . import DistributedSZTreasure
from panda3d.core import CardMaker

class DistributedArchiTreasure(DistributedSZTreasure.DistributedSZTreasure):

    def __init__(self, cr):
        DistributedSZTreasure.DistributedSZTreasure.__init__(self, cr)
        cm = CardMaker('ap-treasure')
        self.modelPath = cm
        self.grabSoundPath = 'phase_4/audio/sfx/SZ_DD_treasure.ogg'
