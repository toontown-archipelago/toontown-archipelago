from direct.distributed.ClockDelta import *
from direct.showbase import DirectObject
from direct.directnotify import DirectNotifyGlobal
from direct.task import Task
import random
from . import TreasurePlannerAI, TreasureGlobals

class RegenTreasurePlannerAI(TreasurePlannerAI.TreasurePlannerAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('RegenTreasurePlannerAI')

    def __init__(self, zoneId, treasureConstructor, taskName, spawnInterval=TreasureGlobals.HOOD_SPAWN_FREQUENCY, maxTreasures=TreasureGlobals.HOOD_SPAWN_CAP, callback = None):
        TreasurePlannerAI.TreasurePlannerAI.__init__(self, zoneId, treasureConstructor, callback)
        self.taskName = '%s-%s' % (taskName, zoneId)
        self.spawnInterval = spawnInterval
        self.maxTreasures = maxTreasures
        if zoneId in TreasureGlobals.healAmounts:
            self.healAmount = TreasureGlobals.healAmounts[zoneId]
        else:
            self.healAmount = 0

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

    def preSpawnTreasures(self):
        for i in range(self.maxTreasures):
            self.placeRandomTreasure()
