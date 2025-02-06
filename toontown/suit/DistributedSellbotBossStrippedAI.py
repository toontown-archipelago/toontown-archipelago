import random

from direct.distributed.ClockDelta import *
from direct.task.TaskManagerGlobal import taskMgr

from otp.ai.AIBaseGlobal import *
from toontown.suit import SellbotBossGlobals
from toontown.toonbase import ToontownGlobals
from . import BossCogGlobals
from .DistributedBossCogStrippedAI import DistributedBossCogStrippedAI


class DistributedSellbotBossStrippedAI(DistributedBossCogStrippedAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedSellbotBossStrippedAI')
    limitHitCount = 6

    def __init__(self, air, game):
        DistributedBossCogStrippedAI.__init__(self, air, game, 's')
        self.game = game

        self.bossMaxDamage = ToontownGlobals.SellbotBossMaxDamage
        self.pieHitToonup = SellbotBossGlobals.PieToonup
        self.recoverRate = 0
        self.recoverStartTime = 0

    def hitBoss(self, bossDamage):
        avId = self.air.getAvatarIdFromSender()
        if not self.validate(avId, avId in self.game.avIdList, 'DistributedSellbotBossAI.hitBoss from unknown avatar'):
            return
        self.validate(avId, bossDamage == 1, 'invalid bossDamage %s' % bossDamage)
        if bossDamage < 1:
            return
        if self.attackCode != ToontownGlobals.BossCogDizzyNow:
            return
        self.game.d_damageDealt(avId, bossDamage)
        self.game.incrementCombo(avId, int(round(self.game.getComboLength(avId) / 3.0) + 2.0))
        bossDamage = min(self.getBossDamage() + bossDamage, self.bossMaxDamage)
        self.b_setBossDamage(bossDamage, 0, 0)
        if self.bossDamage >= self.bossMaxDamage:
            self.game.gameFSM.request('victory')
        else:
            self.__recordHit()

    def hitBossInsides(self):
        avId = self.air.getAvatarIdFromSender()
        if not self.validate(avId, avId in self.game.avIdList, 'hitBossInsides from unknown avatar'):
            return
        self.game.d_stunBonus(avId, BossCogGlobals.POINTS_STUN_VP)
        self.game.incrementCombo(avId, int(round(self.game.getComboLength(avId) / 3.0) + 5.0))
        self.b_setAttackCode(ToontownGlobals.BossCogDizzyNow)
        self.b_setBossDamage(self.getBossDamage(), 0, 0)

    def hitToon(self, toonId):
        avId = self.air.getAvatarIdFromSender()
        if not self.validate(avId, avId != toonId, 'hitToon on self'):
            return
        if avId not in self.game.avIdList or toonId not in self.game.avIdList:
            return
        toon = self.air.doId2do.get(toonId)
        if toon and toon.hp > 0:
            hp = min(self.pieHitToonup, toon.getMaxHp() - toon.getHp())
            self.game.d_avHealed(avId, hp)
            self.healToon(toon, self.pieHitToonup)

    def getDamageMultiplier(self):
        return SellbotBossGlobals.AttackMult

    def doNextAttack(self, task):
        if self.attackCode == ToontownGlobals.BossCogDizzyNow:
            attackCode = ToontownGlobals.BossCogRecoverDizzyAttack
        else:
            attackCode = random.choice([ToontownGlobals.BossCogAreaAttack, ToontownGlobals.BossCogFrontAttack, ToontownGlobals.BossCogDirectedAttack, ToontownGlobals.BossCogDirectedAttack, ToontownGlobals.BossCogDirectedAttack, ToontownGlobals.BossCogDirectedAttack])
        if attackCode == ToontownGlobals.BossCogAreaAttack:
            self.__doAreaAttack()
        else:
            if attackCode == ToontownGlobals.BossCogDirectedAttack:
                self.__doDirectedAttack()
            else:
                self.b_setAttackCode(attackCode)

    def __doAreaAttack(self):
        self.b_setAttackCode(ToontownGlobals.BossCogAreaAttack)
        if self.recoverRate:
            newRecoverRate = min(200, self.recoverRate * 1.2)
        else:
            newRecoverRate = 2
        now = globalClock.getFrameTime()
        self.b_setBossDamage(self.getBossDamage(), newRecoverRate, now)

    def __doDirectedAttack(self):
        if self.nearToons:
            toonId = random.choice(self.nearToons)
            self.b_setAttackCode(ToontownGlobals.BossCogDirectedAttack, toonId)
        else:
            self.__doAreaAttack()

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

        # It is important that we consistently represent bossDamage as
        # an integer value, so there is never any chance of client and
        # AI disagreeing about whether bossDamage < bossMaxDamage.
        return int(max(self.bossDamage - self.recoverRate * elapsed / 60.0, 0))

    def d_setBossDamage(self, bossDamage, recoverRate, recoverStartTime):
        timestamp = globalClockDelta.localToNetworkTime(recoverStartTime, bits=32)
        self.sendUpdate('setBossDamage', [bossDamage, recoverRate, timestamp])

    def waitForNextStrafe(self, delayTime):
        taskName = self.uniqueName('NextStrafe')
        taskMgr.remove(taskName)
        taskMgr.doMethodLater(delayTime, self.doNextStrafe, taskName)

    def stopStrafes(self):
        taskName = self.uniqueName('NextStrafe')
        taskMgr.remove(taskName)

    def doNextStrafe(self, task):
        if self.attackCode != ToontownGlobals.BossCogDizzyNow:
            side = random.choice([0, 1])
            direction = random.choice([0, 1])
            # If we are on a slope, force open the back
            if (self.getHealthPercentage() <= 0.84 and self.getHealthPercentage() >= 0.65) or (self.getHealthPercentage() <= 0.48 and self.getHealthPercentage() >= 0.28):
                side = 1
            # If we are near the end, always force the front door to open
            if self.getHealthPercentage() <= 0.06:
                side = 0
            self.sendUpdate('doStrafe', [side, direction])
        delayTime = 9
        self.waitForNextStrafe(delayTime)

    def prepareBossForBattle(self) -> None:
        self.b_setBossDamage(0, 0, 0)
        self.waitForNextAttack(5)
        self.waitForNextStrafe(9)

    def cleanupBossBattle(self):
        self.stopAttacks()
        self.stopStrafes()

    def __recordHit(self):
        self.hitCount += 1
        if self.hitCount < self.limitHitCount or self.bossDamage < SellbotBossGlobals.HitCountDamage:
            return
        self.b_setAttackCode(ToontownGlobals.BossCogRecoverDizzyAttack)
