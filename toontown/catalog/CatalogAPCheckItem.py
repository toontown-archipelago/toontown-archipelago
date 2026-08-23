from panda3d.core import CardMaker, TransparencyAttrib

from . import CatalogItem
from toontown.archipelago.definitions import util
from toontown.toonbase import ToontownGlobals


class CatalogAPCheckItem(CatalogItem.CatalogItem):

    def makeNewItem(self, checkIndex=0):
        self.checkIndex = checkIndex
        CatalogItem.CatalogItem.makeNewItem(self)

    def getTypeName(self):
        return 'Archipelago Check'

    def getName(self):
        return "Cattlelog Check #%d" % (self.checkIndex + 1)

    def getDisplayName(self):
        av = None
        try:
            av = base.localAvatar
        except (AttributeError, NameError):
            return self.getName()

        if not av or not av.hasCachedLocationReward(self.getLocationId()):
            return self.getName()

        return av.getCachedLocationReward(self.getLocationId())

    def getLocationName(self):
        return util.catalog_check_to_location(self.checkIndex)

    def getLocationId(self):
        return util.ap_location_name_to_id(self.getLocationName())

    def recordPurchase(self, avatar, optional):
        if not avatar:
            return ToontownGlobals.P_ItemAvailable

        if avatar.hasCheckedLocation(self.getLocationId()):
            return ToontownGlobals.P_ReachedPurchaseLimit

        avatar.addCheckedLocation(self.getLocationId())
        return ToontownGlobals.P_ItemAvailable

    def reachedPurchaseLimit(self, avatar):
        return avatar.hasCheckedLocation(self.getLocationId())

    def saveHistory(self):
        return 0

    def isGift(self):
        return 0

    def getDeliveryTime(self):
        return 0

    def getBasePrice(self):
        return 1600 + self.checkIndex * 1000

    def getPicture(self, avatar):
        self.hasPicture = True
        frame = self.makeFrame()
        cardMaker = CardMaker('ap-catalog-check')
        cardMaker.setFrame(-1, 1, -1, 1)
        card = frame.attachNewNode(cardMaker.generate())
        card.setTexture(loader.loadTexture('phase_14/maps/ap_icon_outline.png'), 1)
        card.setTransparency(TransparencyAttrib.MAlpha)
        return (frame, None)

    def output(self, store=-1):
        return 'CatalogAPCheckItem(%s%s)' % (self.checkIndex, self.formatOptionalData(store))

    def compareTo(self, other):
        return self.checkIndex - other.checkIndex

    def getHashContents(self):
        return self.checkIndex

    def __eq__(self, other):
        return isinstance(other, CatalogAPCheckItem) and self.checkIndex == other.checkIndex

    def __hash__(self):
        return hash((self.__class__, self.checkIndex))

    def decodeDatagram(self, di, versionNumber, store):
        CatalogItem.CatalogItem.decodeDatagram(self, di, versionNumber, store)
        self.checkIndex = di.getUint8()

    def encodeDatagram(self, dg, store):
        CatalogItem.CatalogItem.encodeDatagram(self, dg, store)
        dg.addUint8(self.checkIndex)
