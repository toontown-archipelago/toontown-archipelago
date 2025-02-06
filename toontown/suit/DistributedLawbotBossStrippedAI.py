import random

from direct.distributed.ClockDelta import *
from direct.task.TaskManagerGlobal import taskMgr

from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals
from .DistributedBossCogStrippedAI import DistributedBossCogStrippedAI


class DistributedLawbotBossStrippedAI(DistributedBossCogStrippedAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedLawbotBossAI')

    def __init__(self, air, game):
        DistributedBossCogStrippedAI.__init__(self, air, game, 'l')
        self.game = game

        self.bossMaxDamage = ToontownGlobals.LawbotBossMaxDamage
        self.recoverRate = 0
        self.recoverStartTime = 0
        self.bossDamage = ToontownGlobals.LawbotBossInitialDamage
        self.battleThreeTimeInMin = 0
        self.lastAreaAttackTime = 0

    def delete(self):
        self.notify.debug('DistributedLawbotBossAI.delete')
        return DistributedBossCogStrippedAI.delete(self)

    def doTaunt(self):
        tauntIndex = random.randrange(len(TTLocalizer.LawbotBossTaunts))
        extraInfo = 0
        if tauntIndex == 0 and self.game.avIdList:
            extraInfo = random.randrange(len(self.game.avIdList))
        self.sendUpdate('setTaunt', [tauntIndex, extraInfo])

    def doNextAttack(self, task):
        for lawyer in self.game.lawyers:
            lawyer.doNextAttack()

        self.waitForNextAttack(ToontownGlobals.LawbotBossLawyerCycleTime)
        timeSinceLastAttack = globalClock.getFrameTime() - self.lastAreaAttackTime
        allowedByTime = 15 < timeSinceLastAttack or self.lastAreaAttackTime == 0
        doAttack = random.randrange(1, 101)
        self.notify.debug('allowedByTime=%d doAttack=%d' % (allowedByTime, doAttack))
        if doAttack <= ToontownGlobals.LawbotBossChanceToDoAreaAttack and allowedByTime:
            self.__doAreaAttack()
            self.lastAreaAttackTime = globalClock.getFrameTime()
        else:
            chanceToDoTaunt = ToontownGlobals.LawbotBossChanceForTaunt
            action = random.randrange(1, 101)
            if action <= chanceToDoTaunt:
                self.doTaunt()

    def __doAreaAttack(self):
        self.b_setAttackCode(ToontownGlobals.BossCogAreaAttack)

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

    def prepareBossForBattle(self):
        jurorsOver = self.game.ruleset.JURORS_SEATED - ToontownGlobals.LawbotBossJurorsForBalancedScale
        dmgAdjust = jurorsOver * ToontownGlobals.LawbotBossDamagePerJuror
        self.b_setBossDamage(ToontownGlobals.LawbotBossInitialDamage + dmgAdjust, 0, 0)

        self.waitForNextAttack(5)

    def cleanupBossBattle(self):
        self.stopAttacks()
