import random
import typing

from direct.fsm import State
from direct.gui.DirectButton import DirectButton
from direct.gui.DirectFrame import DirectFrame
from direct.gui.DirectGui import DGG
from direct.gui.DirectLabel import DirectLabel
from direct.interval.FunctionInterval import Func, Wait
from direct.interval.MetaInterval import Parallel, Sequence
from panda3d.core import Point3, Vec3, TextNode

from libotp import CFSpeech, CFTimeout
from otp.avatar import Emote
from toontown.battle import SuitBattleGlobals, DistributedBattleFinal
from toontown.battle.DistributedBattle import DistributedBattle
from toontown.suit.SuitDNA import getSuitType
from toontown.toonbase import ToontownGlobals

if typing.TYPE_CHECKING:
    from toontown.toonbase.ToonBaseGlobals import *


# Astron command #s
SET_MIN_LEVEL = 1
SET_MAX_LEVEL = 2


class ButtonGroup(DirectFrame):

    def __init__(self, option: str, callback, **kw: typing.Any):
        super().__init__(**kw)

        self.optionName: str = option
        self.value: int = 50

        self.__label = DirectLabel(parent=self, scale=0.05, text_align=TextNode.ACenter)
        self.__update_label()
        self.__decButton = DirectButton(parent=self, scale=.06, pos=(-.15, 0, 0), text='-1', command=self.__change_value, extraArgs=[-1])
        self.__bigDecButton = DirectButton(parent=self, scale=.06, pos=(-.25, 0, 0), text='-10', command=self.__change_value, extraArgs=[-10])
        self.__incButton = DirectButton(parent=self, scale=.06, pos=(.15, 0, 0), text='+1', command=self.__change_value, extraArgs=[1])
        self.__bigIncButton = DirectButton(parent=self, scale=.06, pos=(.25, 0, 0), text='+10', command=self.__change_value, extraArgs=[10])

        self.callback = callback

    def __change_value(self, delta: int):
        self.value += delta
        self.value = min(200, max(0, self.value))
        self.__update_label()
        self.callback(self.value)

    def __update_label(self):
        self.__label['text'] = f"{self.optionName}\n{self.value}"


class SandboxInterface(DirectFrame):
    def __init__(self, battle, **kw):

        optiondefs = (
            ('parent', kw['parent'], None),
            ('pos', kw['pos'], None),
        )
        self.defineoptions(kw, optiondefs)
        super().__init__(**kw)
        self.initialiseoptions(SandboxInterface)

        self.battle = battle

        self.minLevelGroup: ButtonGroup = ButtonGroup('Min Level', self.__setMinLevel, parent=self, pos=(0, 0, 0))
        self.maxLevelGroup: ButtonGroup = ButtonGroup('Max Level', self.__setMaxLevel, parent=self, pos=(0, 0, -.12))

    def __setMinLevel(self, level: int):
        self.battle.d_sendCommand(SET_MIN_LEVEL, level)

    def __setMaxLevel(self, level: int):
        self.battle.d_sendCommand(SET_MAX_LEVEL, level)


class DistributedBattleSandbox(DistributedBattle):
    def __init__(self, cr):
        super().__init__(cr)
        self.streetBattle = 0

        self.__optionsMenu: SandboxInterface = None


    """
    Management for spawning the "mod menu"
    """

    def __createOptionsMenu(self):
        self.__destroyOptionsMenu()
        self.__optionsMenu = SandboxInterface(self, parent=base.a2dLeftCenter, pos=(.35, 0, .3))

    def __destroyOptionsMenu(self):
        if self.__optionsMenu:
            self.__optionsMenu.destroy()
            self.__optionsMenu = None

    # If local toon is active, spawn the menu
    def enterWaitForInput(self, ts = 0):
        super().enterWaitForInput(ts)
        self.__destroyOptionsMenu()

        if self.localToonActive():
            self.__createOptionsMenu()

    # If menu was created, destroy it
    def exitWaitForInput(self):
        super().exitWaitForInput()
        self.__destroyOptionsMenu()

    # If local av is not in list of toons and menu was created, destroy it
    def setMembers(self, suits, suitsJoining, suitsPending, suitsActive, suitsLured, suitTraps, toons, toonsJoining, toonsPending, toonsActive, toonsRunning, immuneSuits, timestamp):
        super().setMembers(suits, suitsJoining, suitsPending, suitsActive, suitsLured, suitTraps, toons, toonsJoining, toonsPending, toonsActive, toonsRunning, immuneSuits, timestamp)

        if localAvatar.doId not in list(toons) + list(toonsActive) + list(toonsPending):
            self.__destroyOptionsMenu()

    # If menu was created, destroy it
    def delete(self):
        super().delete()
        self.__destroyOptionsMenu()

    # Sending command to the AI version of this battle
    def d_sendCommand(self, setting: int, value: int):
        self.sendUpdate('updateSetting', [setting, value])

    """
    Boilerplate code to make the battle function, can be ignored
    """

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
