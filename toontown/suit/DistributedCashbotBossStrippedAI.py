import math
import random
import time

from direct.directnotify import DirectNotifyGlobal
from direct.fsm import FSM
from direct.task.TaskManagerGlobal import taskMgr

from toontown.coghq import CraneLeagueGlobals
from toontown.coghq import DistributedCashbotBossSideCraneAI
from toontown.coghq.CashbotBossComboTracker import CashbotBossComboTracker
from toontown.toonbase import ToontownGlobals
from .DistributedBossCogStrippedAI import DistributedBossCogStrippedAI


class DistributedCashbotBossStrippedAI(DistributedBossCogStrippedAI, FSM.FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedCashbotBossAI')

    # How long should we wait before being able to safe helmet the CFO twice?
    SAFE_HELMET_COOLDOWN: int = 60

    def __init__(self, air, game):
        DistributedBossCogStrippedAI.__init__(self, air, game, 'm')
        FSM.FSM.__init__(self, 'DistributedCashbotBossAI')

        self.game = game

        self.ruleset = CraneLeagueGlobals.CFORuleset()
        self.rulesetFallback = self.ruleset  # A fallback ruleset for when we rcr, or change mods mid round
        self.oldMaxLaffs = {}
        self.heldObject = None

        # Some overrides from commands
        self.doTimer = None  # If true, make timer run down instead of count up, modified from a command, if false, count up, if none, use the rule
        self.timerOverride = self.ruleset.TIMER_MODE_TIME_LIMIT  # Amount of time to override in seconds

        # Map of damage multipliers for toons
        self.toonDmgMultipliers = {}

        # The index order to spawn toons
        self.toonSpawnpointOrder = [i for i in range(8)]

        # The intentional safe helmet cooldowns. These are used to prevent safe helmet abuse.
        # Maps toon id -> next available safe helmet timestamp.
        self.safeHelmetCooldownsDict: dict[int, float] = {}

    def allowedToSafeHelmet(self, toonId: int) -> bool:
        if toonId not in self.safeHelmetCooldownsDict:
            return True

        allowedToSafeHelmetTimestamp = self.safeHelmetCooldownsDict[toonId]
        if time.time() >= allowedToSafeHelmetTimestamp:
            return True

        return False

    def addSafeHelmetCooldown(self, toonId: int):
        self.safeHelmetCooldownsDict[toonId] = time.time() + self.SAFE_HELMET_COOLDOWN

    def clearSafeHelmetCooldowns(self):
        self.safeHelmetCooldownsDict.clear()

    def d_setToonSpawnpointOrder(self):
        self.sendUpdate('setToonSpawnpoints', [self.toonSpawnpointOrder])

    def getToonOutgoingMultiplier(self, avId):
        n = self.toonDmgMultipliers.get(avId)
        if not n:
            n = 100
            self.toonDmgMultipliers[avId] = n

        return n

    def updateActivityLog(self, doId, content):
        self.sendUpdate('addToActivityLog', [doId, content])

    def debug(self, doId=None, content='null'):

        if not doId:
            doId = self.doId

        if self.ruleset.GENERAL_DEBUG:
            self.updateActivityLog(doId, content)

    def goonStatesDebug(self, doId='system', content='null'):
        if self.ruleset.GOON_STATES_DEBUG:
            self.updateActivityLog(doId, content)

    def safeStatesDebug(self, doId='system', content='null'):
        if self.ruleset.SAFE_STATES_DEBUG:
            self.updateActivityLog(doId, content)

    def craneStatesDebug(self, doId='system', content='null'):
        if self.ruleset.CRANE_STATES_DEBUG:
            self.updateActivityLog(doId, content)

    def getInvolvedToonsNotSpectating(self):
        return self.involvedToons

    # Clears all current modifiers and restores the ruleset before modifiers were applied
    def resetModifiers(self):
        self.modifiers = []
        self.ruleset = self.rulesetFallback
        self.d_setRawRuleset()

    def getRawRuleset(self):
        return self.ruleset.asStruct()

    def getRuleset(self):
        return self.ruleset

    def doNextAttack(self, task):
        # Choose an attack and do it.

        # Make sure we're waiting for a helmet.
        if self.heldObject is None and not self.waitingForHelmet:
            self.waitForNextHelmet()

        # Rare chance to do a jump attack if we want it
        if self.ruleset.WANT_CFO_JUMP_ATTACK:
            if random.randint(0, 99) < self.ruleset.CFO_JUMP_ATTACK_CHANCE:
                self.__doAreaAttack()
                return

        # Do a directed attack.
        self.__doDirectedAttack()

    def __doDirectedAttack(self):
        # Choose the next toon in line to get the assault.

        # Check if we ran out of targets, if so reset the list back to everyone involved
        if len(self.toonsToAttack) <= 0:
            self.toonsToAttack = list(self.game.avIdList)
            # Shuffle the toons if we want random gear throws
            if self.ruleset.RANDOM_GEAR_THROW_ORDER:
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

    def __doAreaAttack(self):
        self.b_setAttackCode(ToontownGlobals.BossCogAreaAttack)

    def setAttackCode(self, attackCode, avId=0):
        self.attackCode = attackCode
        self.attackAvId = avId

        if attackCode in (ToontownGlobals.BossCogDizzy, ToontownGlobals.BossCogDizzyNow):
            delayTime = self.game.progressValue(20, 5)
            self.hitCount = 0
        elif attackCode in (ToontownGlobals.BossCogSlowDirectedAttack,):
            delayTime = ToontownGlobals.BossCogAttackTimes.get(attackCode)
            delayTime += self.game.progressValue(10, 0)
        elif attackCode in (ToontownGlobals.BossCogAreaAttack,):
            delayTime = self.game.progressValue(20, 9)
        else:
            delayTime = ToontownGlobals.BossCogAttackTimes.get(attackCode, 5.0)

        self.waitForNextAttack(delayTime)
        return

    def d_setAttackCode(self, attackCode, avId=0, delayTime=0):
        self.sendUpdate('setAttackCode', [attackCode, avId, delayTime])

    def b_setAttackCode(self, attackCode, avId=0, delayTime=0):
        self.d_setAttackCode(attackCode, avId, delayTime=delayTime)
        self.setAttackCode(attackCode, avId)

    def getDamageMultiplier(self, allowFloat=False):
        mult = self.game.progressValue(1, self.ruleset.CFO_ATTACKS_MULTIPLIER + (0 if allowFloat else 1))
        if not allowFloat:
            mult = int(mult)
        return mult

    def zapToon(self, x, y, z, h, p, r, bpx, bpy, attackCode, timestamp):

        avId = self.air.getAvatarIdFromSender()
        if not self.validate(avId, avId in self.game.avIdList, 'zapToon from unknown avatar'):
            return

        toon = simbase.air.doId2do.get(avId)
        if not toon:
            return

        # Is the cfo stunned?
        isStunned = self.attackCode == ToontownGlobals.BossCogDizzy
        # Are we setting to swat?
        if isStunned and attackCode == ToontownGlobals.BossCogElectricFence:
            self.d_updateUnstun(avId)

        self.d_showZapToon(avId, x, y, z, h, p, r, attackCode, timestamp)

        damage = self.ruleset.CFO_ATTACKS_BASE_DAMAGE.get(attackCode)
        if damage == None:
            self.notify.warning('No damage listed for attack code %s' % attackCode)
            damage = 5
            raise KeyError('No damage listed for attack code %s' % attackCode)  # temp

        damage *= self.getDamageMultiplier(allowFloat=self.ruleset.CFO_ATTACKS_MULTIPLIER_INTERPOLATE)
        # Clamp the damage to make sure it at least does 1
        damage = max(int(damage), 1)

        self.debug(doId=avId, content='Damaged for %s' % damage)

        self.game.damageToon(toon, damage)

        if attackCode == ToontownGlobals.BossCogElectricFence:
            if bpy < 0 and abs(bpx / bpy) > 0.5:
                if bpx < 0:
                    self.b_setAttackCode(ToontownGlobals.BossCogSwatRight)
                else:
                    self.b_setAttackCode(ToontownGlobals.BossCogSwatLeft)

    def waitForNextHelmet(self):
        taskName = self.uniqueName('NextHelmet')
        taskMgr.remove(taskName)
        delayTime = self.game.progressValue(45, 15)
        taskMgr.doMethodLater(delayTime, self.donHelmet, taskName)
        self.debug(content='Next auto-helmet in %s seconds' % delayTime)
        self.waitingForHelmet = 1

    def donHelmet(self, task):

        if self.ruleset.DISABLE_SAFE_HELMETS:
            return

        self.waitingForHelmet = 0
        if self.heldObject == None:
            # Ok, the boss wants to put on a helmet now.  He can have
            # his special safe 0, which was created for just this
            # purpose.
            safe = self.game.safes[0]
            safe.request('Grabbed', self.doId, self.doId)
            self.heldObject = safe

    def stopHelmets(self):
        self.waitingForHelmet = 0
        taskName = self.uniqueName('NextHelmet')
        taskMgr.remove(taskName)

    # Given a crane, the damage dealt from the crane, and the impact of the hit, should we stun the CFO?
    def considerStun(self, crane, damage, impact):

        damage_stuns = damage >= self.ruleset.CFO_STUN_THRESHOLD
        is_sidecrane = isinstance(crane, DistributedCashbotBossSideCraneAI.DistributedCashbotBossSideCraneAI)
        hard_hit = impact >= self.ruleset.SIDECRANE_IMPACT_STUN_THRESHOLD

        # Is the damage enough?
        if damage_stuns:
            return True

        # Was this a knarbuckle sidecrane hit?
        if is_sidecrane and hard_hit:
            return True

        return False

    def b_setBossDamage(self, bossDamage, avId=0, objId=0, isGoon=False):
        self.d_setBossDamage(bossDamage, avId=avId, objId=objId, isGoon=isGoon)
        self.setBossDamage(bossDamage)

    def setBossDamage(self, bossDamage):
        self.reportToonHealth()
        self.bossDamage = bossDamage

    def d_setBossDamage(self, bossDamage, avId=0, objId=0, isGoon=False):
        self.sendUpdate('setBossDamage', [bossDamage, avId, objId, isGoon])

    def waitForNextAttack(self, delayTime):
        DistributedBossCogStrippedAI.waitForNextAttack(self, delayTime)
        self.debug(content='Next attack in %.2fs' % delayTime)

    def prepareBossForBattle(self):
        # Force unstun the CFO if he was stunned in a previous Battle Three round
        if self.attackCode == ToontownGlobals.BossCogDizzy or self.attackCode == ToontownGlobals.BossCogDizzyNow:
            self.b_setAttackCode(ToontownGlobals.BossCogNoAttack)

        # It's important to set our position correctly even on the AI,
        # so the goons can orient to the center of the room.
        self.setPosHpr(*ToontownGlobals.CashbotBossBattleThreePosHpr)

        # A list of toons to attack.  We start out with the list in
        # random order.
        self.toonsToAttack = []

        if self.ruleset.RANDOM_GEAR_THROW_ORDER:
            random.shuffle(self.toonsToAttack)

        self.b_setBossDamage(0)
        self.battleThreeStart = globalClock.getFrameTime()
        self.waitForNextAttack(15)
        self.waitForNextHelmet()

        self.oldMaxLaffs = {}
        self.toonDmgMultipliers = {}

        self.toonsWon = False

    def cleanupBossBattle(self):
        helmetName = self.uniqueName('NextHelmet')
        taskMgr.remove(helmetName)
        self.stopAttacks()
        self.stopHelmets()
        self.heldObject = None

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
        for safe in self.game.safes:
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

    def setObjectID(self, objId):
        self.objectId = objId
