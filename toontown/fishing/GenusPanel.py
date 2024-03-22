from apworld.toontown import fish
from apworld.toontown.fish import FishZone, FishLocation, FishZoneToName, can_av_fish_at_zone
from toontown.toonbase import ToontownGlobals
from direct.directnotify import DirectNotifyGlobal
from direct.gui.DirectGui import *
from panda3d.core import *
from toontown.toonbase import TTLocalizer
from . import FishBase
from . import FishGlobals
from . import FishPhoto
from ..toonbase.TTLocalizerEnglish import FishingRodNameDict


class GenusPanel(DirectFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory('GenusPanel')

    def __init__(self, genus = None, itemIndex = 0, *extraArgs):
        fishingGui = loader.loadModel('phase_3.5/models/gui/fishingBook')
        albumGui = fishingGui.find('**/photo_frame1').copyTo(hidden)
        albumGui.find('**/picture_frame').reparentTo(albumGui, -1)
        albumGui.find('**/arrows').removeNode()
        optiondefs = (('relief', None, None),
         ('state', DGG.NORMAL, None),
         ('image', albumGui, None),
         ('image_scale', (0.025, 0.025, 0.025), None),
         ('image_pos', (0, 1, 0), None),
         ('text', TTLocalizer.UnknownFish, None),
         ('text_scale', 0.065, None),
         ('text_fg', (0.2, 0.1, 0.0, 1), None),
         ('text_pos', (-0.5, -0.34), None),
         ('text_font', ToontownGlobals.getInterfaceFont(), None),
         ('text_wordwrap', 13.5, None),
         ('text_align', TextNode.ALeft, None))
        self.defineoptions({}, optiondefs)
        DirectFrame.__init__(self)
        self.initialiseoptions(GenusPanel)
        self.fishPanel = None
        self.genus = None
        self.setGenus(int(genus))
        self.setScale(1.2)
        albumGui.removeNode()
        return

    def destroy(self):
        if self.fishPanel:
            self.fishPanel.destroy()
            del self.fishPanel
        DirectFrame.destroy(self)

    def load(self):
        pass

    def setGenus(self, genus):
        if self.genus == genus:
            return
        self.genus = genus
        if self.genus != None:
            if self.fishPanel:
                self.fishPanel.destroy()
            f = FishBase.FishBase(self.genus, 0, 0)
            self.fishPanel = FishPhoto.FishPhoto(fish=f, parent=self)
            self.fishPanel.setPos(-0.23, 1, -0.01)
            self.fishPanel.setSwimBounds(-0.2461, 0.2367, -0.207, 0.2664)
            self.fishPanel.setSwimColor(0.47, 1.0, 0.99, 1.0)
            speciesList = FishGlobals.getSpecies(self.genus)
            self.speciesLabels = []

            startZ = 0.05
            spacing = 0.085
            startZ -= (len(speciesList) / 2) * spacing

            for species in range(len(speciesList)):
                label = DirectLabel(
                    parent=self, relief=None, state=DGG.NORMAL,
                    pos=(0.06, 0, startZ + species * spacing),
                    text=TTLocalizer.UnknownFish,
                    text_fg=(0.2, 0.1, 0.0, 1),
                    text_scale=(0.041, 0.045),
                    text_align=TextNode.ALeft,
                    text_font=ToontownGlobals.getInterfaceFont()
                )
                self.speciesLabels.append(label)

        return

    def show(self):
        self.update()
        DirectFrame.show(self)

    def hide(self):
        if self.fishPanel is not None:
            self.fishPanel.hide()
        DirectFrame.hide(self)
        return

    def update(self):
        hasGenus = base.localAvatar.fishCollection.hasGenus(self.genus)

        if self.fishPanel is not None:
            self.fishPanel.show(showBackground=1)
            textProperty = '\1black\1' if hasGenus else '\1red\1'
            self['text'] = textProperty + TTLocalizer.FishGenusNames[self.genus] + '\2'
        for species in range(len(FishGlobals.getSpecies(self.genus))):
            fishDef = fish.get_fish_def(self.genus, species)

            hasFish = base.localAvatar.fishCollection.hasFish(self.genus, species)
            rodRequired = fish.get_required_rod(fishDef)
            rodName = FishingRodNameDict[rodRequired]
            hasSufficientRod = fish.can_catch_fish(fishDef, base.localAvatar.fishingRod)

            textProperty = '\1measly_brown\1' if hasFish else '\1red\1' if hasSufficientRod else '\1red\1'

            speciesText = textProperty + TTLocalizer.FishSpeciesNames[self.genus][species] + '\2\n\1json_fish_subtext\1'
            if hasFish:
                speciesSubtext = '\2'
            elif hasSufficientRod:
                # Show the location of the fish.
                fishLocation = FishLocation(base.localAvatar.slotData.get('fish_locations', 1))
                location_strings = [
                    (
                        '\1black\1' if can_av_fish_at_zone(base.localAvatar, fishZone) else '\1red\1'
                    ) + FishZoneToName[fishZone] + '\2'
                    for fishZone in fishDef.get_filtered_zones(fishLocation)
                ]
                speciesSubtext = f'  {", ".join(location_strings)}\2'
            else:
                # Show the rod required.
                speciesSubtext = f'  \1red\1{rodName} Rod\2'

            self.speciesLabels[species]['text'] = speciesText + speciesSubtext

        return
