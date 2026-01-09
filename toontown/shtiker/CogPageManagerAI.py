from apworld.toontown import locations
from direct.directnotify import DirectNotifyGlobal

from toontown.archipelago.definitions.util import cog_code_to_ap_location, ap_location_name_to_id
from toontown.shtiker.CogPageGlobals import *
from toontown.suit import SuitDNA


class CogPageManagerAI:
    notify = DirectNotifyGlobal.directNotify.newCategory('CogPageManagerAI')

    def __init__(self, air):
        self.air = air

    def toonEncounteredCogs(self, toon, suitsEncountered, zoneId):
        # zoneId is unused, SAD
        cogStatus = toon.getCogStatus()
        for suit in suitsEncountered:
            if toon.getDoId() in suit['activeToons']:
                suitIndex = SuitDNA.suitHeadTypes.index(suit['type'])
                # Loop past suits we don't keep track of in gallery
                if suit['type'] in SuitDNA.notMainTypes:
                    continue
                if cogStatus[suitIndex] == COG_UNSEEN:
                    cogStatus[suitIndex] = COG_BATTLED

        toon.b_setCogStatus(cogStatus)

    def toonKilledCogs(self, toon, suitsKilled, zoneId):
        # Thank you zoneId, very cool!
        cogStatus = toon.getCogStatus()
        cogCount = toon.getCogCount()
        for suit in suitsKilled:
            if suit['isVP'] or suit['isCFO']:
                continue

            if toon.getDoId() in suit['activeToons']:

                # ik this is hacky, but it works for now with custom cogs as we dont have extra room for cog gallery besides the OG 32.
                try:
                    # AP location check
                    cog_location_unique_name = cog_code_to_ap_location(suit['type'])[0]
                    location_id = ap_location_name_to_id(cog_location_unique_name)
                    if location_id > 0:
                        toon.addCheckedLocation(location_id)

                    if suit['level'] > 0:
                        toon.addCheckedLocation(self.checkKilledCogLevel(suit['level']))

                    suitIndex = SuitDNA.suitHeadTypes.index(suit['type'])
                    suitDept = SuitDNA.suitDepts.index(suit['track'])
                    cogQuota = get_min_cog_quota(toon)
                    buildingQuota = get_max_cog_quota(toon)

                    cogCount[suitIndex] += 1
                    cogStatus[suitIndex] = COG_DEFEATED

                    if cogQuota <= cogCount[suitIndex] < buildingQuota:
                        cogStatus[suitIndex] = COG_COMPLETE1
                    else:
                        cogStatus[suitIndex] = COG_COMPLETE2
                        cog_location_unique_name = cog_code_to_ap_location(suit['type'])[1]
                        location_id = ap_location_name_to_id(cog_location_unique_name)
                        if location_id > 0:
                            toon.addCheckedLocation(location_id)
                except:
                    pass

        toon.b_setCogStatus(cogStatus)
        toon.ap_setCogCount(cogCount)

        self.updateRadar(toon)

    def checkKilledCogLevel(self, level):
        levelToLocation = [
            ap_location_name_to_id(locations.ToontownLocationName.LEVEL_ONE_COG_DEFEATED.value),
            ap_location_name_to_id(locations.ToontownLocationName.LEVEL_TWO_COG_DEFEATED.value),
            ap_location_name_to_id(locations.ToontownLocationName.LEVEL_THREE_COG_DEFEATED.value),
            ap_location_name_to_id(locations.ToontownLocationName.LEVEL_FOUR_COG_DEFEATED.value),
            ap_location_name_to_id(locations.ToontownLocationName.LEVEL_FIVE_COG_DEFEATED.value),
            ap_location_name_to_id(locations.ToontownLocationName.LEVEL_SIX_COG_DEFEATED.value),
            ap_location_name_to_id(locations.ToontownLocationName.LEVEL_SEVEN_COG_DEFEATED.value),
            ap_location_name_to_id(locations.ToontownLocationName.LEVEL_EIGHT_COG_DEFEATED.value),
            ap_location_name_to_id(locations.ToontownLocationName.LEVEL_NINE_COG_DEFEATED.value),
            ap_location_name_to_id(locations.ToontownLocationName.LEVEL_TEN_COG_DEFEATED.value),
            ap_location_name_to_id(locations.ToontownLocationName.LEVEL_ELEVEN_COG_DEFEATED.value),
            ap_location_name_to_id(locations.ToontownLocationName.LEVEL_TWELVE_COG_DEFEATED.value),
            ap_location_name_to_id(locations.ToontownLocationName.LEVEL_THIRTEEN_COG_DEFEATED.value),
            ap_location_name_to_id(locations.ToontownLocationName.LEVEL_FOURTEEN_COG_DEFEATED.value),
        ]
        return levelToLocation[level - 1]

    def updateRadar(self, toon):
        cogRadar = toon.getCogRadar()
        buildingRadar = toon.getBuildingRadar()

        for suitDept in range(len(SuitDNA.suitDepts)):
            if buildingRadar[suitDept] == 1:
                continue

            hasBuildingRadar = 1
            hasCogRadar = 1

            for suit in range(SuitDNA.suitsPerDept):
                cogStatus = toon.getCogStatus()[suitDept * SuitDNA.suitsPerDept + suit]
                if cogStatus != COG_COMPLETE2:
                    hasBuildingRadar = 0
                    if cogStatus != COG_COMPLETE1:
                        hasCogRadar = 0

            buildingRadar[suitDept] = hasBuildingRadar
            cogRadar[suitDept] = hasCogRadar

        toon.b_setBuildingRadar(buildingRadar)
        toon.b_setCogRadar(cogRadar)
