import math
import random
from operator import itemgetter

from direct.fsm import ClassicFSM
from direct.fsm import State
from direct.showbase.PythonUtil import clamp
from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import CollisionInvSphere, CollisionNode, CollisionSphere, NodePath, Vec3, Point3

from toontown.coghq import CraneLeagueGlobals
from toontown.coghq.CashbotBossComboTracker import CashbotBossComboTracker
from toontown.coghq.CraneLeagueGlobals import ScoreReason
from toontown.coghq.DistributedCashbotBossCraneAI import DistributedCashbotBossCraneAI
from toontown.coghq.DistributedCashbotBossHeavyCraneAI import DistributedCashbotBossHeavyCraneAI
from toontown.coghq.DistributedCashbotBossSafeAI import DistributedCashbotBossSafeAI
from toontown.coghq.DistributedCashbotBossSideCraneAI import DistributedCashbotBossSideCraneAI
from toontown.coghq.DistributedCashbotBossTreasureAI import DistributedCashbotBossTreasureAI
from toontown.minigame.DistributedMinigameAI import DistributedMinigameAI
from toontown.minigame.craning.CraneGamePracticeCheatAI import CraneGamePracticeCheatAI
from toontown.suit.DistributedCashbotBossGoonAI import DistributedCashbotBossGoonAI
from toontown.suit.DistributedCashbotBossStrippedAI import DistributedCashbotBossStrippedAI
from toontown.toon.DistributedToonAI import DistributedToonAI
from toontown.toonbase import ToontownGlobals


class DistributedCraneGameAI(DistributedMinigameAI):
    DESPERATION_MODE_ACTIVATE_THRESHOLD = 1800

    def __init__(self, air, minigameId):
        DistributedMinigameAI.__init__(self, air, minigameId)

        self.ruleset = CraneLeagueGlobals.CFORuleset()
        self.modifiers = []  # A list of CFORulesetModifierBase instances
        self.goonCache = ("Recent emerging side", 0) # Cache for goon spawn bad luck protection
        self.cranes = []
        self.safes = []
        self.goons = []
        self.treasures = {}
        self.grabbingTreasures = {}
        self.recycledTreasures = []
        self.boss = None

        # We need a scene to do the collision detection in.
        self.scene = NodePath('scene')

        self.toonsWon = False

        self.rollModsOnStart = False
        self.numModsWanted = 5

        self.customSpawnPositions = {}
        self.goonMinScale = 0.8
        self.goonMaxScale = 2.4

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

        # State tracking related to the overtime mechanic.
        self.overtimeWillHappen = True  # Setting this to True will cause the CFO to enter "overtime" mode when time runs out.
        self.currentlyInOvertime = False  # Only true when the game is currently in overtime.

        # Instances of "cheats" that can be interacted with to make the crane round behave a certain way.
        self.practiceCheatHandler: CraneGamePracticeCheatAI = CraneGamePracticeCheatAI(self)

    def generate(self):
        self.notify.debug("generate")
        self.__makeBoss()
        DistributedMinigameAI.generate(self)

    def announceGenerate(self):
        self.notify.debug("announceGenerate")

        # Until the proper setup is finished for coming into these, only the first toons are non spectators.
        # Everyone else will be a spectator.
        # When the group/party system is implemented, this can be deleted.
        #spectators = []
        #if len(self.getParticipants()) > 2:
        #    spectators = self.getParticipants()[2:]
        #self.b_setSpectators(spectators)

    def __makeBoss(self):
        self.__deleteBoss()

        self.boss = DistributedCashbotBossStrippedAI(self.air, self)
        self.boss.generateWithRequired(self.zoneId)
        self.d_setBossCogId()
        self.boss.reparentTo(self.scene)

        # And some solids to keep the goons constrained to our room.
        cn = CollisionNode('walls')
        cs = CollisionSphere(0, 0, 0, 13)
        cn.addSolid(cs)
        cs = CollisionInvSphere(0, 0, 0, 42)
        cn.addSolid(cs)
        self.boss.attachNewNode(cn)

    def __deleteBoss(self):
        if self.__bossExists():
            self.boss.cleanupBossBattle()
            self.boss.requestDelete()
        self.boss = None

    def __bossExists(self) -> bool:
        return self.boss is not None

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

        # Until the proper setup is finished for coming into these, only the first two toons are non spectators.
        # Everyone else will be a spectator.
        # When the group/party system is implemented, this can be deleted.
        #spectators = []
        #if len(self.getParticipants()) > 2:
        #    spectators = self.getParticipants()[2:]
        # self.b_setSpectators(spectators)

        self.setupRuleset()
        self.setupSpawnpoints()

    def setupRuleset(self):
        self.ruleset = CraneLeagueGlobals.CFORuleset()
        if self.getBoss() is not None:
            self.getBoss().setRuleset(self.ruleset)

        # Should we randomize some modifiers?
        if self.rollModsOnStart:
            self.rollRandomModifiers()

        self.applyModifiers()
        # Make sure they didn't do anything bad
        self.ruleset.validate()

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

    def clearObjectSpeedCaching(self):
        for safe in self.safes:
            safe.d_resetSpeedCaching()

        for goon in self.goons:
            goon.d_resetSpeedCaching()

    def __makeCraningObjects(self):

        # Generate all of the cranes.
        self.cranes.clear()
        ind = 0

        for _ in CraneLeagueGlobals.NORMAL_CRANE_POSHPR:
            crane = DistributedCashbotBossCraneAI(self.air, self, ind)
            crane.generateWithRequired(self.zoneId)
            self.cranes.append(crane)
            ind += 1

        # Generate the sidecranes if wanted
        if self.ruleset.WANT_SIDECRANES:
            for _ in CraneLeagueGlobals.SIDE_CRANE_POSHPR:
                crane = DistributedCashbotBossSideCraneAI(self.air, self, ind)
                crane.generateWithRequired(self.zoneId)
                self.cranes.append(crane)
                ind += 1

        # Generate the heavy cranes if wanted
        if self.ruleset.WANT_HEAVY_CRANES:
            for _ in CraneLeagueGlobals.HEAVY_CRANE_POSHPR:
                crane = DistributedCashbotBossHeavyCraneAI(self.air, self, ind)
                crane.generateWithRequired(self.zoneId)
                self.cranes.append(crane)
                ind += 1

        # And all of the safes.
        self.safes.clear()
        for index in range(min(self.ruleset.SAFES_TO_SPAWN, len(CraneLeagueGlobals.SAFE_POSHPR))):
            safe = DistributedCashbotBossSafeAI(self.air, self, index)
            safe.generateWithRequired(self.zoneId)
            self.safes.append(safe)

        self.goons.clear()
        return

    def __resetCraningObjects(self):
        for crane in self.cranes:
            crane.request('Free')

        for safe in self.safes:
            safe.request('Initial')

    def __deleteCraningObjects(self):
        for crane in self.cranes:
            crane.request('Off')
            crane.requestDelete()

        self.cranes.clear()

        for safe in self.safes:
            safe.request('Off')
            safe.requestDelete()
        self.safes.clear()

        for goon in self.goons:
            goon.request('Off')
            goon.requestDelete()
        self.goons.clear()

    # Call to listen for toon death events. Useful for catching deaths caused by DeathLink.
    def listenForToonDeaths(self):
        self.ignoreToonDeaths()
        for toon in self.getParticipatingToons():
            self.__listenForToonDeath(toon)

    # Ignore toon death events. We don't need to worry about toons dying in specific scenarios
    # Such as turn based battles as BattleBase handles that for us.
    def ignoreToonDeaths(self):
        for toon in self.getParticipants():
            self.__ignoreToonDeath(toon)

    def __listenForToonDeath(self, toon):
        self.accept(toon.getGoneSadMessage(), self.toonDied, [toon])

    def __ignoreToonDeath(self, avId):
        self.ignore(DistributedToonAI.getGoneSadMessageForAvId(avId))

    def toonDied(self, toon):
        self.resetCombo(toon.doId)
        self.sendUpdate('toonDied', [toon.doId])

        # If we are in overtime, we don't need to do anything else.
        if self.currentlyInOvertime:
            self.__checkOvertimeState()
            return

        # Toons are expected to die in overtime. Only penalize them if it is in the normal round.
        self.addScore(toon.doId, self.ruleset.POINTS_PENALTY_GO_SAD, reason=ScoreReason.WENT_SAD)

        # Add a task to revive the toon.
        taskMgr.doMethodLater(self.ruleset.REVIVE_TOONS_TIME, self.reviveToon,
                              self.uniqueName(f"reviveToon-{toon.doId}"), extraArgs=[toon.doId])

    def reviveToon(self, toonId: int) -> None:
        toon = self.air.getDo(toonId)
        if toon is None:
            return

        toon.b_setHp(int(self.ruleset.REVIVE_TOONS_LAFF_PERCENTAGE * toon.getMaxHp()))

        self.sendUpdate("revivedToon", [toonId])

    def d_updateCombo(self, avId, comboLength):
        self.sendUpdate('updateCombo', [avId, comboLength])

    def handleExitedAvatar(self, avId):
        taskMgr.remove(self.uniqueName(f"reviveToon-{avId}"))
        self.removeToon(avId)

        super().handleExitedAvatar(avId)

    def removeToon(self, avId):
        # The toon leaves the zone, either through disconnect, death,
        # or something else.  Tell all of the safes, cranes, and goons.
        for crane in self.cranes:
            crane.removeToon(avId)

        for safe in self.safes:
            safe.removeToon(avId)

        for goon in self.goons:
            goon.removeToon(avId)

    def initializeComboTrackers(self):
        self.cleanupComboTrackers()
        for avId in self.getParticipants():
            if avId in self.air.doId2do:
                self.comboTrackers[avId] = CashbotBossComboTracker(self, avId)

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
        """
        A toon wants to grab a certain treasure. Validates the treasure is valid to grab
        """

        # First, try to see if we can find the treasure that was grabbed.
        treasure = self.treasures.get(treasureId)
        if treasure is None:
            return

        # Now get the toon that wants to grab it.
        toon = simbase.air.getDo(avId)
        if toon is None:
            return

        # Are they allowed to take this treasure?
        if not treasure.validAvatar(toon):
            treasure.d_setReject()
            return

        del self.treasures[treasureId]
        treasure.d_setGrab(avId)  # Todo a lot of logic is in this method call. This is such bad design and should prob be refactored.
        self.grabbingTreasures[treasureId] = treasure

        # Wait a few seconds for the animation to play, then
        # recycle the treasure.
        taskMgr.doMethodLater(5, self.__recycleTreasure, treasure.uniqueName('recycleTreasure'), extraArgs=[treasure])

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
            return

        # Drop chance?
        if self.ruleset.GOON_TREASURE_DROP_CHANCE < 1.0:
            if random.random() > self.ruleset.GOON_TREASURE_DROP_CHANCE:
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

    def __chooseGoonEmergeSide(self) -> str:
        """
        Determines the next side for a goon to emerge from.
        To limit the amount of RNG present, we prevent goons from spawning from the same side over and over in a row.
        """

        if self.practiceCheatHandler.wantOpeningModifications:
            # Controlled goon spawning logic, activated through commands.
            # Evaluate the toon position and spawn a goon based on it.
            avId = self.avIdList[self.practiceCheatHandler.openingModificationsToonIndex]
            toon = self.air.doId2do.get(avId)
            pos = toon.getPos()[1]
            if pos < -315:
                return 'EmergeB'
            return 'EmergeA'

        # Default goon spawning logic.
        # Is it okay to pick a random side?
        if self.goonCache[1] < 2:
            return random.choice(['EmergeA', 'EmergeB'])

        # There's too many goons coming from a certain side. Pick the opposite one.
        if self.goonCache[0] == 'EmergeA':
            return 'EmergeB'
        return 'EmergeA'

    def makeGoon(self, side = None):

        self.goonMovementTime = globalClock.getFrameTime()

        # If a side wasn't provided, we want to generate one
        if side is None:
            side = self.__chooseGoonEmergeSide()

        # Updates goon cache
        if side == self.goonCache[0]:
            self.goonCache = (side, self.goonCache[1] + 1)
        else:
            self.goonCache = (side, 1)

        # Check if we can make a new goon
        if len(self.goons) >= self.getMaxGoons():
            return

        # Make a new goon
        goon = DistributedCashbotBossGoonAI(self.air, self)
        goon.generateWithRequired(self.zoneId)
        self.goons.append(goon)

        # Attributes for desperation mode goons
        goon_stun_time = 4
        goon_velocity = 8
        goon_hfov = 85
        goon_attack_radius = 16
        goon_strength = self.ruleset.MAX_GOON_DAMAGE + 10
        goon_scale = self.goonMaxScale + .3

        # If the battle isn't in desperation yet override the values to normal values
        if self.getBattleThreeTime() <= 1.0:
            goon_stun_time = self.progressValue(30, 8)
            goon_velocity = self.progressRandomValue(3, 7)
            goon_hfov = self.progressRandomValue(70, 80)
            goon_attack_radius = self.progressRandomValue(6, 15)
            goon_strength = int(self.progressRandomValue(self.ruleset.MIN_GOON_DAMAGE, self.ruleset.MAX_GOON_DAMAGE))
            goon_scale = self.progressRandomValue(self.goonMinScale, self.goonMaxScale, noRandom=self.practiceCheatHandler.wantMaxSizeGoons)

        # Apply multipliers if necessary
        goon_velocity *= self.ruleset.GOON_SPEED_MULTIPLIER

        # Apply attributes to the goon
        goon.STUN_TIME = goon_stun_time
        goon.b_setupGoon(velocity=goon_velocity, hFov=goon_hfov, attackRadius=goon_attack_radius,
                         strength=goon_strength, scale=goon_scale)
        goon.request(side)

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

    def stopGoons(self):
        taskName = self.uniqueName('NextGoon')
        taskMgr.remove(taskName)

    def doNextGoon(self, task):
        if not self.boss.isStunned():
            self.makeGoon()

        # How long to wait for the next goon?
        delayTime = self.progressValue(10, 2)
        if self.practiceCheatHandler.wantFasterGoonSpawns:
            delayTime = 4
        self.waitForNextGoon(delayTime)

    def progressValue(self, fromValue, toValue):
        if self.ruleset.TIMER_MODE:
            elapsed = globalClock.getFrameTime() - self.battleThreeStart
            t = elapsed / float(self.ruleset.TIMER_MODE_TIME_LIMIT)
        else:
            t0 = float(self.getBoss().bossDamage) / float(self.ruleset.CFO_MAX_HP)
            elapsed = globalClock.getFrameTime() - self.battleThreeStart
            t1 = elapsed / float(self.DESPERATION_MODE_ACTIVATE_THRESHOLD)
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
        duration = self.ruleset.TIMER_MODE_TIME_LIMIT if self.ruleset.TIMER_MODE else self.DESPERATION_MODE_ACTIVATE_THRESHOLD
        t1 = elapsed / float(duration)
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

        if self.isSpectating(toon.getDoId()):
            return

        toon.takeDamage(deduction)

    def getToonOutgoingMultiplier(self, avId):
        return 100

    def recordHit(self, damage, impact=0, craneId=-1, objId=0, isGoon=False):
        avId = self.air.getAvatarIdFromSender()
        crane = simbase.air.doId2do.get(craneId)
        if not self.validate(avId, avId in self.getParticipants(), 'recordHit from unknown avatar'):
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
            self.addScore(avId, self.ruleset.POINTS_IMPACT, reason=CraneLeagueGlobals.ScoreReason.FULL_IMPACT)
        self.addScore(avId, damage)

        comboTracker = self.comboTrackers[avId]
        comboTracker.incrementCombo((comboTracker.combo + 1.0) / 10.0 * damage)

        # The CFO has been defeated, proceed to Victory state
        if self.boss.bossDamage >= self.ruleset.CFO_MAX_HP:
            self.addScore(avId, self.ruleset.POINTS_KILLING_BLOW, CraneLeagueGlobals.ScoreReason.KILLING_BLOW)
            self.toonsWon = True
            self.gameFSM.request('victory')
            return

        # The CFO is already dizzy, OR the crane is None, so get outta here
        if self.boss.attackCode == ToontownGlobals.BossCogDizzy or not crane:
            return

        self.boss.stopHelmets()

        # Is the damage high enough to stun? or did a side crane hit a high impact hit?
        hitMeetsStunRequirements = self.boss.considerStun(crane, damage, impact)
        if hitMeetsStunRequirements:
            # A particularly good hit (when he's not already
            # dizzy) will make the boss dizzy for a little while.
            delayTime = self.progressValue(20, 5)
            self.boss.b_setAttackCode(ToontownGlobals.BossCogDizzy, delayTime=delayTime)
            isSideCrane = isinstance(crane, DistributedCashbotBossSideCraneAI)
            reason = CraneLeagueGlobals.ScoreReason.SIDE_STUN if isSideCrane else CraneLeagueGlobals.ScoreReason.STUN
            self.addScore(avId, crane.getPointsForStun(), reason=reason)
        else:

            if self.ruleset.CFO_FLINCHES_ON_HIT:
                self.boss.b_setAttackCode(ToontownGlobals.BossCogNoAttack)

            self.boss.waitForNextHelmet()

        # Now at the very end, if we have momentum mechanic on add some damage multiplier
        if self.ruleset.WANT_MOMENTUM_MECHANIC:
            self.increaseToonOutgoingMultiplier(avId, damage)

    def increaseToonOutgoingMultiplier(self, avId, n):
        """
        todo: implement
        """
        pass

    def addScore(self, avId: int, amount: int, reason: CraneLeagueGlobals.ScoreReason = CraneLeagueGlobals.ScoreReason.DEFAULT):

        if amount == 0:
            return
        if avId not in self.scoreDict:
            return

        self.scoreDict[avId] += amount
        self.d_addScore(avId, amount, reason)

        self.__awardUberBonusIfEligible(avId, amount, reason)

    def __awardUberBonusIfEligible(self, avId, amount, reason):
        if not self.ruleset.WANT_LOW_LAFF_BONUS:
            return

        if reason.ignore_uber_bonus():
            return

        toon = simbase.air.getDo(avId)
        if toon is None:
            return

        if toon.getHp() > self.ruleset.LOW_LAFF_BONUS_THRESHOLD:
            return

        uberAmount = int(self.ruleset.LOW_LAFF_BONUS * amount)
        if uberAmount == 0:
            return

        # Add additional score if uber bonus is on.
        self.addScore(avId, uberAmount, reason=CraneLeagueGlobals.ScoreReason.LOW_LAFF)


    def d_addScore(self, avId: int, amount: int, reason: CraneLeagueGlobals.ScoreReason = CraneLeagueGlobals.ScoreReason.DEFAULT):
        self.sendUpdate('addScore', [avId, amount, reason.to_astron()])

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
        taskMgr.remove(self.uniqueName("craneGameVictory"))
        self.battleThreeStart = globalClock.getFrameTime()

        self.setupRuleset()

        # Stop toon passive healing.
        for toon in self.getParticipatingToons():
            toon.stopToonUp()

        # Listen to death messages.
        self.listenForToonDeaths()

        # Start up the big boy.
        if not self.__bossExists():
            self.__makeBoss()
        self.boss.clearSafeHelmetCooldowns()
        self.__makeCraningObjects()
        self.__resetCraningObjects()
        self.boss.prepareBossForBattle()

        # Just in case we didn't pass through PrepareBattleThree state.
        self.setupSpawnpoints()
        self.d_restart()

        # Make four goons up front to keep things interesting from the
        # beginning.
        self.makeGoon(side='EmergeA')
        self.makeGoon(side='EmergeB')
        taskName = self.uniqueName('NextGoon')
        taskMgr.remove(taskName)
        taskMgr.doMethodLater(2, self.__doInitialGoons, taskName)

        self.initializeComboTrackers()

        # Fix all toon's HP that are present.
        for toon in self.getParticipatingToons():
            if self.ruleset.FORCE_MAX_LAFF:
                toon.b_setMaxHp(self.ruleset.FORCE_MAX_LAFF_AMOUNT)

            if self.ruleset.HEAL_TOONS_ON_START:
                toon.b_setHp(toon.getMaxHp())

        self.toonsWon = False
        taskMgr.remove(self.uniqueName('times-up-task'))
        taskMgr.remove(self.uniqueName('post-times-up-task'))
        # If timer mode is active, end the crane round later
        if self.ruleset.TIMER_MODE:
            taskMgr.doMethodLater(self.ruleset.TIMER_MODE_TIME_LIMIT, self.__timesUp, self.uniqueName('times-up-task'))

        if self.practiceCheatHandler.wantAimPractice:
            self.practiceCheatHandler.setupAimMode()

    # Called when we actually run out of time, simply tell the clients we ran out of time then handle it later
    def __timesUp(self, task=None):
        taskMgr.remove(self.uniqueName('times-up-task'))

        # If we aren't about to enter overtime, feel free to end the game here.
        if not self.overtimeWillHappen:
            self.toonsWon = False
            self.gameFSM.request('victory')
            return

        self.__enterOvertimeMode()

    def enableOvertime(self):
        """
        Marks this game in progress to enter overtime when time is up.
        """
        self.overtimeWillHappen = True
        self.d_setOvertime(True)

    def __enterOvertimeMode(self):
        """
        Adjust the state of the boss to force this game to find a winner with more extreme measures.
        """
        self.currentlyInOvertime = True
        self.d_setOvertime(True)

        self.startDrainingLaff(.5)

        self.ruleset.MAX_GOON_AMOUNT_END += 3  # Add 3 goons

        self.ruleset.DISABLE_SAFE_HELMETS = True  # Turn off helmets
        self.getBoss().stopHelmets()

        # Cut treasures in half
        self.ruleset.STRONG_TREASURE_HEAL_AMOUNT = int(math.ceil(self.ruleset.STRONG_TREASURE_HEAL_AMOUNT * .5))
        self.ruleset.AVERAGE_TREASURE_HEAL_AMOUNT = int(math.ceil(self.ruleset.AVERAGE_TREASURE_HEAL_AMOUNT * .5))
        self.ruleset.WEAK_TREASURE_HEAL_AMOUNT = int(math.ceil(self.ruleset.WEAK_TREASURE_HEAL_AMOUNT * .5))
        self.ruleset.REALLY_WEAK_TREASURE_HEAL_AMOUNT = int(math.ceil(self.ruleset.REALLY_WEAK_TREASURE_HEAL_AMOUNT * .5))
        self.ruleset.update_lists()

        self.__cancelReviveTasks()

    def __checkOvertimeState(self):
        """
        Analyze the state of the game right now. If all toons are dead, we can now end the game.
        """
        for toon in self.getParticipantsNotSpectating():
            if toon.getHp() > 0:
                return  # A toon is alive! Don't do anything.

        # No toon is alive. End the game.
        self.toonsWon = False
        self.gameFSM.request('victory')

    def __getLaffDrainTaskName(self):
        return self.uniqueName('laff-drain-task')

    def stopDrainingLaff(self):
        taskMgr.remove(self.__getLaffDrainTaskName())

    def startDrainingLaff(self, interval):
        taskMgr.add(self.__laffDrainTask, self.__getLaffDrainTaskName(), delay=interval)

    def __laffDrainTask(self, task):
        """
        Drain all present toons' laff by one.
        """
        for toon in self.getParticipantsNotSpectating():
            self.damageToon(toon, 1)
        self.__checkOvertimeState()  # Check if we are allowed to end the game. This will cancel the task for us if we choose to.
        return task.again

    def __doInitialGoons(self, task):
        self.makeGoon(side='EmergeA')
        self.makeGoon(side='EmergeB')
        self.goonCache = (None, 0)
        self.waitForNextGoon(10)
        self.__cancelReviveTasks()

    def __cancelReviveTasks(self):
        """
        Cleanup function to cancel any impending revives.
        """
        for toonId in self.getParticipants():
            taskMgr.remove(self.uniqueName(f"reviveToon-{toonId}"))

    def exitPlay(self):

        for comboTracker in self.comboTrackers.values():
            comboTracker.finishCombo()

        # Get rid of all the CFO objects.
        self.deleteAllTreasures()
        self.stopGoons()
        self.__resetCraningObjects()
        self.deleteAllTreasures()
        taskMgr.remove(self.uniqueName('times-up-task'))
        taskName = self.uniqueName('NextGoon')
        taskMgr.remove(taskName)

        self.stopDrainingLaff()
        self.currentlyInOvertime = False
        # self.overtimeWillHappen = False  # todo, uncomment when overtime logic is in place
        self.d_setOvertime(False)

        # Ignore death messages.
        self.ignoreToonDeaths()
        self.__cancelReviveTasks()

        for toon in self.getParticipatingToons():
            # Restart toon passive healing.
            toon.startToonUp(ToontownGlobals.PassiveHealFrequency)
            # Restore health.
            toon.b_setHp(toon.getMaxHp())

        if self.boss is not None:
            self.boss.cleanupBossBattle()

        craneTime = globalClock.getFrameTime()
        actualTime = craneTime - self.battleThreeStart
        timeToSend = 0.0 if self.ruleset.TIMER_MODE and not self.toonsWon else actualTime
        self.d_updateTimer(timeToSend)

    def __calculateTimeToSend(self):
        """
        Determine a proper time to send to the client to show on their timers.
        """
        craneTime = globalClock.getFrameTime()
        actualTime = craneTime - self.battleThreeStart
        return actualTime if not self.ruleset.TIMER_MODE else self.ruleset.TIMER_MODE_TIME_LIMIT - actualTime

    def d_updateTimer(self, time=None):
        if time is None:
            time = self.__calculateTimeToSend()
        self.sendUpdate('updateTimer', [time])

    def d_restart(self):
        self.sendUpdate('restart', [])

    def d_setOvertime(self, flag):
        self.sendUpdate('setOvertime', [flag])

    def enterVictory(self):
        victorId = max(self.scoreDict.items(), key=itemgetter(1))[0]
        self.sendUpdate("declareVictor", [victorId])
        taskMgr.doMethodLater(5, self.gameOver, self.uniqueName("craneGameVictory"), extraArgs=[])

    def exitVictory(self):
        taskMgr.remove(self.uniqueName("craneGameVictory"))

    def enterCleanup(self):
        self.notify.debug("enterCleanup")
        self.__deleteCraningObjects()
        self.__deleteBoss()
        self.gameFSM.request('inactive')

    def exitCleanup(self):
        pass

    def handleSpotStatusChanged(self, spotIndex, isPlayer):
        """
        Called when the leader changes a spot's status between Player and Spectator
        """
        if spotIndex >= len(self.avIdList):
            return
            
        avId = self.avIdList[spotIndex]
        currentSpectators = list(self.getSpectators())
        
        if isPlayer and avId in currentSpectators:
            currentSpectators.remove(avId)
        elif not isPlayer and avId not in currentSpectators:
            currentSpectators.append(avId)
            
        self.b_setSpectators(currentSpectators)
        # Broadcast the spot status change to all clients
        self.sendUpdate('updateSpotStatus', [spotIndex, isPlayer])
