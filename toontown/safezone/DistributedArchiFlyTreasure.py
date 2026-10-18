from . import DistributedSZTreasure
from panda3d.core import CardMaker, NodePath, TransparencyAttrib, Texture
from direct.interval.IntervalGlobal import *
from direct.distributed import DistributedObject
from panda3d.direct import ShowInterval, HideInterval

from typing import Union


class DistributedArchiFlyTreasure(DistributedSZTreasure.DistributedSZTreasure):
    def __init__(self, cr):
        DistributedSZTreasure.DistributedSZTreasure.__init__(self, cr)
        self.grabSoundPath = 'phase_4/audio/sfx/SZ_DD_treasure.ogg'
        self.billboard = True
        self.bounceLoop = None

    def prepareModel(self, modelPath: str, modelFindString: Union[str, None]) -> NodePath:
        model = NodePath(CardMaker('ap-treasure').generate())
        model.setScale(3)
        model.setPos(-1.5, 0, 0.5)
        model.setColor(0.9, 0.9, 0.9, 1)
        model.setTransparency(TransparencyAttrib.MAlpha)
        tex = loader.loadTexture('phase_14/maps/ap_icon_fly.png')
        tex.setMinfilter(Texture.FTLinear)
        tex.setMagfilter(Texture.FTLinear)
        model.setTexture(tex)
        self.bounceLoop = Sequence(LerpPosInterval(model, startPos=(-1.5, 0, 0.5), pos=(-1.5, 0, 1.1), duration=1.75, blendType='easeInOut'),
                                   LerpPosInterval(model, startPos=(-1.5, 0, 1.1), pos=(-1.5, 0, 0.5), duration=1.75, blendType='easeInOut'),
                                   )
        self.dropShadow.hide()
        return model

    def getSphereRadius(self):
        return 1.0

    def startAnimation(self):
        self.bounceLoop.loop()

    def handleGrab(self, avId):
        self.collNodePath.stash()
        self.avId = avId
        if avId in self.cr.doId2do:
            av = self.cr.doId2do[avId]
            self.av = av
        else:
            self.nodePath.detachNode()
            return
        if self.playSoundForRemoteToons or self.avId == base.localAvatar.getDoId():
            base.playSfx(self.grabSound, node=self.nodePath)
        if not self.fly:
            self.nodePath.detachNode()
            return
        self.dropShadow.wrtReparentTo(self.nodePath)
        self.nodePath.wrtReparentTo(av)
        if self.treasureFlyTrack:
            self.treasureFlyTrack.finish()
            self.treasureFlyTrack = None
        if self.bounceLoop:
            self.bounceLoop.stop()
            self.bounceLoop = None
        avatarGoneName = self.av.uniqueName('disable')
        self.accept(avatarGoneName, self.handleUnexpectedExit)
        flytime = 1.0
        track = Sequence(LerpPosInterval(self.nodePath, flytime, pos=(0, 0, 3), startPos=self.nodePath.getPos(), blendType='easeInOut'), Func(self.nodePath.detachNode), Func(self.ignore, avatarGoneName))
        if self.shadow:
            self.treasureFlyTrack = Sequence(HideInterval(self.dropShadow), track, ShowInterval(self.dropShadow), name=self.uniqueName('treasureFlyTrack'))
        else:
            self.treasureFlyTrack = Sequence(track, name=self.uniqueName('treasureFlyTrack'))
        self.treasureFlyTrack.start()
        return

    def delete(self):
        if self.treasureFlyTrack:
            self.treasureFlyTrack.finish()
            self.treasureFlyTrack = None
        if self.bounceLoop:
            self.bounceLoop.stop()
            self.bounceLoop = None
        DistributedObject.DistributedObject.delete(self)
        self.dropShadow.reparentTo(self.nodePath)
        self.nodePath.removeNode()
        return

    def handleUnexpectedExit(self):
        self.notify.warning('While getting treasure, ' + str(self.avId) + ' disconnected.')
        if self.treasureFlyTrack:
            self.treasureFlyTrack.finish()
            self.treasureFlyTrack = None
        if self.bounceLoop:
            self.bounceLoop.stop()
            self.bounceLoop = None
        return

