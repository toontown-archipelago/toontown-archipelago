"""DistributedMinigameTemplateAI module: contains the DistributedMinigameTemplateAI class"""
import random
from operator import itemgetter
from typing import Optional

from direct.fsm.ClassicFSM import ClassicFSM
from direct.fsm.State import State
from direct.task.TaskManagerGlobal import taskMgr

from toontown.coghq.BossComboTrackerAI import BossComboTrackerAI
from toontown.minigame.DistributedMinigameAI import DistributedMinigameAI
from toontown.suit.DistributedSellbotBossStrippedAI import DistributedSellbotBossStrippedAI
from toontown.toon.DistributedToonAI import DistributedToonAI
from toontown.toonbase import TTLocalizer, ToontownGlobals


class DistributedPieGameAI(DistributedMinigameAI):
    battleThreeDuration = 1800

    def __init__(self, air, minigameId):
        super().__init__(air, minigameId)

        self.cagedToonDialogIndex = 100
        self.toonsTouchedCage = {}
        self.comboTrackers = {}
        self.boss: Optional[DistributedSellbotBossStrippedAI] = None

        self.gameFSM = ClassicFSM('DistributedMinigameTemplateAI',
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

        self.boss = DistributedSellbotBossStrippedAI(self.air, self)
        self.boss.generateWithRequired(self.zoneId)

        super().generate()

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
        self.battleThreeStart = globalClock.getFrameTime()

        self.initializeComboTrackers()

        for avId in self.avIdList:
            av = self.air.getDo(avId)
            if av:
                # Stop toon passive healing.
                av.stopToonUp()

                # Give the toon a nice heal.
                av.b_setHp(av.getMaxHp())

        # Start up the big boy.
        self.boss.prepareBossForBattle()

        self.setPieType()
        self.__saySomethingLater()
        self.listenForToonDeaths()

    def exitPlay(self):
        self.takeAwayPies()
        taskName = self.uniqueName('CagedToonSaySomething')
        taskMgr.remove(taskName)

        if self.boss is not None:
            self.boss.cleanupBossBattle()

        for avId in self.avIdList:
            av = self.air.getDo(avId)
            if av:
                # Restart toon passive healing.
                av.startToonUp(ToontownGlobals.PassiveHealFrequency)

        self.ignoreToonDeaths()

        pieTime = globalClock.getFrameTime()
        actualTime = pieTime - self.battleThreeStart
        self.d_updateTimer(actualTime)

    def enterVictory(self):
        victorId = max(self.scoreDict.items(), key=itemgetter(1))[0]
        self.sendUpdate("declareVictor", [victorId])
        taskMgr.doMethodLater(10, self.gameOver, self.uniqueName("pieGameVictory"), extraArgs=[])

    def exitVictory(self):
        taskMgr.remove(self.uniqueName("pieGameVictory"))

    def enterCleanup(self):
        self.notify.debug("enterCleanup")

        self.boss.requestDelete()
        del self.boss

        self.gameFSM.request('inactive')

    def exitCleanup(self):
        pass

    """
    Misc shit
    """

    def d_setBossCogId(self) -> None:
        self.sendUpdate("setBossCogId", [self.boss.getDoId()])

    def d_updateCombo(self, avId, comboLength):
        self.sendUpdate('updateCombo', [avId, comboLength])

    def d_awardCombo(self, avId, comboLength, amount):
        self.sendUpdate('awardCombo', [avId, comboLength, amount])

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

    def setPieType(self):
        for toonId in self.avIdList:
            toon = self.air.doId2do.get(toonId)
            if toon:
                toon.d_setPieType(4)

    def takeAwayPies(self):
        for toonId in self.avIdList:
            toon = self.air.doId2do.get(toonId)
            if toon:
                toon.b_setNumPies(0)

    def __saySomething(self, task):
        index = None
        avId = random.choice(self.avIdList)
        if self.toonsTouchedCage.get(avId):
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

    def __saySomethingLater(self, delayTime=15):
        taskName = self.uniqueName('CagedToonSaySomething')
        taskMgr.remove(taskName)
        taskMgr.doMethodLater(delayTime, self.__saySomething, taskName)

    def __goodJump(self, avId):
        index = random.randrange(10, TTLocalizer.CagedToonBattleThreeMaxGivePies + 1)
        self.d_cagedToonBattleThree(index, avId)
        self.__saySomethingLater()

    def d_cagedToonBattleThree(self, index, avId):
        self.sendUpdate('cagedToonBattleThree', [index, avId])

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
        self.sendUpdate('toonDied', [toon.doId])

        # Add a task to revive the toon.
        taskMgr.doMethodLater(5, self.reviveToon, self.uniqueName(f"reviveToon-{toon.doId}"), extraArgs=[toon.doId])

    def reviveToon(self, toonId: int) -> None:
        toon = self.air.getDo(toonId)
        if toon is None:
            return

        toon.b_setHp(1)

        self.sendUpdate("revivedToon", [toonId])

    def touchCage(self):
        avId = self.air.getAvatarIdFromSender()
        if not self.validate(avId, avId in self.avIdList, 'touchCage from unknown avatar'):
            return
        toon = self.air.doId2do.get(avId)
        if not toon:
            return
        if toon.getHp() <= 0:
            return
        toon.b_setNumPies(ToontownGlobals.FullPies)
        self.toonsTouchedCage[avId] = True
        self.__goodJump(avId)

    def damageToon(self, toon, deduction):
        if toon.getHp() <= 0:
            return

        toon.takeDamage(deduction)

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

    def progressValue(self, fromValue, toValue):
        t0 = float(self.boss.bossDamage) / float(self.boss.bossMaxDamage)
        elapsed = globalClock.getFrameTime() - self.battleThreeStart
        t1 = elapsed / float(self.battleThreeDuration)
        t = max(t0, t1)
        return fromValue + (toValue - fromValue) * min(t, 1)
