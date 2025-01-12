import math
import random
from operator import itemgetter

from direct.fsm import ClassicFSM
from direct.fsm import State
from direct.showbase.PythonUtil import clamp
from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import CollisionInvSphere, CollisionNode, CollisionSphere, NodePath, Vec3, Point3

from toontown.coghq import CraneLeagueGlobals
from toontown.coghq.BossComboTrackerAI import BossComboTrackerAI
from toontown.coghq.CashbotBossComboTracker import CashbotBossComboTracker
from toontown.coghq.DistributedCashbotBossCraneAI import DistributedCashbotBossCraneAI
from toontown.coghq.DistributedCashbotBossHeavyCraneAI import DistributedCashbotBossHeavyCraneAI
from toontown.coghq.DistributedCashbotBossSafeAI import DistributedCashbotBossSafeAI
from toontown.coghq.DistributedCashbotBossSideCraneAI import DistributedCashbotBossSideCraneAI
from toontown.coghq.DistributedCashbotBossTreasureAI import DistributedCashbotBossTreasureAI
from toontown.minigame.DistributedMinigameAI import DistributedMinigameAI
from toontown.suit.DistributedCashbotBossGoonAI import DistributedCashbotBossGoonAI
from toontown.suit.DistributedCashbotBossStrippedAI import DistributedCashbotBossStrippedAI
from toontown.toon.DistributedToonAI import DistributedToonAI
from toontown.toonbase import ToontownGlobals


class DistributedCraneGameAI(DistributedMinigameAI):
    battleThreeDuration = 1800

    def __init__(self, air, minigameId):
        try:
            self.DistributedMinigameTemplateAI_initialized
            return
        except:
            self.DistributedMinigameTemplateAI_initialized = 1

        DistributedMinigameAI.__init__(self, air, minigameId)

        self.ruleset = CraneLeagueGlobals.CFORuleset()
        self.modifiers = []  # A list of CFORulesetModifierBase instances
        self.cranes = None
        self.safes = None
        self.goons = None
        self.treasures = {}
        self.grabbingTreasures = {}
        self.recycledTreasures = []

        # We need a scene to do the collision detection in.
        self.scene = NodePath('scene')

        self.wantCustomCraneSpawns = False
        self.wantAimPractice = False
        self.toonsWon = False

        # Controlled RNG parameters, True to enable, False to disable
        self.wantOpeningModifications = False
        self.openingModificationsToonIndex = 0
        self.wantMaxSizeGoons = False
        self.wantLiveGoonPractice = False
        self.wantNoStunning = False

        self.rollModsOnStart = False
        self.numModsWanted = 5

        self.customSpawnPositions = {}
        self.goonMinScale = 0.8
        self.goonMaxScale = 2.4
        self.safesWanted = 5

        self.comboTrackers = {}  # Maps avId -> CashbotBossComboTracker instance

        self.gameFSM = ClassicFSM.ClassicFSM('DistributedMinigameTemplateAI',
                               [
                                State.State('inactive',
                                            self.enterInactive,
                                            self.exitInactive,
                                            ['play']),
                                State.State('play',
                                            self.enterPlay,
                                            self.exitPlay,
                                            ['victory', 'cleanup']),
                                State.State('victory',
                                            self.enterVictory,
                                            self.exitVictory,
                                            ['cleanup']),
                                State.State('cleanup',
                                            self.enterCleanup,
                                            self.exitCleanup,
                                            ['inactive']),
                                ],
                               # Initial State
                               'inactive',
                               # Final State
                               'inactive',
                               )

        # Add our game ClassicFSM to the framework ClassicFSM
        self.addChildGameFSM(self.gameFSM)

    def generate(self):
        self.notify.debug("generate")

        self.boss = DistributedCashbotBossStrippedAI(self.air, self)
        self.boss.generateWithRequired(self.zoneId)
        self.boss.reparentTo(self.scene)

        # And some solids to keep the goons constrained to our room.
        cn = CollisionNode('walls')
        cs = CollisionSphere(0, 0, 0, 13)
        cn.addSolid(cs)
        cs = CollisionInvSphere(0, 0, 0, 42)
        cn.addSolid(cs)
        self.boss.attachNewNode(cn)

        DistributedMinigameAI.generate(self)

    # Disable is never called on the AI so we do not define one

    def delete(self):
        self.notify.debug("delete")
        del self.gameFSM
        DistributedMinigameAI.delete(self)

    # override some network message handlers
    def setGameReady(self):
        self.notify.debug("setGameReady")
        DistributedMinigameAI.setGameReady(self)
        # all of the players have checked in
        # they will now be shown the rules
        self.d_setBossCogId()

        self.__makeCraningObjects()
        self.__resetCraningObjects()

        self.setupRuleset()
        self.setupSpawnpoints()

    def setupRuleset(self):
        self.ruleset = CraneLeagueGlobals.CFORuleset()

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

    # Call to update the ruleset with the modifiers active, note calling more than once can cause unexpected behavior
    # if the ruleset doesn't fallback to an initial value, for example if a cfo hp increasing modifier is active and we
    # call this multiply times, his hp will be 1500 * 1.5 * 1.5 * 1.5 etc etc
    def applyModifiers(self, updateClient=False):
        for modifier in self.modifiers:
            modifier.apply(self.ruleset)

        if updateClient:
            self.d_setRawRuleset()

    # Any time you change the ruleset, you should call this to sync the clients
    def d_setRawRuleset(self):
        print((self.getRawRuleset()))
        self.sendUpdate('setRawRuleset', [self.getRawRuleset()])

    def __getRawModifierList(self):
        mods = []
        for modifier in self.modifiers:
            mods.append(modifier.asStruct())

        return mods

    def d_setModifiers(self):
        self.sendUpdate('setModifiers', [self.__getRawModifierList()])

    def rollRandomModifiers(self):
        tierLeftBound = self.ruleset.MODIFIER_TIER_RANGE[0]
        tierRightBound = self.ruleset.MODIFIER_TIER_RANGE[1]
        pool = [c(random.randint(tierLeftBound, tierRightBound)) for c in
                CraneLeagueGlobals.NON_SPECIAL_MODIFIER_CLASSES]
        random.shuffle(pool)

        self.modifiers = [pool.pop() for _ in range(self.numModsWanted)]

        # If we roll a % roll, go ahead and make this a special cfo
        # Doing this last also ensures any rules that the special mod needs to set override
        if random.randint(0, 99) < CraneLeagueGlobals.SPECIAL_MODIFIER_CHANCE:
            cls = random.choice(CraneLeagueGlobals.SPECIAL_MODIFIER_CLASSES)
            tier = random.randint(tierLeftBound, tierRightBound)
            mod_instance = cls(tier)
            self.modifiers.append(mod_instance)

    def setGameStart(self, timestamp):
        self.notify.debug("setGameStart")
        # base class will cause gameFSM to enter initial state
        DistributedMinigameAI.setGameStart(self, timestamp)
        # all of the players are ready to start playing the game
        # transition to the appropriate ClassicFSM state
        self.gameFSM.request('play')

    def setGameAbort(self):
        self.notify.debug("setGameAbort")
        # this is called when the minigame is unexpectedly
        # ended (a player got disconnected, etc.)
        if self.gameFSM.getCurrentState():
            self.gameFSM.request('cleanup')
        DistributedMinigameAI.setGameAbort(self)

    def gameOver(self):
        self.notify.debug("gameOver")
        # call this when the game is done
        # clean things up in this class
        self.gameFSM.request('cleanup')
        # tell the base class to wrap things up
        DistributedMinigameAI.gameOver(self)

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

    def clearObjectSpeedCaching(self):
        if self.safes:
            for safe in self.safes:
                safe.d_resetSpeedCaching()

        if self.goons:
            for goon in self.goons:
                goon.d_resetSpeedCaching()

    def __makeCraningObjects(self):
        if self.cranes is None:
            # Generate all of the cranes.
            self.cranes = []
            ind = 0

            self.debug(content='Generating %s normal cranes' % len(CraneLeagueGlobals.NORMAL_CRANE_POSHPR))
            for _ in CraneLeagueGlobals.NORMAL_CRANE_POSHPR:
                crane = DistributedCashbotBossCraneAI(self.air, self, ind)
                crane.generateWithRequired(self.zoneId)
                self.cranes.append(crane)
                ind += 1

            # Generate the sidecranes if wanted
            if self.ruleset.WANT_SIDECRANES:
                self.debug(content='Generating %s sidecranes' % len(CraneLeagueGlobals.SIDE_CRANE_POSHPR))
                for _ in CraneLeagueGlobals.SIDE_CRANE_POSHPR:
                    crane = DistributedCashbotBossSideCraneAI(self.air, self, ind)
                    crane.generateWithRequired(self.zoneId)
                    self.cranes.append(crane)
                    ind += 1

            # Generate the heavy cranes if wanted
            if self.ruleset.WANT_HEAVY_CRANES:
                self.debug(content='Generating %s heavy cranes' % len(CraneLeagueGlobals.HEAVY_CRANE_POSHPR))
                for _ in CraneLeagueGlobals.HEAVY_CRANE_POSHPR:
                    crane = DistributedCashbotBossHeavyCraneAI(self.air, self, ind)
                    crane.generateWithRequired(self.zoneId)
                    self.cranes.append(crane)
                    ind += 1

        if self.safes is None:
            # And all of the safes.
            self.safes = []
            for index in range(min(self.ruleset.SAFES_TO_SPAWN, len(CraneLeagueGlobals.SAFE_POSHPR))):
                safe = DistributedCashbotBossSafeAI(self.air, self, index)
                safe.generateWithRequired(self.zoneId)
                self.safes.append(safe)

        if self.goons is None:
            # We don't actually make the goons right now, but we make
            # a place to hold them.
            self.goons = []
        return

    def __resetCraningObjects(self):
        if self.cranes is not None:
            for crane in self.cranes:
                crane.request('Free')

        if self.safes is not None:
            for safe in self.safes:
                safe.request('Initial')

    def __deleteCraningObjects(self):
        if self.cranes is not None:
            for crane in self.cranes:
                crane.request('Off')
                crane.requestDelete()

            self.cranes = None
        if self.safes is not None:
            for safe in self.safes:
                safe.request('Off')
                safe.requestDelete()

            self.safes = None
        if self.goons is not None:
            for goon in self.goons:
                goon.request('Off')
                goon.requestDelete()

            self.goons = None

    # Call to listen for toon death events. Useful for catching deaths caused by DeathLink.
    def listenForToonDeaths(self):
        self.ignoreToonDeaths()
        for avId in self.avIdList:
            toon = self.air.doId2do.get(avId)
            if toon is None:
                continue
            self.__listenForToonDeath(toon)

    # Ignore toon death events. We don't need to worry about toons dying in specific scenarios
    # Such as turn based battles as BattleBase handles that for us.
    def ignoreToonDeaths(self):
        for toon in self.avIdList:
            self.__ignoreToonDeath(toon)

    def __listenForToonDeath(self, toon):
        self.accept(toon.getGoneSadMessage(), self.toonDied, [toon])

    def __ignoreToonDeath(self, avId):
        self.ignore(DistributedToonAI.getGoneSadMessageForAvId(avId))

    def toonDied(self, toon):
        self.resetCombo(toon.doId)
        self.sendUpdate('toonDied', [toon.doId])

        # Reset the toon's combo
        ct = self.comboTrackers.get(toon.doId)
        if ct:
            ct.resetCombo()

        # Add a task to revive the toon.
        taskMgr.doMethodLater(5, self.reviveToon, self.uniqueName(f"reviveToon-{toon.doId}"), extraArgs=[toon.doId])

    def reviveToon(self, toonId: int) -> None:
        toon = self.air.getDo(toonId)
        if toon is None:
            return

        toon.b_setHp(1)

        self.sendUpdate("revivedToon", [toonId])

    def d_updateCombo(self, avId, comboLength):
        self.sendUpdate('updateCombo', [avId, comboLength])

    def d_awardCombo(self, avId, comboLength, amount):
        self.sendUpdate('awardCombo', [avId, comboLength, amount])

    def d_updateGoonKilledBySafe(self, avId):
        self.sendUpdate('goonKilledBySafe', [avId])

    def d_updateUnstun(self, avId):
        self.sendUpdate('updateUnstun', [avId])

    def handleExitedAvatar(self, avId):
        taskMgr.remove(self.uniqueName(f"reviveToon-{avId}"))
        self.removeToon(avId)

        super().handleExitedAvatar(avId)

    def removeToon(self, avId):
        # The toon leaves the zone, either through disconnect, death,
        # or something else.  Tell all of the safes, cranes, and goons.

        if self.cranes is not None:
            for crane in self.cranes:
                crane.removeToon(avId)

        if self.safes is not None:
            for safe in self.safes:
                safe.removeToon(avId)

        if self.goons is not None:
            for goon in self.goons:
                goon.removeToon(avId)

    def initializeComboTrackers(self):
        self.cleanupComboTrackers()
        for avId in self.avIdList:
            if avId in self.air.doId2do:
                self.comboTrackers[avId] = BossComboTrackerAI(self, avId)

    def incrementCombo(self, avId, amount):
        tracker = self.comboTrackers.get(avId)
        if not tracker:
            return

        tracker.incrementCombo(amount)

    def resetCombo(self, avId):
        tracker = self.comboTrackers.get(avId)
        if not tracker:
            return

        tracker.resetCombo()

    def getComboLength(self, avId):
        tracker = self.comboTrackers.get(avId)
        if not tracker:
            return 0

        return tracker.combo

    def getComboAmount(self, avId):
        tracker = self.comboTrackers.get(avId)
        if not tracker:
            return 0

        return tracker.pointBonus

    def cleanupComboTrackers(self):
        for comboTracker in self.comboTrackers.values():
            comboTracker.cleanup()

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
                taskMgr.doMethodLater(5, self.__recycleTreasure, treasure.uniqueName('recycleTreasure'),
                                      extraArgs=[treasure])
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

    def makeTreasure(self, goon):
        # Places a treasure, as pooped out by the given goon.  We
        # place the treasure at the goon's current position, or at
        # least at the beginning of its current path.  Actually, we
        # ignore Z, and always place the treasure at Z == 0,
        # presumably the ground.

        # Too many treasures on the field?
        if len(self.treasures) >= self.ruleset.MAX_TREASURE_AMOUNT:
            self.debug(doId=goon.doId,
                       content='Not spawning treasure, already %s present' % self.ruleset.MAX_TREASURE_AMOUNT)
            return

        # Drop chance?
        if self.ruleset.GOON_TREASURE_DROP_CHANCE < 1.0:
            r = random.random()
            self.debug(doId=goon.doId, content='Rolling for treasure drop, need > %s, got %s' % (
            self.ruleset.GOON_TREASURE_DROP_CHANCE, r))
            if r > self.ruleset.GOON_TREASURE_DROP_CHANCE:
                return

        # The BossCog acts like a treasure planner as far as the
        # treasure is concerned.
        pos = goon.getPos(self.boss)

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

        fpos = self.scene.getRelativePoint(self.boss, Point3(v[0] + dx, v[1] + dy, 0))

        # Find an index based on the goon strength we should use
        treasureHealIndex = 1.0 * (goon.strength - self.ruleset.MIN_GOON_DAMAGE) / (
                    self.ruleset.MAX_GOON_DAMAGE - self.ruleset.MIN_GOON_DAMAGE)
        treasureHealIndex *= len(self.ruleset.GOON_HEALS)
        treasureHealIndex = int(clamp(treasureHealIndex, 0, len(self.ruleset.GOON_HEALS) - 1))
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
        else:
            # Create a new treasure object
            treasure = DistributedCashbotBossTreasureAI(self.air, self, goon, style, fpos[0], fpos[1], 0)
            treasure.generateWithRequired(self.zoneId)
        treasure.healAmount = healAmount
        self.treasures[treasure.doId] = treasure

    def getMaxGoons(self):
        return self.progressValue(self.ruleset.MAX_GOON_AMOUNT_START, self.ruleset.MAX_GOON_AMOUNT_END)

    def makeGoon(self, side=None):
        self.goonMovementTime = globalClock.getFrameTime()
        if side == None:
            if not self.wantOpeningModifications:
                side = random.choice(['EmergeA', 'EmergeB'])
            else:
                avId = self.avIdList[self.openingModificationsToonIndex]
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
            goon = DistributedCashbotBossGoonAI(self.air, self)
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
        goon.b_setupGoon(velocity=goon_velocity, hFov=goon_hfov, attackRadius=goon_attack_radius,
                         strength=goon_strength, scale=goon_scale)
        goon.request(side)

        self.debug(doId=goon.doId,
                   content='Spawning on %s, stun=%.2f, vel=%.2f, hfov=%.2f, attRadius=%.2f, str=%s, scale=%.2f' % (
                   side, goon_stun_time, goon_velocity, goon_hfov, goon_attack_radius, goon_strength, goon_scale))

    def __chooseOldGoon(self):
        # Walks through the list of goons managed by the boss to see
        # if any of them have recently been deleted and can be
        # recycled.

        for goon in self.goons:
            if goon.state == 'Off':
                return goon

    def waitForNextGoon(self, delayTime):
        taskName = self.uniqueName('NextGoon')
        taskMgr.remove(taskName)
        taskMgr.doMethodLater(delayTime, self.doNextGoon, taskName)
        self.debug(content='Spawning goon in %.2fs' % delayTime)

    def stopGoons(self):
        taskName = self.uniqueName('NextGoon')
        taskMgr.remove(taskName)

    def doNextGoon(self, task):
        if not self.boss.isStunned():
            self.makeGoon()

        # How long to wait for the next goon?
        delayTime = self.progressValue(10, 2)
        self.waitForNextGoon(delayTime)

    def progressValue(self, fromValue, toValue):
        t0 = float(self.boss.bossDamage) / float(self.ruleset.CFO_MAX_HP)
        elapsed = globalClock.getFrameTime() - self.battleThreeStart
        t1 = elapsed / float(self.battleThreeDuration)
        t = max(t0, t1)
        return fromValue + (toValue - fromValue) * min(t, 1)

    def progressRandomValue(self, fromValue, toValue, radius=0.2, noRandom=False):
        t = self.progressValue(0, 1)
        radius = radius * (1.0 - abs(t - 0.5) * 2.0)
        if noRandom:
            t += radius
        else:
            t += radius * random.uniform(-1, 1)
        t = max(min(t, 1.0), 0.0)
        return fromValue + (toValue - fromValue) * t

    def getBattleThreeTime(self):
        elapsed = globalClock.getFrameTime() - self.battleThreeStart
        t1 = elapsed / float(self.battleThreeDuration)
        return t1

    def setupSpawnpoints(self):
        self.toonSpawnpointOrder = [i for i in range(8)]
        if self.ruleset.RANDOM_SPAWN_POSITIONS:
            random.shuffle(self.toonSpawnpointOrder)
        self.d_setToonSpawnpointOrder()

    def d_setToonSpawnpointOrder(self):
        self.sendUpdate('setToonSpawnpoints', [self.toonSpawnpointOrder])

    def getRawRuleset(self):
        return self.ruleset.asStruct()

    def d_setBossCogId(self) -> None:
        self.sendUpdate("setBossCogId", [self.boss.getDoId()])

    def getBoss(self):
        return self.boss

    def damageToon(self, toon, deduction):
        if toon.getHp() <= 0:
            return

        toon.takeDamage(deduction)

    def getToonOutgoingMultiplier(self, avId):
        n = self.toonDmgMultipliers.get(avId)
        if not n:
            n = 100
            self.toonDmgMultipliers[avId] = n

        return n

    def recordHit(self, damage, impact=0, craneId=-1, objId=0, isGoon=False):
        avId = self.air.getAvatarIdFromSender()
        crane = simbase.air.doId2do.get(craneId)
        if not self.validate(avId, avId in self.avIdList, 'recordHit from unknown avatar'):
            return

        # Momentum mechanic?
        if self.ruleset.WANT_MOMENTUM_MECHANIC:
            damage *= (self.getToonOutgoingMultiplier(avId) / 100.0)
            print(('multiplying damage by ' + str(
                self.getToonOutgoingMultiplier(avId) / 100.0) + ' damage is now ' + str(damage)))

        # Record a successful hit in battle three.
        self.boss.b_setBossDamage(self.boss.bossDamage + damage, avId=avId, objId=objId, isGoon=isGoon)

        # Award bonus points for hits with maximum impact
        if impact == 1.0:
            self.d_updateMaxImpactHits(avId)
        self.d_updateDamageDealt(avId, damage)

        comboTracker = self.comboTrackers[avId]
        comboTracker.incrementCombo((comboTracker.combo + 1.0) / 10.0 * damage)

        self.debug(doId=avId, content='Damaged for %s with impact: %.2f' % (damage, impact))

        # The CFO has been defeated, proceed to Victory state
        if self.boss.bossDamage >= self.ruleset.CFO_MAX_HP:
            self.d_killingBlowDealt(avId)
            self.toonsWon = True
            self.gameFSM.request('victory')
            return

        # The CFO is already dizzy, OR the crane is None, so get outta here
        if self.boss.attackCode == ToontownGlobals.BossCogDizzy or not crane:
            return

        self.boss.stopHelmets()

        # Is the damage high enough to stun? or did a side crane hit a high impact hit?
        hitMeetsStunRequirements = self.boss.considerStun(crane, damage, impact)
        if self.wantNoStunning:
            hitMeetsStunRequirements = False
        if hitMeetsStunRequirements:
            # A particularly good hit (when he's not already
            # dizzy) will make the boss dizzy for a little while.
            delayTime = self.progressValue(20, 5)
            self.boss.b_setAttackCode(ToontownGlobals.BossCogDizzy, delayTime=delayTime)
            self.d_updateStunCount(avId, craneId)
        else:

            if self.ruleset.CFO_FLINCHES_ON_HIT:
                self.boss.b_setAttackCode(ToontownGlobals.BossCogNoAttack)

            self.boss.waitForNextHelmet()

        # Now at the very end, if we have momentum mechanic on add some damage multiplier
        if self.ruleset.WANT_MOMENTUM_MECHANIC:
            self.increaseToonOutgoingMultiplier(avId, damage)

    def increaseToonOutgoingMultiplier(self, avId, n):
        # Makes sure theres something in the dict
        old = self.getToonOutgoingMultiplier(avId)
        self.toonDmgMultipliers[avId] = old + n
        print(("avId now does +" + str(old + n) + "% damage"))

    def d_killingBlowDealt(self, avId):
        self.scoreDict[avId] += self.ruleset.POINTS_KILLING_BLOW
        self.sendUpdate('killingBlowDealt', [avId])

    def d_updateDamageDealt(self, avId, damageDealt):
        self.scoreDict[avId] += damageDealt
        self.sendUpdate('updateDamageDealt', [avId, damageDealt])

    def d_updateStunCount(self, avId, craneId):
        crane = self.air.doId2do.get(craneId)
        if crane:
            self.scoreDict[avId] += crane.getPointsForStun()
        self.sendUpdate('updateStunCount', [avId, craneId])

    def d_updateGoonsStomped(self, avId):
        self.scoreDict[avId] += self.ruleset.POINTS_GOON_STOMP
        self.sendUpdate('updateGoonsStomped', [avId])

    # call with 10 when we take a safe off, -20 when we put a safe on
    def d_updateSafePoints(self, avId, amount):
        self.scoreDict[avId] += amount
        self.sendUpdate('updateSafePoints', [avId, amount])

    def d_updateMaxImpactHits(self, avId):
        self.scoreDict[avId] += self.ruleset.POINTS_IMPACT
        self.sendUpdate('updateMaxImpactHits', [avId])

    def d_updateLowImpactHits(self, avId):
        self.scoreDict[avId] += self.ruleset.POINTS_PENALTY_SANDBAG
        self.sendUpdate('updateLowImpactHits', [avId])

    def d_setCraneSpawn(self, want, spawn, toonId):
        self.sendUpdate('setCraneSpawn', [want, spawn, toonId])

    """
    FSM states
    """

    def enterInactive(self):
        self.notify.debug("enterInactive")

    def exitInactive(self):
        pass

    def enterPlay(self):
        self.notify.debug("enterPlay")

        self.battleThreeStart = globalClock.getFrameTime()

        # Stop toon passive healing.
        for avId in self.avIdList:
            av = self.air.getDo(avId)
            if av:
                av.stopToonUp()

        # Listen to death messages.
        self.listenForToonDeaths()

        # Start up the big boy.
        self.boss.prepareBossForBattle()

        # Just in case we didn't pass through PrepareBattleThree state.
        self.setupSpawnpoints()

        # Make four goons up front to keep things interesting from the
        # beginning.
        self.makeGoon(side='EmergeA')
        self.makeGoon(side='EmergeB')
        taskName = self.uniqueName('NextGoon')
        taskMgr.remove(taskName)
        taskMgr.doMethodLater(2, self.__doInitialGoons, taskName)

        self.oldMaxLaffs = {}
        self.toonDmgMultipliers = {}

        taskMgr.remove(self.uniqueName('failedCraneRound'))

        for comboTracker in self.comboTrackers.values():
            comboTracker.cleanup()

        # heal all toons and setup a combo tracker for them
        for avId in self.avIdList:
            if avId in self.air.doId2do:
                self.comboTrackers[avId] = CashbotBossComboTracker(self, avId)
                av = self.air.doId2do[avId]

                if self.ruleset.FORCE_MAX_LAFF:
                    self.oldMaxLaffs[avId] = av.getMaxHp()
                    av.b_setMaxHp(self.ruleset.FORCE_MAX_LAFF_AMOUNT)
                    self.debug(content='Forcing max laff to %s' % self.ruleset.FORCE_MAX_LAFF_AMOUNT)

                if self.ruleset.HEAL_TOONS_ON_START:
                    av.b_setHp(av.getMaxHp())
                    self.debug(content='Healing all toons')

        self.toonsWon = False
        taskMgr.remove(self.uniqueName('times-up-task'))
        taskMgr.remove(self.uniqueName('post-times-up-task'))

    def __doInitialGoons(self, task):
        self.makeGoon(side='EmergeA')
        self.makeGoon(side='EmergeB')
        self.waitForNextGoon(10)

    def exitPlay(self):
        self.deleteAllTreasures()
        self.stopGoons()
        self.__resetCraningObjects()
        self.deleteAllTreasures()
        taskName = self.uniqueName('NextGoon')
        taskMgr.remove(taskName)

        # Ignore death messages.
        self.ignoreToonDeaths()

        for avId in self.avIdList:
            taskMgr.remove(self.uniqueName(f"reviveToon-{avId}"))

            av = self.air.doId2do.get(avId)
            if av:
                # Restore old max HPs
                if avId in self.oldMaxLaffs:
                    av.b_setMaxHp(self.oldMaxLaffs[avId])

                # Restart toon passive healing.
                av.startToonUp(ToontownGlobals.PassiveHealFrequency)

                # Restore health.
                av.b_setHp(av.getMaxHp())

        if self.boss is not None:
            self.boss.cleanupBossBattle()

        craneTime = globalClock.getFrameTime()
        actualTime = craneTime - self.battleThreeStart
        timeToSend = 0.0 if self.ruleset.TIMER_MODE and not self.toonsWon else actualTime
        self.debug(content='Crane round over in %ss' % timeToSend)
        self.d_updateTimer(timeToSend)

    def d_updateTimer(self, time):
        self.sendUpdate('updateTimer', [time])

    def enterVictory(self):
        victorId = max(self.scoreDict.items(), key=itemgetter(1))[0]
        self.sendUpdate("declareVictor", [victorId])
        taskMgr.doMethodLater(5, self.gameOver, self.uniqueName("craneGameVictory"), extraArgs=[])

    def exitVictory(self):
        taskMgr.remove(self.uniqueName("craneGameVictory"))

    def enterCleanup(self):
        self.notify.debug("enterCleanup")
        self.__deleteCraningObjects()

        self.boss.requestDelete()
        del self.boss

        self.gameFSM.request('inactive')

    def exitCleanup(self):
        pass
