from direct.showbase.PythonUtil import invertDict
from toontown.toonbase import ToontownGlobals
from toontown.coghq import NullCogs
from toontown.coghq import LawbotOfficeOilRoom_Battle00_Cogs
from toontown.coghq import LawbotOfficeOilRoom_Battle01_Cogs
from toontown.coghq import LawbotOfficeBoilerRoom_Battle00_Cogs
from toontown.coghq import LawbotOfficeBoilerRoom_Trap00_Cogs
from toontown.coghq import LawbotOfficeLobby_Trap00_Cogs
from toontown.coghq import LawbotOfficeDiamondRoom_Trap00_Cogs
from toontown.coghq import LawbotOfficeDiamondRoom_Battle00_Cogs
from toontown.coghq import LawbotOfficeGearRoom_Battle00_Cogs

from toontown.coghq import LawbotOfficeEntrance_Action00
from toontown.coghq import LawbotOfficeOilRoom_Battle00
from toontown.coghq import LawbotOfficeOilRoom_Battle01
from toontown.coghq import LawbotOfficeBoilerRoom_Security00
from toontown.coghq import LawbotOfficeBoilerRoom_Battle00
from toontown.coghq import LawbotOfficeGearRoom_Action00
from toontown.coghq import LawbotOfficeLobby_Action00
from toontown.coghq import LawbotOfficeGearRoom_Security00
from toontown.coghq import LawbotOfficeLobby_Trap00
from toontown.coghq import LawbotOfficeDiamondRoom_Security00
from toontown.coghq import LawbotOfficeDiamondRoom_Trap00
from toontown.coghq import LawbotOfficeGearRoom_Platform00
from toontown.coghq import LawbotOfficeLobby_Lights00
from toontown.coghq import LawbotOfficeBoilerRoom_Action01
from toontown.coghq import LawbotOfficeDiamondRoom_Action00
from toontown.coghq import LawbotOfficeDiamondRoom_Action01
from toontown.coghq import LawbotOfficeLobby_Action01
from toontown.coghq import LawbotOfficeDiamondRoom_Battle00
from toontown.coghq import LawbotOfficeGearRoom_Battle00


LawbotStageSpecModules = {
    0: LawbotOfficeEntrance_Action00,
    1: LawbotOfficeOilRoom_Battle00,
    2: LawbotOfficeOilRoom_Battle01,
    3: LawbotOfficeBoilerRoom_Security00,
    4: LawbotOfficeBoilerRoom_Battle00,
    5: LawbotOfficeGearRoom_Action00,
    6: LawbotOfficeLobby_Action00,
    7: LawbotOfficeGearRoom_Security00,
    8: LawbotOfficeLobby_Trap00,
    9: LawbotOfficeDiamondRoom_Security00,
    10: LawbotOfficeDiamondRoom_Trap00,
    11: LawbotOfficeGearRoom_Platform00,
    12: LawbotOfficeLobby_Lights00,
    100: LawbotOfficeBoilerRoom_Action01,
    101: LawbotOfficeDiamondRoom_Action00,
    102: LawbotOfficeDiamondRoom_Action01,
    103: LawbotOfficeLobby_Action01,
    104: LawbotOfficeDiamondRoom_Battle00,
    105: LawbotOfficeGearRoom_Battle00,
}

# Ok don't freak out. What we are doing here is grabbing the name of the module that we imported.
# The problem is that it will include the path to this python module meaning we get: toontown.coghq.<MODULE_NAME>
# All we are doing is splitting the string by the periods, and grabbing the last section of it.
# For example, 'toontown.coghq.LawbotOfficeDiamondRoom_Trap00' becomes 'LawbotOfficeDiamondRoom_Trap00'
LawbotStageRoomId2RoomName = {_id: module.__name__.split('.')[-1] for _id, module in LawbotStageSpecModules.items()}

CogSpecModules = {
    'LawbotOfficeOilRoom_Battle00': LawbotOfficeOilRoom_Battle00_Cogs,
    'LawbotOfficeOilRoom_Battle01': LawbotOfficeOilRoom_Battle01_Cogs,
    'LawbotOfficeBoilerRoom_Battle00': LawbotOfficeBoilerRoom_Battle00_Cogs,
    'LawbotOfficeBoilerRoom_Trap00': LawbotOfficeBoilerRoom_Trap00_Cogs,
    'LawbotOfficeLobby_Trap00': LawbotOfficeLobby_Trap00_Cogs,
    'LawbotOfficeDiamondRoom_Trap00': LawbotOfficeDiamondRoom_Trap00_Cogs,
    'LawbotOfficeDiamondRoom_Battle00': LawbotOfficeDiamondRoom_Battle00_Cogs,
    'LawbotOfficeGearRoom_Battle00': LawbotOfficeGearRoom_Battle00_Cogs
}


def getStageRoomSpecModule(roomId):
    return LawbotStageSpecModules[roomId]


def getCogSpecModule(roomId):
    roomName = LawbotStageRoomId2RoomName[roomId]
    return CogSpecModules.get(roomName, NullCogs)


def getNumBattles(roomId):
    return roomId2numBattles[roomId]


CashbotStageRoomName2RoomId = invertDict(LawbotStageRoomId2RoomName)
CashbotStageEntranceIDs = (0,)
CashbotStageMiddleRoomIDs = (1,)
CashbotStageFinalRoomIDs = (2,)
CashbotStageConnectorRooms = ('phase_11/models/lawbotHQ/LB_connector_7cubeL2', 'phase_11/models/lawbotHQ/LB_connector_7cubeLR')


roomId2numBattles = {}
for roomName, roomId in list(CashbotStageRoomName2RoomId.items()):
    if roomName not in CogSpecModules:
        roomId2numBattles[roomId] = 0
    else:
        cogSpecModule = CogSpecModules[roomName]
        roomId2numBattles[roomId] = len(cogSpecModule.BattleCells)

roomId2numCogs = {}
for roomName, roomId in list(CashbotStageRoomName2RoomId.items()):
    if roomName not in CogSpecModules:
        roomId2numCogs[roomId] = 0
    else:
        cogSpecModule = CogSpecModules[roomName]
        roomId2numCogs[roomId] = len(cogSpecModule.CogData)

roomId2numCogLevels = {}
for roomName, roomId in list(CashbotStageRoomName2RoomId.items()):
    if roomName not in CogSpecModules:
        roomId2numCogLevels[roomId] = 0
    else:
        cogSpecModule = CogSpecModules[roomName]
        levels = 0
        for cogData in cogSpecModule.CogData:
            levels += cogData['level']

        roomId2numCogLevels[roomId] = levels

roomId2numMeritCogLevels = {}
for roomName, roomId in list(CashbotStageRoomName2RoomId.items()):
    if roomName not in CogSpecModules or roomId in (8, 10):
        roomId2numMeritCogLevels[roomId] = 0
    else:
        cogSpecModule = CogSpecModules[roomName]
        levels = 0
        for cogData in cogSpecModule.CogData:
            levels += cogData['level']

        roomId2numMeritCogLevels[roomId] = levels

middleRoomId2numBattles = {}
for roomId in CashbotStageMiddleRoomIDs:
    middleRoomId2numBattles[roomId] = roomId2numBattles[roomId]
