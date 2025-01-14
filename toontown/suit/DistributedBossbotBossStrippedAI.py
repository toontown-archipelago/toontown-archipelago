import math
import random

from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import globalClockDelta
from direct.task.TaskManagerGlobal import taskMgr

from toontown.coghq import SeltzerLeagueGlobals
from toontown.suit import BossCogGlobals
from toontown.suit.DistributedBossCogStrippedAI import DistributedBossCogStrippedAI
from toontown.toonbase import ToontownGlobals


class DistributedBossbotBossStrippedAI(DistributedBossCogStrippedAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBossbotBossAI')

    def __init__(self, air, game):
        DistributedBossCogStrippedAI.__init__(self, air, game, 'c')
        self.ruleset = SeltzerLeagueGlobals.CEORuleset()
        self.threatDict = {}
        self.battleFourStart = 0
        self.movingToTable = False
        self.tableDest = -1
        self.curTable = -1
        self.speedDamage = 0
        self.maxSpeedDamage = ToontownGlobals.BossbotMaxSpeedDamage
        self.speedRecoverRate = ToontownGlobals.BossbotSpeedRecoverRate
        self.speedRecoverStartTime = 0
        self.battleFourTimeStarted = 0
        self.doneOvertimeOneAttack = False
        self.doneOvertimeTwoAttack = False

    def prepareBossForBattle(self):
        self.waitForNextAttack(5)

    def cleanupBossBattle(self):
        taskMgr.remove(self.uniqueName("NextAttack"))
        for tableIndex, _ in enumerate(self.game.tables):
            taskMgr.remove(self.uniqueName('Unflatten-%d' % tableIndex))

    def hitBoss(self, bossDamage):
        avId = self.air.getAvatarIdFromSender()
        if not self.validate(avId, avId in self.game.avIdList, 'hitBoss from unknown avatar'):
            return
        self.validate(avId, bossDamage <= 3, 'invalid bossDamage %s' % bossDamage)
        if bossDamage not in (1, 2, 3):
            return
        dmg = self.ruleset.SELTZER_DAMAGE_VALUES[bossDamage - 1]
        if self.attackCode in (ToontownGlobals.BossCogDizzy, ToontownGlobals.BossCogDizzyNow):
            dmg *= 1.5
            dmg = int(math.ceil(dmg))
        elif dmg >= self.ruleset.CEO_STUN_THRESHOLD:
            self.b_setAttackCode(ToontownGlobals.BossCogDizzyNow)
            self.movingToTable = False
            self.hitCount = 0
            self.game.d_stunBonus(avId, BossCogGlobals.POINTS_STUN_CEO)
            self.game.incrementCombo(avId, int(round(self.game.getComboLength(avId) / 3.0) + 7.0))

        self.game.incrementCombo(avId, int(round(self.game.getComboLength(avId) / 3.0) + 3.0))
        self.game.d_damageDealt(avId, dmg)
        dmg = min(self.getBossDamage() + dmg, self.ruleset.CEO_MAX_HP)
        self.b_setBossDamage(dmg, 0, 0)
        if self.bossDamage >= self.ruleset.CEO_MAX_HP:
            self.game.gameFSM.request('victory')
        else:
            self.__recordHit(bossDamage)

    def __recordHit(self, bossDamage):
        now = globalClock.getFrameTime()
        self.hitCount += 1
        if self.hitCount >= self.ruleset.CEO_STUN_HIT_LIMIT and self.attackCode in (
        ToontownGlobals.BossCogDizzy, ToontownGlobals.BossCogDizzyNow):
            self.b_setAttackCode(ToontownGlobals.BossCogRecoverDizzyAttack)
            self.movingToTable = False
            self.waitForNextAttack(self.game.progressValue(10, 3))
        avId = self.air.getAvatarIdFromSender()
        self.addThreat(avId, bossDamage)

    def getBossDamage(self):
        return self.bossDamage

    def b_setBossDamage(self, bossDamage, recoverRate, recoverStartTime):
        self.d_setBossDamage(bossDamage, recoverRate, recoverStartTime)
        self.setBossDamage(bossDamage, recoverRate, recoverStartTime)

    def setBossDamage(self, bossDamage, recoverRate, recoverStartTime):
        self.bossDamage = bossDamage
        self.recoverRate = recoverRate
        self.recoverStartTime = recoverStartTime

    def d_setBossDamage(self, bossDamage, recoverRate, recoverStartTime):
        timestamp = globalClockDelta.localToNetworkTime(recoverStartTime)
        self.sendUpdate('setBossDamage', [bossDamage, recoverRate, timestamp])

    def getSpeedDamage(self):
        now = globalClock.getFrameTime()
        elapsed = now - self.speedRecoverStartTime
        self.notify.debug('elapsed=%s' % elapsed)
        floatSpeedDamage = max(self.speedDamage - self.speedRecoverRate * elapsed / 60.0, 0)
        self.notify.debug('floatSpeedDamage = %s' % floatSpeedDamage)
        return int(max(self.speedDamage - self.speedRecoverRate * elapsed / 60.0, 0))

    def getFloatSpeedDamage(self):
        now = globalClock.getFrameTime()
        elapsed = now - self.speedRecoverStartTime
        floatSpeedDamage = max(self.speedDamage - self.speedRecoverRate * elapsed / 60.0, 0)
        self.notify.debug('floatSpeedDamage = %s' % floatSpeedDamage)
        return max(self.speedDamage - self.speedRecoverRate * elapsed / 60.0, 0)

    def b_setSpeedDamage(self, speedDamage, recoverRate, recoverStartTime):
        self.d_setSpeedDamage(speedDamage, recoverRate, recoverStartTime)
        self.setSpeedDamage(speedDamage, recoverRate, recoverStartTime)

    def setSpeedDamage(self, speedDamage, recoverRate, recoverStartTime):
        self.speedDamage = speedDamage
        self.speedRecoverRate = recoverRate
        self.speedRecoverStartTime = recoverStartTime

    def d_setSpeedDamage(self, speedDamage, recoverRate, recoverStartTime):
        timestamp = globalClockDelta.localToNetworkTime(recoverStartTime)
        self.sendUpdate('setSpeedDamage', [speedDamage, recoverRate, timestamp])

    def ballHitBoss(self, speedDamage):
        avId = self.air.getAvatarIdFromSender()
        if not self.validate(avId, avId in self.game.avIdList, 'hitBoss from unknown avatar'):
            return
        if speedDamage < 1:
            return
        now = globalClock.getFrameTime()
        newDamage = self.getSpeedDamage() + speedDamage
        self.notify.debug('newDamage = %s' % newDamage)
        speedDamage = min(self.getFloatSpeedDamage() + speedDamage, self.maxSpeedDamage)
        self.b_setSpeedDamage(speedDamage, self.speedRecoverRate, now)
        self.addThreat(avId, 0.1)

    def getThreat(self, toonId):
        if toonId in self.threatDict:
            return self.threatDict[toonId]
        else:
            return 0

    def addThreat(self, toonId, threat):
        if toonId in self.threatDict:
            self.threatDict[toonId] += threat
        else:
            self.threatDict[toonId] = threat

    def subtractThreat(self, toonId, threat):
        if toonId in self.threatDict:
            self.threatDict[toonId] -= threat
        else:
            self.threatDict[toonId] = 0
        if self.threatDict[toonId] < 0:
            self.threatDict[toonId] = 0

    def waitForNextAttack(self, delayTime):
        taskName = self.uniqueName('NextAttack')
        taskMgr.remove(taskName)
        taskMgr.doMethodLater(delayTime, self.doNextAttack, taskName)

    def doNextAttack(self, task):
        if self.attackCode in ToontownGlobals.BossCogDizzyStates:
            self.b_setAttackCode(ToontownGlobals.BossCogRecoverDizzyAttack)
            return

        attackCode = -1
        optionalParam = 0
        if self.movingToTable:
            self.waitForNextAttack(5)
        elif self.getHealthPercentage() <= self.ruleset.REORG_THRESHOLD and not self.doneOvertimeOneAttack:
            attackCode = ToontownGlobals.BossCogOvertimeAttack
            self.doneOvertimeOneAttack = True
            optionalParam = 0
        elif self.getHealthPercentage() <= self.ruleset.DOWNSIZE_THRESHOLD and not self.doneOvertimeTwoAttack:
            attackCode = ToontownGlobals.BossCogOvertimeAttack
            self.doneOvertimeTwoAttack = True
            optionalParam = 1
        else:
            attackCode = random.choice([ToontownGlobals.BossCogGolfAreaAttack,
                                        ToontownGlobals.BossCogDirectedAttack,
                                        ToontownGlobals.BossCogDirectedAttack,
                                        ToontownGlobals.BossCogDirectedAttack,
                                        ToontownGlobals.BossCogDirectedAttack])
        if attackCode == ToontownGlobals.BossCogAreaAttack:
            self.__doAreaAttack()
        if attackCode == ToontownGlobals.BossCogGolfAreaAttack:
            self.__doGolfAreaAttack()
        elif attackCode == ToontownGlobals.BossCogDirectedAttack:
            self.__doDirectedAttack()
        elif attackCode >= 0:
            self.b_setAttackCode(attackCode, optionalParam)

    def __doDirectedAttack(self):
        toonId = self.getMaxThreatToon()
        self.notify.debug('toonToAttack=%s' % toonId)
        unflattenedToons = self.getUnflattenedToons()
        attackTotallyRandomToon = random.random() < 0.1
        if unflattenedToons and (attackTotallyRandomToon or toonId == 0):
            toonId = random.choice(unflattenedToons)
        if toonId:
            toonThreat = self.getThreat(toonId)
            toonThreat *= 0.25
            threatToSubtract = max(toonThreat, 10)
            self.subtractThreat(toonId, threatToSubtract)
            if self.game.isToonRoaming(toonId):
                self.b_setAttackCode(ToontownGlobals.BossCogGolfAttack, toonId)
            elif self.game.isToonOnTable(toonId):
                if random.random() < 0.25:
                    self.b_setAttackCode(ToontownGlobals.BossCogGearDirectedAttack, toonId)
                else:
                    tableIndex = self.game.getToonTableIndex(toonId)
                    self.doMoveAttack(tableIndex)
            else:
                self.b_setAttackCode(ToontownGlobals.BossCogGolfAttack, toonId)
        else:
            uprightTables = self.getUprightTables()
            if uprightTables:
                tableToMoveTo = random.choice(uprightTables)
                self.doMoveAttack(tableToMoveTo)
            else:
                self.waitForNextAttack(4)

    def doMoveAttack(self, tableIndex):
        self.movingToTable = True
        self.tableDest = tableIndex
        self.b_setAttackCode(ToontownGlobals.BossCogMoveAttack, tableIndex)

    def getUnflattenedToons(self):
        result = []
        uprightTables = self.getUprightTables()
        for toonId in self.game.avIdList:
            toon = self.air.doId2do.get(toonId)
            if toon and toon.getHp() <= 0:
                continue
            toonTable = self.game.getToonTableIndex(toonId)
            if toonTable >= 0 and toonTable not in uprightTables:
                pass
            else:
                result.append(toonId)

        return result

    def getMaxThreatToon(self):
        returnedToonId = 0
        maxThreat = 0
        maxToons = []
        for toonId in self.threatDict:
            toon = self.air.doId2do.get(toonId)
            if toon and toon.getHp() <= 0:
                continue
            curThreat = self.threatDict[toonId]
            tableIndex = self.game.getToonTableIndex(toonId)
            if tableIndex > -1 and self.game.tables[tableIndex].state == 'Flat':
                pass
            elif curThreat > maxThreat:
                maxToons = [toonId]
                maxThreat = curThreat
            elif curThreat == maxThreat:
                maxToons.append(toonId)

        if maxToons:
            returnedToonId = random.choice(maxToons)
        return returnedToonId

    def getUprightTables(self):
        tableList = []
        for table in self.game.tables:
            if table.state != 'Flat':
                tableList.append(table.index)

        return tableList

    def reachedTable(self, tableIndex):
        if self.movingToTable and self.tableDest == tableIndex:
            self.movingToTable = False
            self.curTable = self.tableDest
            self.tableDest = -1

    def hitTable(self, tableIndex):
        self.notify.debug('hitTable tableIndex=%d' % tableIndex)
        if tableIndex < len(self.game.tables):
            table = self.game.tables[tableIndex]
            if table.state != 'Flat':
                table.goFlat()

    def awayFromTable(self, tableIndex):
        self.notify.debug('awayFromTable tableIndex=%d' % tableIndex)
        if tableIndex < len(self.game.tables):
            taskName = self.uniqueName('Unflatten-%d' % tableIndex)
            taskMgr.doMethodLater(self.ruleset.TABLE_UNFLATTEN_TIME, self.unflattenTable, taskName, extraArgs=[tableIndex])

    def unflattenTable(self, tableIndex):
        if tableIndex < len(self.game.tables):
            table = self.game.tables[tableIndex]
            if table.state == 'Flat':
                if table.avId and table.avId in self.game.avIdList:
                    table.forceControl(table.avId)
                else:
                    table.goFree()

    def __doAreaAttack(self):
        self.b_setAttackCode(ToontownGlobals.BossCogAreaAttack)

    def __doGolfAreaAttack(self):
        self.b_setAttackCode(ToontownGlobals.BossCogGolfAreaAttack)

    def hitToon(self, toonId):
        avId = self.air.getAvatarIdFromSender()
        if not self.validate(avId, avId != toonId, 'hitToon on self'):
            return
        if avId not in self.game.avIdList or toonId not in self.game.avIdList:
            return
        toon = self.air.doId2do.get(toonId)

        # todo maybe make this a mechanic from hitting teammates w seltzers?
        # i added a clamp check to support this if we want to
        if toon and toon.hp > 0:
            hp = min(1, toon.getMaxHp() - toon.getHp())
            self.game.d_avHealed(avId, hp)
            self.healToon(toon, hp)
            self.sendUpdate('toonGotHealed', [toonId])

    def toonLeftTable(self, tableIndex):
        if self.movingToTable and self.tableDest == tableIndex:
            if random.random() < 0.5:
                self.movingToTable = False
                self.waitForNextAttack(0)

    def getDamageMultiplier(self):
        mult = 1.0
        if self.doneOvertimeOneAttack and not self.doneOvertimeTwoAttack:
            mult = 1.25
        if self.game.getBattleFourTime() > 1.0:
            mult = self.game.getBattleFourTime() + 1
        return mult

    def getMaxHealth(self):
        return self.ruleset.CEO_MAX_HP
