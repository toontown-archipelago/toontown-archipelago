import base64
import json
from typing import Dict, List, Union

from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal

from toontown.friends import FriendsGlobals
from toontown.friends.OnlineToon import OnlineToon


class OnlinePlayerManager(DistributedObjectGlobal):
    notify = DirectNotifyGlobal.directNotify.newCategory('OnlinePlayerManager')

    def __init__(self, cr):
        super().__init__(cr)

        # Start AP Code
        # Keep a cache of currently online toons so clients can request/receive this.
        # Maps Toon IDs to OnlineToon struct.
        self._onlineToonCache: Dict[int, OnlineToon] = {}

    """
    Internal util used within this class.
    """

    # Call to cache a toon that just came online.
    def __cacheOnlineToon(self, toonInfo: OnlineToon):
        self._onlineToonCache[toonInfo.avId] = toonInfo

    # Call to un-cache a toon that just went offline.
    def __decacheOfflineToon(self, toonId: int):
        if toonId in self._onlineToonCache:
            del self._onlineToonCache[toonId]

    """
    Util to be used throughout the codebase.
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

        # Sometimes we may call this method when we do not have all our required attributes.
        # This can be from pre toon generation since we need to intercept name/dna change events.
        if None in (toon.doId, toon.name, toon.style):
            return False

        # If we don't want to overwrite data in our cache and the toon is already cached don't do anything
        if not overwrite and toon.getDoId() in self._onlineToonCache:
            return False

        # New data!
        self.__cacheOnlineToon(OnlineToon(toon.getDoId(), toon.getName(), toon.style.makeNetString()))
        return True

    """
    Astron updates received via the UD view of this object.
    """

    # Called when a toon just came online.
    def toonCameOnline(self, onlineToonData):
        onlineToon: OnlineToon = OnlineToon.from_struct(onlineToonData)
        self.__cacheOnlineToon(onlineToon)

        # The client repository may want to do some extra functionality. Tell it a toon went online.
        self.cr.onToonCameOnline(onlineToon)

        # Now fire an event if anywhere else in the code would like to implement some functionality.
        messenger.send(FriendsGlobals.FRIENDS_ONLINE_EVENT, [onlineToon.avId])

    # Called when a toon just went offline
    def toonWentOffline(self, avId):
        oldToon: OnlineToon = self.getOnlineToon(avId)
        self.__decacheOfflineToon(avId)

        # The client repository may want to do some extra functionality. Tell it a toon went offline.
        if oldToon is not None:
            self.cr.onToonWentOffline(oldToon)
            # Now fire an event if anywhere else in the code would like to implement some functionality.
            messenger.send(FriendsGlobals.FRIENDS_OFFLINE_EVENT, [oldToon.avId])

    # Called when we need to completely re-sync all online toons from the UD.
    def setOnlineToons(self, listOfToonData):
        self._onlineToonCache.clear()
        for toonData in listOfToonData:
            toon: OnlineToon = OnlineToon.from_struct(toonData)
            self.__cacheOnlineToon(toon)

    def avatarDetailsResp(self, avId, details):
        fields = json.loads(details)
        newName = 'Unknown Toon'
        newDna = None

        # The following fields were converted to a string to satisfy json.dumps() from UD and need conversion
        BYTE_FIELDS = ('setDNAString', 'setInventory')

        for currentField in fields:
            fieldName: str = currentField[0]

            # If we have an encoded byte field, go back to what it was
            if fieldName in BYTE_FIELDS:
                currentField[1] = base64.b64decode(currentField[1])

            value = currentField[1]


            # See if we found our name or DNA to update
            if fieldName == 'setName':
                newName = value
            if fieldName == 'setDNAString':
                newDna = value

        # We also received an up to date dump of this avatar's information that we are caching. Overwrite it.
        if newName is not None and newDna is not None:
            onlineToon = OnlineToon(avId, newName, newDna)
            self.__cacheOnlineToon(onlineToon)

        # Tell the client repository we received this information
        base.cr.handleGetAvatarDetailsResp(avId, fields=fields)

    """
    Astron updates to be send to the UD view of this object.
    """

    def d_getAvatarDetails(self, avId):
        self.sendUpdate('getAvatarDetails', [avId])
