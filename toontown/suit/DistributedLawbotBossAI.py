from otp.ai.AIBaseGlobal import *
from direct.distributed.ClockDelta import *
from . import DistributedBossCogAI
from direct.directnotify import DirectNotifyGlobal
from toontown.battle import BattleExperienceAI
from direct.fsm import FSM
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from toontown.toon import NPCToons
from toontown.chat import ResistanceChat
from . import SuitDNA
import random
from toontown.coghq import DistributedLawbotBossGavelAI, ScaleLeagueGlobals
from toontown.suit import DistributedLawbotBossSuitAI
from toontown.coghq import DistributedLawbotCannonAI
from toontown.coghq import DistributedLawbotChairAI
from toontown.toonbase import ToontownBattleGlobals

from apworld.toontown import locations
from ..archipelago.definitions.death_reason import DeathReason

from ..archipelago.definitions.util import ap_location_name_to_id


class DistributedLawbotBossAI(DistributedBossCogAI.DistributedBossCogAI, FSM.FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedLawbotBossAI')
    limitHitCount = 6
    hitCountDamage = 35
    numPies = 10
    maxToonLevels = 77

    def __init__(self, air):
        DistributedBossCogAI.DistributedBossCogAI.__init__(self, air, 'l')
        FSM.FSM.__init__(self, 'DistributedLawbotBossAI')
        self.lawyers = []
        self.cannons = None
        self.chairs = None
        self.gavels = None
        self.cagedToonNpcId = random.choice(list(NPCToons.npcFriends.keys()))
        self.bossMaxDamage = ToontownGlobals.LawbotBossMaxDamage
        self.recoverRate = 0
        self.recoverStartTime = 0
        self.bossDamage = ToontownGlobals.LawbotBossInitialDamage
        self.useCannons = 1
        self.numToonJurorsSeated = 0
        self.cannonBallsLeft = {}
        self.toonLevels = 0
        if 'Defeat' not in self.keyStates:
            self.keyStates.append('Defeat')
        self.toonupValue = 1
        self.bonusState = False
        self.bonusTimeStarted = 0
        self.numBonusStates = 0
        self.battleThreeTimeStarted = 0
        self.battleThreeTimeInMin = 0
        self.numAreaAttacks = 0
        self.lastAreaAttackTime = 0
        self.weightPerToon = {}
        self.cannonIndexPerToon = {}
        self.battleDifficulty = 0

        self.ruleset = ScaleLeagueGlobals.CJRuleset()
        return

    def toonDied(self, toon):
        toon.b_setNumPies(0)
        DistributedBossCogAI.DistributedBossCogAI.toonDied(self, toon)

    def announceGenerate(self):
        DistributedBossCogAI.DistributedBossCogAI.announceGenerate(self)
        self.setupRuleset()

    def d_lawyerDisable(self, avId):
        self.incrementCombo(avId, int(round(self.getComboLength(avId) / 5.0) + 2.0))
        self.sendUpdate('lawyerDisabled', [avId])

    def setupRuleset(self):
        self.ruleset = ScaleLeagueGlobals.CJRuleset()
        # Make sure they didn't do anything bad
        self.ruleset.validate()
        # Update the client
        self.d_setRawRuleset()

    # Any time you change the ruleset, you should call this to sync the clients
    def d_setRawRuleset(self):
        print((self.getRawRuleset()))
        self.sendUpdate('setRawRuleset', [self.getRawRuleset()])

    def getRawRuleset(self):
        return self.ruleset.asStruct()

    def delete(self):
        self.notify.debug('DistributedLawbotBossAI.delete')
        self.__deleteBattleThreeObjects()
        self.__deleteBattleTwoObjects()
        taskName = self.uniqueName('clearBonus')
        taskMgr.remove(taskName)
        return DistributedBossCogAI.DistributedBossCogAI.delete(self)

    def getHoodId(self):
        return ToontownGlobals.LawbotHQ

    def getCagedToonNpcId(self):
        return self.cagedToonNpcId

    def magicWordHit(self, damage, avId):
        if self.attackCode != ToontownGlobals.BossCogDizzyNow:
            self.hitBossInsides()
        self.hitBoss(damage)

    def hitBoss(self, bossDamage):
        avId = self.air.getAvatarIdFromSender()
        if not self.validate(avId, avId in self.involvedToons, 'hitBoss from unknown avatar'):
            return
        self.validate(avId, bossDamage == 1, 'invalid bossDamage %s' % bossDamage)
        if bossDamage < 1:
            return
        currState = self.getCurrentOrNextState()
        if currState != 'BattleThree':
            return
        if bossDamage <= 50:
            newWeight = self.weightPerToon.get(avId)
            if newWeight:
                bossDamage = newWeight
        if self.bonusState and bossDamage <= 50:
            bossDamage *= ToontownGlobals.LawbotBossBonusWeightMultiplier

        dmgDealt = bossDamage

        bossDamage = min(self.getBossDamage() + bossDamage, self.bossMaxDamage)
        self.b_setBossDamage(bossDamage, 0, 0)
        if self.bossDamage >= self.bossMaxDamage:
            self.b_setState('Victory')
        else:
            self.__recordHit()

        self.incrementCombo(avId, int(round(self.getComboLength(avId)) / 5 + 1))
        self.d_damageDealt(avId, dmgDealt)

    def healBoss(self, bossHeal):
        bossDamage = -bossHeal
        avId = self.air.getAvatarIdFromSender()
        currState = self.getCurrentOrNextState()
        if currState != 'BattleThree':
            return
        bossDamage = min(self.getBossDamage() + bossDamage, self.bossMaxDamage)
        bossDamage = max(bossDamage, 0)
        self.b_setBossDamage(bossDamage, 0, 0)
        if self.bossDamage == 0:
            self.b_setState('Defeat')
        else:
            self.__recordHit()

    def hitBossInsides(self):
        avId = self.air.getAvatarIdFromSender()
        if not self.validate(avId, avId in self.involvedToons, 'hitBossInsides from unknown avatar'):
            return
        currState = self.getCurrentOrNextState()
        if currState != 'BattleThree':
            return
        self.b_setAttackCode(ToontownGlobals.BossCogDizzyNow)
        self.b_setBossDamage(self.getBossDamage(), 0, 0)

    def hitToon(self, toonId):
        avId = self.air.getAvatarIdFromSender()
        if not self.validate(avId, avId != toonId, 'hitToon on self'):
            return
        if avId not in self.involvedToons or toonId not in self.involvedToons:
            return
        toon = self.air.doId2do.get(toonId)
        if toon and toon.hp > 0:
            hp = min(self.toonupValue, toon.maxHp - toon.hp)
            self.healToon(toon, hp)
            self.d_avHealed(avId, hp)
            self.sendUpdate('toonGotHealed', [toonId])

    def touchCage(self):
        avId = self.air.getAvatarIdFromSender()
        currState = self.getCurrentOrNextState()
        if currState != 'BattleThree' and currState != 'NearVictory':
            return
        if not self.validate(avId, avId in self.involvedToons, 'touchCage from unknown avatar'):
            return
        toon = simbase.air.doId2do.get(avId)
        if toon:
            toon.b_setNumPies(self.numPies)
            toon.__touchedCage = 1

    def touchWitnessStand(self):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        if av and av.getHp() <= 0:
            return

        self.touchCage()

    def finalPieSplat(self):
        self.notify.debug('finalPieSplat')
        if self.state != 'NearVictory':
            return
        self.b_setState('Victory')

    def doTaunt(self):
        if not self.state == 'BattleThree':
            return
        tauntIndex = random.randrange(len(TTLocalizer.LawbotBossTaunts))
        extraInfo = 0
        if tauntIndex == 0 and self.involvedToons:
            extraInfo = random.randrange(len(self.involvedToons))
        self.sendUpdate('setTaunt', [tauntIndex, extraInfo])

    def doNextAttack(self, task):
        for lawyer in self.lawyers:
            lawyer.doNextAttack(self)
            
        self.waitForNextAttack(ToontownGlobals.LawbotBossLawyerCycleTime)
        timeSinceLastAttack = globalClock.getFrameTime() - self.lastAreaAttackTime
        allowedByTime = 15 < timeSinceLastAttack or self.lastAreaAttackTime == 0
        doAttack = random.randrange(1,101)
        self.notify.debug('allowedByTime=%d doAttack=%d' % (allowedByTime, doAttack))
        if doAttack <= ToontownGlobals.LawbotBossChanceToDoAreaAttack and allowedByTime:
            self.__doAreaAttack()
            self.numAreaAttacks += 1
            self.lastAreaAttackTime = globalClock.getFrameTime()
        else:
            chanceToDoTaunt = ToontownGlobals.LawbotBossChanceForTaunt
            action = random.randrange(1,101)
            if action <= chanceToDoTaunt:
                self.doTaunt()
                pass
        return
        if self.attackCode == ToontownGlobals.BossCogDizzyNow:
            attackCode = ToontownGlobals.BossCogRecoverDizzyAttack
        else:
            attackCode = random.choice([ToontownGlobals.BossCogAreaAttack,
             ToontownGlobals.BossCogFrontAttack,
             ToontownGlobals.BossCogDirectedAttack,
             ToontownGlobals.BossCogDirectedAttack,
             ToontownGlobals.BossCogDirectedAttack,
             ToontownGlobals.BossCogDirectedAttack])
        if attackCode == ToontownGlobals.BossCogAreaAttack: 
            self.__doAreaAttack()
        elif attackCode == ToontownGlobals.BossCogDirectedAttack:
            self.__doDirectedAttack()
        else:
            self.b_setAttackCode(attackCode)

    def __doAreaAttack(self):
        self.b_setAttackCode(ToontownGlobals.BossCogAreaAttack)

    def __doDirectedAttack(self):
        if self.nearToons:
            toonId = random.choice(self.nearToons)
            self.b_setAttackCode(ToontownGlobals.BossCogDirectedAttack, toonId)
        else:
            self.__doAreaAttack()

    def b_setBossDamage(self, bossDamage, recoverRate, recoverStartTime):
        self.d_setBossDamage(bossDamage, recoverRate, recoverStartTime)
        self.setBossDamage(bossDamage, recoverRate, recoverStartTime)

    def setBossDamage(self, bossDamage, recoverRate, recoverStartTime):
        self.bossDamage = bossDamage
        self.recoverRate = recoverRate
        self.recoverStartTime = recoverStartTime

    def getBossDamage(self):
        now = globalClock.getFrameTime()
        elapsed = now - self.recoverStartTime
        return int(max(self.bossDamage - self.recoverRate * elapsed / 60.0, 0))

    def d_setBossDamage(self, bossDamage, recoverRate, recoverStartTime):
        timestamp = globalClockDelta.localToNetworkTime(recoverStartTime)
        self.sendUpdate('setBossDamage', [bossDamage, recoverRate, timestamp])

    def waitForNextStrafe(self, delayTime):
        currState = self.getCurrentOrNextState()
        if currState == 'BattleThree':
            taskName = self.uniqueName('NextStrafe')
            taskMgr.remove(taskName)
            taskMgr.doMethodLater(delayTime, self.doNextStrafe, taskName)

    def stopStrafes(self):
        taskName = self.uniqueName('NextStrafe')
        taskMgr.remove(taskName)

    def doNextStrafe(self, task):
        if self.attackCode != ToontownGlobals.BossCogDizzyNow:
            side = random.choice([0, 1])
            direction = random.choice([0, 1])
            self.sendUpdate('doStrafe', [side, direction])
        delayTime = 9
        self.waitForNextStrafe(delayTime)

    def __sendLawyerIds(self):
        lawyerIds = []
        for suit in self.lawyers:
            lawyerIds.append(suit.doId)

        self.sendUpdate('setLawyerIds', [lawyerIds])

    def d_cagedToonBattleThree(self, index, avId):
        self.sendUpdate('cagedToonBattleThree', [index, avId])

    def formatReward(self):
        return str(self.cagedToonNpcId)

    def makeBattleOneBattles(self):
        self.postBattleState = 'RollToBattleTwo'
        self.initializeBattles(1, ToontownGlobals.LawbotBossBattleOnePosHpr)

    def generateSuits(self, battleNumber):
        if battleNumber == 1:
            return self.invokeSuitPlanner(4, 0)
        else:
            return self.invokeSuitPlanner(4, 1)

    def removeToon(self, avId, died=False):
        toon = simbase.air.doId2do.get(avId)
        if toon:
            toon.b_setNumPies(0)
        DistributedBossCogAI.DistributedBossCogAI.removeToon(self, avId, died=died)

    def enterOff(self):
        self.notify.debug('enterOff')
        DistributedBossCogAI.DistributedBossCogAI.enterOff(self)
        self.__deleteBattleThreeObjects()
        self.__resetLawyers()

    def enterElevator(self):
        self.notify.debug('enterElevatro')
        DistributedBossCogAI.DistributedBossCogAI.enterElevator(self)
        self.b_setBossDamage(ToontownGlobals.LawbotBossInitialDamage, 0, 0)

    def enterIntroduction(self):
        self.notify.debug('enterIntroduction')
        DistributedBossCogAI.DistributedBossCogAI.enterIntroduction(self)
        self.b_setBossDamage(ToontownGlobals.LawbotBossInitialDamage, 0, 0)
        self.__makeChairs()

    def exitIntroduction(self):
        self.notify.debug('exitIntroduction')
        DistributedBossCogAI.DistributedBossCogAI.exitIntroduction(self)

    def enterRollToBattleTwo(self):
        self.canSkip = True
        self.listenForToonDeaths()
        self.divideToons()
        self.__makeCannons()
        self.barrier = self.beginBarrier('RollToBattleTwo', self.involvedToons, 50, self.__doneRollToBattleTwo)

    def __doneRollToBattleTwo(self, avIds):
        self.b_setState('PrepareBattleTwo')

    def exitRollToBattleTwo(self):
        self.canSkip = False
        self.ignoreBarrier(self.barrier)

    def enterPrepareBattleTwo(self):
        self.__makeCannons()
        self.barrier = self.beginBarrier('PrepareBattleTwo', self.involvedToons, 45, self.__donePrepareBattleTwo)
        self.makeBattleTwoBattles()

    def __donePrepareBattleTwo(self, avIds):
        self.b_setState('BattleTwo')

    def exitPrepareBattleTwo(self):
        self.ignoreBarrier(self.barrier)

    def __makeCannons(self):
        if self.cannons == None:
            self.cannons = []
            startPt = Point3(*ToontownGlobals.LawbotBossCannonPosA)
            endPt = Point3(*ToontownGlobals.LawbotBossCannonPosB)
            totalDisplacement = endPt - startPt
            self.notify.debug('totalDisplacement=%s' % totalDisplacement)
            numToons = len(self.involvedToons)
            numToons = 8
            stepDisplacement = totalDisplacement / (numToons + 1)
            for index in range(numToons):
                newPos = stepDisplacement * (index + 1)
                self.notify.debug('curDisplacement = %s' % newPos)
                newPos += startPt
                self.notify.debug('newPos = %s' % newPos)
                cannon = DistributedLawbotCannonAI.DistributedLawbotCannonAI(self.air, self, index, newPos[0], newPos[1], newPos[2], -90, 0, 0)
                cannon.generateWithRequired(self.zoneId)
                self.cannons.append(cannon)

        return

    def __makeChairs(self):
        if self.chairs == None:
            self.chairs = []
            for index in range(12):
                chair = DistributedLawbotChairAI.DistributedLawbotChairAI(self.air, self, index)
                chair.generateWithRequired(self.zoneId)
                self.chairs.append(chair)

        return

    def __makeBattleTwoObjects(self):
        self.__makeCannons()
        self.__makeChairs()

    def __deleteCannons(self):
        if self.cannons != None:
            for cannon in self.cannons:
                cannon.requestDelete()

            self.cannons = None
        return

    def __deleteChairs(self):
        if self.chairs != None:
            for chair in self.chairs:
                chair.requestDelete()

            self.chairs = None
        return

    def __stopChairs(self):
        if self.chairs != None:
            for chair in self.chairs:
                chair.stopCogs()

        return

    def __deleteBattleTwoObjects(self):
        self.__deleteCannons()
        self.__deleteChairs()

    def getCannonBallsLeft(self, avId):
        if avId in self.cannonBallsLeft:
            return self.cannonBallsLeft[avId]
        else:
            self.notify.warning('getCannonBalsLeft invalid avId: %d' % avId)
            return 0

    def decrementCannonBallsLeft(self, avId):
        if avId in self.cannonBallsLeft:
            self.cannonBallsLeft[avId] -= 1
            if self.cannonBallsLeft[avId] < 0:
                self.notify.warning('decrementCannonBallsLeft <0 cannonballs for %d' % avId)
                self.cannonBallsLeft[avId] = 0
        else:
            self.notify.warning('decrementCannonBallsLeft invalid avId: %d' % avId)

    def makeBattleTwoBattles(self):
        self.postBattleState = 'RollToBattleThree'
        if self.useCannons:
            self.__makeBattleTwoObjects()
        else:
            self.initializeBattles(2, ToontownGlobals.LawbotBossBattleTwoPosHpr)

    def enterBattleTwo(self):
        if self.useCannons:
            self.cannonBallsLeft = {}
            for toonId in self.involvedToons:
                self.cannonBallsLeft[toonId] = ToontownGlobals.LawbotBossCannonBallMax

            for chair in self.chairs:
                chair.requestEmptyJuror()

            self.barrier = self.beginBarrier('BattleTwo', self.involvedToons, ToontownGlobals.LawbotBossJuryBoxMoveTime + 1, self.__doneBattleTwo)
        if not self.useCannons:
            if self.battleA:
                self.battleA.startBattle(self.toonsA, self.suitsA)
            if self.battleB:
                self.battleB.startBattle(self.toonsB, self.suitsB)

    def __doneBattleTwo(self, avIds):
        if self.useCannons:
            self.b_setState('PrepareBattleThree')
        else:
            self.b_setState('RollToBattleThree')

    def exitBattleTwo(self):
        self.resetBattles()
        self.numToonJurorsSeated = 0
        for chair in self.chairs:
            self.notify.debug('chair.state==%s' % chair.state)
            if chair.state == 'ToonJuror':
                self.numToonJurorsSeated += 1

        self.notify.debug('numToonJurorsSeated=%d' % self.numToonJurorsSeated)
        self.air.writeServerEvent('jurorsSeated', self.doId, '%s|%s|%s' % (self.dept, self.involvedToons, self.numToonJurorsSeated))
        self.__deleteCannons()
        self.__stopChairs()

    def enterRollToBattleThree(self):
        self.divideToons()
        self.barrier = self.beginBarrier('RollToBattleThree', self.involvedToons, 20, self.__doneRollToBattleThree)

    def __doneRollToBattleThree(self, avIds):
        self.b_setState('PrepareBattleThree')

    def exitRollToBattleThree(self):
        self.ignoreBarrier(self.barrier)

    def enterPrepareBattleThree(self):
        self.calcAndSetBattleDifficulty()
        self.barrier = self.beginBarrier('PrepareBattleThree', self.involvedToons, 45, self.__donePrepareBattleThree)

    def __donePrepareBattleThree(self, avIds):
        self.b_setState('BattleThree')

    def exitPrepareBattleThree(self):
        self.ignoreBarrier(self.barrier)

    def enterBattleThree(self):
        self.divideToons()
        self.battleThreeTimeStarted = globalClock.getFrameTime()
        self.calcAndSetBattleDifficulty()
        if self.chairs != None:
            self.calculateWeightPerToon()
        diffSettings = ToontownGlobals.LawbotBossDifficultySettings[self.battleDifficulty]
        self.ammoCount = diffSettings[0]
        self.numGavels = diffSettings[1]
        if self.numGavels >= len(ToontownGlobals.LawbotBossGavelPosHprs):
            self.numGavels = len(ToontownGlobals.LawbotBossGavelPosHprs)
        self.numLawyers = diffSettings[2]
        if self.numLawyers >= len(ToontownGlobals.LawbotBossLawyerPosHprs):
            self.numLawyers = len(ToontownGlobals.LawbotBossLawyerPosHprs)
        self.toonupValue = diffSettings[3]
        self.notify.debug('diffLevel=%d ammoCount=%d gavels=%d lawyers = %d, toonup=%d' % (self.battleDifficulty,
         self.ammoCount,
         self.numGavels,
         self.numLawyers,
         self.toonupValue))
        self.air.writeServerEvent('lawbotBossSettings', self.doId, '%s|%s|%s|%s|%s|%s' % (self.dept,
         self.battleDifficulty,
         self.ammoCount,
         self.numGavels,
         self.numLawyers,
         self.toonupValue))
        self.__makeBattleThreeObjects()
        self.__makeLawyers()
        self.numPies = self.ammoCount
        self.resetBattles()
        self.setPieType()
        jurorsOver = self.numToonJurorsSeated - ToontownGlobals.LawbotBossJurorsForBalancedScale
        dmgAdjust = jurorsOver * ToontownGlobals.LawbotBossDamagePerJuror
        self.b_setBossDamage(ToontownGlobals.LawbotBossInitialDamage + dmgAdjust, 0, 0)
        if simbase.config.GetBool('lawbot-boss-cheat', 0):
            self.b_setBossDamage(ToontownGlobals.LawbotBossMaxDamage - 1, 0, 0)
        self.battleThreeStart = globalClock.getFrameTime()
        for toonId in self.involvedToons:
            toon = simbase.air.doId2do.get(toonId)
            if toon:
                toon.__touchedCage = 0

        for aGavel in self.gavels:
            aGavel.turnOn()

        self.waitForNextAttack(5)
        self.notify.debug('battleDifficulty = %d' % self.battleDifficulty)
        self.numToonsAtStart = len(self.involvedToons)
        if self.chairs != None:
             self.__deleteChairs()

        self.initializeComboTrackers()
        self.listenForToonDeaths()

    def getToonDifficulty(self):
        totalCogSuitLevels = 0.0
        totalNumToons = 0.0
        for toonId in self.involvedToons:
            toon = simbase.air.doId2do.get(toonId)
            if toon:
                toonLevel = toon.getNumPromotions(self.dept)
                totalCogSuitLevels += toonLevel
                totalNumToons += 1

        if not totalNumToons:
            totalNumToons = 1.0
        averageLevel = totalCogSuitLevels / totalNumToons
        retval = min(averageLevel, self.maxToonLevels)
        return retval

    def __saySomething(self, task = None):
        index = None
        avId = 0
        if len(self.involvedToons) == 0:
            return
        avId = random.choice(self.involvedToons)
        toon = simbase.air.doId2do.get(avId)
        if toon.__touchedCage:
            if self.cagedToonDialogIndex <= TTLocalizer.CagedToonBattleThreeMaxAdvice:
                index = self.cagedToonDialogIndex
                self.cagedToonDialogIndex += 1
            elif random.random() < 0.2:
                index = random.randrange(100, TTLocalizer.CagedToonBattleThreeMaxAdvice + 1)
        else:
            index = random.randrange(20, TTLocalizer.CagedToonBattleThreeMaxTouchCage + 1)
        if index:
            self.d_cagedToonBattleThree(index, avId)
        self.__saySomethingLater()
        return

    def __saySomethingLater(self, delayTime = 15):
        taskName = self.uniqueName('CagedToonSaySomething')
        taskMgr.remove(taskName)
        taskMgr.doMethodLater(delayTime, self.__saySomething, taskName)

    def __goodJump(self, avId):
        currState = self.getCurrentOrNextState()
        if currState != 'BattleThree':
            return
        index = random.randrange(10, TTLocalizer.CagedToonBattleThreeMaxGivePies + 1)
        self.d_cagedToonBattleThree(index, avId)
        self.__saySomethingLater()

    def __makeBattleThreeObjects(self):
        if self.gavels == None:
            self.gavels = []
            for index in range(self.numGavels):
                gavel = DistributedLawbotBossGavelAI.DistributedLawbotBossGavelAI(self.air, self, index)
                gavel.generateWithRequired(self.zoneId)
                self.gavels.append(gavel)

        return

    def __deleteBattleThreeObjects(self):
        if self.gavels != None:
            for gavel in self.gavels:
                gavel.request('Off')
                gavel.requestDelete()

            self.gavels = None
        return

    def doBattleThreeInfo(self):
        didTheyWin = 0
        if self.bossDamage == ToontownGlobals.LawbotBossMaxDamage:
            didTheyWin = 1
        self.battleThreeTimeInMin = globalClock.getFrameTime() - self.battleThreeTimeStarted
        self.battleThreeTimeInMin /= 60.0
        self.numToonsAtEnd = 0
        toonHps = []
        for toonId in self.involvedToons:
            toon = simbase.air.doId2do.get(toonId)
            if toon:
                self.numToonsAtEnd += 1
                toonHps.append(toon.hp)

        self.air.writeServerEvent('b3Info', self.doId, '%d|%.2f|%d|%d|%d|%d|%d|%d|%d|%d|%d|%d|%s|%s' % (didTheyWin,
         self.battleThreeTimeInMin,
         self.numToonsAtStart,
         self.numToonsAtEnd,
         self.numToonJurorsSeated,
         self.battleDifficulty,
         self.ammoCount,
         self.numGavels,
         self.numLawyers,
         self.toonupValue,
         self.numBonusStates,
         self.numAreaAttacks,
         toonHps,
         self.weightPerToon))

    def exitBattleThree(self):
        self.doBattleThreeInfo()
        self.stopAttacks()
        self.stopStrafes()
        taskName = self.uniqueName('CagedToonSaySomething')
        taskMgr.remove(taskName)
        self.__resetLawyers()
        self.__deleteBattleThreeObjects()

    def enterNearVictory(self):
        self.resetBattles()

    def exitNearVictory(self):
        pass

    def syncSpeedrunTimer(self):
        self.scaleTime = globalClock.getFrameTime()
        timeToSend = self.scaleTime - self.battleThreeTimeStarted
        self.d_updateTimer(timeToSend)

    def enterVictory(self):
        #Whisper out the time from the start of CJ until end of CJ
        self.syncSpeedrunTimer()
        self.ignoreToonDeaths()
        self.resetBattles()
        self.suitsKilled.append({'type': None,
         'level': 0,
         'track': self.dna.dept,
         'isSkelecog': 0,
         'isForeman': 0,
         'isVP': 1,
         'isCFO': 0,
         'isSupervisor': 0,
         'isVirtual': 0,
         'activeToons': self.involvedToons[:]})
        self.barrier = self.beginBarrier('Victory', self.involvedToons, 30, self.__doneVictory)
        return

    def __doneVictory(self, avIds):
        self.d_setBattleExperience()
        self.b_setState('Reward')
        BattleExperienceAI.assignRewards(self.involvedToons, self.toonSkillPtsGained, self.suitsKilled, ToontownGlobals.dept2cogHQ(self.dept), self.helpfulToons)
        numRewards = 6
        numOtherRewards = 2
        for toonId in self.involvedToons:
            toon = self.air.doId2do.get(toonId)
            if toon:
                bundleCount = toon.slotData.get('checks_per_boss', 4)
                bundle = [locations.ToontownLocationName.LAWBOT_PROOF_1.value,
                          locations.ToontownLocationName.LAWBOT_PROOF_2.value,
                          locations.ToontownLocationName.LAWBOT_PROOF_3.value,
                          locations.ToontownLocationName.LAWBOT_PROOF_4.value,
                          locations.ToontownLocationName.LAWBOT_PROOF_5.value]
                if bundleCount:
                    for checkNum in range(bundleCount):
                        toon.addCheckedLocation(ap_location_name_to_id(bundle[checkNum]))
                for reward in range(numRewards):
                    preferredDept = random.randrange(len(SuitDNA.suitDepts))
                    typeWeights = ['single'] * 70 + ['building'] * 27 + ['invasion'] * 3
                    preferredSummonType = random.choice(typeWeights)
                    self.giveCogSummonReward(toon, preferredDept, preferredSummonType)
                for reward in range(numOtherRewards):
                    randomSOS = random.choice(NPCToons.npcFriendsMinMaxStars(4, 5))
                    toon.attemptAddNPCFriend(randomSOS)
                    uniteType = random.choice([ResistanceChat.RESISTANCE_TOONUP, ResistanceChat.RESISTANCE_RESTOCK])
                    if uniteType == ResistanceChat.RESISTANCE_RESTOCK:
                        restockItems = ResistanceChat.getItems(uniteType)
                        uniteChoice = restockItems[random.randint(3, 6)]
                    else:
                        uniteChoice = random.choice(ResistanceChat.getItems(uniteType))
                    toon.addResistanceMessage(ResistanceChat.encodeId(uniteType, uniteChoice))
                toon.addPinkSlips(numOtherRewards)
                toon.b_promote(self.deptIndex)

    def giveCogSummonReward(self, toon, prefDeptIndex, prefSummonType):
        cogLevel = int(self.toonLevels / self.maxToonLevels * SuitDNA.suitsPerDept)
        cogLevel = min(cogLevel, SuitDNA.suitsPerDept - 1)
        deptIndex = prefDeptIndex
        summonType = prefSummonType
        hasSummon = toon.hasParticularCogSummons(prefDeptIndex, cogLevel, prefSummonType)
        if hasSummon:
            self.notify.debug('trying to find another reward')
            if not toon.hasParticularCogSummons(prefDeptIndex, cogLevel, 'single'):
                summonType = 'single'
            elif not toon.hasParticularCogSummons(prefDeptIndex, cogLevel, 'building'):
                summonType = 'building'
            elif not toon.hasParticularCogSummons(prefDeptIndex, cogLevel, 'invasion'):
                summonType = 'invasion'
            else:
                foundOne = False
                for curDeptIndex in range(len(SuitDNA.suitDepts)):
                    if not toon.hasParticularCogSummons(curDeptIndex, cogLevel, prefSummonType):
                        deptIndex = curDeptIndex
                        foundOne = True
                        break
                    elif not toon.hasParticularCogSummons(curDeptIndex, cogLevel, 'single'):
                        deptIndex = curDeptIndex
                        summonType = 'single'
                        foundOne = True
                        break
                    elif not toon.hasParticularCogSummons(curDeptIndex, cogLevel, 'building'):
                        deptIndex = curDeptIndex
                        summonType = 'building'
                        foundOne = True
                        break
                    elif not toon.hasParticularCogSummons(curDeptIndex, cogLevel, 'invasion'):
                        summonType = 'invasion'
                        deptIndex = curDeptIndex
                        foundOne = True
                        break

                possibleCogLevel = range(SuitDNA.suitsPerDept)
                possibleDeptIndex = range(len(SuitDNA.suitDepts))
                possibleSummonType = ['single', 'building', 'invasion']
                typeWeights = ['single'] * 70 + ['building'] * 27 + ['invasion'] * 3
                if not foundOne:
                    for i in range(5):
                        randomCogLevel = random.choice(possibleCogLevel)
                        randomSummonType = random.choice(typeWeights)
                        randomDeptIndex = random.choice(possibleDeptIndex)
                        if not toon.hasParticularCogSummons(randomDeptIndex, randomCogLevel, randomSummonType):
                            foundOne = True
                            cogLevel = randomCogLevel
                            summonType = randomSummonType
                            deptIndex = randomDeptIndex
                            break

                for curType in possibleSummonType:
                    if foundOne:
                        break
                    for curCogLevel in possibleCogLevel:
                        if foundOne:
                            break
                        for curDeptIndex in possibleDeptIndex:
                            if foundOne:
                                break
                            if not toon.hasParticularCogSummons(curDeptIndex, curCogLevel, curType):
                                foundOne = True
                                cogLevel = curCogLevel
                                summonType = curType
                                deptIndex = curDeptIndex

                if not foundOne:
                    cogLevel = None
                    summonType = None
                    deptIndex = None
        toon.assignNewCogSummons(cogLevel, summonType, deptIndex)
        return

    def exitVictory(self):
        self.takeAwayPies()

    def enterDefeat(self):
        super().enterDefeat()
        self.takeAwayPies()
        self.resetBattles()

    def exitDefeat(self):
        self.takeAwayPies()

    def enterFrolic(self):
        DistributedBossCogAI.DistributedBossCogAI.enterFrolic(self)
        self.b_setBossDamage(0, 0, 0)

    def setPieType(self):
        for toonId in self.involvedToons:
            toon = simbase.air.doId2do.get(toonId)
            if toon:
                toon.d_setPieType(ToontownBattleGlobals.MAX_TRACK_INDEX + 1)

    def takeAwayPies(self):
        for toonId in self.involvedToons:
            toon = simbase.air.doId2do.get(toonId)
            if toon:
                toon.b_setNumPies(0)

    def __recordHit(self):
        now = globalClock.getFrameTime()
        self.hitCount += 1
        if self.hitCount < self.limitHitCount or self.bossDamage < self.hitCountDamage:
            return

    def __resetLawyers(self):
        for suit in self.lawyers:
            suit.requestDelete()

        self.lawyers = []

    def __makeLawyers(self):
        self.__resetLawyers()
        lawCogChoices = ['b','dt', 'ac', 'bs', 'sd', 'le', 'bw']
        for i in range(self.numLawyers):
            suit = DistributedLawbotBossSuitAI.DistributedLawbotBossSuitAI(self.air, None)
            suit.dna = SuitDNA.SuitDNA()
            lawCog = random.choice(lawCogChoices)
            #if (i == 0): lawCog = 'le' #Cog 8
            #elif (i == 1): lawCog = 'sd' #Cog 7
            #elif (i == 2): lawCog = 'sd' #Cog 6
            #elif (i == 3): lawCog = 'dt' #Cog 5
            #elif (i == 4): lawCog = 'dt' #Cog 4
            #elif (i == 5): lawCog = 'bs' #Cog 3
            #elif (i == 6): lawCog = 'b' #Cog 2
            #elif (i == 7): lawCog = 'le' #Cog 1
            #elif (i == 8): lawCog = 'le' #Cog 9
            #elif (i == 9): lawCog = 'bw' #Cog 10
            #elif (i == 10): lawCog = 'le' #Cog 8m
            #elif (i == 11): lawCog = 'bs' #Cog 7m
            #elif (i == 12): lawCog = 'b' #Cog 6m
            #elif (i == 13): lawCog = 'dt' #Cog 5m
            #elif (i == 14): lawCog = 'bs' #Cog 4m
            #elif (i == 15): lawCog = 'sd' #Cog 3m
            #elif (i == 16): lawCog = 'dt' #Cog 2m
            #elif (i == 17): lawCog = 'bw' #Cog 1m
            #lif (i == 18): lawCog = 'le' #Cog 9m
            #elif (i == 19): lawCog = 'le' #Cog 10m
            #elif (i == 20): lawCog = 'le' #Cog 21
            #elif (i == 21): lawCog = 'le' #Cog 22
            suit.dna.newSuit(lawCog)
            suit.setPosHpr(*ToontownGlobals.LawbotBossLawyerPosHprs[i])
            suit.setBoss(self)
            suit.generateWithRequired(self.zoneId)
            self.lawyers.append(suit)

        self.__sendLawyerIds()
        return

    def hitChair(self, chairIndex, npcToonIndex):
        avId = self.air.getAvatarIdFromSender()
        if not self.validate(avId, avId in self.involvedToons, 'hitChair from unknown avatar'):
            return
        if not self.chairs:
            return
        if chairIndex < 0 or chairIndex >= len(self.chairs):
            self.notify.warning('invalid chairIndex = %d' % chairIndex)
            return
        if not self.state == 'BattleTwo':
            return
        self.chairs[chairIndex].b_setToonJurorIndex(npcToonIndex)
        self.chairs[chairIndex].requestToonJuror()

    def clearBonus(self, taskName):
        if self and hasattr(self, 'bonusState'):
            self.bonusState = False

    def startBonusState(self):
        self.notify.debug('startBonusState')
        self.bonusState = True
        self.numBonusStates += 1
        healingDone = 0
        for toonId in self.involvedToons:
            toon = self.air.doId2do.get(toonId)
            if toon and toon.hp > 0:
                hp = min(ToontownGlobals.LawbotBossBonusToonup, toon.maxHp - toon.hp)
                healingDone += hp
                self.healToon(toon, hp)

        # Calculate point handouts for people who helped stunned
        freq = {avId: 0 for avId in self.involvedToons}
        # Loop through the lawyers and add 1 for the toon that stunned it
        for lawyer in self.lawyers:
            toonThatStunned = lawyer.stunnedBy
            if toonThatStunned in freq:
                freq[toonThatStunned] += 1

        # Now with our frequency map, give a percentage of the points based on how many they had
        for avId in freq:
            percentageStunned = float(freq[avId]) / float(len(self.lawyers))
            pointBonus = int(math.ceil(percentageStunned * 25))
            healBonus = int(math.ceil(percentageStunned * healingDone))
            self.d_stunBonus(avId, pointBonus)
            self.d_avHealed(avId, healBonus)

        taskMgr.doMethodLater(ToontownGlobals.LawbotBossBonusDuration, self.clearBonus, self.uniqueName('clearBonus'))
        self.sendUpdate('enteredBonusState', [])
        
        #Whisper out the time from the start of CJ
        self.bonusTimeStarted = globalClock.getFrameTime()

    def areAllLawyersStunned(self):
        for lawyer in self.lawyers:
            if not lawyer.stunned:
                return False

        return True

    def checkForBonusState(self):
        if self.bonusState:
            return
        if not self.areAllLawyersStunned():
            return
        curTime = globalClock.getFrameTime()
        delta = curTime - self.bonusTimeStarted
        if ToontownGlobals.LawbotBossBonusWaitTime < delta:
            self.startBonusState()

    def toonEnteredCannon(self, toonId, cannonIndex):
        self.cannonIndexPerToon[toonId] = cannonIndex

    def numJurorsSeatedByCannon(self, cannonIndex):
        retVal = 0
        for chair in self.chairs:
            if chair.state == 'ToonJuror':
                if chair.toonJurorIndex == cannonIndex:
                    retVal += 1

        return retVal

    def calculateWeightPerToon(self):
        for toonId in self.involvedToons:
            defaultWeight = 1
            bonusWeight = 0
            cannonIndex = self.cannonIndexPerToon.get(toonId)
            if not cannonIndex == None:
                diffSettings = ToontownGlobals.LawbotBossDifficultySettings[self.battleDifficulty]
                if diffSettings[4]:
                    bonusWeight = self.numJurorsSeatedByCannon(cannonIndex) - diffSettings[5]
                    if bonusWeight < 0:
                        bonusWeight = 0
            newWeight = defaultWeight + bonusWeight
            self.weightPerToon[toonId] = newWeight
            self.notify.debug('toon %d has weight of %d' % (toonId, newWeight))

        return

    def b_setBattleDifficulty(self, batDiff):
        self.setBattleDifficulty(batDiff)
        self.d_setBattleDifficulty(batDiff)

    def setBattleDifficulty(self, batDiff):
        self.battleDifficulty = batDiff

    def d_setBattleDifficulty(self, batDiff):
        self.sendUpdate('setBattleDifficulty', [batDiff])

    def calcAndSetBattleDifficulty(self):
        self.toonLevels = self.getToonDifficulty()
        numDifficultyLevels = len(ToontownGlobals.LawbotBossDifficultySettings)
        battleDifficulty = int(self.toonLevels / self.maxToonLevels * numDifficultyLevels)
        if battleDifficulty >= numDifficultyLevels:
            battleDifficulty = numDifficultyLevels - 1
        self.b_setBattleDifficulty(battleDifficulty)

    # Given an attack code, return a death reason that corresponds with it.
    def getDeathReasonFromAttackCode(self, attackCode) -> DeathReason:

        return {
            ToontownGlobals.BossCogAreaAttack: DeathReason.CJ_JUMP,
            ToontownGlobals.BossCogSwatLeft: DeathReason.CJ_SWAT,
            ToontownGlobals.BossCogSwatRight: DeathReason.CJ_SWAT,
            ToontownGlobals.BossCogElectricFence: DeathReason.CJ_RUNOVER,

            ToontownGlobals.BossCogLawyerAttack: DeathReason.CJ_LAWYER,
            ToontownGlobals.BossCogGavelHandle: DeathReason.CJ_GAVEL_SMALL,
            ToontownGlobals.BossCogGavelStomp: DeathReason.CJ_GAVEL_BIG
        }.get(attackCode, DeathReason.CJ)

    def getDeathReasonFromBattle(self) -> DeathReason:
        return DeathReason.BATTLING_CJ

