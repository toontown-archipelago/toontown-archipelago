from panda3d.core import *

from otp.otpbase.PythonUtil import clampScalar
from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedSmoothNodeAI
from direct.distributed import DistributedSmoothNodeBase
from direct.distributed import ClockDelta
from direct.fsm import ClassicFSM, State
from toontown.toonbase import ToontownGlobals
from direct.task import Task
from toontown.pets import PetLookerAI
from toontown.pets import PetConstants, PetTraits
from toontown.pets import PetBase, PetTricks
from toontown.toon import DistributedToonAI
import random
import time

from direct.showbase.PythonUtil import StackTrace


class DistributedPetAI(DistributedSmoothNodeAI.DistributedSmoothNodeAI, PetLookerAI.PetLookerAI, PetBase.PetBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPetAI')
    movieTimeSwitch = {PetConstants.PET_MOVIE_FEED: PetConstants.FEED_TIME,
     PetConstants.PET_MOVIE_SCRATCH: PetConstants.SCRATCH_TIME,
     PetConstants.PET_MOVIE_CALL: PetConstants.CALL_TIME}
    movieDistSwitch = {PetConstants.PET_MOVIE_FEED: PetConstants.FEED_DIST.get,
     PetConstants.PET_MOVIE_SCRATCH: PetConstants.SCRATCH_DIST.get}

    def __init__(self, air, dna = None):
        DistributedSmoothNodeAI.DistributedSmoothNodeAI.__init__(self, air)
        PetLookerAI.PetLookerAI.__init__(self)
        self.ownerId = 0
        self.petName = 'unnamed'
        self.traitSeed = 0
        self.safeZone = ToontownGlobals.ToontownCentral
        self.initialDNA = dna
        self.active = 1
        self.activated = 0
        self._outOfBounds = False
        self.traitList = [0] * PetTraits.PetTraits.NumTraits
        self.head = -1
        self.ears = -1
        self.nose = -1
        self.tail = -1
        self.bodyTexture = 0
        self.color = 0
        self.colorScale = 0
        self.eyeColor = 0
        self.gender = 0
        self.movieMode = None
        self.lockMoverEnabled = 0
        self.trickAptitudes = []
        self.inEstate = 0
        self.estateOwnerId = None
        self.estateZones = []
        self.lastSeenTimestamp = self.getCurEpochTimestamp()
        self.requiredMoodComponents = {}
        self.__funcsToDelete = []

        self.busy = 0
        self.gaitFSM = ClassicFSM.ClassicFSM('petGaitFSM', [State.State('off', self.gaitEnterOff, self.gaitExitOff),
         State.State('neutral', self.gaitEnterNeutral, self.gaitExitNeutral),
         State.State('happy', self.gaitEnterHappy, self.gaitExitHappy),
         State.State('sad', self.gaitEnterSad, self.gaitExitSad)], 'off', 'off')
        self.gaitFSM.enterInitialState()
        self.unstickFSM = ClassicFSM.ClassicFSM('unstickFSM', [State.State('off', self.unstickEnterOff, self.unstickExitOff), State.State('on', self.unstickEnterOn, self.unstickExitOn)], 'off', 'off')
        self.unstickFSM.enterInitialState()

    def setInactive(self):
        self.active = 0

    def setDNA(self, dna):
        head, ears, nose, tail, body, color, colorScale, eyes, gender = dna
        self.b_setHead(head)
        self.b_setEars(ears)
        self.b_setNose(nose)
        self.b_setTail(tail)
        self.b_setBodyTexture(body)
        self.b_setColor(color)
        self.b_setColorScale(colorScale)
        self.b_setEyeColor(eyes)
        self.b_setGender(gender)

    def getOwnerId(self):
        return self.ownerId

    def b_setOwnerId(self, ownerId):
        self.d_setOwnerId(ownerId)
        self.setOwnerId(ownerId)

    def d_setOwnerId(self, ownerId):
        self.sendUpdate('setOwnerId', [ownerId])

    def setOwnerId(self, ownerId):
        self.ownerId = ownerId

    def getPetName(self):
        return self.petName

    def b_setPetName(self, petName):
        self.d_setPetName(petName)
        self.setPetName(petName)

    def d_setPetName(self, petName):
        self.sendUpdate('setPetName', [petName])

    def setPetName(self, petName):
        self.petName = petName
        DistributedSmoothNodeAI.DistributedSmoothNodeAI.setName(self, self.petName)

    def getTraitSeed(self):
        return self.traitSeed

    def b_setTraitSeed(self, traitSeed):
        self.d_setTraitSeed(traitSeed)
        self.setTraitSeed(traitSeed)

    def d_setTraitSeed(self, traitSeed):
        self.sendUpdate('setTraitSeed', [traitSeed])

    def setTraitSeed(self, traitSeed):
        self.traitSeed = traitSeed

    def getSafeZone(self):
        return self.safeZone

    def b_setSafeZone(self, safeZone):
        self.d_setSafeZone(safeZone)
        self.setSafeZone(safeZone)

    def d_setSafeZone(self, safeZone):
        self.sendUpdate('setSafeZone', [safeZone])

    def setSafeZone(self, safeZone):
        self.safeZone = safeZone

    def setTraits(self, traitList):
        self.traitList = traitList

    def getHead(self):
        return self.head

    def b_setHead(self, head):
        self.d_setHead(head)
        self.setHead(head)

    def d_setHead(self, head):
        self.sendUpdate('setHead', [head])

    def setHead(self, head):
        self.head = head

    def getEars(self):
        return self.ears

    def b_setEars(self, ears):
        self.d_setEars(ears)
        self.setEars(ears)

    def d_setEars(self, ears):
        self.sendUpdate('setEars', [ears])

    def setEars(self, ears):
        self.ears = ears

    def getNose(self):
        return self.nose

    def b_setNose(self, nose):
        self.d_setNose(nose)
        self.setNose(nose)

    def d_setNose(self, nose):
        self.sendUpdate('setNose', [nose])

    def setNose(self, nose):
        self.nose = nose

    def getTail(self):
        return self.tail

    def b_setTail(self, tail):
        self.d_setTail(tail)
        self.setTail(tail)

    def d_setTail(self, tail):
        self.sendUpdate('setTail', [tail])

    def setTail(self, tail):
        self.tail = tail

    def getBodyTexture(self):
        return self.bodyTexture

    def b_setBodyTexture(self, bodyTexture):
        self.d_setBodyTexture(bodyTexture)
        self.setBodyTexture(bodyTexture)

    def d_setBodyTexture(self, bodyTexture):
        self.sendUpdate('setBodyTexture', [bodyTexture])

    def setBodyTexture(self, bodyTexture):
        self.bodyTexture = bodyTexture

    def getColor(self):
        return self.color

    def b_setColor(self, color):
        self.d_setColor(color)
        self.setColor(color)

    def d_setColor(self, color):
        self.sendUpdate('setColor', [color])

    def setColor(self, color):
        self.color = color

    def getColorScale(self):
        return self.colorScale

    def b_setColorScale(self, colorScale):
        self.d_setColorScale(colorScale)
        self.setColorScale(colorScale)

    def d_setColorScale(self, colorScale):
        self.sendUpdate('setColorScale', [colorScale])

    def setColorScale(self, colorScale):
        self.colorScale = colorScale

    def getEyeColor(self):
        return self.eyeColor

    def b_setEyeColor(self, eyeColor):
        self.d_setEyeColor(eyeColor)
        self.setEyeColor(eyeColor)

    def d_setEyeColor(self, eyeColor):
        self.sendUpdate('setEyeColor', [eyeColor])

    def setEyeColor(self, eyeColor):
        self.eyeColor = eyeColor

    def getGender(self):
        return self.gender

    def b_setGender(self, gender):
        self.d_setGender(gender)
        self.setGender(gender)

    def d_setGender(self, gender):
        self.sendUpdate('setGender', [gender])

    def setGender(self, gender):
        self.gender = gender

    def teleportIn(self, timestamp = None):
        self.notify.debug('DPAI: teleportIn')
        timestamp = ClockDelta.globalClockDelta.getRealNetworkTime()
        self.notify.debug('DPAI: sending update @ ts = %s' % timestamp)
        self.sendUpdate('teleportIn', [timestamp])
        return None

    def teleportOut(self, timestamp = None):
        self.notify.debug('DPAI: teleportOut')
        timestamp = ClockDelta.globalClockDelta.getRealNetworkTime()
        self.notify.debug('DPAI: sending update @ ts = %s' % timestamp)
        self.sendUpdate('teleportOut', [timestamp])
        return None

    def getLastSeenTimestamp(self):
        return self.lastSeenTimestamp

    def b_setLastSeenTimestamp(self, timestamp):
        self.d_setLastSeenTimestamp(timestamp)
        self.setLastSeenTimestamp(timestamp)

    def d_setLastSeenTimestamp(self, timestamp):
        self.sendUpdate('setLastSeenTimestamp', [timestamp])

    def setLastSeenTimestamp(self, timestamp):
        self.lastSeenTimestamp = timestamp

    def getCurEpochTimestamp(self):
        return int(time.time())

    def getTimeSinceLastSeen(self):
        t = time.time() - self.lastSeenTimestamp
        return max(0.0, t)

    def getTrickAptitudes(self):
        return self.trickAptitudes

    def b_setTrickAptitudes(self, aptitudes):
        self.setTrickAptitudes(aptitudes, local=1)
        self.d_setTrickAptitudes(aptitudes)

    def d_setTrickAptitudes(self, aptitudes):

        while len(aptitudes) < len(PetTricks.Tricks) - 1:
            aptitudes.append(0.0)

        self.sendUpdate('setTrickAptitudes', [aptitudes])

    def setTrickAptitudes(self, aptitudes, local = 0):
        if not local:
            DistributedPetAI.notify.debug('setTrickAptitudes: %s' % aptitudes)
        while len(self.trickAptitudes) < len(PetTricks.Tricks) - 1:
            self.trickAptitudes.append(0.0)

        self.trickAptitudes = aptitudes

    def getTrickAptitude(self, trickId):
        if trickId > len(self.trickAptitudes) - 1:
            return 0.0
        return self.trickAptitudes[trickId]

    def setTrickAptitude(self, trickId, aptitude, send = 1):
        aptitude = clampScalar(aptitude, 0.0, 1.0)
        aptitudes = self.trickAptitudes
        while len(aptitudes) - 1 < trickId:
            aptitudes.append(0.0)

        if aptitudes[trickId] != aptitude:
            aptitudes[trickId] = aptitude
            if send:
                self.b_setTrickAptitudes(aptitudes)
            else:
                self.setTrickAptitudes(aptitudes, local=1)

    def _isPet(self):
        return 1

    def setHasRequestedDelete(self, flag):
        self._requestedDeleteFlag = flag

    def hasRequestedDelete(self):
        return self._requestedDeleteFlag

    def requestDelete(self, task = None):
        DistributedPetAI.notify.info('PetAI.requestDelete: %s, owner=%s' % (self.doId, self.ownerId))
        if self.hasRequestedDelete():
            DistributedPetAI.notify.info('PetAI.requestDelete: %s, owner=%s returning immediately' % (self.doId, self.ownerId))
            return
        self.setHasRequestedDelete(True)
        self.b_setLastSeenTimestamp(self.getCurEpochTimestamp())
        DistributedSmoothNodeAI.DistributedSmoothNodeAI.requestDelete(self)

    def _doDeleteCleanup(self):
        taskMgr.remove(self.uniqueName('clearMovie'))
        taskMgr.remove(self.uniqueName('PetMovieWait'))
        taskMgr.remove(self.uniqueName('PetMovieClear'))
        taskMgr.remove(self.uniqueName('PetMovieComplete'))
        taskMgr.remove(self.getLockMoveTaskName())
        taskMgr.remove(self.getMoveTaskName())
        if hasattr(self, 'zoneId'):
            self.announceZoneChange(ToontownGlobals.QuietZone, self.zoneId)
        else:
            myDoId = 'No doId'
            myTaskName = 'No task name'
            myStackTrace = StackTrace().trace
            myOldStackTrace = 'No Trace'
            if hasattr(self, 'doId'):
                myDoId = self.doId
            if task:
                myTaskName = task.name
            if hasattr(self, 'destroyDoStackTrace'):
                myOldStackTrace = self.destroyDoStackTrace.trace
            simbase.air.writeServerEvent('Pet RequestDelete duplicate', myDoId, 'from task %s' % myTaskName)
            simbase.air.writeServerEvent('Pet RequestDelete duplicate StackTrace', myDoId, '%s' % myStackTrace)
            simbase.air.writeServerEvent('Pet RequestDelete duplicate OldStackTrace', myDoId, '%s' % myOldStackTrace)
            DistributedPetAI.notify.warning('double requestDelete from task %s' % myTaskName)
        self.setParent(ToontownGlobals.SPHidden)
        if hasattr(self, 'activated'):
            if self.activated:
                self.activated = 0
                self.exitPetLook()
                self.stopPosHprBroadcast()
        if hasattr(self, 'mood'):
            self.mood.destroy()
            del self.mood
        if hasattr(self, 'traits'):
            del self.traits
        try:
            for funcName in self.__funcsToDelete:
                del self.__dict__[funcName]

        except:
            pass

        if hasattr(self, 'gaitFSM'):
            if self.gaitFSM:
                self.gaitFSM.requestFinalState()
            del self.gaitFSM
        if hasattr(self, 'unstickFSM'):
            if self.unstickFSM:
                self.unstickFSM.requestFinalState()
            del self.unstickFSM
        PetLookerAI.PetLookerAI.destroy(self)
        self.ignoreAll()
        self._hasCleanedUp = True

    def delete(self):
        DistributedPetAI.notify.info('PetAI.delete: %s, owner=%s' % (self.doId, self.ownerId))
        if not self._hasCleanedUp:
            self._doDeleteCleanup()
        self.setHasRequestedDelete(False)
        DistributedSmoothNodeAI.DistributedSmoothNodeAI.delete(self)

    def patchDelete(self):
        for funcName in self.__funcsToDelete:
            del self.__dict__[funcName]

        del self.gaitFSM
        del self.unstickFSM
        PetLookerAI.PetLookerAI.destroy(self)
        self.doNotDeallocateChannel = True
        self.zoneId = None
        DistributedSmoothNodeAI.DistributedSmoothNodeAI.delete(self)
        self.ignoreAll()
        return

    def getMoveTaskName(self):
        return 'petMove-%s' % self.doId

    def getLockMoveTaskName(self):
        return 'petLockMove-%s' % self.doId

    def move(self, task = None):
        pass

    def startPosHprBroadcast(self):
        if self._outOfBounds:
            return
        DistributedSmoothNodeAI.DistributedSmoothNodeAI.startPosHprBroadcast(self, period=simbase.petPosBroadcastPeriod, type=DistributedSmoothNodeBase.DistributedSmoothNodeBase.BroadcastTypes.XYH)

    def setMoodComponent(self, component, value):
        pass

    def addToMood(self, component, delta):
        pass

    def lerpMood(self, component, factor):
        pass

    def addToMoods(self, mood2delta):
        pass

    def lerpMoods(self, mood2factor):
        pass

    def handleMoodChange(self, components = [], distribute = 1):
        pass

    def isContented(self):
        return True

    def call(self, avatar):
        pass

    def feed(self, avatar):
        if avatar.takeMoney(PetConstants.FEED_AMOUNT):
            pass

    def scratch(self, avatar):
        pass

    def lockPet(self):
        DistributedPetAI.notify.debug('%s: lockPet' % self.doId)
        pass

    def isLockedDown(self):
        return False

    def unlockPet(self):
        pass

    def handleStay(self, avatar):
        pass

    def handleShoo(self, avatar):
        pass

    def gaitEnterOff(self):
        pass

    def gaitExitOff(self):
        pass

    def gaitEnterNeutral(self):
        pass

    def gaitExitNeutral(self):
        pass

    def gaitEnterHappy(self):
        pass

    def gaitExitHappy(self):
        pass

    def gaitEnterSad(self):
        pass

    def gaitExitSad(self):
        pass

    def unstickEnterOff(self):
        pass

    def unstickExitOff(self):
        pass

    def unstickEnterOn(self):
        pass

    def _handleCollided(self, collEntry):
        pass

    def unstickExitOn(self):
        pass

    def ownerIsOnline(self):
        return self.ownerId in simbase.air.doId2do

    def ownerIsInSameZone(self):
        if not self.ownerIsOnline():
            return 0
        return self.zoneId == simbase.air.doId2do[self.ownerId].zoneId

    def _getOwnerDict(self):
        pass

    def _getFullNearbyToonDict(self):
        toons = self.air.getObjectsOfClassInZone(self.air.districtId, self.zoneId, DistributedToonAI.DistributedToonAI)
        return toons

    def _getNearbyToonDict(self):
        toons = self._getFullNearbyToonDict()
        if self.ownerId in toons:
            del toons[self.ownerId]
        return toons

    def _getNearbyPetDict(self):
        pets = self.air.getObjectsOfClassInZone(self.air.districtId, self.zoneId, DistributedPetAI)
        if self.doId in pets:
            del pets[self.doId]
        return pets

    def _getNearbyAvatarDict(self):
        avs = self._getFullNearbyToonDict()
        avs.update(self._getNearbyPetDict())
        return avs

    def _getOwner(self):
        return self.air.doId2do.get(self.ownerId)

    def _getNearbyToon(self):
        nearbyToonDict = self._getFullNearbyToonDict()
        if not len(nearbyToonDict):
            return None
        return nearbyToonDict[random.choice(nearbyToonDict.keys())]

    def _getNearbyToonNonOwner(self):
        nearbyToonDict = self._getNearbyToonDict()
        if not len(nearbyToonDict):
            return None
        return nearbyToonDict[random.choice(nearbyToonDict.keys())]

    def _getNearbyPet(self):
        nearbyPetDict = self._getNearbyPetDict()
        if not len(nearbyPetDict):
            return None
        return nearbyPetDict[random.choice(nearbyPetDict.keys())]

    def _getNearbyAvatar(self):
        nearbyAvDict = self._getNearbyAvatarDict()
        if not len(nearbyAvDict):
            return None
        return nearbyAvDict[random.choice(nearbyAvDict.keys())]

    def isBusy(self):
        return self.busy > 0

    def freeAvatar(self, avId):
        self.sendUpdateToAvatarId(avId, 'freeAvatar', [])

    def avatarInteract(self, avId):
        av = self.air.doId2do.get(avId)
        if av is None:
            self.notify.warning('Avatar: %s not found' % avId)
            return 0
        if self.isBusy():
            self.notify.debug('freeing avatar!')
            self.freeAvatar(avId)
            return 0
        self.busy = avId
        self.notify.debug('sending update')
        self.sendUpdateToAvatarId(avId, 'avatarInteract', [avId])
        self.acceptOnce(self.air.getAvatarExitEvent(avId), self.__handleUnexpectedExit, extraArgs=[avId])
        return 1

    def rejectAvatar(self, avId):
        self.notify.error('rejectAvatar: should not be called by a pet!')

    def d_setMovie(self, avId, flag):
        self.sendUpdate('setMovie', [flag, avId, ClockDelta.globalClockDelta.getRealNetworkTime()])

    def sendClearMovie(self, task = None):
        if self.air != None:
            self.ignore(self.air.getAvatarExitEvent(self.busy))
        taskMgr.remove(self.uniqueName('clearMovie'))
        self.busy = 0
        self.d_setMovie(0, PetConstants.PET_MOVIE_CLEAR)
        return Task.done

    def __handleUnexpectedExit(self, avId):
        self.notify.warning('avatar:' + str(avId) + ' has exited unexpectedly')
        self.notify.warning('not busy with avId: %s, busy: %s ' % (avId, self.busy))
        taskMgr.remove(self.uniqueName('clearMovie'))
        self.sendClearMovie()

    def handleAvPetInteraction(self, mode, avId):
        if mode not in (PetConstants.PET_MOVIE_SCRATCH, PetConstants.PET_MOVIE_FEED, PetConstants.PET_MOVIE_CALL):
            self.air.writeServerEvent('suspicious', avId, 'DistributedPetAI: unknown mode: %s' % mode)
            return
        if self.avatarInteract(avId):
            self.notify.debug('handleAvPetInteraction() avatarInteract calling callback')
            self.movieMode = mode
            callback = {PetConstants.PET_MOVIE_SCRATCH: self.scratch,
             PetConstants.PET_MOVIE_FEED: self.feed,
             PetConstants.PET_MOVIE_CALL: self.call}.get(mode)
            callback(self.air.doId2do.get(avId))
        else:
            self.notify.debug('handleAvPetInteraction() avatarInteract was busy or unhappy')

    def __petMovieStart(self, avId):
        self.d_setMovie(avId, self.movieMode)
        time = self.movieTimeSwitch.get(self.movieMode)
        taskMgr.doMethodLater(time, self.__petMovieComplete, self.uniqueName('PetMovieComplete'))

    def __petMovieComplete(self, task = None):
        self.disableLockMover()
        self.unlockPet()
        self.sendClearMovie()
        self.movieMode = None
        return Task.done


    def getAverageDist(self):
        return 1.0

    def __lockPetMoveTask(self, avId):
        pass

    def endLockPetMove(self, avId):
        pass

    def enableLockMover(self):
        pass

    def isLockMoverEnabled(self):
        return self.lockMoverEnabled > 0

    def disableLockMover(self):
        pass

    def _willDoTrick(self, trickId):
        return True

    def _handleGotPositiveTrickFeedback(self, trickId, magnitude):
        if trickId == PetTricks.Tricks.BALK:
            return
        self.setTrickAptitude(trickId, self.getTrickAptitude(trickId) + PetTricks.MaxAptitudeIncrementGotPraise * magnitude)

    def toggleLeash(self, avId):
        response = 'leash OFF'
        return response
