from toontown.toonbase import ToontownGlobals
from . import SellbotLegFactorySpec
from . import SellbotLegFactoryCogs
from . import SellbotLegFactorySpecS
from . import SellbotLegFactoryCogsS
from . import SellbotLegFactoryCogsTwo
from . import SellbotLegFactorySpecTwo
from . import SellbotLegFactoryCogsThree
from . import SellbotLegFactorySpecThree
from . import SellbotLegFactoryCogsSTwo
from . import SellbotLegFactorySpecSTwo
from . import SellbotLegFactoryCogsSThree
from . import SellbotLegFactorySpecSThree
from . import LawbotLegFactorySpec
from . import LawbotLegFactoryCogs


def getFactorySpecModule(factoryId, sector):
    return FactorySpecModules[factoryId][sector - 1]


def getCogSpecModule(factoryId, sector):
    return CogSpecModules[factoryId][sector - 1]


FactorySpecModules = {
    ToontownGlobals.SellbotFactoryInt: [SellbotLegFactorySpec, SellbotLegFactorySpecTwo, SellbotLegFactorySpecThree],
    ToontownGlobals.SellbotFactoryIntS: [SellbotLegFactorySpecS, SellbotLegFactorySpecSTwo, SellbotLegFactorySpecSThree],
    ToontownGlobals.LawbotOfficeInt: [LawbotLegFactorySpec, LawbotLegFactorySpec, LawbotLegFactorySpec]
}

CogSpecModules = {
    ToontownGlobals.SellbotFactoryInt: [SellbotLegFactoryCogs, SellbotLegFactoryCogsTwo, SellbotLegFactoryCogsThree],
    ToontownGlobals.SellbotFactoryIntS: [SellbotLegFactoryCogsS, SellbotLegFactoryCogsSTwo, SellbotLegFactoryCogsSThree],
    ToontownGlobals.LawbotOfficeInt: [LawbotLegFactoryCogs, LawbotLegFactoryCogs, LawbotLegFactoryCogs]
}

if __dev__:
    from . import FactoryMockupSpec
    FactorySpecModules[ToontownGlobals.MockupFactoryId] = FactoryMockupSpec
    from . import FactoryMockupCogs
    CogSpecModules[ToontownGlobals.MockupFactoryId] = FactoryMockupCogs
