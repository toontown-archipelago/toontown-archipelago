from otp.ai.AIBaseGlobal import *
from panda3d.core import *
from .DistributedNPCToonBaseAI import *
from toontown.toonbase import TTLocalizer
from direct.task import Task
from toontown.fishing import FishGlobals
from toontown.pets import PetUtil, PetDNA, PetConstants
from apworld.toontown.options import RewardDisplayOption
from toontown.archipelago.definitions import util
from toontown.archipelago.packets.serverbound.location_scouts_packet import LocationScoutsPacket
from toontown.hood import ZoneUtil
import random

class DistributedNPCPetclerkAI(DistributedNPCToonBaseAI):

    def __init__(self, air, npcId, subId=1):
        DistributedNPCToonBaseAI.__init__(self, air, npcId)
        self.subId = subId
        self.givesQuests = 0

    def delete(self):
        self.ignoreAll()
        DistributedNPCToonBaseAI.delete(self)

    def avatarEnter(self):
        avId = self.air.getAvatarIdFromSender()
        if avId not in self.air.doId2do:
            self.notify.warning('Avatar: %s not found' % avId)
            return
        self.d_setSubId()
        self.petSeeds = simbase.air.petMgr.getAvailablePets(3, 2)
        numGenders = len(PetDNA.PetGenders)
        self.petSeeds *= numGenders
        self.petSeeds.sort()
        self.sendUpdateToAvatarId(avId, 'setPetSeeds', [self.petSeeds])
        self.transactionType = ''
        av = self.air.doId2do[avId]
        self.acceptOnce(self.air.getAvatarExitEvent(avId), self.__handleUnexpectedExit, extraArgs=[avId])
        flag = NPCToons.SELL_MOVIE_START
        self.d_setMovie(avId, flag)
        # taskMgr.doMethodLater(PetConstants.PETCLERK_TIMER, self.sendTimeoutMovie, self.uniqueName('clearMovie'))
        #is auto hint turned on?
        if av.slotData.get("pet_shop_display", RewardDisplayOption.default) == RewardDisplayOption.option_auto_hint:
            packet = LocationScoutsPacket()
            packet.create_as_hint = 2 # only announce new hints
            packet.locations = [util.ap_location_name_to_id(self.getCheckName())]
            av.archipelago_session.client.send_packet(packet)
        DistributedNPCToonBaseAI.avatarEnter(self)

    def rejectAvatar(self, avId):
        self.notify.warning('rejectAvatar: should not be called by a fisherman!')

    def d_setMovie(self, avId, flag, extraArgs = []):
        self.sendUpdate('setMovie', [flag,
         self.npcId,
         avId,
         extraArgs,
         ClockDelta.globalClockDelta.getRealNetworkTime()])

    def d_setSubId(self):
        self.sendUpdate('setSubId', [self.subId])

    def sendTimeoutMovie(self, task, avId=0):
        self.d_setMovie(avId, NPCToons.SELL_MOVIE_TIMEOUT)
        self.sendClearMovie(avId, None)
        return Task.done

    def sendClearMovie(self, avId=0, task=None):
        self.ignore(self.air.getAvatarExitEvent(avId))
        self.d_setMovie(avId, NPCToons.SELL_MOVIE_CLEAR)
        return Task.done

    def fishSold(self):
        avId = self.air.getAvatarIdFromSender()
        av = simbase.air.doId2do.get(avId)
        if av:
            trophyResult = self.air.fishManager.creditFishTank(av)
            if trophyResult:
                movieType = NPCToons.SELL_MOVIE_TROPHY
                extraArgs = [len(av.fishCollection), FishGlobals.getTotalNumFish()]
            else:
                movieType = NPCToons.SELL_MOVIE_COMPLETE
                extraArgs = []
            self.d_setMovie(avId, movieType, extraArgs)
            self.transactionType = 'fish'
        self.sendClearMovie(avId)
        return

    def petAdopted(self, petNum, nameIndex):
        avId = self.air.getAvatarIdFromSender()
        av = simbase.air.doId2do.get(avId)
        if av:
            zoneId = ZoneUtil.getCanonicalSafeZoneId(self.zoneId)
            if petNum not in range(0, len(self.petSeeds)):
                self.air.writeServerEvent('suspicious', avId, 'DistributedNPCPetshopAI.petAdopted and no such pet!')
                self.notify.warning('somebody called petAdopted on a non-existent pet! avId: %s' % avId)
                return
            baseCost = ToontownGlobals.ZONE_TO_CHECK_COST[zoneId]
            if av.slotData.get('random_prices', False):
                rng = random.Random()
                rng.seed(f"{av.getSeed()}-{self.subId}")
                # This price will be consistent based on our archi rng setting
                cost = rng.randint((baseCost - 500), (baseCost + 1000))
            else:
                cost = baseCost
            if cost > av.getMoney():
                self.air.writeServerEvent('suspicious', avId, "DistributedNPCPetshopAI.petAdopted and toon doesn't have enough money!")
                self.notify.warning("somebody called petAdopted and didn't have enough money to adopt! avId: %s" % avId)
                return
            if av.petId != 0:
                simbase.air.petMgr.deleteToonsPet(avId)
            gender = petNum % len(PetDNA.PetGenders)
            if nameIndex not in range(0, TTLocalizer.PetNameIndexMAX):
                self.air.writeServerEvent('avoid_crash', avId, "DistributedNPCPetclerkAI.petAdopted and didn't have valid nameIndex!")
                self.notify.warning("somebody called petAdopted and didn't have valid nameIndex to adopt! avId: %s" % avId)
                return
            if not av.hasCheckedLocation(util.ap_location_name_to_id(self.getCheckName())):
                av.addCheckedLocation(util.ap_location_name_to_id(self.getCheckName()))
                self.transactionType = 'adopt'
            else:
                self.transactionType = 'checked'
                return
            av.takeMoney(cost)

    def getCheckName(self):
        zoneId = ZoneUtil.getCanonicalSafeZoneId(self.zoneId)
        return ToontownGlobals.ZONE_TO_ID_TO_CHECK[zoneId][self.subId]

    def petReturned(self):
        avId = self.air.getAvatarIdFromSender()
        av = simbase.air.doId2do.get(avId)
        if av:
            simbase.air.petMgr.deleteToonsPet(avId)
            self.transactionType = 'return'

    def transactionDone(self):
        avId = self.air.getAvatarIdFromSender()
        av = simbase.air.doId2do.get(avId)
        if av:
            if self.transactionType == 'adopt':
                self.d_setMovie(avId, NPCToons.SELL_MOVIE_PETADOPTED)
            elif self.transactionType == 'return':
                self.d_setMovie(avId, NPCToons.SELL_MOVIE_PETRETURNED)
            elif self.transactionType == '':
                self.d_setMovie(avId, NPCToons.SELL_MOVIE_PETCANCELED)
            elif self.transactionType == 'checked':
                self.d_setMovie(avId, NPCToons.SELL_MOVIE_ALREADYCHECKED)
        self.sendClearMovie(avId)
        return

    def __handleUnexpectedExit(self, avId):
        self.notify.warning('avatar:' + str(avId) + ' has exited unexpectedly')
        self.sendClearMovie(avId)
        return
