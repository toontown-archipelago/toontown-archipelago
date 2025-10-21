from toontown.toonbase.ToontownBattleGlobals import *
import types
from direct.fsm import StateData
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from . import TownBattleAttackPanel
from . import TownBattleWaitPanel
from . import TownBattleChooseAvatarPanel
from . import TownBattleSOSPanel
from . import TownBattleSOSPetSearchPanel
from . import TownBattleSOSPetInfoPanel
from . import TownBattleToonPanel
from . import TownBattleSuitPanel
from toontown.toontowngui import TTDialog
from direct.directnotify import DirectNotifyGlobal
from toontown.battle import BattleBase
from toontown.toonbase import ToontownTimer
from direct.showbase import PythonUtil
from toontown.toonbase import TTLocalizer
from toontown.pets import PetConstants
from direct.gui.DirectGui import DGG
from toontown.battle import FireCogPanel

class TownBattle(StateData.StateData):
    notify = DirectNotifyGlobal.directNotify.newCategory('TownBattle')
    evenPos = (0.75,
     0.25,
     -0.25,
     -0.75)
    oddPos = (0.5, 0, -0.5)

    def __init__(self, doneEvent):
        StateData.StateData.__init__(self, doneEvent)
        self.numCogs = 1
        self.creditLevel = None
        self.luredIndices = []
        self.trappedIndices = []
        self.immuneIndices = []
        self.numToons = 1
        self.toons = []
        self.localNum = 0
        self.time = 0
        self.bldg = 0
        self.track = -1
        self.level = -1
        self.target = 0
        self.maxSuitLevel = 0
        self.toonAttacks = [(-1, 0, 0),
         (-1, 0, 0),
         (-1, 0, 0),
         (-1, 0, 0)]
        self.fsm = ClassicFSM.ClassicFSM('TownBattle', [
            State.State('Off',
                self.enterOff,
                self.exitOff,
                ['Attack']),
            State.State('Attack',
                self.enterAttack,
                self.exitAttack,
                ['ChooseCog',
                 'ChooseToon',
                 'AttackWait',
                 'Run',
                 'Fire',
                 'SOS']),
            State.State('ChooseCog',
                self.enterChooseCog,
                self.exitChooseCog,
                ['AttackWait',
                 'Attack']),
            State.State('AttackWait',
                self.enterAttackWait,
                self.exitAttackWait,
                ['ChooseCog',
                 'ChooseToon',
                 'Attack',
                 'Run']),
            State.State('ChooseToon',
                self.enterChooseToon,
                self.exitChooseToon,
                ['AttackWait',
                 'Attack']),
            State.State('Run',
                self.enterRun,
                self.exitRun,
                ['Attack']),
            State.State('SOS',
                self.enterSOS,
                self.exitSOS,
                ['Attack',
                 'AttackWait',
                 'SOSPetSearch',
                 'SOSPetInfo']),
            State.State('SOSPetSearch',
                self.enterSOSPetSearch,
                self.exitSOSPetSearch,
                ['SOS',
                 'SOSPetInfo']),
            State.State('SOSPetInfo',
                self.enterSOSPetInfo,
                self.exitSOSPetInfo,
                ['SOS',
                 'AttackWait']),
            State.State('Fire',
                self.enterFire,
                self.exitFire,
                ['Attack',
                 'AttackWait'])],
            'Off', 'Off')
        self.runPanel = TTDialog.TTDialog(dialogName='TownBattleRunPanel', text=TTLocalizer.TownBattleRun, style=TTDialog.TwoChoice, command=self.__handleRunPanelDone)
        self.runPanel.hide()
        self.attackPanelDoneEvent = 'attack-panel-done'
        self.attackPanel = TownBattleAttackPanel.TownBattleAttackPanel(self.attackPanelDoneEvent)
        self.waitPanelDoneEvent = 'wait-panel-done'
        self.waitPanel = TownBattleWaitPanel.TownBattleWaitPanel(self.waitPanelDoneEvent)
        self.chooseCogPanelDoneEvent = 'choose-cog-panel-done'
        self.chooseCogPanel = TownBattleChooseAvatarPanel.TownBattleChooseAvatarPanel(self.chooseCogPanelDoneEvent, 0)
        self.chooseToonPanelDoneEvent = 'choose-toon-panel-done'
        self.chooseToonPanel = TownBattleChooseAvatarPanel.TownBattleChooseAvatarPanel(self.chooseToonPanelDoneEvent, 1)
        self.SOSPanelDoneEvent = 'SOS-panel-done'
        self.SOSPanel = TownBattleSOSPanel.TownBattleSOSPanel(self.SOSPanelDoneEvent)
        self.SOSPetSearchPanelDoneEvent = 'SOSPetSearch-panel-done'
        self.SOSPetSearchPanel = TownBattleSOSPetSearchPanel.TownBattleSOSPetSearchPanel(self.SOSPetSearchPanelDoneEvent)
        self.SOSPetInfoPanelDoneEvent = 'SOSPetInfo-panel-done'
        self.SOSPetInfoPanel = TownBattleSOSPetInfoPanel.TownBattleSOSPetInfoPanel(self.SOSPetInfoPanelDoneEvent)
        self.fireCogPanelDoneEvent = 'fire-cog-panel-done'
        self.FireCogPanel = FireCogPanel.FireCogPanel(self.fireCogPanelDoneEvent)
        self.cogFireCosts = [None,
         None,
         None,
         None]
        self.toonPanels = (TownBattleToonPanel.TownBattleToonPanel(0),
         TownBattleToonPanel.TownBattleToonPanel(1),
         TownBattleToonPanel.TownBattleToonPanel(2),
         TownBattleToonPanel.TownBattleToonPanel(3))
        self.suitPanels = []
        for i in range(8):
            self.suitPanels.append(TownBattleSuitPanel.TownBattleSuitPanel(i))
        self.timer = ToontownTimer.ToontownTimer()
        self.timer.reparentTo(base.a2dBottomRight)
        self.timer.setPos(-0.151, 0, 0.158)
        self.timer.setScale(0.4)
        self.timer.hide()
        return

    def cleanup(self):
        self.ignore(self.attackPanelDoneEvent)
        self.unload()
        del self.fsm
        self.runPanel.cleanup()
        del self.runPanel
        del self.attackPanel
        del self.waitPanel
        del self.chooseCogPanel
        del self.chooseToonPanel
        del self.SOSPanel
        del self.FireCogPanel
        del self.SOSPetSearchPanel
        del self.SOSPetInfoPanel
        for toonPanel in self.toonPanels:
            toonPanel.cleanup()

        del self.toonPanels

        for suitPanel in self.suitPanels:
            suitPanel.cleanup()

        del self.suitPanels

        self.timer.destroy()
        del self.timer
        del self.toons

    def enter(self, event, parentFSMState, bldg = 0, creditMultiplier = 1, tutorialFlag = 0):
        self.parentFSMState = parentFSMState
        self.parentFSMState.addChild(self.fsm)
        if not self.isLoaded:
            self.load()
        print('Battle Event %s' % event)
        self.battleEvent = event
        self.fsm.enterInitialState()
        base.localAvatar.laffMeter.start()
        self.numToons = 1
        self.numCogs = 1
        self.toons = [base.localAvatar.doId]
        self.toonPanels[0].setLaffMeter(base.localAvatar)
        self.bldg = bldg
        self.creditLevel = None
        self.creditMultiplier = creditMultiplier
        self.tutorialFlag = tutorialFlag
        base.localAvatar.inventory.setBattleCreditMultiplier(self.creditMultiplier)
        base.localAvatar.inventory.setActivateMode('battle', heal=0, bldg=bldg, tutorialFlag=tutorialFlag)
        self.SOSPanel.bldg = bldg
        return

    def exit(self):
        base.localAvatar.laffMeter.stop()
        self.parentFSMState.removeChild(self.fsm)
        del self.parentFSMState
        localAvatar.inventory.setDefaultBattleCreditMultiplier()

    def load(self):
        if self.isLoaded:
            return
        self.attackPanel.load()
        self.waitPanel.load()
        self.chooseCogPanel.load()
        self.chooseToonPanel.load()
        self.SOSPanel.load()
        self.SOSPetSearchPanel.load()
        self.SOSPetInfoPanel.load()
        self.isLoaded = 1

    def unload(self):
        if not self.isLoaded:
            return
        self.attackPanel.unload()
        self.waitPanel.unload()
        self.chooseCogPanel.unload()
        self.chooseToonPanel.unload()
        self.FireCogPanel.unload()
        self.SOSPanel.unload()
        self.SOSPetSearchPanel.unload()
        self.SOSPetInfoPanel.unload()
        self.isLoaded = 0

    def setState(self, state):
        if hasattr(self, 'fsm'):
            self.fsm.request(state)

    def updateTimer(self, time):
        self.time = time
        self.timer.setTime(time)
        return None
    
    def __suitPanels(self, num):
        for panel in self.suitPanels:
            panel.hide()
            panel.setPos(0, 0, 0.7)

        for i in range(num):
            self.suitPanels[i].setX(((num - 1) * 0.25) - (i * 0.5))
            self.suitPanels[i].show()

    def __enterPanels(self, num, localNum):
        self.notify.debug('enterPanels() num: %d localNum: %d' % (num, localNum))
        for toonPanel in self.toonPanels:
            toonPanel.hide()
            toonPanel.setPos(0, 0, -0.9)

        if num == 1:
            self.toonPanels[0].setX(self.oddPos[1])
            self.toonPanels[0].show()
        elif num == 2:
            self.toonPanels[0].setX(self.evenPos[1])
            self.toonPanels[0].show()
            self.toonPanels[1].setX(self.evenPos[2])
            self.toonPanels[1].show()
        elif num == 3:
            self.toonPanels[0].setX(self.oddPos[0])
            self.toonPanels[0].show()
            self.toonPanels[1].setX(self.oddPos[1])
            self.toonPanels[1].show()
            self.toonPanels[2].setX(self.oddPos[2])
            self.toonPanels[2].show()
        elif num == 4:
            self.toonPanels[0].setX(self.evenPos[0])
            self.toonPanels[0].show()
            self.toonPanels[1].setX(self.evenPos[1])
            self.toonPanels[1].show()
            self.toonPanels[2].setX(self.evenPos[2])
            self.toonPanels[2].show()
            self.toonPanels[3].setX(self.evenPos[3])
            self.toonPanels[3].show()
        else:
            self.notify.error('Bad number of toons: %s' % num)
        return None

    def updateChosenAttacks(self, battleIndices, tracks, levels, targets):
        self.notify.debug('updateChosenAttacks bi=%s tracks=%s levels=%s targets=%s' % (battleIndices,
         tracks,
         levels,
         targets))
        numSounds = 0
        for i in range(4):
            if battleIndices[i] == -1:
                pass
            else:
                if tracks[i] == BattleBase.SOUND:
                    numSounds += 1
        for i in range(4):
            if battleIndices[i] == -1:
                pass
            else:
                if tracks[i] == BattleBase.NO_ATTACK:
                    numTargets = 0
                    target = -2
                elif tracks[i] == BattleBase.PASS_ATTACK:
                    numTargets = 0
                    target = -2
                elif tracks[i] == BattleBase.SOS or tracks[i] == BattleBase.NPCSOS or tracks[i] == BattleBase.PETSOS:
                    numTargets = 0
                    target = -2
                elif tracks[i] == HEAL_TRACK:
                    numTargets = self.numToons
                    if self.__isGroupHeal(levels[i]):
                        target = -2
                    else:
                        target = targets[i]
                else:
                    numTargets = self.numCogs
                    if self.__isGroupAttack(tracks[i], levels[i]):
                        target = -1
                    else:
                        target = targets[i]
                        if target == -1:
                            numTargets = None
                self.toonPanels[battleIndices[i]].setValues(battleIndices[i], tracks[i], levels[i], numTargets, target, self.localNum, numSounds, self.maxSuitLevel)

        return

    def chooseDefaultTarget(self):
        if self.track > -1:
            response = {}
            response['mode'] = 'Attack'
            response['track'] = self.track
            response['level'] = self.level
            response['target'] = self.target
            messenger.send(self.battleEvent, [response])
            return 1
        return 0

    def updateLaffMeter(self, toonNum, hp, maxHp):
        self.toonPanels[toonNum].updateLaffMeter(hp, maxHp)

    def enterOff(self):
        if self.isLoaded:
            for toonPanel in self.toonPanels:
                toonPanel.hide()
            
            for suitPanel in self.suitPanels:
                suitPanel.hide()

        self.toonAttacks = [(-1, 0, 0),
         (-1, 0, 0),
         (-1, 0, 0),
         (-1, 0, 0)]
        self.target = 0
        if hasattr(self, 'timer'):
            self.timer.hide()
        return None

    def exitOff(self):
        if self.isLoaded:
            self.__enterPanels(self.numToons, self.localNum)
            self.__suitPanels(self.numCogs)
        self.timer.show()
        self.track = -1
        self.level = -1
        self.target = 0
        return None

    def enterAttack(self):
        self.attackPanel.enter()
        self.accept(self.attackPanelDoneEvent, self.__handleAttackPanelDone)
        for toonPanel in self.toonPanels:
            toonPanel.setValues(0, BattleBase.NO_ATTACK)

        # If we are dead force a pass
        if localAvatar.hp <= 0:
            messenger.send('inventory-pass')

        return None

    def exitAttack(self):
        self.ignore(self.attackPanelDoneEvent)
        self.attackPanel.exit()
        return None

    def __handleAttackPanelDone(self, doneStatus):
        self.notify.debug('doneStatus: %s' % doneStatus)
        mode = doneStatus['mode']
        if mode == 'Inventory':
            self.track = doneStatus['track']
            self.level = doneStatus['level']
            self.toonPanels[self.localNum].setValues(self.localNum, self.track, self.level)
            if self.track == HEAL_TRACK:

                # Group TU
                if self.__isGroupHeal(self.level):
                    response = {}
                    response['mode'] = 'Attack'
                    response['track'] = self.track
                    response['level'] = self.level
                    response['target'] = self.target
                    messenger.send(self.battleEvent, [response])
                    self.fsm.request('AttackWait')

                # We need to pick the target
                elif self.numToons in (2, 3, 4):
                    self.fsm.request('ChooseToon')

                # We are alone, we can only heal ourselves
                elif self.numToons == 1:
                    response = {}
                    response['mode'] = 'Attack'
                    response['track'] = self.track
                    response['level'] = self.level
                    response['target'] = self.localNum
                    messenger.send(self.battleEvent, [response])
                    self.fsm.request('AttackWait')
                else:
                    self.notify.error('Heal was chosen when number of toons is %s' % self.numToons)
            elif self.__isCogChoiceNecessary():
                self.notify.debug('choice needed')
                self.fsm.request('ChooseCog')
                response = {}
                response['mode'] = 'Attack'
                response['track'] = self.track
                response['level'] = self.level
                response['target'] = -1
                messenger.send(self.battleEvent, [response])
            else:
                self.notify.debug('no choice needed')
                self.fsm.request('AttackWait')
                response = {}
                response['mode'] = 'Attack'
                response['track'] = self.track
                response['level'] = self.level
                response['target'] = 0
                messenger.send(self.battleEvent, [response])
        elif mode == 'Run':
            self.fsm.request('Run')
        elif mode == 'SOS':
            self.fsm.request('SOS')
        elif mode == 'Fire':
            self.fsm.request('Fire')
        elif mode == 'Pass':
            response = {}
            response['mode'] = 'Pass'
            response['id'] = -1
            messenger.send(self.battleEvent, [response])
            self.fsm.request('AttackWait')
        else:
            self.notify.warning('unknown mode: %s' % mode)

    def checkHealTrapLure(self):
        self.notify.debug('numToons: %s, numCogs: %s, lured: %s, trapped: %s' % (self.numToons,
         self.numCogs,
         self.luredIndices,
         self.trappedIndices))
        if len(PythonUtil.union(self.trappedIndices, self.luredIndices)) == self.numCogs:
            canTrap = 0
        else:
            canTrap = 1
        if len(self.luredIndices) == self.numCogs:
            canLure = 0
            canTrap = 0
        else:
            canLure = 1

        canHeal = 1
        return (canHeal, canTrap, canLure)

    def adjustCogsAndToons(self, cogs, luredIndices, trappedIndices, toons, immuneIndices):
        numCogs = len(cogs)
        self.notify.debug('adjustCogsAndToons() numCogs: %s self.numCogs: %s' % (numCogs, self.numCogs))
        self.notify.debug('adjustCogsAndToons() luredIndices: %s self.luredIndices: %s' % (luredIndices, self.luredIndices))
        self.notify.debug('adjustCogsAndToons() trappedIndices: %s self.trappedIndices: %s' % (trappedIndices, self.trappedIndices))
        toonIds = [toon.doId for toon in toons]
        self.notify.debug('adjustCogsAndToons() toonIds: %s self.toons: %s' % (toonIds, self.toons))
        self.notify.debug('adjustCogsAndToons() immuneIndices: %s self.immuneIndices: %s' % (immuneIndices, self.immuneIndices))
        self.maxSuitLevel = 0
        cogFireCostIndex = 0
        for cog in cogs:
            self.maxSuitLevel = max(self.maxSuitLevel, cog.getActualLevel())
            self.cogFireCosts[cogFireCostIndex] = 1
            cogFireCostIndex += 1

        creditLevel = self.maxSuitLevel
        if numCogs == self.numCogs and creditLevel == self.creditLevel and luredIndices == self.luredIndices and trappedIndices == self.trappedIndices and toonIds == self.toons and immuneIndices == self.immuneIndices:
            resetActivateMode = 0
        else:
            resetActivateMode = 1
        self.notify.debug('adjustCogsAndToons() resetActivateMode: %s' % resetActivateMode)
        self.numCogs = numCogs
        self.creditLevel = creditLevel
        self.luredIndices = luredIndices
        self.trappedIndices = trappedIndices
        self.immuneIndices = immuneIndices
        self.toons = toonIds
        self.numToons = len(toons)
        self.localNum = toons.index(base.localAvatar)
        currStateName = self.fsm.getCurrentState().getName()
        if resetActivateMode:
            self.__enterPanels(self.numToons, self.localNum)
            for i in range(len(toons)):
                self.toonPanels[i].setLaffMeter(toons[i])
            
            self.__suitPanels(self.numCogs)
                
            for i in range(self.numCogs):
                self.suitPanels[i].setCogInformation(cogs[i])

            if currStateName == 'ChooseCog':
                self.chooseCogPanel.adjustCogs(self.numCogs, self.luredIndices, self.trappedIndices, self.track, self.immuneIndices)
            elif currStateName == 'ChooseToon':
                self.immuneIndices = []
                for toonIndex, toon in enumerate(self.toons):
                    if base.cr.archipelagoManager and base.cr.archipelagoManager.onEnemyTeams(toon, base.localAvatar.doId):
                        self.immuneIndices.append(toon)
                self.chooseToonPanel.adjustToons(self.numToons, self.localNum, invalidTargets=self.immuneIndices)
            canHeal, canTrap, canLure = self.checkHealTrapLure()
            base.localAvatar.inventory.setBattleCreditMultiplier(self.creditMultiplier)
            base.localAvatar.inventory.setActivateMode('battle', heal=canHeal, trap=canTrap, lure=canLure, bldg=self.bldg, creditLevel=self.creditLevel, tutorialFlag=self.tutorialFlag)

    def enterChooseCog(self):
        self.cog = 0
        self.chooseCogPanel.enter(self.numCogs, luredIndices=self.luredIndices, trappedIndices=self.trappedIndices, immuneIndices=self.immuneIndices, track=self.track)
        self.accept(self.chooseCogPanelDoneEvent, self.__handleChooseCogPanelDone)
        return None

    def exitChooseCog(self):
        self.ignore(self.chooseCogPanelDoneEvent)
        self.chooseCogPanel.exit()
        return None

    def __handleChooseCogPanelDone(self, doneStatus):
        mode = doneStatus['mode']
        if mode == 'Back':
            self.fsm.request('Attack')
        elif mode == 'Avatar':
            self.cog = doneStatus['avatar']
            self.target = self.cog
            self.fsm.request('AttackWait')
            response = {}
            response['mode'] = 'Attack'
            response['track'] = self.track
            response['level'] = self.level
            response['target'] = self.cog
            messenger.send(self.battleEvent, [response])
        else:
            self.notify.warning('unknown mode: %s' % mode)

    def enterAttackWait(self, chosenToon = -1):
        self.accept(self.waitPanelDoneEvent, self.__handleAttackWaitBack)
        self.waitPanel.enter(self.numToons)

    def exitAttackWait(self):
        self.waitPanel.exit()
        self.ignore(self.waitPanelDoneEvent)

    def __handleAttackWaitBack(self, doneStatus):
        mode = doneStatus['mode']
        if mode == 'Back':

            # If we are dead this works as an alternative to run
            if localAvatar.hp <= 0:
                self.fsm.request('Run')
                return

            if self.track == HEAL_TRACK:
                self.fsm.request('Attack')
            elif self.track == BattleBase.NO_ATTACK:
                self.fsm.request('Attack')
            elif self.__isCogChoiceNecessary():
                self.fsm.request('ChooseCog')
            else:
                self.fsm.request('Attack')
            response = {}
            response['mode'] = 'UnAttack'
            messenger.send(self.battleEvent, [response])
        else:
            self.notify.error('unknown mode: %s' % mode)

    def enterChooseToon(self):

        immuneIndices = []
        for toonIndex, toon in enumerate(self.toons):
            if base.cr.archipelagoManager and base.cr.archipelagoManager.onEnemyTeams(toon, base.localAvatar.doId):
                immuneIndices.append(toonIndex)

        self.toon = 0
        self.chooseToonPanel.enter(self.numToons, localNum=self.localNum, immuneIndices=immuneIndices)
        self.accept(self.chooseToonPanelDoneEvent, self.__handleChooseToonPanelDone)
        return None

    def exitChooseToon(self):
        self.ignore(self.chooseToonPanelDoneEvent)
        self.chooseToonPanel.exit()
        return None

    def __handleChooseToonPanelDone(self, doneStatus):
        mode = doneStatus['mode']
        if mode == 'Back':
            self.fsm.request('Attack')
        elif mode == 'Avatar':
            self.toon = doneStatus['avatar']
            self.target = self.toon
            self.fsm.request('AttackWait', [self.toon])
            response = {}
            response['mode'] = 'Attack'
            response['track'] = self.track
            response['level'] = self.level
            response['target'] = self.toon
            messenger.send(self.battleEvent, [response])
        else:
            self.notify.warning('unknown mode: %s' % mode)

    def enterRun(self):
        self.runPanel.show()

    def exitRun(self):
        self.runPanel.hide()

    def __handleRunPanelDone(self, doneStatus):
        if doneStatus == DGG.DIALOG_OK:
            response = {}
            response['mode'] = 'Run'
            messenger.send(self.battleEvent, [response])
        else:
            self.fsm.request('Attack')

    def enterFire(self):
        canHeal, canTrap, canLure = self.checkHealTrapLure()
        self.FireCogPanel.enter(self.numCogs, luredIndices=self.luredIndices, trappedIndices=self.trappedIndices, track=self.track, fireCosts=self.cogFireCosts, immuneIndices=self.immuneIndices)
        self.accept(self.fireCogPanelDoneEvent, self.__handleCogFireDone)
        return None

    def exitFire(self):
        self.ignore(self.fireCogPanelDoneEvent)
        self.FireCogPanel.exit()
        return None

    def __handleCogFireDone(self, doneStatus):
        mode = doneStatus['mode']
        if mode == 'Back':
            self.fsm.request('Attack')
        elif mode == 'Avatar':
            self.cog = doneStatus['avatar']
            self.target = self.cog
            self.fsm.request('AttackWait')
            response = {}
            response['mode'] = 'Fire'
            response['target'] = self.cog
            messenger.send(self.battleEvent, [response])
        else:
            self.notify.warning('unknown mode: %s' % mode)

    def enterSOS(self):
        canHeal, canTrap, canLure = self.checkHealTrapLure()
        self.SOSPanel.enter(canLure, canTrap)
        self.accept(self.SOSPanelDoneEvent, self.__handleSOSPanelDone)
        return None

    def exitSOS(self):
        self.ignore(self.SOSPanelDoneEvent)
        self.SOSPanel.exit()
        return None

    def __handleSOSPanelDone(self, doneStatus):
        mode = doneStatus['mode']
        if mode == 'Friend':
            doId = doneStatus['friend']
            response = {}
            response['mode'] = 'SOS'
            response['id'] = doId
            messenger.send(self.battleEvent, [response])
            self.fsm.request('AttackWait')
        elif mode == 'Pet':
            self.petId = doneStatus['petId']
            self.petName = doneStatus['petName']
            self.fsm.request('SOSPetSearch')
        elif mode == 'NPCFriend':
            doId = doneStatus['friend']
            response = {}
            response['mode'] = 'NPCSOS'
            response['id'] = doId
            messenger.send(self.battleEvent, [response])
            self.fsm.request('AttackWait')
        elif mode == 'Back':
            self.fsm.request('Attack')

    def enterSOSPetSearch(self):
        response = {}
        response['mode'] = 'PETSOSINFO'
        response['id'] = self.petId
        self.SOSPetSearchPanel.enter(self.petId, self.petName)
        self.proxyGenerateMessage = 'petProxy-%d-generated' % self.petId
        self.accept(self.proxyGenerateMessage, self.__handleProxyGenerated)
        self.accept(self.SOSPetSearchPanelDoneEvent, self.__handleSOSPetSearchPanelDone)
        messenger.send(self.battleEvent, [response])
        return None

    def exitSOSPetSearch(self):
        self.ignore(self.proxyGenerateMessage)
        self.ignore(self.SOSPetSearchPanelDoneEvent)
        self.SOSPetSearchPanel.exit()
        return None

    def __handleSOSPetSearchPanelDone(self, doneStatus):
        mode = doneStatus['mode']
        if mode == 'Back':
            self.fsm.request('SOS')
        else:
            self.notify.error('invalid mode in handleSOSPetSearchPanelDone')

    def __handleProxyGenerated(self):
        self.fsm.request('SOSPetInfo')

    def enterSOSPetInfo(self):
        self.SOSPetInfoPanel.enter(self.petId)
        self.accept(self.SOSPetInfoPanelDoneEvent, self.__handleSOSPetInfoPanelDone)
        return None

    def exitSOSPetInfo(self):
        self.ignore(self.SOSPetInfoPanelDoneEvent)
        self.SOSPetInfoPanel.exit()
        return None

    def __handleSOSPetInfoPanelDone(self, doneStatus):
        mode = doneStatus['mode']
        if mode == 'OK':
            response = {}
            response['mode'] = 'PETSOS'
            response['id'] = self.petId
            response['trickId'] = doneStatus['trickId']
            messenger.send(self.battleEvent, [response])
            self.fsm.request('AttackWait')
            bboard.post(PetConstants.OurPetsMoodChangedKey, True)
        elif mode == 'Back':
            self.fsm.request('SOS')

    def __isCogChoiceNecessary(self):
        if self.numCogs > 1 and not self.__isGroupAttack(self.track, self.level):
            return 1
        else:
            return 0

    def __isGroupAttack(self, trackNum, levelNum):
        retval = BattleBase.attackAffectsGroup(trackNum, levelNum)
        return retval

    def __isGroupHeal(self, levelNum):
        retval = BattleBase.attackAffectsGroup(HEAL_TRACK, levelNum)
        return retval
