from direct.distributed.ClockDelta import *
from direct.showbase import DirectObject
from direct.directnotify import DirectNotifyGlobal
from direct.task import Task
import random
from . import TreasurePlannerAI, TreasureGlobals

class ArchipelagoTreasurePlannerAI(TreasurePlannerAI.TreasurePlannerAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('ArchipelagoTreasurePlannerAI')

    def __init__(self, zoneId, treasureConstructor, archiIndex, treasureCount=4, callback=None):
        self.archiCode = zoneId + archiIndex
        TreasurePlannerAI.TreasurePlannerAI.__init__(self, zoneId, treasureConstructor, callback)
        self.taskName = '%s%s' % (zoneId, archiIndex)
        self.spawnInterval = 3
        self.maxTreasures = treasureCount

    def start(self):
        self.preSpawnTreasures()
        self.startSpawning()

    def stop(self):
        self.stopSpawning()

    def stopSpawning(self):
        taskMgr.remove(self.taskName)

    def startSpawning(self):
        self.stopSpawning()
        taskMgr.doMethodLater(self.spawnInterval, self.upkeepTreasurePopulation, self.taskName)

    def initSpawnPoints(self):
        self.spawnPoints = TreasureGlobals.archiSpawnPoints[self.archiCode]
        return self.spawnPoints

    def roomForNewTreasure(self):
        return self.numTreasures() < self.maxTreasures

    def upkeepTreasurePopulation(self, task):
        if self.numTreasures() < self.maxTreasures:
            self.placeRandomTreasure()
        taskMgr.doMethodLater(self.spawnInterval, self.upkeepTreasurePopulation, self.taskName)
        return Task.done

    def placeRandomTreasure(self):

        if not self.roomForNewTreasure():
            return

        self.notify.debug('Placing a Treasure...')
        spawnPointIndex = self.nthEmptyIndex(random.randrange(self.countEmptySpawnPoints()))
        self.placeTreasure(spawnPointIndex)

    def grabAttempt(self, avId, treasureId):
        if self.lastRequestId == avId:
            self.requestCount += 1
            now = globalClock.getFrameTime()
            elapsed = now - self.requestStartTime
            if elapsed > 10:
                self.requestCount = 1
                self.requestStartTime = now
            else:
                secondsPerGrab = elapsed / self.requestCount
                if self.requestCount >= 3 and secondsPerGrab <= 0.4:
                    simbase.air.writeServerEvent('suspicious', avId, 'TreasurePlannerAI.grabAttempt %s treasures in %s seconds' % (self.requestCount, elapsed))
        else:
            self.lastRequestId = avId
            self.requestCount = 1
            self.requestStartTime = globalClock.getFrameTime()
        index = self.findIndexOfTreasureId(treasureId)
        if index == None:
            pass
        else:
            av = simbase.air.doId2do.get(avId)
            if av == None:
                simbase.air.writeServerEvent('suspicious', avId, 'TreasurePlannerAI.grabAttempt unknown avatar')
                self.notify.warning('avid: %s does not exist' % avId)
            else:
                treasure = self.treasures[index]
                if treasure.validAvatar(av, self.archiCode):
                    self.treasures[index] = None
                    if self.callback:
                        self.callback(avId)
                    treasure.d_setGrab(avId, self.archiCode)
                    self.deleteTreasureSoon(treasure)
                else:
                    treasure.d_setReject()
        return

    def preSpawnTreasures(self):
        for i in range(self.maxTreasures):
            self.placeRandomTreasure()
