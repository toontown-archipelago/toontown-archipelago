from direct.gui.DirectGui import *

from apworld.archipelago.worlds.toontown.fish import FishLocation, get_catchable_fish_no_rarity, FishProgression
from toontown.toonbase import ToontownGlobals


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
