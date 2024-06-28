from typing import List, Tuple

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

    # Similarly to getAllowedGagLevels(), but does this for all the tracks in the game.
    # returns a list of tuple pairs of (track, level) where every member is a gag that is able to be bought
    def getAllowedGagsAndLevels(self) -> List[Tuple[int, int]]:
        gags: List[Tuple[int, int]] = []

        # Loop through all the tracks
        for track in range(len(ToontownBattleGlobals.Tracks)):

            # If we don't have access to the track skip it
            if not self.owner.hasTrackAccess(track):
                continue

            # Get all the levels allowed and add them all
            levelsForTrack: List[int] = self.getAllowedGagLevels(track)
            for lvl in levelsForTrack:
                gag = (track, lvl)
                gags.append(gag)

        return gags

    # Given a track, return the gag levels that this toon has maxed. For a toon's gag level to be considered "maxed",
    # They must be either 1 xp under their next gag threshold or above it.
    def getMaxedGagLevels(self, track) -> List[int]:

        # Loop through the gag levels and the thresholds they unlock
        maxedGagLevels = []
        for gagLevelIndex, nextTrackUnlockExp in enumerate(ToontownBattleGlobals.Levels[track]):
            # Skip the first gag, not important
            if gagLevelIndex == 0:
                continue

            # Figure out the previous gag and subtract one from the unlock threshold for the current gag
            previousGag = gagLevelIndex - 1
            maxExpForPreviousGag = nextTrackUnlockExp - 1

            # Have we maxed this gag?
            if self.experience[track] >= maxExpForPreviousGag:
                maxedGagLevels.append(previousGag)

        # Now check if we "maxed" this track (i.e. our lvl 7 does max damage
        if self.experience[track] >= ToontownBattleGlobals.regMaxSkill - 1:
            maxedGagLevels.append(ToontownBattleGlobals.LAST_REGULAR_GAG_LEVEL)

        return maxedGagLevels

    def addExp(self, track, amount=1):

        self.notify.debug('adding %d exp to track %d' % (amount, track))

        trackExperienceCap = self.getExperienceCapForTrack(track)

        # Add the xp, and make sure that it does not go above our cap
        newXp = self.experience[track] + amount
        self.experience[track] = min(trackExperienceCap, newXp)

        # Here temporarily until i make options not bad.
        # 0 = unlock, 1 = trained
        checkBehavior = self.owner.slotData.get('gag_training_check_behavior', 1)
        if checkBehavior not in (0, 1): checkBehavior = 1
        # Now determine the checks that we are eligible for

        if checkBehavior == 0:
            # This is the line of code to have the legacy system where we unlock checks based on the actual gags we have
            # unlocked. Leaving this here in case we would rather keep this logic
            gagLevels = self.getAllowedGagLevels(track)
        else:
            # This line of code is the new system where we do gag location checks based on maxing a gag's exp.
            # (Maxed as in highest exp amount before unlocking the next gag or higher)
            gagLevels = self.getMaxedGagLevels(track)

        # Now convert our gags to the corresponding AP checks.
        apChecks = []
        for gagLevel in gagLevels:
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
    def getUberDamageBonus(self, track, overflowMod=None) -> float:
        return ToontownBattleGlobals.getUberDamageBonus(self.experience[track], track, overflowMod)

    # Returns a clean string representation of the damage bonus from above
    def getUberDamageBonusString(self, track) -> str:
        return str(int((self.getUberDamageBonus(track) - 1) * 100))
