from . import ToontownTestBase
from ..fish import FISH_DICT, FishZone, FishDef, FishLocation, GENUS_SPECIES_TO_LOCATION, get_required_rod
from ..items import *


class ToontownTestFishingProgression(ToontownTestBase):
    options = {
        'tpsanity': 'keys',
        'fish_locations': 'playgrounds',
        'fish_checks': 'all_species',
        'fish_progression': 'licenses_and_rods',
    }

    FISHING_DATA = {
        FishZone.ToontownCentral:   [ToontownItemName.TTC_ACCESS.value, ToontownItemName.TTC_FISHING.value],
        FishZone.DonaldsDock:       [ToontownItemName.DD_ACCESS.value, ToontownItemName.DD_FISHING.value],
        FishZone.DaisyGardens:      [ToontownItemName.DG_ACCESS.value, ToontownItemName.DG_FISHING.value],
        FishZone.MinniesMelodyland: [ToontownItemName.MML_ACCESS.value, ToontownItemName.MML_FISHING.value],
        FishZone.TheBrrrgh:         [ToontownItemName.TB_ACCESS.value, ToontownItemName.TB_FISHING.value],
        FishZone.DonaldsDreamland:  [ToontownItemName.DDL_ACCESS.value, ToontownItemName.DDL_FISHING.value],
    }

    def test_all_species(self):
        LOCATION_TESTS = []

        def add_location_test(location: str, expected: bool, item_pool: list[str]):
            LOCATION_TESTS.append([location, expected, item_pool])

        # Start building location tests.
        for genus, fds in FISH_DICT.items():
            for fishIndex, fish_def in enumerate(fds):
                fish_def: FishDef
                expected_fish: str = GENUS_SPECIES_TO_LOCATION[(genus, fishIndex)].value
                rods = [ToontownItemName.FISHING_ROD_UPGRADE.value] * get_required_rod(fish_def)

                # Determine the zones this Fish can be in.
                TEST_ZONES: set[FishZone] = set()
                for fz in fish_def.get_filtered_zones(FishLocation.Playgrounds):
                    if fz == FishZone.Anywhere:
                        for _fz in self.FISHING_DATA.keys():
                            TEST_ZONES.add(_fz)
                        break
                    TEST_ZONES.add(fz)

                # Test each of them.
                for fz in TEST_ZONES:
                    tp_access, license = self.FISHING_DATA[fz]

                    if tp_access == ToontownItemName.TTC_ACCESS.value:
                        # TTC has optional TP access still
                        add_location_test(expected_fish, True, [license] + rods)
                    else:
                        add_location_test(expected_fish, True, [tp_access, license] + rods)

        # Run all location tests.
        self.run_location_tests(LOCATION_TESTS)
