import json

from typing import Dict, List

from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.distributed.PyDatagram import PyDatagram
from direct.fsm.FSM import FSM


from toontown.friends.OnlineToon import OnlineToon

# Do not delete this import even though it says it is unused!!!
# It defines some globals that we need to work.
from direct.distributed.MsgTypes import *

import base64


# Base class used for starting and managing operations that need to query the database.
class FriendManagerOperation(FSM):

    def start(self):
        raise NotImplementedError("Please implement the start() method!")


class GetAvatarInfoOperation(FriendManagerOperation):

    # A list of supported dclasses we are allowed to query.
    SUPPORTED_DCLASSES = (
        'DistributedToonUD',
        # 'DistributedPetAI',
    )

    def __init__(self, mgr, senderId, avId, callback):
        FSM.__init__(self, 'GetAvatarInfoOperation')
        self.mgr = mgr
        self.senderId = senderId
        self.avId = avId
        self.callback = callback

    def __getSupportedDClasses(self):
        return (self.mgr.air.dclassesByName[dclass] for dclass in self.SUPPORTED_DCLASSES)

    def start(self):
        self.demand('GetAvatarInfo')

    def enterGetAvatarInfo(self):
        self.mgr.air.dbInterface.queryObject(self.mgr.air.dbId, self.avId, self.__gotAvatarInfo)

    def __gotAvatarInfo(self, dclass, fields):
        if dclass not in self.__getSupportedDClasses():
            self.demand('Failure', 'Invalid dclass for avId %d' % self.avId)
            return

        self.fields = fields
        self.fields['avId'] = self.avId
        self.demand('Finished')

    def enterFinished(self):
        self.callback(success=True, avId=self.senderId, fields=self.fields)

    def enterFailure(self, reason):
        self.mgr.notify.warning(reason)
        self.callback(success=False, avId=None, fields=None)


class OnlinePlayerManagerUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('OnlinePlayerManagerUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)

        # Stores a map of avIds to current operations in progress.
        self.operations: Dict[int, FriendManagerOperation] = {}

        # Keep a cache of currently online toons so clients can request/receive this.
        # Maps Toon IDs to OnlineToon struct.
        self._onlineToonCache: Dict[int, OnlineToon] = {}

    """
    Internal util to make management easier.
    """

    # Call to cache a toon that just came online.
    def __cacheOnlineToon(self, toonInfo: OnlineToon):
        self._onlineToonCache[toonInfo.avId] = toonInfo

    # Call to un-cache a toon that just went offline.
    def __decacheOfflineToon(self, toonId: int):
        if toonId in self._onlineToonCache:
            del self._onlineToonCache[toonId]

    def __gotAvatarDetails(self, success, avId, fields):
        self.cancelOperation(avId)
        if not success:
            return

        details = [
            ['setName', fields['setName'][0]],
            ['setExperience', fields['setExperience'][0]],
            ['setTrackAccess', fields['setTrackAccess'][0]],
            ['setTrackBonusLevel', fields['setTrackBonusLevel'][0]],
            ['setInventory', base64.b64encode(fields['setInventory'][0]).decode(encoding='ascii')],
            ['setHp', fields['setHp'][0]],
            ['setMaxHp', fields['setMaxHp'][0]],
            ['setDefaultShard', fields['setDefaultShard'][0]],
            ['setLastHood', fields['setLastHood'][0]],
            ['setDNAString', base64.b64encode(fields['setDNAString'][0]).decode(encoding='ascii')],
            ['setHat', fields['setHat'][0], fields['setHat'][1], fields['setHat'][2]],
            ['setGlasses', fields['setGlasses'][0], fields['setGlasses'][1], fields['setGlasses'][2]],
            ['setBackpack', fields['setBackpack'][0], fields['setBackpack'][1], fields['setBackpack'][2]],
            ['setShoes', fields['setShoes'][0], fields['setShoes'][1], fields['setShoes'][2]],
            ['setHatList', fields['setHatList'][0]],
            ['setGlassesList', fields['setGlassesList'][0]],
            ['setBackpackList', fields['setBackpackList'][0]],
            ['setShoesList', fields['setShoesList'][0]],
            ['setCustomMessages', fields['setCustomMessages'][0]],
            ['setEmoteAccess', fields['setEmoteAccess'][0]],
            ['setClothesTopsList', fields['setClothesTopsList'][0]],
            ['setClothesBottomsList', fields['setClothesBottomsList'][0]],
            ['setPetTrickPhrases', fields['setPetTrickPhrases'][0]]
        ]

        self.d_avatarDetailsResp(avId, fields['avId'], json.dumps(details))

        # Since we queried avatar data, we might as well update the cache if we have some data present.
        # This is for the event that someone changed their name or DNA we can have something more up to date.
        # We should also only do this if the toon is online.
        queriedAvId = fields['avId']

        if queriedAvId not in self._onlineToonCache:
            return

        queriedName = fields['setName'][0]
        queriedDNA = fields['setDNAString'][0]
        self.__cacheOnlineToon(OnlineToon(queriedAvId, queriedName, queriedDNA))

    # Given two avIds, make them both aware of each other's existence.
    # This is used so that on initial login, they can immediately start communicating with each other
    # via astron updates.
    # If we don't do this, the CLIENTAGENT will boot someone for attempting to call an update on an object they
    # haven't "seen" yet.
    def __declareAvatarExistence(self, avId, otherAvId):

        # Declare our avatar to their friend.
        dg = PyDatagram()
        dg.addServerHeader(self.GetPuppetConnectionChannel(avId), self.air.ourChannel, CLIENTAGENT_DECLARE_OBJECT)
        dg.addUint32(otherAvId)
        dg.addUint16(self.air.dclassesByName['DistributedToonUD'].getNumber())
        self.air.send(dg)

        # Declare their friend to our avatar.
        dg = PyDatagram()
        dg.addServerHeader(self.GetPuppetConnectionChannel(otherAvId), self.air.ourChannel, CLIENTAGENT_DECLARE_OBJECT)
        dg.addUint32(avId)
        dg.addUint16(self.air.dclassesByName['DistributedToonUD'].getNumber())
        self.air.send(dg)

    # Similarly to declaring existence above, we also need to do the opposite when a toon logs out.
    def __undeclareAvatarExistence(self, avId, otherAvId, accountId):
        # Undeclare to the friend.
        dg = PyDatagram()
        dg.addServerHeader(self.GetPuppetConnectionChannel(avId), self.air.ourChannel, CLIENTAGENT_UNDECLARE_OBJECT)
        dg.addUint32(otherAvId)
        self.air.send(dg)

        # Undeclare to the now-offline avId.
        dg = PyDatagram()
        dg.addServerHeader(self.GetAccountConnectionChannel(accountId), self.air.ourChannel, CLIENTAGENT_UNDECLARE_OBJECT)
        dg.addUint32(avId)
        self.air.send(dg)

    """
    Util to be used throughout the codebase (mainly GameServicesManagerUD).
    """

    # Called from GameServicesManagerUD to inform us that a toon has just come online.
    def comingOnline(self, avId, name, dnaString: bytes):

        # START AP CODE
        # Cache online toon then send an update to the client DOG
        onlineToon = OnlineToon(avId, name, dnaString)

        # For every toon that is currently online, they need to be aware of the new toon.
        # Our toon also needs to be aware of them.
        for otherAvId in self._onlineToonCache.keys():
            self.d_toonCameOnline(otherAvId, onlineToon)
            self.__declareAvatarExistence(avId, otherAvId)

        self.__cacheOnlineToon(onlineToon)
        # We also need to send the person who came online a current list of everyone else online.
        self.d_setOnlineToons(avId)

    # Called from GameServicesManagerUD to inform us that a toon has just went offline.
    def goingOffline(self, avId, accountId):

        # START AP CODE
        # Uncache the avatar and tell all other toons this toon went offline.
        self.__decacheOfflineToon(avId)

        # Tell the other toons this toon went offline, also undeclare the existence for everyone.
        for otherAvId in self._onlineToonCache.keys():
            self.d_toonWentOffline(otherAvId, avId)
            self.__undeclareAvatarExistence(avId, otherAvId, accountId)

    # Call to cancel and stop tracking of a specific operation in progress.
    def cancelOperation(self, avId):
        operation = self.operations.get(avId)
        if not operation:
            self.notify.debug('%s tried to delete non-existent operation!' % avId)
            return

        if operation.state != 'Off':
            operation.demand('Off')

        del self.operations[avId]

    # Deprecated.
    # Originally used to clear friend list data but it is mingled a bit more in the codebase than I had hoped :3
    # Will be removed at some point.
    def clearList(self, avId):
        pass
    """
    Astron updates received from clients.
    """

    # Called when a client is requesting avatar details of some avId.
    def getAvatarDetails(self, avId):
        senderId = self.air.getAvatarIdFromSender()
        if not senderId:
            return

        if senderId in self.operations:
            return

        newOperation = GetAvatarInfoOperation(self, senderId, avId, self.__gotAvatarDetails)
        newOperation.start()
        self.operations[senderId] = newOperation

    """
    Methods that invoke astron updates to clients.
    """

    # Call to tell the clients that a toon came online and provide the info of said toon.
    def d_toonCameOnline(self, targetAvId: int, toon: OnlineToon):
        self.sendUpdateToAvatarId(targetAvId, 'toonCameOnline', [toon.struct()])

    # Call to tell the clients that some toon went offline and provide the avId of said toon.
    def d_toonWentOffline(self, targetAvId: int, offlineAvId: int):
        self.sendUpdateToAvatarId(targetAvId, 'toonWentOffline', [offlineAvId])

    # Call to tell a specific client all the toons we have stored on our cache of online toons.
    # Used for initial login to sync data for them.
    def d_setOnlineToons(self, avId: int):
        onlineToons: List[OnlineToon] = [toon for toon in self._onlineToonCache.values()]
        onlineToonsStructs: List[List] = [toon.struct() for toon in onlineToons]
        self.sendUpdateToAvatarId(avId, 'setOnlineToons', [onlineToonsStructs])

    # Call to tell a specific client some detailed info of some avId.
    # requesterAvId - The avId who requested the information.
    # requestingOfAvId - The avId's information that was requested.
    # jsonStr - A string representing a json dump of the detailed information to send to the client.
    def d_avatarDetailsResp(self, requesterAvId: int, requestingOfAvId: int, data: str):
        self.sendUpdateToAvatarId(requesterAvId, 'avatarDetailsResp', [requestingOfAvId, data])
