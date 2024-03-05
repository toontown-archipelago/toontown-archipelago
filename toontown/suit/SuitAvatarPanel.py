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

    def __init__(self, avatar):
        AvatarPanel.AvatarPanel.__init__(self, avatar, FriendsListPanel=FriendsListPanel)
        self.avName = avatar.getName()
        self.avatr = avatar
        gui = loader.loadModel('phase_3.5/models/gui/suit_detail_panel')
        gui.find('**/shadow').setTransparency(TransparencyAttrib.MAlpha)
        gui.find('**/shadow').setColor(1, 1, 1, 0.4)
        self.frame = DirectFrame(geom=gui.find('**/avatar_panel'), geom_scale=0.21, geom_color=Suit.Suit.medallionColors[avatar.dna.dept], geom_pos=(0, 0, 0.02), relief=None, pos=(-0.2348, 0, -0.475), parent=base.a2dTopRight)
        disabledImageColor = Vec4(1, 1, 1, 0.4)
        text0Color = Vec4(1, 1, 1, 1)
        text1Color = Vec4(0.5, 1, 0.5, 1)
        text2Color = Vec4(1, 1, 0.5, 1)
        text3Color = Vec4(1, 1, 1, 0.2)
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
        self.nameLabel = DirectLabel(parent=self.frame, pos=(0.0125, 0, 0.36), relief=None, text=self.avName, text_font=avatar.getFont(), text_fg=Vec4(0, 0, 0, 1), text_pos=(0, 0), text_scale=0.047, text_wordwrap=7.5, text_shadow=(1, 1, 1, 1))
        level = avatar.getActualLevel()
        relativelevel = avatar.getLevel()
        revives = avatar.getMaxSkeleRevives() + 1
        attributes = SuitBattleGlobals.SuitAttributes[avatar.getStyleName()]
        maxHP = avatar.maxHP
        HP = avatar.currHP
        self.hpLabel = DirectLabel(parent=self.frame, pos=(0.0125, 0, -0.15), relief=None, text=TTLocalizer.AvatarPanelCogHP % (HP, maxHP), text_font=avatar.getFont(), text_fg=Vec4(0, 0, 0, 1), text_pos=(0, 0), text_scale = 0.047, text_wordwrap = 7.5, text_shadow=(1, 1, 1, 1))
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
        menuX = -0.05
        menuScale = 0.064
        base.localAvatar.obscureFriendsListButton(1)
        #create a LerpScaleInterval that scales the frame from 0 to 1
        self.scaleUpVisual = LerpScaleInterval(self.frame, 0.25, Vec3(1.2, 1.2, 1.2), Vec3(0, 0, 0), blendType='easeIn')
        self.scaleUpToNormal = LerpScaleInterval(self.frame, 0.15, Vec3(1, 1, 1), Vec3(1.2, 1.2, 1.2), blendType='easeInOut')
        self.scaleUpInterval = Sequence(self.scaleUpVisual, self.scaleUpToNormal)
        self.scaleUpInterval.start()
        self.frame.show()
        self.wantClose = False
        messenger.send('avPanelDone')
        return

    def cleanup(self):
        if self.wantClose == True:
            if self.frame == None:
                return
            self.frame.destroy()
            del self.frame
            self.frame = None
            self.head.removeNode()
            del self.head

            del self.scaleUpVisual
            del self.scaleUpToNormal
            del self.scaleUpInterval
            del self.scaleDownVisual
            del self.scaleDownToNormal
            del self.scaleDownInterval

            base.localAvatar.obscureFriendsListButton(-1)
            AvatarPanel.AvatarPanel.cleanup(self)
            self.panelNoneFunc()
        return
    
    def panelNoneFunc(self):
        AvatarPanel.currentAvatarPanel = None
        return
    
    def setWantClose(self, wantClose):
        self.wantClose = wantClose
        return

    def __handleClose(self):
        self.scaleUpInterval.finish()
        self.scaleDownVisual = LerpScaleInterval(self.frame, 0.25, Vec3(1.2, 1.2, 1.2), Vec3(1, 1, 1), blendType='easeIn')
        self.scaleDownToNormal = LerpScaleInterval(self.frame, 0.15, Vec3(0, 0, 0), Vec3(1.2, 1.2, 1.2), blendType='easeInOut')
        self.scaleDownInterval = Sequence(self.scaleDownVisual, self.scaleDownToNormal, Func(self.setWantClose, True), Func(self.cleanup), Func(self.setWantClose, False))
        self.scaleDownInterval.start()
        return

    @classmethod
    def getRevives(cls, cog):
        return cog.getSkeleRevives()
