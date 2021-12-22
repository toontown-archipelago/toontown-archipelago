from panda3d.core import *
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownGlobals
from toontown.coghq import DistributedCashbotBossCraneAI
from toontown.coghq import DistributedCashbotBossSideCraneAI
from toontown.coghq import DistributedCashbotBossSafeAI
from toontown.suit import DistributedCashbotBossGoonAI
from toontown.coghq import DistributedCashbotBossTreasureAI
from toontown.battle import BattleExperienceAI
from toontown.chat import ResistanceChat
from toontown.toon import DistributedToonAI
from direct.fsm import FSM
import DistributedBossCogAI
import SuitDNA
import random
import math

class DistributedCashbotBossAI(DistributedBossCogAI.DistributedBossCogAI, FSM.FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedCashbotBossAI')
    maxGoons = 8

    def __init__(self, air):
        DistributedBossCogAI.DistributedBossCogAI.__init__(self, air, 'm')
        FSM.FSM.__init__(self, 'DistributedCashbotBossAI')
        self.cranes = None
        self.safes = None
        self.goons = None
        self.treasures = {}
        self.grabbingTreasures = {}
        self.recycledTreasures = []
        self.healAmount = 0
        self.rewardId = ResistanceChat.getRandomId()
        self.rewardedToons = []
        self.scene = NodePath('scene')
        self.reparentTo(self.scene)
        cn = CollisionNode('walls')
        cs = CollisionSphere(0, 0, 0, 13)
        cn.addSolid(cs)
        cs = CollisionInvSphere(0, 0, 0, 42)
        cn.addSolid(cs)
        self.attachNewNode(cn)
        self.heldObject = None
        self.waitingForHelmet = 0
        self.avatarHelmets = {}
        self.knockoutDamage = ToontownGlobals.CashbotBossKnockoutDamage
        self.bossMaxDamage = ToontownGlobals.CashbotBossMaxDamage
        self.wantSafeRushPractice = False
        self.wantCustomCraneSpawns = False
        self.customSpawnPositions = {}
        self.goonMinStrength = 10
        self.goonMaxStrength = 43
        self.goonMinScale = 0.8
        self.goonMaxScale = 2.6
        self.toonDamagesDict = {}
        self.toonStunsDict = {}
        self.toonGoonStompsDict = {}
        self.participantPoints = {}
        self.safesPutOn = {}
        self.safesPutOff = {}
        self.perfectImpactThrows = {}
        self.wantAimPractice = False
        self.safesWanted = 5
        self.want4ManPractice = True
        self.wantMovementModification = True
        self.wantOpeningModifications = False
        return

    def generate(self):
        DistributedBossCogAI.DistributedBossCogAI.generate(self)
        if __dev__:
            self.scene.reparentTo(self.getRender())

    def getHoodId(self):
        return ToontownGlobals.CashbotHQ

    def formatReward(self):
        return str(self.rewardId)

    def makeBattleOneBattles(self):
        self.postBattleState = 'PrepareBattleThree'
        self.initializeBattles(1, ToontownGlobals.CashbotBossBattleOnePosHpr)

    def generateSuits(self, battleNumber):
        cogs = self.invokeSuitPlanner(11, 0)
        skelecogs = self.invokeSuitPlanner(12, 1)
        activeSuits = cogs['activeSuits'] + skelecogs['activeSuits']
        reserveSuits = cogs['reserveSuits'] + skelecogs['reserveSuits']
        random.shuffle(activeSuits)
        while len(activeSuits) > 4:
            suit = activeSuits.pop()
            reserveSuits.append((suit, 100))

        def compareJoinChance(a, b):
            return cmp(a[1], b[1])

        reserveSuits.sort(compareJoinChance)
        return {'activeSuits': activeSuits,
         'reserveSuits': reserveSuits}

    def removeToon(self, avId):
        if self.cranes != None:
            for crane in self.cranes:
                crane.removeToon(avId)

        if self.safes != None:
            for safe in self.safes:
                safe.removeToon(avId)

        if self.goons != None:
            for goon in self.goons:
                goon.removeToon(avId)

        DistributedBossCogAI.DistributedBossCogAI.removeToon(self, avId)
        return

    def __makeBattleThreeObjects(self):
        if self.cranes == None:
            self.cranes = []
            for index in xrange(len(ToontownGlobals.CashbotBossCranePosHprs)):
                if index <= 3:
                    crane = DistributedCashbotBossCraneAI.DistributedCashbotBossCraneAI(self.air, self, index)
                else:
                    crane = DistributedCashbotBossSideCraneAI.DistributedCashbotBossSideCraneAI(self.air, self, index)
                crane.generateWithRequired(self.zoneId)
                self.cranes.append(crane)

        if self.safes == None:
            self.safes = []
            for index in xrange(len(ToontownGlobals.CashbotBossSafePosHprs)):
                safe = DistributedCashbotBossSafeAI.DistributedCashbotBossSafeAI(self.air, self, index)
                safe.generateWithRequired(self.zoneId)
                self.safes.append(safe)

        if self.goons == None:
            self.goons = []
        return

    def __resetBattleThreeObjects(self):
        if self.cranes != None:
            for crane in self.cranes:
                crane.request('Free')

        if self.safes != None:
            for safe in self.safes:
                safe.request('Initial')

        return

    def __deleteBattleThreeObjects(self):
        if self.cranes != None:
            for crane in self.cranes:
                crane.request('Off')
                crane.requestDelete()

            self.cranes = None
        if self.safes != None:
            for safe in self.safes:
                safe.request('Off')
                safe.requestDelete()

            self.safes = None
        if self.goons != None:
            for goon in self.goons:
                goon.request('Off')
                goon.requestDelete()

            self.goons = None
        return

    def doNextAttack(self, task):
        self.__doDirectedAttack()
        if self.heldObject == None and not self.waitingForHelmet:
            self.waitForNextHelmet()
        return

    def __doDirectedAttack(self):
        if self.toonsToAttack:
            toonId = self.toonsToAttack.pop(0)
            while toonId not in self.involvedToons:
                if not self.toonsToAttack:
                    self.b_setAttackCode(ToontownGlobals.BossCogNoAttack)
                    return
                toonId = self.toonsToAttack.pop(0)

            self.toonsToAttack.append(toonId)
            self.b_setAttackCode(ToontownGlobals.BossCogSlowDirectedAttack, toonId)

    def reprieveToon(self, avId):
        if avId in self.toonsToAttack:
            i = self.toonsToAttack.index(avId)
            del self.toonsToAttack[i]
            self.toonsToAttack.append(avId)

    def makeTreasure(self, goon):
        if self.state != 'BattleThree':
            return
        avId = self.air.getAvatarIdFromSender()
        pos = goon.getPos(self)
        v = Vec3(pos[0], pos[1], 0.0)
        if not v.normalize():
            v = Vec3(1, 0, 0)
        v = v * 27
        angle = random.uniform(0.0, 2.0 * math.pi)
        radius = 10
        dx = radius * math.cos(angle)
        dy = radius * math.sin(angle)
        fpos = self.scene.getRelativePoint(self, Point3(v[0] + dx, v[1] + dy, 0))
        if goon.strength <= 10:
            style = random.choice([ToontownGlobals.ToontownCentral, ToontownGlobals.DonaldsDock, ToontownGlobals.DaisyGardens, ToontownGlobals.MinniesMelodyland, ToontownGlobals.TheBrrrgh, ToontownGlobals.DonaldsDreamland])
            healAmount = 4
        elif goon.strength <= 15:
            style = random.choice([ToontownGlobals.DonaldsDock, ToontownGlobals.DaisyGardens, ToontownGlobals.MinniesMelodyland])
            healAmount = 10
        else:
            style = random.choice([ToontownGlobals.TheBrrrgh, ToontownGlobals.DonaldsDreamland])
            healAmount = 12
        if self.recycledTreasures:
            treasure = self.recycledTreasures.pop(0)
            treasure.d_setGrab(0)
            treasure.b_setGoonId(goon.doId)
            treasure.b_setStyle(style)
            treasure.b_setPosition(pos[0], pos[1], 0)
            treasure.b_setFinalPosition(fpos[0], fpos[1], 0)
        else:
            treasure = DistributedCashbotBossTreasureAI.DistributedCashbotBossTreasureAI(self.air, self, goon, style, fpos[0], fpos[1], 0)
            treasure.generateWithRequired(self.zoneId)
        treasure.healAmount = healAmount
        self.treasures[treasure.doId] = treasure

    def grabAttempt(self, avId, treasureId):
        av = self.air.doId2do.get(avId)
        if not av:
            return
        treasure = self.treasures.get(treasureId)
        if treasure:
            if treasure.validAvatar(av):
                del self.treasures[treasureId]
                treasure.d_setGrab(avId)
                self.grabbingTreasures[treasureId] = treasure
                taskMgr.doMethodLater(5, self.__recycleTreasure, treasure.uniqueName('recycleTreasure'), extraArgs=[treasure])
            else:
                treasure.d_setReject()

    def __recycleTreasure(self, treasure):
        if treasure.doId in self.grabbingTreasures:
            del self.grabbingTreasures[treasure.doId]
            self.recycledTreasures.append(treasure)

    def deleteAllTreasures(self):
        for treasure in self.treasures.values():
            treasure.requestDelete()

        self.treasures = {}
        for treasure in self.grabbingTreasures.values():
            taskMgr.remove(treasure.uniqueName('recycleTreasure'))
            treasure.requestDelete()

        self.grabbingTreasures = {}
        for treasure in self.recycledTreasures:
            treasure.requestDelete()

        self.recycledTreasures = []

    def getMaxGoons(self):
        t = self.getBattleThreeTime()
        if t <= 1.0:
            return self.maxGoons
        elif t <= 1.1:
            return self.maxGoons + 1
        elif t <= 1.2:
            return self.maxGoons + 2
        elif t <= 1.3:
            return self.maxGoons + 3
        elif t <= 1.4:
            return self.maxGoons + 4
        else:
            return self.maxGoons + 8

    def makeGoon(self, side = None):
        self.goonMovementTime = globalClock.getFrameTime()
        if side == None:
            if not self.wantOpeningModifications:
                side = random.choice(['EmergeA', 'EmergeB'])
            else:
                for t in self.involvedToons:
                    avId = t
                toon = self.air.doId2do.get(avId)
                pos = toon.getPos()[1]
                if pos < -315:
                    side = 'EmergeB'
                else:
                    side = 'EmergeA'
        goon = DistributedCashbotBossGoonAI.DistributedCashbotBossGoonAI(self.air, self)
        if goon != None:
            if len(self.goons) >= self.getMaxGoons():
                return
            goon.generateWithRequired(self.zoneId)
            self.goons.append(goon)
        if self.getBattleThreeTime() > 1.0:
            goon.STUN_TIME = 4
            goon.b_setupGoon(velocity=8, hFov=90, attackRadius=20, strength=self.goonMaxStrength, scale=1.8)
        else:
            goon.STUN_TIME = self.progressValue(30, 8)
            goon.b_setupGoon(velocity=self.progressRandomValue(3, 7), hFov=self.progressRandomValue(70, 80), attackRadius=self.progressRandomValue(6, 15), strength=int(self.progressRandomValue(self.goonMinStrength, self.goonMaxStrength)), scale=self.progressRandomValue(self.goonMinScale, self.goonMaxScale, noRandom=False))
        goon.request(side)
        return

    def __chooseOldGoon(self):
        for goon in self.goons:
            if goon.state == 'Off':
                return goon

    def waitForNextGoon(self, delayTime):
        currState = self.getCurrentOrNextState()
        if currState == 'BattleThree':
            taskName = self.uniqueName('NextGoon')
            taskMgr.remove(taskName)
            taskMgr.doMethodLater(delayTime, self.doNextGoon, taskName)

    def stopGoons(self):
        taskName = self.uniqueName('NextGoon')
        taskMgr.remove(taskName)

    def doNextGoon(self, task):
        if self.attackCode != ToontownGlobals.BossCogDizzy:
            self.makeGoon()
        delayTime = self.progressValue(10, 2)
        self.waitForNextGoon(delayTime)

    def waitForNextHelmet(self):
        currState = self.getCurrentOrNextState()
        if currState == 'BattleThree':
            taskName = self.uniqueName('NextHelmet')
            taskMgr.remove(taskName)
            delayTime = self.progressValue(45, 15)
            taskMgr.doMethodLater(delayTime, self.__donHelmet, taskName)
            self.waitingForHelmet = 1

    def __donHelmet(self, task):
        self.waitingForHelmet = 0
        if self.heldObject == None:
            safe = self.safes[0]
            safe.request('Grabbed', self.doId, self.doId)
            self.heldObject = safe
        return

    def stopHelmets(self):
        self.waitingForHelmet = 0
        taskName = self.uniqueName('NextHelmet')
        taskMgr.remove(taskName)

    def acceptHelmetFrom(self, avId):
        now = globalClock.getFrameTime()
        then = self.avatarHelmets.get(avId, None)
        if then == None or now - then > 300:
            self.avatarHelmets[avId] = now
            return 1
        return 1

    def magicWordHit(self, damage, avId):
        if self.heldObject:
            self.heldObject.demand('Dropped', avId, self.doId)
            self.heldObject.avoidHelmet = 1
            self.heldObject = None
            self.waitForNextHelmet()
        else:
            self.recordHit(damage)
        return

    def magicWordReset(self):
        if self.state == 'BattleThree':
            self.__resetBattleThreeObjects()

    def magicWordResetGoons(self):
        if self.state == 'BattleThree':
            if self.goons != None:
                for goon in self.goons:
                    goon.request('Off')
                    goon.requestDelete()

                self.goons = None
            self.__makeBattleThreeObjects()
        return

    def recordHit(self, damage, impact=0, craneId=-1):
        avId = self.air.getAvatarIdFromSender()
        crane = simbase.air.doId2do.get(craneId)
        if not self.validate(avId, avId in self.involvedToons, 'recordHit from unknown avatar'):
            return
        if self.state != 'BattleThree':
            return
        self.b_setBossDamage(self.bossDamage + damage)
        if impact == 1.0:
            self.d_updateMaxImpactHits(avId)
        if avId in self.toonDamagesDict:
            self.toonDamagesDict[avId] += damage
        else:
            self.toonDamagesDict[avId] = damage
        self.d_updateDamageDealt(avId, damage)
        if self.wantSafeRushPractice:
            self.knockoutDamage = 2
        else:
            self.knockoutDamage = ToontownGlobals.CashbotBossKnockoutDamage
        if self.bossDamage >= self.bossMaxDamage:
            self.b_setState('Victory')
        elif self.attackCode != ToontownGlobals.BossCogDizzy:
            if crane:
                if damage >= self.knockoutDamage:
                    self.b_setAttackCode(ToontownGlobals.BossCogDizzy)
                    
                    self.d_updateStunCount(avId)
                    if avId in self.toonStunsDict:
                        self.toonStunsDict[avId] += 20
                    else:
                        self.toonStunsDict[avId] = 20

                    self.stopHelmets()

                    #Whisper out the time from the start of CFO
                    #self.stunTime = globalClock.getFrameTime()
                    #for doId, do in simbase.air.doId2do.items():
                        #if str(doId)[0] != str(simbase.air.districtId)[0]:
                            #do.d_setSystemMessage(0, "CFO Stunned From Start: {0:.3f}s".format(self.stunTime - self.battleThreeTimeStarted))
                            
                            
                elif crane.getIndex() > 3 and (impact >= 0.8 or damage >= self.knockoutDamage):
                    self.b_setAttackCode(ToontownGlobals.BossCogDizzy)
                    self.d_updateStunCount(avId)
                    if avId in self.toonStunsDict:
                        self.toonStunsDict[avId] += 20
                    else:
                        self.toonStunsDict[avId] = 20
                    self.stopHelmets()
                else:
                    self.b_setAttackCode(ToontownGlobals.BossCogNoAttack)
                    self.stopHelmets()
                    self.waitForNextHelmet()

    def b_setBossDamage(self, bossDamage):
        self.d_setBossDamage(bossDamage)
        self.setBossDamage(bossDamage)

    def setBossDamage(self, bossDamage):
        self.reportToonHealth()
        self.bossDamage = bossDamage

    def d_setBossDamage(self, bossDamage):
        self.sendUpdate('setBossDamage', [bossDamage])
        
    def d_updateDamageDealt(self, avId, damageDealt):
        self.sendUpdate('updateDamageDealt', [avId, damageDealt])
		
    def d_updateStunCount(self, avId):
        self.sendUpdate('updateStunCount', [avId])
		
    def d_updateGoonsStomped(self, avId):
        self.sendUpdate('updateGoonsStomped', [avId])

    # call with 10 when we take a safe off, -20 when we put a safe on
    def d_updateSafePoints(self, avId, amount):
        self.sendUpdate('updateSafePoints', [avId, amount])

    def d_updateMaxImpactHits(self, avId):
        self.sendUpdate('updateMaxImpactHits', [avId])

    def d_setCraneSpawn(self, want, spawn, toonId):
        self.sendUpdate('setCraneSpawn', [want, spawn, toonId])

    def d_setRewardId(self, rewardId):
        self.sendUpdate('setRewardId', [rewardId])

    def applyReward(self):
        avId = self.air.getAvatarIdFromSender()
        if avId in self.involvedToons and avId not in self.rewardedToons:
            self.rewardedToons.append(avId)
            toon = self.air.doId2do.get(avId)
            if toon:
                toon.doResistanceEffect(self.rewardId)

    def enterOff(self):
        DistributedBossCogAI.DistributedBossCogAI.enterOff(self)
        self.rewardedToons = []

    def exitOff(self):
        DistributedBossCogAI.DistributedBossCogAI.exitOff(self)

    def enterIntroduction(self):
        DistributedBossCogAI.DistributedBossCogAI.enterIntroduction(self)
        self.__makeBattleThreeObjects()
        self.__resetBattleThreeObjects()

    def exitIntroduction(self):
        DistributedBossCogAI.DistributedBossCogAI.exitIntroduction(self)
        self.__deleteBattleThreeObjects()

    def enterPrepareBattleThree(self):
        self.resetBattles()
        self.__makeBattleThreeObjects()
        self.__resetBattleThreeObjects()
        self.barrier = self.beginBarrier('PrepareBattleThree', self.involvedToons, 55, self.__donePrepareBattleThree)

    def __donePrepareBattleThree(self, avIds):
        self.b_setState('BattleThree')

    def exitPrepareBattleThree(self):
        if self.newState != 'BattleThree':
            self.__deleteBattleThreeObjects()
        self.ignoreBarrier(self.barrier)

    def enterBattleThree(self):
        if self.attackCode == ToontownGlobals.BossCogDizzy or self.attackCode == ToontownGlobals.BossCogDizzyNow:
            self.b_setAttackCode(ToontownGlobals.BossCogNoAttack)
        self.setPosHpr(*ToontownGlobals.CashbotBossBattleThreePosHpr)
        self.__makeBattleThreeObjects()
        self.__resetBattleThreeObjects()
        self.reportToonHealth()
        self.toonsToAttack = self.involvedToons[:]
        random.shuffle(self.toonsToAttack)
        self.b_setBossDamage(0)
        self.battleThreeStart = globalClock.getFrameTime()
        self.resetBattles()
        self.waitForNextAttack(15)
        self.waitForNextHelmet()
        self.makeGoon(side='EmergeA')
        self.makeGoon(side='EmergeB')
        taskName = self.uniqueName('NextGoon')
        taskMgr.remove(taskName)
        taskMgr.doMethodLater(2, self.__doInitialGoons, taskName)
        self.battleThreeTimeStarted = globalClock.getFrameTime()
        self.toonDamagesDict = {}
        self.toonStunsDict = {}
        self.toonGoonStompsDict = {}
        self.participantPoints = {}
        self.safesPutOn = {}
        self.safesPutOff = {}
        self.perfectImpactThrows = {}
        for avId in self.involvedToons:
            if avId in self.air.doId2do:
                av = self.air.doId2do[avId]
                av.b_setHp(av.getMaxHp())

    def __doInitialGoons(self, task):
        self.makeGoon(side='EmergeA')
        self.makeGoon(side='EmergeB')
        self.waitForNextGoon(10)

    def exitBattleThree(self):
        helmetName = self.uniqueName('helmet')
        taskMgr.remove(helmetName)
        if self.newState != 'Victory':
            self.__deleteBattleThreeObjects()
        self.deleteAllTreasures()
        self.stopAttacks()
        self.stopGoons()
        self.stopHelmets()
        self.heldObject = None
        return

    def enterVictory(self):
        #Whisper out the time from the start of CFO until end of CFO
        self.craneTime = globalClock.getFrameTime()
        actualTime = self.craneTime - self.battleThreeTimeStarted
        resultsString = ""
        for avId in self.involvedToons:
            avPoints = 0
            av = self.air.doId2do.get(avId)
            if (avId in self.toonDamagesDict):
                avPoints += self.toonDamagesDict[avId]
            if (avId in self.toonStunsDict):
                avPoints += self.toonStunsDict[avId]
            if (avId in self.safesPutOff):
                avPoints += self.safesPutOff[avId]
            if (avId in self.safesPutOn):
                avPoints += self.safesPutOn[avId]
            if (avId in self.perfectImpactThrows):
                avPoints += self.perfectImpactThrows[avId]
            self.participantPoints[av.getName()] = avPoints
            resultsString += ("%s: %s\n" % (av.getName(), avPoints))
        resultsString = resultsString[:-1]
        for doId, do in simbase.air.doId2do.items():
            if str(doId)[0] != str(simbase.air.districtId)[0]:
                if isinstance(do, DistributedToonAI.DistributedToonAI):
                    #do.d_setSystemMessage(0, "Crane Round Ended In {0:.5f}s".format(actualTime))
                    do.d_setSystemMessage(0, resultsString)
        self.d_updateTimer(actualTime)
        self.resetBattles()
        self.suitsKilled.append({'type': None,
         'level': None,
         'track': self.dna.dept,
         'isSkelecog': 0,
         'isForeman': 0,
         'isVP': 0,
         'isCFO': 1,
         'isSupervisor': 0,
         'isVirtual': 0,
         'activeToons': self.involvedToons[:]})
        self.barrier = self.beginBarrier('Victory', self.involvedToons, 30, self.__doneVictory)
        return

    def d_updateTimer(self, time):
        self.sendUpdate('updateTimer', [time])

    def __doneVictory(self, avIds):
        self.d_setBattleExperience()
        self.b_setState('Reward')
        BattleExperienceAI.assignRewards(self.involvedToons, self.toonSkillPtsGained, self.suitsKilled, ToontownGlobals.dept2cogHQ(self.dept), self.helpfulToons)
        for toonId in self.involvedToons:
            toon = self.air.doId2do.get(toonId)
            if toon:
                toon.addResistanceMessage(self.rewardId)
                toon.b_promote(self.deptIndex)

    def exitVictory(self):
        self.__deleteBattleThreeObjects()

    def enterEpilogue(self):
        DistributedBossCogAI.DistributedBossCogAI.enterEpilogue(self)
        self.d_setRewardId(self.rewardId)
        
    def checkNearby(self, task=None):
        # Prevent helmets, stun CFO, destroy goons
        self.stopHelmets()
        self.b_setAttackCode(ToontownGlobals.BossCogDizzy)
        for goon in self.goons:
            goon.request('Off')
            goon.requestDelete()

        nearbyDistance = 22
    
        # Get the toon's position
        toon = self.air.doId2do.get(self.involvedToons[0])
        toonX = toon.getPos().x
        toonY = toon.getPos().y
        
        # Count nearby safes
        nearbySafes = []
        farSafes = []
        farDistances = []
        for safe in self.safes:
            # Safe on his head doesn't count and is not a valid target to move
            if self.heldObject is safe:
                continue
        
            safeX = safe.getPos().x
            safeY = safe.getPos().y

            distance = math.sqrt((toonX - safeX) ** 2 + (toonY - safeY) ** 2)
            if distance <= nearbyDistance:
                nearbySafes.append(safe)
            else:
                farDistances.append(distance)
                farSafes.append(safe)

        # Sort the possible safes by their distance away from us
        farSafes = [x for y, x in sorted(zip(farDistances, farSafes), reverse=True)]

        # If there's not enough nearby safes, relocate far ones
        if len(nearbySafes) < self.safesWanted:
            self.relocateSafes(farSafes, self.safesWanted - len(nearbySafes), toonX, toonY)
    
        # Schedule this to be done again in 1s unless the user stops it
        taskName = self.uniqueName('CheckNearbySafes')
        taskMgr.doMethodLater(4, self.checkNearby, taskName)

    def stopCheckNearby(self):
        taskName = self.uniqueName('CheckNearbySafes')
        taskMgr.remove(taskName)

    def relocateSafes(self, farSafes, numRelocate, toonX, toonY):
        for safe in farSafes[:numRelocate]:
            randomDistance = 22 * random.random()
            randomAngle = 2 * math.pi * random.random()
            newX = toonX + randomDistance * math.cos(randomAngle)
            newY = toonY + randomDistance * math.sin(randomAngle)
            while not self.isLocationInBounds(newX, newY):
                randomDistance = 22 * random.random()
                randomAngle = 2 * math.pi * random.random()
                newX = toonX + randomDistance * math.cos(randomAngle)
                newY = toonY + randomDistance * math.sin(randomAngle)

            safe.move(newX, newY, 0, 360 * random.random())

    # Probably a better way to do this but o well
    # Checking each line of the octogon to see if the location is outside
    def isLocationInBounds(self, x, y):
        if x > 165.7:
            return False
        if x < 77.1:
            return False
        if y > -274.1:
            return False
        if y < -359.1:
            return False
        
        if y - 0.936455 * x > -374.901:
            return False
        if y + 0.973856 * x < -254.118:
            return False
        if y - 1.0283 * x < -496.79:
            return False
        if y + 0.884984 * x > -155.935:
            return False

        return True
