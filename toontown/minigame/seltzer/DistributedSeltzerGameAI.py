from operator import itemgetter
from typing import Optional

from direct.fsm.ClassicFSM import ClassicFSM
from direct.fsm.State import State
from direct.task.TaskManagerGlobal import taskMgr

from toontown.coghq import SeltzerLeagueGlobals
from toontown.coghq.BossComboTrackerAI import BossComboTrackerAI
from toontown.coghq.DistributedBanquetTableAI import DistributedBanquetTableAI
from toontown.coghq.DistributedFoodBeltAI import DistributedFoodBeltAI
from toontown.coghq.DistributedGolfSpotAI import DistributedGolfSpotAI
from toontown.minigame.DistributedMinigameAI import DistributedMinigameAI
from toontown.suit.DistributedBossbotBossStrippedAI import DistributedBossbotBossStrippedAI
from toontown.toon.DistributedToonAI import DistributedToonAI
from toontown.toonbase import ToontownGlobals


class DistributedSeltzerGameAI(DistributedMinigameAI):
    battleFourDuration = 1800

    def __init__(self, air, minigameId):
        super().__init__(air, minigameId)

        self.ruleset = SeltzerLeagueGlobals.CEORuleset()

        self.boss: Optional[DistributedBossbotBossStrippedAI] = None

        self.tables = []
        self.foodBelts = []
        self.golfSpots = []
        self.toonupsGranted = []

        self.comboTrackers = {}

        self.gameFSM = ClassicFSM(self.__class__.__name__,
                                  [
                                      State('inactive',
                                            self.enterInactive,
                                            self.exitInactive,
                                            ['play']),
                                      State('play',
                                            self.enterPlay,
                                            self.exitPlay,
                                            ['victory', 'cleanup']),
                                      State('victory',
                                            self.enterVictory,
                                            self.exitVictory,
                                            ['cleanup']),
                                      State('cleanup',
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

        self.boss = DistributedBossbotBossStrippedAI(self.air, self)
        self.boss.generateWithRequired(self.zoneId)

        super().generate()

    def cleanup(self) -> None:
        self.deleteBanquetTables()
        self.deleteFoodBelts()

        if self.boss is not None:
            self.boss.requestDelete()
            self.boss = None

    # Disable is never called on the AI so we do not define one

    def delete(self):
        self.notify.debug("delete")
        del self.gameFSM
        super().delete()

    # override some network message handlers
    def setGameReady(self):
        self.notify.debug("setGameReady")
        super().setGameReady()
        # all of the players have checked in
        # they will now be shown the rules
        self.d_setBossCogId()
        self.createFoodBelts()
        self.createBanquetTables()

    def setGameStart(self, timestamp):
        self.notify.debug("setGameStart")
        # base class will cause gameFSM to enter initial state
        super().setGameStart(timestamp)
        # all of the players are ready to start playing the game
        # transition to the appropriate ClassicFSM state
        self.gameFSM.request('play')

    def setGameAbort(self):
        self.notify.debug("setGameAbort")
        # this is called when the minigame is unexpectedly
        # ended (a player got disconnected, etc.)
        if self.gameFSM.getCurrentState():
            self.gameFSM.request('cleanup')
        self.cleanup()
        super().setGameAbort()

    def gameOver(self):
        self.notify.debug("gameOver")
        # call this when the game is done
        # clean things up in this class
        self.gameFSM.request('cleanup')
        # tell the base class to wrap things up
        super().gameOver()

    def enterInactive(self):
        self.notify.debug("enterInactive")

    def exitInactive(self):
        pass

    def enterPlay(self):
        self.notify.debug("enterPlay")

        self.battleFourStart = globalClock.getFrameTime()

        # Start up the big guy.
        self.boss.prepareBossForBattle()

        for avId in self.avIdList:
            av = self.air.getDo(avId)
            if av:
                # Stop toon passive healing.
                av.stopToonUp()

                # Give the toon a nice heal.
                av.b_setHp(av.getMaxHp())

        self.listenForToonDeaths()
        self.setupBattleFourObjects()
        self.initializeComboTrackers()

    def exitPlay(self):
        for belt in self.foodBelts:
            belt.goInactive()

        if self.boss is not None:
            self.boss.cleanupBossBattle()

        for avId in self.avIdList:
            av = self.air.getDo(avId)
            if av:
                # Restart toon passive healing.
                av.startToonUp(ToontownGlobals.PassiveHealFrequency)

        self.ignoreToonDeaths()

        pieTime = globalClock.getFrameTime()
        actualTime = pieTime - self.battleFourStart
        self.d_updateTimer(actualTime)

    def enterVictory(self):
        victorId = max(self.scoreDict.items(), key=itemgetter(1))[0]
        self.sendUpdate("declareVictor", [victorId])
        taskMgr.doMethodLater(10, self.gameOver, self.uniqueName("seltzerGameVictory"), extraArgs=[])

    def exitVictory(self):
        taskMgr.remove(self.uniqueName("seltzerGameVictory"))

    def enterCleanup(self):
        self.notify.debug("enterCleanup")
        self.cleanup()
        self.gameFSM.request('inactive')

    def exitCleanup(self):
        pass

    """
    yeah
    """

    def createFoodBelts(self):
        if self.foodBelts:
            return
        for i in range(2):
            newBelt = DistributedFoodBeltAI(self.air, self, i)
            self.foodBelts.append(newBelt)
            newBelt.generateWithRequired(self.zoneId)

    def deleteFoodBelts(self):
        for belt in self.foodBelts:
            belt.requestDelete()

        self.foodBelts = []

    def createBanquetTables(self):
        if self.tables:
            return
        for i in range(self.ruleset.NUM_TABLES):
            newTable = DistributedBanquetTableAI(self.air, self, i, 0, 0)
            self.tables.append(newTable)
            newTable.generateWithRequired(self.zoneId)

    def deleteBanquetTables(self):
        for table in self.tables:
            table.requestDelete()

        self.tables = []

    def createGolfSpots(self):
        if self.golfSpots:
            return
        for i in range(self.ruleset.NUM_GOLF_SPOTS):
            newGolfSpot = DistributedGolfSpotAI(self.air, self, i)
            self.golfSpots.append(newGolfSpot)
            newGolfSpot.generateWithRequired(self.zoneId)
            newGolfSpot.forceFree()

    def deleteGolfSpots(self):
        for spot in self.golfSpots:
            spot.requestDelete()

        self.golfSpots = []

    def setupBattleFourObjects(self):
        if not self.tables:
            self.createBanquetTables()
        for table in self.tables:
            table.goFree()

        if not self.golfSpots:
            self.createGolfSpots()
        self.createFoodBelts()
        for belt in self.foodBelts:
            belt.goToonup()

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

    def cleanupComboTrackers(self):
        for comboTracker in self.comboTrackers.values():
            comboTracker.cleanup()

    def d_setBossCogId(self) -> None:
        self.sendUpdate("setBossCogId", [self.boss.getDoId()])

    def d_damageDealt(self, avId, dmg):
        self.scoreDict[avId] += dmg
        self.sendUpdate('updateDamageDealt', [avId, dmg])

    def d_stunBonus(self, avId, points):
        self.scoreDict[avId] += points
        self.sendUpdate('updateStunCount', [avId, points])

    def d_avHealed(self, avId, hp):
        self.scoreDict[avId] += hp
        self.sendUpdate('avHealed', [avId, hp])

    def d_updateTimer(self, time):
        self.sendUpdate('updateTimer', [time])

    def getBattleFourTime(self):
        elapsed = globalClock.getFrameTime() - self.battleFourStart
        t1 = elapsed / float(self.battleFourDuration)
        return t1

    def damageToon(self, toon, deduction):
        if toon.getHp() <= 0:
            return

        toon.takeDamage(deduction)

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

    def setupRuleset(self):
        self.ruleset = SeltzerLeagueGlobals.CEORuleset()
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

    def requestGetToonup(self, beltIndex, toonupIndex, toonupNum):
        avId = self.air.getAvatarIdFromSender()
        toon = self.air.doId2do.get(avId)
        if toon is None or toon.hp <= 0:
            return

        self.toonupsGranted.insert(0, (beltIndex, toonupNum))
        if len(self.toonupsGranted) > 8:
            self.toonupsGranted = self.toonupsGranted[0:8]
        self.sendUpdate('toonGotToonup', [avId,
                                          beltIndex,
                                          toonupIndex,
                                          toonupNum])
        if toonupIndex < len(self.ruleset.FOOD_HEAL_VALUES):
            hp = min(toon.getMaxHp() - toon.getHp(), self.ruleset.FOOD_HEAL_VALUES[toonupIndex])
            self.d_avHealed(avId, hp)
            self.healToon(toon, hp)

    def healToon(self, toon, increment):
        toon.toonUp(increment)

    def getToonTableIndex(self, toonId):
        tableIndex = -1
        for table in self.tables:
            if table.avId == toonId:
                tableIndex = table.index
                break

        return tableIndex

    def getToonGolfSpotIndex(self, toonId):
        golfSpotIndex = -1
        for golfSpot in self.golfSpots:
            if golfSpot.avId == toonId:
                golfSpotIndex = golfSpot.index
                break

        return golfSpotIndex

    def isToonOnTable(self, toonId):
        result = self.getToonTableIndex(toonId) != -1
        return result

    def isToonOnGolfSpot(self, toonId):
        result = self.getToonGolfSpotIndex(toonId) != -1
        return result

    def isToonRoaming(self, toonId):
        result = not self.isToonOnTable(toonId) and not self.isToonOnGolfSpot(toonId)
        return result

    def getBoss(self):
        return self.boss

    def progressValue(self, fromValue, toValue):
        t0 = float(self.boss.bossDamage) / float(self.ruleset.CEO_MAX_HP)
        elapsed = globalClock.getFrameTime() - self.battleFourStart
        t1 = elapsed / float(self.battleFourDuration)
        t = max(t0, t1)
        progVal = fromValue + (toValue - fromValue) * min(t, 1)
        self.notify.debug('progVal=%s' % progVal)
        return progVal
