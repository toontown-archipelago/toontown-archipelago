"""DistributedMinigameTemplateAI module: contains the DistributedMinigameTemplateAI class"""
import math
import random
from operator import itemgetter
from typing import Optional

from direct.fsm.ClassicFSM import ClassicFSM
from direct.fsm.State import State
from direct.task.TaskManagerGlobal import taskMgr

from toontown.coghq import ScaleLeagueGlobals
from toontown.coghq.BossComboTrackerAI import BossComboTrackerAI
from toontown.coghq.DistributedLawbotBossGavelAI import DistributedLawbotBossGavelAI
from toontown.coghq.DistributedLawbotChairAI import DistributedLawbotChairAI
from toontown.minigame.DistributedMinigameAI import DistributedMinigameAI
from toontown.suit.DistributedLawbotBossStrippedAI import DistributedLawbotBossStrippedAI
from toontown.suit.DistributedLawbotBossSuitAI import DistributedLawbotBossSuitAI
from toontown.suit.SuitDNA import SuitDNA
from toontown.toon.DistributedToonAI import DistributedToonAI
from toontown.toonbase import ToontownBattleGlobals, ToontownGlobals


class DistributedScaleGameAI(DistributedMinigameAI):

    def __init__(self, air, minigameId):
        super().__init__(air, minigameId)

        self.ruleset = ScaleLeagueGlobals.CJRuleset()
        self.comboTrackers = {}
        self.boss: Optional[DistributedLawbotBossStrippedAI] = None
        self.weightPerToon = 1
        self.bonusState = False
        self.bonusTimeStarted = 0

        self.lawyers = []
        self.chairs = None
        self.gavels = None

        self.gameFSM = ClassicFSM(self.__class__.__name__,
                                  [
                                      State('inactive',
                                            self.enterInactive,
                                            self.exitInactive,
                                            ['play']),
                                      State('play',
                                            self.enterPlay,
                                            self.exitPlay,
                                            ['victory', 'defeat', 'cleanup']),
                                      State('victory',
                                            self.enterVictory,
                                            self.exitVictory,
                                            ['cleanup']),
                                      State('defeat',
                                            self.enterDefeat,
                                            self.exitDefeat,
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

        self.boss = DistributedLawbotBossStrippedAI(self.air, self)
        self.boss.generateWithRequired(self.zoneId)

        super().generate()

    def cleanup(self) -> None:
        if self.boss is not None:
            self.boss.requestDelete()
            self.boss = None

        self.__deleteChairs()
        self.__deleteGavels()

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
        self.__makeChairs()

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

        self.battleThreeStart = globalClock.getFrameTime()

        # Prepare the big boy.
        self.boss.prepareBossForBattle()

        self.weightPerToon = self.ruleset.JURORS_SEATED // len(self.avIdList)

        self.__makeGavels()
        self.__makeLawyers()
        self.setPieType()

        for aGavel in self.gavels:
            aGavel.turnOn()

        for avId in self.avIdList:
            av = self.air.getDo(avId)
            if av:
                # Stop toon passive healing.
                av.stopToonUp()

                # Give the toon a nice heal.
                av.b_setHp(av.getMaxHp())

        self.initializeComboTrackers()
        self.listenForToonDeaths()

    def exitPlay(self):
        self.takeAwayPies()
        self.__deleteGavels()
        self.__resetLawyers()

        if self.boss is not None:
            self.boss.cleanupBossBattle()

        taskName = self.uniqueName('clearBonus')
        taskMgr.remove(taskName)

        for avId in self.avIdList:
            av = self.air.getDo(avId)
            if av:
                # Restart toon passive healing.
                av.startToonUp(ToontownGlobals.PassiveHealFrequency)

                # Restore health.
                av.b_setHp(av.getMaxHp())

        scaleTime = globalClock.getFrameTime()
        actualTime = scaleTime - self.battleThreeStart
        self.d_updateTimer(actualTime)

    def enterVictory(self):
        victorId = max(self.scoreDict.items(), key=itemgetter(1))[0]
        self.sendUpdate("declareVictor", [victorId])
        taskMgr.doMethodLater(5, self.gameOver, self.uniqueName("scaleGameVictory"), extraArgs=[])

    def exitVictory(self):
        taskMgr.remove(self.uniqueName("scaleGameVictory"))

    def enterDefeat(self):
        self.sendUpdate("weLost", [])
        taskMgr.doMethodLater(5, self.gameOver, self.uniqueName("scaleGameDefeat"), extraArgs=[])

    def exitDefeat(self):
        taskMgr.remove(self.uniqueName("scaleGameDefeat"))

    def enterCleanup(self):
        self.notify.debug("enterCleanup")
        self.cleanup()
        self.gameFSM.request('inactive')

    def exitCleanup(self):
        pass

    """
    yeah
    """

    def __makeChairs(self):
        if self.chairs is None:
            self.chairs = []
            for index in range(12):
                chair = DistributedLawbotChairAI(self.air, self, index)
                chair.generateWithRequired(self.zoneId)

                if index < self.ruleset.JURORS_SEATED:
                    chair.b_setToonJurorIndex(0)
                    self.chairs.append(chair)

    def __deleteChairs(self):
        if self.chairs is not None:
            for chair in self.chairs:
                chair.requestDelete()

            self.chairs = None

    def __makeGavels(self):
        if self.gavels is None:
            self.gavels = []
            for index in range(self.ruleset.NUM_GAVELS):
                gavel = DistributedLawbotBossGavelAI(self.air, self, index)
                gavel.generateWithRequired(self.zoneId)
                gavel.turnOn()
                self.gavels.append(gavel)

    def __deleteGavels(self):
        if self.gavels is not None:
            for gavel in self.gavels:
                gavel.request('Off')
                gavel.requestDelete()

            self.gavels = None

    def __resetLawyers(self):
        for suit in self.lawyers:
            suit.requestDelete()

        self.lawyers = []

    def __makeLawyers(self):
        self.__resetLawyers()
        lawCogChoices = ['b', 'dt', 'ac', 'bs', 'sd', 'le', 'bw']
        for i in range(self.ruleset.NUM_LAWYERS):
            suit = DistributedLawbotBossSuitAI(self.air, None)
            suit.dna = SuitDNA()
            lawCog = random.choice(lawCogChoices)
            suit.dna.newSuit(lawCog)
            suit.setPosHpr(*ToontownGlobals.LawbotBossLawyerPosHprs[i])
            suit.setBoss(self)
            suit.generateWithRequired(self.zoneId)
            self.lawyers.append(suit)

        self.__sendLawyerIds()

    def __sendLawyerIds(self):
        lawyerIds = []
        for suit in self.lawyers:
            lawyerIds.append(suit.doId)

        self.sendUpdate('setLawyerIds', [lawyerIds])

    def setPieType(self):
        for toonId in self.avIdList:
            toon = self.air.doId2do.get(toonId)
            if toon:
                toon.d_setPieType(ToontownBattleGlobals.MAX_TRACK_INDEX + 1)

    def takeAwayPies(self):
        for toonId in self.avIdList:
            toon = self.air.doId2do.get(toonId)
            if toon:
                toon.b_setNumPies(0)

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

    def touchWitnessStand(self):
        avId = self.air.getAvatarIdFromSender()
        toon = self.air.doId2do.get(avId)
        if not toon or toon.getHp() <= 0:
            return

        if not self.validate(avId, avId in self.avIdList, 'touchWitnessStand from unknown avatar'):
            return

        toon.b_setNumPies(self.ruleset.AMMO_COUNT)

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

    def clearBonus(self, taskName):
        self.bonusState = False

    def startBonusState(self):
        self.notify.debug('startBonusState')
        self.bonusState = True
        healingDone = 0
        for toonId in self.avIdList:
            toon = self.air.doId2do.get(toonId)
            if toon and toon.hp > 0:
                hp = min(ToontownGlobals.LawbotBossBonusToonup, toon.maxHp - toon.hp)
                healingDone += hp
                self.healToon(toon, hp)

        # Calculate point handouts for people who helped stunned
        freq = {avId: 0 for avId in self.avIdList}
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

        # Whisper out the time from the start of CJ
        self.bonusTimeStarted = globalClock.getFrameTime()

    def areAllLawyersStunned(self):
        for lawyer in self.lawyers:
            if not lawyer.stunned:
                return False

        return True

    def checkForBonusState(self):
        if self.gameFSM.getCurrentState().getName() != "play":
            return
        if self.bonusState:
            return
        if not self.areAllLawyersStunned():
            return
        curTime = globalClock.getFrameTime()
        delta = curTime - self.bonusTimeStarted
        if ToontownGlobals.LawbotBossBonusWaitTime < delta:
            self.startBonusState()

    def hitBoss(self):
        avId = self.air.getAvatarIdFromSender()
        if not self.validate(avId, avId in self.avIdList, 'hitBoss from unknown avatar'):
            return
        if self.gameFSM.getCurrentState().getName() != "play":
            return

        bossDamage = self.weightPerToon + 1
        bossDamage = min(self.boss.getBossDamage() + bossDamage, self.boss.bossMaxDamage)
        self.boss.b_setBossDamage(bossDamage, 0, 0)
        if self.boss.bossDamage >= self.boss.bossMaxDamage - 50:
            self.gameFSM.request('victory')

        self.incrementCombo(avId, int(round(self.getComboLength(avId)) / 5 + 1))
        self.d_damageDealt(avId, bossDamage)

    def healBoss(self, bossHeal):
        if self.gameFSM.getCurrentState().getName() != "play":
            return
        bossDamage = -bossHeal
        bossDamage = min(self.boss.getBossDamage() + bossDamage, self.boss.bossMaxDamage)
        bossDamage = max(bossDamage, 0)
        self.boss.b_setBossDamage(bossDamage, 0, 0)
        if self.boss.bossDamage == 0:
            self.gameFSM.request('defeat')

    def hitToon(self, toonId):
        if self.gameFSM.getCurrentState().getName() != "play":
            return
        avId = self.air.getAvatarIdFromSender()
        if not self.validate(avId, avId != toonId, 'hitToon on self'):
            return
        if avId not in self.avIdList or toonId not in self.avIdList:
            return
        toon = self.air.doId2do.get(toonId)
        if toon and toon.hp > 0:
            hp = min(self.ruleset.HEAL_AMOUNT, toon.maxHp - toon.hp)
            self.healToon(toon, hp)
            self.d_avHealed(avId, hp)
            self.sendUpdate('toonGotHealed', [toonId])

    def healToon(self, toon, increment):
        toon.toonUp(increment)

    def damageToon(self, toon, deduction):
        if toon.getHp() <= 0:
            return

        toon.takeDamage(deduction)
