from direct.directnotify import DirectNotifyGlobal
from toontown.coghq import CogHQExterior
from toontown.hood import ZoneUtil
from panda3d.toontown import *
from libotp import *

class SellbotHQExterior(CogHQExterior.CogHQExterior):
    notify = DirectNotifyGlobal.directNotify.newCategory('SellbotHQExterior')

    def enter(self, requestStatus):
        CogHQExterior.CogHQExterior.enter(self, requestStatus)
        self.loader.hood.startSky()

    def exit(self):
        self.loader.hood.stopSky()
        CogHQExterior.CogHQExterior.exit(self)

    def handleInterests(self):
       # Grab the "starting" zone ID for this zone
        branchZone = ZoneUtil.getBranchZone(self.zoneId)

        # First, we need to load the DNA file for this Cog HQ.
        dnaStore = DNAStorage()
        dnaFileName = self.genDNAFileName(branchZone)
        loadDNAFile(dnaStore, dnaFileName)

        # Next, we need to collect all of the visgroup zone IDs.
        self.zoneVisDict = {}
        for i in range(dnaStore.getNumDNAVisGroups()):
            groupFullName = dnaStore.getDNAVisGroupName(i)
            visGroup = dnaStore.getDNAVisGroup(i)
            visZoneId = int(base.cr.hoodMgr.extractGroupName(groupFullName))
            visZoneId = ZoneUtil.getTrueZoneId(visZoneId, branchZone)
            visibles = []
            for i in range(visGroup.getNumVisibles()):
                visibles.append(int(visGroup.getVisibleName(i)))

            visibles.append(ZoneUtil.getBranchZone(visZoneId))
            self.zoneVisDict[visZoneId] = visibles
        base.cr.sendSetZoneMsg(self.zoneId, list(self.zoneVisDict.values())[0])