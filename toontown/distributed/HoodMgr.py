from panda3d.core import *
from direct.showbase import DirectObject
from direct.directnotify import DirectNotifyGlobal
from toontown.launcher import DownloadForceAcknowledge
import string
import random
from toontown.toonbase import ToontownGlobals
from toontown.hood import ZoneUtil

class HoodMgr(DirectObject.DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('HoodMgr')

    dropPoints = {

        ToontownGlobals.DonaldsDock: (
            [-28.0, -2.5, 5.8, 120.0, 0.0, 0.0],
            [-22, 13, 5.8, 155.6, 0.0, 0.0],
            [67, 47, 5.7, 134.7, 0.0, 0.0],
            [62, 19, 5.7, 97.0, 0.0, 0.0],
            [66, -27, 5.7, 80.5, 0.0, 0.0],
            [-114, -7, 5.7, -97.0, -0.0, 0.0],
            [-108, 36, 5.7, -153.8, -0.0, 0.0],
            [-116, -46, 5.7, -70.1, -0.0, 0.0],
            [-63, -79, 5.7, -41.2, -0.0, 0.0],
            [-2, -79, 5.7, 57.4, -0.0, 0.0],
            [-38, -78, 5.7, 9.1, -0.0, 0.0]
        ),

        ToontownGlobals.ToontownCentral: (
            [-60, -8, 1.3, -90, 0, 0],
            [-66, -9, 1.3, -274, 0, 0],
            [17, -28, 4.1, -44, 0, 0],
            [87.7, -22, 4, 66, 0, 0],
            [-9.6, 61.1, 0, 132, 0, 0],
            [-109.0, -2.5, -1.656, -90, 0, 0],
            [-35.4, -81.3, 0.5, -4, 0, 0],
            [-103, 72, 0, -141, 0, 0],
            [93.5, -148.4, 2.5, 43, 0, 0],
            [25, 123.4, 2.55, 272, 0, 0],
            [48, 39, 4, 201, 0, 0],
            [-80, -61, 0.1, -265, 0, 0],
            [-46.875, 43.68, -1.05, 124, 0, 0],
            [34, -105, 2.55, 45, 0, 0],
            [16, -75, 2.55, 56, 0, 0],
            [-27, -56, 0.1, 45, 0, 0],
            [100, 27, 4.1, 150, 0, 0],
            [-70, 4.6, -1.9, 90, 0, 0],
            [-130.7, 50, 0.55, -111, 0, 0]
        ),

        ToontownGlobals.TheBrrrgh: (
            [35, -32, 6.2, 138, 0.0, 0.0],
            [26, -105, 6.2, -339, 0.0, 0.0],
            [-29, -139, 6.2, -385, 0.0, 0.0],
            [-79, -123, 6.2, -369, 0.0, 0.0],
            [-114, -86, 3, -54, 0.0, 0.0],
            [-136, 9, 6.2, -125, 0.0, 0.0],
            [-75, 92, 6.2, -187, 0.0, 0.0],
            [-7, 75, 6.2, -187, 0.0, 0.0],
            [-106, -42, 8.6, -111, 0.0, 0.0],
            [-116, -44, 8.3, -20, 0.0, 0.0]
        ),

        ToontownGlobals.MinniesMelodyland: (
            [86, 44, -13.5, 121.1, 0.0, 0.0],
            [88, -8, -13.5, 91, 0, 0],
            [92, -76, -13.5, 62.5, 0.0, 0.0],
            [53, -112, 6.5, 65.8, 0.0, 0.0],
            [-69, -71, 6.5, -67.2, 0.0, 0.0],
            [-75, 21, 6.5, -100.9, 0.0, 0.0],
            [-21, 72, 6.5, -129.5, 0.0, 0.0],
            [56, 72, 6.5, 138.2, 0.0, 0.0],
            [-41, 47, 6.5, -98.9, 0.0, 0.0]
        ),

        ToontownGlobals.DaisyGardens: (
            [0, 0, 0, -10.5, 0, 0],
            [76, 35, 1.1, -30.2, 0.0, 0.0],
            [97, 106, 0.0, 51.4, 0.0, 0.0],
            [51, 180, 10.0, 22.6, 0.0, 0.0],
            [-14, 203, 10.0, 85.6, 0.0, 0.0],
            [-58, 158, 10.0, -146.9, 0.0, 0.0],
            [-86, 128, 0.0, -178.9, 0.0, 0.0],
            [-64, 65, 0.0, 17.7, 0.0, 0.0],
            [-13, 39, 0.0, -15.7, 0.0, 0.0],
            [-12, 193, 0.0, -112.4, 0.0, 0.0],
            [87, 128, 0.0, 45.4, 0.0, 0.0]
        ),

        ToontownGlobals.DonaldsDreamland: (
            [77, 91, 0.0, 124.4, 0.0, 0.0],
            [29, 92, 0.0, -154.5, 0.0, 0.0],
            [-28, 49, -16.4, -142.0, 0.0, 0.0],
            [21, 40, -16.0, -65.1, 0.0, 0.0],
            [48, 27, -15.4, -161.0, 0.0, 0.0],
            [-2, -22, -15.2, -132.1, 0.0, 0.0],
            [-92, -88, 0.0, -116.3, 0.0, 0.0],
            [-56, -93, 0.0, -21.5, 0.0, 0.0],
            [20, -88, 0.0, -123.4, 0.0, 0.0],
            [76, -90, 0.0, 11.0, 0.0, 0.0]
        ),

        ToontownGlobals.GoofySpeedway: (
            [-0.7, 62, 0.08, 182, 0, 0],
            [-1, -30, 0.06, 183, 0, 0],
            [-13, -120, 0, 307, 0, 0],
            [16.4, -120, 0, 65, 0, 0],
            [-0.5, -90, 0, 182, 0, 0],
            [-30, -25, -0.373, 326, 0, 0],
            [29, -17, -0.373, 32, 0, 0]
        ),

        ToontownGlobals.GolfZone: (
            [-49.6, 102, 0, 162, 0, 0],
            [-22.8, 36.6, 0, 157.5, 0, 0],
            [40, 51, 0, 185, 0, 0],
            [48.3, 122.2, 0, 192, 0, 0],
            [106.3, 69.2, 0, 133, 0, 0],
            [-81.5, 47.2, 0, 183, 0, 0],
            [-80.5, -84.2, 0, 284, 0, 0],
            [73, -111, 0, 354, 0, 0]
        ),

        ToontownGlobals.OutdoorZone: (
            [-165.8, 108, 0.025, 252, 0, 0],
            [21, 130, 0.16, 170, 0, 0],
            [93, 78.5, 0.23, 112, 0, 0],
            [79, -1.6, 0.75, 163, 0, 0],
            [10, 33, 5.32, 130.379, 0, 0],
            [-200, -42, 0.025, 317.543, 0, 0],
            [-21, -65, 0.335, -18, 0, 0],
            [23, 68.5, 4.51, -22.808, 0, 0]
        ),

        ToontownGlobals.Tutorial: (
            [130.9, -8.6, -1.3, 105.5, 0, 0],
        ),

        ToontownGlobals.SellbotHQ: (
            [-15.1324, -197.522, -19.5944, 4.92024, 0, 0],
            [35.9713, -193.266, -19.5944, 4.38194, 0, 0],
            [136.858, -155.959, -0.139187, 88.4705, 0, 0],
            [0.2818, -281.656, 0.883273, 355.735, 0, 0],
            [53.7832, -160.498, -4.33266, 397.602, 0, 0],
            [-55.1619, -184.358, -3.06033, 342.677, 0, 0]
        ),

        ToontownGlobals.CashbotHQ: (
            [117.272,  406.174,  -23.555, -180, 0, 0],
            [109.936,  71.133,  -23.439, -180, 0, 0],
            [52.987,  -172.744,  -63.244, 90, 0, 0],
            [45.325,  -410.603,  -23.439, 30, 0, 0],
            [53.724,  387.432,  -23.555, -120, 0, 0],
            [200.396,  385.046,  -23.555, 140, 0, 0],
            [40.288,  50.693,  -23.439, -70, 0, 0],
            [184.880,  52.997,  -23.439, 70, 0, 0],
            [-30.973,  -93.634,  -63.244, -90, 0, 0],
            [331.529,  -164.959,  -63.244, 125, 0, 0],
            [-13.151,  -257.716,  -63.244, -50, 0, 0],
            [-94.628,  -361.811,  -63.244, -70, 0, 0],
        ),

        ToontownGlobals.LawbotHQ: (
            [77.5, 129.13, -68.4, -166.6, 0, 0],
            [-57.7, 80.75, -68.4, -139.2, 0, 0],
            [203.3, 46.36, -68.4, -213.37, 0, 0],
            [88.2, -336.52, -68.4, -720.4, 0, 0],
            [-20.16, -345.76, -68.4, -777.98, 0, 0],
            [-120.0, -180.75, -28.61, -270, 0, 0],
            [315, -182.96, -42.88, 90, 0, 0],
            [88.2, -336.52, -68.4, -720.4, 0, 0]
        ),

        ToontownGlobals.BossbotHQ: (
            [82.856,  135.019,  0.025, -140, 0, 0],
            [169.307,  -4.546,  0.025, 80, 0, 0],
            [117.247,  -99.977,  0.025, 20, 0, 0],
            [11.846,  -62.417,  0.025, -50, 0, 0],
            [88.102,  -47.011,  0.025, 40, 0, 0],
            [-11.687,  128.536,  0.025, -90, 0, 0],
            [107.012,  73.708,  0.025, 115, 0, 0],
            [26.303,  17.000,  0.025, -30, 0, 0],

        )
    }

    hoodName2Id = {'dd': ToontownGlobals.DonaldsDock,
     'tt': ToontownGlobals.ToontownCentral,
     'br': ToontownGlobals.TheBrrrgh,
     'mm': ToontownGlobals.MinniesMelodyland,
     'dg': ToontownGlobals.DaisyGardens,
     'oz': ToontownGlobals.OutdoorZone,
     'ff': ToontownGlobals.FunnyFarm,
     'gs': ToontownGlobals.GoofySpeedway,
     'dl': ToontownGlobals.DonaldsDreamland,
     'bosshq': ToontownGlobals.BossbotHQ,
     'sellhq': ToontownGlobals.SellbotHQ,
     'cashhq': ToontownGlobals.CashbotHQ,
     'lawhq': ToontownGlobals.LawbotHQ,
     'gz': ToontownGlobals.GolfZone}
    hoodId2Name = {ToontownGlobals.DonaldsDock: 'dd',
     ToontownGlobals.ToontownCentral: 'tt',
     ToontownGlobals.Tutorial: 'tt',
     ToontownGlobals.TheBrrrgh: 'br',
     ToontownGlobals.MinniesMelodyland: 'mm',
     ToontownGlobals.DaisyGardens: 'dg',
     ToontownGlobals.OutdoorZone: 'oz',
     ToontownGlobals.FunnyFarm: 'ff',
     ToontownGlobals.GoofySpeedway: 'gs',
     ToontownGlobals.DonaldsDreamland: 'dl',
     ToontownGlobals.BossbotHQ: 'bosshq',
     ToontownGlobals.SellbotHQ: 'sellhq',
     ToontownGlobals.CashbotHQ: 'cashhq',
     ToontownGlobals.LawbotHQ: 'lawhq',
     ToontownGlobals.GolfZone: 'gz'}
    DefaultDropPoint = [0,
     0,
     0,
     0,
     0,
     0]
    dbgDropMode = 0
    currentDropPoint = 0

    def __init__(self, cr):
        self.cr = cr

    def getDropPoint(self, dropPointList):
        if self.dbgDropMode == 0:
            return random.choice(dropPointList)
        else:
            droppnt = self.currentDropPoint % len(dropPointList)
            self.currentDropPoint = (self.currentDropPoint + 1) % len(dropPointList)
            return dropPointList[droppnt]

    def getAvailableZones(self):
        if base.launcher == None:
            return self.getZonesInPhase(4) + self.getZonesInPhase(6) + self.getZonesInPhase(8) + self.getZonesInPhase(9) + self.getZonesInPhase(10) + self.getZonesInPhase(11) + self.getZonesInPhase(12) + self.getZonesInPhase(13)
        else:
            zones = []
            for phase in set(ToontownGlobals.phaseMap.values()):
                if base.launcher.getPhaseComplete(phase):
                    zones = zones + self.getZonesInPhase(phase)

            return zones
        return

    def getZonesInPhase(self, phase):
        p = []
        for i in list(ToontownGlobals.phaseMap.items()):
            if i[1] == phase:
                p.append(i[0])

        return p

    def getPhaseFromHood(self, hoodId):
        hoodId = ZoneUtil.getCanonicalHoodId(hoodId)
        return ToontownGlobals.phaseMap[hoodId]

    def getPlaygroundCenterFromId(self, hoodId):
        dropPointList = self.dropPoints.get(hoodId, None)
        if dropPointList:
            return self.getDropPoint(dropPointList)
        else:
            self.notify.warning('getPlaygroundCenterFromId: No such hood name as: ' + str(hoodId))
            return self.DefaultDropPoint
        return

    def getIdFromName(self, hoodName):
        id = self.hoodName2Id.get(hoodName)
        if id:
            return id
        else:
            self.notify.error('No such hood name as: %s' % hoodName)
            return None
        return None

    def getNameFromId(self, hoodId):
        name = self.hoodId2Name.get(hoodId)
        if name:
            return name
        else:
            self.notify.error('No such hood id as: %s' % hoodId)
            return None
        return None

    def getFullnameFromId(self, hoodId):
        hoodId = ZoneUtil.getCanonicalZoneId(hoodId)
        return ToontownGlobals.hoodNameMap[hoodId][-1]

    def addLinkTunnelHooks(self, hoodPart, nodeList, currentZoneId):
        tunnelOriginList = []
        for i in nodeList:
            linkTunnelNPC = i.findAllMatches('**/linktunnel*')
            for p in range(linkTunnelNPC.getNumPaths()):
                linkTunnel = linkTunnelNPC.getPath(p)
                name = linkTunnel.getName()
                nameParts = name.split('_')
                hoodStr = nameParts[1]
                zoneStr = nameParts[2]
                hoodId = self.getIdFromName(hoodStr)
                zoneId = int(zoneStr)
                hoodId = ZoneUtil.getTrueZoneId(hoodId, currentZoneId)
                zoneId = ZoneUtil.getTrueZoneId(zoneId, currentZoneId)
                linkSphere = linkTunnel.find('**/tunnel_trigger')
                if linkSphere.isEmpty():
                    linkSphere = linkTunnel.find('**/tunnel_sphere')
                if not linkSphere.isEmpty():
                    cnode = linkSphere.node()
                    cnode.setName('tunnel_trigger_' + hoodStr + '_' + zoneStr)
                    cnode.setCollideMask(ToontownGlobals.WallBitmask | ToontownGlobals.GhostBitmask)
                else:
                    linkSphere = linkTunnel.find('**/tunnel_trigger_' + hoodStr + '_' + zoneStr)
                    if linkSphere.isEmpty():
                        self.notify.error('tunnel_trigger not found')
                tunnelOrigin = linkTunnel.find('**/tunnel_origin')
                if tunnelOrigin.isEmpty():
                    self.notify.error('tunnel_origin not found')
                tunnelOriginPlaceHolder = render.attachNewNode('toph_' + hoodStr + '_' + zoneStr)
                tunnelOriginList.append(tunnelOriginPlaceHolder)
                tunnelOriginPlaceHolder.setPos(tunnelOrigin.getPos(render))
                tunnelOriginPlaceHolder.setHpr(tunnelOrigin.getHpr(render))
                hood = base.localAvatar.cr.playGame.hood
                if ZoneUtil.tutorialDict:
                    how = 'teleportIn'
                    tutorialFlag = 1
                else:
                    how = 'tunnelIn'
                    tutorialFlag = 0
                hoodPart.accept('enter' + linkSphere.getName(), hoodPart.handleEnterTunnel, [{'loader': ZoneUtil.getLoaderName(zoneId),
                  'where': ZoneUtil.getToonWhereName(zoneId),
                  'how': how,
                  'hoodId': hoodId,
                  'zoneId': zoneId,
                  'shardId': None,
                  'tunnelOrigin': tunnelOriginPlaceHolder,
                  'tutorial': tutorialFlag}])

        return tunnelOriginList

    def extractGroupName(self, groupFullName):
        # return string.split(groupFullName, ':', 1)[0]
        return groupFullName.split(':', 1)[0]

    def makeLinkTunnelName(self, hoodId, currentZone):
        return '**/toph_' + self.getNameFromId(hoodId) + '_' + str(currentZone)
