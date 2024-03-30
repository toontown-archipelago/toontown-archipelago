import json
from typing import Dict, List, Union

from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal

from toontown.friends.OnlineToon import OnlineToon


class TTOffFriendsManager(DistributedObjectGlobal):
    notify = DirectNotifyGlobal.directNotify.newCategory('TTOffFriendsManager')

    def __init__(self, cr):
        super().__init__(cr)

        # Start AP Code
        # Keep a cache of currently online toons so clients can request/receive this.
        # Maps Toon IDs to OnlineToon struct.
        self._onlineToonCache: Dict[int, OnlineToon] = {}

    # Call to cache a toon that just came online.
    def __cacheOnlineToon(self, toonInfo: OnlineToon):
        self._onlineToonCache[toonInfo.avId] = toonInfo

    # Call to un-cache a toon that just went offline.
    def __decacheOfflineToon(self, toonId: int):
        if toonId in self._onlineToonCache:
            del self._onlineToonCache[toonId]

    def d_getAvatarDetails(self, avId):
        self.sendUpdate('getAvatarDetails', [avId])

    def avatarDetailsResp(self, avId, details):
        fields = json.loads(details)
        for currentField in fields:
            if currentField[0] in (
                    'setDNAString', 'setMailboxContents', 'setAwardMailboxContents', 'setGiftSchedule',
                    'setDeliverySchedule', 'setAwardSchedule', 'setInventory'):
                currentField[1] = bytes(currentField[1], 'utf-8')

        base.cr.handleGetAvatarDetailsResp(avId, fields=fields)

    def d_getFriendsListRequest(self):
        self.sendUpdate('getFriendsListRequest')

    def friendsListRequestResp(self, resp):
        base.cr.handleGetFriendsList(resp)

    def friendOnline(self, id, commonChatFlags, whitelistChatFlags, alert=True):
        base.cr.handleFriendOnline(id, commonChatFlags, whitelistChatFlags, alert)

    def d_removeFriend(self, friendId):
        self.sendUpdate('removeFriend', [friendId])

    def friendOffline(self, id):
        base.cr.handleFriendOffline(id)

    """
    Helper methods to be used in game code to interact with this class
    """

    # Gets a list of OnlineToon instances representing the toons that are currently online.
    def getOnlineToons(self) -> List[OnlineToon]:
        return list(self._onlineToonCache.values())

    # Returns an OnlineToon instance if toon with toon ID is online. None if they are not.
    def getOnlineToon(self, toonId) -> Union[OnlineToon, None]:
        return self._onlineToonCache.get(toonId, None)

    # Given a DistributedToon instance, cache this toon's data. This is used in the rare instance that
    # UberDOG fails while we are online allowing us to still have access to our "friends list" when
    # UberDOG comes back to life.
    # Returns False if toon was already cached and we didn't do anything. True if we updated the cache.
    def cacheOnlineToon(self, toon, overwrite=False) -> bool:

        # If we don't want to overwrite data in our cache and the toon is already cached don't do anything
        if not overwrite and toon.getDoId() in self._onlineToonCache:
            return False

        # New data!
        self.__cacheOnlineToon(OnlineToon(toon.getDoId(), toon.getName()))
        return True

    """
    Astron updates received via UD view of this object
    """

    # Called when a toon just came online.
    def toonCameOnline(self, onlineToonData):
        onlineToon: OnlineToon = OnlineToon.from_struct(onlineToonData)
        self.__cacheOnlineToon(onlineToon)

    # Called when a toon just went offline
    def toonWentOffline(self, avId):
        self.__decacheOfflineToon(avId)

    # Called when we need to completely re-sync all online toons from the UD.
    def setOnlineToons(self, listOfToonData):
        self._onlineToonCache.clear()
        for toonData in listOfToonData:
            toon: OnlineToon = OnlineToon.from_struct(toonData)
            self.__cacheOnlineToon(toon)
