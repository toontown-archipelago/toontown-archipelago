from panda3d.core import *
from direct.gui.DirectGui import *
from direct.showbase import DirectObject
from otp.avatar import Avatar
from direct.distributed import DistributedObject
from . import SuitDNA
from toontown.battle import SuitBattleGlobals
from toontown.toonbase import TTLocalizer
from otp.avatar import AvatarPanel
from toontown.friends import FriendsListPanel
from toontown.suit import Suit
from direct.interval.IntervalGlobal import *
from direct.showbase import DirectObject
from panda3d.core import *


class SuitAvatarPanel(AvatarPanel.AvatarPanel, DirectObject.DirectObject):
    currentAvatarPanel = None

    POPUP_ANIMATION_DURATION = 0.1
    POPOUT_ANIMATION_DURATION = 0.1

    def __init__(self, avatar):
        AvatarPanel.AvatarPanel.__init__(self, avatar, FriendsListPanel=FriendsListPanel)
        self.avName = avatar.getName()
        self.avatr = avatar
        gui = loader.loadModel('phase_3.5/models/gui/suit_detail_panel')
        gui.find('**/shadow').setTransparency(TransparencyAttrib.MAlpha)
        gui.find('**/shadow').setColor(1, 1, 1, 0.4)
        self.frame = DirectFrame(geom=gui.find('**/avatar_panel'), geom_scale=0.21, geom_color=Suit.Suit.medallionColors[avatar.dna.dept], geom_pos=(0, 0, 0.02), relief=None, pos=(-0.2348, 0, -0.475), parent=base.a2dTopRight)
        self.head = self.frame.attachNewNode('head')
        for part in avatar.headParts:
            copyPart = part.copyTo(self.head)
            copyPart.setDepthTest(1)
            copyPart.setDepthWrite(1)

        p1 = Point3()
        p2 = Point3()
        self.head.calcTightBounds(p1, p2)
        d = p2 - p1
        biggest = max(d[0], d[1], d[2])
        s = 0.3 / biggest
        self.head.setPosHprScale(0, 0, 0, 180, 0, 0, s, s, s)
        self.nameLabel = DirectLabel(parent=self.frame, pos=(0.0125, 0, 0.36), relief=None, text=self.avName, text_font=avatar.getFont(), text_fg=Vec4(0, 0, 0, 1), text_pos=(0, 0), text_scale=0.047, text_wordwrap=7.5)
        level = avatar.getActualLevel()
        revives = avatar.getMaxSkeleRevives() + 1
        maxHP = avatar.maxHP
        HP = avatar.currHP
        self.hpLabel = DirectLabel(parent=self.frame, pos=(0.0125, 0, -0.15), relief=None, text=TTLocalizer.AvatarPanelCogHP % (HP, maxHP), text_font=avatar.getFont(), text_fg=Vec4(0, 0, 0, 1), text_pos=(0, 0), text_scale = 0.047, text_wordwrap = 7.5)
        dept = SuitDNA.getSuitDeptFullname(avatar.dna.name)
        if revives == 1:
            self.levelLabel = DirectLabel(parent=self.frame, pos=(0, 0, -0.1), relief=None, text=TTLocalizer.AvatarPanelCogLevel % level, text_font=avatar.getFont(), text_align=TextNode.ACenter, text_fg=Vec4(0, 0, 0, 1), text_pos=(0, 0), text_scale=0.05, text_wordwrap=8.0)
        elif revives > 1:
            self.levelLabel = DirectLabel(parent=self.frame, pos=(0, 0, -0.1), relief=None, text=TTLocalizer.AvatarPanelCogLevel % level + TTLocalizer.AvatarPanelCogRevives % revives, text_font=avatar.getFont(), text_align=TextNode.ACenter, text_fg=Vec4(0, 0, 0, 1), text_pos=(0, 0), text_scale=0.045, text_wordwrap=8.0)
        corpIcon = avatar.corpMedallion.copyTo(hidden)
        corpIcon.setPosHprScale(0, 0, 0, 0, 0, 0, 0, 0, 0)
        self.corpIcon = DirectLabel(parent=self.frame, geom=corpIcon, geom_scale=0.115, pos=(0, 0, -0.215), relief=None)
        corpIcon.removeNode()
        self.deptLabel = DirectLabel(parent=self.frame, pos=(0, 0, -0.31), relief=None, text=dept, text_font=avatar.getFont(), text_align=TextNode.ACenter, text_fg=Vec4(0, 0, 0, 1), text_pos=(0, 0), text_scale=0.05, text_wordwrap=8.0)
        self.closeButton = DirectButton(parent=self.frame, relief=None, pos=(0.0, 0, -0.36), text=TTLocalizer.AvatarPanelCogDetailClose, text_font=avatar.getFont(), text0_fg=Vec4(0, 0, 0, 1), text1_fg=Vec4(0.5, 0, 0, 1), text2_fg=Vec4(1, 0, 0, 1), text_pos=(0, 0), text_scale=0.05, command=self.__handleClose)
        gui.removeNode()
        base.localAvatar.obscureFriendsListButton(1)

        #create a LerpScaleInterval that scales the frame from 0 to 1
        self.currentInterval = self.__getOpenSequence()
        self.currentInterval.start()

        self.labelInterval = None

        self.frame.setBin("gui-popup", 0)
        self.frame.show()
        messenger.send('avPanelDone')

        self.accept(avatar.uniqueName('suitHpUpdate'), self.__updateHp)
        return

    def __updateHp(self, currHp, maxHp, delta):
        def __updateLabel(tempHp):
            self.hpLabel['text'] = TTLocalizer.AvatarPanelCogHP % (int(tempHp), maxHp)

        self.labelInterval = Parallel(
            LerpColorScaleInterval(self.hpLabel, duration=.2, startColorScale=(1, 0, 0, 1), colorScale=(1, 1, 1, 1), blendType='easeInOut'),
            LerpFunctionInterval(__updateLabel, duration=.2, fromData=currHp+delta, toData=currHp, blendType='easeInOut')
        )
        self.labelInterval.start()



    def __getOpenSequence(self) -> Sequence:
        return Sequence(
            LerpScaleInterval(self.frame, self.POPUP_ANIMATION_DURATION, Vec3(1.2, 1.2, 1.2), Vec3(0, 0, 0), blendType='easeIn'),
            LerpScaleInterval(self.frame, self.POPUP_ANIMATION_DURATION/2.0, Vec3(1, 1, 1), Vec3(1.2, 1.2, 1.2), blendType='easeInOut'),
        )

    def __getCloseSequence(self) -> Sequence:
        return Sequence(
            LerpScaleInterval(self.frame, self.POPOUT_ANIMATION_DURATION, Vec3(1.2, 1.2, 1.2), Vec3(1, 1, 1), blendType='easeIn'),
            LerpScaleInterval(self.frame, self.POPOUT_ANIMATION_DURATION/2.0, Vec3(0, 0, 0), Vec3(1.2, 1.2, 1.2),blendType='easeInOut'),
            Func(self.cleanup),
        )

    def __cleanupSequence(self):
        if self.currentInterval:
            self.currentInterval.finish()
            self.currentInterval = None

        if self.labelInterval:
            self.labelInterval.finish()
            self.labelInterval = None

    def cleanup(self):
        self.ignoreAll()
        self.__cleanupSequence()

        if self.frame:
            self.frame.destroy()
            self.frame = None
            base.localAvatar.obscureFriendsListButton(-1)

        if self.head:
            self.head.removeNode()
            self.head = None

        AvatarPanel.AvatarPanel.cleanup(self)
        self.panelNoneFunc()
        return
    
    def panelNoneFunc(self):
        AvatarPanel.currentAvatarPanel = None
        return

    def __handleClose(self):
        self.__cleanupSequence()

        # If someone abuses the GUI enough, frame could get deleted before we have a chance to play an animation :(
        if self.frame is None:
            self.cleanup()
            return

        self.currentInterval = self.__getCloseSequence()
        self.currentInterval.start()
        return

    @classmethod
    def getRevives(cls, cog):
        return cog.getSkeleRevives()
