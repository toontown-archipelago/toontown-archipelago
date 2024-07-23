from . import ToontownTestBase
from ..locations import *
from ..items import *


class ToontownTestTreasures(ToontownTestBase):
    options = {
        'tpsanity': 'keys',
        'treasures_per_location': 6,
    }

    TREASURE_DATA = {
        ToontownItemName.TTC_ACCESS.value:  [ToontownLocationName.TTC_TREASURE_1, ToontownLocationName.TTC_TREASURE_2, ToontownLocationName.TTC_TREASURE_3, ToontownLocationName.TTC_TREASURE_4, ToontownLocationName.TTC_TREASURE_5, ToontownLocationName.TTC_TREASURE_6],
        ToontownItemName.DD_ACCESS.value:   [ToontownLocationName.DD_TREASURE_1, ToontownLocationName.DD_TREASURE_2, ToontownLocationName.DD_TREASURE_3, ToontownLocationName.DD_TREASURE_4, ToontownLocationName.DD_TREASURE_5, ToontownLocationName.DD_TREASURE_6],
        ToontownItemName.DG_ACCESS.value:   [ToontownLocationName.DG_TREASURE_1, ToontownLocationName.DG_TREASURE_2, ToontownLocationName.DG_TREASURE_3, ToontownLocationName.DG_TREASURE_4, ToontownLocationName.DG_TREASURE_5, ToontownLocationName.DG_TREASURE_6],
        ToontownItemName.MML_ACCESS.value:  [ToontownLocationName.MML_TREASURE_1, ToontownLocationName.MML_TREASURE_2, ToontownLocationName.MML_TREASURE_3, ToontownLocationName.MML_TREASURE_4, ToontownLocationName.MML_TREASURE_5, ToontownLocationName.MML_TREASURE_6],
        ToontownItemName.TB_ACCESS.value:   [ToontownLocationName.TB_TREASURE_1, ToontownLocationName.TB_TREASURE_2, ToontownLocationName.TB_TREASURE_3, ToontownLocationName.TB_TREASURE_4, ToontownLocationName.TB_TREASURE_5, ToontownLocationName.TB_TREASURE_6],
        ToontownItemName.DDL_ACCESS.value:  [ToontownLocationName.DDL_TREASURE_1, ToontownLocationName.DDL_TREASURE_2, ToontownLocationName.DDL_TREASURE_3, ToontownLocationName.DDL_TREASURE_4, ToontownLocationName.DDL_TREASURE_5, ToontownLocationName.DDL_TREASURE_6],
    }

    def test_all_species(self):
        LOCATION_TESTS = []

        def add_location_test(location: str, expected: bool, item_pool: list[str]):
            LOCATION_TESTS.append([location, expected, item_pool])

        # Start building location tests.
        for tp_access, locations in self.TREASURE_DATA.items():
            for location in locations:
                add_location_test(location.value, True, [tp_access])
