import random
import typing

from direct.interval.FunctionInterval import Func, Wait
from direct.interval.MetaInterval import Parallel, Sequence
from panda3d.core import Point3, Vec3
from panda3d.otp import CFSpeech, CFTimeout

from otp.avatar import Emote
from toontown.battle import SuitBattleGlobals
from toontown.battle.DistributedBattle import DistributedBattle
from toontown.suit.SuitDNA import getSuitType
from toontown.toonbase import ToontownGlobals

if typing.TYPE_CHECKING:
    from toontown.toonbase.ToonBaseGlobals import *


class DistributedBattleSandbox(DistributedBattle):
    def __init__(self, cr):
        super().__init__(cr)

    def __faceOff(self, ts, name, callback):
        if len(self.suits) == 0:
            self.notify.warning('__faceOff(): no suits.')
            return
        if len(self.toons) == 0:
            self.notify.warning('__faceOff(): no toons.')
            return
        elevatorPos = self.toons[0].getPos()
        if len(self.suits) == 1:
            leaderIndex = 0
        elif self.bossBattle == 1:
            leaderIndex = 1
        else:
            maxTypeNum = -1
            for suit in self.suits:
                suitTypeNum = getSuitType(suit.dna.name)
                if maxTypeNum < suitTypeNum:
                    maxTypeNum = suitTypeNum
                    leaderIndex = self.suits.index(suit)

        delay = 4.0
        suitTrack = Parallel()
        suitLeader = None
        for suit in self.suits:
            suit.setState('Battle')
            suitIsLeader = 0
            oneSuitTrack = Sequence()
            oneSuitTrack.append(Func(suit.loop, 'neutral'))
            oneSuitTrack.append(Func(suit.headsUp, elevatorPos))
            if self.suits.index(suit) == leaderIndex:
                suitLeader = suit
                suitIsLeader = 1
                taunt = SuitBattleGlobals.getFaceoffTaunt(suit.getStyleName(), suit.doId)
                oneSuitTrack.append(Func(suit.setChatAbsolute, taunt, CFSpeech | CFTimeout))
            destPos, destHpr = self.getActorPosHpr(suit, self.suits)
            oneSuitTrack.append(Wait(delay))
            if suitIsLeader == 1:
                oneSuitTrack.append(Func(suit.clearChat))
            oneSuitTrack.append(self.createAdjustInterval(suit, destPos, destHpr))
            suitTrack.append(oneSuitTrack)

        toonTrack = Parallel()
        for toon in self.toons:
            oneToonTrack = Sequence()
            destPos, destHpr = self.getActorPosHpr(toon, self.toons)
            oneToonTrack.append(Wait(delay))
            oneToonTrack.append(self.createAdjustInterval(toon, destPos, destHpr, toon=1, run=1))
            toonTrack.append(oneToonTrack)

        camTrack = Sequence()

        def setCamFov(fov):
            base.camLens.setMinFov(fov / (4. / 3.))

        camTrack.append(Func(camera.wrtReparentTo, suitLeader))
        camTrack.append(Func(setCamFov, self.camFOFov))
        suitHeight = suitLeader.getHeight()
        suitOffsetPnt = Point3(0, 0, suitHeight)
        MidTauntCamHeight = suitHeight * 0.66
        MidTauntCamHeightLim = suitHeight - 1.8
        if MidTauntCamHeight < MidTauntCamHeightLim:
            MidTauntCamHeight = MidTauntCamHeightLim
        TauntCamY = 18
        TauntCamX = 0
        TauntCamHeight = random.choice((MidTauntCamHeight, 1, 11))
        camTrack.append(Func(camera.setPos, TauntCamX, TauntCamY, TauntCamHeight))
        camTrack.append(Func(camera.lookAt, suitLeader, suitOffsetPnt))
        camTrack.append(Wait(delay))
        camPos = Point3(0, -6, 4)
        camHpr = Vec3(0, 0, 0)
        camTrack.append(Func(camera.reparentTo, base.localAvatar))
        camTrack.append(Func(setCamFov, ToontownGlobals.DefaultCameraFov))
        camTrack.append(Func(camera.setPosHpr, camPos, camHpr))
        mtrack = Parallel(suitTrack, toonTrack, camTrack)
        done = Func(callback)
        track = Sequence(mtrack, done, name=name)
        track.start(ts)
        self.storeInterval(track, name)
        return

    def enterFaceOff(self, ts):
        if len(self.toons) > 0 and base.localAvatar == self.toons[0]:
            Emote.globalEmote.disableAll(self.toons[0], 'dbattlebldg, enterFaceOff')
        self.delayDeleteMembers()
        self.__faceOff(ts, self.faceOffName, self.__handleFaceOffDone)
        return None

    def __handleFaceOffDone(self):
        self.notify.debug('FaceOff done')
        self.d_faceOffDone(base.localAvatar.doId)

    def exitFaceOff(self):
        self.notify.debug('exitFaceOff()')
        if len(self.toons) > 0 and base.localAvatar == self.toons[0]:
            Emote.globalEmote.releaseAll(self.toons[0], 'dbattlebldg exitFaceOff')
        self.clearInterval(self.faceOffName)
        self._removeMembersKeep()
        camera.wrtReparentTo(self)
        base.camLens.setMinFov(self.camFov / (4. / 3.))
        return None
