from test.bases import WorldTestBase
from .. import locations

from ..locations import *


class ToontownTestBase(WorldTestBase):
    game = "Toontown"


class ToontownTestDefault(ToontownTestBase):
    pass


class ToontownTestPlaygroundAccess(ToontownTestBase):

    def test_playground_access(self):

        # TTC always available
        for i in range(12):
            self.assertTrue(self.can_reach_location(f"Toontown Central Task #{i + 1}"))

        # Test task + clearance working correctly
        for pg_name in ("Donald's Dock", "Daisy Gardens", "Minnie's Melodyland", "The Brrrgh", "Donald's Dreamland"):

            for i in range(12):
                self.assertFalse(self.can_reach_location(f"{pg_name} Task #{i + 1}"))

            self.collect_by_name([f"{pg_name} HQ Clearance"])

            for i in range(12):
                self.assertTrue(self.can_reach_location(f"{pg_name} Task #{i + 1}"))


class TestFacilityAccess(ToontownTestBase):
    def test_facility_access(self):
        self.assertAccessDependency([CLEAR_FRONT_FACTORY], [["Front Factory Key"]])
        self.assertAccessDependency([CLEAR_SIDE_FACTORY], [["Side Factory Key"]])

        self.assertAccessDependency([CLEAR_COIN_MINT], [["Coin Mint Key"]])
        self.assertAccessDependency([CLEAR_DOLLAR_MINT], [["Dollar Mint Key"]])
        self.assertAccessDependency([CLEAR_BULLION_MINT], [["Bullion Mint Key"]])

        self.assertAccessDependency([CLEAR_A_OFFICE], [["A Office Key"]])
        self.assertAccessDependency([CLEAR_B_OFFICE], [["B Office Key"]])
        self.assertAccessDependency([CLEAR_C_OFFICE], [["C Office Key"]])
        self.assertAccessDependency([CLEAR_D_OFFICE], [["D Office Key"]])

        self.assertAccessDependency([CLEAR_FRONT_THREE], [["Front One Key"]])
        self.assertAccessDependency([CLEAR_MIDDLE_THREE], [["Middle Two Key"]])
        self.assertAccessDependency([CLEAR_BACK_THREE], [["Back Three Key"]])

class TestBossAccess(ToontownTestBase):

    def test_boss_access(self):
        self.assertFalse(self.can_reach_location(locations.CLEAR_VP))
        self.collect_by_name(["Sellbot Disguise"])
        self.assertTrue(self.can_reach_location(locations.CLEAR_VP))

        self.assertFalse(self.can_reach_location(locations.CLEAR_CFO))
        self.collect_by_name(["Cashbot Disguise"])
        self.assertTrue(self.can_reach_location(locations.CLEAR_CFO))

        self.assertFalse(self.can_reach_location(locations.CLEAR_CJ))
        self.collect_by_name(["Lawbot Disguise"])
        self.assertTrue(self.can_reach_location(locations.CLEAR_CJ))

        self.assertFalse(self.can_reach_location(locations.CLEAR_CEO))
        self.collect_by_name(["Bossbot Disguise"])
        self.assertTrue(self.can_reach_location(locations.CLEAR_CEO))

    def test_victory_condition(self):

        self.assertFalse(self.can_reach_location(SAVED_TOONTOWN))
        self.collect_by_name(["Sellbot Disguise"])
        self.collect_by_name(["Sellbot Proof"])
        self.assertFalse(self.can_reach_location(SAVED_TOONTOWN))
        self.collect_by_name(["Cashbot Proof"])
        self.collect_by_name(["Cashbot Disguise"])
        self.assertFalse(self.can_reach_location(SAVED_TOONTOWN))
        self.collect_by_name(["Lawbot Proof"])
        self.collect_by_name(["Lawbot Disguise"])
        self.assertFalse(self.can_reach_location(SAVED_TOONTOWN))
        self.collect_by_name(["Bossbot Proof"])
        self.collect_by_name(["Bossbot Disguise"])

        self.assertTrue(self.can_reach_location(SAVED_TOONTOWN))
