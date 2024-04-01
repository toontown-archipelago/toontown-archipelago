import functools
from typing import Dict

from panda3d.core import *
from direct.gui.DirectGui import *
from direct.fsm import StateData
from toontown.toon import ToonAvatarPanel
from toontown.friends import ToontownFriendSecret, FriendsGlobals
from toontown.toon.DistributedToon import DistributedToon
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from otp.otpbase import OTPGlobals
FLPNearby = 1
FLPOnline = 2
FLPAll = 3
FLPOnlinePlayers = 4
FLPPlayers = 5
FLPEnemies = 6
globalFriendsList = None

def determineFriendName(friendTuple):
    friendName = None
    if len(friendTuple) == 2:
        avId, flags = friendTuple
        playerId = None
        showType = 0
    elif len(friendTuple) == 3:
        avId, flags, playerId = friendTuple
        showType = 0
    elif len(friendTuple) == 4:
        avId, flags, playerId, showType = friendTuple
    if showType == 1 and playerId:
        playerInfo = base.cr.playerFriendsManager.playerId2Info.get(playerId)
        friendName = playerInfo.playerName
    else:
        hasManager = hasattr(base.cr, 'playerFriendsManager')
        handle = base.cr.identifyFriend(avId)
        if not handle and hasManager:
            handle = base.cr.playerFriendsManager.getAvHandleFromId(avId)
        if handle:
            friendName = handle.getName()

    if avId == base.localAvatar.doId:
        return base.localAvatar.getName()

    return friendName


def compareFriends(f1, f2):
    name1 = determineFriendName(f1)
    name2 = determineFriendName(f2)
    if name1 > name2:
        return 1
    elif name1 == name2:
        return 0
    else:
        return -1


def showFriendsList():
    global globalFriendsList
    if globalFriendsList == None:
        globalFriendsList = FriendsListPanel()
    globalFriendsList.enter()
    return


def hideFriendsList():
    if globalFriendsList != None:
        globalFriendsList.exit()
    return


def showFriendsListTutorial():
    global globalFriendsList
    if globalFriendsList == None:
        globalFriendsList = FriendsListPanel()
    globalFriendsList.enter()
    if not base.cr.isPaid():
        globalFriendsList.secrets['state'] = DGG.DISABLED
    globalFriendsList.closeCommand = globalFriendsList.close['command']
    globalFriendsList.close['command'] = None
    return


def hideFriendsListTutorial():
    if globalFriendsList != None:
        if hasattr(globalFriendsList, 'closeCommand'):
            globalFriendsList.close['command'] = globalFriendsList.closeCommand
        if not base.cr.isPaid():
            globalFriendsList.secrets['state'] = DGG.NORMAL
        globalFriendsList.exit()
    return


def isFriendsListShown():
    if globalFriendsList != None:
        return globalFriendsList.isEntered
    return 0


def unloadFriendsList():
    global globalFriendsList
    if globalFriendsList != None:
        globalFriendsList.unload()
        globalFriendsList = None
    return


class FriendsListPanel(DirectFrame, StateData.StateData):

    # Bound the pages we are allowed to scroll to
    LEFT_MOST_PANEL = FLPNearby
    RIGHT_MOST_PANEL = FLPOnline

    def __init__(self):
        DirectFrame.__init__(self, relief=None)
        self.initialiseoptions(FriendsListPanel)
        StateData.StateData.__init__(self, 'friends-list-done')

        self.listScrollIndex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.playerButtons: Dict[int, DirectButton] = {}  # Maps Toon ID -> DirectButton
        self.currentPanelPage = self.RIGHT_MOST_PANEL

        self.isLoaded = False
        self.isEntered = False

        self.title = None
        self.scrollList = None
        self.close = None
        self.leftButton = None
        self.rightButton = None

    def load(self):

        if self.isLoaded:
            return

        self.isLoaded = True
        gui = loader.loadModel('phase_3.5/models/gui/friendslist_gui')
        auxGui = loader.loadModel('phase_3.5/models/gui/avatar_panel_gui')
        self.title = DirectLabel(parent=self, relief=None, text='', text_scale=TTLocalizer.FLPtitle, text_fg=(0, 0.1, 0.4, 1), pos=(0.007, 0.0, 0.2))
        background_image = gui.find('**/FriendsBox_Open')
        self['image'] = background_image
        self.reparentTo(base.a2dTopRight)
        self.setPos(-0.233, 0, -0.46)
        self.scrollList = DirectScrolledList(parent=self, relief=None, incButton_image=(gui.find('**/FndsLst_ScrollUp'),
         gui.find('**/FndsLst_ScrollDN'),
         gui.find('**/FndsLst_ScrollUp_Rllvr'),
         gui.find('**/FndsLst_ScrollUp')), incButton_relief=None, incButton_pos=(0.0, 0.0, -0.316), incButton_image3_color=Vec4(0.6, 0.6, 0.6, 0.6), incButton_scale=(1.0, 1.0, -1.0), decButton_image=(gui.find('**/FndsLst_ScrollUp'),
         gui.find('**/FndsLst_ScrollDN'),
         gui.find('**/FndsLst_ScrollUp_Rllvr'),
         gui.find('**/FndsLst_ScrollUp')), decButton_relief=None, decButton_pos=(0.0, 0.0, 0.117), decButton_image3_color=Vec4(0.6, 0.6, 0.6, 0.6), itemFrame_pos=(-0.17, 0.0, 0.06), itemFrame_relief=None, numItemsVisible=8, items=[])
        clipper = PlaneNode('clipper')
        clipper.setPlane(Plane(Vec3(-1, 0, 0), Point3(0.2, 0, 0)))
        clipNP = self.scrollList.attachNewNode(clipper)
        self.scrollList.setClipPlane(clipNP)
        self.close = DirectButton(parent=self, relief=None, image=(auxGui.find('**/CloseBtn_UP'), auxGui.find('**/CloseBtn_DN'), auxGui.find('**/CloseBtn_Rllvr')), pos=(0.01, 0, -0.38), command=self.__close)
        self.leftButton = DirectButton(parent=self, relief=None, image=(gui.find('**/Horiz_Arrow_UP'),
                                                                        gui.find('**/Horiz_Arrow_DN'),
                                                                        gui.find('**/Horiz_Arrow_Rllvr'),
                                                                        gui.find('**/Horiz_Arrow_UP')), image3_color=Vec4(0.6, 0.6, 0.6, 0.6), pos=(-0.15, 0.0, -0.38), scale=(-1.0, 1.0, 1.0), command=self.__left)
        self.rightButton = DirectButton(parent=self, relief=None, image=(gui.find('**/Horiz_Arrow_UP'),
                                                                         gui.find('**/Horiz_Arrow_DN'),
                                                                         gui.find('**/Horiz_Arrow_Rllvr'),
                                                                         gui.find('**/Horiz_Arrow_UP')), image3_color=Vec4(0.6, 0.6, 0.6, 0.6), pos=(0.17, 0, -0.38), command=self.__right)
        gui.removeNode()
        auxGui.removeNode()
        return

    def unload(self):

        if self.isLoaded is False:
            return

        self.isLoaded = False
        self.exit()
        del self.title
        del self.scrollList
        del self.close
        del self.leftButton
        del self.rightButton
        del self.playerButtons
        DirectFrame.destroy(self)

    def makeFriendButton(self, toonId, name):
        teamColor = base.cr.archipelagoManager.getToonColorProfile(toonId)
        return DirectButton(
            relief=None,
            text=name,
            text_scale=0.04,
            text_align=TextNode.ALeft,
            text_fg=teamColor.clickable,
            text_shadow=None,
            text1_bg=teamColor.pressed,
            text2_bg=teamColor.hover,
            text3_fg=teamColor.disabled,
            text_font=ToontownGlobals.getToonFont(),
            textMayChange=0,
            command=self.__clickedPlayerButton,
            extraArgs=[toonId]
        )

    def enter(self):

        if self.isEntered:
            return

        self.isEntered = True

        if self.isLoaded is False:
            self.load()

        # Hide the friends list button and the current TAP.
        base.localAvatar.obscureFriendsListButton(1)
        if ToonAvatarPanel.ToonAvatarPanel.currentAvatarPanel:
            ToonAvatarPanel.ToonAvatarPanel.currentAvatarPanel.cleanup()
            ToonAvatarPanel.ToonAvatarPanel.currentAvatarPanel = None

        # Update the entire GUI.
        self.__updateScrollList()
        self.__updateTitle()
        self.__updateArrows()
        self.show()

        # Accept all events that fire when our friends list changes.
        self.accept(FriendsGlobals.FRIENDS_ONLINE_EVENT, self.__friendOnline)
        self.accept(FriendsGlobals.FRIENDS_OFFLINE_EVENT, self.__friendOffline)

    def exit(self):

        if not self.isEntered:
            return

        self.isEntered = False
        self.listScrollIndex[self.currentPanelPage] = self.scrollList.index
        self.hide()
        base.cr.cleanPetsFromFriendsMap()
        self.ignore(FriendsGlobals.FRIENDS_ONLINE_EVENT)
        self.ignore(FriendsGlobals.FRIENDS_OFFLINE_EVENT)
        base.localAvatar.obscureFriendsListButton(-1)
        messenger.send(self.doneEvent)

    def __close(self):
        messenger.send('wakeup')
        self.exit()

    def __left(self):
        messenger.send('wakeup')
        self.listScrollIndex[self.currentPanelPage] = self.scrollList.index
        if self.currentPanelPage > self.LEFT_MOST_PANEL:
            self.currentPanelPage -= 1
        self.__updateScrollList()
        self.__updateTitle()
        self.__updateArrows()

    def __right(self):
        messenger.send('wakeup')
        self.listScrollIndex[self.currentPanelPage] = self.scrollList.index
        if self.currentPanelPage < self.RIGHT_MOST_PANEL:
            self.currentPanelPage += 1
        self.__updateScrollList()
        self.__updateTitle()
        self.__updateArrows()

    def __clickedPlayerButton(self, avId):
        messenger.send('wakeup')
        hasManager = hasattr(base.cr, 'playerFriendsManager')
        handle = None

        # Always always always first try to find this toon if they are in our area.
        if avId in base.cr.doId2do:
            handle = base.cr.doId2do.get(avId)

        # Attempt to extract the handle from our online player manager.
        onlineToon = base.cr.onlinePlayerManager.getOnlineToon(avId)
        if not handle and onlineToon is not None:
            handle = onlineToon.handle()

        # Attempt to get our handle from our disgusting otp code if ours failed.
        if not handle:
            handle = base.cr.identifyFriend(avId)

        if not handle and hasManager:
            handle = base.cr.playerFriendsManager.getAvHandleFromId(avId)

        if handle is None and avId == base.localAvatar.doId:
            handle = base.localAvatar

        # We failed to find a handle.
        if handle is None:
            self.notify.warning(f"Failed to find handle for friend {avId}!")
            return

        self.notify.info("Clicked on name in friend's list. doId = %s" % handle.doId)
        messenger.send('clickedNametag', [handle])

    def __updateScrollList(self):

        toonIdsToRender = []

        # Nearby toons page
        if self.currentPanelPage == FLPNearby:
            toons = list(base.cr.getObjectsOfExactClass(DistributedToon).values())
            toons.append(base.localAvatar)  # Render us too
            for toon in toons:
                toonIdsToRender.append((toon.getDoId(), toon.getName()))

        # Online Competitors page
        if self.currentPanelPage == FLPOnline:
            for onlineToon in base.cr.getOnlineToons():
                toonIdsToRender.append((onlineToon.avId, onlineToon.name))

        # Remove all the current buttons
        self.scrollList.removeAndDestroyAllItems()
        self.playerButtons.clear()

        # Sort the ID's based on teams
        toonIdsToRender = sorted(toonIdsToRender, key=lambda x: (base.cr.archipelagoManager.getToonTeam(x[0]), x[1]))

        # Create the buttons for all the toons.
        for toonInfo in toonIdsToRender:
            friendButton = self.makeFriendButton(toonInfo[0], toonInfo[1])
            self.scrollList.addItem(friendButton, refresh=0)
            self.playerButtons[toonInfo[0]] = friendButton

        # Update the scroll list.
        self.scrollList.index = self.listScrollIndex[self.currentPanelPage]
        self.scrollList.refresh()

    # Trys to determine if we are in "competition" mode.
    # This is True when there exists someone that is considered your enemy currently online.
    def __competitionMode(self) -> bool:

        # We need both these managers to even consider this.
        if None in (base.cr.archipelagoManager, base.cr.onlinePlayerManager):
            return False

        # Check if any of the currently online toons are our enemy.
        us = base.localAvatar.getDoId()
        for toon in base.cr.onlinePlayerManager.getOnlineToons():
            if base.cr.archipelagoManager.onEnemyTeams(us, toon.avId):
                return True

        # Everyone is our friend. Yay :)
        return False

    def __updateTitle(self):

        # If we are on the online toons tab and we are in "competition mode"
        if self.currentPanelPage == FLPOnline and self.__competitionMode():
            self.title['text'] = TTLocalizer.FriendsListPanelOnlineCompetitors
        # If we are on the online toons tab and we are NOT in competition mode
        elif self.currentPanelPage == FLPOnline:
            self.title['text'] = TTLocalizer.FriendsListPanelOnlineFriends
        elif self.currentPanelPage == FLPNearby:
            self.title['text'] = TTLocalizer.FriendsListPanelNearbyToons
        else:
            self.title['text'] = TTLocalizer.FriendsListPanelUndefined

        self.title.resetFrameSize()

    def __updateArrows(self):
        if self.currentPanelPage == self.LEFT_MOST_PANEL:
            self.leftButton['state'] = 'inactive'
        else:
            self.leftButton['state'] = 'normal'
        if self.currentPanelPage == self.RIGHT_MOST_PANEL:
            self.rightButton['state'] = 'inactive'
        else:
            self.rightButton['state'] = 'normal'

    def __friendOnline(self, doId):
        self.__updateScrollList()

    def __friendOffline(self, doId):
        self.__updateScrollList()
