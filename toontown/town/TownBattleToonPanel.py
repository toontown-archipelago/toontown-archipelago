import math

from panda3d.core import *
from toontown.toonbase import ToontownGlobals
from toontown.toonbase.ToontownBattleGlobals import *
from direct.directnotify import DirectNotifyGlobal
import string
from toontown.toon import LaffMeter
from toontown.battle import BattleBase
from direct.gui.DirectGui import *
from toontown.toonbase import TTLocalizer

class TownBattleToonPanel(DirectFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory('TownBattleToonPanel')

    def __init__(self, id):
        gui = loader.loadModel('phase_3.5/models/gui/battle_gui')
        DirectFrame.__init__(self, relief=None, image=gui.find('**/ToonBtl_Status_BG'), image_color=Vec4(0.5, 0.9, 0.5, 0.7))
        self.setScale(0.8)
        self.initialiseoptions(TownBattleToonPanel)
        self.avatar = None
        self.sosText = DirectLabel(parent=self, relief=None, pos=(0.1, 0, 0.015), text=TTLocalizer.TownBattleToonSOS, text_scale=0.06)
        self.sosText.hide()
        self.fireText = DirectLabel(parent=self, relief=None, pos=(0.1, 0, 0.015), text=TTLocalizer.TownBattleToonFire, text_scale=0.06)
        self.fireText.hide()
        self.undecidedText = DirectLabel(parent=self, relief=None, pos=(0.1, 0, 0.015), text=TTLocalizer.TownBattleUndecided, text_scale=0.1)
        self.healthText = DirectLabel(parent=self, text='', pos=(-0.06, 0, -0.075), text_scale=0.055)
        self.gagDamageText = DirectLabel(parent=self, relief=None, pos=(0, 0, 0.15), text='', text_scale=.12, text_font=getSignFont(), text_fg=(1, 0, 0, 1))
        self.hpChangeEvent = None
        self.gagNode = self.attachNewNode('gag')
        self.gagNode.setPos(0.1, 0, 0.03)
        self.hasGag = 0
        passGui = gui.find('**/tt_t_gui_bat_pass')
        passGui.detachNode()
        self.passNode = self.attachNewNode('pass')
        self.passNode.setPos(0.1, 0, 0.05)
        passGui.setScale(0.2)
        passGui.reparentTo(self.passNode)
        self.passNode.hide()
        self.organicText = DirectLabel(parent=self, relief=None, pos=(0.135, 0, 0), text='+', text_scale=0.14, text_font=getSignFont(), text_fg=(0, 1, 0, 1))
        self.organicText.hide()
        self.laffMeter = None
        self.whichText = DirectLabel(parent=self, text='', pos=(0.1, 0, -0.08), text_scale=0.05)
        self.hide()
        gui.removeNode()
        return

    def setLaffMeter(self, avatar):
        self.notify.debug('setLaffMeter: new avatar %s' % avatar.doId)
        if self.avatar == avatar:
            messenger.send(self.avatar.uniqueName('hpChange'), [avatar.hp, avatar.maxHp, 1])
            return None
        else:
            if self.avatar:
                self.cleanupLaffMeter()
            self.avatar = avatar
            self.laffMeter = LaffMeter.LaffMeter(avatar.style, avatar.hp, avatar.maxHp)
            self.laffMeter.setAvatar(self.avatar)
            self.laffMeter.reparentTo(self)
            self.laffMeter.setPos(-0.06, 0, 0.05)
            self.laffMeter.setScale(0.045)
            self.laffMeter.start()
            self.setHealthText(avatar.hp, avatar.maxHp)
            self.hpChangeEvent = self.avatar.uniqueName('hpChange')
            self.accept(self.hpChangeEvent, self.setHealthText)
        return None

    def setHealthText(self, hp, maxHp, quietly = 0):
        self.healthText['text'] = TTLocalizer.TownBattleHealthText % {'hitPoints': hp,
         'maxHit': maxHp}

    def show(self):
        DirectFrame.show(self)
        if self.laffMeter:
            self.laffMeter.start()

    def hide(self):
        DirectFrame.hide(self)
        if self.laffMeter:
            self.laffMeter.stop()

    def updateLaffMeter(self, hp, maxHp):
        if self.laffMeter:
            self.laffMeter.adjustFace(hp, self.avatar.maxHp)
        self.setHealthText(hp, maxHp)

    def setValues(self, index, track, level = None, numTargets = None, targetIndex = None, localNum = None, numSounds=0, highestLevel=0):
        self.notify.debug('Toon Panel setValues: index=%s track=%s level=%s numTargets=%s targetIndex=%s localNum=%s' % (index,
         track,
         level,
         numTargets,
         targetIndex,
         localNum))
        self.undecidedText.hide()
        self.organicText.hide()
        self.sosText.hide()
        self.fireText.hide()
        self.gagNode.hide()
        self.whichText.hide()
        self.gagDamageText.hide()
        self.passNode.hide()
        if self.hasGag:
            self.gag.removeNode()
            self.hasGag = 0
        if track == BattleBase.NO_ATTACK or track == BattleBase.UN_ATTACK:
            self.undecidedText.show()
        elif track == BattleBase.PASS_ATTACK:
            self.passNode.show()
        elif track == BattleBase.FIRE:
            self.fireText.show()
            self.whichText.show()
            self.whichText['text'] = self.determineWhichText(numTargets, targetIndex, localNum, index)
        elif track == BattleBase.SOS or track == BattleBase.NPCSOS or track == BattleBase.PETSOS:
            self.sosText.show()
        elif track >= MIN_TRACK_INDEX and track <= MAX_TRACK_INDEX:
            self.undecidedText.hide()
            self.passNode.hide()
            self.gagNode.show()
            invButton = base.localAvatar.inventory.buttonLookup(track, level)
            self.gag = invButton.instanceUnderNode(self.gagNode, 'gag')
            if self.avatar.trackBonusLevel[track] >= level:
                self.organicText.show()
            else:
                self.organicText.hide()
            self.gag.setScale(0.8)
            self.gag.setPos(0, 0, 0.02)
            self.hasGag = 1
            dmg = getAvPropDamage(track, level, self.avatar.experience, self.avatar.trackBonusLevel[track] >= level, toonDamageMultiplier=self.avatar.getDamageMultiplier(), overflowMod=self.avatar.getOverflowMod())
            if track == BattleBase.SOUND:
                if self.avatar.trackBonusLevel[track] >= level:
                    mult = 1 + ((highestLevel * 2) / 100)
                    dmg = dmg * mult
                soundMults = [100, 80, 70, 60]
                dmg = math.ceil(dmg * soundMults[numSounds-1]/100)
            operator = '+' if track == HEAL_TRACK else '-'
            if track == LURE_TRACK:
                operator = '%'
                color = (1, 0.5, 0, 1)
            if track == HEAL_TRACK:
                color = (0, 1, 0, 1)
            elif track != LURE_TRACK:
                color = (1, 0, 0, 1)
            if track == LURE_TRACK:
                self.gagDamageText['text'] = f"{int(dmg)}{operator}"
            else:
                self.gagDamageText['text'] = f"{operator}{int(dmg)}"
            self.gagDamageText['text_fg'] = color
            self.gagDamageText.show()
            if numTargets is not None and targetIndex is not None and localNum is not None:
                self.whichText.show()
                self.whichText['text'] = self.determineWhichText(numTargets, targetIndex, localNum, index)
        else:
            self.notify.error('Bad track value: %s' % track)
        return

    def determineWhichText(self, numTargets, targetIndex, localNum, index):
        returnStr = ''
        targetList = list(range(numTargets))
        targetList.reverse()
        for i in targetList:
            if targetIndex in (-1, -2):
                returnStr += 'X'
            elif 0 <= targetIndex <= 3:
                if i == targetIndex:
                    returnStr += 'X'
                else:
                    returnStr += '-'
            else:
                self.notify.error('Bad target index: %s' % targetIndex)

        return returnStr

    def cleanup(self):
        self.ignoreAll()
        self.cleanupLaffMeter()
        if self.hasGag:
            self.gag.removeNode()
            del self.gag
        self.gagNode.removeNode()
        del self.gagNode
        DirectFrame.destroy(self)

    def cleanupLaffMeter(self):
        self.notify.debug('Cleaning up laffmeter!')
        self.ignore(self.hpChangeEvent)
        if self.laffMeter:
            self.laffMeter.destroy()
            self.laffMeter = None
        return
