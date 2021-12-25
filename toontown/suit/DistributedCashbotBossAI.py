from panda3d.core import *
from direct.directnotify import DirectNotifyGlobal
from direct.showbase.PythonUtil import clamp
from toontown.coghq.CashbotBossComboTracker import CashbotBossComboTracker
from toontown.toonbase import ToontownGlobals
from toontown.coghq import DistributedCashbotBossCraneAI
from toontown.coghq import DistributedCashbotBossSideCraneAI
from toontown.coghq import DistributedCashbotBossSafeAI
from toontown.suit import DistributedCashbotBossGoonAI
from toontown.coghq import DistributedCashbotBossTreasureAI
from toontown.coghq import CraneLeagueGlobals
from toontown.battle import BattleExperienceAI
from toontown.chat import ResistanceChat
from toontown.toon import DistributedToonAI
from direct.fsm import FSM
import DistributedBossCogAI
import random
import math

class DistributedCashbotBossAI(DistributedBossCogAI.DistributedBossCogAI, FSM.FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedCashbotBossAI')

    def __init__(self, air):
        DistributedBossCogAI.DistributedBossCogAI.__init__(self, air, 'm')
        FSM.FSM.__init__(self, 'DistributedCashbotBossAI')
        self.cranes = None
        self.safes = None
        self.goons = None
        self.treasures = {}
        self.grabbingTreasures = {}
        self.recycledTreasures = []
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
        self.bossMaxDamage = CraneLeagueGlobals.CFO_MAX_HP
        self.wantSafeRushPractice = False
        self.wantCustomCraneSpawns = False
        self.customSpawnPositions = {}
        self.goonMinStrength = CraneLeagueGlobals.MIN_GOON_DAMAGE
        self.goonMaxStrength = CraneLeagueGlobals.MAX_GOON_DAMAGE
        self.goonMinScale = 0.8
        self.goonMaxScale = 2.6
        self.wantAimPractice = False
        self.safesWanted = 5
        self.want4ManPractice = True
        self.wantMovementModification = True
        self.wantOpeningModifications = False
        self.comboTrackers = {}  # Maps avId -> CashbotBossComboTracker instance
        return

    def generate(self):
        DistributedBossCogAI.DistributedBossCogAI.generate(self)
        if __dev__:
            self.scene.reparentTo(self.getRender())

    def getHoodId(self):
        return ToontownGlobals.CashbotHQ

    def formatReward(self):
        return 'No rewards here :)'

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

        # Check if we ran out of targets, if so reset the list back to everyone involved
        if len(self.toonsToAttack) <= 0:
            self.toonsToAttack = self.involvedToons[:]
            # Shuffle the toons if we want random gear throws
            if CraneLeagueGlobals.RANDOM_GEAR_THROW_ORDER:
                random.shuffle(self.toonsToAttack)
            # remove people who are dead or gone
            for id in self.toonsToAttack[:]:
                toon = self.air.doId2do.get(id)
                if not toon or toon.getHp() <= 0:
                    self.toonsToAttack.remove(id)

        # are there no valid targets even after resetting? i.e. is everyone sad
        if len(self.toonsToAttack) <= 0:
            self.b_setAttackCode(ToontownGlobals.BossCogNoAttack)
            return

        # pop toon off list and set as target
        toonToAttack = self.toonsToAttack.pop(0)
        # is toon here and alive? if not skip over and try the next toon
        toon = self.air.doId2do.get(toonToAttack)
        if not toon or toon.getHp() <= 0:
            return self.__doDirectedAttack()  # next toon

        # we have a toon to attack
        self.b_setAttackCode(ToontownGlobals.BossCogSlowDirectedAttack, toonToAttack)


    def getDamageMultiplier(self):
        return int(self.progressValue(1, 4))  # Mult of 1-3 depending on how far we are in the battle

    def zapToon(self, x, y, z, h, p, r, bpx, bpy, attackCode, timestamp):

        avId = self.air.getAvatarIdFromSender()
        if not self.validate(avId, avId in self.involvedToons, 'zapToon from unknown avatar'):
            return

        toon = simbase.air.doId2do.get(avId)
        if not toon:
            return

        self.d_showZapToon(avId, x, y, z, h, p, r, attackCode, timestamp)

        damage = CraneLeagueGlobals.CFO_ATTACKS_BASE_DAMAGE.get(attackCode)
        if damage == None:
            self.notify.warning('No damage listed for attack code %s' % attackCode)
            damage = 5
            raise KeyError('No damage listed for attack code %s' % attackCode)  # temp

        damage *= self.getDamageMultiplier()
        # Clamp the damage to make sure it at least does 1
        damage = max(int(damage), 1)

        self.damageToon(toon, damage)
        currState = self.getCurrentOrNextState()

        if attackCode == ToontownGlobals.BossCogElectricFence and (currState == 'RollToBattleTwo' or currState == 'BattleThree'):
            if bpy < 0 and abs(bpx / bpy) > 0.5:
                if bpx < 0:
                    self.b_setAttackCode(ToontownGlobals.BossCogSwatRight)
                else:
                    self.b_setAttackCode(ToontownGlobals.BossCogSwatLeft)

    def makeTreasure(self, goon):

        if self.state != 'BattleThree':
            return

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

        # Find an index based on the goon strength we should use
        treasureHealIndex = 1.0*(goon.strength-CraneLeagueGlobals.MIN_GOON_DAMAGE) / (CraneLeagueGlobals.MAX_GOON_DAMAGE-CraneLeagueGlobals.MIN_GOON_DAMAGE)
        treasureHealIndex *= len(CraneLeagueGlobals.GOON_HEALS)
        treasureHealIndex = int(clamp(treasureHealIndex, 0, len(CraneLeagueGlobals.GOON_HEALS)-1))
        healAmount = CraneLeagueGlobals.GOON_HEALS[treasureHealIndex]
        availStyles = CraneLeagueGlobals.TREASURE_STYLES[treasureHealIndex]
        style = random.choice(availStyles)

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
        return self.progressValue(CraneLeagueGlobals.MAX_GOON_AMOUNT_START, CraneLeagueGlobals.MAX_GOON_AMOUNT_END)

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
        return True

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
        self.d_updateDamageDealt(avId, damage)

        self.comboTrackers[avId].incrementCombo(damage*CraneLeagueGlobals.COMBO_DAMAGE_PERCENTAGE)

        if self.bossDamage >= self.bossMaxDamage:
            self.b_setState('Victory')
            return

        if self.attackCode == ToontownGlobals.BossCogDizzy or not crane:
            return

        self.stopHelmets()

        if damage >= CraneLeagueGlobals.CFO_STUN_THRESHOLD or (crane.getIndex() > 3 and impact >= CraneLeagueGlobals.SIDECRANE_IMPACT_STUN_THRESHOLD):
            self.b_setAttackCode(ToontownGlobals.BossCogDizzy)
            self.d_updateStunCount(avId)
        else:
            self.b_setAttackCode(ToontownGlobals.BossCogNoAttack)
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
        pass

    def enterOff(self):
        DistributedBossCogAI.DistributedBossCogAI.enterOff(self)

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
        if CraneLeagueGlobals.RANDOM_GEAR_THROW_ORDER:
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

        self.oldMaxLaffs = {}

        taskMgr.remove(self.uniqueName('failedCraneRound'))

        for comboTracker in self.comboTrackers.values():
            comboTracker.cleanup()

        # heal all toons and setup a combo tracker for them
        for avId in self.involvedToons:
            if avId in self.air.doId2do:
                self.comboTrackers[avId] = CashbotBossComboTracker(self, avId)
                av = self.air.doId2do[avId]

                if CraneLeagueGlobals.FORCE_MAX_LAFF:
                    self.oldMaxLaffs[avId] = av.getMaxHp()
                    av.b_setMaxHp(CraneLeagueGlobals.FORCE_MAX_LAFF_AMOUNT)

                if CraneLeagueGlobals.HEAL_TOONS_ON_START:
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

        # Restore old max HPs
        for avId in self.involvedToons:
            av = self.air.doId2do.get(avId)
            if av and avId in self.oldMaxLaffs:
                av.b_setMaxHp(self.oldMaxLaffs[avId])

        craneTime = globalClock.getFrameTime()
        actualTime = craneTime - self.battleThreeTimeStarted
        self.d_updateTimer(actualTime)
        self.resetBattles()
        self.barrier = self.beginBarrier('Victory', self.involvedToons, 30, self.__doneVictory)
        return

    def d_updateTimer(self, time):
        self.sendUpdate('updateTimer', [time])

    def __doneVictory(self, avIds):
        for comboTracker in self.comboTrackers.values():
            comboTracker.cleanup()
        self.d_setBattleExperience()
        self.b_setState('Reward')
        # BattleExperienceAI.assignRewards(self.involvedToons, self.toonSkillPtsGained, self.suitsKilled, ToontownGlobals.dept2cogHQ(self.dept), self.helpfulToons)

    def exitVictory(self):
        self.__deleteBattleThreeObjects()

    def enterEpilogue(self):
        DistributedBossCogAI.DistributedBossCogAI.enterEpilogue(self)

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

    def __restartCraneRoundTask(self, task):
        self.exitIntroduction()
        self.b_setState('PrepareBattleThree')
        self.b_setState('BattleThree')

    def toonDied(self, toon):
        DistributedBossCogAI.DistributedBossCogAI.toonDied(self, toon)

        # have all toons involved died?
        aliveToons = 0
        for toonId in self.involvedToons:
            toon = self.air.doId2do.get(toonId)
            if toon and toon.getHp() > 0:
                aliveToons += 1

        # Restart the crane round if toons are dead and we want to restart
        if CraneLeagueGlobals.RESTART_CRANE_ROUND_ON_FAIL and not aliveToons:
            taskMgr.doMethodLater(10.0, self.__restartCraneRoundTask, self.uniqueName('failedCraneRound'))
            self.sendUpdate('announceCraneRestart', [])



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

    def d_updateCombo(self, avId, comboLength):
        self.sendUpdate('updateCombo', [avId, comboLength])

    def d_awardCombo(self, avId, comboLength, amount):
        self.sendUpdate('awardCombo', [avId, comboLength, amount])
