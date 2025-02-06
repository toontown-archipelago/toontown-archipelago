from direct.fsm import ClassicFSM
from direct.fsm import State
from direct.gui.DirectGui import *
from direct.showbase import DirectObject

from otp.otpbase import OTPGlobals
from otp.otpbase import OTPLocalizer
from otp.speedchat import SpeedChatGlobals
from otp.speedchat.SpeedChat import SpeedChat
from otp.speedchat.SpeedChatGlobals import speedChatStyles
from otp.speedchat.SpeedChatTypes import *
from toontown.chat import SpeedChatLocalizer
from toontown.speedchat import TTSCIndexedTerminal
from toontown.speedchat import TTSpeedChatGlobals
from toontown.speedchat.TTSpeedChatTypes import *
from toontown.toonbase import TTLocalizer

scStructure = [[SpeedChatLocalizer.SCMenuHello,
                {100: 0},
                {101: 0},
                {102: 0},
                {103: 0},
                {104: 0},
                {105: 0},
                106,
                107,
                108],
               [SpeedChatLocalizer.SCMenuBye,
                {200: 0},
                {201: 0},
                {202: 0},
                203,
                204,
                205,
                206,
                208,
                209,
                207],
               [SpeedChatLocalizer.SCMenuChitChat,
                [SpeedChatLocalizer.SCMenuChitChatEmoticons, 300, 301, 302, 303, 304, 305, 306, 307],
                400, 401, 402, 403, 404, 405, 406],
               [SpeedChatLocalizer.SCMenuReplies,
                [SpeedChatLocalizer.SCMenuRepliesGood, {500: 1}, 501, 502, 503],
                [SpeedChatLocalizer.SCMenuRepliesBad, 600, 601, {602: 2}, {603: 2}],
                [SpeedChatLocalizer.SCMenuHappy,
                 {700: 1}, {701: 1}, {702: 1}, {703: 1}, {704: 1}, {705: 1}, 706, 707, 708, 709, 710, 711, 712, 713],
                [SpeedChatLocalizer.SCMenuSad, {800: 2}, {801: 2}, 802, 803, 804, 805, 806, 807, 808],
                900, 901, 902, 903, 904, 905],
               [SpeedChatLocalizer.SCMenuFriendly,
                [SpeedChatLocalizer.SCMenuFriendlyCompliments,
                 [SpeedChatLocalizer.SCMenuFriendlyILike,
                  1100, 1101, 1102, 1103, 1104, 1105, 1106, 1107, 1108, 1109],
                 1000, 1001, 1002, 1003, 1004],
                1200, 1201, 1202, 1203, 1204, 1205, 1206, 1207, 1208, 1209, 1210,
                ],
               [SpeedChatLocalizer.SCMenuSorry,
                [SpeedChatLocalizer.SCMenuSorryBugs, 1300, 1301, 1302, 1303],
                1400, 1401, 1402, 1403, 1404, 1405, 1406, 1407, 1408, 1409, 1410
                ],
               [SpeedChatLocalizer.SCMenuStinky,
                [SpeedChatLocalizer.SCMenuBattleTaunts, 1507, 1508, 1509],
                {1500: 3},
                {1501: 3},
                {1502: 3},
                {1503: 3},
                1504,
                {1505: 3},
                1506,],
               [SpeedChatLocalizer.SCMenuPlaces,
                [SpeedChatLocalizer.SCMenuPlacesPlayground,
                 1800, 1801, 1802],
                [SpeedChatLocalizer.SCMenuPlacesWait,
                 1700, 1701, 1702, 1703, 1704, 1705, 1706, 1707],
                1600,
                1601,
                1602,
                1603,
                1604,
                1605,
                1606,
                1607],
               [SpeedChatLocalizer.SCMenuMinigames,
                [SpeedChatLocalizer.SCMenuMinigamesGames,
                 1950, 1951, 1952, 1953, 1954, 1955],
                1900, 1901, 1902, 1903, 1904, 1905, 1906, 1907
                ],
               {1: 17},
               {2: 18},
               3]
cfoMenuStructure = [[OTPLocalizer.SCMenuCFOBattleCranes,
                     2100,
                     2101,
                     2102,
                     2103,
                     2104,
                     2105,
                     2106,
                     2107,
                     2108,
                     2109,
                     2110],
                    [OTPLocalizer.SCMenuCFOBattleGoons,
                     2120,
                     2121,
                     2122,
                     2123,
                     2124,
                     2125,
                     2126],
                    2130,
                    2131,
                    2132,
                    2133,
                    1410]
cjMenuStructure = [2200,
                   2201,
                   2202,
                   2203,
                   2204,
                   2205,
                   2206,
                   2207,
                   2208,
                   2209,
                   2210]
ceoMenuStructure = [2300,
                    2301,
                    2302,
                    2303,
                    2304,
                    2305,
                    2306,
                    2307,
                    2312,
                    2313,
                    2314,
                    2315,
                    2308,
                    2309,
                    2310,
                    2311,
                    2316,
                    2317]


class TTChatInputSpeedChat(DirectObject.DirectObject):
    DefaultSCColorScheme = SCColorScheme()

    def __init__(self, chatMgr):
        self.chatMgr = chatMgr
        self.whisperAvatarId = None
        self.toPlayer = 0
        buttons = loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui')
        okButtonImage = (
        buttons.find('**/ChtBx_OKBtn_UP'), buttons.find('**/ChtBx_OKBtn_DN'), buttons.find('**/ChtBx_OKBtn_Rllvr'))
        self.emoteNoAccessPanel = DirectFrame(parent=hidden, relief=None, state='normal',
                                              text=OTPLocalizer.SCEmoteNoAccessMsg, frameSize=(-1, 1, -1, 1),
                                              geom=DGG.getDefaultDialogGeom(), geom_color=OTPGlobals.GlobalDialogColor,
                                              geom_scale=(0.92, 1, 0.6), geom_pos=(0, 0, -.08), text_scale=0.08)
        self.okButton = DirectButton(parent=self.emoteNoAccessPanel, image=okButtonImage, relief=None,
                                     text=OTPLocalizer.SCEmoteNoAccessOK, text_scale=0.05, text_pos=(0.0, -0.1),
                                     textMayChange=0, pos=(0.0, 0.0, -0.2), command=self.handleEmoteNoAccessDone)
        self.insidePartiesMenu = None
        self.createSpeedChat()
        self.whiteList = None
        self.allowWhiteListSpeedChat = base.config.GetBool('white-list-speed-chat', 0)
        if self.allowWhiteListSpeedChat:
            self.addWhiteList()
        self.factoryMenu = None
        self.kartRacingMenu = None
        self.cogMenu = None
        self.cfoMenu = None
        self.cjMenu = None
        self.ceoMenu = None
        self.golfMenu = None
        self.boardingGroupMenu = None
        self.singingGroupMenu = None
        self.aprilToonsMenu = None
        self.victoryPartiesMenu = None
        self.sillyPhaseOneMenu = None
        self.sillyPhaseTwoMenu = None
        self.sillyPhaseThreeMenu = None
        self.sillyPhaseFourMenu = None
        self.sillyPhaseFiveMenu = None
        self.sellbotNerfMenu = None
        self.jellybeanJamMenu = None
        self.halloweenMenu = None
        self.winterMenu = None
        self.sellbotInvasionMenu = None
        self.sellbotFieldOfficeMenu = None
        self.idesOfMarchMenu = None

        def listenForSCEvent(eventBaseName, handler, self=self):
            eventName = self.speedChat.getEventName(eventBaseName)
            self.accept(eventName, handler)

        listenForSCEvent(SpeedChatGlobals.SCTerminalLinkedEmoteEvent, self.handleLinkedEmote)
        listenForSCEvent(SpeedChatGlobals.SCStaticTextMsgEvent, self.handleStaticTextMsg)
        listenForSCEvent(SpeedChatGlobals.SCCustomMsgEvent, self.handleCustomMsg)
        listenForSCEvent(SpeedChatGlobals.SCEmoteMsgEvent, self.handleEmoteMsg)
        listenForSCEvent(SpeedChatGlobals.SCEmoteNoAccessEvent, self.handleEmoteNoAccess)
        listenForSCEvent(TTSpeedChatGlobals.TTSCToontaskMsgEvent, self.handleToontaskMsg)
        listenForSCEvent(TTSpeedChatGlobals.TTSCResistanceMsgEvent, self.handleResistanceMsg)
        listenForSCEvent('SpeedChatStyleChange', self.handleSpeedChatStyleChange)
        listenForSCEvent(TTSCIndexedTerminal.TTSCIndexedMsgEvent, self.handleStaticTextMsg)
        self.fsm = ClassicFSM.ClassicFSM('SpeedChat', [State.State('off', self.enterOff, self.exitOff, ['active']),
                                                       State.State('active', self.enterActive, self.exitActive,
                                                                   ['off'])], 'off', 'off')
        self.fsm.enterInitialState()
        return

    def delete(self):
        self.ignoreAll()
        self.removeWhiteList()
        self.okButton.destroy()
        self.emoteNoAccessPanel.destroy()
        del self.emoteNoAccessPanel
        self.speedChat.destroy()
        del self.speedChat
        del self.fsm
        del self.chatMgr

    def show(self, whisperAvatarId=None, toPlayer=0):
        self.whisperAvatarId = whisperAvatarId
        self.toPlayer = toPlayer
        self.fsm.request('active')

    def hide(self):
        self.fsm.request('off')

    def createSpeedChat(self):
        structure = [
            [SCEmoteMenu, OTPLocalizer.SCMenuEmotions],
            [SCCustomMenu, OTPLocalizer.SCMenuCustom],
            [TTSCResistanceMenu, OTPLocalizer.SCMenuResistance]
        ]
        structure += scStructure
        self.createSpeedChatObject(structure)

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterActive(self):

        def handleCancel(self=self):
            self.chatMgr.fsm.request('mainMenu')

        self.accept('mouse1', handleCancel)

        def selectionMade(self=self):
            self.chatMgr.fsm.request('mainMenu')

        self.terminalSelectedEvent = self.speedChat.getEventName(SpeedChatGlobals.SCTerminalSelectedEvent)
        if base.config.GetBool('want-sc-auto-hide', 1):
            self.accept(self.terminalSelectedEvent, selectionMade)
        self.speedChat.reparentTo(base.a2dpTopLeft, DGG.FOREGROUND_SORT_INDEX)
        scZ = -0.04
        self.speedChat.setPos(0.283, 0, scZ)
        self.speedChat.setWhisperMode(self.whisperAvatarId != None)
        self.speedChat.enter()
        return

    def exitActive(self):
        self.ignore('mouse1')
        self.ignore(self.terminalSelectedEvent)
        self.speedChat.exit()
        self.speedChat.reparentTo(hidden)
        self.emoteNoAccessPanel.reparentTo(hidden)

    def handleLinkedEmote(self, emoteId, displayType=0):
        if self.whisperAvatarId is None and displayType != 2:
            lt = base.localAvatar
            lt.b_setEmoteState(emoteId, animMultiplier=lt.animMultiplier)
        return

    def handleStaticTextMsg(self, textId, displayType=0):
        if self.whisperAvatarId is None:
            self.chatMgr.sendSCChatMessage(textId, displayType)
        else:
            self.chatMgr.sendSCWhisperMessage(textId, self.whisperAvatarId, self.toPlayer)
        self.toPlayer = 0
        return

    def handleCustomMsg(self, textId):
        if self.whisperAvatarId is None:
            self.chatMgr.sendSCCustomChatMessage(textId)
        else:
            self.chatMgr.sendSCCustomWhisperMessage(textId, self.whisperAvatarId, self.toPlayer)
        self.toPlayer = 0
        return

    def handleEmoteMsg(self, emoteId):
        if self.whisperAvatarId is None:
            self.chatMgr.sendSCEmoteChatMessage(emoteId)
        else:
            self.chatMgr.sendSCEmoteWhisperMessage(emoteId, self.whisperAvatarId, self.toPlayer)
        self.toPlayer = 0
        return

    def handleEmoteNoAccess(self):
        if self.whisperAvatarId is None:
            self.emoteNoAccessPanel.setPos(0, 0, 0)
        else:
            self.emoteNoAccessPanel.setPos(0.37, 0, 0)
        self.emoteNoAccessPanel.reparentTo(aspect2d)
        return

    def handleEmoteNoAccessDone(self):
        self.emoteNoAccessPanel.reparentTo(hidden)

    def handleToontaskMsg(self, taskId, toNpcId, toonProgress, msgIndex):
        if self.whisperAvatarId is None:
            self.chatMgr.sendSCToontaskChatMessage(taskId, toNpcId, toonProgress, msgIndex)
        else:
            self.chatMgr.sendSCToontaskWhisperMessage(taskId, toNpcId, toonProgress, msgIndex, self.whisperAvatarId,
                                                      self.toPlayer)
        self.toPlayer = 0
        return

    def handleResistanceMsg(self, textId):
        self.chatMgr.sendSCResistanceChatMessage(textId)

    def handleSpeedChatStyleChange(self):
        nameKey, arrowColor, rolloverColor, frameColor = speedChatStyles[base.localAvatar.getSpeedChatStyleIndex()]
        newSCColorScheme = SCColorScheme(arrowColor=arrowColor, rolloverColor=rolloverColor, frameColor=frameColor)
        self.speedChat.setColorScheme(newSCColorScheme)

    def createSpeedChatObject(self, structure):
        if hasattr(self, 'speedChat'):
            self.speedChat.exit()
            self.speedChat.destroy()
            del self.speedChat
        self.speedChat = SpeedChat(structure=structure, backgroundModelName='phase_3/models/gui/ChatPanel',
                                   guiModelName='phase_3.5/models/gui/speedChatGui')
        self.speedChat.setScale(TTLocalizer.TTCISCspeedChat)
        self.speedChat.setBin('gui-popup', 0)
        self.speedChat.setTopLevelOverlap(TTLocalizer.TTCISCtopLevelOverlap)
        self.speedChat.setColorScheme(self.DefaultSCColorScheme)
        self.speedChat.finalizeAll()

    def addFactoryMenu(self):
        return

    def removeFactoryMenu(self):
        return

    def addKartRacingMenu(self):
        return

    def removeKartRacingMenu(self):
        return

    def addCogMenu(self, indices):
        return

    def removeCogMenu(self):
        return

    def addCFOMenu(self):
        return

    def removeCFOMenu(self):
        return

    def addCJMenu(self, bonusWeight=-1):
        return

    def removeCJMenu(self):
        return

    def addCEOMenu(self):
        return

    def removeCEOMenu(self):
        return

    def addInsidePartiesMenu(self):
        return

    def removeInsidePartiesMenu(self):
        return

    def addGolfMenu(self):
        return

    def removeGolfMenu(self):
        return

    def addBoardingGroupMenu(self, zoneId):
        return

    def removeBoardingGroupMenu(self):
        return

    def addAprilToonsMenu(self):
        return

    def removeAprilToonsMenu(self):
        return

    def addHalloweenMenu(self):
        return

    def removeHalloweenMenu(self):
        return

    def addWinterMenu(self, carol=False):
        return

    def removeWinterMenu(self):
        return

    def addCarolMenu(self):
        self.removeWinterMenu()
        self.addWinterMenu(carol=True)

    def removeCarolMenu(self):
        pass

    def addWhiteList(self):
        return

    def removeWhiteList(self):
        return

    def addSellbotInvasionMenu(self):
        return

    def removeSellbotInvasionMenu(self):
        return
