from direct.gui.DirectGui import *
from panda3d.core import *

from apworld.toontown.fish import FishLocation, get_catchable_fish_no_rarity, FishProgression
from apworld.toontown import ToontownItemName, get_item_def_from_id
from toontown.toonbase import ToontownGlobals
from toontown.archipelago.definitions import util


class QuestsAvailablePoster(DirectFrame):
    def __init__(self, hoodId, **kw):

        self.hoodId = hoodId

        optiondefs = (
            ('parent', kw['parent'], None),
            ('relief', None, None),
            ('image', self.getImageNode(), None),
            ('image_scale', (0.8, 1.0, 0.58), None),
            ('state', DGG.NORMAL, None)
        )
        self.defineoptions(kw, optiondefs)

        DirectFrame.__init__(self, relief=None, **kw)
        self.initialiseoptions(QuestsAvailablePoster)

        self.numQuestsAvailableLabel = DirectLabel(self, relief=None, text=f"0", text_scale=.9,
                                                   text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1),
                                                   text_font=ToontownGlobals.getSignFont(), pos=(-0.3, 0, 0))

    def getImageNode(self):
        bookModel = loader.loadModel('phase_3.5/models/gui/stickerbook_gui')
        questCard = bookModel.find('**/questCard')
        bookModel.removeNode()
        return questCard

    def getHoodId(self):
        return self.hoodId

    def showLocked(self):
        self.numQuestsAvailableLabel['text'] = 'X'
        self.numQuestsAvailableLabel['text_fg'] = (1, 0, 0, 1)

    def showNumAvailable(self, number):

        color = (.9, .9, .9, 1)
        if number <= 0:
            number = 0
            color = (.1, .9, .1, 1)

        self.numQuestsAvailableLabel['text'] = str(number)
        self.numQuestsAvailableLabel['text_fg'] = color

    def destroy(self):
        super().destroy()
        self.numQuestsAvailableLabel.destroy()


class FishAvailablePoster(QuestsAvailablePoster):
    def __init__(self, hoodId, **kw):
        QuestsAvailablePoster.__init__(self, hoodId=hoodId, **kw)
        self.initialiseoptions(FishAvailablePoster)
        self.numQuestsAvailableLabel['text_scale'] = 0.55
        self.setScale(self.getScale() * 1.3)

    def getImageNode(self):
        iconModels = loader.loadModel('phase_3.5/models/gui/sos_textures')
        iconGeom = iconModels.find('**/fish')
        iconModels.detachNode()
        return iconGeom

    def isVisible(self, av) -> bool:
        # Do we render this at all?
        fishProgression = FishProgression(av.slotData.get('fish_progression', 0))
        if fishProgression in (FishProgression.Nonne,):
            return False
        return True

    def update(self, av):
        # How many fish are present?
        location = FishLocation(av.slotData.get('fish_locations', 1))
        if location == FishLocation.Vanilla:
            # Lump up vanilla locations into playgrounds for display purposes
            location = FishLocation.Playgrounds

        fishRemaining = 0
        for genus, species in get_catchable_fish_no_rarity(self.hoodId, av.fishingRod, location):
            if not av.fishCollection.hasFish(genus, species):
                fishRemaining += 1

        # Show num available.
        self.showNumAvailable(fishRemaining)


class TreasureAvailablePoster(QuestsAvailablePoster):
    def __init__(self, hoodId, **kw):
        QuestsAvailablePoster.__init__(self, hoodId=hoodId, **kw)

        optiondefs = (
            ('parent', kw['parent'], None),
            ('relief', None, None),
            ('image', None, None),
            ('image_scale', None, None),
            ('state', DGG.NORMAL, None)
        )
        self.defineoptions(kw, optiondefs)

        self.initialiseoptions(TreasureAvailablePoster)
        self.numQuestsAvailableLabel['text_scale'] = 0.55
        self.setImage(self.getImageNode())
        self.setTransparency(TransparencyAttrib.MAlpha)
        self['image_scale'] = (0.3, 0.3, 0.3)
        self.setScale(self.getScale() * 1.3)

    def getImageNode(self):
        return 'phase_14/maps/ap_icon_outline.png'

    def getLocationFromCode(self, hood, index):
        return ToontownGlobals.ARCHI_CODE_TO_LOCATION[hood][index]

    def update(self, av):
        # How many treasures are present?
        treasureCount = av.slotData.get('treasures_per_location', 4)

        treasuresRemaining = 0
        for treasure in range(treasureCount):
            if self.getLocationFromCode(self.hoodId, treasure) not in av.getCheckedLocations():
                treasuresRemaining += 1

        # Show num available.
        self.showNumAvailable(treasuresRemaining)


class PetsAvailablePoster(QuestsAvailablePoster):
    def __init__(self, hoodId, **kw):
        QuestsAvailablePoster.__init__(self, hoodId=hoodId, **kw)

        optiondefs = (
            ('parent', kw['parent'], None),
            ('relief', None, None),
            ('image', None, None),
            ('image_scale', None, None),
            ('state', DGG.NORMAL, None)
        )
        self.defineoptions(kw, optiondefs)

        self.initialiseoptions(TreasureAvailablePoster)
        self.numQuestsAvailableLabel['text_scale'] = 0.55
        self.setImage(self.getImageNode())
        self.setTransparency(TransparencyAttrib.MAlpha)
        self['image_scale'] = (0.3, 0.3, 0.3)
        self.setScale(self.getScale() * 1.4)

    def getImageNode(self):
        return 'phase_3.5/maps/doodle_silouette.png'

    def getLocationFromZone(self, hood, index):
        return util.ap_location_name_to_id(ToontownGlobals.ZONE_TO_ID_TO_CHECK[hood][index])

    def update(self, av):
        petsRemaining = 0
        petsPerPlayground = 3
        for pet in range(petsPerPlayground):
            if self.getLocationFromZone(self.hoodId, pet+1) not in av.getCheckedLocations():
                petsRemaining += 1

        # Show num available.
        self.showNumAvailable(petsRemaining)


class CanRacePoster(QuestsAvailablePoster):
    def __init__(self, hoodId, **kw):
        QuestsAvailablePoster.__init__(self, hoodId=hoodId, **kw)

        optiondefs = (
            ('parent', kw['parent'], None),
            ('relief', None, None),
            ('image', None, None),
            ('image_scale', None, None),
            ('state', DGG.NORMAL, None)
        )
        self.defineoptions(kw, optiondefs)

        self.initialiseoptions(TreasureAvailablePoster)
        self.numQuestsAvailableLabel['text_scale'] = 0.55
        self.setImage(self.getImageNode())
        self.setTransparency(TransparencyAttrib.MAlpha)
        self['image_scale'] = (0.55, 0.55, 0.55)
        self.setScale(self.getScale() * 1.4)

    def getImageNode(self):
        iconModels = loader.loadModel('phase_3.5/models/gui/sos_textures')
        iconGeom = iconModels.find('**/kartIcon')
        iconModels.detachNode()
        return iconGeom

    def update(self, av):
        haveItem = False
        items = av.getReceivedItems()
        for item in items:
            index_received, item_id = item
            if get_item_def_from_id(item_id).name == ToontownItemName.GO_KART:
                haveItem = True
                break

        # Show if available.
        self.displayStatus(haveItem)

    def displayStatus(self, status):
        if status:
            self.showUnlocked()
        else:
            self.showLocked()

    def showUnlocked(self):
        self.numQuestsAvailableLabel['text'] = '!'
        self.numQuestsAvailableLabel['text_fg'] = (0, 1, 0, 1)


class CanGolfPoster(QuestsAvailablePoster):
    def __init__(self, hoodId, **kw):
        QuestsAvailablePoster.__init__(self, hoodId=hoodId, **kw)

        optiondefs = (
            ('parent', kw['parent'], None),
            ('relief', None, None),
            ('image', None, None),
            ('image_scale', None, None),
            ('state', DGG.NORMAL, None)
        )
        self.defineoptions(kw, optiondefs)

        self.initialiseoptions(TreasureAvailablePoster)
        self.numQuestsAvailableLabel['text_scale'] = 0.55
        self.setImage(self.getImageNode())
        self.setTransparency(TransparencyAttrib.MAlpha)
        self['image_scale'] = (0.55, 0.55, 0.55)
        self.setScale(self.getScale() * 1.4)

    def getImageNode(self):
        iconModels = loader.loadModel('phase_6/models/golf/golf_gui')
        iconGeom = iconModels.find('**/score_card_icon')
        iconModels.detachNode()
        return iconGeom

    def update(self, av):
        haveItem = False
        items = av.getReceivedItems()
        for item in items:
            index_received, item_id = item
            if get_item_def_from_id(item_id).name == ToontownItemName.GOLF_PUTTER:
                haveItem = True
                break

        # Show if available.
        self.displayStatus(haveItem)

    def displayStatus(self, status):
        if status:
            self.showUnlocked()
        else:
            self.showLocked()

    def showUnlocked(self):
        self.numQuestsAvailableLabel['text'] = '!'
        self.numQuestsAvailableLabel['text_fg'] = (0, 1, 0, 1)
