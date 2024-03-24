from . import DistributedSZTreasureAI
from ..archipelago.definitions import util

from apworld.toontown import locations
from toontown.toonbase import ToontownGlobals

ARCHI_CODE_TO_LOCATION = {
    ToontownGlobals.ToontownCentral: [util.ap_location_name_to_id(locations.ToontownLocationName.TTC_TREASURE_1.value),
                                      util.ap_location_name_to_id(locations.ToontownLocationName.TTC_TREASURE_2.value),
                                      util.ap_location_name_to_id(locations.ToontownLocationName.TTC_TREASURE_3.value),
                                      util.ap_location_name_to_id(locations.ToontownLocationName.TTC_TREASURE_4.value),
                                      util.ap_location_name_to_id(locations.ToontownLocationName.TTC_TREASURE_5.value)
                                      ],
    ToontownGlobals.DonaldsDock: [util.ap_location_name_to_id(locations.ToontownLocationName.DD_TREASURE_1.value),
                                  util.ap_location_name_to_id(locations.ToontownLocationName.DD_TREASURE_2.value),
                                  util.ap_location_name_to_id(locations.ToontownLocationName.DD_TREASURE_3.value),
                                  util.ap_location_name_to_id(locations.ToontownLocationName.DD_TREASURE_4.value),
                                  util.ap_location_name_to_id(locations.ToontownLocationName.DD_TREASURE_5.value)
                                  ],
    ToontownGlobals.DaisyGardens: [util.ap_location_name_to_id(locations.ToontownLocationName.DG_TREASURE_1.value),
                                   util.ap_location_name_to_id(locations.ToontownLocationName.DG_TREASURE_2.value),
                                   util.ap_location_name_to_id(locations.ToontownLocationName.DG_TREASURE_3.value),
                                   util.ap_location_name_to_id(locations.ToontownLocationName.DG_TREASURE_4.value),
                                   util.ap_location_name_to_id(locations.ToontownLocationName.DG_TREASURE_5.value)
                                   ],
    ToontownGlobals.MinniesMelodyland: [util.ap_location_name_to_id(locations.ToontownLocationName.MML_TREASURE_1.value),
                                        util.ap_location_name_to_id(locations.ToontownLocationName.MML_TREASURE_2.value),
                                        util.ap_location_name_to_id(locations.ToontownLocationName.MML_TREASURE_3.value),
                                        util.ap_location_name_to_id(locations.ToontownLocationName.MML_TREASURE_4.value),
                                        util.ap_location_name_to_id(locations.ToontownLocationName.MML_TREASURE_5.value)
                                        ],
    ToontownGlobals.TheBrrrgh: [util.ap_location_name_to_id(locations.ToontownLocationName.TB_TREASURE_1.value),
                                util.ap_location_name_to_id(locations.ToontownLocationName.TB_TREASURE_2.value),
                                util.ap_location_name_to_id(locations.ToontownLocationName.TB_TREASURE_3.value),
                                util.ap_location_name_to_id(locations.ToontownLocationName.TB_TREASURE_4.value),
                                util.ap_location_name_to_id(locations.ToontownLocationName.TB_TREASURE_5.value)
                                ],
    ToontownGlobals.DonaldsDreamland: [util.ap_location_name_to_id(locations.ToontownLocationName.DDL_TREASURE_1.value),
                                       util.ap_location_name_to_id(locations.ToontownLocationName.DDL_TREASURE_2.value),
                                       util.ap_location_name_to_id(locations.ToontownLocationName.DDL_TREASURE_3.value),
                                       util.ap_location_name_to_id(locations.ToontownLocationName.DDL_TREASURE_4.value),
                                       util.ap_location_name_to_id(locations.ToontownLocationName.DDL_TREASURE_5.value)
                                       ],
    ToontownGlobals.OutdoorZone: [util.ap_location_name_to_id(locations.ToontownLocationName.AA_TREASURE_1.value),
                                  util.ap_location_name_to_id(locations.ToontownLocationName.AA_TREASURE_2.value),
                                  util.ap_location_name_to_id(locations.ToontownLocationName.AA_TREASURE_3.value),
                                  util.ap_location_name_to_id(locations.ToontownLocationName.AA_TREASURE_4.value),
                                  util.ap_location_name_to_id(locations.ToontownLocationName.AA_TREASURE_5.value)
                                  ],
    ToontownGlobals.GoofySpeedway: [util.ap_location_name_to_id(locations.ToontownLocationName.GS_TREASURE_1.value),
                                    util.ap_location_name_to_id(locations.ToontownLocationName.GS_TREASURE_2.value),
                                    util.ap_location_name_to_id(locations.ToontownLocationName.GS_TREASURE_3.value),
                                    util.ap_location_name_to_id(locations.ToontownLocationName.GS_TREASURE_4.value),
                                    util.ap_location_name_to_id(locations.ToontownLocationName.GS_TREASURE_5.value)
                                    ],
    ToontownGlobals.SellbotHQ: [util.ap_location_name_to_id(locations.ToontownLocationName.SBHQ_TREASURE_1.value),
                                util.ap_location_name_to_id(locations.ToontownLocationName.SBHQ_TREASURE_2.value),
                                util.ap_location_name_to_id(locations.ToontownLocationName.SBHQ_TREASURE_3.value),
                                util.ap_location_name_to_id(locations.ToontownLocationName.SBHQ_TREASURE_4.value),
                                util.ap_location_name_to_id(locations.ToontownLocationName.SBHQ_TREASURE_5.value)
                                ],
    ToontownGlobals.CashbotHQ: [util.ap_location_name_to_id(locations.ToontownLocationName.CBHQ_TREASURE_1.value),
                                util.ap_location_name_to_id(locations.ToontownLocationName.CBHQ_TREASURE_2.value),
                                util.ap_location_name_to_id(locations.ToontownLocationName.CBHQ_TREASURE_3.value),
                                util.ap_location_name_to_id(locations.ToontownLocationName.CBHQ_TREASURE_4.value),
                                util.ap_location_name_to_id(locations.ToontownLocationName.CBHQ_TREASURE_5.value)
                                ],
    ToontownGlobals.LawbotHQ: [util.ap_location_name_to_id(locations.ToontownLocationName.LBHQ_TREASURE_1.value),
                               util.ap_location_name_to_id(locations.ToontownLocationName.LBHQ_TREASURE_2.value),
                               util.ap_location_name_to_id(locations.ToontownLocationName.LBHQ_TREASURE_3.value),
                               util.ap_location_name_to_id(locations.ToontownLocationName.LBHQ_TREASURE_4.value),
                               util.ap_location_name_to_id(locations.ToontownLocationName.LBHQ_TREASURE_5.value)
                               ],
    ToontownGlobals.BossbotHQ: [util.ap_location_name_to_id(locations.ToontownLocationName.BBHQ_TREASURE_1.value),
                                util.ap_location_name_to_id(locations.ToontownLocationName.BBHQ_TREASURE_2.value),
                                util.ap_location_name_to_id(locations.ToontownLocationName.BBHQ_TREASURE_3.value),
                                util.ap_location_name_to_id(locations.ToontownLocationName.BBHQ_TREASURE_4.value),
                                util.ap_location_name_to_id(locations.ToontownLocationName.BBHQ_TREASURE_5.value)
                                ]
}


class DistributedArchiTreasureAI(DistributedSZTreasureAI.DistributedSZTreasureAI):

    def __init__(self, air, treasurePlanner, x, y, z):
        DistributedSZTreasureAI.DistributedSZTreasureAI.__init__(self, air, treasurePlanner, x, y, z)

    def getLocationFromCode(self, archiCode, index):
        return ARCHI_CODE_TO_LOCATION[archiCode][index]

    def validAvatar(self, av, archiCode):
        if av:
            treasureCount = av.slotData.get('treasures_per_location', 2)
            if not treasureCount:
                return False
            for treasure in range(treasureCount):
                if self.getLocationFromCode(archiCode, treasure) in av.getCheckedLocations():
                    continue
                else:
                    return True
            return False
        return False

    def d_setGrab(self, avId, archiCode):
        self.notify.debug('d_setGrab %s' % avId)
        self.sendUpdate('setGrab', [avId])
        av = self.air.doId2do[avId]
        if av:
            treasureCount = av.slotData.get('treasures_per_location', 2)
            for treasure in range(treasureCount):
                if self.getLocationFromCode(archiCode, treasure) in av.getCheckedLocations():
                    continue
                else:
                    av.addCheckedLocation(self.getLocationFromCode(archiCode, treasure))
                    return

