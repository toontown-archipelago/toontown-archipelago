from typing import List

from panda3d.core import *

from toontown.archipelago.definitions.util import track_and_level_to_location, ap_location_name_to_id
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

    def getExperienceCapForTrack(self, track):
        trackExperienceCap = ToontownBattleGlobals.MaxSkill

        # If we have an access level below the # of levels of gags, determine the max xp we can obtain
        # If none of these checks pass, we are allowed to go to 999,999 exp
        highestLevelGagAllowed = self.owner.getTrackAccessLevel(track)
        highestLevelGagAllowed = max(0, highestLevelGagAllowed)  # Allow negative to just mean 0
        if highestLevelGagAllowed <= ToontownBattleGlobals.LAST_REGULAR_GAG_LEVEL:
            trackExperienceCap = ToontownBattleGlobals.Levels[track][highestLevelGagAllowed] - 1
        # Do we have access to the max gag level but not overflowing?
        elif highestLevelGagAllowed == ToontownBattleGlobals.LAST_REGULAR_GAG_LEVEL+1:
            trackExperienceCap = ToontownBattleGlobals.regMaxSkill - 1

        # Make sure it is not negative
        trackExperienceCap = max(0, trackExperienceCap)
        return trackExperienceCap

    def getAllowedGagLevels(self, track):

        levels: List[int] = []

        # Grab the exp requirements for this track
        thresholds = ToontownBattleGlobals.Levels[track]

        # Loop through the thresholds
        for gagIndex, requiredExp in enumerate(thresholds):

            # No track not valid
            if not self.owner.hasTrackAccess(track):
                continue

            # if we have the required experience to learn this gag
            if self.experience[track] >= requiredExp:
                levels.append(gagIndex)

        return levels

    def addExp(self, track, amount=1):

        self.notify.debug('adding %d exp to track %d' % (amount, track))

        trackExperienceCap = self.getExperienceCapForTrack(track)

        # Add the xp, and make sure that it does not go above our cap
        newXp = self.experience[track] + amount
        self.experience[track] = min(trackExperienceCap, newXp)

        # Now determine the checks that we are eligible for
        allowedGagLevelsForTrack = self.getAllowedGagLevels(track)
        apChecks = []
        for gagLevel in allowedGagLevelsForTrack:
            apCheckID = ap_location_name_to_id(track_and_level_to_location(track, gagLevel))
            apChecks.append(apCheckID)

        self.owner.addCheckedLocations(apChecks)

    # Call when we decrement track access levels, this will decrease our xp to correct values
    def fixTrackAccessLimits(self):
        for track in range(len(ToontownBattleGlobals.Tracks)):
            self.addExp(track, 0)

    def zeroOutExp(self):
        for track in range(0, len(ToontownBattleGlobals.Tracks)):
            self.experience[track] = ToontownBattleGlobals.StartingLevel

    def getExp(self, track):
        if type(track) == type(''):
            track = ToontownBattleGlobals.Tracks.index(track)
        return self.experience[track]

    def setExp(self, track, exp):
        if type(track) == type(''):
            track = ToontownBattleGlobals.Tracks.index(track)
        self.experience[track] = exp
        self.addExp(track, 0)

    def getExpLevel(self, track):
        if type(track) == type(''):
            track = ToontownBattleGlobals.Tracks.index(track)
        level = 0
        for amount in ToontownBattleGlobals.Levels[track]:
            if self.experience[track] >= amount:
                level = ToontownBattleGlobals.Levels[track].index(amount)

        return level

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
        return ToontownBattleGlobals.getUberDamageBonus(self.experience[track])

    # Returns a clean string representation of the damage bonus from above
    def getUberDamageBonusString(self, track) -> str:
        return str(int((self.getUberDamageBonus(track) - 1) * 100))
