from typing import Dict, NamedTuple, List

from otp.otpbase import OTPGlobals
from apworld.toontown import locations
from toontown.archipelago.definitions import util
from toontown.toonbase import ToontownBattleGlobals
from toontown.toonbase import ToontownGlobals
from toontown.battle import SuitBattleGlobals
from toontown.coghq import CogDisguiseGlobals
import random
from toontown.toon import NPCToons
import copy, string
from toontown.hood import ZoneUtil
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import TTLocalizer
from direct.showbase import PythonUtil
import time, types, random
notify = DirectNotifyGlobal.directNotify.newCategory('Quests')
ItemDict = TTLocalizer.QuestsItemDict
CompleteString = TTLocalizer.QuestsCompleteString
NotChosenString = TTLocalizer.QuestsNotChosenString
DefaultGreeting = TTLocalizer.QuestsDefaultGreeting
DefaultIncomplete = TTLocalizer.QuestsDefaultIncomplete
DefaultIncompleteProgress = TTLocalizer.QuestsDefaultIncompleteProgress
DefaultIncompleteWrongNPC = TTLocalizer.QuestsDefaultIncompleteWrongNPC
DefaultComplete = TTLocalizer.QuestsDefaultComplete
DefaultLeaving = TTLocalizer.QuestsDefaultLeaving
DefaultReject = TTLocalizer.QuestsDefaultReject
DefaultTierNotDone = TTLocalizer.QuestsDefaultTierNotDone
DefaultQuest = TTLocalizer.QuestsDefaultQuest
DefaultVisitQuestDialog = TTLocalizer.QuestsDefaultVisitQuestDialog
GREETING = 0
QUEST = 1
INCOMPLETE = 2
INCOMPLETE_PROGRESS = 3
INCOMPLETE_WRONG_NPC = 4
COMPLETE = 5
LEAVING = 6
Any = 1
OBSOLETE = 'OBSOLETE'
Start = 1
Cont = 0
Anywhere = 1
NA = 2
Same = 3
AnyFish = 4
AnyCashbotSuitPart = 5
AnyLawbotSuitPart = 6
AnyBossbotSuitPart = 7
ToonTailor = 999
ToonHQ = 1000
QuestDictTierIndex = 0
QuestDictStartIndex = 1
QuestDictDescIndex = 2
QuestDictFromNpcIndex = 3
QuestDictToNpcIndex = 4
QuestDictRewardIndex = 5
QuestDictNextQuestIndex = 6
QuestDictDialogIndex = 7
VeryEasy = 100
Easy = 75
Medium = 50
Hard = 25
VeryHard = 20
TT_TIER = 0
DD_TIER = 4
DG_TIER = 7
MM_TIER = 8
BR_TIER = 11
DL_TIER = 14
LAWBOT_HQ_TIER = 18
BOSSBOT_HQ_TIER = 32
ELDER_TIER = 49
AP_TIER = 100
LOOPING_FINAL_TIER = ELDER_TIER
VISIT_QUEST_ID = 1000
TROLLEY_QUEST_ID = 110
FIRST_COG_QUEST_ID = 145
FRIEND_QUEST_ID = 150
PHONE_QUEST_ID = 175
NEWBIE_HP = 25
SELLBOT_HQ_NEWBIE_HP = 50
CASHBOT_HQ_NEWBIE_HP = 85
from toontown.toonbase.ToontownGlobals import FT_FullSuit, FT_Leg, FT_Arm, FT_Torso
QuestRandGen = random.Random()

def seedRandomGen(npcId, avId, tier, rewardHistory):
    QuestRandGen.seed(npcId * 100 + avId + tier + len(rewardHistory))


def seededRandomChoice(seq):
    return QuestRandGen.choice(seq)


def getCompleteStatusWithNpc(questComplete, toNpcId, npc):
    if questComplete:
        if npc:
            if npcMatches(toNpcId, npc):
                return COMPLETE
            else:
                return INCOMPLETE_WRONG_NPC
        else:
            return COMPLETE
    elif npc:
        if npcMatches(toNpcId, npc):
            return INCOMPLETE_PROGRESS
        else:
            return INCOMPLETE
    else:
        return INCOMPLETE


def npcMatches(toNpcId, npc):
    return toNpcId == npc.getNpcId() or toNpcId == Any or toNpcId == ToonHQ and npc.getHq() or toNpcId == ToonTailor and npc.getTailor()


def calcRecoverChance(numberNotDone, baseChance, cap = 1):
    chance = baseChance
    avgNum2Kill = 1.0 / (chance / 100.0)
    if numberNotDone >= avgNum2Kill * 1.5 and cap:
        chance = 1000
    elif numberNotDone > avgNum2Kill * 0.5:
        diff = float(numberNotDone - avgNum2Kill * 0.5)
        luck = 1.0 + abs(diff / (avgNum2Kill * 0.5))
        chance *= luck
    return chance


def simulateRecoveryVar(numNeeded, baseChance, list = 0, cap = 1):
    numHave = 0
    numTries = 0
    greatestFailChain = 0
    currentFail = 0
    capHits = 0
    attemptList = {}
    while numHave < numNeeded:
        numTries += 1
        chance = calcRecoverChance(currentFail, baseChance, cap)
        test = random.random() * 100
        if chance == 1000:
            capHits += 1
        if test < chance:
            numHave += 1
            if currentFail > greatestFailChain:
                greatestFailChain = currentFail
            if attemptList.get(currentFail):
                attemptList[currentFail] += 1
            else:
                attemptList[currentFail] = 1
            currentFail = 0
        else:
            currentFail += 1

    print('Test results: %s tries, %s longest failure chain, %s cap hits' % (numTries, greatestFailChain, capHits))
    if list:
        print('failures for each succes %s' % attemptList)


def simulateRecoveryFix(numNeeded, baseChance, list = 0):
    numHave = 0
    numTries = 0
    greatestFailChain = 0
    currentFail = 0
    attemptList = {}
    while numHave < numNeeded:
        numTries += 1
        chance = baseChance
        test = random.random() * 100
        if test < chance:
            numHave += 1
            if currentFail > greatestFailChain:
                greatestFailChain = currentFail
            if attemptList.get(currentFail):
                attemptList[currentFail] += 1
            else:
                attemptList[currentFail] = 1
            currentFail = 0
        else:
            currentFail += 1

    print('Test results: %s tries, %s longest failure chain' % (numTries, greatestFailChain))
    if list:
        print('failures for each succes %s' % attemptList)


class Quest:
    _cogTracks = [Any,
     'c',
     'l',
     'm',
     's']
    _factoryTypes = [Any,
     FT_FullSuit,
     FT_Leg,
     FT_Arm,
     FT_Torso]

    def check(self, cond, msg):
        pass

    def checkLocation(self, location):
        locations = [Anywhere] + list(TTLocalizer.GlobalStreetNames.keys())
        self.check(location in locations, 'invalid location: %s' % location)

    def checkNumCogs(self, num):
        self.check(1, 'invalid number of cogs: %s' % num)

    def checkNewbieLevel(self, level):
        self.check(1, 'invalid newbie level: %s' % level)

    def checkCogType(self, type):
        types = [Any] + SuitBattleGlobals.getAllRegisteredSuits()
        self.check(type in types, 'invalid cog type: %s' % type)

    def checkCogTrack(self, track):
        self.check(track in self._cogTracks, 'invalid cog track: %s' % track)

    def checkCogLevel(self, level):
        self.check(level >= 1 and level <= 12, 'invalid cog level: %s' % level)

    def checkNumSkelecogs(self, num):
        self.check(1, 'invalid number of cogs: %s' % num)

    def checkSkelecogTrack(self, track):
        self.check(track in self._cogTracks, 'invalid cog track: %s' % track)

    def checkSkelecogLevel(self, level):
        self.check(level >= 1 and level <= 12, 'invalid cog level: %s' % level)

    def checkNumSkeleRevives(self, num):
        self.check(1, 'invalid number of cogs: %s' % num)

    def checkNumForemen(self, num):
        self.check(num > 0, 'invalid number of foremen: %s' % num)

    def checkNumVPs(self, num):
        self.check(num > 0, 'invalid number of VPs: %s' % num)

    def checkNumSupervisors(self, num):
        self.check(num > 0, 'invalid number of supervisors: %s' % num)

    def checkNumCFOs(self, num):
        self.check(num > 0, 'invalid number of CFOs: %s' % num)

    def checkNumBuildings(self, num):
        self.check(1, 'invalid num buildings: %s' % num)

    def checkBuildingTrack(self, track):
        self.check(track in self._cogTracks, 'invalid building track: %s' % track)

    def checkBuildingFloors(self, floors):
        self.check(floors >= 1 and floors <= 5, 'invalid num floors: %s' % floors)

    def checkNumFactories(self, num):
        self.check(1, 'invalid num factories: %s' % num)

    def checkFactoryType(self, type):
        self.check(type in self._factoryTypes, 'invalid factory type: %s' % type)

    def checkNumMints(self, num):
        self.check(1, 'invalid num mints: %s' % num)

    def checkNumCogParts(self, num):
        self.check(1, 'invalid num cog parts: %s' % num)

    def checkNumGags(self, num):
        self.check(1, 'invalid num gags: %s' % num)

    def checkGagTrack(self, track):
        self.check(track >= ToontownBattleGlobals.MIN_TRACK_INDEX and track <= ToontownBattleGlobals.MAX_TRACK_INDEX, 'invalid gag track: %s' % track)

    def checkGagItem(self, item):
        self.check(item >= ToontownBattleGlobals.MIN_LEVEL_INDEX and item <= ToontownBattleGlobals.MAX_LEVEL_INDEX, 'invalid gag item: %s' % item)

    def checkDeliveryItem(self, item):
        self.check(item in ItemDict, 'invalid delivery item: %s' % item)

    def checkNumItems(self, num):
        self.check(1, 'invalid num items: %s' % num)

    def checkRecoveryItem(self, item):
        self.check(item in ItemDict, 'invalid recovery item: %s' % item)

    def checkPercentChance(self, chance):
        self.check(chance > 0 and chance <= 100, 'invalid percent chance: %s' % chance)

    def checkRecoveryItemHolderAndType(self, holder, holderType = 'type'):
        holderTypes = ['type', 'level', 'track']
        self.check(holderType in holderTypes, 'invalid recovery item holderType: %s' % holderType)
        if holderType == 'type':
            holders = [Any, AnyFish] + SuitBattleGlobals.getAllRegisteredSuits()
            self.check(holder in holders, 'invalid recovery item holder: %s for holderType: %s' % (holder, holderType))
        elif holderType == 'level':
            pass
        elif holderType == 'track':
            self.check(holder in self._cogTracks, 'invalid recovery item holder: %s for holderType: %s' % (holder, holderType))

    def checkTrackChoice(self, option):
        self.check(option >= ToontownBattleGlobals.MIN_TRACK_INDEX and option <= ToontownBattleGlobals.MAX_TRACK_INDEX, 'invalid track option: %s' % option)

    def checkNumFriends(self, num):
        self.check(1, 'invalid number of friends: %s' % num)

    def checkNumMinigames(self, num):
        self.check(1, 'invalid number of minigames: %s' % num)

    def filterFunc(avatar):
        return 1

    filterFunc = staticmethod(filterFunc)

    def __init__(self, id, quest):
        self.id = id
        self.quest = quest

    def getId(self):
        return self.id

    def getType(self):
        return self.__class__

    def getObjectiveStrings(self):
        return ['']

    def getString(self):
        return self.getObjectiveStrings()[0]

    def getRewardString(self, progressString):
        return self.getString() + ' : ' + progressString

    def getChooseString(self):
        return self.getString()

    def getPosterString(self):
        return self.getString()

    def getHeadlineString(self):
        return self.getString()

    def getDefaultQuestDialog(self):
        return self.getString() + TTLocalizer.Period

    def getNumQuestItems(self):
        return -1

    def addArticle(self, num, oString):
        if len(oString) == 0:
            return oString
        if num == 1:
            return oString
        else:
            return '%d %s' % (num, oString)

    def __repr__(self):
        return 'Quest type: %s id: %s params: %s' % (self.__class__.__name__, self.id, self.quest[0:])

    def doesCogCount(self, avId, cogDict, zoneId, avList):
        return 0

    def doesVPCount(self, avId, cogDict, zoneId, avList):
        return 0

    def doesCFOCount(self, avId, cogDict, zoneId, avList):
        return 0

    def doesFactoryCount(self, avId, location, avList):
        return 0

    def doesMintCount(self, avId, location, avList):
        return 0

    def doesCogPartCount(self, avId, location, avList):
        return 0

    def getCompletionStatus(self, av, questDesc, npc = None):
        notify.error('Pure virtual - please override me')
        return None


class LocationBasedQuest(Quest):
    def __init__(self, id, quest):
        Quest.__init__(self, id, quest)
        self.checkLocation(self.quest[0])

    def getLocation(self):
        return self.quest[0]

    def getLocationName(self):
        loc = self.getLocation()
        if loc == Anywhere:
            locName = ''
        elif loc in ToontownGlobals.hoodNameMap:
            locName = TTLocalizer.QuestInLocationString % {'inPhrase': ToontownGlobals.hoodNameMap[loc][1],
             'location': ToontownGlobals.hoodNameMap[loc][-1] + TTLocalizer.QuestsLocationArticle}
        elif loc in ToontownGlobals.StreetBranchZones:
            locName = TTLocalizer.QuestInLocationString % {'inPhrase': ToontownGlobals.StreetNames[loc][1],
             'location': ToontownGlobals.StreetNames[loc][-1] + TTLocalizer.QuestsLocationArticle}
        else:
            locName = f"Unknown Location: {loc}"
        return locName

    def isLocationMatch(self, zoneId):
        loc = self.getLocation()
        if loc is Anywhere:
            return 1
        if ZoneUtil.isPlayground(loc):
            if loc == ZoneUtil.getCanonicalHoodId(zoneId):
                return 1
            else:
                return 0
        elif loc == ZoneUtil.getCanonicalBranchZone(zoneId):
            return 1
        elif loc == zoneId:
            return 1
        else:
            return 0

    def getChooseString(self):
        return TTLocalizer.QuestsLocationString % {'string': self.getString(),
         'location': self.getLocationName()}

    def getPosterString(self):
        return TTLocalizer.QuestsLocationString % {'string': self.getString(),
         'location': self.getLocationName()}

    def getDefaultQuestDialog(self):
        return (TTLocalizer.QuestsLocationString + TTLocalizer.Period) % {'string': self.getString(),
         'location': self.getLocationName()}


class NewbieQuest:
    def getNewbieLevel(self):
        notify.error('Pure virtual - please override me')

    def getString(self, newStr = TTLocalizer.QuestsCogNewNewbieQuestObjective, oldStr = TTLocalizer.QuestsCogOldNewbieQuestObjective):
        laff = self.getNewbieLevel()
        if laff <= NEWBIE_HP:
            return newStr % self.getObjectiveStrings()[0]
        else:
            return oldStr % {'laffPoints': laff,
             'objective': self.getObjectiveStrings()[0]}

    def getCaption(self):
        laff = self.getNewbieLevel()
        if laff <= NEWBIE_HP:
            return TTLocalizer.QuestsCogNewNewbieQuestCaption % laff
        else:
            return TTLocalizer.QuestsCogOldNewbieQuestCaption % laff

    def getNumNewbies(self, avId, avList):
        newbieHp = self.getNewbieLevel()
        num = 0
        for av in avList:
            if av.getDoId() != avId and av.getMaxHp() <= newbieHp:
                num += 1

        return num


class CogQuest(LocationBasedQuest):
    def __init__(self, id, quest):
        LocationBasedQuest.__init__(self, id, quest)
        if self.__class__ == CogQuest:
            self.checkNumCogs(self.quest[1])
            self.checkCogType(self.quest[2])

    def getCogType(self):
        return self.quest[2]

    def getNumQuestItems(self):
        return self.getNumCogs()

    def getNumCogs(self):
        return self.quest[1]

    def getCompletionStatus(self, av, questDesc, npc = None):
        questId, fromNpcId, toNpcId, rewardId, toonProgress = questDesc
        questComplete = toonProgress >= self.getNumCogs()
        return getCompleteStatusWithNpc(questComplete, toNpcId, npc)

    def getProgressString(self, avatar, questDesc):
        if self.getCompletionStatus(avatar, questDesc) == COMPLETE:
            return CompleteString
        elif self.getNumCogs() == 1:
            return ''
        else:
            return TTLocalizer.QuestsCogQuestProgress % {'progress': questDesc[4],
             'numCogs': self.getNumCogs()}

    def getCogNameString(self):
        numCogs = self.getNumCogs()
        cogType = self.getCogType()
        if numCogs == 1:
            if cogType == Any:
                return TTLocalizer.Cog
            else:
                return SuitBattleGlobals.getSuitAttributes(cogType).singular
        elif cogType == Any:
            return TTLocalizer.Cogs
        else:
            return SuitBattleGlobals.getSuitAttributes(cogType).plural

    def getObjectiveStrings(self):
        cogName = self.getCogNameString()
        numCogs = self.getNumCogs()
        if numCogs == 1:
            text = cogName
        else:
            text = TTLocalizer.QuestsCogQuestDefeatDesc % {'numCogs': numCogs,
             'cogName': cogName}
        return (text,)

    def getString(self):
        return TTLocalizer.QuestsCogQuestDefeat % self.getObjectiveStrings()[0]

    def getSCStrings(self, toNpcId, progress):
        if progress >= self.getNumCogs():
            return getFinishToonTaskSCStrings(toNpcId)
        cogName = self.getCogNameString()
        numCogs = self.getNumCogs()
        if numCogs == 1:
            text = TTLocalizer.QuestsCogQuestSCStringS
        else:
            text = TTLocalizer.QuestsCogQuestSCStringP
        cogLoc = self.getLocationName()
        return text % {'cogName': cogName,
         'cogLoc': cogLoc}

    def getHeadlineString(self):
        return TTLocalizer.QuestsCogQuestHeadline

    def doesCogCount(self, avId, cogDict, zoneId, avList):
        questCogType = self.getCogType()
        return (questCogType is Any or questCogType is cogDict['type']) and avId in cogDict['activeToons'] and self.isLocationMatch(zoneId)


class CogNewbieQuest(CogQuest, NewbieQuest):
    def __init__(self, id, quest):
        CogQuest.__init__(self, id, quest)
        if self.__class__ == CogNewbieQuest:
            self.checkNumCogs(self.quest[1])
            self.checkCogType(self.quest[2])
            self.checkNewbieLevel(self.quest[3])

    def getNewbieLevel(self):
        return self.quest[3]

    def getString(self):
        return NewbieQuest.getString(self)

    def doesCogCount(self, avId, cogDict, zoneId, avList):
        if CogQuest.doesCogCount(self, avId, cogDict, zoneId, avList):
            return self.getNumNewbies(avId, avList)
        else:
            return 0


class CogTrackQuest(CogQuest):
    trackCodes = ['c',
     'l',
     'm',
     's']
    trackNamesS = [TTLocalizer.BossbotS,
     TTLocalizer.LawbotS,
     TTLocalizer.CashbotS,
     TTLocalizer.SellbotS]
    trackNamesP = [TTLocalizer.BossbotP,
     TTLocalizer.LawbotP,
     TTLocalizer.CashbotP,
     TTLocalizer.SellbotP]

    def __init__(self, id, quest):
        CogQuest.__init__(self, id, quest)
        if self.__class__ == CogTrackQuest:
            self.checkNumCogs(self.quest[1])
            self.checkCogTrack(self.quest[2])

    def getCogTrack(self):
        return self.quest[2]

    def getProgressString(self, avatar, questDesc):
        if self.getCompletionStatus(avatar, questDesc) == COMPLETE:
            return CompleteString
        elif self.getNumCogs() == 1:
            return ''
        else:
            return TTLocalizer.QuestsCogTrackQuestProgress % {'progress': questDesc[4],
             'numCogs': self.getNumCogs()}

    def getObjectiveStrings(self):
        numCogs = self.getNumCogs()
        track = self.trackCodes.index(self.getCogTrack())
        if numCogs == 1:
            text = self.trackNamesS[track]
        else:
            text = TTLocalizer.QuestsCogTrackDefeatDesc % {'numCogs': numCogs,
             'trackName': self.trackNamesP[track]}
        return (text,)

    def getString(self):
        return TTLocalizer.QuestsCogTrackQuestDefeat % self.getObjectiveStrings()[0]

    def getSCStrings(self, toNpcId, progress):
        if progress >= self.getNumCogs():
            return getFinishToonTaskSCStrings(toNpcId)
        numCogs = self.getNumCogs()
        track = self.trackCodes.index(self.getCogTrack())
        if numCogs == 1:
            cogText = self.trackNamesS[track]
            text = TTLocalizer.QuestsCogTrackQuestSCStringS
        else:
            cogText = self.trackNamesP[track]
            text = TTLocalizer.QuestsCogTrackQuestSCStringP
        cogLocName = self.getLocationName()
        return text % {'cogText': cogText,
         'cogLoc': cogLocName}

    def getHeadlineString(self):
        return TTLocalizer.QuestsCogTrackQuestHeadline

    def doesCogCount(self, avId, cogDict, zoneId, avList):
        questCogTrack = self.getCogTrack()
        return questCogTrack == cogDict['track'] and avId in cogDict['activeToons'] and self.isLocationMatch(zoneId)


class CogLevelQuest(CogQuest):
    def __init__(self, id, quest):
        CogQuest.__init__(self, id, quest)
        self.checkNumCogs(self.quest[1])
        self.checkCogLevel(self.quest[2])

    def getCogType(self):
        return Any

    def getCogLevel(self):
        return self.quest[2]

    def getProgressString(self, avatar, questDesc):
        if self.getCompletionStatus(avatar, questDesc) == COMPLETE:
            return CompleteString
        elif self.getNumCogs() == 1:
            return ''
        else:
            return TTLocalizer.QuestsCogLevelQuestProgress % {'progress': questDesc[4],
             'numCogs': self.getNumCogs()}

    def getObjectiveStrings(self):
        count = self.getNumCogs()
        level = self.getCogLevel()
        name = self.getCogNameString()
        if count == 1:
            text = TTLocalizer.QuestsCogLevelQuestDesc
        else:
            text = TTLocalizer.QuestsCogLevelQuestDescC
        return (text % {'count': count,
          'level': level,
          'name': name},)

    def getString(self):
        return TTLocalizer.QuestsCogLevelQuestDefeat % self.getObjectiveStrings()[0]

    def getSCStrings(self, toNpcId, progress):
        if progress >= self.getNumCogs():
            return getFinishToonTaskSCStrings(toNpcId)
        count = self.getNumCogs()
        level = self.getCogLevel()
        name = self.getCogNameString()
        if count == 1:
            text = TTLocalizer.QuestsCogLevelQuestDesc
        else:
            text = TTLocalizer.QuestsCogLevelQuestDescI
        objective = text % {'level': level,
         'name': name}
        location = self.getLocationName()
        return TTLocalizer.QuestsCogLevelQuestSCString % {'objective': objective,
         'location': location}

    def getHeadlineString(self):
        return TTLocalizer.QuestsCogLevelQuestHeadline

    def doesCogCount(self, avId, cogDict, zoneId, avList):
        questCogLevel = self.getCogLevel()

        # (py2->3) Just in case a TTO dev decided that putting a boss in the dict with a level of None was a good idea
        if cogDict['level'] is None:
            return False

        return questCogLevel <= cogDict['level'] and avId in cogDict['activeToons'] and self.isLocationMatch(zoneId)


class SkelecogQBase:
    def getCogNameString(self):
        numCogs = self.getNumCogs()
        if numCogs == 1:
            return TTLocalizer.ASkeleton
        else:
            return TTLocalizer.SkeletonP

    def doesCogCount(self, avId, cogDict, zoneId, avList):
        return cogDict['isSkelecog'] and avId in cogDict['activeToons'] and self.isLocationMatch(zoneId)


class SkelecogQuest(CogQuest, SkelecogQBase):
    def __init__(self, id, quest):
        CogQuest.__init__(self, id, quest)
        self.checkNumSkelecogs(self.quest[1])

    def getCogType(self):
        return Any

    def getCogNameString(self):
        return SkelecogQBase.getCogNameString(self)

    def doesCogCount(self, avId, cogDict, zoneId, avList):
        return SkelecogQBase.doesCogCount(self, avId, cogDict, zoneId, avList)


class SkelecogNewbieQuest(SkelecogQuest, NewbieQuest):
    def __init__(self, id, quest):
        SkelecogQuest.__init__(self, id, quest)
        self.checkNewbieLevel(self.quest[2])

    def getNewbieLevel(self):
        return self.quest[2]

    def getString(self):
        return NewbieQuest.getString(self)

    def doesCogCount(self, avId, cogDict, zoneId, avList):
        if SkelecogQuest.doesCogCount(self, avId, cogDict, zoneId, avList):
            return self.getNumNewbies(avId, avList)
        else:
            return 0


class SkelecogTrackQuest(CogTrackQuest, SkelecogQBase):
    trackNamesS = [TTLocalizer.BossbotSkelS,
     TTLocalizer.LawbotSkelS,
     TTLocalizer.CashbotSkelS,
     TTLocalizer.SellbotSkelS]
    trackNamesP = [TTLocalizer.BossbotSkelP,
     TTLocalizer.LawbotSkelP,
     TTLocalizer.CashbotSkelP,
     TTLocalizer.SellbotSkelP]

    def __init__(self, id, quest):
        CogTrackQuest.__init__(self, id, quest)
        self.checkNumSkelecogs(self.quest[1])
        self.checkSkelecogTrack(self.quest[2])

    def getCogNameString(self):
        return SkelecogQBase.getCogNameString(self)

    def doesCogCount(self, avId, cogDict, zoneId, avList):
        return SkelecogQBase.doesCogCount(self, avId, cogDict, zoneId, avList) and self.getCogTrack() == cogDict['track']


class SkelecogLevelQuest(CogLevelQuest, SkelecogQBase):
    def __init__(self, id, quest):
        CogLevelQuest.__init__(self, id, quest)
        self.checkNumSkelecogs(self.quest[1])
        self.checkSkelecogLevel(self.quest[2])

    def getCogType(self):
        return Any

    def getCogNameString(self):
        return SkelecogQBase.getCogNameString(self)

    def doesCogCount(self, avId, cogDict, zoneId, avList):
        level = cogDict['level']
        if level is None:
            level = 1
        return SkelecogQBase.doesCogCount(self, avId, cogDict, zoneId, avList) and self.getCogLevel() <= level


class SkeleReviveQBase:
    def getCogNameString(self):
        numCogs = self.getNumCogs()
        if numCogs == 1:
            return TTLocalizer.Av2Cog
        else:
            return TTLocalizer.v2CogP

    def doesCogCount(self, avId, cogDict, zoneId, avList):
        return cogDict['hasRevives'] and avId in cogDict['activeToons'] and self.isLocationMatch(zoneId)


class SkeleReviveQuest(CogQuest, SkeleReviveQBase):
    def __init__(self, id, quest):
        CogQuest.__init__(self, id, quest)
        self.checkNumSkeleRevives(self.quest[1])

    def getCogType(self):
        return Any

    def getCogNameString(self):
        return SkeleReviveQBase.getCogNameString(self)

    def doesCogCount(self, avId, cogDict, zoneId, avList):
        return SkeleReviveQBase.doesCogCount(self, avId, cogDict, zoneId, avList)


class ForemanQuest(CogQuest):
    def __init__(self, id, quest):
        CogQuest.__init__(self, id, quest)
        self.checkNumForemen(self.quest[1])

    def getCogType(self):
        return Any

    def getCogNameString(self):
        numCogs = self.getNumCogs()
        if numCogs == 1:
            return TTLocalizer.AForeman
        else:
            return TTLocalizer.ForemanP

    def doesCogCount(self, avId, cogDict, zoneId, avList):
        return bool(CogQuest.doesCogCount(self, avId, cogDict, zoneId, avList) and cogDict['isForeman'])


class ForemanNewbieQuest(ForemanQuest, NewbieQuest):
    def __init__(self, id, quest):
        ForemanQuest.__init__(self, id, quest)
        self.checkNewbieLevel(self.quest[2])

    def getNewbieLevel(self):
        return self.quest[2]

    def getString(self):
        return NewbieQuest.getString(self)

    def doesCogCount(self, avId, cogDict, zoneId, avList):
        if ForemanQuest.doesCogCount(self, avId, cogDict, zoneId, avList):
            return self.getNumNewbies(avId, avList)
        else:
            return 0


class VPQuest(CogQuest):
    def __init__(self, id, quest):
        CogQuest.__init__(self, id, quest)
        self.checkNumVPs(self.quest[1])

    def getCogType(self):
        return Any

    def getCogNameString(self):
        numCogs = self.getNumCogs()
        if numCogs == 1:
            return TTLocalizer.ACogVP
        else:
            return TTLocalizer.CogVPs

    def doesCogCount(self, avId, cogDict, zoneId, avList):
        return 0

    def doesVPCount(self, avId, cogDict, zoneId, avList):
        return self.isLocationMatch(zoneId)


class VPNewbieQuest(VPQuest, NewbieQuest):
    def __init__(self, id, quest):
        VPQuest.__init__(self, id, quest)
        self.checkNewbieLevel(self.quest[2])

    def getNewbieLevel(self):
        return self.quest[2]

    def getString(self):
        return NewbieQuest.getString(self)

    def doesVPCount(self, avId, cogDict, zoneId, avList):
        if VPQuest.doesVPCount(self, avId, cogDict, zoneId, avList):
            return self.getNumNewbies(avId, avList)
        else:
            return 0


class SupervisorQuest(CogQuest):
    def __init__(self, id, quest):
        CogQuest.__init__(self, id, quest)
        self.checkNumSupervisors(self.quest[1])

    def getCogType(self):
        return Any

    def getCogNameString(self):
        numCogs = self.getNumCogs()
        if numCogs == 1:
            return TTLocalizer.ASupervisor
        else:
            return TTLocalizer.SupervisorP

    def doesCogCount(self, avId, cogDict, zoneId, avList):
        return bool(CogQuest.doesCogCount(self, avId, cogDict, zoneId, avList) and cogDict['isSupervisor'])


class SupervisorNewbieQuest(SupervisorQuest, NewbieQuest):
    def __init__(self, id, quest):
        SupervisorQuest.__init__(self, id, quest)
        self.checkNewbieLevel(self.quest[2])

    def getNewbieLevel(self):
        return self.quest[2]

    def getString(self):
        return NewbieQuest.getString(self)

    def doesCogCount(self, avId, cogDict, zoneId, avList):
        if SupervisorQuest.doesCogCount(self, avId, cogDict, zoneId, avList):
            return self.getNumNewbies(avId, avList)
        else:
            return 0


class CFOQuest(CogQuest):
    def __init__(self, id, quest):
        CogQuest.__init__(self, id, quest)
        self.checkNumCFOs(self.quest[1])

    def getCogType(self):
        return Any

    def getCogNameString(self):
        numCogs = self.getNumCogs()
        if numCogs == 1:
            return TTLocalizer.ACogCFO
        else:
            return TTLocalizer.CogCFOs

    def doesCogCount(self, avId, cogDict, zoneId, avList):
        return 0

    def doesCFOCount(self, avId, cogDict, zoneId, avList):
        return self.isLocationMatch(zoneId)


class CFONewbieQuest(CFOQuest, NewbieQuest):
    def __init__(self, id, quest):
        CFOQuest.__init__(self, id, quest)
        self.checkNewbieLevel(self.quest[2])

    def getNewbieLevel(self):
        return self.quest[2]

    def getString(self):
        return NewbieQuest.getString(self)

    def doesCFOCount(self, avId, cogDict, zoneId, avList):
        if CFOQuest.doesCFOCount(self, avId, cogDict, zoneId, avList):
            return self.getNumNewbies(avId, avList)
        else:
            return 0


class RescueQuest(VPQuest):
    def __init__(self, id, quest):
        VPQuest.__init__(self, id, quest)

    def getNumToons(self):
        return self.getNumCogs()

    def getProgressString(self, avatar, questDesc):
        if self.getCompletionStatus(avatar, questDesc) == COMPLETE:
            return CompleteString
        elif self.getNumToons() == 1:
            return ''
        else:
            return TTLocalizer.QuestsRescueQuestProgress % {'progress': questDesc[4],
             'numToons': self.getNumToons()}

    def getObjectiveStrings(self):
        numToons = self.getNumCogs()
        if numToons == 1:
            text = TTLocalizer.QuestsRescueQuestToonS
        else:
            text = TTLocalizer.QuestsRescueQuestRescueDesc % {'numToons': numToons}
        return (text,)

    def getString(self):
        return TTLocalizer.QuestsRescueQuestRescue % self.getObjectiveStrings()[0]

    def getSCStrings(self, toNpcId, progress):
        if progress >= self.getNumToons():
            return getFinishToonTaskSCStrings(toNpcId)
        numToons = self.getNumToons()
        if numToons == 1:
            text = TTLocalizer.QuestsRescueQuestSCStringS
        else:
            text = TTLocalizer.QuestsRescueQuestSCStringP
        toonLoc = self.getLocationName()
        return text % {'toonLoc': toonLoc}

    def getHeadlineString(self):
        return TTLocalizer.QuestsRescueQuestHeadline


class RescueNewbieQuest(RescueQuest, NewbieQuest):
    def __init__(self, id, quest):
        RescueQuest.__init__(self, id, quest)
        self.checkNewbieLevel(self.quest[2])

    def getNewbieLevel(self):
        return self.quest[2]

    def getString(self):
        return NewbieQuest.getString(self, newStr=TTLocalizer.QuestsRescueNewNewbieQuestObjective, oldStr=TTLocalizer.QuestsRescueOldNewbieQuestObjective)

    def doesVPCount(self, avId, cogDict, zoneId, avList):
        if RescueQuest.doesVPCount(self, avId, cogDict, zoneId, avList):
            return self.getNumNewbies(avId, avList)
        else:
            return 0


class BuildingQuest(CogQuest):
    trackCodes = ['c',
     'l',
     'm',
     's']
    trackNames = [TTLocalizer.Bossbot,
     TTLocalizer.Lawbot,
     TTLocalizer.Cashbot,
     TTLocalizer.Sellbot]

    def __init__(self, id, quest):
        CogQuest.__init__(self, id, quest)
        self.checkNumBuildings(self.quest[1])
        self.checkBuildingTrack(self.quest[2])
        self.checkBuildingFloors(self.quest[3])

    def getNumFloors(self):
        return self.quest[3]

    def getBuildingTrack(self):
        return self.quest[2]

    def getNumQuestItems(self):
        return self.getNumBuildings()

    def getNumBuildings(self):
        return self.quest[1]

    def getCompletionStatus(self, av, questDesc, npc = None):
        questId, fromNpcId, toNpcId, rewardId, toonProgress = questDesc
        questComplete = toonProgress >= self.getNumBuildings()
        return getCompleteStatusWithNpc(questComplete, toNpcId, npc)

    def getProgressString(self, avatar, questDesc):
        if self.getCompletionStatus(avatar, questDesc) == COMPLETE:
            return CompleteString
        elif self.getNumBuildings() == 1:
            return ''
        else:
            return TTLocalizer.QuestsBuildingQuestProgressString % {'progress': questDesc[4],
             'num': self.getNumBuildings()}

    def getObjectiveStrings(self):
        count = self.getNumBuildings()
        floors = TTLocalizer.QuestsBuildingQuestFloorNumbers[self.getNumFloors() - 1]
        buildingTrack = self.getBuildingTrack()
        if buildingTrack == Any:
            type = TTLocalizer.Cog
        else:
            type = self.trackNames[self.trackCodes.index(buildingTrack)]
        if count == 1:
            if floors == '':
                text = TTLocalizer.QuestsBuildingQuestDesc
            else:
                text = TTLocalizer.QuestsBuildingQuestDescF
        elif floors == '':
            text = TTLocalizer.QuestsBuildingQuestDescC
        else:
            text = TTLocalizer.QuestsBuildingQuestDescCF
        return (text % {'count': count,
          'floors': floors,
          'type': type},)

    def getString(self):
        return TTLocalizer.QuestsBuildingQuestString % self.getObjectiveStrings()[0]

    def getSCStrings(self, toNpcId, progress):
        if progress >= self.getNumBuildings():
            return getFinishToonTaskSCStrings(toNpcId)
        count = self.getNumBuildings()
        floors = TTLocalizer.QuestsBuildingQuestFloorNumbers[self.getNumFloors() - 1]
        buildingTrack = self.getBuildingTrack()
        if buildingTrack == Any:
            type = TTLocalizer.Cog
        else:
            type = self.trackNames[self.trackCodes.index(buildingTrack)]
        if count == 1:
            if floors == '':
                text = TTLocalizer.QuestsBuildingQuestDesc
            else:
                text = TTLocalizer.QuestsBuildingQuestDescF
        elif floors == '':
            text = TTLocalizer.QuestsBuildingQuestDescI
        else:
            text = TTLocalizer.QuestsBuildingQuestDescIF
        objective = text % {'floors': floors,
         'type': type}
        location = self.getLocationName()
        return TTLocalizer.QuestsBuildingQuestSCString % {'objective': objective,
         'location': location}

    def getHeadlineString(self):
        return TTLocalizer.QuestsBuildingQuestHeadline

    def doesCogCount(self, avId, cogDict, zoneId, avList):
        return 0

    def doesBuildingCount(self, avId, avList):
        return 1


class BuildingNewbieQuest(BuildingQuest, NewbieQuest):
    def __init__(self, id, quest):
        BuildingQuest.__init__(self, id, quest)
        self.checkNewbieLevel(self.quest[4])

    def getNewbieLevel(self):
        return self.quest[4]

    def getString(self):
        return NewbieQuest.getString(self)

    def getHeadlineString(self):
        return TTLocalizer.QuestsNewbieQuestHeadline

    def doesBuildingCount(self, avId, avList):
        return self.getNumNewbies(avId, avList)


class FactoryQuest(LocationBasedQuest):
    factoryTypeNames = {FT_FullSuit: TTLocalizer.Cog,
     FT_Leg: TTLocalizer.FactoryTypeLeg,
     FT_Arm: TTLocalizer.FactoryTypeArm,
     FT_Torso: TTLocalizer.FactoryTypeTorso}

    def __init__(self, id, quest):
        LocationBasedQuest.__init__(self, id, quest)
        self.checkNumFactories(self.quest[1])

    def getNumQuestItems(self):
        return self.getNumFactories()

    def getNumFactories(self):
        return self.quest[1]

    def getFactoryType(self):
        loc = self.getLocation()
        type = Any
        if loc in ToontownGlobals.factoryId2factoryType:
            type = ToontownGlobals.factoryId2factoryType[loc]
        return type

    def getCompletionStatus(self, av, questDesc, npc = None):
        questId, fromNpcId, toNpcId, rewardId, toonProgress = questDesc
        questComplete = toonProgress >= self.getNumFactories()
        return getCompleteStatusWithNpc(questComplete, toNpcId, npc)

    def getProgressString(self, avatar, questDesc):
        if self.getCompletionStatus(avatar, questDesc) == COMPLETE:
            return CompleteString
        elif self.getNumFactories() == 1:
            return ''
        else:
            return TTLocalizer.QuestsFactoryQuestProgressString % {'progress': questDesc[4],
             'num': self.getNumFactories()}

    def getObjectiveStrings(self):
        count = self.getNumFactories()
        factoryType = self.getFactoryType()
        if factoryType == Any:
            type = TTLocalizer.Cog
        else:
            type = FactoryQuest.factoryTypeNames[factoryType]
        if count == 1:
            text = TTLocalizer.QuestsFactoryQuestDesc
        else:
            text = TTLocalizer.QuestsFactoryQuestDescC
        return (text % {'count': count,
          'type': type},)

    def getString(self):
        return TTLocalizer.QuestsFactoryQuestString % self.getObjectiveStrings()[0]

    def getSCStrings(self, toNpcId, progress):
        if progress >= self.getNumFactories():
            return getFinishToonTaskSCStrings(toNpcId)
        factoryType = self.getFactoryType()
        if factoryType == Any:
            type = TTLocalizer.Cog
        else:
            type = FactoryQuest.factoryTypeNames[factoryType]
        count = self.getNumFactories()
        if count == 1:
            text = TTLocalizer.QuestsFactoryQuestDesc
        else:
            text = TTLocalizer.QuestsFactoryQuestDescI
        objective = text % {'type': type}
        location = self.getLocationName()
        return TTLocalizer.QuestsFactoryQuestSCString % {'objective': objective,
         'location': location}

    def getHeadlineString(self):
        return TTLocalizer.QuestsFactoryQuestHeadline

    def doesFactoryCount(self, avId, location, avList):
        return self.isLocationMatch(location)


class FactoryNewbieQuest(FactoryQuest, NewbieQuest):
    def __init__(self, id, quest):
        FactoryQuest.__init__(self, id, quest)
        self.checkNewbieLevel(self.quest[2])

    def getNewbieLevel(self):
        return self.quest[2]

    def getString(self):
        return NewbieQuest.getString(self)

    def getHeadlineString(self):
        return TTLocalizer.QuestsNewbieQuestHeadline

    def doesFactoryCount(self, avId, location, avList):
        if FactoryQuest.doesFactoryCount(self, avId, location, avList):
            return self.getNumNewbies(avId, avList)
        else:
            return num


class MintQuest(LocationBasedQuest):
    def __init__(self, id, quest):
        LocationBasedQuest.__init__(self, id, quest)
        self.checkNumMints(self.quest[1])

    def getNumQuestItems(self):
        return self.getNumMints()

    def getNumMints(self):
        return self.quest[1]

    def getCompletionStatus(self, av, questDesc, npc = None):
        questId, fromNpcId, toNpcId, rewardId, toonProgress = questDesc
        questComplete = toonProgress >= self.getNumMints()
        return getCompleteStatusWithNpc(questComplete, toNpcId, npc)

    def getProgressString(self, avatar, questDesc):
        if self.getCompletionStatus(avatar, questDesc) == COMPLETE:
            return CompleteString
        elif self.getNumMints() == 1:
            return ''
        else:
            return TTLocalizer.QuestsMintQuestProgressString % {'progress': questDesc[4],
             'num': self.getNumMints()}

    def getObjectiveStrings(self):
        count = self.getNumMints()
        if count == 1:
            text = TTLocalizer.QuestsMintQuestDesc
        else:
            text = TTLocalizer.QuestsMintQuestDescC % {'count': count}
        return (text,)

    def getString(self):
        return TTLocalizer.QuestsMintQuestString % self.getObjectiveStrings()[0]

    def getSCStrings(self, toNpcId, progress):
        if progress >= self.getNumMints():
            return getFinishToonTaskSCStrings(toNpcId)
        count = self.getNumMints()
        if count == 1:
            objective = TTLocalizer.QuestsMintQuestDesc
        else:
            objective = TTLocalizer.QuestsMintQuestDescI
        location = self.getLocationName()
        return TTLocalizer.QuestsMintQuestSCString % {'objective': objective,
         'location': location}

    def getHeadlineString(self):
        return TTLocalizer.QuestsMintQuestHeadline

    def doesMintCount(self, avId, location, avList):
        return self.isLocationMatch(location)


class StageQuest(MintQuest):

    def getCompletionStatus(self, av, questDesc, npc=None):
        questId, fromNpcId, toNpcId, rewardId, toonProgress = questDesc
        questComplete = toonProgress >= self.getNumMints()
        return getCompleteStatusWithNpc(questComplete, toNpcId, npc)

    def getObjectiveStrings(self):
        count = self.getNumMints()
        if count == 1:
            text = TTLocalizer.QuestsStageQuestDesc
        else:
            text = TTLocalizer.QuestsStageQuestDescC % {'count': count}
        return (text,)

    def getSCStrings(self, toNpcId, progress):
        if progress >= self.getNumMints():
            return getFinishToonTaskSCStrings(toNpcId)
        count = self.getNumMints()
        if count == 1:
            objective = TTLocalizer.QuestsStageQuestDesc
        else:
            objective = TTLocalizer.QuestsStageQuestDescI
        location = self.getLocationName()
        return TTLocalizer.QuestsMintQuestSCString % {'objective': objective,
                                                      'location': location}

    def doesMintCount(self, avId, location, avList):
        return avId in avList


class CountryClubQuest(StageQuest):

    def getObjectiveStrings(self):
        count = self.getNumMints()
        if count == 1:
            text = TTLocalizer.QuestsCountryClubQuestDesc
        else:
            text = TTLocalizer.QuestsStageQuestDescC % {'count': count}
        return (text,)

    def getSCStrings(self, toNpcId, progress):
        if progress >= self.getNumMints():
            return getFinishToonTaskSCStrings(toNpcId)
        count = self.getNumMints()
        if count == 1:
            objective = TTLocalizer.QuestsCountryClubQuestDesc
        else:
            objective = TTLocalizer.QuestsCountryClubQuestDescI
        location = self.getLocationName()
        return TTLocalizer.QuestsMintQuestSCString % {'objective': objective,
                                                      'location': location}

    def doesMintCount(self, avId, location, avList):
        return avId in avList


class MintNewbieQuest(MintQuest, NewbieQuest):
    def __init__(self, id, quest):
        MintQuest.__init__(self, id, quest)
        self.checkNewbieLevel(self.quest[2])

    def getNewbieLevel(self):
        return self.quest[2]

    def getString(self):
        return NewbieQuest.getString(self)

    def getHeadlineString(self):
        return TTLocalizer.QuestsNewbieQuestHeadline

    def doesMintCount(self, avId, location, avList):
        if MintQuest.doesMintCount(self, avId, location, avList):
            return self.getNumNewbies(avId, avList)
        else:
            return num


class CogPartQuest(LocationBasedQuest):
    def __init__(self, id, quest):
        LocationBasedQuest.__init__(self, id, quest)
        self.checkNumCogParts(self.quest[1])

    def getNumQuestItems(self):
        return self.getNumParts()

    def getNumParts(self):
        return self.quest[1]

    def getCompletionStatus(self, av, questDesc, npc = None):
        questId, fromNpcId, toNpcId, rewardId, toonProgress = questDesc
        questComplete = toonProgress >= self.getNumParts()
        return getCompleteStatusWithNpc(questComplete, toNpcId, npc)

    def getProgressString(self, avatar, questDesc):
        if self.getCompletionStatus(avatar, questDesc) == COMPLETE:
            return CompleteString
        elif self.getNumParts() == 1:
            return ''
        else:
            return TTLocalizer.QuestsCogPartQuestProgressString % {'progress': questDesc[4],
             'num': self.getNumParts()}

    def getObjectiveStrings(self):
        count = self.getNumParts()
        if count == 1:
            text = TTLocalizer.QuestsCogPartQuestDesc
        else:
            text = TTLocalizer.QuestsCogPartQuestDescC
        return (text % {'count': count},)

    def getString(self):
        return TTLocalizer.QuestsCogPartQuestString % self.getObjectiveStrings()[0]

    def getSCStrings(self, toNpcId, progress):
        if progress >= self.getNumParts():
            return getFinishToonTaskSCStrings(toNpcId)
        count = self.getNumParts()
        if count == 1:
            text = TTLocalizer.QuestsCogPartQuestDesc
        else:
            text = TTLocalizer.QuestsCogPartQuestDescI
        objective = text
        location = self.getLocationName()
        return TTLocalizer.QuestsCogPartQuestSCString % {'objective': objective,
         'location': location}

    def getHeadlineString(self):
        return TTLocalizer.QuestsCogPartQuestHeadline

    def doesCogPartCount(self, avId, location, avList):
        return self.isLocationMatch(location)


class CogPartNewbieQuest(CogPartQuest, NewbieQuest):
    def __init__(self, id, quest):
        CogPartQuest.__init__(self, id, quest)
        self.checkNewbieLevel(self.quest[2])

    def getNewbieLevel(self):
        return self.quest[2]

    def getString(self):
        return NewbieQuest.getString(self, newStr=TTLocalizer.QuestsCogPartNewNewbieQuestObjective, oldStr=TTLocalizer.QuestsCogPartOldNewbieQuestObjective)

    def getHeadlineString(self):
        return TTLocalizer.QuestsNewbieQuestHeadline

    def doesCogPartCount(self, avId, location, avList):
        if CogPartQuest.doesCogPartCount(self, avId, location, avList):
            return self.getNumNewbies(avId, avList)
        else:
            return num


class DeliverGagQuest(Quest):
    def __init__(self, id, quest):
        Quest.__init__(self, id, quest)
        self.checkNumGags(self.quest[0])
        self.checkGagTrack(self.quest[1])
        self.checkGagItem(self.quest[2])

    def getGagType(self):
        return (self.quest[1], self.quest[2])

    def getNumQuestItems(self):
        return self.getNumGags()

    def getNumGags(self):
        return self.quest[0]

    def getCompletionStatus(self, av, questDesc, npc = None):
        questId, fromNpcId, toNpcId, rewardId, toonProgress = questDesc
        gag = self.getGagType()
        num = self.getNumGags()
        track = gag[0]
        level = gag[1]
        questComplete = npc and av.inventory and av.inventory.numItem(track, level) >= num
        return getCompleteStatusWithNpc(questComplete, toNpcId, npc)

    def getProgressString(self, avatar, questDesc):
        if self.getCompletionStatus(avatar, questDesc) == COMPLETE:
            return CompleteString
        elif self.getNumGags() == 1:
            return ''
        else:
            return TTLocalizer.QuestsDeliverGagQuestProgress % {'progress': questDesc[4],
             'numGags': self.getNumGags()}

    def getObjectiveStrings(self):
        track, item = self.getGagType()
        num = self.getNumGags()
        if num == 1:
            text = ToontownBattleGlobals.AvPropStringsSingular[track][item]
        else:
            gagName = ToontownBattleGlobals.AvPropStringsPlural[track][item]
            text = TTLocalizer.QuestsItemNameAndNum % {'num': TTLocalizer.getLocalNum(num),
             'name': gagName}
        return (text,)

    def getString(self):
        return TTLocalizer.QuestsDeliverGagQuestString % self.getObjectiveStrings()[0]

    def getRewardString(self, progress):
        return TTLocalizer.QuestsDeliverGagQuestStringLong % self.getObjectiveStrings()[0]

    def getDefaultQuestDialog(self):
        return TTLocalizer.QuestsDeliverGagQuestStringLong % self.getObjectiveStrings()[0] + '\x07' + TTLocalizer.QuestsDeliverGagQuestInstructions

    def getSCStrings(self, toNpcId, progress):
        if progress >= self.getNumGags():
            return getFinishToonTaskSCStrings(toNpcId)
        track, item = self.getGagType()
        num = self.getNumGags()
        if num == 1:
            text = TTLocalizer.QuestsDeliverGagQuestToSCStringS
            gagName = ToontownBattleGlobals.AvPropStringsSingular[track][item]
        else:
            text = TTLocalizer.QuestsDeliverGagQuestToSCStringP
            gagName = ToontownBattleGlobals.AvPropStringsPlural[track][item]
        return [text % {'gagName': gagName}, TTLocalizer.QuestsDeliverGagQuestSCString] + getVisitSCStrings(toNpcId)

    def getHeadlineString(self):
        return TTLocalizer.QuestsDeliverGagQuestHeadline


class DeliverItemQuest(Quest):
    def __init__(self, id, quest):
        Quest.__init__(self, id, quest)
        self.checkDeliveryItem(self.quest[0])

    def getItem(self):
        return self.quest[0]

    def getCompletionStatus(self, av, questDesc, npc = None):
        questId, fromNpcId, toNpcId, rewardId, toonProgress = questDesc
        if npc and npcMatches(toNpcId, npc):
            return COMPLETE
        else:
            return INCOMPLETE_WRONG_NPC

    def getProgressString(self, avatar, questDesc):
        return TTLocalizer.QuestsDeliverItemQuestProgress

    def getObjectiveStrings(self):
        iDict = ItemDict[self.getItem()]
        article = iDict[2]
        itemName = iDict[0]
        return [article + itemName]

    def getString(self):
        return TTLocalizer.QuestsDeliverItemQuestString % self.getObjectiveStrings()[0]

    def getRewardString(self, progress):
        return TTLocalizer.QuestsDeliverItemQuestStringLong % self.getObjectiveStrings()[0]

    def getDefaultQuestDialog(self):
        return TTLocalizer.QuestsDeliverItemQuestStringLong % self.getObjectiveStrings()[0]

    def getSCStrings(self, toNpcId, progress):
        iDict = ItemDict[self.getItem()]
        article = iDict[2]
        itemName = iDict[0]
        return [TTLocalizer.QuestsDeliverItemQuestSCString % {'article': article,
          'itemName': itemName}] + getVisitSCStrings(toNpcId)

    def getHeadlineString(self):
        return TTLocalizer.QuestsDeliverItemQuestHeadline


class VisitQuest(Quest):
    def __init__(self, id, quest):
        Quest.__init__(self, id, quest)

    def getCompletionStatus(self, av, questDesc, npc = None):
        questId, fromNpcId, toNpcId, rewardId, toonProgress = questDesc
        if npc and npcMatches(toNpcId, npc):
            return COMPLETE
        else:
            return INCOMPLETE_WRONG_NPC

    def getProgressString(self, avatar, questDesc):
        return TTLocalizer.QuestsVisitQuestProgress

    def getObjectiveStrings(self):
        return ['']

    def getString(self):
        return TTLocalizer.QuestsVisitQuestStringShort

    def getChooseString(self):
        return TTLocalizer.QuestsVisitQuestStringLong

    def getRewardString(self, progress):
        return TTLocalizer.QuestsVisitQuestStringLong

    def getDefaultQuestDialog(self):
        return random.choice(DefaultVisitQuestDialog)

    def getSCStrings(self, toNpcId, progress):
        return getVisitSCStrings(toNpcId)

    def getHeadlineString(self):
        return TTLocalizer.QuestsVisitQuestHeadline


class RecoverItemQuest(LocationBasedQuest):
    def __init__(self, id, quest):
        LocationBasedQuest.__init__(self, id, quest)
        self.checkNumItems(self.quest[1])
        self.checkRecoveryItem(self.quest[2])
        self.checkPercentChance(self.quest[3])
        if len(self.quest) > 5:
            self.checkRecoveryItemHolderAndType(self.quest[4], self.quest[5])
        else:
            self.checkRecoveryItemHolderAndType(self.quest[4])

    def testRecover(self, progress):
        test = random.random() * 100
        chance = self.getPercentChance()
        numberDone = progress & pow(2, 16) - 1
        numberNotDone = progress >> 16
        returnTest = None
        avgNum2Kill = 1.0 / (chance / 100.0)
        if numberNotDone >= avgNum2Kill * 1.5:
            chance = 100
        elif numberNotDone > avgNum2Kill * 0.5:
            diff = float(numberNotDone - avgNum2Kill * 0.5)
            luck = 1.0 + abs(diff / (avgNum2Kill * 0.5))
            chance *= luck
        if test <= chance:
            returnTest = 1
            numberNotDone = 0
            numberDone += 1
        else:
            returnTest = 0
            numberNotDone += 1
            numberDone += 0
        returnCount = numberNotDone << 16
        returnCount += numberDone
        return (returnTest, returnCount)

    def testDone(self, progress):
        numberDone = progress & pow(2, 16) - 1
        print('Quest number done %s' % numberDone)
        if numberDone >= self.getNumItems():
            return 1
        else:
            return 0

    def getNumQuestItems(self):
        return self.getNumItems()

    def getNumItems(self):
        return self.quest[1]

    def getItem(self):
        return self.quest[2]

    def getPercentChance(self):
        return self.quest[3]

    def getHolder(self):
        return self.quest[4]

    def getHolderType(self):
        if len(self.quest) == 5:
            return 'type'
        else:
            return self.quest[5]

    def getCompletionStatus(self, av, questDesc, npc = None):
        questId, fromNpcId, toNpcId, rewardId, toonProgress = questDesc
        forwardProgress = toonProgress & pow(2, 16) - 1
        questComplete = forwardProgress >= self.getNumItems()
        return getCompleteStatusWithNpc(questComplete, toNpcId, npc)

    def getProgressString(self, avatar, questDesc):
        if self.getCompletionStatus(avatar, questDesc) == COMPLETE:
            return CompleteString
        elif self.getNumItems() == 1:
            return ''
        else:
            progress = questDesc[4] & pow(2, 16) - 1
            return TTLocalizer.QuestsRecoverItemQuestProgress % {'progress': progress,
             'numItems': self.getNumItems()}

    def getObjectiveStrings(self):
        holder = self.getHolder()
        holderType = self.getHolderType()
        if holder == Any:
            holderName = TTLocalizer.TheCogs
        elif holder == AnyFish:
            holderName = TTLocalizer.AFish
        elif holderType == 'type':
            holderName = SuitBattleGlobals.getSuitAttributes(holder).plural
        elif holderType == 'level':
            holderName = TTLocalizer.QuestsRecoverItemQuestHolderString % {'level': TTLocalizer.Level,
             'holder': holder,
             'cogs': TTLocalizer.Cogs}
        elif holderType == 'track':
            if holder == 'c':
                holderName = TTLocalizer.BossbotP
            elif holder == 's':
                holderName = TTLocalizer.SellbotP
            elif holder == 'm':
                holderName = TTLocalizer.CashbotP
            elif holder == 'l':
                holderName = TTLocalizer.LawbotP
        item = self.getItem()
        num = self.getNumItems()
        if num == 1:
            itemName = ItemDict[item][2] + ItemDict[item][0]
        else:
            itemName = TTLocalizer.QuestsItemNameAndNum % {'num': TTLocalizer.getLocalNum(num),
             'name': ItemDict[item][1]}
        return [itemName, holderName]

    def getString(self):
        return TTLocalizer.QuestsRecoverItemQuestString % {'item': self.getObjectiveStrings()[0],
         'holder': self.getObjectiveStrings()[1]}

    def getSCStrings(self, toNpcId, progress):
        item = self.getItem()
        num = self.getNumItems()
        forwardProgress = progress & pow(2, 16) - 1
        if forwardProgress >= self.getNumItems():
            if num == 1:
                itemName = ItemDict[item][2] + ItemDict[item][0]
            else:
                itemName = TTLocalizer.QuestsItemNameAndNum % {'num': TTLocalizer.getLocalNum(num),
                 'name': ItemDict[item][1]}
            if toNpcId == ToonHQ:
                strings = [TTLocalizer.QuestsRecoverItemQuestReturnToHQSCString % itemName, TTLocalizer.QuestsRecoverItemQuestGoToHQSCString]
            elif toNpcId:
                npcName, hoodName, buildingArticle, buildingName, toStreet, streetName, isInPlayground = getNpcInfo(toNpcId)
                strings = [TTLocalizer.QuestsRecoverItemQuestReturnToSCString % {'item': itemName,
                  'npcName': npcName}]
                if isInPlayground:
                    strings.append(TTLocalizer.QuestsRecoverItemQuestGoToPlaygroundSCString % hoodName)
                else:
                    strings.append(TTLocalizer.QuestsRecoverItemQuestGoToStreetSCString % {'to': toStreet,
                     'street': streetName,
                     'hood': hoodName})
                strings.extend([TTLocalizer.QuestsRecoverItemQuestVisitBuildingSCString % (buildingArticle, buildingName), TTLocalizer.QuestsRecoverItemQuestWhereIsBuildingSCString % (buildingArticle, buildingName)])
            return strings
        holder = self.getHolder()
        holderType = self.getHolderType()
        locName = self.getLocationName()
        if holder == Any:
            holderName = TTLocalizer.TheCogs
        elif holder == AnyFish:
            holderName = TTLocalizer.TheFish
        elif holderType == 'type':
            holderName = SuitBattleGlobals.getSuitAttributes(holder).plural
        elif holderType == 'level':
            holderName = TTLocalizer.QuestsRecoverItemQuestHolderString % {'level': TTLocalizer.Level,
             'holder': holder,
             'cogs': TTLocalizer.Cogs}
        elif holderType == 'track':
            if holder == 'c':
                holderName = TTLocalizer.BossbotP
            elif holder == 's':
                holderName = TTLocalizer.SellbotP
            elif holder == 'm':
                holderName = TTLocalizer.CashbotP
            elif holder == 'l':
                holderName = TTLocalizer.LawbotP
        if num == 1:
            itemName = ItemDict[item][2] + ItemDict[item][0]
        else:
            itemName = TTLocalizer.QuestsItemNameAndNum % {'num': TTLocalizer.getLocalNum(num),
             'name': ItemDict[item][1]}
        return TTLocalizer.QuestsRecoverItemQuestRecoverFromSCString % {'item': itemName,
         'holder': holderName,
         'loc': locName}

    def getHeadlineString(self):
        return TTLocalizer.QuestsRecoverItemQuestHeadline


class TrackChoiceQuest(Quest):
    def __init__(self, id, quest):
        Quest.__init__(self, id, quest)
        self.checkTrackChoice(self.quest[0])
        self.checkTrackChoice(self.quest[1])

    def getChoices(self):
        return (self.quest[0], self.quest[1])

    def getCompletionStatus(self, av, questDesc, npc = None):
        questId, fromNpcId, toNpcId, rewardId, toonProgress = questDesc
        if npc and npcMatches(toNpcId, npc):
            return COMPLETE
        else:
            return INCOMPLETE_WRONG_NPC

    def getProgressString(self, avatar, questDesc):
        if self.getCompletionStatus(avatar, questDesc) == COMPLETE:
            return CompleteString
        else:
            return NotChosenString

    def getObjectiveStrings(self):
        trackA, trackB = self.getChoices()
        trackAName = ToontownBattleGlobals.Tracks[trackA].capitalize()
        trackBName = ToontownBattleGlobals.Tracks[trackB].capitalize()
        return [trackAName, trackBName]

    def getString(self):
        return TTLocalizer.QuestsTrackChoiceQuestString % {'trackA': self.getObjectiveStrings()[0],
         'trackB': self.getObjectiveStrings()[1]}

    def getSCStrings(self, toNpcId, progress):
        trackA, trackB = self.getChoices()
        trackAName = ToontownBattleGlobals.Tracks[trackA].capitalize()
        trackBName = ToontownBattleGlobals.Tracks[trackB].capitalize()
        return [TTLocalizer.QuestsTrackChoiceQuestSCString % {'trackA': trackAName,
          'trackB': trackBName}, TTLocalizer.QuestsTrackChoiceQuestMaybeSCString % trackAName, TTLocalizer.QuestsTrackChoiceQuestMaybeSCString % trackBName] + getVisitSCStrings(toNpcId)

    def getHeadlineString(self):
        return TTLocalizer.QuestsTrackChoiceQuestHeadline


class FriendQuest(Quest):
    def filterFunc(avatar):
        if len(avatar.getFriendsList()) == 0:
            return 1
        else:
            return 0

    filterFunc = staticmethod(filterFunc)

    def __init__(self, id, quest):
        Quest.__init__(self, id, quest)

    def getCompletionStatus(self, av, questDesc, npc = None):
        questId, fromNpcId, toNpcId, rewardId, toonProgress = questDesc
        questComplete = toonProgress >= 1 or len(av.getFriendsList()) > 0
        return getCompleteStatusWithNpc(questComplete, toNpcId, npc)

    def getProgressString(self, avatar, questDesc):
        if self.getCompletionStatus(avatar, questDesc) == COMPLETE:
            return CompleteString
        else:
            return ''

    def getString(self):
        return TTLocalizer.QuestsFriendQuestString

    def getSCStrings(self, toNpcId, progress):
        if progress:
            return getFinishToonTaskSCStrings(toNpcId)
        return TTLocalizer.QuestsFriendQuestSCString

    def getHeadlineString(self):
        return TTLocalizer.QuestsFriendQuestHeadline

    def getObjectiveStrings(self):
        return [TTLocalizer.QuestsFriendQuestString]

    def doesFriendCount(self, av, otherAv):
        return 1


class FriendNewbieQuest(FriendQuest, NewbieQuest):
    def filterFunc(avatar):
        return 1

    filterFunc = staticmethod(filterFunc)

    def __init__(self, id, quest):
        FriendQuest.__init__(self, id, quest)
        self.checkNumFriends(self.quest[0])
        self.checkNewbieLevel(self.quest[1])

    def getNumQuestItems(self):
        return self.getNumFriends()

    def getNumFriends(self):
        return self.quest[0]

    def getNewbieLevel(self):
        return self.quest[1]

    def getCompletionStatus(self, av, questDesc, npc = None):
        questId, fromNpcId, toNpcId, rewardId, toonProgress = questDesc
        questComplete = toonProgress >= self.getNumFriends()
        return getCompleteStatusWithNpc(questComplete, toNpcId, npc)

    def getProgressString(self, avatar, questDesc):
        if self.getCompletionStatus(avatar, questDesc) == COMPLETE:
            return CompleteString
        elif self.getNumFriends() == 1:
            return ''
        else:
            return TTLocalizer.QuestsFriendNewbieQuestProgress % {'progress': questDesc[4],
             'numFriends': self.getNumFriends()}

    def getString(self):
        return TTLocalizer.QuestsFriendNewbieQuestObjective % self.getNumFriends()

    def getObjectiveStrings(self):
        return [TTLocalizer.QuestsFriendNewbieQuestString % (self.getNumFriends(), self.getNewbieLevel())]

    def doesFriendCount(self, av, otherAv):
        if otherAv != None and otherAv.getMaxHp() <= self.getNewbieLevel():
            return 1
        return 0


class TrolleyQuest(Quest):
    def __init__(self, id, quest):
        Quest.__init__(self, id, quest)

    def getCompletionStatus(self, av, questDesc, npc = None):
        questId, fromNpcId, toNpcId, rewardId, toonProgress = questDesc
        questComplete = toonProgress >= 1
        return getCompleteStatusWithNpc(questComplete, toNpcId, npc)

    def getProgressString(self, avatar, questDesc):
        if self.getCompletionStatus(avatar, questDesc) == COMPLETE:
            return CompleteString
        else:
            return ''

    def getString(self):
        return TTLocalizer.QuestsFriendQuestString

    def getSCStrings(self, toNpcId, progress):
        if progress:
            return getFinishToonTaskSCStrings(toNpcId)
        return TTLocalizer.QuestsTrolleyQuestSCString

    def getHeadlineString(self):
        return TTLocalizer.QuestsTrolleyQuestHeadline

    def getObjectiveStrings(self):
        return [TTLocalizer.QuestsTrolleyQuestString]


class MailboxQuest(Quest):
    def __init__(self, id, quest):
        Quest.__init__(self, id, quest)

    def getCompletionStatus(self, av, questDesc, npc = None):
        questId, fromNpcId, toNpcId, rewardId, toonProgress = questDesc
        questComplete = toonProgress >= 1
        return getCompleteStatusWithNpc(questComplete, toNpcId, npc)

    def getProgressString(self, avatar, questDesc):
        if self.getCompletionStatus(avatar, questDesc) == COMPLETE:
            return CompleteString
        else:
            return ''

    def getString(self):
        return TTLocalizer.QuestsMailboxQuestString

    def getSCStrings(self, toNpcId, progress):
        if progress:
            return getFinishToonTaskSCStrings(toNpcId)
        return TTLocalizer.QuestsMailboxQuestSCString

    def getHeadlineString(self):
        return TTLocalizer.QuestsMailboxQuestHeadline

    def getObjectiveStrings(self):
        return [TTLocalizer.QuestsMailboxQuestString]


class PhoneQuest(Quest):
    def __init__(self, id, quest):
        Quest.__init__(self, id, quest)

    def getCompletionStatus(self, av, questDesc, npc = None):
        questId, fromNpcId, toNpcId, rewardId, toonProgress = questDesc
        questComplete = toonProgress >= 1
        return getCompleteStatusWithNpc(questComplete, toNpcId, npc)

    def getProgressString(self, avatar, questDesc):
        if self.getCompletionStatus(avatar, questDesc) == COMPLETE:
            return CompleteString
        else:
            return ''

    def getString(self):
        return TTLocalizer.QuestsPhoneQuestString

    def getSCStrings(self, toNpcId, progress):
        if progress:
            return getFinishToonTaskSCStrings(toNpcId)
        return TTLocalizer.QuestsPhoneQuestSCString

    def getHeadlineString(self):
        return TTLocalizer.QuestsPhoneQuestHeadline

    def getObjectiveStrings(self):
        return [TTLocalizer.QuestsPhoneQuestString]


class MinigameNewbieQuest(Quest, NewbieQuest):
    def __init__(self, id, quest):
        Quest.__init__(self, id, quest)
        self.checkNumMinigames(self.quest[0])
        self.checkNewbieLevel(self.quest[1])

    def getNumQuestItems(self):
        return self.getNumMinigames()

    def getNumMinigames(self):
        return self.quest[0]

    def getNewbieLevel(self):
        return self.quest[1]

    def getCompletionStatus(self, av, questDesc, npc = None):
        questId, fromNpcId, toNpcId, rewardId, toonProgress = questDesc
        questComplete = toonProgress >= self.getNumMinigames()
        return getCompleteStatusWithNpc(questComplete, toNpcId, npc)

    def getProgressString(self, avatar, questDesc):
        if self.getCompletionStatus(avatar, questDesc) == COMPLETE:
            return CompleteString
        elif self.getNumMinigames() == 1:
            return ''
        else:
            return TTLocalizer.QuestsMinigameNewbieQuestProgress % {'progress': questDesc[4],
             'numMinigames': self.getNumMinigames()}

    def getString(self):
        return TTLocalizer.QuestsMinigameNewbieQuestObjective % self.getNumMinigames()

    def getObjectiveStrings(self):
        return [TTLocalizer.QuestsMinigameNewbieQuestString % self.getNumMinigames()]

    def getHeadlineString(self):
        return TTLocalizer.QuestsNewbieQuestHeadline

    def getSCStrings(self, toNpcId, progress):
        if progress:
            return getFinishToonTaskSCStrings(toNpcId)
        return TTLocalizer.QuestsTrolleyQuestSCString

    def doesMinigameCount(self, av, avList):
        newbieHp = self.getNewbieLevel()
        points = 0
        for toon in avList:
            if toon != av and toon.getMaxHp() <= newbieHp:
                points += 1

        return points


DefaultDialog = {GREETING: DefaultGreeting,
 QUEST: DefaultQuest,
 INCOMPLETE: DefaultIncomplete,
 INCOMPLETE_PROGRESS: DefaultIncompleteProgress,
 INCOMPLETE_WRONG_NPC: DefaultIncompleteWrongNPC,
 COMPLETE: DefaultComplete,
 LEAVING: DefaultLeaving}

def getQuestFromNpcId(id):
    return QuestDict.get(id)[QuestDictFromNpcIndex]


def getQuestToNpcId(id):
    return QuestDict.get(id)[QuestDictToNpcIndex]


def getQuestDialog(id):
    return QuestDict.get(id)[QuestDictDialogIndex]


def getQuestReward(questId):
    baseRewardId = QuestDict.get(questId)[QuestDictRewardIndex]
    return transformReward(baseRewardId)

def isQuestJustForFun(questId, rewardId):
    return True



class APQuestDefinition(NamedTuple):
    questDescription: tuple
    rewardID: int


# Quests are defined like so:
# tier, start, questDesc, fromNpc, toNpc, reward, nextQuest, dialog = quest
# {
#      quest_id: (tier, Start/Cont, (QuestClass, arg1, arg2...), ToonHQ, ToonHQ, rewardID/NA, nextQuestID/NA, dialog/DefaultDialog)
# }

# A quest dict that contains all possible Archipelago quests that NPCs can give
# This dict assumes that no IDs are going to clash with the vanilla QuestDict and would be safe to be merged
# This dict's quest ID scheme is going to follow the same principle as the base one where quest IDs are based on
# Their residing hood, but an offset will be applied to prevent collision
# TTC AP Quests: 15000-15999
# DD AP Quests: 16000-16999
# ...
# DDL AP Quests: 20000-20999

# For our AP Quests definitions, we are only going to provide bare minimum information as all AP quests are literally
# Just simple do one thing types of tasks. If you ever want to use a quest in this dict you should ALWAYS call
# getAPQuest(questId) defined right below this dict, also make sure to check if the return value is not None
# This method will fill in the blanks so that quests have the necessary information consistent with all other quests

# AP Quest Definition = tuple( (QuestClass, arg1, arg2...), rewardID)
__AP_QUEST_DICT: Dict[int, APQuestDefinition] = {

    ### TOONTOWN CENTRAL AP QUESTS

    # Location Check #1 (TTC) defeat some tier 1 cog
    15000: APQuestDefinition((CogQuest, Anywhere, 1, 'f'), 5000),
    15001: APQuestDefinition((CogQuest, Anywhere, 1, 'bf'), 5000),
    15002: APQuestDefinition((CogQuest, Anywhere, 1, 'sc'), 5000),
    15003: APQuestDefinition((CogQuest, Anywhere, 1, 'cc'), 5000),

    # Location Check #2 (TTC) defeat 2 of some dept
    15010: APQuestDefinition((CogTrackQuest, Anywhere, 2, 'c'), 5001),
    15011: APQuestDefinition((CogTrackQuest, Anywhere, 2, 'l'), 5001),
    15012: APQuestDefinition((CogTrackQuest, Anywhere, 2, 'm'), 5001),
    15013: APQuestDefinition((CogTrackQuest, Anywhere, 2, 's'), 5001),

    # Location Check #3 (TTC) Recover 2 Cog Gears from lvl 3 cogs in TTC
    15020: APQuestDefinition((RecoverItemQuest, ToontownGlobals.ToontownCentral, 2, 2007, Easy, 3, "level"), 5002),

    # Location Check #4 (TTC) Defeat 5 cogs on a random TTC street
    15030: APQuestDefinition((CogQuest, ToontownGlobals.PunchlinePlace, 4, Any), 5003),
    15031: APQuestDefinition((CogQuest, ToontownGlobals.LoopyLane, 5, Any), 5003),
    15032: APQuestDefinition((CogQuest, ToontownGlobals.SillyStreet, 6, Any), 5003),

    # Location Check #5 (TTC) Defeat either 3-5 level 2s or 5 cogs in TTC
    15040: APQuestDefinition((CogLevelQuest, ToontownGlobals.ToontownCentral, 3, 2), 5004),
    15041: APQuestDefinition((CogLevelQuest, ToontownGlobals.ToontownCentral, 4, 2), 5004),
    15042: APQuestDefinition((CogLevelQuest, ToontownGlobals.ToontownCentral, 5, 2), 5004),
    15043: APQuestDefinition((CogQuest, ToontownGlobals.ToontownCentral, 5, Any), 5004),

    # Location Check #6 (TTC) Some random tasks
    15050: APQuestDefinition((CogTrackQuest, Anywhere, 3, 'c'), 5005),
    15051: APQuestDefinition((CogQuest, Anywhere, 6, Any), 5005),
    15052: APQuestDefinition((CogLevelQuest, Anywhere, 6, 2), 5005),
    15053: APQuestDefinition((CogQuest, Anywhere, 1, 'b'), 5005),
    15054: APQuestDefinition((CogQuest, Anywhere, 1, 'tm'), 5005),
    15055: APQuestDefinition((RecoverItemQuest, ToontownGlobals.ToontownCentral, 1, 20, Easy, Any, "type",), 5005),
    15056: APQuestDefinition((RecoverItemQuest, ToontownGlobals.ToontownCentral, 2, 20, Easy, Any, "type",), 5005),
    15057: APQuestDefinition((RecoverItemQuest, ToontownGlobals.ToontownCentral, 3, 20, Easy, Any, "type",), 5005),

    # Location Check #7 (TTC) Defeat 2 tier 2 cogs
    15060: APQuestDefinition((CogQuest, Anywhere, 2, 'p'), 5006),
    15061: APQuestDefinition((CogQuest, Anywhere, 2, 'b'), 5006),
    15062: APQuestDefinition((CogQuest, Anywhere, 2, 'pp'), 5006),
    15063: APQuestDefinition((CogQuest, Anywhere, 2, 'tm'), 5006),

    # Location Check #8 (TTC) Some amount of level 2 cogs or recover 3-5 clown car tires from cogs
    15070: APQuestDefinition((CogLevelQuest, Anywhere, 5, 2), 5007),
    15071: APQuestDefinition((CogLevelQuest, Anywhere, 6, 2), 5007),
    15072: APQuestDefinition((CogLevelQuest, Anywhere, 7, 2), 5007),
    15073: APQuestDefinition((RecoverItemQuest, Anywhere, 3, 2007, Easy, 2, "level"), 5007),
    15074: APQuestDefinition((RecoverItemQuest, Anywhere, 4, 2007, Easy, 2, "level"), 5007),
    15075: APQuestDefinition((RecoverItemQuest, Anywhere, 5, 2007, Easy, 2, "level"), 5007),

    # Location Check #9 (TTC) Random Tasks
    15080: APQuestDefinition((CogTrackQuest, Anywhere, 6, 's'), 5008),
    15081: APQuestDefinition((CogTrackQuest, Anywhere, 7, 'l'), 5008),
    15082: APQuestDefinition((CogQuest, Anywhere, 10, Any), 5008),
    15083: APQuestDefinition((CogLevelQuest, Anywhere, 4, 3), 5008),
    15084: APQuestDefinition((CogQuest, Anywhere, 1, 'ym'), 5008),
    15085: APQuestDefinition((CogQuest, Anywhere, 1, 'dt'), 5008),
    15086: APQuestDefinition((RecoverItemQuest, ToontownGlobals.ToontownCentral, 1, 17, Easy, Any, "type",), 5008),
    15087: APQuestDefinition((RecoverItemQuest, ToontownGlobals.ToontownCentral, 2, 17, Easy, Any, "type",), 5008),
    15088: APQuestDefinition((RecoverItemQuest, ToontownGlobals.ToontownCentral, 3, 17, Easy, Any, "type",), 5008),

    # Location Check #10 (TTC) defeat 3 of some dept
    15090: APQuestDefinition((CogTrackQuest, Anywhere, 3, 'c'), 5009),
    15091: APQuestDefinition((CogTrackQuest, Anywhere, 3, 'l'), 5009),
    15092: APQuestDefinition((CogTrackQuest, Anywhere, 3, 'm'), 5009),
    15093: APQuestDefinition((CogTrackQuest, Anywhere, 3, 's'), 5009),

    # Location Check #11 (TTC) defeat some amount of level 3 cogs
    15100: APQuestDefinition((CogLevelQuest, Anywhere, 2, 3), 5010),
    15101: APQuestDefinition((CogLevelQuest, Anywhere, 3, 3), 5010),
    15102: APQuestDefinition((CogLevelQuest, Anywhere, 4, 3), 5010),

    # Location Check #12 (TTC) Defeat some tier 3 cog
    15110: APQuestDefinition((CogQuest, Anywhere, 1, 'ym'), 5011),
    15111: APQuestDefinition((CogQuest, Anywhere, 1, 'dt'), 5011),
    15112: APQuestDefinition((CogQuest, Anywhere, 1, 'tw'), 5011),
    15113: APQuestDefinition((CogQuest, Anywhere, 1, 'nd'), 5011),

    # DONALDS DOCK AP QUESTS

    # Location Check #1 (DD) Defeat 7-10 cogs
    16000: APQuestDefinition((CogQuest, Anywhere, 7, Any), 5012),
    16001: APQuestDefinition((CogQuest, Anywhere, 8, Any), 5012),
    16002: APQuestDefinition((CogQuest, Anywhere, 9, Any), 5012),
    16003: APQuestDefinition((CogQuest, Anywhere, 10, Any), 5012),

    # Location Check #2 (DD) Some variation of defeat x level y cogs in Donald's Dock
    16010: APQuestDefinition((CogLevelQuest, ToontownGlobals.DonaldsDock, 5, 2), 5013),
    16011: APQuestDefinition((CogLevelQuest, ToontownGlobals.DonaldsDock, 6, 2), 5013),
    16012: APQuestDefinition((CogLevelQuest, ToontownGlobals.DonaldsDock, 5, 3), 5013),
    16013: APQuestDefinition((CogLevelQuest, ToontownGlobals.DonaldsDock, 4, 3), 5013),
    16014: APQuestDefinition((CogLevelQuest, ToontownGlobals.DonaldsDock, 3, 4), 5013),

    # Location Check #3 (DD) Defeat a cog building (num, dept, floors) or big white wig from back stabbers
    16020: APQuestDefinition((BuildingQuest, Anywhere, 1, Any, 1), 5014),
    16021: APQuestDefinition((RecoverItemQuest, Anywhere, 1, 2005, Easy, "bs"), 5014),

    # Location Check #4 (DD) Defeat some tier 4 cog
    16030: APQuestDefinition((CogQuest, Anywhere, 1, 'mm'), 5015),
    16031: APQuestDefinition((CogQuest, Anywhere, 1, 'ac'), 5015),
    16032: APQuestDefinition((CogQuest, Anywhere, 1, 'bc'), 5015),
    16033: APQuestDefinition((CogQuest, Anywhere, 1, 'gh'), 5015),

    # Location Check #5 (DD) Defeat x cogs in dept y
    16040: APQuestDefinition((CogTrackQuest, Anywhere, 6, 'c'), 5016),
    16041: APQuestDefinition((CogTrackQuest, Anywhere, 6, 'l'), 5016),
    16042: APQuestDefinition((CogTrackQuest, Anywhere, 6, 'm'), 5016),
    16043: APQuestDefinition((CogTrackQuest, Anywhere, 6, 's'), 5016),

    # Location Check #6 (DD) Defeat x level 6 cogs
    16050: APQuestDefinition((CogLevelQuest, Anywhere, 4, 6), 5017),
    16051: APQuestDefinition((CogLevelQuest, Anywhere, 5, 6), 5017),
    16052: APQuestDefinition((CogLevelQuest, Anywhere, 6, 6), 5017),

    # Location Check #7 (DD) Defeat 7-10 cogs or recover 2-4 sea charts
    16060: APQuestDefinition((CogQuest, Anywhere, 7, Any), 5018),
    16061: APQuestDefinition((CogQuest, Anywhere, 8, Any), 5018),
    16062: APQuestDefinition((CogQuest, Anywhere, 9, Any), 5018),
    16063: APQuestDefinition((CogQuest, Anywhere, 10, Any), 5018),
    16064: APQuestDefinition((RecoverItemQuest, ToontownGlobals.DonaldsDock, 2, 2008, Hard, Any), 5018),
    16065: APQuestDefinition((RecoverItemQuest, ToontownGlobals.DonaldsDock, 3, 2008, Medium, Any), 5018),
    16066: APQuestDefinition((RecoverItemQuest, ToontownGlobals.DonaldsDock, 4, 2008, Medium, Any), 5018),

    # Location Check #8 (DD) Defeat 10 level 3/4 cogs
    16070: APQuestDefinition((CogLevelQuest, Anywhere, 10, 3), 5019),
    16071: APQuestDefinition((CogLevelQuest, Anywhere, 10, 4), 5019),

    # Location Check #9 (DD) Defeat a two story building
    16080: APQuestDefinition((BuildingQuest, Anywhere, 1, Any, 2), 5020),

    # Location Check #10 (DD) Defeat 2 type 3 cogs
    16090: APQuestDefinition((CogQuest, Anywhere, 2, 'ym'), 5021),
    16091: APQuestDefinition((CogQuest, Anywhere, 2, 'dt'), 5021),
    16092: APQuestDefinition((CogQuest, Anywhere, 2, 'tw'), 5021),
    16093: APQuestDefinition((CogQuest, Anywhere, 2, 'nd'), 5021),

    # Location Check #11 (DD) Either 6 of some dept or 10 level 3+ cogs or 15 cogs
    16100: APQuestDefinition((CogLevelQuest, Anywhere, 10, 3), 5022),
    16101: APQuestDefinition((CogQuest, Anywhere, 15, Any), 5022),
    16102: APQuestDefinition((CogTrackQuest, Anywhere, 6, 'c'), 5022),
    16103: APQuestDefinition((CogTrackQuest, Anywhere, 6, 'l'), 5022),
    16104: APQuestDefinition((CogTrackQuest, Anywhere, 6, 'm'), 5022),
    16105: APQuestDefinition((CogTrackQuest, Anywhere, 6, 's'), 5022),

    # Location Check #12 (DD) Defeat x level 5s
    16110: APQuestDefinition((CogLevelQuest, Anywhere, 6, 5), 5023),
    16111: APQuestDefinition((CogLevelQuest, Anywhere, 7, 5), 5023),
    16112: APQuestDefinition((CogLevelQuest, Anywhere, 8, 5), 5023),

    # DAISYS GARDENS TASKS

    # Location Check #1 (DG) Defeat x amount of cogs
    17000: APQuestDefinition((CogQuest, Anywhere, 10, Any), 5024),
    17001: APQuestDefinition((CogQuest, Anywhere, 11, Any), 5024),
    17002: APQuestDefinition((CogQuest, Anywhere, 12, Any), 5024),

    # Location Check #2 (DG) Defeat 5 of some dept
    17010: APQuestDefinition((CogTrackQuest, Anywhere, 5, 'c'), 5025),
    17011: APQuestDefinition((CogTrackQuest, Anywhere, 5, 'l'), 5025),
    17012: APQuestDefinition((CogTrackQuest, Anywhere, 5, 'm'), 5025),
    17013: APQuestDefinition((CogTrackQuest, Anywhere, 5, 's'), 5025),

    # Location Check #3 (DG) Defeat 20 sellbots
    17020: APQuestDefinition((CogTrackQuest, Anywhere, 20, 's'), 5026),

    # Location Check #4 (DG) Defeat x level 6 cogs
    17030: APQuestDefinition((CogLevelQuest, Anywhere, 4, 5), 5027),
    17031: APQuestDefinition((CogLevelQuest, Anywhere, 5, 5), 5027),
    17032: APQuestDefinition((CogLevelQuest, Anywhere, 6, 5), 5027),

    # Location Check #5 (DG) Defeat sellbots cogs on oak street
    17040: APQuestDefinition((CogTrackQuest, ToontownGlobals.OakStreet, 5, 's'), 5028),
    17041: APQuestDefinition((CogTrackQuest, ToontownGlobals.OakStreet, 6, 's'), 5028),
    17042: APQuestDefinition((CogTrackQuest, ToontownGlobals.OakStreet, 7, 's'), 5028),

    # Location Check #6 (DG) Defeat a tier 5 cog
    17050: APQuestDefinition((CogQuest, Anywhere, 1, 'ds'), 5029),
    17051: APQuestDefinition((CogQuest, Anywhere, 1, 'bs'), 5029),
    17052: APQuestDefinition((CogQuest, Anywhere, 1, 'nc'), 5029),
    17053: APQuestDefinition((CogQuest, Anywhere, 1, 'ms'), 5029),

    # Location Check #7 (DD) Defeat x amount of cogs
    17060: APQuestDefinition((CogQuest, Anywhere, 10, Any), 5030),
    17061: APQuestDefinition((CogQuest, Anywhere, 11, Any), 5030),
    17062: APQuestDefinition((CogQuest, Anywhere, 12, Any), 5030),

    # Location Check #8 (DD) Defeat some specific types of cogs or low drop chance memos on oak street
    17070: APQuestDefinition((CogQuest, Anywhere, 1, 'tf'), 5031),
    17071: APQuestDefinition((CogQuest, Anywhere, 2, 'ms'), 5031),
    17072: APQuestDefinition((CogQuest, Anywhere, 3, 'gh'), 5031),
    17073: APQuestDefinition((RecoverItemQuest, ToontownGlobals.OakStreet, 2, 5013, Medium, "s", "track"), 5031),
    17074: APQuestDefinition((RecoverItemQuest, ToontownGlobals.OakStreet, 3, 5013, Medium, "s", "track"), 5031),
    17075: APQuestDefinition((RecoverItemQuest, ToontownGlobals.OakStreet, 4, 5013, Easy, "s", "track"), 5031),

    # Location Check #9 (DG) Infamous recover key from mingler/legal eagles
    17080: APQuestDefinition((RecoverItemQuest, Anywhere, 1, 5012, Medium, "m"), 5032),
    17081: APQuestDefinition((RecoverItemQuest, Anywhere, 1, 5012, Easy, "le"), 5032),

    # Location Check #10 (DG) Defeat x lvl 5s
    17090: APQuestDefinition((CogLevelQuest, Anywhere, 4, 5), 5033),
    17091: APQuestDefinition((CogLevelQuest, Anywhere, 5, 5), 5033),
    17092: APQuestDefinition((CogLevelQuest, Anywhere, 6, 5), 5033),

    # Location Check #11 (DG) Defeat 4 of some suit that isnt sellbot
    17100: APQuestDefinition((CogTrackQuest, Anywhere, 4, 'c'), 5034),
    17101: APQuestDefinition((CogTrackQuest, Anywhere, 4, 'l'), 5034),
    17102: APQuestDefinition((CogTrackQuest, Anywhere, 4, 'm'), 5034),

    # Location Check #12 (DG) Defeat 10 level 6s
    17110: APQuestDefinition((CogLevelQuest, Anywhere, 10, 6), 5035),

    # MINNIE"S MELODYLAND TASKS

    # Location Check #1 (MML) Defeat x amount of cogs
    18000: APQuestDefinition((CogQuest, Anywhere, 8, Any), 5036),
    18001: APQuestDefinition((CogQuest, Anywhere, 10, Any), 5036),
    18002: APQuestDefinition((CogQuest, Anywhere, 12, Any), 5036),

    # Location Check #2 (MML) Random Quests
    18010: APQuestDefinition((CogLevelQuest, Anywhere, 10, 6), 5037),
    18011: APQuestDefinition((CogQuest, Anywhere, 12, Any), 5037),
    18012: APQuestDefinition((CogTrackQuest, Anywhere, 5, 'c'), 5037),
    18013: APQuestDefinition((CogTrackQuest, Anywhere, 5, 'l'), 5037),
    18014: APQuestDefinition((CogTrackQuest, Anywhere, 5, 'm'), 5037),
    18015: APQuestDefinition((CogTrackQuest, Anywhere, 5, 's'), 5037),

    # Location Check #3 (MML) Recover silk ties from tier 7
    18020: APQuestDefinition((RecoverItemQuest, Anywhere, 1, 5001, VeryEasy, "cr"), 5038),
    18021: APQuestDefinition((RecoverItemQuest, Anywhere, 1, 5001, VeryEasy, "m"), 5038),
    18022: APQuestDefinition((RecoverItemQuest, Anywhere, 1, 5001, VeryEasy, "ls"), 5038),
    18023: APQuestDefinition((RecoverItemQuest, Anywhere, 1, 5001, VeryEasy, "le"), 5038),

    # Location Check #4 (MML) Random quests
    18030: APQuestDefinition((CogLevelQuest, Anywhere, 8, 7), 5039),
    18031: APQuestDefinition((CogQuest, Anywhere, 12, Any), 5039),
    18032: APQuestDefinition((CogTrackQuest, Anywhere, 5, 'c'), 5039),
    18033: APQuestDefinition((CogTrackQuest, Anywhere, 5, 'l'), 5039),
    18034: APQuestDefinition((CogTrackQuest, Anywhere, 5, 'm'), 5039),
    18035: APQuestDefinition((CogTrackQuest, Anywhere, 5, 's'), 5039),

    # Location Check #5 (MML) Defeat x amount of cogs in MML
    18040: APQuestDefinition((CogQuest, ToontownGlobals.MinniesMelodyland, 7, Any), 5040),
    18041: APQuestDefinition((CogQuest, ToontownGlobals.MinniesMelodyland, 8, Any), 5040),
    18042: APQuestDefinition((CogQuest, ToontownGlobals.MinniesMelodyland, 9, Any), 5040),
    18043: APQuestDefinition((CogQuest, ToontownGlobals.MinniesMelodyland, 10, Any), 5040),

    # Location Check #6 (MML) Defeat 2 tier 6 cog
    18050: APQuestDefinition((CogQuest, Anywhere, 2, 'hh'), 5041),
    18051: APQuestDefinition((CogQuest, Anywhere, 2, 'sd'), 5041),
    18052: APQuestDefinition((CogQuest, Anywhere, 2, 'mb'), 5041),
    18053: APQuestDefinition((CogQuest, Anywhere, 2, 'tf'), 5041),

    # Location Check #7 (MML) Defeat x amount of lvl 6s
    18060: APQuestDefinition((CogLevelQuest, Anywhere, 4, 6), 5042),
    18061: APQuestDefinition((CogLevelQuest, Anywhere, 5, 6), 5042),
    18062: APQuestDefinition((CogLevelQuest, Anywhere, 6, 6), 5042),

    # Location Check #8 (MML) Defeat 5 cogs of dept x
    18070: APQuestDefinition((CogTrackQuest, Anywhere, 5, 'c'), 5043),
    18071: APQuestDefinition((CogTrackQuest, Anywhere, 5, 'l'), 5043),
    18072: APQuestDefinition((CogTrackQuest, Anywhere, 5, 'm'), 5043),
    18073: APQuestDefinition((CogTrackQuest, Anywhere, 5, 's'), 5043),

    # Location Check #9 (MML) Defeat a level 9 cog
    18080: APQuestDefinition((CogLevelQuest, Anywhere, 1, 9), 5044),

    # Location Check #10 (MML) Defeat x amount of level y cogs anywhere
    18090: APQuestDefinition((CogLevelQuest, Anywhere, 5, 6), 5045),
    18091: APQuestDefinition((CogLevelQuest, Anywhere, 5, 5), 5045),
    18092: APQuestDefinition((CogLevelQuest, Anywhere, 6, 6), 5045),
    18093: APQuestDefinition((CogLevelQuest, Anywhere, 6, 5), 5045),

    # Location Check #11 (MML) Random Quests
    18100: APQuestDefinition((CogLevelQuest, Anywhere, 10, 3), 5046),
    18101: APQuestDefinition((CogQuest, Anywhere, 15, Any), 5046),
    18102: APQuestDefinition((CogTrackQuest, Anywhere, 6, 'c'), 5046),
    18103: APQuestDefinition((CogTrackQuest, Anywhere, 6, 'l'), 5046),
    18104: APQuestDefinition((CogTrackQuest, Anywhere, 6, 'm'), 5046),
    18105: APQuestDefinition((CogTrackQuest, Anywhere, 6, 's'), 5046),

    # Location Check #12 (MML) Defeat 25 cogs
    18110: APQuestDefinition((CogQuest, Anywhere, 25, Any), 5047),

    ### THE BRRRGH AP TASKS

    # Location Check #1 (TB) Defeat x amount of cogs
    19000: APQuestDefinition((CogQuest, Anywhere, 8, Any), 5048),
    19001: APQuestDefinition((CogQuest, Anywhere, 10, Any), 5048),
    19002: APQuestDefinition((CogQuest, Anywhere, 12, Any), 5048),

    # Location Check #2 (TB) Random Quests
    19010: APQuestDefinition((CogLevelQuest, Anywhere, 7, 7), 5049),
    19011: APQuestDefinition((CogQuest, Anywhere, 12, Any), 5049),
    19012: APQuestDefinition((CogTrackQuest, Anywhere, 5, 'c'), 5049),
    19013: APQuestDefinition((CogTrackQuest, Anywhere, 5, 'l'), 5049),
    19014: APQuestDefinition((CogTrackQuest, Anywhere, 5, 'm'), 5049),
    19015: APQuestDefinition((CogTrackQuest, Anywhere, 5, 's'), 5049),

    # Location Check #3 (TB) Defeat 20 lawbots anywhere
    19020: APQuestDefinition((CogTrackQuest, Anywhere, 20, 'l'), 5050),

    # Location Check #4 (TB) Recover 2 fuzzy dice from lvl 8 cogs
    19030: APQuestDefinition((RecoverItemQuest, Anywhere, 2, 3018, Medium, 8, "level"), 5051),

    # Location Check #5 (TB) Defeat 7 Lawbots in the brrrgh
    19040: APQuestDefinition((CogTrackQuest, ToontownGlobals.TheBrrrgh, 7, 'l'), 5052),

    # Location Check #6 (TB) Recover Platform shoes from random tier 8 cog
    19050: APQuestDefinition((RecoverItemQuest, Anywhere, 1, 3021, VeryEasy, "tbc"), 5053),
    19051: APQuestDefinition((RecoverItemQuest, Anywhere, 1, 3021, VeryEasy, "bw"), 5053),
    19052: APQuestDefinition((RecoverItemQuest, Anywhere, 1, 3021, VeryEasy, "rb"), 5053),
    19053: APQuestDefinition((RecoverItemQuest, Anywhere, 1, 3021, VeryEasy, "mh"), 5053),

    # Location Check #7 (TB) Random Quests
    19060: APQuestDefinition((CogLevelQuest, Anywhere, 6, 8), 5054),
    19061: APQuestDefinition((CogQuest, Anywhere, 10, Any), 5054),
    19062: APQuestDefinition((CogTrackQuest, Anywhere, 5, 'c'), 5054),
    19063: APQuestDefinition((CogTrackQuest, Anywhere, 5, 'l'), 5054),
    19064: APQuestDefinition((CogTrackQuest, Anywhere, 5, 'm'), 5054),
    19065: APQuestDefinition((CogTrackQuest, Anywhere, 5, 's'), 5054),

    # Location Check #8 (TB) Defeat x cogs of type y on polar place
    19070: APQuestDefinition((CogQuest, ToontownGlobals.PolarPlace, 1, 'sd'), 5055),
    19071: APQuestDefinition((CogQuest, ToontownGlobals.PolarPlace, 2, 'bs'), 5055),

    # Location Check #9 (TB) Recover external temp sensors
    19080: APQuestDefinition((RecoverItemQuest, Anywhere, 7, 3027, Medium, Any), 5056),
    19081: APQuestDefinition((RecoverItemQuest, Anywhere, 12, 3027, Easy, Any), 5056),
    19082: APQuestDefinition((RecoverItemQuest, Anywhere, 20, 3027, VeryEasy, Any), 5056),

    # Location Check #10 (TB) Defeat x amount of level 7 cogs
    19090: APQuestDefinition((CogLevelQuest, Anywhere, 6, 7), 5057),
    19091: APQuestDefinition((CogLevelQuest, Anywhere, 7, 7), 5057),
    19092: APQuestDefinition((CogLevelQuest, Anywhere, 8, 7), 5057),

    # Location Check #11 (TB) Random Quests
    19100: APQuestDefinition((CogLevelQuest, Anywhere, 5, 8), 5058),
    19101: APQuestDefinition((CogQuest, Anywhere, 15, Any), 5058),
    19102: APQuestDefinition((CogTrackQuest, Anywhere, 6, 'c'), 5058),
    19103: APQuestDefinition((CogTrackQuest, Anywhere, 6, 'l'), 5058),
    19104: APQuestDefinition((CogTrackQuest, Anywhere, 6, 'm'), 5058),
    19105: APQuestDefinition((CogTrackQuest, Anywhere, 6, 's'), 5058),

    # Location Check #12 (TB) Defeat a 5 story building
    19110: APQuestDefinition((BuildingQuest, Anywhere, 1, Any, 5), 5059),

    ### DDL AP TASKS

    # Location Check #1 (DDL) Defeat x amount of cogs
    20000: APQuestDefinition((CogQuest, Anywhere, 15, Any), 5060),
    20001: APQuestDefinition((CogQuest, Anywhere, 16, Any), 5060),
    20002: APQuestDefinition((CogQuest, Anywhere, 17, Any), 5060),
    20003: APQuestDefinition((CogQuest, Anywhere, 18, Any), 5060),

    # Location Check #2 (DDL) Defeat x amount of cogs at level y
    20010: APQuestDefinition((CogLevelQuest, Anywhere, 8, 7), 5061),
    20011: APQuestDefinition((CogLevelQuest, Anywhere, 7, 8), 5061),
    20012: APQuestDefinition((CogLevelQuest, Anywhere, 6, 9), 5061),
    20013: APQuestDefinition((CogLevelQuest, Anywhere, 5, 10), 5061),

    # Location Check #3 (DDL) Defeat 20 cashbots
    20020: APQuestDefinition((CogTrackQuest, Anywhere, 20, 'm'), 5062),

    # Location Check #4 (DDL) Defeat x amount of cogs at level y
    20030: APQuestDefinition((CogLevelQuest, Anywhere, 7, 6), 5063),
    20031: APQuestDefinition((CogLevelQuest, Anywhere, 6, 7), 5063),
    20032: APQuestDefinition((CogLevelQuest, Anywhere, 5, 8), 5063),
    20033: APQuestDefinition((CogLevelQuest, Anywhere, 4, 9), 5063),

    # Location Check #5 (DDL) Defeat x amount of cogs at level y
    20040: APQuestDefinition((CogLevelQuest, Anywhere, 2, 10), 5064),
    20041: APQuestDefinition((CogLevelQuest, Anywhere, 3, 9), 5064),
    20042: APQuestDefinition((CogLevelQuest, Anywhere, 5, 8), 5064),
    20043: APQuestDefinition((CogLevelQuest, Anywhere, 7, 7), 5064),

    # Location Check #6 (DDL) Defeat a random tier 8 cog
    20050: APQuestDefinition((CogQuest, Anywhere, 1, 'tbc'), 5065),
    20051: APQuestDefinition((CogQuest, Anywhere, 1, 'bw'), 5065),
    20052: APQuestDefinition((CogQuest, Anywhere, 1, 'rb'), 5065),
    20053: APQuestDefinition((CogQuest, Anywhere, 1, 'mh'), 5065),

    # Location Check #7 (DDL) Defeat 10 cashbots on pajama place or cashbot plans
    20060: APQuestDefinition((CogTrackQuest, ToontownGlobals.PajamaPlace, 10, 'm'), 5066),
    20061: APQuestDefinition((RecoverItemQuest, ToontownGlobals.PajamaPlace, 5, 6001, Medium, "m", "track"), 5066),

    # Location Check #8 (DDL) Defeat x amount of cogs
    20070: APQuestDefinition((CogQuest, Anywhere, 13, Any), 5067),
    20071: APQuestDefinition((CogQuest, Anywhere, 15, Any), 5067),
    20072: APQuestDefinition((CogQuest, Anywhere, 17, Any), 5067),
    20073: APQuestDefinition((CogQuest, Anywhere, 19, Any), 5067),

    # Location Check #9 (DDL) Defeat 4 level 11+ cogs or 7 level 10+
    20080: APQuestDefinition((CogLevelQuest, Anywhere, 4, 11), 5068),
    20081: APQuestDefinition((CogLevelQuest, Anywhere, 7, 10), 5068),

    # Location Check #10 (DDL) Defeat x amount of cogs or recover pajamas
    20090: APQuestDefinition((CogQuest, Anywhere, 10, Any), 5069),
    20091: APQuestDefinition((CogQuest, Anywhere, 14, Any), 5069),
    20092: APQuestDefinition((CogQuest, Anywhere, 18, Any), 5069),
    20093: APQuestDefinition((RecoverItemQuest, Anywhere, 5, 7007, Medium, Any), 5069),
    20094: APQuestDefinition((RecoverItemQuest, Anywhere, 7, 7007, Medium, Any), 5069),
    20095: APQuestDefinition((RecoverItemQuest, Anywhere, 9, 7007, Medium, Any), 5069),

    # Location Check #11 (DDL) Defeat x cogs of type y in DDL
    20100: APQuestDefinition((CogQuest, ToontownGlobals.DonaldsDreamland, 1, 'mb'), 5070),
    20101: APQuestDefinition((CogQuest, ToontownGlobals.DonaldsDreamland, 2, 'nc'), 5070),
    20102: APQuestDefinition((CogQuest, ToontownGlobals.DonaldsDreamland, 3, 'bc'), 5070),

    # Location Check #12 (DDL) Recover Hard Pillows from level 9s in DDL (very low drop chance)
    20110: APQuestDefinition((RecoverItemQuest, ToontownGlobals.DonaldsDreamland, 2, 7006, VeryHard, 9, "level"), 5071),
    20111: APQuestDefinition((RecoverItemQuest, ToontownGlobals.DonaldsDreamland, 4, 7006, Medium, 9, "level"), 5071),

}


# Gets an entry from the AP Quest Dict and transforms it into a normal toontown quest as if it was defined in QuestDict
def getAPQuest(questId: int):

    apQuest: APQuestDefinition = __AP_QUEST_DICT.get(questId)
    if apQuest is None:
        return None

    # Now format it as if it was a normal quest
    # AP tier, start of a quest, from and to NPC is HQ officer, No next quest, and default dialog

    quest = (AP_TIER, Start, apQuest.questDescription, ToonHQ, ToonHQ, apQuest.rewardID, NA, DefaultDialog)
    return quest

# All the registered quests in the game. If you want the legacy TTO quests, see LegacyQuestDict

QuestDict = {

}

# For Archipelago purposes, we only need archipelago quests to be registered in the game
for questID, questDefinition in __AP_QUEST_DICT.items():
    quest = getAPQuest(questID)
    QuestDict[questID] = quest

WANT_LEGACY_QUESTS = False
# If we want the original quests, simply just extend the quest dict above
if WANT_LEGACY_QUESTS:
    from toontown.quest import LegacyQuestDict
    for key, value in LegacyQuestDict.QuestDict.items():
        QuestDict[key] = value



Quest2RewardDict = {}
Tier2Reward2QuestsDict = {}
Quest2RemainingStepsDict = {}

def getAllRewardIdsForReward(rewardId):
    if rewardId is AnyCashbotSuitPart:
        return list(range(4000, 4011 + 1))
    if rewardId is AnyLawbotSuitPart:
        return list(range(4100, 4113 + 1))
    if rewardId is AnyBossbotSuitPart:
        return list(range(4200, 4216 + 1))
    return (rewardId,)


def findFinalRewardId(questID, depth=0):

    questDesc = QuestDict.get(questID)
    if questDesc is None:
        return -1, -1

    nextQuest = questDesc[QuestDictNextQuestIndex]

    if nextQuest == NA:
        return questDesc[QuestDictRewardIndex], depth

    return findFinalRewardId(nextQuest, depth+1)


for questId in list(QuestDict.keys()):
    findFinalRewardId(questId)


def getFinalRewardId(questId, fAll = 0):
    if fAll or isStartingQuest(questId):
        return Quest2RewardDict.get(questId)
    else:
        return None

    return None


def isStartingQuest(questId):
    try:
        return QuestDict[questId][QuestDictStartIndex] == Start
    except KeyError:
        return None

    return None


def getNumChoices(tier):
    if tier in (0,):
        return 0
    if tier in (1,):
        return 2
    else:
        return 3


def getAvatarRewardId(av, questId):
    for quest in av.quests:
        if questId == quest[0]:
            return quest[3]

    notify.warning('getAvatarRewardId(): quest not found on avatar')
    return None


def getNextQuest(id, currentNpc, av):
    nextQuest = QuestDict[id][QuestDictNextQuestIndex]
    if nextQuest == NA:
        return (NA, NA)

    if not getQuestClass(nextQuest).filterFunc(av):
        return getNextQuest(nextQuest, currentNpc, av)

    nextToNpcId = getQuestToNpcId(nextQuest)
    if nextToNpcId == Any:
        nextToNpcId = 2004
    elif nextToNpcId == Same:
        if currentNpc.getHq():
            nextToNpcId = ToonHQ
        else:
            nextToNpcId = currentNpc.getNpcId()
    elif nextToNpcId == ToonHQ:
        nextToNpcId = ToonHQ
    return nextQuest, nextToNpcId


def transformReward(baseRewardId):
    return baseRewardId


# Called when we talk to an HQ Officer, which quests should we offer the player?
# Pass in the NPC, the toon to give quests for, and a list of reward IDs to ignore
def chooseBestQuests(currentNpc, av, excludeRewards: List[int], seed=None):

    # If this is not an HQ npc, ignore them
    if not currentNpc.getHq():
        return []

    # Get the hood ID this HQ officer is residing in and use it to find the locations this playground offers
    hoodId = ZoneUtil.getHoodId(currentNpc.zoneId)

    # What AP locations can this hood offer for us?
    allHoodTaskLocationNames = util.hood_to_task_locations(hoodId)

    # Use the index of this NPC to choose ideal quests
    npcHQIndex = currentNpc.getPositionIndex()

    # Quests in each playground are 12 quests each, meaning we should have gotten a list of 12 location names
    # This NPC will offer 3 of those. Find some offset and offer that subsection of all the tasks
    taskLocationOffset = npcHQIndex * 3
    taskLocationEnd = taskLocationOffset + 3
    # Splice the list to choose 3 tasks we want, this should splice like so: 0-2, 3-5, 6-8, 9-11
    locationsWeOffer = allHoodTaskLocationNames[taskLocationOffset:taskLocationEnd]

    # Now convert these AP locations into base Toontown quest reward items
    rewardsFromLocation = []
    for location in locationsWeOffer:

        # If the player has already checked the location via AP, they do not need to do this quest
        locationID = util.ap_location_name_to_id(location)
        if av.hasCheckedLocation(locationID):
            continue

        convertedRewardID = getRewardIdFromAPLocationName(location)

        # If we want to exclude this reward ID for whatever reason, do not include it
        if convertedRewardID in excludeRewards:
            continue

        # This quest will be valid for our player to grab
        rewardsFromLocation.append(convertedRewardID)

    # Now that we have the rewards these quests choices should give, let's generate some options
    # These need to be formatted like so for the QuestMgr to process them correctly:
    # Return a list of Quests like so:
    # We only need a questID and a rewardID essentially
    # [
    #   [bestQuestId, rewardId, ToonHQ],
    #   [bestQuestId, rewardId, ToonHQ],
    #   [bestQuestId, rewardId, ToonHQ],
    # ]

    # RNG seeding
    rng = random.Random()
    if seed is not None:
        rng.seed(seed)

    # Define our pool of quests per reward ID
    questPool: Dict[int, List[int]] = {}  # Reward ID -> List of Quest IDs with reward
    for rewardID in rewardsFromLocation:
        questPool[rewardID] = []

    # Loop through every quest in the game and find quests that have a reward we are interested in
    for questId, questInformation in QuestDict.items():
        thisQuestReward = questInformation[QuestDictRewardIndex]
        # Does the reward match one of the ones we have?
        if thisQuestReward in questPool:
            questPool[thisQuestReward].append(questId)

    bestQuests = []

    # Now randomly choose a quest per reward ID that we want to show
    for rewardID, questIdChoices in questPool.items():
        randomQuest = rng.choice(questIdChoices)
        bestQuests.append([randomQuest, rewardID, ToonHQ])

    # Reverse the list bc it looks better for the client lol
    bestQuests.reverse()

    return bestQuests


def getQuest(id):
    questEntry = QuestDict.get(id)
    if questEntry:
        questDesc = questEntry[QuestDictDescIndex]
        questClass = questDesc[0]
        return questClass(id, questDesc[1:])
    else:
        return None
    return None


def getQuestClass(id):
    questEntry = QuestDict.get(id)
    if questEntry:
        return questEntry[QuestDictDescIndex][0]
    else:
        return None
    return None


def getVisitSCStrings(npcId):
    if npcId == ToonHQ:
        strings = [TTLocalizer.QuestsRecoverItemQuestSeeHQSCString, TTLocalizer.QuestsRecoverItemQuestGoToHQSCString]
    elif npcId == ToonTailor:
        strings = [TTLocalizer.QuestsTailorQuestSCString]
    elif npcId:
        npcName, hoodName, buildingArticle, buildingName, toStreet, streetName, isInPlayground = getNpcInfo(npcId)
        strings = [TTLocalizer.QuestsVisitQuestSeeSCString % npcName]
        if isInPlayground:
            strings.append(TTLocalizer.QuestsRecoverItemQuestGoToPlaygroundSCString % hoodName)
        else:
            strings.append(TTLocalizer.QuestsRecoverItemQuestGoToStreetSCString % {'to': toStreet,
             'street': streetName,
             'hood': hoodName})
        strings.extend([TTLocalizer.QuestsRecoverItemQuestVisitBuildingSCString % (buildingArticle, buildingName), TTLocalizer.QuestsRecoverItemQuestWhereIsBuildingSCString % (buildingArticle, buildingName)])
    return strings


def getFinishToonTaskSCStrings(npcId):
    return [TTLocalizer.QuestsGenericFinishSCString] + getVisitSCStrings(npcId)


def chooseQuestDialog(id, status):
    questDialog = getQuestDialog(id).get(status)
    if questDialog == None:
        if status == QUEST:
            quest = getQuest(id)
            questDialog = quest.getDefaultQuestDialog()
        else:
            questDialog = DefaultDialog[status]
    if type(questDialog) == type(()):
        return random.choice(questDialog)
    else:
        return questDialog
    return


def chooseQuestDialogReject():
    return random.choice(DefaultReject)


def chooseQuestDialogTierNotDone():
    return random.choice(DefaultTierNotDone)


def getNpcInfo(npcId):
    npcName = NPCToons.getNPCName(npcId)
    npcZone = NPCToons.getNPCZone(npcId)
    hoodId = ZoneUtil.getCanonicalHoodId(npcZone)
    hoodName = base.cr.hoodMgr.getFullnameFromId(hoodId)
    buildingArticle = NPCToons.getBuildingArticle(npcZone)
    buildingName = NPCToons.getBuildingTitle(npcZone)
    branchId = ZoneUtil.getCanonicalBranchZone(npcZone)
    toStreet = ToontownGlobals.StreetNames[branchId][0]
    streetName = ToontownGlobals.StreetNames[branchId][-1]
    isInPlayground = ZoneUtil.isPlayground(branchId)
    return (npcName,
     hoodName,
     buildingArticle,
     buildingName,
     toStreet,
     streetName,
     isInPlayground)


def getNpcLocationDialog(fromNpcId, toNpcId):
    if not toNpcId:
        return (None, None, None)
    fromNpcZone = None
    fromBranchId = None
    if fromNpcId:
        fromNpcZone = NPCToons.getNPCZone(fromNpcId)
        fromBranchId = ZoneUtil.getCanonicalBranchZone(fromNpcZone)
    toNpcZone = NPCToons.getNPCZone(toNpcId)
    toBranchId = ZoneUtil.getCanonicalBranchZone(toNpcZone)
    toNpcName, toHoodName, toBuildingArticle, toBuildingName, toStreetTo, toStreetName, isInPlayground = getNpcInfo(toNpcId)
    if fromBranchId == toBranchId:
        if isInPlayground:
            streetDesc = TTLocalizer.QuestsStreetLocationThisPlayground
        else:
            streetDesc = TTLocalizer.QuestsStreetLocationThisStreet
    elif isInPlayground:
        streetDesc = TTLocalizer.QuestsStreetLocationNamedPlayground % toHoodName
    else:
        streetDesc = TTLocalizer.QuestsStreetLocationNamedStreet % {'toStreetName': toStreetName,
         'toHoodName': toHoodName}
    paragraph = TTLocalizer.QuestsLocationParagraph % {'building': TTLocalizer.QuestsLocationBuilding % toNpcName,
     'buildingName': toBuildingName,
     'buildingVerb': TTLocalizer.QuestsLocationBuildingVerb,
     'street': streetDesc}
    return (paragraph, toBuildingName, streetDesc)


def fillInQuestNames(text, avName = None, fromNpcId = None, toNpcId = None):
    text = copy.deepcopy(text)
    if avName != None:
        text = text.replace('_avName_', avName)
    if toNpcId:
        if toNpcId == ToonHQ:
            toNpcName = TTLocalizer.QuestsHQOfficerFillin
            where = TTLocalizer.QuestsHQWhereFillin
            buildingName = TTLocalizer.QuestsHQBuildingNameFillin
            streetDesc = TTLocalizer.QuestsHQLocationNameFillin
        elif toNpcId == ToonTailor:
            toNpcName = TTLocalizer.QuestsTailorFillin
            where = TTLocalizer.QuestsTailorWhereFillin
            buildingName = TTLocalizer.QuestsTailorBuildingNameFillin
            streetDesc = TTLocalizer.QuestsTailorLocationNameFillin
        else:
            toNpcName = str(NPCToons.getNPCName(toNpcId))
            where, buildingName, streetDesc = getNpcLocationDialog(fromNpcId, toNpcId)

        text = text.replace('_toNpcName_', toNpcName)
        text = text.replace('_where_', where)
        text = text.replace('_buildingName_', buildingName)
        text = text.replace('_streetDesc_', streetDesc)
    return text


def getVisitingQuest():
    return VisitQuest(VISIT_QUEST_ID)


class Reward:
    def __init__(self, id, reward):
        self.id = id
        self.reward = reward

    def getId(self):
        return self.id

    def getType(self):
        return self.__class__

    def getAmount(self):
        return None

    def sendRewardAI(self, av):
        raise NotImplementedError

    def countReward(self, qrc):
        raise NotImplementedError

    def getString(self):
        return 'undefined'

    def getPosterString(self):
        return 'base class'


class MaxHpReward(Reward):
    def __init__(self, id, reward):
        Reward.__init__(self, id, reward)

    def getAmount(self):
        return self.reward[0]

    def sendRewardAI(self, av):
        # maxHp = av.getMaxHp()
        # maxHp = min(ToontownGlobals.MaxHpLimit, maxHp + self.getAmount())
        # av.b_setMaxHp(maxHp)
        # av.toonUp(maxHp)
        pass

    def countReward(self, qrc):
        qrc.maxHp += self.getAmount()

    def getString(self):
        return TTLocalizer.QuestsMaxHpReward % self.getAmount()

    def getPosterString(self):
        return TTLocalizer.QuestsMaxHpRewardPoster % self.getAmount()


class MoneyReward(Reward):
    def __init__(self, id, reward):
        Reward.__init__(self, id, reward)

    def getAmount(self):
        return self.reward[0]

    def sendRewardAI(self, av):
        money = av.getMoney()
        maxMoney = av.getMaxMoney()
        av.addMoney(self.getAmount())

    def countReward(self, qrc):
        qrc.money += self.getAmount()

    def getString(self):
        amt = self.getAmount()
        if amt == 1:
            return TTLocalizer.QuestsMoneyRewardSingular
        else:
            return TTLocalizer.QuestsMoneyRewardPlural % amt

    def getPosterString(self):
        amt = self.getAmount()
        if amt == 1:
            return TTLocalizer.QuestsMoneyRewardPosterSingular
        else:
            return TTLocalizer.QuestsMoneyRewardPosterPlural % amt


class MaxMoneyReward(Reward):
    def __init__(self, id, reward):
        Reward.__init__(self, id, reward)

    def getAmount(self):
        return self.reward[0]

    def sendRewardAI(self, av):
        av.b_setMaxMoney(self.getAmount())

    def countReward(self, qrc):
        qrc.maxMoney = self.getAmount()

    def getString(self):
        amt = self.getAmount()
        if amt == 1:
            return TTLocalizer.QuestsMaxMoneyRewardSingular
        else:
            return TTLocalizer.QuestsMaxMoneyRewardPlural % amt

    def getPosterString(self):
        amt = self.getAmount()
        if amt == 1:
            return TTLocalizer.QuestsMaxMoneyRewardPosterSingular
        else:
            return TTLocalizer.QuestsMaxMoneyRewardPosterPlural % amt


class MaxGagCarryReward(Reward):
    def __init__(self, id, reward):
        Reward.__init__(self, id, reward)

    def getAmount(self):
        return self.reward[0]

    def getName(self):
        return self.reward[1]

    def sendRewardAI(self, av):
        av.b_setMaxCarry(self.getAmount())

    def countReward(self, qrc):
        qrc.maxCarry = self.getAmount()

    def getString(self):
        name = self.getName()
        amt = self.getAmount()
        return TTLocalizer.QuestsMaxGagCarryReward % {'name': name,
         'num': amt}

    def getPosterString(self):
        name = self.getName()
        amt = self.getAmount()
        return TTLocalizer.QuestsMaxGagCarryRewardPoster % {'name': name,
         'num': amt}


class MaxQuestCarryReward(Reward):
    def __init__(self, id, reward):
        Reward.__init__(self, id, reward)

    def getAmount(self):
        return self.reward[0]

    def sendRewardAI(self, av):
        av.b_setQuestCarryLimit(self.getAmount())

    def countReward(self, qrc):
        qrc.questCarryLimit = self.getAmount()

    def getString(self):
        amt = self.getAmount()
        return TTLocalizer.QuestsMaxQuestCarryReward % amt

    def getPosterString(self):
        amt = self.getAmount()
        return TTLocalizer.QuestsMaxQuestCarryRewardPoster % amt


class TeleportReward(Reward):
    def __init__(self, id, reward):
        Reward.__init__(self, id, reward)

    def getZone(self):
        return self.reward[0]

    def sendRewardAI(self, av):
        av.addTeleportAccess(self.getZone())

    def countReward(self, qrc):
        qrc.addTeleportAccess(self.getZone())

    def getString(self):
        hoodName = ToontownGlobals.hoodNameMap[self.getZone()][-1]
        return TTLocalizer.QuestsTeleportReward % hoodName

    def getPosterString(self):
        hoodName = ToontownGlobals.hoodNameMap[self.getZone()][-1]
        return TTLocalizer.QuestsTeleportRewardPoster % hoodName


TrackTrainingQuotas = {ToontownBattleGlobals.HEAL_TRACK: 15,
 ToontownBattleGlobals.TRAP_TRACK: 15,
 ToontownBattleGlobals.LURE_TRACK: 15,
 ToontownBattleGlobals.SOUND_TRACK: 15,
 ToontownBattleGlobals.THROW_TRACK: 15,
 ToontownBattleGlobals.SQUIRT_TRACK: 15,
 ToontownBattleGlobals.DROP_TRACK: 15}

class TrackTrainingReward(Reward):
    def __init__(self, id, reward):
        Reward.__init__(self, id, reward)

    def getTrack(self):
        track = self.reward[0]
        if track == None:
            track = 0
        return track

    def sendRewardAI(self, av):
        av.b_setTrackProgress(self.getTrack(), 0)

    def countReward(self, qrc):
        qrc.trackProgressId = self.getTrack()
        qrc.trackProgress = 0

    def getString(self):
        trackName = ToontownBattleGlobals.Tracks[self.getTrack()].capitalize()
        return TTLocalizer.QuestsTrackTrainingReward % trackName

    def getPosterString(self):
        return TTLocalizer.QuestsTrackTrainingRewardPoster


class TrackProgressReward(Reward):
    def __init__(self, id, reward):
        Reward.__init__(self, id, reward)

    def getTrack(self):
        track = self.reward[0]
        if track == None:
            track = 0
        return track

    def getProgressIndex(self):
        return self.reward[1]

    def sendRewardAI(self, av):
        av.addTrackProgress(self.getTrack(), self.getProgressIndex())

    def countReward(self, qrc):
        qrc.addTrackProgress(self.getTrack(), self.getProgressIndex())

    def getString(self):
        trackName = ToontownBattleGlobals.Tracks[self.getTrack()].capitalize()
        return TTLocalizer.QuestsTrackProgressReward % {'frameNum': self.getProgressIndex(),
         'trackName': trackName}

    def getPosterString(self):
        trackName = ToontownBattleGlobals.Tracks[self.getTrack()].capitalize()
        return TTLocalizer.QuestsTrackProgressRewardPoster % {'trackName': trackName,
         'frameNum': self.getProgressIndex()}


class TrackCompleteReward(Reward):
    def __init__(self, id, reward):
        Reward.__init__(self, id, reward)

    def getTrack(self):
        track = self.reward[0]
        if track == None:
            track = 0
        return track

    def sendRewardAI(self, av):
        av.addTrackAccess(self.getTrack())
        av.clearTrackProgress()

    def countReward(self, qrc):
        qrc.addTrackAccess(self.getTrack())
        qrc.clearTrackProgress()

    def getString(self):
        trackName = ToontownBattleGlobals.Tracks[self.getTrack()].capitalize()
        return TTLocalizer.QuestsTrackCompleteReward % trackName

    def getPosterString(self):
        trackName = ToontownBattleGlobals.Tracks[self.getTrack()].capitalize()
        return TTLocalizer.QuestsTrackCompleteRewardPoster % trackName


class ClothingTicketReward(Reward):
    def __init__(self, id, reward):
        Reward.__init__(self, id, reward)

    def sendRewardAI(self, av):
        pass

    def countReward(self, qrc):
        pass

    def getString(self):
        return TTLocalizer.QuestsClothingTicketReward

    def getPosterString(self):
        return TTLocalizer.QuestsClothingTicketRewardPoster


class TIPClothingTicketReward(ClothingTicketReward):
    def __init__(self, id, reward):
        ClothingTicketReward.__init__(self, id, reward)

    def getString(self):
        return TTLocalizer.TIPQuestsClothingTicketReward

    def getPosterString(self):
        return TTLocalizer.TIPQuestsClothingTicketRewardPoster


class CheesyEffectReward(Reward):
    def __init__(self, id, reward):
        Reward.__init__(self, id, reward)

    def getEffect(self):
        return self.reward[0]

    def getHoodId(self):
        return self.reward[1]

    def getDurationMinutes(self):
        return self.reward[2]

    def sendRewardAI(self, av):
        expireTime = int(time.time() / 60 + 0.5) + self.getDurationMinutes()
        av.b_setCheesyEffect(self.getEffect(), self.getHoodId(), expireTime)

    def countReward(self, qrc):
        pass

    def getString(self):
        effect = self.getEffect()
        hoodId = self.getHoodId()
        duration = self.getDurationMinutes()
        string = TTLocalizer.CheesyEffectMinutes
        if duration > 90:
            duration = int((duration + 30) / 60)
            string = TTLocalizer.CheesyEffectHours
            if duration > 36:
                duration = int((duration + 12) / 24)
                string = TTLocalizer.CheesyEffectDays
        desc = TTLocalizer.CheesyEffectDescriptions[effect][1]
        if hoodId == 0:
            whileStr = ''
        elif hoodId == 1:
            whileStr = TTLocalizer.CheesyEffectExceptIn % TTLocalizer.ToontownCentral[-1]
        else:
            hoodName = base.cr.hoodMgr.getFullnameFromId(hoodId)
            whileStr = TTLocalizer.CheesyEffectWhileYouAreIn % hoodName
        if duration:
            return string % {'time': duration,
             'effectName': desc,
             'whileIn': whileStr}
        else:
            return TTLocalizer.CheesyEffectIndefinite % {'effectName': desc,
             'whileIn': whileStr}

    def getPosterString(self):
        effect = self.getEffect()
        desc = TTLocalizer.CheesyEffectDescriptions[effect][0]
        return TTLocalizer.QuestsCheesyEffectRewardPoster % desc


class CogSuitPartReward(Reward):
    trackNames = [TTLocalizer.Bossbot,
     TTLocalizer.Lawbot,
     TTLocalizer.Cashbot,
     TTLocalizer.Sellbot]

    def __init__(self, id, reward):
        Reward.__init__(self, id, reward)

    def getCogTrack(self):
        return self.reward[0]

    def getCogPart(self):
        return self.reward[1]

    def sendRewardAI(self, av):
        dept = self.getCogTrack()
        part = self.getCogPart()
        av.giveCogPart(part, dept)

    def countReward(self, qrc):
        pass

    def getCogTrackName(self):
        index = ToontownGlobals.cogDept2index[self.getCogTrack()]
        return CogSuitPartReward.trackNames[index]

    def getCogPartName(self):
        index = ToontownGlobals.cogDept2index[self.getCogTrack()]
        return CogDisguiseGlobals.PartsQueryNames[index][self.getCogPart()]

    def getString(self):
        return TTLocalizer.QuestsCogSuitPartReward % {'cogTrack': self.getCogTrackName(),
         'part': self.getCogPartName()}

    def getPosterString(self):
        return TTLocalizer.QuestsCogSuitPartRewardPoster % {'cogTrack': self.getCogTrackName(),
         'part': self.getCogPartName()}


class APLocationReward(Reward):

    # Location string given is the Donald's Dock Task #4 etc
    def getCheckName(self) -> str:
        return self.reward[0]

    def getCheckId(self) -> int:
        return util.ap_location_name_to_id(self.getCheckName())

    def sendRewardAI(self, av):
        checkID = self.getCheckId()

        if checkID < 0:
            raise Exception(f"Invalid location name for AP Location reward!: {self.getCheckName()}")

        av.addCheckedLocation(self.getCheckId())

    def getRewardName(self):


        # First try to find out if we are running this locally or on the ai
        av = None
        try:
            av = base.localAvatar
        # This is the AI, just use the check name
        except AttributeError:
            return self.getCheckName()

        # Do we have it cached?
        if not av.hasCachedLocationReward(self.getCheckId()):
            return self.getCheckName()

        # Send
        return av.getCachedLocationReward(self.getCheckId())

    def getString(self):
        return f"You have completed {self.getCheckName()}"

    def getPosterString(self):
        return self.getRewardName()


REWARD_INDEX_CLASS = 0

def getRewardClass(rewardID):
    reward = RewardDict.get(rewardID)
    if reward is not None:
        return reward[REWARD_INDEX_CLASS]

    return None


def getReward(rewardID):
    reward = RewardDict.get(rewardID)
    if reward is not None:
        rewardClass = reward[REWARD_INDEX_CLASS]
        return rewardClass(rewardID, reward[1:])

    notify.warning('getReward(): id %s not found.' % rewardID)
    return None


RewardDict = {
    100: (MaxHpReward, 1),
    101: (MaxHpReward, 2),
    102: (MaxHpReward, 3),
    103: (MaxHpReward, 4),
    104: (MaxHpReward, 5),
    105: (MaxHpReward, 6),
    106: (MaxHpReward, 7),
    107: (MaxHpReward, 8),
    108: (MaxHpReward, 9),
    109: (MaxHpReward, 10),
    200: (MaxGagCarryReward, 25, TTLocalizer.QuestsMediumPouch),
    201: (MaxGagCarryReward, 30, TTLocalizer.QuestsLargePouch),
    202: (MaxGagCarryReward, 35, TTLocalizer.QuestsSmallBag),
    203: (MaxGagCarryReward, 40, TTLocalizer.QuestsMediumBag),
    204: (MaxGagCarryReward, 50, TTLocalizer.QuestsLargeBag),
    205: (MaxGagCarryReward, 60, TTLocalizer.QuestsSmallBackpack),
    206: (MaxGagCarryReward, 70, TTLocalizer.QuestsMediumBackpack),
    207: (MaxGagCarryReward, 80, TTLocalizer.QuestsLargeBackpack),
    300: (TeleportReward, ToontownGlobals.ToontownCentral),
    301: (TeleportReward, ToontownGlobals.DonaldsDock),
    302: (TeleportReward, ToontownGlobals.DaisyGardens),
    303: (TeleportReward, ToontownGlobals.MinniesMelodyland),
    304: (TeleportReward, ToontownGlobals.TheBrrrgh),
    305: (TeleportReward, ToontownGlobals.DonaldsDreamland),
    400: (TrackTrainingReward, None),
    401: (TrackTrainingReward, ToontownBattleGlobals.HEAL_TRACK),
    402: (TrackTrainingReward, ToontownBattleGlobals.TRAP_TRACK),
    403: (TrackTrainingReward, ToontownBattleGlobals.LURE_TRACK),
    404: (TrackTrainingReward, ToontownBattleGlobals.SOUND_TRACK),
    405: (TrackTrainingReward, ToontownBattleGlobals.THROW_TRACK),
    406: (TrackTrainingReward, ToontownBattleGlobals.SQUIRT_TRACK),
    407: (TrackTrainingReward, ToontownBattleGlobals.DROP_TRACK),
    500: (MaxQuestCarryReward, 2),
    501: (MaxQuestCarryReward, 3),
    502: (MaxQuestCarryReward, 4),
    600: (MoneyReward, 10),
    601: (MoneyReward, 20),
    602: (MoneyReward, 40),
    603: (MoneyReward, 60),
    604: (MoneyReward, 100),
    605: (MoneyReward, 150),
    606: (MoneyReward, 200),
    607: (MoneyReward, 250),
    608: (MoneyReward, 300),
    609: (MoneyReward, 400),
    610: (MoneyReward, 500),
    611: (MoneyReward, 600),
    612: (MoneyReward, 700),
    613: (MoneyReward, 800),
    614: (MoneyReward, 900),
    615: (MoneyReward, 1000),
    616: (MoneyReward, 1100),
    617: (MoneyReward, 1200),
    618: (MoneyReward, 1300),
    619: (MoneyReward, 1400),
    620: (MoneyReward, 1500),
    621: (MoneyReward, 1750),
    622: (MoneyReward, 2000),
    623: (MoneyReward, 2500),
    700: (MaxMoneyReward, 50),
    701: (MaxMoneyReward, 60),
    702: (MaxMoneyReward, 80),
    703: (MaxMoneyReward, 100),
    704: (MaxMoneyReward, 120),
    705: (MaxMoneyReward, 150),
    706: (MaxMoneyReward, 200),
    707: (MaxMoneyReward, 250),
    801: (TrackProgressReward, None, 1),
    802: (TrackProgressReward, None, 2),
    803: (TrackProgressReward, None, 3),
    804: (TrackProgressReward, None, 4),
    805: (TrackProgressReward, None, 5),
    806: (TrackProgressReward, None, 6),
    807: (TrackProgressReward, None, 7),
    808: (TrackProgressReward, None, 8),
    809: (TrackProgressReward, None, 9),
    810: (TrackProgressReward, None, 10),
    811: (TrackProgressReward, None, 11),
    812: (TrackProgressReward, None, 12),
    813: (TrackProgressReward, None, 13),
    814: (TrackProgressReward, None, 14),
    815: (TrackProgressReward, None, 15),
    110: (TIPClothingTicketReward,),
    1000: (ClothingTicketReward,),
    1001: (TrackProgressReward, ToontownBattleGlobals.HEAL_TRACK, 1),
    1002: (TrackProgressReward, ToontownBattleGlobals.HEAL_TRACK, 2),
    1003: (TrackProgressReward, ToontownBattleGlobals.HEAL_TRACK, 3),
    1004: (TrackProgressReward, ToontownBattleGlobals.HEAL_TRACK, 4),
    1005: (TrackProgressReward, ToontownBattleGlobals.HEAL_TRACK, 5),
    1006: (TrackProgressReward, ToontownBattleGlobals.HEAL_TRACK, 6),
    1007: (TrackProgressReward, ToontownBattleGlobals.HEAL_TRACK, 7),
    1008: (TrackProgressReward, ToontownBattleGlobals.HEAL_TRACK, 8),
    1009: (TrackProgressReward, ToontownBattleGlobals.HEAL_TRACK, 9),
    1010: (TrackProgressReward, ToontownBattleGlobals.HEAL_TRACK, 10),
    1011: (TrackProgressReward, ToontownBattleGlobals.HEAL_TRACK, 11),
    1012: (TrackProgressReward, ToontownBattleGlobals.HEAL_TRACK, 12),
    1013: (TrackProgressReward, ToontownBattleGlobals.HEAL_TRACK, 13),
    1014: (TrackProgressReward, ToontownBattleGlobals.HEAL_TRACK, 14),
    1015: (TrackProgressReward, ToontownBattleGlobals.HEAL_TRACK, 15),
    1101: (TrackProgressReward, ToontownBattleGlobals.TRAP_TRACK, 1),
    1102: (TrackProgressReward, ToontownBattleGlobals.TRAP_TRACK, 2),
    1103: (TrackProgressReward, ToontownBattleGlobals.TRAP_TRACK, 3),
    1104: (TrackProgressReward, ToontownBattleGlobals.TRAP_TRACK, 4),
    1105: (TrackProgressReward, ToontownBattleGlobals.TRAP_TRACK, 5),
    1106: (TrackProgressReward, ToontownBattleGlobals.TRAP_TRACK, 6),
    1107: (TrackProgressReward, ToontownBattleGlobals.TRAP_TRACK, 7),
    1108: (TrackProgressReward, ToontownBattleGlobals.TRAP_TRACK, 8),
    1109: (TrackProgressReward, ToontownBattleGlobals.TRAP_TRACK, 9),
    1110: (TrackProgressReward, ToontownBattleGlobals.TRAP_TRACK, 10),
    1111: (TrackProgressReward, ToontownBattleGlobals.TRAP_TRACK, 11),
    1112: (TrackProgressReward, ToontownBattleGlobals.TRAP_TRACK, 12),
    1113: (TrackProgressReward, ToontownBattleGlobals.TRAP_TRACK, 13),
    1114: (TrackProgressReward, ToontownBattleGlobals.TRAP_TRACK, 14),
    1115: (TrackProgressReward, ToontownBattleGlobals.TRAP_TRACK, 15),
    1201: (TrackProgressReward, ToontownBattleGlobals.LURE_TRACK, 1),
    1202: (TrackProgressReward, ToontownBattleGlobals.LURE_TRACK, 2),
    1203: (TrackProgressReward, ToontownBattleGlobals.LURE_TRACK, 3),
    1204: (TrackProgressReward, ToontownBattleGlobals.LURE_TRACK, 4),
    1205: (TrackProgressReward, ToontownBattleGlobals.LURE_TRACK, 5),
    1206: (TrackProgressReward, ToontownBattleGlobals.LURE_TRACK, 6),
    1207: (TrackProgressReward, ToontownBattleGlobals.LURE_TRACK, 7),
    1208: (TrackProgressReward, ToontownBattleGlobals.LURE_TRACK, 8),
    1209: (TrackProgressReward, ToontownBattleGlobals.LURE_TRACK, 9),
    1210: (TrackProgressReward, ToontownBattleGlobals.LURE_TRACK, 10),
    1211: (TrackProgressReward, ToontownBattleGlobals.LURE_TRACK, 11),
    1212: (TrackProgressReward, ToontownBattleGlobals.LURE_TRACK, 12),
    1213: (TrackProgressReward, ToontownBattleGlobals.LURE_TRACK, 13),
    1214: (TrackProgressReward, ToontownBattleGlobals.LURE_TRACK, 14),
    1215: (TrackProgressReward, ToontownBattleGlobals.LURE_TRACK, 15),
    1301: (TrackProgressReward, ToontownBattleGlobals.SOUND_TRACK, 1),
    1302: (TrackProgressReward, ToontownBattleGlobals.SOUND_TRACK, 2),
    1303: (TrackProgressReward, ToontownBattleGlobals.SOUND_TRACK, 3),
    1304: (TrackProgressReward, ToontownBattleGlobals.SOUND_TRACK, 4),
    1305: (TrackProgressReward, ToontownBattleGlobals.SOUND_TRACK, 5),
    1306: (TrackProgressReward, ToontownBattleGlobals.SOUND_TRACK, 6),
    1307: (TrackProgressReward, ToontownBattleGlobals.SOUND_TRACK, 7),
    1308: (TrackProgressReward, ToontownBattleGlobals.SOUND_TRACK, 8),
    1309: (TrackProgressReward, ToontownBattleGlobals.SOUND_TRACK, 9),
    1310: (TrackProgressReward, ToontownBattleGlobals.SOUND_TRACK, 10),
    1311: (TrackProgressReward, ToontownBattleGlobals.SOUND_TRACK, 11),
    1312: (TrackProgressReward, ToontownBattleGlobals.SOUND_TRACK, 12),
    1313: (TrackProgressReward, ToontownBattleGlobals.SOUND_TRACK, 13),
    1314: (TrackProgressReward, ToontownBattleGlobals.SOUND_TRACK, 14),
    1315: (TrackProgressReward, ToontownBattleGlobals.SOUND_TRACK, 15),
    1601: (TrackProgressReward, ToontownBattleGlobals.DROP_TRACK, 1),
    1602: (TrackProgressReward, ToontownBattleGlobals.DROP_TRACK, 2),
    1603: (TrackProgressReward, ToontownBattleGlobals.DROP_TRACK, 3),
    1604: (TrackProgressReward, ToontownBattleGlobals.DROP_TRACK, 4),
    1605: (TrackProgressReward, ToontownBattleGlobals.DROP_TRACK, 5),
    1606: (TrackProgressReward, ToontownBattleGlobals.DROP_TRACK, 6),
    1607: (TrackProgressReward, ToontownBattleGlobals.DROP_TRACK, 7),
    1608: (TrackProgressReward, ToontownBattleGlobals.DROP_TRACK, 8),
    1609: (TrackProgressReward, ToontownBattleGlobals.DROP_TRACK, 9),
    1610: (TrackProgressReward, ToontownBattleGlobals.DROP_TRACK, 10),
    1611: (TrackProgressReward, ToontownBattleGlobals.DROP_TRACK, 11),
    1612: (TrackProgressReward, ToontownBattleGlobals.DROP_TRACK, 12),
    1613: (TrackProgressReward, ToontownBattleGlobals.DROP_TRACK, 13),
    1614: (TrackProgressReward, ToontownBattleGlobals.DROP_TRACK, 14),
    1615: (TrackProgressReward, ToontownBattleGlobals.DROP_TRACK, 15),
    900: (TrackCompleteReward, None),
    901: (TrackCompleteReward, ToontownBattleGlobals.HEAL_TRACK),
    902: (TrackCompleteReward, ToontownBattleGlobals.TRAP_TRACK),
    903: (TrackCompleteReward, ToontownBattleGlobals.LURE_TRACK),
    904: (TrackCompleteReward, ToontownBattleGlobals.SOUND_TRACK),
    905: (TrackCompleteReward, ToontownBattleGlobals.THROW_TRACK),
    906: (TrackCompleteReward, ToontownBattleGlobals.SQUIRT_TRACK),
    907: (TrackCompleteReward, ToontownBattleGlobals.DROP_TRACK),
    2205: (CheesyEffectReward, ToontownGlobals.CEBigToon, 2000, 10),
    2206: (CheesyEffectReward, ToontownGlobals.CESmallToon, 2000, 10),
    2101: (CheesyEffectReward, ToontownGlobals.CEBigHead, 1000, 10),
    2102: (CheesyEffectReward, ToontownGlobals.CESmallHead, 1000, 10),
    2105: (CheesyEffectReward, ToontownGlobals.CEBigToon, 0, 20),
    2106: (CheesyEffectReward, ToontownGlobals.CESmallToon, 0, 20),
    2501: (CheesyEffectReward, ToontownGlobals.CEBigHead, 5000, 60),
    2502: (CheesyEffectReward, ToontownGlobals.CESmallHead, 5000, 60),
    2503: (CheesyEffectReward, ToontownGlobals.CEBigLegs, 5000, 20),
    2504: (CheesyEffectReward, ToontownGlobals.CESmallLegs, 5000, 20),
    2505: (CheesyEffectReward, ToontownGlobals.CEBigToon, 0, 60),
    2506: (CheesyEffectReward, ToontownGlobals.CESmallToon, 0, 60),
    2401: (CheesyEffectReward, ToontownGlobals.CEBigHead, 1, 120),
    2402: (CheesyEffectReward, ToontownGlobals.CESmallHead, 1, 120),
    2403: (CheesyEffectReward, ToontownGlobals.CEBigLegs, 4000, 60),
    2404: (CheesyEffectReward, ToontownGlobals.CESmallLegs, 4000, 60),
    2405: (CheesyEffectReward, ToontownGlobals.CEBigToon, 0, 120),
    2406: (CheesyEffectReward, ToontownGlobals.CESmallToon, 0, 120),
    2407: (CheesyEffectReward, ToontownGlobals.CEFlatPortrait, 4000, 30),
    2408: (CheesyEffectReward, ToontownGlobals.CEFlatProfile, 4000, 30),
    2409: (CheesyEffectReward, ToontownGlobals.CETransparent, 4000, 30),
    2410: (CheesyEffectReward, ToontownGlobals.CENoColor, 4000, 30),
    2301: (CheesyEffectReward, ToontownGlobals.CEBigHead, 1, 360),
    2302: (CheesyEffectReward, ToontownGlobals.CESmallHead, 1, 360),
    2303: (CheesyEffectReward, ToontownGlobals.CEBigLegs, 1, 360),
    2304: (CheesyEffectReward, ToontownGlobals.CESmallLegs, 1, 360),
    2305: (CheesyEffectReward, ToontownGlobals.CEBigToon, 0, 1440),
    2306: (CheesyEffectReward, ToontownGlobals.CESmallToon, 0, 1440),
    2307: (CheesyEffectReward, ToontownGlobals.CEFlatPortrait, 3000, 240),
    2308: (CheesyEffectReward, ToontownGlobals.CEFlatProfile, 3000, 240),
    2309: (CheesyEffectReward, ToontownGlobals.CETransparent, 1, 120),
    2310: (CheesyEffectReward, ToontownGlobals.CENoColor, 1, 120),
    2311: (CheesyEffectReward, ToontownGlobals.CEInvisible, 3000, 120),
    2900: (CheesyEffectReward, ToontownGlobals.CENormal, 0, 0),
    2901: (CheesyEffectReward, ToontownGlobals.CEBigHead, 1, 1440),
    2902: (CheesyEffectReward, ToontownGlobals.CESmallHead, 1, 1440),
    2903: (CheesyEffectReward, ToontownGlobals.CEBigLegs, 1, 1440),
    2904: (CheesyEffectReward, ToontownGlobals.CESmallLegs, 1, 1440),
    2905: (CheesyEffectReward, ToontownGlobals.CEBigToon, 0, 1440),
    2906: (CheesyEffectReward, ToontownGlobals.CESmallToon, 0, 1440),
    2907: (CheesyEffectReward, ToontownGlobals.CEFlatPortrait, 1, 1440),
    2908: (CheesyEffectReward, ToontownGlobals.CEFlatProfile, 1, 1440),
    2909: (CheesyEffectReward, ToontownGlobals.CETransparent, 1, 1440),
    2910: (CheesyEffectReward, ToontownGlobals.CENoColor, 1, 1440),
    2911: (CheesyEffectReward, ToontownGlobals.CEInvisible, 1, 1440),
    2920: (CheesyEffectReward, ToontownGlobals.CENormal, 0, 0),
    2921: (CheesyEffectReward, ToontownGlobals.CEBigHead, 1, 2880),
    2922: (CheesyEffectReward, ToontownGlobals.CESmallHead, 1, 2880),
    2923: (CheesyEffectReward, ToontownGlobals.CEBigLegs, 1, 2880),
    2924: (CheesyEffectReward,ToontownGlobals.CESmallLegs,1,2880),
    2925: (CheesyEffectReward,ToontownGlobals.CEBigToon,0,2880),
    2926: (CheesyEffectReward,ToontownGlobals.CESmallToon,0,2880),
    2927: (CheesyEffectReward,ToontownGlobals.CEFlatPortrait,1,2880),
    2928: (CheesyEffectReward,ToontownGlobals.CEFlatProfile,1,2880),
    2929: (CheesyEffectReward,ToontownGlobals.CETransparent,1,2880),
    2930: (CheesyEffectReward,ToontownGlobals.CENoColor,1,2880),
    2931: (CheesyEffectReward,ToontownGlobals.CEInvisible,1,2880),
    2940: (CheesyEffectReward,ToontownGlobals.CENormal,0,0),
    2941: (CheesyEffectReward,ToontownGlobals.CEBigHead,1,10080),
    2942: (CheesyEffectReward, ToontownGlobals.CESmallHead, 1, 10080),
    2943: (CheesyEffectReward, ToontownGlobals.CEBigLegs, 1, 10080),
    2944: (CheesyEffectReward, ToontownGlobals.CESmallLegs, 1, 10080),
    2945: (CheesyEffectReward, ToontownGlobals.CEBigToon, 0, 10080),
    2946: (CheesyEffectReward, ToontownGlobals.CESmallToon, 0, 10080),
    2947: (CheesyEffectReward, ToontownGlobals.CEFlatPortrait, 1, 10080),
    2948: (CheesyEffectReward, ToontownGlobals.CEFlatProfile, 1, 10080),
    2949: (CheesyEffectReward, ToontownGlobals.CETransparent, 1, 10080),
    2950: (CheesyEffectReward, ToontownGlobals.CENoColor, 1, 10080),
    2951: (CheesyEffectReward, ToontownGlobals.CEInvisible, 1, 10080),
    2960: (CheesyEffectReward, ToontownGlobals.CENormal, 0, 0),
    2961: (CheesyEffectReward, ToontownGlobals.CEBigHead, 1, 43200),
    2962: (CheesyEffectReward, ToontownGlobals.CESmallHead, 1, 43200),
    2963: (CheesyEffectReward, ToontownGlobals.CEBigLegs, 1, 43200),
    2964: (CheesyEffectReward, ToontownGlobals.CESmallLegs, 1, 43200),
    2965: (CheesyEffectReward, ToontownGlobals.CEBigToon, 0, 43200),
    2966: (CheesyEffectReward, ToontownGlobals.CESmallToon, 0, 43200),
    2967: (CheesyEffectReward, ToontownGlobals.CEFlatPortrait, 1,43200),
    2968: (CheesyEffectReward, ToontownGlobals.CEFlatProfile, 1, 43200),
    2969: (CheesyEffectReward, ToontownGlobals.CETransparent, 1, 43200),
    2970: (CheesyEffectReward, ToontownGlobals.CENoColor, 1, 43200),
    2971: (CheesyEffectReward, ToontownGlobals.CEInvisible, 1, 43200),
    4000: (CogSuitPartReward, 'm', CogDisguiseGlobals.leftLegUpper),
    4001: (CogSuitPartReward, 'm', CogDisguiseGlobals.leftLegLower),
    4002: (CogSuitPartReward, 'm', CogDisguiseGlobals.leftLegFoot),
    4003: (CogSuitPartReward, 'm', CogDisguiseGlobals.rightLegUpper),
    4004: (CogSuitPartReward, 'm', CogDisguiseGlobals.rightLegLower),
    4005: (CogSuitPartReward, 'm', CogDisguiseGlobals.rightLegFoot),
    4006: (CogSuitPartReward, 'm', CogDisguiseGlobals.upperTorso),
    4007: (CogSuitPartReward, 'm', CogDisguiseGlobals.torsoPelvis),
    4008: (CogSuitPartReward, 'm', CogDisguiseGlobals.leftArmUpper),
    4009: (CogSuitPartReward, 'm', CogDisguiseGlobals.leftArmLower),
    4010: (CogSuitPartReward, 'm', CogDisguiseGlobals.rightArmUpper),
    4011: (CogSuitPartReward, 'm', CogDisguiseGlobals.rightArmLower),
    4100: (CogSuitPartReward, 'l', CogDisguiseGlobals.leftLegUpper),
    4101: (CogSuitPartReward, 'l', CogDisguiseGlobals.leftLegLower),
    4102: (CogSuitPartReward, 'l', CogDisguiseGlobals.leftLegFoot),
    4103: (CogSuitPartReward, 'l', CogDisguiseGlobals.rightLegUpper),
    4104: (CogSuitPartReward, 'l', CogDisguiseGlobals.rightLegLower),
    4105: (CogSuitPartReward, 'l', CogDisguiseGlobals.rightLegFoot),
    4106: (CogSuitPartReward, 'l', CogDisguiseGlobals.upperTorso),
    4107: (CogSuitPartReward, 'l', CogDisguiseGlobals.torsoPelvis),
    4108: (CogSuitPartReward, 'l', CogDisguiseGlobals.leftArmUpper),
    4109: (CogSuitPartReward, 'l', CogDisguiseGlobals.leftArmLower),
    4110: (CogSuitPartReward, 'l', CogDisguiseGlobals.leftArmHand),
    4111: (CogSuitPartReward, 'l', CogDisguiseGlobals.rightArmUpper),
    4112: (CogSuitPartReward, 'l', CogDisguiseGlobals.rightArmLower),
    4113: (CogSuitPartReward, 'l', CogDisguiseGlobals.rightArmHand),
    4200: (CogSuitPartReward, 'c', CogDisguiseGlobals.leftLegUpper),
    4201: (CogSuitPartReward, 'c', CogDisguiseGlobals.leftLegLower),
    4202: (CogSuitPartReward, 'c', CogDisguiseGlobals.leftLegFoot),
    4203: (CogSuitPartReward, 'c', CogDisguiseGlobals.rightLegUpper),
    4204: (CogSuitPartReward, 'c', CogDisguiseGlobals.rightLegLower),
    4205: (CogSuitPartReward, 'c', CogDisguiseGlobals.rightLegFoot),
    4206: (CogSuitPartReward, 'c', CogDisguiseGlobals.torsoLeftShoulder),
    4207: (CogSuitPartReward, 'c', CogDisguiseGlobals.torsoRightShoulder),
    4208: (CogSuitPartReward, 'c', CogDisguiseGlobals.torsoChest),
    4209: (CogSuitPartReward, 'c', CogDisguiseGlobals.torsoHealthMeter),
    4210: (CogSuitPartReward, 'c', CogDisguiseGlobals.torsoPelvis),
    4211: (CogSuitPartReward, 'c', CogDisguiseGlobals.leftArmUpper),
    4212: (CogSuitPartReward, 'c', CogDisguiseGlobals.leftArmLower),
    4213: (CogSuitPartReward, 'c', CogDisguiseGlobals.leftArmHand),
    4214: (CogSuitPartReward, 'c', CogDisguiseGlobals.rightArmUpper),
    4215: (CogSuitPartReward, 'c', CogDisguiseGlobals.rightArmLower),
    4216: (CogSuitPartReward, 'c', CogDisguiseGlobals.rightArmHand),

    # Start AP Rewards, these essentially are just maps to the location checks for AP
    5000: (APLocationReward, locations.ToontownLocationName.TOONTOWN_CENTRAL_TASK_1.value),
    5001: (APLocationReward, locations.ToontownLocationName.TOONTOWN_CENTRAL_TASK_2.value),
    5002: (APLocationReward, locations.ToontownLocationName.TOONTOWN_CENTRAL_TASK_3.value),
    5003: (APLocationReward, locations.ToontownLocationName.TOONTOWN_CENTRAL_TASK_4.value),
    5004: (APLocationReward, locations.ToontownLocationName.TOONTOWN_CENTRAL_TASK_5.value),
    5005: (APLocationReward, locations.ToontownLocationName.TOONTOWN_CENTRAL_TASK_6.value),
    5006: (APLocationReward, locations.ToontownLocationName.TOONTOWN_CENTRAL_TASK_7.value),
    5007: (APLocationReward, locations.ToontownLocationName.TOONTOWN_CENTRAL_TASK_8.value),
    5008: (APLocationReward, locations.ToontownLocationName.TOONTOWN_CENTRAL_TASK_9.value),
    5009: (APLocationReward, locations.ToontownLocationName.TOONTOWN_CENTRAL_TASK_10.value),
    5010: (APLocationReward, locations.ToontownLocationName.TOONTOWN_CENTRAL_TASK_11.value),
    5011: (APLocationReward, locations.ToontownLocationName.TOONTOWN_CENTRAL_TASK_12.value),
    5012: (APLocationReward, locations.ToontownLocationName.DONALDS_DOCK_TASK_1.value),
    5013: (APLocationReward, locations.ToontownLocationName.DONALDS_DOCK_TASK_2.value),
    5014: (APLocationReward, locations.ToontownLocationName.DONALDS_DOCK_TASK_3.value),
    5015: (APLocationReward, locations.ToontownLocationName.DONALDS_DOCK_TASK_4.value),
    5016: (APLocationReward, locations.ToontownLocationName.DONALDS_DOCK_TASK_5.value),
    5017: (APLocationReward, locations.ToontownLocationName.DONALDS_DOCK_TASK_6.value),
    5018: (APLocationReward, locations.ToontownLocationName.DONALDS_DOCK_TASK_7.value),
    5019: (APLocationReward, locations.ToontownLocationName.DONALDS_DOCK_TASK_8.value),
    5020: (APLocationReward, locations.ToontownLocationName.DONALDS_DOCK_TASK_9.value),
    5021: (APLocationReward, locations.ToontownLocationName.DONALDS_DOCK_TASK_10.value),
    5022: (APLocationReward, locations.ToontownLocationName.DONALDS_DOCK_TASK_11.value),
    5023: (APLocationReward, locations.ToontownLocationName.DONALDS_DOCK_TASK_12.value),
    5024: (APLocationReward, locations.ToontownLocationName.DAISYS_GARDENS_TASK_1.value),
    5025: (APLocationReward, locations.ToontownLocationName.DAISYS_GARDENS_TASK_2.value),
    5026: (APLocationReward, locations.ToontownLocationName.DAISYS_GARDENS_TASK_3.value),
    5027: (APLocationReward, locations.ToontownLocationName.DAISYS_GARDENS_TASK_4.value),
    5028: (APLocationReward, locations.ToontownLocationName.DAISYS_GARDENS_TASK_5.value),
    5029: (APLocationReward, locations.ToontownLocationName.DAISYS_GARDENS_TASK_6.value),
    5030: (APLocationReward, locations.ToontownLocationName.DAISYS_GARDENS_TASK_7.value),
    5031: (APLocationReward, locations.ToontownLocationName.DAISYS_GARDENS_TASK_8.value),
    5032: (APLocationReward, locations.ToontownLocationName.DAISYS_GARDENS_TASK_9.value),
    5033: (APLocationReward, locations.ToontownLocationName.DAISYS_GARDENS_TASK_10.value),
    5034: (APLocationReward, locations.ToontownLocationName.DAISYS_GARDENS_TASK_11.value),
    5035: (APLocationReward, locations.ToontownLocationName.DAISYS_GARDENS_TASK_12.value),
    5036: (APLocationReward, locations.ToontownLocationName.MINNIES_MELODYLAND_TASK_1.value),
    5037: (APLocationReward, locations.ToontownLocationName.MINNIES_MELODYLAND_TASK_2.value),
    5038: (APLocationReward, locations.ToontownLocationName.MINNIES_MELODYLAND_TASK_3.value),
    5039: (APLocationReward, locations.ToontownLocationName.MINNIES_MELODYLAND_TASK_4.value),
    5040: (APLocationReward, locations.ToontownLocationName.MINNIES_MELODYLAND_TASK_5.value),
    5041: (APLocationReward, locations.ToontownLocationName.MINNIES_MELODYLAND_TASK_6.value),
    5042: (APLocationReward, locations.ToontownLocationName.MINNIES_MELODYLAND_TASK_7.value),
    5043: (APLocationReward, locations.ToontownLocationName.MINNIES_MELODYLAND_TASK_8.value),
    5044: (APLocationReward, locations.ToontownLocationName.MINNIES_MELODYLAND_TASK_9.value),
    5045: (APLocationReward, locations.ToontownLocationName.MINNIES_MELODYLAND_TASK_10.value),
    5046: (APLocationReward, locations.ToontownLocationName.MINNIES_MELODYLAND_TASK_11.value),
    5047: (APLocationReward, locations.ToontownLocationName.MINNIES_MELODYLAND_TASK_12.value),
    5048: (APLocationReward, locations.ToontownLocationName.THE_BRRRGH_TASK_1.value),
    5049: (APLocationReward, locations.ToontownLocationName.THE_BRRRGH_TASK_2.value),
    5050: (APLocationReward, locations.ToontownLocationName.THE_BRRRGH_TASK_3.value),
    5051: (APLocationReward, locations.ToontownLocationName.THE_BRRRGH_TASK_4.value),
    5052: (APLocationReward, locations.ToontownLocationName.THE_BRRRGH_TASK_5.value),
    5053: (APLocationReward, locations.ToontownLocationName.THE_BRRRGH_TASK_6.value),
    5054: (APLocationReward, locations.ToontownLocationName.THE_BRRRGH_TASK_7.value),
    5055: (APLocationReward, locations.ToontownLocationName.THE_BRRRGH_TASK_8.value),
    5056: (APLocationReward, locations.ToontownLocationName.THE_BRRRGH_TASK_9.value),
    5057: (APLocationReward, locations.ToontownLocationName.THE_BRRRGH_TASK_10.value),
    5058: (APLocationReward, locations.ToontownLocationName.THE_BRRRGH_TASK_11.value),
    5059: (APLocationReward, locations.ToontownLocationName.THE_BRRRGH_TASK_12.value),
    5060: (APLocationReward, locations.ToontownLocationName.DONALDS_DREAMLAND_TASK_1.value),
    5061: (APLocationReward, locations.ToontownLocationName.DONALDS_DREAMLAND_TASK_2.value),
    5062: (APLocationReward, locations.ToontownLocationName.DONALDS_DREAMLAND_TASK_3.value),
    5063: (APLocationReward, locations.ToontownLocationName.DONALDS_DREAMLAND_TASK_4.value),
    5064: (APLocationReward, locations.ToontownLocationName.DONALDS_DREAMLAND_TASK_5.value),
    5065: (APLocationReward, locations.ToontownLocationName.DONALDS_DREAMLAND_TASK_6.value),
    5066: (APLocationReward, locations.ToontownLocationName.DONALDS_DREAMLAND_TASK_7.value),
    5067: (APLocationReward, locations.ToontownLocationName.DONALDS_DREAMLAND_TASK_8.value),
    5068: (APLocationReward, locations.ToontownLocationName.DONALDS_DREAMLAND_TASK_9.value),
    5069: (APLocationReward, locations.ToontownLocationName.DONALDS_DREAMLAND_TASK_10.value),
    5070: (APLocationReward, locations.ToontownLocationName.DONALDS_DREAMLAND_TASK_11.value),
    5071: (APLocationReward, locations.ToontownLocationName.DONALDS_DREAMLAND_TASK_12.value),


}

# Maps AP location strings to the Quest Reward IDs defined in RewardDict
__AP_LOCATION_TO_REWARD_ID: Dict[str, int] = {

}
# Loop through every single reward, if it is an APLocationReward, map its string ID to the rewardID
for rewardID, rewardDescription in RewardDict.items():
    rewardClass = rewardDescription[0]
    if rewardClass == APLocationReward:
        __AP_LOCATION_TO_REWARD_ID[rewardDescription[1]] = rewardID


# Given an AP location name (locations.DONALDS_DREAMLAND_TASK_11 for example) return the reward ID that corresponds w it
# Returns -1 if not a valid AP location
def getRewardIdFromAPLocationName(location_name: str) -> int:
    return __AP_LOCATION_TO_REWARD_ID[location_name]


# Given a hood ID, return a list of reward IDs that this hood will have
def getRewardIdsFromHood(hoodId) -> List[int]:
    # Loop through all the AP location names for this hood and find the reward id from it
    rewards = []
    for apLocationName in util.hood_to_task_locations(hoodId):
        rewardId = getRewardIdFromAPLocationName(apLocationName)
        rewards.append(rewardId)

    return rewards


# Given an AP Reward ID, return the first playground that is able to give a task that contains this reward
def getHoodFromRewardId(rewardId) -> int:
    for hood in ToontownGlobals.Hoods:
        if rewardId in getRewardIdsFromHood(hood):
            return hood

    raise KeyError(f"Reward ID: {rewardID} is unobtainable from all available hoods")



# Returns all registered AP reward IDs
def getAllAPRewardIds() -> set[int]:
    return set(__AP_LOCATION_TO_REWARD_ID.values())


def isLoopingFinalTier(tier):
    return tier == LOOPING_FINAL_TIER


def getRewardsInTier(tier):
    return RequiredRewardTrackDict.get(tier, [])


def getOptionalRewardsInTier(tier):
    return OptionalRewardTrackDict.get(tier, [])


RequiredRewardTrackDict = {TT_TIER: (100,),
 TT_TIER + 1: (400,),
 TT_TIER + 2: (100,
               801,
               200,
               802,
               803,
               101,
               804,
               805,
               102,
               806,
               807,
               100,
               808,
               809,
               101,
               810,
               811,
               500,
               812,
               813,
               700,
               814,
               815,
               300),
 TT_TIER + 3: (900,),
 DD_TIER: (400,),
 DD_TIER + 1: (100,
               801,
               802,
               201,
               803,
               804,
               101,
               805,
               806,
               102,
               807,
               808,
               100,
               809,
               810,
               101,
               811,
               812,
               701,
               813,
               814,
               815,
               301),
 DD_TIER + 2: (900,),
 DG_TIER: (100,
           202,
           101,
           102,
           100,
           101,
           501,
           702,
           302),
 MM_TIER: (400,),
 MM_TIER + 1: (100,
               801,
               802,
               203,
               803,
               804,
               101,
               805,
               806,
               102,
               807,
               808,
               100,
               809,
               810,
               101,
               811,
               812,
               703,
               813,
               814,
               815,
               303),
 MM_TIER + 2: (900,),
 BR_TIER: (400,),
 BR_TIER + 1: (100,
               801,
               802,
               704,
               803,
               804,
               101,
               805,
               806,
               502,
               807,
               808,
               102,
               809,
               810,
               204,
               811,
               812,
               100,
               813,
               814,
               101,
               815,
               304),
 BR_TIER + 2: (900,),
 DL_TIER: (4000,
           100,
           205,
           101,
           102,
           705,
           103,
           305,
           4001,
           4002),
 DL_TIER + 1: (100,
               206,
               101,
               4003,
               4004,
               4005,
               102,
               4006,
               4007,
               4008,
               706,
               103,
               4009,
               4010,
               4011,
               4000,
               4001,
               4002),
 DL_TIER + 2: (4006,
               4007,
               4008,
               100,
               4000,
               4001,
               4002,
               4003,
               101,
               4004,
               4005,
               4009,
               102,
               103,
               4010,
               4011),
 DL_TIER + 3: (4009,
               4010,
               4011,
               100,
               4000,
               4001,
               101,
               4002,
               4003,
               102,
               4004,
               4005,
               102,
               4006,
               4007,
               707,
               207,
               4008),
 LAWBOT_HQ_TIER: (4100,),
 LAWBOT_HQ_TIER + 1: (4101,),
 LAWBOT_HQ_TIER + 2: (4102,),
 LAWBOT_HQ_TIER + 3: (4103,),
 LAWBOT_HQ_TIER + 4: (4104,),
 LAWBOT_HQ_TIER + 5: (4105,),
 LAWBOT_HQ_TIER + 6: (4106,),
 LAWBOT_HQ_TIER + 7: (4107,),
 LAWBOT_HQ_TIER + 8: (4108,),
 LAWBOT_HQ_TIER + 9: (4109,),
 LAWBOT_HQ_TIER + 10: (4110,),
 LAWBOT_HQ_TIER + 11: (4111,),
 LAWBOT_HQ_TIER + 12: (4112,),
 LAWBOT_HQ_TIER + 13: (4113,),
 BOSSBOT_HQ_TIER: (4200,),
 BOSSBOT_HQ_TIER + 1: (4201,),
 BOSSBOT_HQ_TIER + 2: (4202,),
 BOSSBOT_HQ_TIER + 3: (4203,),
 BOSSBOT_HQ_TIER + 4: (4204,),
 BOSSBOT_HQ_TIER + 5: (4205,),
 BOSSBOT_HQ_TIER + 6: (4206,),
 BOSSBOT_HQ_TIER + 7: (4207,),
 BOSSBOT_HQ_TIER + 8: (4208,),
 BOSSBOT_HQ_TIER + 9: (4209,),
 BOSSBOT_HQ_TIER + 10: (4210,),
 BOSSBOT_HQ_TIER + 11: (4211,),
 BOSSBOT_HQ_TIER + 12: (4212,),
 BOSSBOT_HQ_TIER + 13: (4213,),
 BOSSBOT_HQ_TIER + 14: (4214,),
 BOSSBOT_HQ_TIER + 15: (4215,),
 BOSSBOT_HQ_TIER + 16: (4216,),
 ELDER_TIER: (4000,
              4001,
              4002,
              4003,
              4004,
              4005,
              4006,
              4007,
              4008,
              4009,
              4010,
              4011)}
OptionalRewardTrackDict = {TT_TIER: (),
 TT_TIER + 1: (),
 TT_TIER + 2: (1000,
               601,
               601,
               602,
               602,
               2205,
               2206,
               2205,
               2206),
 TT_TIER + 3: (601,
               601,
               602,
               602,
               2205,
               2206,
               2205,
               2206),
 DD_TIER: (1000,
           602,
           602,
           603,
           603,
           2101,
           2102,
           2105,
           2106),
 DD_TIER + 1: (1000,
               602,
               602,
               603,
               603,
               2101,
               2102,
               2105,
               2106),
 DD_TIER + 2: (1000,
               602,
               602,
               603,
               603,
               2101,
               2102,
               2105,
               2106),
 DG_TIER: (1000,
           603,
           603,
           604,
           604,
           2501,
           2502,
           2503,
           2504,
           2505,
           2506),
 MM_TIER: (1000,
           604,
           604,
           605,
           605,
           2403,
           2404,
           2405,
           2406,
           2407,
           2408,
           2409),
 MM_TIER + 1: (1000,
               604,
               604,
               605,
               605,
               2403,
               2404,
               2405,
               2406,
               2407,
               2408,
               2409),
 MM_TIER + 2: (1000,
               604,
               604,
               605,
               605,
               2403,
               2404,
               2405,
               2406,
               2407,
               2408,
               2409),
 BR_TIER: (1000,
           606,
           606,
           606,
           606,
           606,
           607,
           607,
           607,
           607,
           607,
           2305,
           2306,
           2307,
           2308,
           2309,
           2310,
           2311),
 BR_TIER + 1: (1000,
               606,
               606,
               606,
               606,
               606,
               607,
               607,
               607,
               607,
               607,
               2305,
               2306,
               2307,
               2308,
               2309,
               2310,
               2311),
 BR_TIER + 2: (1000,
               606,
               606,
               606,
               606,
               606,
               607,
               607,
               607,
               607,
               607,
               2305,
               2306,
               2307,
               2308,
               2309,
               2310,
               2311),
 DL_TIER: (607,
           607,
           607,
           607,
           608,
           608,
           608,
           608,
           2901,
           2902,
           2907,
           2908,
           2909,
           2910,
           2911),
 DL_TIER + 1: (1000,
               607,
               607,
               607,
               607,
               608,
               608,
               608,
               608,
               2923,
               2924,
               2927,
               2928,
               2929,
               2930,
               2931),
 DL_TIER + 2: (608,
               608,
               608,
               608,
               609,
               609,
               609,
               609,
               2941,
               2942,
               2943,
               2944,
               2947,
               2948,
               2949,
               2950,
               2951),
 DL_TIER + 3: (1000,
               609,
               609,
               609,
               609,
               609,
               609,
               2961,
               2962,
               2963,
               2964,
               2965,
               2966,
               2967,
               2968,
               2969,
               2970,
               2971),
 ELDER_TIER: (1000,
              1000,
              610,
              611,
              612,
              613,
              614,
              615,
              616,
              617,
              618,
              2961,
              2962,
              2963,
              2964,
              2965,
              2966,
              2967,
              2968,
              2969,
              2970,
              2971)}


def isRewardOptional(tier, rewardId):
    return tier in OptionalRewardTrackDict and rewardId in OptionalRewardTrackDict[tier]


def getItemName(itemId):
    return ItemDict[itemId][0]


def avatarWorkingOnRequiredRewards(av):
    tier = av.getRewardTier()
    rewardList = list(getRewardsInTier(tier))
    for i in range(len(rewardList)):
        actualRewardId = transformReward(rewardList[i])
        rewardList[i] = actualRewardId

    for questDesc in av.quests:
        questId = questDesc[0]
        rewardId = questDesc[3]
        if rewardId in rewardList:
            return 1
        elif rewardId == NA:
            rewardId = transformReward(getFinalRewardId(questId, fAll=1))
            if rewardId in rewardList:
                return 1

    return 0


def avatarHasAllRequiredRewards(av, tier):
    rewardHistory = list(av.getRewardHistory()[1])
    rewardList = getRewardsInTier(tier)
    notify.debug('checking avatarHasAllRequiredRewards: history: %s, tier: %s' % (rewardHistory, rewardList))
    for rewardId in rewardList:
        if rewardId == 900:
            found = 0
            for actualRewardId in (901, 902, 903, 904, 905, 906, 907):
                if actualRewardId in rewardHistory:
                    found = 1
                    rewardHistory.remove(actualRewardId)
                    if notify.getDebug():
                        notify.debug('avatarHasAllRequiredRewards: rewardId 900 found as: %s' % actualRewardId)
                    break

            if not found:
                if notify.getDebug():
                    notify.debug('avatarHasAllRequiredRewards: rewardId 900 not found')
                return 0
        else:
            actualRewardId = transformReward(rewardId)
            if actualRewardId in rewardHistory:
                rewardHistory.remove(actualRewardId)
            elif getRewardClass(rewardId) == CogSuitPartReward:
                deptStr = RewardDict.get(rewardId)[1]
                cogPart = RewardDict.get(rewardId)[2]
                dept = ToontownGlobals.cogDept2index[deptStr]
                if av.hasCogPart(cogPart, dept):
                    if notify.getDebug():
                        notify.debug('avatarHasAllRequiredRewards: rewardId: %s counts, avatar has cog part: %s dept: %s' % (actualRewardId, cogPart, dept))
                else:
                    if notify.getDebug():
                        notify.debug('avatarHasAllRequiredRewards: CogSuitPartReward: %s not found' % actualRewardId)
                    return 0
            else:
                if notify.getDebug():
                    notify.debug('avatarHasAllRequiredRewards: rewardId %s not found' % actualRewardId)
                return 0

    if notify.getDebug():
        notify.debug('avatarHasAllRequiredRewards: remaining rewards: %s' % rewardHistory)
        for rewardId in rewardHistory:
            if not isRewardOptional(tier, rewardId):
                notify.warning('required reward found, expected only optional: %s' % rewardId)

    return 1