import functools

from panda3d.core import *
from direct.directnotify import DirectNotifyGlobal
from direct.showbase.PythonUtil import clamp
from toontown.toonbase import ToontownGlobals
from toontown.coghq import DistributedCashbotBossCraneAI
from toontown.coghq import DistributedCashbotBossSideCraneAI
from toontown.coghq import DistributedCashbotBossHeavyCraneAI
from toontown.coghq import DistributedCashbotBossSafeAI
from toontown.suit import DistributedCashbotBossGoonAI
from toontown.coghq import DistributedCashbotBossTreasureAI
from toontown.coghq import CraneLeagueGlobals
from toontown.battle import BattleExperienceAI
from toontown.chat import ResistanceChat
from direct.fsm import FSM
from . import DistributedBossCogAI
import random
import math

from apworld.toontown import locations
from ..archipelago.definitions.death_reason import DeathReason

from ..archipelago.definitions.util import ap_location_name_to_id

# How many unites do we award on victory
NUM_RESISTANCE_REWARDS = 6


class DistributedCashbotBossAI(DistributedBossCogAI.DistributedBossCogAI, FSM.FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedCashbotBossAI')

    def __init__(self, air):
        DistributedBossCogAI.DistributedBossCogAI.__init__(self, air, 'm')
        FSM.FSM.__init__(self, 'DistributedCashbotBossAI')
        self.ruleset = CraneLeagueGlobals.CFORuleset()
        self.rulesetFallback = self.ruleset  # A fallback ruleset for when we rcr, or change mods mid round
        self.modifiers = []  # A list of CFORulesetModifierBase instances
        self.oldMaxLaffs = {}
        self.rewardId = ResistanceChat.getRandomId()
        self.rewardedToons = []
        self.cranes = None
        self.safes = None
        self.goons = None
        self.treasures = {}
        self.grabbingTreasures = {}
        self.recycledTreasures = []
        self.bossMaxDamage = self.bossMaxDamage

        # We need a scene to do the collision detection in.
        self.scene = NodePath('scene')
        self.reparentTo(self.scene)

        # And some solids to keep the goons constrained to our room.
        cn = CollisionNode('walls')
        cs = CollisionSphere(0, 0, 0, 13)
        cn.addSolid(cs)
        cs = CollisionInvSphere(0, 0, 0, 42)
        cn.addSolid(cs)
        self.attachNewNode(cn)


        # By "heldObject", we mean the safe he's currently wearing as
        # a helmet, if any.  It's called a heldObject because this is
        # the way the cranes refer to the same thing, and we use the
        # same interface to manage this.
        self.heldObject = None

        self.waitingForHelmet = 0

        self.wantSafeRushPractice = False
        self.wantCustomCraneSpawns = False
        self.wantAimPractice = False
        self.toonsWon = False
        
        # Controlled RNG parameters, True to enable, False to disable
        self.wantOpeningModifications = False
        self.wantMaxSizeGoons = False
        self.wantLiveGoonPractice = False
        self.wantNoStunning = False

        self.customSpawnPositions = {}
        self.goonMinScale = 0.8
        self.goonMaxScale = 2.4
        self.safesWanted = 5

        # A list of toon ids that are spectating
        self.spectators = []

        self.rollModsOnStart = False
        self.numModsWanted = 5

        # Some overrides from commands
        self.doTimer = None  # If true, make timer run down instead of count up, modified from a command, if false, count up, if none, use the rule
        self.timerOverride = self.ruleset.TIMER_MODE_TIME_LIMIT  # Amount of time to override in seconds

        # Map of damage multipliers for toons
        self.toonDmgMultipliers = {}

        # The index order to spawn toons
        self.toonSpawnpointOrder = [i for i in range(8)]

    def d_setToonSpawnpointOrder(self):
        self.sendUpdate('setToonSpawnpoints', [self.toonSpawnpointOrder])

    def getToonOutgoingMultiplier(self, avId):
        n = self.toonDmgMultipliers.get(avId)
        if not n:
            n = 100
            self.toonDmgMultipliers[avId] = n

        return n

    def increaseToonOutgoingMultiplier(self, avId, n):
        # Makes sure theres something in the dict
        old = self.getToonOutgoingMultiplier(avId)
        self.toonDmgMultipliers[avId] = old + n
        print(("avId now does +" + str(old+n) + "% damage"))

    def debug(self, doId=None, content='null'):
        pass
            
    def clearObjectSpeedCaching(self):
        if self.safes:
            for safe in self.safes:
                safe.d_resetSpeedCaching()
        
        if self.goons:
            for goon in self.goons:
                goon.d_resetSpeedCaching()

    def getInvolvedToonsNotSpectating(self):
        toons = list(self.involvedToons)
        for s in self.spectators:
            if s in toons:
                toons.remove(s)

        return toons

    def progressValue(self, fromValue, toValue):
        t0 = float(self.bossDamage) / float(self.bossMaxDamage)
        elapsed = globalClock.getFrameTime() - self.battleThreeStart
        t1 = elapsed / float(self.battleThreeDuration)
        t = max(t0, t1)
        return fromValue + (toValue - fromValue) * min(t, 1)

    # Any time you change the ruleset, you should call this to sync the clients
    def d_setRawRuleset(self):
        self.sendUpdate('setRawRuleset', [self.getRawRuleset()])

    def __getRawModifierList(self):
        mods = []
        for modifier in self.modifiers:
            mods.append(modifier.asStruct())

        return mods

    def d_setModifiers(self):
        self.sendUpdate('setModifiers', [self.__getRawModifierList()])

    # Call to update the ruleset with the modifiers active, note calling more than once can cause unexpected behavior
    # if the ruleset doesn't fallback to an initial value, for example if a cfo hp increasing modifier is active and we
    # call this multiply times, his hp will be 1500 * 1.5 * 1.5 * 1.5 etc etc
    def applyModifiers(self, updateClient=False):
        for modifier in self.modifiers:
            modifier.apply(self.ruleset)

        if updateClient:
            self.d_setRawRuleset()

    # Clears all current modifiers and restores the ruleset before modifiers were applied
    def resetModifiers(self):
        self.modifiers = []
        self.ruleset = self.rulesetFallback
        self.d_setRawRuleset()

    def getRawRuleset(self):
        return self.ruleset.asStruct()

    def getRuleset(self):
        return self.ruleset

    def setupTimer(self):
        # If command says we should force the timer into a certain state
        # Nothing changed, don't do anything
        if self.doTimer is None:
            return

        # Timer should always count up
        if not self.doTimer:
            self.ruleset.TIMER_MODE = False
            return

        # Timer should always go down
        self.ruleset.TIMER_MODE = True
        self.ruleset.TIMER_MODE_TIME_LIMIT = self.timerOverride if self.timerOverride > 0 else self.ruleset.TIMER_MODE_TIME_LIMIT

    def setupRuleset(self):

        self.ruleset = CraneLeagueGlobals.CFORuleset()

        self.setupTimer()

        self.rulesetFallback = self.ruleset

        # Should we randomize some modifiers?
        if self.rollModsOnStart:
            self.rollRandomModifiers()

        self.applyModifiers()
        # Make sure they didn't do anything bad
        self.ruleset.validate()
        self.debug(content='Applied %s modifiers' % len(self.modifiers))

        # Update the client
        self.d_setRawRuleset()
        self.d_setModifiers()

    def rollRandomModifiers(self):
        tierLeftBound = self.ruleset.MODIFIER_TIER_RANGE[0]
        tierRightBound = self.ruleset.MODIFIER_TIER_RANGE[1]
        pool = [c(random.randint(tierLeftBound, tierRightBound)) for c in CraneLeagueGlobals.NON_SPECIAL_MODIFIER_CLASSES]
        random.shuffle(pool)

        self.modifiers = [pool.pop() for _ in range(self.numModsWanted)]

        # If we roll a % roll, go ahead and make this a special cfo
        # Doing this last also ensures any rules that the special mod needs to set override
        if random.randint(0, 99) < CraneLeagueGlobals.SPECIAL_MODIFIER_CHANCE:
            cls = random.choice(CraneLeagueGlobals.SPECIAL_MODIFIER_CLASSES)
            tier = random.randint(tierLeftBound, tierRightBound)
            mod_instance = cls(tier)
            self.modifiers.append(mod_instance)

    def generate(self):
        """
        Inheritors should put functions that require self.zoneId or
        other networked info in this function.
        """
        DistributedBossCogAI.DistributedBossCogAI.generate(self)

        if __dev__:
            self.scene.reparentTo(self.getRender())

    def getHoodId(self):
        return ToontownGlobals.CashbotHQ

    def formatReward(self):
        # Returns the reward indication to write to the event log.
        return f'{self.rewardId}'

    def makeBattleOneBattles(self):
        self.postBattleState = 'PrepareBattleThree'
        self.initializeBattles(1, ToontownGlobals.CashbotBossBattleOnePosHpr)

    def generateSuits(self, battleNumber):
        cogs = self.invokeSuitPlanner(2, 0)
        skelecogs = self.invokeSuitPlanner(3, 1)

        # Now combine the lists of suits together, so that they all
        # come out mix-and-match.
        activeSuits = cogs['activeSuits'] + skelecogs['activeSuits']
        reserveSuits = cogs['reserveSuits'] + skelecogs['reserveSuits']

        random.shuffle(activeSuits)

        # We might have ended up with too many suits on the
        # activeSuits list.  If that happens, put the overflow suits
        # on the reserve list, with a 100% joinChance.
        while len(activeSuits) > 4:
            suit = activeSuits.pop()
            reserveSuits.append((suit, 100))

        # We must keep the reserveSuits sorted in increasing order of
        # joinChance.
        def compareJoinChance(a, b):
            return cmp(a[1], b[1])
        reserveSuits.sort(key=functools.cmp_to_key(compareJoinChance))

        return {'activeSuits': activeSuits, 'reserveSuits': reserveSuits}

    def removeToon(self, avId, died=False):
        # The toon leaves the zone, either through disconnect, death,
        # or something else.  Tell all of the safes, cranes, and goons.

        if self.cranes != None:
            for crane in self.cranes:
                crane.removeToon(avId)

        if self.safes != None:
            for safe in self.safes:
                safe.removeToon(avId)

        if self.goons != None:
            for goon in self.goons:
                goon.removeToon(avId)

        DistributedBossCogAI.DistributedBossCogAI.removeToon(self, avId, died=died)
        return

    def __makeBattleThreeObjects(self):
        if self.cranes == None:
            # Generate all of the cranes.
            self.cranes = []
            ind = 0

            self.debug(content='Generating %s normal cranes' % len(CraneLeagueGlobals.NORMAL_CRANE_POSHPR))
            for _ in CraneLeagueGlobals.NORMAL_CRANE_POSHPR:
                crane = DistributedCashbotBossCraneAI.DistributedCashbotBossCraneAI(self.air, self, ind)
                crane.generateWithRequired(self.zoneId)
                self.cranes.append(crane)
                ind += 1

            # Generate the sidecranes if wanted
            if self.ruleset.WANT_SIDECRANES:
                self.debug(content='Generating %s sidecranes' % len(CraneLeagueGlobals.SIDE_CRANE_POSHPR))
                for _ in CraneLeagueGlobals.SIDE_CRANE_POSHPR:
                    crane = DistributedCashbotBossSideCraneAI.DistributedCashbotBossSideCraneAI(self.air, self, ind)
                    crane.generateWithRequired(self.zoneId)
                    self.cranes.append(crane)
                    ind += 1

            # Generate the heavy cranes if wanted
            if self.ruleset.WANT_HEAVY_CRANES:
                self.debug(content='Generating %s heavy cranes' % len(CraneLeagueGlobals.HEAVY_CRANE_POSHPR))
                for _ in CraneLeagueGlobals.HEAVY_CRANE_POSHPR:
                    crane = DistributedCashbotBossHeavyCraneAI.DistributedCashbotBossHeavyCraneAI(self.air, self, ind)
                    crane.generateWithRequired(self.zoneId)
                    self.cranes.append(crane)
                    ind += 1

        if self.safes == None:
            # And all of the safes.
            self.safes = []
            for index in range(min(self.ruleset.SAFES_TO_SPAWN, len(CraneLeagueGlobals.SAFE_POSHPR))):
                safe = DistributedCashbotBossSafeAI.DistributedCashbotBossSafeAI(self.air, self, index)
                safe.generateWithRequired(self.zoneId)
                self.safes.append(safe)

        if self.goons == None:
            # We don't actually make the goons right now, but we make
            # a place to hold them.
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
        # Choose an attack and do it.

        # Make sure we're waiting for a helmet.
        if self.heldObject == None and not self.waitingForHelmet:
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
            self.toonsToAttack = self.getInvolvedToonsNotSpectating()
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
            delayTime = self.progressValue(20, 5)
            self.hitCount = 0
        elif attackCode in (ToontownGlobals.BossCogSlowDirectedAttack,):
            delayTime = ToontownGlobals.BossCogAttackTimes.get(attackCode)
            delayTime += self.progressValue(10, 0)
        elif attackCode in (ToontownGlobals.BossCogAreaAttack,):
            delayTime = self.progressValue(20, 9)
        else:
            delayTime = ToontownGlobals.BossCogAttackTimes.get(attackCode, 5.0)

        if len(self.involvedToons) == 1 and attackCode not in (ToontownGlobals.BossCogDizzy, ToontownGlobals.BossCogDizzyNow):
            delayTime *= 1.5

        self.waitForNextAttack(delayTime)
        return

    def getDamageMultiplier(self, allowFloat=False):
        mult = self.progressValue(1, self.ruleset.CFO_ATTACKS_MULTIPLIER + (0 if allowFloat else 1))
        if not allowFloat:
            mult = int(mult)
        return mult

    def zapToon(self, x, y, z, h, p, r, bpx, bpy, attackCode, timestamp):

        avId = self.air.getAvatarIdFromSender()
        if not self.validate(avId, avId in self.involvedToons, 'zapToon from unknown avatar'):
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

        toon.setDeathReason(self.getDeathReasonFromAttackCode(attackCode))
        self.damageToon(toon, damage)
        currState = self.getCurrentOrNextState()

        if attackCode == ToontownGlobals.BossCogElectricFence and (currState == 'RollToBattleTwo' or currState == 'BattleThree'):
            if bpy < 0 and abs(bpx / bpy) > 0.5:
                if bpx < 0:
                    self.b_setAttackCode(ToontownGlobals.BossCogSwatRight)
                else:
                    self.b_setAttackCode(ToontownGlobals.BossCogSwatLeft)

    def makeTreasure(self, goon):
        # Places a treasure, as pooped out by the given goon.  We
        # place the treasure at the goon's current position, or at
        # least at the beginning of its current path.  Actually, we
        # ignore Z, and always place the treasure at Z == 0,
        # presumably the ground.

        if self.state != 'BattleThree':
            return

        # Too many treasures on the field?
        if len(self.treasures) >= self.ruleset.MAX_TREASURE_AMOUNT:
            self.debug(doId=goon.doId, content='Not spawning treasure, already %s present' % self.ruleset.MAX_TREASURE_AMOUNT)
            return

        # Drop chance?
        if self.ruleset.GOON_TREASURE_DROP_CHANCE < 1.0:
            r = random.random()
            self.debug(doId=goon.doId, content='Rolling for treasure drop, need > %s, got %s' % (self.ruleset.GOON_TREASURE_DROP_CHANCE, r))
            if r > self.ruleset.GOON_TREASURE_DROP_CHANCE:
                return

        # The BossCog acts like a treasure planner as far as the
        # treasure is concerned.
        pos = goon.getPos(self)

        # The treasure pops out and lands somewhere nearby.  Let's
        # start by choosing a point on a ring around the boss, based
        # on our current angle to the boss.
        v = Vec3(pos[0], pos[1], 0.0)
        if not v.normalize():
            v = Vec3(1, 0, 0)
        v = v * 27

        # Then perterb that point by a distance in some random
        # direction.
        angle = random.uniform(0.0, 2.0 * math.pi)
        radius = 10
        dx = radius * math.cos(angle)
        dy = radius * math.sin(angle)

        fpos = self.scene.getRelativePoint(self, Point3(v[0] + dx, v[1] + dy, 0))

        # Find an index based on the goon strength we should use
        treasureHealIndex = 1.0*(goon.strength-self.ruleset.MIN_GOON_DAMAGE) / (self.ruleset.MAX_GOON_DAMAGE-self.ruleset.MIN_GOON_DAMAGE)
        treasureHealIndex *= len(self.ruleset.GOON_HEALS)
        treasureHealIndex = int(clamp(treasureHealIndex, 0, len(self.ruleset.GOON_HEALS)-1))
        healAmount = self.ruleset.GOON_HEALS[treasureHealIndex]
        availStyles = self.ruleset.TREASURE_STYLES[treasureHealIndex]
        style = random.choice(availStyles)

        if self.recycledTreasures:
            # Reuse a previous treasure object
            treasure = self.recycledTreasures.pop(0)
            treasure.d_setGrab(0)
            treasure.b_setGoonId(goon.doId)
            treasure.b_setStyle(style)
            treasure.b_setPosition(pos[0], pos[1], 0)
            treasure.b_setFinalPosition(fpos[0], fpos[1], 0)
            treasure.setResponsibleAv(goon.getStunnedByAvId())
        else:
            # Create a new treasure object
            treasure = DistributedCashbotBossTreasureAI.DistributedCashbotBossTreasureAI(self.air, self, goon, style, fpos[0], fpos[1], 0)
            treasure.setResponsibleAv(goon.getStunnedByAvId())
            treasure.generateWithRequired(self.zoneId)
        treasure.healAmount = healAmount
        self.treasures[treasure.doId] = treasure

    # Called from treasures when they are picked up, tells us who should be credited for this healing
    def toonHealedFromTreasure(self, avId, responsibleAv, healAmount):
        self.d_avHealed(responsibleAv, healAmount)

    def grabAttempt(self, avId, treasureId):
        # An avatar has attempted to grab a treasure.
        av = self.air.doId2do.get(avId)
        if not av:
            return
        treasure = self.treasures.get(treasureId)
        if treasure:
            if treasure.validAvatar(av):
                del self.treasures[treasureId]
                treasure.d_setGrab(avId)
                self.grabbingTreasures[treasureId] = treasure
                # Wait a few seconds for the animation to play, then
                # recycle the treasure.
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
        return self.progressValue(self.ruleset.MAX_GOON_AMOUNT_START, self.ruleset.MAX_GOON_AMOUNT_END)

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

        # First, look to see if we have a goon we can recycle.
        goon = self.__chooseOldGoon()
        if goon == None:
            # No, no old goon; is there room for a new one?
            if len(self.goons) >= self.getMaxGoons():
                return
            # make a new one.
            goon = DistributedCashbotBossGoonAI.DistributedCashbotBossGoonAI(self.air, self)
            goon.generateWithRequired(self.zoneId)
            self.goons.append(goon)

        # Attributes for desperation mode goons
        goon_stun_time = 4
        goon_velocity = 8
        goon_hfov = 90
        goon_attack_radius = 20
        goon_strength = self.ruleset.MAX_GOON_DAMAGE
        goon_scale = 1.8

        # If the battle isn't in desperation yet override the values to normal values
        if self.getBattleThreeTime() <= 1.0:
            goon_stun_time = self.progressValue(30, 8)
            goon_velocity = self.progressRandomValue(3, 7)
            goon_hfov = self.progressRandomValue(70, 80)
            goon_attack_radius = self.progressRandomValue(6, 15)
            goon_strength = int(self.progressRandomValue(self.ruleset.MIN_GOON_DAMAGE, self.ruleset.MAX_GOON_DAMAGE))
            goon_scale = self.progressRandomValue(self.goonMinScale, self.goonMaxScale, noRandom=self.wantMaxSizeGoons)

        # Apply multipliers if necessary
        goon_velocity *= self.ruleset.GOON_SPEED_MULTIPLIER

        # Apply attributes to the goon
        goon.STUN_TIME = goon_stun_time
        goon.b_setupGoon(velocity=goon_velocity, hFov=goon_hfov, attackRadius=goon_attack_radius, strength=goon_strength, scale=goon_scale)
        goon.request(side)

        self.debug(doId=goon.doId, content='Spawning on %s, stun=%.2f, vel=%.2f, hfov=%.2f, attRadius=%.2f, str=%s, scale=%.2f' % (side, goon_stun_time, goon_velocity, goon_hfov, goon_attack_radius, goon_strength, goon_scale))

    def __chooseOldGoon(self):
        # Walks through the list of goons managed by the boss to see
        # if any of them have recently been deleted and can be
        # recycled.

        for goon in self.goons:
            if goon.state == 'Off':
                return goon

    def waitForNextGoon(self, delayTime):
        currState = self.getCurrentOrNextState()
        if currState == 'BattleThree':
            taskName = self.uniqueName('NextGoon')
            taskMgr.remove(taskName)
            taskMgr.doMethodLater(delayTime, self.doNextGoon, taskName)
            self.debug(content='Spawning goon in %.2fs' % delayTime)

    def stopGoons(self):
        taskName = self.uniqueName('NextGoon')
        taskMgr.remove(taskName)

    def doNextGoon(self, task):
        if self.attackCode != ToontownGlobals.BossCogDizzy:
            self.makeGoon()

        # How long to wait for the next goon?
        if self.wantLiveGoonPractice:
            delayTime = 4
        else:
            delayTime = self.progressValue(10, 2)
        self.waitForNextGoon(delayTime)

    def waitForNextHelmet(self):
        currState = self.getCurrentOrNextState()
        if currState == 'BattleThree':
            taskName = self.uniqueName('NextHelmet')
            taskMgr.remove(taskName)
            delayTime = self.progressValue(60, 30)
            taskMgr.doMethodLater(delayTime, self.__donHelmet, taskName)
            self.debug(content='Next auto-helmet in %s seconds' % delayTime)
            self.waitingForHelmet = 1

    def setObjectID(self, objId):
        self.objectId = objId

    def __donHelmet(self, task):

        if self.ruleset.DISABLE_SAFE_HELMETS:
            return

        self.waitingForHelmet = 0
        if self.heldObject == None:
            # Ok, the boss wants to put on a helmet now.  He can have
            # his special safe 0, which was created for just this
            # purpose.
            safe = self.safes[0]
            safe.request('Grabbed', self.doId, self.doId)
            self.heldObject = safe

    def stopHelmets(self):
        self.waitingForHelmet = 0
        taskName = self.uniqueName('NextHelmet')
        taskMgr.remove(taskName)

    def acceptHelmetFrom(self, avId):
        # Returns true if we can accept a helmet from the indicated
        # avatar, false otherwise.  Each avatar gets a timeout of five
        # minutes after giving us a helmet, so we don't accept too
        # many helmets from the same avatar--this cuts down on helmet
        # griefing.

        # NOTE (by Lou): the block of code below completely eliminates
        # the cooldown on the ability to safe-on the CFO with helmets,
        # and was commented out for Crane League purposes:

        '''
        now = globalClock.getFrameTime()
        then = self.avatarHelmets.get(avId, None)
        if then == None or (now - then > 300):
            self.avatarHelmets[avId] = now
            return 1

        return 0
        '''

        return True

    def magicWordHit(self, damage, avId):
        # Called by the magic word "~bossBattle hit damage"
        if self.heldObject:
            # Drop the current helmet.
            self.heldObject.demand('Dropped', avId, self.doId)
            self.heldObject.avoidHelmet = 1
            self.heldObject = None
            self.waitForNextHelmet()

        else:
            # Ouch!
            self.recordHit(damage)
        return

    def magicWordReset(self):
        # Resets all of the cranes and safes.
        # Called only by the magic word "~bossBattle reset"
        if self.state == 'BattleThree':
            self.__resetBattleThreeObjects()

    def magicWordResetGoons(self):
        # Resets all of the goons.
        # Called only by the magic word "~bossBattle goons"
        if self.state == 'BattleThree':
            if self.goons != None:
                for goon in self.goons:
                    goon.request('Off')
                    goon.requestDelete()

                self.goons = None
            self.__makeBattleThreeObjects()
        return

    # Given a crane, the damage dealt from the crane, and the impact of the hit, should we stun the CFO?
    def considerStun(self, crane, damage, impact):

        damage_stuns = damage >= self.ruleset.CFO_STUN_THRESHOLD
        is_sidecrane = isinstance(crane, DistributedCashbotBossSideCraneAI.DistributedCashbotBossSideCraneAI)
        hard_hit = impact >= self.ruleset.SIDECRANE_IMPACT_STUN_THRESHOLD

        # Are we in safe rush practice mode? All hits stun in this mode
        if self.wantSafeRushPractice:
            return True

        # Is the damage enough?
        if damage_stuns:
            return True

        # Was this a knarbuckle sidecrane hit?
        if is_sidecrane and hard_hit:
            return True

        return False

    def recordHit(self, damage, impact=0, craneId=-1):
        avId = self.air.getAvatarIdFromSender()
        crane = simbase.air.doId2do.get(craneId)
        if not self.validate(avId, avId in self.getInvolvedToonsNotSpectating(), 'recordHit from unknown avatar'):
            return

        if self.state != 'BattleThree':
            return

        # Momentum mechanic?
        if self.ruleset.WANT_MOMENTUM_MECHANIC:
            damage *= (self.getToonOutgoingMultiplier(avId) / 100.0)
            print(('multiplying damage by ' + str(self.getToonOutgoingMultiplier(avId) / 100.0) + ' damage is now ' + str(damage)))

        # Record a successful hit in battle three.
        self.b_setBossDamage(self.bossDamage + damage)

        # Award bonus points for hits with maximum impact
        if impact == 1.0:
            self.d_updateMaxImpactHits(avId)
        self.d_damageDealt(avId, damage)

        self.incrementCombo(avId, (self.getComboLength(avId)+1.0) / 10.0 * damage)

        self.debug(doId=avId, content='Damaged for %s with impact: %.2f' % (damage, impact))

        # The CFO has been defeated, proceed to Victory state
        if self.bossDamage >= self.bossMaxDamage:
            self.d_killingBlowDealt(avId)
            self.toonsWon = True
            self.b_setState('Victory')
            return

        # The CFO is already dizzy, OR the crane is None, so get outta here
        if self.attackCode == ToontownGlobals.BossCogDizzy or not crane:
            return

        self.stopHelmets()

        # Is the damage high enough to stun? or did a side crane hit a high impact hit?
        hitMeetsStunRequirements = self.considerStun(crane, damage, impact)
        if self.wantNoStunning:
            hitMeetsStunRequirements = False
        if hitMeetsStunRequirements:
            # A particularly good hit (when he's not already
            # dizzy) will make the boss dizzy for a little while.
            self.b_setAttackCode(ToontownGlobals.BossCogDizzy)
            self.d_stunBonus(avId, self.ruleset.POINTS_STUN)
        else:

            if self.ruleset.CFO_FLINCHES_ON_HIT:
                self.b_setAttackCode(ToontownGlobals.BossCogNoAttack)

            self.waitForNextHelmet()

        # Now at the very end, if we have momentum mechanic on add some damage multiplier
        if self.ruleset.WANT_MOMENTUM_MECHANIC:
            self.increaseToonOutgoingMultiplier(avId, damage)

    def b_setBossDamage(self, bossDamage):
        self.d_setBossDamage(bossDamage)
        self.setBossDamage(bossDamage)

    def setBossDamage(self, bossDamage):
        self.reportToonHealth()
        self.bossDamage = bossDamage

    def d_setBossDamage(self, bossDamage):
        self.sendUpdate('setBossDamage', [bossDamage])

    def d_killingBlowDealt(self, avId):
        self.sendUpdate('killingBlowDealt', [avId])

    def d_updateGoonsStomped(self, avId):
        self.incrementCombo(avId, math.ceil((self.getComboLength(avId) + 1.0) / 4.0))
        self.sendUpdate('updateGoonsStomped', [avId])

    # call with 10 when we take a safe off, -20 when we put a safe on
    def d_updateSafePoints(self, avId, amount):
        self.sendUpdate('updateSafePoints', [avId, amount])

    def d_updateMaxImpactHits(self, avId):
        self.sendUpdate('updateMaxImpactHits', [avId])

    def d_updateLowImpactHits(self, avId):
        self.sendUpdate('updateLowImpactHits', [avId])

    def d_setCraneSpawn(self, want, spawn, toonId):
        self.sendUpdate('setCraneSpawn', [want, spawn, toonId])

    def d_setRewardId(self, rewardId):
        self.sendUpdate('setRewardId', [rewardId])

    def applyReward(self):
        # The client has reached that point in the movie where he
        # should have the reward applied to him.
        avId = self.air.getAvatarIdFromSender()
        if avId in self.involvedToons and \
                avId not in self.rewardedToons:
            self.rewardedToons.append(avId)
            toon = self.air.doId2do.get(avId)
            if toon:
                toon.doResistanceEffect(self.rewardId)

    ####### FSM STATES ########


    ##### Off state #####
    def enterOff(self):
        DistributedBossCogAI.DistributedBossCogAI.enterOff(self)
        self.rewardedToons = []

    def exitOff(self):
        DistributedBossCogAI.DistributedBossCogAI.exitOff(self)

    ##### Introduction state #####
    def enterIntroduction(self):
        DistributedBossCogAI.DistributedBossCogAI.enterIntroduction(self)

        # We want to have cranes and safes visible in the next room
        # for the introduction cutscene.
        self.__makeBattleThreeObjects()
        self.__resetBattleThreeObjects()

    def exitIntroduction(self):
        DistributedBossCogAI.DistributedBossCogAI.exitIntroduction(self)

        # Clean up battle objects until we need them again later.
        self.__deleteBattleThreeObjects()

    def setupSpawnpoints(self):
        self.toonSpawnpointOrder = [i for i in range(8)]
        if self.ruleset.RANDOM_SPAWN_POSITIONS:
            random.shuffle(self.toonSpawnpointOrder)
        self.d_setToonSpawnpointOrder()

    ##### PrepareBattleThree state #####
    def enterPrepareBattleThree(self):
        self.canSkip = True
        self.setupRuleset()
        self.setupSpawnpoints()
        self.divideToons()

        self.resetBattles()

        self.__makeBattleThreeObjects()
        self.__resetBattleThreeObjects()

        # The clients will play a cutscene.  When they are done
        # watching the movie, we continue.
        self.barrier = self.beginBarrier('PrepareBattleThree', self.involvedToons, 55, self.__donePrepareBattleThree)

    def __donePrepareBattleThree(self, avIds):
        self.b_setState('BattleThree')

    def exitPrepareBattleThree(self):
        self.canSkip = False
        if hasattr(self, 'newState'):
            if self.newState != 'BattleThree':
                self.__deleteBattleThreeObjects()
        self.ignoreBarrier(self.barrier)

    def waitForNextAttack(self, delayTime):
        DistributedBossCogAI.DistributedBossCogAI.waitForNextAttack(self, delayTime)
        self.debug(content='Next attack in %.2fs' % delayTime)

    ##### BattleThree state #####
    def enterBattleThree(self):
        self.divideToons()
        # Calculate the max hp of the boss
        cfoMaxHp = self.ruleset.CFO_MAX_HP + self.ruleset.HP_PER_EXTRA * (len(self.involvedToons) - 1)
        self.bossMaxDamage = min(self.ruleset.get_max_allowed_hp(), cfoMaxHp)

        # Force unstun the CFO if he was stunned in a previous Battle Three round
        if self.attackCode == ToontownGlobals.BossCogDizzy or self.attackCode == ToontownGlobals.BossCogDizzyNow:
            self.b_setAttackCode(ToontownGlobals.BossCogNoAttack)

        # It's important to set our position correctly even on the AI,
        # so the goons can orient to the center of the room.
        self.setPosHpr(*ToontownGlobals.CashbotBossBattleThreePosHpr)

        # Just in case we didn't pass through PrepareBattleThree state.
        self.__makeBattleThreeObjects()
        self.__resetBattleThreeObjects()

        self.reportToonHealth()

        # A list of toons to attack.  We start out with the list in
        # random order.
        self.toonsToAttack = self.getInvolvedToonsNotSpectating()

        if self.ruleset.RANDOM_GEAR_THROW_ORDER:
            random.shuffle(self.toonsToAttack)

        self.b_setBossDamage(0)
        self.battleThreeStart = globalClock.getFrameTime()

        self.resetBattles()
        self.waitForNextAttack(15)
        self.waitForNextHelmet()

        # Make four goons up front to keep things interesting from the
        # beginning.
        self.makeGoon(side='EmergeA')
        self.makeGoon(side='EmergeB')
        taskName = self.uniqueName('NextGoon')
        taskMgr.remove(taskName)
        taskMgr.doMethodLater(2, self.__doInitialGoons, taskName)
        self.battleThreeTimeStarted = globalClock.getFrameTime()

        self.oldMaxLaffs = {}
        self.toonDmgMultipliers = {}

        taskMgr.remove(self.uniqueName('failedCraneRound'))
        self.cancelReviveTasks()

        self.initializeComboTrackers()
        self.listenForToonDeaths()

        self.toonsWon = False
        taskMgr.remove(self.uniqueName('times-up-task'))
        taskMgr.remove(self.uniqueName('post-times-up-task'))
        # If timer mode is active, end the crane round later
        if self.ruleset.TIMER_MODE:
            taskMgr.doMethodLater(self.ruleset.TIMER_MODE_TIME_LIMIT, self.__timesUp, self.uniqueName('times-up-task'))
            self.debug(content='Time will run out in %ss' % self.ruleset.TIMER_MODE_TIME_LIMIT)

    # Called when we actually run out of time, simply tell the clients we ran out of time then handle it later
    def __timesUp(self, task=None):
        self.__donHelmet(None)
        for avId in self.getInvolvedToonsNotSpectating():
            av = self.air.doId2do.get(avId)
            if av:
                av.takeDamage(av.getMaxHp())

        self.sendUpdate('timesUp', [])

        self.toonsWon = False
        taskMgr.remove(self.uniqueName('times-up-task'))
        taskMgr.doMethodLater(10.0, self.__handlePostTimesUp, self.uniqueName('post-times-up-task'))

    # Called a small amount of time later after we run out of time
    def __handlePostTimesUp(self, task=None):
        taskMgr.remove(self.uniqueName('times-up-task'))
        taskMgr.remove(self.uniqueName('post-times-up-task'))

        if self.ruleset.RESTART_CRANE_ROUND_ON_FAIL:
            self.__restartCraneRoundTask(None)
        else:
            self.b_setState('Victory')

    def __doInitialGoons(self, task):
        self.makeGoon(side='EmergeA')
        self.makeGoon(side='EmergeB')
        if self.wantLiveGoonPractice:
            self.waitForNextGoon(7)
        else:
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
        self.cancelReviveTasks()
        taskMgr.remove(self.uniqueName('times-up-task'))
        taskMgr.remove(self.uniqueName('post-times-up-task'))
        return

    ##### Victory state #####
    def enterVictory(self):

        # Calculate how long the crane round took
        craneTime = globalClock.getFrameTime()
        actualTime = craneTime - self.battleThreeTimeStarted
        self.d_updateTimer(actualTime)

        self.ignoreToonDeaths()
        # add a suit-defeat entry for the CFO
        self.suitsKilled.append({
            'type': None, 'level': 0, 'track': self.dna.dept, 'isSkelecog': 0, 'isForeman': 0, 'isVP': 0, 'isCFO': 1,'isSupervisor': 0, 'isVirtual': 0, 'activeToons': self.involvedToons[:]
        })
        # based on code in DistributedBattleBaseAI.__movieDone
        self.resetBattles()
        self.barrier = self.beginBarrier('Victory', self.involvedToons, 30, self.__doneVictory)
        return

    def __doneVictory(self, avIds):

        # Tell the client the information it needs to generate a
        # reward movie.
        self.d_setBattleExperience()

        # First, move the clients into the reward start.  They'll
        # build the reward movies immediately.
        self.b_setState('Reward')

        # Now that the clients have started to build their reward
        # movies, we can actually assign all the experience and
        # rewards.  If we did this sooner, the quest reward panel
        # would show the rewards being applied twice.

        # There is no race condition between AI and client here
        # because these messages are sent sequentially on the wire.
        BattleExperienceAI.assignRewards(
            self.involvedToons, self.toonSkillPtsGained, self.suitsKilled,
            ToontownGlobals.dept2cogHQ(self.dept), self.helpfulToons)

        # A list of resistance messages to give the toons as a reward
        rewards = []

        for _ in range(NUM_RESISTANCE_REWARDS):
            rewards.append(self.getRandomResistanceRewardId())

        if len(rewards) > 0:
            self.rewardId = rewards[0]

        # Don't forget to give the toon the resistance chat reward and the
        # promotion!
        for toonId in self.involvedToons:
            toon = self.air.doId2do.get(toonId)
            if toon:
                bundleCount = toon.slotData.get('checks_per_boss', 4)
                bundle = [locations.ToontownLocationName.CASHBOT_PROOF_1.value,
                          locations.ToontownLocationName.CASHBOT_PROOF_2.value,
                          locations.ToontownLocationName.CASHBOT_PROOF_3.value,
                          locations.ToontownLocationName.CASHBOT_PROOF_4.value,
                          locations.ToontownLocationName.CASHBOT_PROOF_5.value]
                if bundleCount:
                    for checkNum in range(bundleCount):
                        toon.addCheckedLocation(ap_location_name_to_id(bundle[checkNum]))
                toon.b_promote(self.deptIndex)

                for rewardId in rewards:
                    toon.addResistanceMessage(rewardId)

    def getRandomResistanceRewardId(self):

        # Figure out if we want a toonup unite or a restock unite
        TYPES = [ResistanceChat.RESISTANCE_TOONUP, ResistanceChat.RESISTANCE_RESTOCK]
        typeToGive = random.choice(TYPES)
        if typeToGive == ResistanceChat.RESISTANCE_RESTOCK:
            restockItems = ResistanceChat.getItems(typeToGive)
            choice = restockItems[random.randint(3, 6)]
        else:
            choice = random.choice(ResistanceChat.getItems(typeToGive))
        return ResistanceChat.encodeId(typeToGive, choice)

    def exitVictory(self):
        self.__deleteBattleThreeObjects()

    ##### Epilogue state #####
    def enterEpilogue(self):
        DistributedBossCogAI.DistributedBossCogAI.enterEpilogue(self)

        # Tell the clients now what the reward Id will be.
        self.d_setRewardId(self.rewardId)

    def __restartCraneRoundTask(self, task):
        self.exitIntroduction()
        self.b_setState('PrepareBattleThree')
        self.b_setState('BattleThree')

    def __reviveToonLater(self, toon):
        taskMgr.doMethodLater(self.ruleset.REVIVE_TOONS_TIME, self.__reviveToon, self.uniqueName('revive-toon-' + str(toon.doId)), extraArgs=[toon])
        self.debug(doId=toon.doId, content='Reviving in %ss' % self.ruleset.REVIVE_TOONS_TIME)

    def __reviveToon(self, toon, task=None):

        if toon.getHp() > 0:
            return

        hpToGive = self.ruleset.REVIVE_TOONS_LAFF_PERCENTAGE * toon.getMaxHp()
        toon.b_setHp(hpToGive)
        self.sendUpdate('revivedToon', [toon.doId])
        self.debug(doId=toon.doId, content='Revived')

    def cancelReviveTasks(self):
        for avId in self.involvedToons:
            taskMgr.remove(self.uniqueName('revive-toon-' + str(avId)))

    def toonDied(self, toon):
        DistributedBossCogAI.DistributedBossCogAI.toonDied(self, toon)
        # If we want to revive toons, revive this toon later and don't do anything else past this point
        if self.ruleset.REVIVE_TOONS_UPON_DEATH and toon.doId in self.getInvolvedToonsNotSpectating():
            self.__reviveToonLater(toon)
            return

        # have all toons involved died?
        aliveToons = 0
        for toonId in self.getInvolvedToonsNotSpectating():
            toon = self.air.doId2do.get(toonId)
            if toon and toon.getHp() > 0:
                aliveToons += 1

        # Restart the crane round if toons are dead and we want to restart
        if self.ruleset.RESTART_CRANE_ROUND_ON_FAIL and not aliveToons:
            taskMgr.remove(self.uniqueName('times-up-task'))
            taskMgr.remove(self.uniqueName('post-times-up-task'))
            taskMgr.doMethodLater(10.0, self.__restartCraneRoundTask, self.uniqueName('failedCraneRound'))
            self.sendUpdate('announceCraneRestart', [])
            return

        # todo if all toons are dead get rid of them
        print("CASHBOTBOSSAI: todo boot all toons out back to the playground, they lost")

    # Given an attack code, return a death reason that corresponds with it.
    def getDeathReasonFromAttackCode(self, attackCode) -> DeathReason:

        return {
            ToontownGlobals.BossCogAreaAttack: DeathReason.CFO_JUMP,
            ToontownGlobals.BossCogSlowDirectedAttack: DeathReason.CFO_GEAR,
            ToontownGlobals.BossCogDirectedAttack: DeathReason.CFO_GEAR,
            ToontownGlobals.BossCogGearDirectedAttack: DeathReason.CFO_GEAR,
            ToontownGlobals.BossCogSwatLeft: DeathReason.CFO_SWAT,
            ToontownGlobals.BossCogSwatRight: DeathReason.CFO_SWAT,
            ToontownGlobals.BossCogElectricFence: DeathReason.CFO_RUNOVER,

            ToontownGlobals.BossCogGoonZap: DeathReason.CFO_GOON,
        }.get(attackCode, DeathReason.CFO)

    def getDeathReasonFromBattle(self) -> DeathReason:
        return DeathReason.BATTLING_CFO

    def d_updateGoonKilledBySafe(self, avId):
        self.sendUpdate('goonKilledBySafe', [avId])

    def d_updateUnstun(self, avId):
        self.sendUpdate('updateUnstun', [avId])