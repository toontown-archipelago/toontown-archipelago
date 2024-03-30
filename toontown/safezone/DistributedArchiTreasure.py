from . import DistributedSZTreasure
from panda3d.core import CardMaker, NodePath, TransparencyAttrib, Texture

from typing import Union


class DistributedArchiTreasure(DistributedSZTreasure.DistributedSZTreasure):
    def __init__(self, cr):
        DistributedSZTreasure.DistributedSZTreasure.__init__(self, cr)
        self.grabSoundPath = 'phase_4/audio/sfx/SZ_DD_treasure.ogg'
        self.billboard = True

    def prepareModel(self, modelPath: str, modelFindString: Union[str, None]) -> NodePath:
        model = NodePath(CardMaker('ap-treasure').generate())
        model.setScale(3)
        model.setPos(-1.5, 0, 0.5)
        model.setColor(0.9, 0.9, 0.9, 1)
        model.setTransparency(TransparencyAttrib.MAlpha)
        tex = loader.loadTexture('phase_14/maps/ap_icon_outline.png')
        tex.setMinfilter(Texture.FTLinear)
        tex.setMagfilter(Texture.FTLinear)
        model.setTexture(tex)
        # self.nodePath.setBillboardPointEye()
        # self.dropShadow.wrtReparentTo(self.getParentNodePath())
        return model
