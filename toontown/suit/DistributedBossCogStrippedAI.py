from direct.directnotify import DirectNotifyGlobal
from direct.task.TaskManagerGlobal import taskMgr

from otp.avatar import DistributedAvatarAI
from toontown.suit import SuitDNA
from toontown.toonbase import ToontownGlobals


class DistributedBossCogStrippedAI(DistributedAvatarAI.DistributedAvatarAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBossCogAI')

    def __init__(self, air, game, dept):
        DistributedAvatarAI.DistributedAvatarAI.__init__(self, air)
        self.game = game
        self.dept = dept
        self.dna = SuitDNA.SuitDNA()
        self.dna.newBossCog(self.dept)
        self.deptIndex = SuitDNA.suitDepts.index(self.dept)
        self.looseToons = []
        self.involvedToons = []
        self.toonsA = []
        self.toonsB = []
        self.nearToons = []
        self.suitsA = []
        self.activeSuitsA = []
        self.suitsB = []
        self.activeSuitsB = []
        self.reserveSuits = []
        self.barrier = None
        self.bossDamage = 0
        self.bossMaxDamage = 100
        self.battleThreeStart = 0
        self.battleThreeDuration = 1800
        self.attackCode = None
        self.attackAvId = 0
        self.hitCount = 0
        self.hardmode = 0
        self.nerfed = False
        self.canSkip = True
        self.toonsSkipped = []
        return

    def delete(self):
        self.ignoreAll()
        del self.game
        return DistributedAvatarAI.DistributedAvatarAI.delete(self)

    def getDNAString(self):
        return self.dna.makeNetString()

    def avatarNearEnter(self):
        avId = self.air.getAvatarIdFromSender()
        if not self.isToonAlive(avId):
            return

        if avId not in self.nearToons:
            self.nearToons.append(avId)

    def avatarNearExit(self):
        avId = self.air.getAvatarIdFromSender()
        if avId in self.nearToons:
            self.nearToons.remove(avId)

    def isToonAlive(self, avId):
        toon = self.air.doId2do.get(avId)
        return avId in self.game.avIdList and toon and toon.getHp() > 0

    def isToonKnown(self, toonId):
        return toonId in self.involvedToons or toonId in self.looseToons

    def getHealthRemaining(self):
        return self.bossMaxDamage - self.bossDamage

    def getMaxHealth(self):
        return self.bossMaxDamage

    def getHealthPercentage(self) -> float:
        if self.getMaxHealth() <= 0:
            return 0
        return self.getHealthRemaining() / self.getMaxHealth()

    def healToon(self, toon, increment):
        toon.toonUp(increment)

    def reportToonHealth(self):
        if self.notify.getDebug():
            str = ''
            for toonId in self.involvedToons:
                toon = self.air.doId2do.get(toonId)
                if toon:
                    str += ', %s (%s/%s)' % (toonId, toon.getHp(), toon.getMaxHp())

            self.notify.debug('%s.toons = %s' % (self.doId, str[2:]))

    def getDamageMultiplier(self):
        if self.hardmode:
            return 2.5
        else:
            return 1.0

    def zapToon(self, x, y, z, h, p, r, bpx, bpy, attackCode, timestamp):
        avId = self.air.getAvatarIdFromSender()
        if not self.validate(avId, avId in self.game.avIdList, 'zapToon from unknown avatar'):
            return
        if attackCode == ToontownGlobals.BossCogLawyerAttack and self.dna.dept != 'l':
            self.notify.warning('got lawyer attack but not in CJ boss battle')
            return
        toon = simbase.air.doId2do.get(avId)
        if toon:
            self.d_showZapToon(avId, x, y, z, h, p, r, attackCode, timestamp)
            damage = ToontownGlobals.BossCogDamageLevels.get(attackCode)
            if damage == None:
                self.notify.warning('No damage listed for attack code %s' % attackCode)
                damage = 5
            damage *= self.getDamageMultiplier()
            damage = max(int(damage), 1)
            self.game.damageToon(toon, damage)
            if attackCode == ToontownGlobals.BossCogElectricFence:
                if bpy < 0 and abs(bpx / bpy) > 0.5:
                    if bpx < 0:
                        self.b_setAttackCode(ToontownGlobals.BossCogSwatRight)
                    else:
                        self.b_setAttackCode(ToontownGlobals.BossCogSwatLeft)

    def d_showZapToon(self, avId, x, y, z, h, p, r, attackCode, timestamp):
        self.sendUpdate('showZapToon', [avId, x, y, z, h, p, r, attackCode, timestamp])

    def b_setAttackCode(self, attackCode, avId=0):
        self.d_setAttackCode(attackCode, avId)
        self.setAttackCode(attackCode, avId)

    def setAttackCode(self, attackCode, avId=0):
        self.attackCode = attackCode
        self.attackAvId = avId
        if attackCode == ToontownGlobals.BossCogDizzy or attackCode == ToontownGlobals.BossCogDizzyNow:
            delayTime = self.game.progressValue(20, 5)
            self.hitCount = 0
        else:
            if attackCode == ToontownGlobals.BossCogSlowDirectedAttack:
                delayTime = ToontownGlobals.BossCogAttackTimes.get(attackCode)
                delayTime += self.game.progressValue(10, 0)
            else:
                delayTime = ToontownGlobals.BossCogAttackTimes.get(attackCode)
                if delayTime == None:
                    return
        self.waitForNextAttack(delayTime)
        return

    def d_setAttackCode(self, attackCode, avId=0):
        self.sendUpdate('setAttackCode', [attackCode, avId])

    def waitForNextAttack(self, delayTime):
        taskName = self.uniqueName('NextAttack')
        taskMgr.remove(taskName)
        taskMgr.doMethodLater(delayTime, self.doNextAttack, taskName)

    def stopAttacks(self):
        taskName = self.uniqueName('NextAttack')
        taskMgr.remove(taskName)

    def doNextAttack(self, task):
        self.b_setAttackCode(ToontownGlobals.BossCogNoAttack)

    def isStunned(self) -> bool:
        return self.attackCode == ToontownGlobals.BossCogDizzy
