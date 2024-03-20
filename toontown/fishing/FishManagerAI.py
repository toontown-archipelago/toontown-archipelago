import random
from typing import Dict

from direct.directnotify import DirectNotifyGlobal

from apworld.toontown import locations
from apworld.toontown.fish import can_catch_new_species

from toontown.archipelago.definitions.util import ap_location_name_to_id
from toontown.fishing import FishGlobals
from toontown.fishing.DistributedFishingPondAI import DistributedFishingPondAI
from toontown.fishing.FishBase import FishBase
from toontown.safezone.DistributedFishingSpotAI import DistributedFishingSpotAI


# How much pity to add per rod (.01) = 1%
FISHING_ROD_PITY = (0.02, 0.05, 0.10, 0.15, 0.25)


class FishManagerAI:
    notify = DirectNotifyGlobal.directNotify.newCategory('FishManagerAI')

    def __init__(self, air):
        self.air = air
        self.requestedFish = {}

        # For every roll a toon does give them some pity, pity starts at 0 and increases slightly and is checked against
        # a random.random() call
        self.newSpeciesPity: Dict[int, float] = {}

    def generatePond(self, area, zoneId):
        # Generate our fishing pond.
        fishingPond = DistributedFishingPondAI(self.air)
        fishingPond.setArea(area)
        fishingPond.generateWithRequired(zoneId)
        fishingPond.generateTargets()
        return fishingPond

    def generateSpots(self, dnaData, fishingPond):
        # Generate our fishing spots.
        zoneId = fishingPond.zoneId
        doId = fishingPond.doId
        fishingSpot = DistributedFishingSpotAI(self.air)
        fishingSpot.setPondDoId(doId)
        x, y, z = dnaData.getPos()
        h, p, r = dnaData.getHpr()
        fishingSpot.setPosHpr(x, y, z, h, p, r)
        fishingSpot.generateWithRequired(zoneId)
        return fishingSpot

    def attemptForceNewSpecies(self, av, zoneId):

        # How many times should we try to get a new catch
        ATTEMPTS = 1000
        fish = None

        # Simulate some amount of casts in the current pond to prioritize the fish here first
        for _ in range(ATTEMPTS):
            success, genus, species, weight = FishGlobals.getRandomFishVitals(zoneId, av.getFishingRod())
            fish = FishBase(genus, species, weight)
            result = av.fishCollection.getCollectResult(fish)  # Simulate us catching the fish but don't actually

            # If this would be a new entry return it and reset pity
            if result == FishGlobals.COLLECT_NEW_ENTRY:
                self.newSpeciesPity[av.doId] = 0
                return fish

        # We failed to find a fish in their current pond, let's try just finding a random species
        all_fish = FishGlobals.getAllFish()
        random.shuffle(all_fish)

        for fish_data in all_fish:
            genus, species = fish_data
            weight = FishGlobals.getRandomWeight(genus, species, rodIndex=av.getFishingRod())
            fish = FishBase(genus, species, weight)

            # Simulate a catch, is this new?
            result = av.fishCollection.getCollectResult(fish)

            # If this would be a new entry return it and reset pity
            if result == FishGlobals.COLLECT_NEW_ENTRY:
                self.newSpeciesPity[av.doId] = 0
                return fish

        # We failed to find a fish in x rolls, just return the last one we got
        assert fish is not None
        return fish

    def attemptBlockNewSpecies(self, original_fish, av, zoneId):
        # How many times should we try to block a new species
        ATTEMPTS = 1000

        # Simulate some amount of casts in the current pond to prioritize the fish here first
        for _ in range(ATTEMPTS):
            success, genus, species, weight = FishGlobals.getRandomFishVitals(zoneId, av.getFishingRod())
            fish = FishBase(genus, species, weight)
            result = av.fishCollection.getCollectResult(fish)  # Simulate us catching the fish but don't actually

            # Return this fish if it's not a new species
            if result != FishGlobals.COLLECT_NEW_ENTRY:
                return fish

        # Check across all fish we've caught (prevent zone cheese at all costs!)
        all_fish = FishGlobals.getAllFish()
        random.shuffle(all_fish)

        for fish_data in all_fish:
            genus, species = fish_data
            weight = FishGlobals.getRandomWeight(genus, species, rodIndex=av.getFishingRod())
            fish = FishBase(genus, species, weight)

            # Simulate a catch, is this new?
            result = av.fishCollection.getCollectResult(fish)

            # Return this fish if it's not a new species
            if result != FishGlobals.COLLECT_NEW_ENTRY:
                return fish

        # We failed reddit
        return original_fish

    def shouldForceNewSpecies(self, av):

        # Maxed toons don't need this
        if len(av.fishCollection) >= 70:
            return False

        rng = random.random()
        threshold = self.newSpeciesPity.get(av.doId, 0)
        return rng < threshold

    def shouldForceBlockNewSpecies(self, av):
        return not can_catch_new_species(len(av.fishCollection), av.fishingRod)

    def addNewSpeciesPity(self, av):

        rod = av.getFishingRod()  # Value from 0-4 representing how good our fishing rod is
        # clamp to length of pity
        rod = min(len(FISHING_ROD_PITY), rod)
        rod = max(0, rod)
        pity = FISHING_ROD_PITY[rod]

        # Add the pity
        oldPity = self.newSpeciesPity.get(av.doId, 0)
        self.newSpeciesPity[av.doId] = oldPity + pity

    def getAvPity(self, av) -> float:
        return self.newSpeciesPity.get(av.doId, 0)

    def generateCatch(self, av, zoneId):
        # Generate our catch.
        if len(av.fishTank) >= av.getMaxFishTank():
            return [FishGlobals.OverTankLimit, 0, 0, 0]

        caughtItem = self.air.questManager.toonFished(av, zoneId)
        if caughtItem:
            return [FishGlobals.QuestItem, caughtItem, 0, 0]

        itemType = FishGlobals.FishItem
        rand = random.random() * 100.0
        for cutoff in FishGlobals.SortedProbabilityCutoffs:
            if rand <= cutoff:
                itemType = FishGlobals.ProbabilityDict[cutoff]
                break

        # For now in this game, we are always going to force fish. If you want vanilla fishing behavior delete this line
        itemType = FishGlobals.FishItem

        # Process if this av used commands to cheat a fish
        if av.doId in self.requestedFish:
            genus, species = self.requestedFish[av.doId]
            weight = FishGlobals.getRandomWeight(genus, species)
            fish = FishBase(genus, species, weight)
            fishType = av.fishCollection.collectFish(fish)
            if fishType == FishGlobals.COLLECT_NEW_ENTRY:
                itemType = FishGlobals.FishItemNewEntry
            elif fishType == FishGlobals.COLLECT_NEW_RECORD:
                itemType = FishGlobals.FishItemNewRecord
            else:
                itemType = FishGlobals.FishItem

            collectionNetList = av.fishCollection.getNetLists()
            av.d_setFishCollection(collectionNetList[0], collectionNetList[1], collectionNetList[2])
            av.fishTank.addFish(fish)
            tankNetList = av.fishTank.getNetLists()
            av.d_setFishTank(tankNetList[0], tankNetList[1], tankNetList[2])
            del self.requestedFish[av.doId]
            return [itemType, genus, species, weight]

        # Process the item we rolled
        if itemType == FishGlobals.FishItem:
            success, genus, species, weight = FishGlobals.getRandomFishVitals(zoneId, av.getFishingRod())
            fish = FishBase(genus, species, weight)

            # Route species logic for pity/blocking
            if self.shouldForceBlockNewSpecies(av):
                fish = self.attemptBlockNewSpecies(fish, av, zoneId)
            elif self.shouldForceNewSpecies(av):
                fish = self.attemptForceNewSpecies(av, zoneId)

            # Catch the fish
            fishType = av.fishCollection.collectFish(fish)

            self.addNewSpeciesPity(av)

            # If we have a new species, reset pity
            if fishType == FishGlobals.COLLECT_NEW_ENTRY:
                itemType = FishGlobals.FishItemNewEntry
                self.newSpeciesPity[av.doId] = 0
            elif fishType == FishGlobals.COLLECT_NEW_RECORD:
                itemType = FishGlobals.FishItemNewRecord
            else:
                itemType = FishGlobals.FishItem

            collectionNetList = av.fishCollection.getNetLists()
            av.d_setFishCollection(collectionNetList[0], collectionNetList[1], collectionNetList[2])
            av.fishTank.addFish(fish)
            tankNetList = av.fishTank.getNetLists()
            av.d_setFishTank(tankNetList[0], tankNetList[1], tankNetList[2])
            return [itemType, fish.getGenus(), fish.getSpecies(), fish.getWeight()]
        elif itemType == FishGlobals.BootItem:
            return [itemType, 0, 0, 0]
        else:
            money = FishGlobals.Rod2JellybeanDict[av.getFishingRod()]
            av.addMoney(money)
            return [itemType, money, 0, 0]

    def creditFishTank(self, av):
        totalFish = len(av.fishCollection)
        trophies = int(totalFish / 10)
        curTrophies = len(av.fishingTrophies)
        av.addMoney(av.fishTank.getTotalValue())
        av.b_setFishTank([], [], [])
        self.checkForFishingLocationCompletions(av)

        if trophies > curTrophies:
            # av.b_setMaxHp(av.getMaxHp() + trophies - curTrophies)
            # av.toonUp(av.getMaxHp())
            av.b_setFishingTrophies(list(range(trophies)))
            return True

        return False

    def checkForFishingLocationCompletions(self, av):

        thresholdToLocation = {
            10: locations.ToontownLocationName.FISHING_10_SPECIES.value,
            20: locations.ToontownLocationName.FISHING_20_SPECIES.value,
            30: locations.ToontownLocationName.FISHING_30_SPECIES.value,
            40: locations.ToontownLocationName.FISHING_40_SPECIES.value,
            50: locations.ToontownLocationName.FISHING_50_SPECIES.value,
            60: locations.ToontownLocationName.FISHING_60_SPECIES.value,
            70: locations.ToontownLocationName.FISHING_COMPLETE_ALBUM.value,
        }

        numFish = len(av.fishCollection)
        for threshold, check in thresholdToLocation.items():
            if numFish < threshold:
                continue

            check_id = ap_location_name_to_id(check)
            av.addCheckedLocation(check_id)
