from . import ShtikerPage
from toontown.toonbase import ToontownBattleGlobals
from direct.gui.DirectGui import *
from panda3d.core import *
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from ..battle.GagTrackBarGUI import GagTrackBarGUI


class InventoryPage(ShtikerPage.ShtikerPage):

    def __init__(self):
        ShtikerPage.ShtikerPage.__init__(self)
        self.currentTrackInfo = None
        self.onscreen = 0
        self.lastInventoryTime = globalClock.getRealTime()
        return

    def load(self):
        ShtikerPage.ShtikerPage.load(self)
        self.title = DirectLabel(parent=self, relief=None, text=TTLocalizer.InventoryPageTitle, text_scale=0.12, textMayChange=1, pos=(0, 0, 0.62))
        self.gagFrame = DirectFrame(parent=self, relief=None, pos=(0.1, 0, -0.47), scale=(0.35, 0.35, 0.35), geom=DGG.getDefaultDialogGeom(), geom_color=ToontownGlobals.GlobalDialogColor)
        self.trackInfo = DirectFrame(parent=self, relief=None, pos=(-0.4, 0, -0.47), scale=(0.35, 0.35, 0.35), geom=DGG.getDefaultDialogGeom(), geom_scale=(1.4, 1, 1), geom_color=ToontownGlobals.GlobalDialogColor, text='', text_wordwrap=11, text_align=TextNode.ALeft, text_scale=0.12, text_pos=(-0.65, 0.3), text_fg=(0.05, 0.14, 0.4, 1))
        self.trackProgress = GagTrackBarGUI(parent=self.trackInfo, track=0, pos=(0, 0, -0.25), scale=1.1)
        self.trackProgress.hide()
        jarGui = loader.loadModel('phase_3.5/models/gui/jar_gui')
        self.moneyDisplay = DirectLabel(parent=self, relief=None, pos=(0.55, 0, -0.5), scale=0.8, text=str(base.localAvatar.getMoney()), text_scale=0.18, text_fg=(0.95, 0.95, 0, 1), text_shadow=(0, 0, 0, 1), text_pos=(0, -0.1, 0), image=jarGui.find('**/Jar'), text_font=ToontownGlobals.getSignFont())
        jarGui.removeNode()
        return

    def unload(self):
        del self.title
        ShtikerPage.ShtikerPage.unload(self)

    def __moneyChange(self, money):
        self.moneyDisplay['text'] = str(money)

    def enter(self):
        ShtikerPage.ShtikerPage.enter(self)
        base.localAvatar.inventory.setActivateMode('book')
        base.localAvatar.inventory.show()
        base.localAvatar.inventory.reparentTo(self)
        self.moneyDisplay['text'] = str(base.localAvatar.getMoney())
        self.accept('enterBookDelete', self.enterDeleteMode)
        self.accept('exitBookDelete', self.exitDeleteMode)
        self.accept('enterTrackFrame', self.updateTrackInfo)
        self.accept('exitTrackFrame', self.clearTrackInfo)
        self.accept(localAvatar.uniqueName('moneyChange'), self.__moneyChange)

    def exit(self):
        ShtikerPage.ShtikerPage.exit(self)
        self.clearTrackInfo(self.currentTrackInfo)
        self.ignore('enterBookDelete')
        self.ignore('exitBookDelete')
        self.ignore('enterTrackFrame')
        self.ignore('exitTrackFrame')
        self.ignore(localAvatar.uniqueName('moneyChange'))
        self.makePageWhite(None)
        base.localAvatar.inventory.hide()
        base.localAvatar.inventory.reparentTo(hidden)
        self.exitDeleteMode()
        return

    def enterDeleteMode(self):
        self.title['text'] = TTLocalizer.InventoryPageDeleteTitle
        self.title['text_fg'] = (0, 0, 0, 1)
        self.book['image_color'] = Vec4(1, 1, 1, 1)

    def exitDeleteMode(self):
        self.title['text'] = TTLocalizer.InventoryPageTitle
        self.title['text_fg'] = (0, 0, 0, 1)
        self.book['image_color'] = Vec4(1, 1, 1, 1)

    def updateTrackInfo(self, trackIndex):
        self.currentTrackInfo = trackIndex
        self.trackProgress.setTrack(trackIndex)
        self.trackProgress.showExperience(base.localAvatar.experience, trackIndex)
        trackName = TextEncoder.upper(ToontownBattleGlobals.Tracks[trackIndex])
        if base.localAvatar.hasTrackAccess(trackIndex):
            curExp, nextExp = base.localAvatar.inventory.getCurAndNextExpValues(trackIndex)
            cap = base.localAvatar.experience.getExperienceCapForTrack(trackIndex)

            if curExp >= ToontownBattleGlobals.regMaxSkill:
                boost = ToontownBattleGlobals.getUberDamageBonusString(curExp)
                newTrackInfoText = TTLocalizer.InventoryPageTrackFull % (trackName, boost)
            elif cap < nextExp:
                newTrackInfoText = TTLocalizer.InventoryPageTrackLocked % trackName
            else:
                morePoints = nextExp - curExp
                newTrackInfoText = TTLocalizer.InventoryPageSinglePoint % {'trackName': trackName, 'numPoints': morePoints} if morePoints == 1 else TTLocalizer.InventoryPagePluralPoints % {'trackName': trackName, 'numPoints': morePoints}
                self.trackProgress.forceShowExperience(curExp, min(ToontownBattleGlobals.regMaxSkill, cap))

            self.trackInfo['text'] = newTrackInfoText
            self.trackProgress.show()
        else:
            newTrackInfoText = TTLocalizer.InventoryPageNoAccess % trackName
            self.trackInfo['text'] = newTrackInfoText
            self.trackProgress.hide()

    def clearTrackInfo(self, trackIndex):
        if self.currentTrackInfo == trackIndex:
            self.trackInfo['text'] = ''
            self.trackProgress.hide()
            self.currentTrackInfo = None
        return

    def acceptOnscreenHooks(self):
        self.accept(ToontownGlobals.InventoryHotkeyOn, self.showInventoryOnscreen)
        self.accept(ToontownGlobals.InventoryHotkeyOff, self.hideInventoryOnscreen)

    def ignoreOnscreenHooks(self):
        self.ignore(ToontownGlobals.InventoryHotkeyOn)
        self.ignore(ToontownGlobals.InventoryHotkeyOff)

    def showInventoryOnscreen(self):
        messenger.send('wakeup')
        timedif = globalClock.getRealTime() - self.lastInventoryTime
        if timedif < 0.7:
            return
        self.lastInventoryTime = globalClock.getRealTime()
        if self.onscreen or base.localAvatar.questPage.onscreen:
            return
        self.onscreen = 1
        base.localAvatar.inventory.setActivateMode('book')
        base.localAvatar.inventory.show()
        base.localAvatar.inventory.reparentTo(self)
        self.moneyDisplay['text'] = str(base.localAvatar.getMoney())
        self.accept('enterTrackFrame', self.updateTrackInfo)
        self.accept('exitTrackFrame', self.clearTrackInfo)
        self.accept(localAvatar.uniqueName('moneyChange'), self.__moneyChange)
        self.reparentTo(aspect2d)
        self.title.hide()
        self.show()

    def hideInventoryOnscreen(self):
        if not self.onscreen:
            return
        self.onscreen = 0
        self.ignore('enterTrackFrame')
        self.ignore('exitTrackFrame')
        self.ignore(localAvatar.uniqueName('moneyChange'))
        base.localAvatar.inventory.hide()
        base.localAvatar.inventory.reparentTo(hidden)
        self.reparentTo(self.book)
        self.title.show()
        self.hide()
