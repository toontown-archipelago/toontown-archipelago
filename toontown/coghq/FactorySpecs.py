from toontown.toonbase import ToontownGlobals
from . import SellbotLegFactorySpec
from . import SellbotLegFactoryCogs
from . import LawbotLegFactorySpec
from . import LawbotLegFactoryCogs


def getFactorySpecModule(factoryId):
    return FactorySpecModules[factoryId]


def getCogSpecModule(factoryId):
    return CogSpecModules[factoryId]


FactorySpecModules = {
    ToontownGlobals.SellbotFactoryInt: SellbotLegFactorySpec,
    ToontownGlobals.SellbotFactoryIntS: SellbotLegFactorySpec,
    ToontownGlobals.LawbotOfficeInt: LawbotLegFactorySpec
}

CogSpecModules = {
    ToontownGlobals.SellbotFactoryInt: SellbotLegFactoryCogs,
    ToontownGlobals.SellbotFactoryIntS: SellbotLegFactoryCogs,
    ToontownGlobals.LawbotOfficeInt: LawbotLegFactoryCogs
}

if __dev__:
    from . import FactoryMockupSpec
    FactorySpecModules[ToontownGlobals.MockupFactoryId] = FactoryMockupSpec
    from . import FactoryMockupCogs
    CogSpecModules[ToontownGlobals.MockupFactoryId] = FactoryMockupCogs
