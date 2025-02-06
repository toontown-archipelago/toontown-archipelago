from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *

from libotp import *
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals
from . import SuitDNA
from .DistributedBossCogStripped import DistributedBossCogStripped


class DistributedLawbotBossStripped(DistributedBossCogStripped):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedLawbotBoss')

    def __init__(self, cr):
        self.notify.debug('----- __init___')
        DistributedBossCogStripped.__init__(self, cr)
        self.game = None
        self.bossDamage = 0
        self.attackCode = None
        self.recoverRate = 0
        self.recoverStartTime = 0
        self.bossMaxDamage = ToontownGlobals.LawbotBossMaxDamage
        self.warningSfx = None

    def announceGenerate(self):
        self.notify.debug('----- announceGenerate')
        DistributedBossCogStripped.announceGenerate(self)
        self.setName(TTLocalizer.LawbotBossName)
        nameInfo = TTLocalizer.BossCogNameWithDept % {'name': self._name,
                                                      'dept': SuitDNA.getDeptFullname(self.style.dept)}
        self.setDisplayName(nameInfo)
        self.warningSfx = loader.loadSfx('phase_9/audio/sfx/CHQ_GOON_tractor_beam_alarmed.ogg')

    def delete(self):
        self.notify.debug('----- delete')
        del self.game
        DistributedBossCogStripped.delete(self)

    def setBossDamage(self, bossDamage, recoverRate, timestamp):
        recoverStartTime = globalClockDelta.networkToLocalTime(timestamp)
        self.bossDamage = bossDamage
        self.recoverRate = recoverRate
        self.recoverStartTime = recoverStartTime
        self.game.makeScaleReflectDamage()
        self.bossHealthBar.update(self.bossMaxDamage - bossDamage, self.bossMaxDamage)

    def getBossDamage(self):
        self.notify.debug('----- getBossDamage')
        now = globalClock.getFrameTime()
        elapsed = now - self.recoverStartTime
        return max(self.bossDamage - self.recoverRate * elapsed / 60.0, 0)

    def prepareBossForBattle(self):
        self.cleanupIntervals()
        self.clearChat()
        self.reparentTo(render)
        self.happy = 1
        self.raised = 1
        self.forward = 1
        self.doAnimate()
        self.stickBossToFloor()
        self.setPosHpr(*ToontownGlobals.LawbotBossBattleThreePosHpr)
        self.bossMaxDamage = ToontownGlobals.LawbotBossMaxDamage
        self.bossHealthBar.initialize(self.bossMaxDamage - self.bossDamage, self.bossMaxDamage)

    def cleanupBossBattle(self):
        self.notify.debug('----- exitBattleThree')
        self.cleanupIntervals()
        self.removeHealthBar()
        self.unstickBoss()

    def cleanupAttacks(self):
        self.notify.debug('----- cleanupAttacks')

    def makeDefeatMovie(self):
        bossTrack = Track(
            (0.0, Sequence(Func(self.clearChat), Func(self.reverseHead), ActorInterval(self, 'Ff_speech'))),
            (1.0, Func(self.setChatAbsolute, TTLocalizer.LawbotBossProsecutionWins, CFSpeech)))
        return bossTrack

    def saySomething(self, chatString):
        intervalName = 'ChiefJusticeTaunt'
        seq = Sequence(name=intervalName)
        seq.append(Func(self.setChatAbsolute, chatString, CFSpeech))
        seq.append(Wait(4.0))
        seq.append(Func(self.clearChat))
        oldSeq = self.activeIntervals.get(intervalName)
        if oldSeq:
            oldSeq.finish()
        seq.start()
        self.storeInterval(seq, intervalName)

    def setTaunt(self, tauntIndex, extraInfo):
        chatString = TTLocalizer.LawbotBossTaunts[1]
        if tauntIndex == 0:
            if extraInfo < len(self.involvedToons):
                toonId = self.involvedToons[extraInfo]
                toon = base.cr.doId2do.get(toonId)
                if toon:
                    chatString = TTLocalizer.LawbotBossTaunts[tauntIndex] % toon.getName()
        else:
            chatString = TTLocalizer.LawbotBossTaunts[tauntIndex]
        self.saySomething(chatString)

    def setAttackCode(self, attackCode, avId=0):
        DistributedBossCogStripped.setAttackCode(self, attackCode, avId)
        if attackCode == ToontownGlobals.BossCogAreaAttack:
            self.saySomething(TTLocalizer.LawbotBossAreaAttackTaunt)
            base.playSfx(self.warningSfx)
