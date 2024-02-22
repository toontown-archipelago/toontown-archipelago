from panda3d.core import *

from toontown.toonbase import ToontownBattleGlobals
from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPGlobals


class Experience:
    notify = DirectNotifyGlobal.directNotify.newCategory('Experience')

    def __init__(self, expValues: list, owner=None):
        self.owner = owner
        if not expValues:
            self.experience = []
            for track in range(0, len(ToontownBattleGlobals.Tracks)):
                self.experience.append(ToontownBattleGlobals.StartingLevel)

        self.experience = expValues

    def __str__(self):
        return str(self.experience)

    def getCurrentExperience(self):
        return self.experience

    def addExp(self, track, amount=1):
        if type(track) == type(''):
            track = ToontownBattleGlobals.Tracks.index(track)
        self.notify.debug('adding %d exp to track %d' % (amount, track))
        if self.owner.getGameAccess() == OTPGlobals.AccessFull:
            if self.experience[track] + amount <= ToontownBattleGlobals.MaxSkill:
                self.experience[track] += amount
            else:
                self.experience[track] = ToontownBattleGlobals.MaxSkill
        elif self.experience[track] + amount <= ToontownBattleGlobals.UnpaidMaxSkills[track]:
            self.experience[track] += amount
        elif self.experience[track] > ToontownBattleGlobals.UnpaidMaxSkills[track]:
            self.experience[track] += 0
        else:
            self.experience[track] = ToontownBattleGlobals.UnpaidMaxSkills[track]

    def maxOutExp(self):
        for track in range(0, len(ToontownBattleGlobals.Tracks)):
            self.experience[track] = ToontownBattleGlobals.MaxSkill

    def maxOutExpMinusOne(self):
        for track in range(0, len(ToontownBattleGlobals.Tracks)):
            self.experience[track] = ToontownBattleGlobals.MaxSkill - 1

    def makeExpHigh(self):
        for track in range(0, len(ToontownBattleGlobals.Tracks)):
            self.experience[track] = ToontownBattleGlobals.Levels[track][
                                         len(ToontownBattleGlobals.Levels[track]) - 1] - 1

    def makeExpRegular(self):
        import random
        for track in range(0, len(ToontownBattleGlobals.Tracks)):
            rank = random.choice((0, int(random.random() * 1500.0), int(random.random() * 2000.0)))
            self.experience[track] = ToontownBattleGlobals.Levels[track][
                                         len(ToontownBattleGlobals.Levels[track]) - 1] - rank

    def zeroOutExp(self):
        for track in range(0, len(ToontownBattleGlobals.Tracks)):
            self.experience[track] = ToontownBattleGlobals.StartingLevel

    def setAllExp(self, num):
        for track in range(0, len(ToontownBattleGlobals.Tracks)):
            self.experience[track] = num

    def getExp(self, track):
        if type(track) == type(''):
            track = ToontownBattleGlobals.Tracks.index(track)
        return self.experience[track]

    def setExp(self, track, exp):
        if type(track) == type(''):
            track = ToontownBattleGlobals.Tracks.index(track)
        self.experience[track] = exp

    def getExpLevel(self, track):
        if type(track) == type(''):
            track = ToontownBattleGlobals.Tracks.index(track)
        level = 0
        for amount in ToontownBattleGlobals.Levels[track]:
            if self.experience[track] >= amount:
                level = ToontownBattleGlobals.Levels[track].index(amount)

        return level

    def getTotalExp(self):
        total = 0
        for level in self.experience:
            total += level

        return total

    def getNextExpValue(self, track, curSkill=None):
        if curSkill == None:
            curSkill = self.experience[track]
        retVal = ToontownBattleGlobals.Levels[track][len(ToontownBattleGlobals.Levels[track]) - 1]
        for amount in ToontownBattleGlobals.Levels[track]:
            if curSkill < amount:
                retVal = amount
                return retVal

        return retVal

    def getNewGagIndexList(self, track, extraSkill):
        retList = []
        curSkill = self.experience[track]
        nextExpValue = self.getNextExpValue(track, curSkill)
        finalGagFlag = 0
        while curSkill + extraSkill >= nextExpValue > curSkill and not finalGagFlag:
            retList.append(ToontownBattleGlobals.Levels[track].index(nextExpValue))
            newNextExpValue = self.getNextExpValue(track, nextExpValue)
            if newNextExpValue == nextExpValue:
                finalGagFlag = 1
            else:
                nextExpValue = newNextExpValue

        return retList

    # Based on how much overflow XP we have, how much damage should we add as a bonus?
    def getUberDamageBonus(self, track) -> float:
        overflow = self.experience[track] - ToontownBattleGlobals.regMaxSkill
        if overflow < 0:
            overflow = 0

        # Returns a multiplier to multiply base damage by, default is 1% damage per 100 xp
        multiplier = 1 + overflow / 10000
        return multiplier

    # Returns a clean string representation of the damage bonus from above
    def getUberDamageBonusString(self, track) -> str:
        return str(int((self.getUberDamageBonus(track) - 1) * 100))
