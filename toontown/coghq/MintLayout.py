from direct.directnotify import DirectNotifyGlobal
from direct.showbase.PythonUtil import invertDictLossless
from toontown.coghq import MintRoomSpecs
from toontown.toonbase import ToontownGlobals
from direct.showbase.PythonUtil import normalDistrib, lerp
import random

def printAllCashbotInfo():
    print('roomId: roomName')
    for roomId, roomName in list(MintRoomSpecs.CashbotMintRoomId2RoomName.items()):
        print('%s: %s' % (roomId, roomName))

    print('\nroomId: numBattles')
    for roomId, numBattles in list(MintRoomSpecs.roomId2numBattles.items()):
        print('%s: %s' % (roomId, numBattles))

    print('\nmintId floor roomIds')
    printMintRoomIds()
    print('\nmintId floor numRooms')
    printNumRooms()
    print('\nmintId floor numForcedBattles')
    printNumBattles()


def iterateCashbotMints(func):
    from toontown.toonbase import ToontownGlobals
    for mintId in [ToontownGlobals.CashbotMintIntA, ToontownGlobals.CashbotMintIntB, ToontownGlobals.CashbotMintIntC]:
        for floorNum in range(ToontownGlobals.MintNumFloors[mintId]):
            func(MintLayout(mintId, floorNum))


def printMintInfo():

    def func(ml):
        print(ml)

    iterateCashbotMints(func)


def printMintRoomIds():

    def func(ml):
        print(ml.getMintId(), ml.getFloorNum(), ml.getRoomIds())

    iterateCashbotMints(func)


def printMintRoomNames():

    def func(ml):
        print(ml.getMintId(), ml.getFloorNum(), ml.getRoomNames())

    iterateCashbotMints(func)


def printNumRooms():

    def func(ml):
        print(ml.getMintId(), ml.getFloorNum(), ml.getNumRooms())

    iterateCashbotMints(func)


def printNumBattles():

    def func(ml):
        print(ml.getMintId(), ml.getFloorNum(), ml.getNumBattles())

    iterateCashbotMints(func)


BakedFloorLayouts = {12500:
         {0: (0,
             13,
             4,
             1,
             15,
             5,
             11,
             7,
             17),
         1: (0,
             4,
             13,
             1,
             15,
             5,
             11,
             7,
             18),
         2: (0,
             4,
             1,
             15,
             13,
             5,
             11,
             7,
             20),
         3: (0,
             4,
             1,
             13,
             15,
             5,
             11,
             7,
             22),
         4: (0,
             4,
             1,
             15,
             5,
             11,
             7,
             13,
             23),
         5: (0,
             14,
             1,
             13,
             12,
             7,
             11,
             6,
             25),
         6: (0,
             14,
             1,
             12,
             7,
             13,
             11,
             6,
             18),
         7: (0,
             14,
             1,
             13,
             12,
             7,
             11,
             6,
             19),
         8: (0,
             14,
             1,
             12,
             7,
             11,
             13,
             6,
             21),
         9: (0,
             14,
             1,
             13,
             12,
             7,
             11,
             6,
             23),
         10: (0,
              6,
              11,
              4,
              9,
              1,
              4,
              13,
              24),
         11: (0,
              6,
              11,
              4,
              13,
              9,
              1,
              4,
              17),
         12: (0,
              6,
              11,
              4,
              9,
              1,
              13,
              4,
              19),
         13: (0,
              6,
              11,
              4,
              13,
              9,
              1,
              4,
              20),
         14: (0,
              6,
              11,
              4,
              9,
              13,
              1,
              4,
              22),
         15: (0,
              16,
              11,
              13,
              12,
              3,
              1,
              6,
              8,
              24),
         16: (0,
              16,
              11,
              12,
              3,
              1,
              6,
              13,
              8,
              25),
         17: (0,
              16,
              11,
              12,
              13,
              3,
              1,
              6,
              8,
              18),
         18: (0,
              16,
              11,
              12,
              3,
              13,
              1,
              6,
              8,
              20),
         19: (0,
              16,
              11,
              12,
              13,
              3,
              1,
              6,
              8,
              21)},
 12600: {0: (0,
             13,
             4,
             1,
             15,
             5,
             11,
             7,
             17),
         1: (0,
             4,
             13,
             1,
             15,
             5,
             11,
             7,
             18),
         2: (0,
             4,
             1,
             15,
             13,
             5,
             11,
             7,
             20),
         3: (0,
             4,
             1,
             13,
             15,
             5,
             11,
             7,
             22),
         4: (0,
             4,
             1,
             15,
             5,
             11,
             7,
             13,
             23),
         5: (0,
             14,
             1,
             13,
             12,
             7,
             11,
             6,
             25),
         6: (0,
             14,
             1,
             12,
             7,
             13,
             11,
             6,
             18),
         7: (0,
             14,
             1,
             13,
             12,
             7,
             11,
             6,
             19),
         8: (0,
             14,
             1,
             12,
             7,
             11,
             13,
             6,
             21),
         9: (0,
             14,
             1,
             13,
             12,
             7,
             11,
             6,
             23),
         10: (0,
              6,
              11,
              4,
              9,
              1,
              4,
              13,
              24),
         11: (0,
              6,
              11,
              4,
              13,
              9,
              1,
              4,
              17),
         12: (0,
              6,
              11,
              4,
              9,
              1,
              13,
              4,
              19),
         13: (0,
              6,
              11,
              4,
              13,
              9,
              1,
              4,
              20),
         14: (0,
              6,
              11,
              4,
              9,
              13,
              1,
              4,
              22),
         15: (0,
              16,
              11,
              13,
              12,
              3,
              1,
              6,
              8,
              24),
         16: (0,
              16,
              11,
              12,
              3,
              1,
              6,
              13,
              8,
              25),
         17: (0,
              16,
              11,
              12,
              13,
              3,
              1,
              6,
              8,
              18),
         18: (0,
              16,
              11,
              12,
              3,
              13,
              1,
              6,
              8,
              20),
         19: (0,
              16,
              11,
              12,
              13,
              3,
              1,
              6,
              8,
              21)},
 12700: {0: (0,
             13,
             4,
             1,
             15,
             5,
             11,
             7,
             17),
         1: (0,
             4,
             13,
             1,
             15,
             5,
             11,
             7,
             18),
         2: (0,
             4,
             1,
             15,
             13,
             5,
             11,
             7,
             20),
         3: (0,
             4,
             1,
             13,
             15,
             5,
             11,
             7,
             22),
         4: (0,
             4,
             1,
             15,
             5,
             11,
             7,
             13,
             23),
         5: (0,
             14,
             1,
             13,
             12,
             7,
             11,
             6,
             25),
         6: (0,
             14,
             1,
             12,
             7,
             13,
             11,
             6,
             18),
         7: (0,
             14,
             1,
             13,
             12,
             7,
             11,
             6,
             19),
         8: (0,
             14,
             1,
             12,
             7,
             11,
             13,
             6,
             21),
         9: (0,
             14,
             1,
             13,
             12,
             7,
             11,
             6,
             23),
         10: (0,
              6,
              11,
              4,
              9,
              1,
              4,
              13,
              24),
         11: (0,
              6,
              11,
              4,
              13,
              9,
              1,
              4,
              17),
         12: (0,
              6,
              11,
              4,
              9,
              1,
              13,
              4,
              19),
         13: (0,
              6,
              11,
              4,
              13,
              9,
              1,
              4,
              20),
         14: (0,
              6,
              11,
              4,
              9,
              13,
              1,
              4,
              22),
         15: (0,
              16,
              11,
              13,
              12,
              3,
              1,
              6,
              8,
              24),
         16: (0,
              16,
              11,
              12,
              3,
              1,
              6,
              13,
              8,
              25),
         17: (0,
              16,
              11,
              12,
              13,
              3,
              1,
              6,
              8,
              18),
         18: (0,
              16,
              11,
              12,
              3,
              13,
              1,
              6,
              8,
              20),
         19: (0,
              16,
              11,
              12,
              13,
              3,
              1,
              6,
              8,
              21)}}

class MintLayout:
    notify = DirectNotifyGlobal.directNotify.newCategory('MintLayout')

    def __init__(self, mintId, floorNum):
        self.mintId = mintId
        self.floorNum = floorNum
        self.roomIds = []
        self.hallways = []
        self.numRooms = 1 + ToontownGlobals.MintNumRooms[self.mintId][self.floorNum]
        self.numHallways = self.numRooms - 1
        if self.mintId in BakedFloorLayouts and self.floorNum in BakedFloorLayouts[self.mintId]:
            self.roomIds = list(BakedFloorLayouts[self.mintId][self.floorNum])
        else:
            self.roomIds = self._genFloorLayout()
        hallwayRng = self.getRng()
        connectorRoomNames = MintRoomSpecs.CashbotMintConnectorRooms
        for i in range(self.numHallways):
            self.hallways.append(hallwayRng.choice(connectorRoomNames))

    def _genFloorLayout(self):
        rng = self.getRng()
        startingRoomIDs = MintRoomSpecs.CashbotMintEntranceIDs
        middleRoomIDs = MintRoomSpecs.CashbotMintMiddleRoomIDs
        finalRoomIDs = MintRoomSpecs.CashbotMintFinalRoomIDs

        numBattlesLeft = ToontownGlobals.MintNumBattles[self.mintId]

        finalRoomId = rng.choice(finalRoomIDs)
        numBattlesLeft -= MintRoomSpecs.getNumBattles(finalRoomId)

        middleRoomIds = []
        middleRoomsLeft = self.numRooms - 2

        numBattles2middleRoomIds = invertDictLossless(MintRoomSpecs.middleRoomId2numBattles)

        allBattleRooms = []
        for num, roomIds in list(numBattles2middleRoomIds.items()):
            if num > 0:
                allBattleRooms.extend(roomIds)
        while 1:
            allBattleRoomIds = list(allBattleRooms)
            rng.shuffle(allBattleRoomIds)
            battleRoomIds = self._chooseBattleRooms(numBattlesLeft,
                                                    allBattleRoomIds)
            if battleRoomIds is not None:
                break

            MintLayout.notify.info('could not find a valid set of battle rooms, trying again')

        middleRoomIds.extend(battleRoomIds)
        middleRoomsLeft -= len(battleRoomIds)

        if middleRoomsLeft > 0:
            actionRoomIds = numBattles2middleRoomIds[0]
            for i in range(middleRoomsLeft):
                roomId = rng.choice(actionRoomIds)
                actionRoomIds.remove(roomId)
                middleRoomIds.append(roomId)

        roomIds = []

        roomIds.append(rng.choice(startingRoomIDs))

        rng.shuffle(middleRoomIds)
        roomIds.extend(middleRoomIds)

        roomIds.append(finalRoomId)

        return roomIds

    def getNumRooms(self):
        return len(self.roomIds)

    def getRoomId(self, n):
        return self.roomIds[n]

    def getRoomIds(self):
        return self.roomIds[:]

    def getRoomNames(self):
        names = []
        for roomId in self.roomIds:
            names.append(MintRoomSpecs.CashbotMintRoomId2RoomName[roomId])

        return names

    def getNumHallways(self):
        return len(self.hallways)

    def getHallwayModel(self, n):
        # sanity check
        if n >= len(self.hallways):
            self.notify.warning(f'Hallway model {n} not found in {self.hallways}')
            n = len(self.hallways) - 1
        return self.hallways[n]

    def getNumBattles(self):
        numBattles = 0
        for roomId in self.getRoomIds():
            numBattles += MintRoomSpecs.roomId2numBattles[roomId]

        return numBattles

    def getMintId(self):
        return self.mintId

    def getFloorNum(self):
        return self.floorNum

    def getRng(self):
        return random.Random(self.mintId * self.floorNum)

    def _chooseBattleRooms(self, numBattlesLeft, allBattleRoomIds, baseIndex = 0, chosenBattleRooms = None):
        if chosenBattleRooms is None:
            chosenBattleRooms = []
        while baseIndex < len(allBattleRoomIds):
            nextRoomId = allBattleRoomIds[baseIndex]
            baseIndex += 1
            newNumBattlesLeft = numBattlesLeft - MintRoomSpecs.middleRoomId2numBattles[nextRoomId]
            if newNumBattlesLeft < 0:
                continue
            elif newNumBattlesLeft == 0:
                chosenBattleRooms.append(nextRoomId)
                return chosenBattleRooms
            chosenBattleRooms.append(nextRoomId)
            result = self._chooseBattleRooms(newNumBattlesLeft, allBattleRoomIds, baseIndex, chosenBattleRooms)
            if result is not None:
                return result
            else:
                del chosenBattleRooms[-1:]
        else:
            return

        return

    def __str__(self):
        return 'MintLayout: id=%s, floor=%s, numRooms=%s, numBattles=%s' % (self.mintId,
         self.floorNum,
         self.getNumRooms(),
         self.getNumBattles())

    def __repr__(self):
        return str(self)
