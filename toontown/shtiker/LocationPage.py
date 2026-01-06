import re
from . import ShtikerPage
from apworld.toontown import locations, options, fish, test_location, ToontownWinCondition
from BaseClasses import MultiWorld
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals
from direct.gui.DirectGui import *
from panda3d.core import *
from toontown.archipelago.definitions import util
from ..util.ui import make_dsl_scrollable

class LocationNode(DirectFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.locationNodes = []

    def __createDisplay(self, text, yOffset, total) -> DirectLabel:
        if yOffset == 25 and total > 26:
            text=f"and {total - yOffset} more..."
        elif yOffset > 25:
            text=""
        return DirectLabel(
            parent=self, relief=None, image_scale=(1.25, 1.25, 1.25),
            pos=(-0.36, 0, -0.06 - 0.044 * yOffset), text=text, text_scale=0.035,
            text_align=TextNode.ALeft, text_pos=(0.03, -0.0125), text_fg=Vec4(0, 0, 0, 1),
            text_wordwrap=24
        )

    def updateDisplays(self, originals: list[str]):
        # Clear the old lines
        for h in self.locationNodes:
            h.destroy()
        self.locationNodes.clear()

        total = len(originals)
        for index, label in enumerate(originals):
            node = self.__createDisplay(label, index, total)
            self.locationNodes.append(node)

    def showDefaultDisplay(self):
        # Clear the old lines (needed for re-entering the page)
        for h in self.locationNodes:
            h.destroy()
        self.locationNodes.clear()

        label = "Select a location group to view all accessible\nlocations within."
        defaultNode = self.__createDisplay(label, 0, 1)
        self.locationNodes.append(defaultNode)

class LocationCategory():
    def __init__(self, name: str, location: list[str] | str | None = None):
        self.name = name
        if location is None:
            self.locations = set()
        elif isinstance(location, str):
            self.locations = {location}
        else:
            self.locations = set(location)

    def add_location(self, location: str):
        self.locations.update([location])

    def get_count(self):
        return len(self.locations)

    def get_locations(self):
        return sorted(self.locations, key=locations.LOCATION_NAME_TO_ID.get)
    
    def get_raw_name(self):
        return self.name
    
    def get_display_name(self):
        if self.get_count() != 1:
            return self.name + f' ({self.get_count()}x)'
        return self.name

    def __str__(self):
        return self.get_raw_name()



class LocationPage(ShtikerPage.ShtikerPage):

    def __init__(self):
        ShtikerPage.ShtikerPage.__init__(self)
        self.locationsPossible: dict[str,LocationCategory] = {}
        self.scrollList = None
        self.textRolloverColor = Vec4(1, 1, 0, 1)
        self.textDownColor = Vec4(0.5, 0.9, 1, 1)
        self.textDisabledColor = Vec4(0.6, 0.5, 1, 1)  # marks selected.
        self.locationButtons = []
        self.LocationNode = LocationNode(self)
        self.LocationNode.setPos(0.42, 0, 0.5)
        self.LocationNode.hide()
        self.selectedLocation: int | None = None


    def load(self):
        title_text_scale = 0.12
        self.title = DirectLabel(parent=self, relief=None, text=TTLocalizer.LocationPageTitle, text_scale=title_text_scale, textMayChange=0, pos=(0, 0, 0.6))
        self.gui = loader.loadModel('phase_3.5/models/gui/friendslist_gui')
        self.listXorigin = 0.02
        self.listFrameSizeX = 0.86
        self.listZorigin = -0.96
        self.listFrameSizeZ = 1.04
        self.arrowButtonScale = 1.3
        self.itemFrameXorigin = -0.237
        self.itemFrameZorigin = 0.365
        self.buttonXstart = self.itemFrameXorigin + 0.475
        self.regenerateScrollList()
        return

    def enter(self):
        ShtikerPage.ShtikerPage.enter(self)
        self.getLocations()
        self.regenerateScrollList()
        self.LocationNode.show()
        self.LocationNode.showDefaultDisplay()
        self.selectedLocation = None

    def getLocations(self):
        # Get our checked locations
        checkedLocationIds = base.localAvatar.getCheckedLocations()
        # Get our remaining locations
        missingLocations: dict[str,LocationCategory] = {}
        # Locations to force to the top of the list.
        priorityMissingLocations: dict[str,LocationCategory] = {}
        # Determine forbidden location types.
        forbidden_location_types: set[locations.ToontownLocationType] = self.get_disabled_location_types()

        training_types = [
            locations.ToontownLocationType.SUPPORT_GAG_TRAINING,
            locations.ToontownLocationType.TRAP_GAG_TRAINING,
            locations.ToontownLocationType.SOUND_GAG_TRAINING,
            locations.ToontownLocationType.THROW_GAG_TRAINING,
            locations.ToontownLocationType.SQUIRT_GAG_TRAINING,
            locations.ToontownLocationType.DROP_GAG_TRAINING,
        ]

        for location_data in locations.LOCATION_DEFINITIONS:
            # Do we need to track this location based on settings?
            if location_data.type in forbidden_location_types:
                continue
            # Do we already have this location?
            if util.ap_location_name_to_id(location_data.name.value) in checkedLocationIds:
                continue
            # Is this location in logic?
            if not test_location(location_data, base.localAvatar, MultiWorld, 1, base.localAvatar.slotData):
                continue

            # Boss checks, combine the rewards into this location for the tracker.
            if location_data.type == locations.ToontownLocationType.BOSS_META:
                cpb = base.localAvatar.slotData.get('checks_per_boss', 4)
                boss_locations = locations.REGION_TO_BOSS_LOCATIONS.get(location_data.region)
                enabled_locations = []
                for x in range(cpb):
                    enabled_locations.append(boss_locations[x].value)
                obj = LocationCategory(location_data.name.value, enabled_locations)
                priorityMissingLocations.update({location_data.name.value:obj})
                continue
            # Locations that are identical with only a number appended.
            if location_data.type in locations.TREASURE_LOCATION_TYPES + locations.TASK_LOCATION_TYPES + locations.KNOCK_KNOCK_LOCATION_TYPES:
                name = location_data.name.value.rsplit(" ", 1)[0]
                name = name.replace("Knock Knock", "Street")
                obj = missingLocations.get(name, LocationCategory(name))
                obj.add_location(location_data.name.value)

            elif location_data.type == locations.ToontownLocationType.COG_LEVELS:
                obj = missingLocations.get("Cog Levels", LocationCategory("Cog Levels"))
                obj.add_location(location_data.name.value)

            elif location_data.region == locations.ToontownRegionName.GALLERY:
                name = location_data.name.value.split('(')[0].rstrip()
                obj = missingLocations.get(name, LocationCategory(name))
                obj.add_location(location_data.name.value)

            elif location_data.region in [locations.ToontownRegionName.FISHING]:
                name = location_data.type.name.replace("_", " ").title()
                obj = missingLocations.get(name, LocationCategory(name))
                obj.add_location(location_data.name.value)

            elif location_data.type == locations.ToontownLocationType.PET_SHOP:
                name=location_data.region.name + " Pet Shop"
                obj = missingLocations.get(name, LocationCategory(name))
                obj.add_location(location_data.name.value)

            elif location_data.type in training_types:
                name = location_data.rules[0].name
                name = re.sub(r'(?<=\B)([A-Z])', r' \1', name).rsplit(" ", 1)[0] + " Training"
                obj = missingLocations.get(name, LocationCategory(name))
                obj.add_location(location_data.name.value)

            elif location_data.type == locations.ToontownLocationType.FACILITIES:
                name = location_data.rules[0].name
                name = re.sub(r'(?<=\B)([A-Z])', r' \1', name).rsplit(" ", 1)[0]
                obj = missingLocations.get(name, LocationCategory(name))
                obj.add_location(location_data.name.value)

            elif location_data.type == locations.ToontownLocationType.BUILDINGS:
                name = "Building Clear"
                obj = missingLocations.get(name, LocationCategory(name))
                obj.add_location(location_data.name.value)

            elif location_data.type in [locations.ToontownLocationType.RACING, locations.ToontownLocationType.GOLF]:
                name = location_data.type.name.title()
                obj = missingLocations.get(name, LocationCategory(name))
                obj.add_location(location_data.name.value)

            else:
                name = location_data.name.value
                obj = LocationCategory(name, name)
            missingLocations.update({name:obj})

        self.locationsPossible = {**priorityMissingLocations, **missingLocations}

    def get_disabled_location_types(self) -> set[locations.ToontownLocationType]:
        """
        Returns a set of disabled location types.
        These location types are removed from logic generation.
        """
        forbidden_location_types: set[locations.ToontownLocationType] = set()
        fish_checks = fish.FishChecks(base.localAvatar.slotData.get('fish_checks', 0))
        if fish_checks == fish.FishChecks.AllSpecies:
            forbidden_location_types.add(locations.ToontownLocationType.FISHING_GENUS)
            forbidden_location_types.add(locations.ToontownLocationType.FISHING_GALLERY)
        elif fish_checks == fish.FishChecks.AllGalleryAndGenus:
            forbidden_location_types.add(locations.ToontownLocationType.FISHING)
        elif fish_checks == fish.FishChecks.AllGallery:
            forbidden_location_types.add(locations.ToontownLocationType.FISHING)
            forbidden_location_types.add(locations.ToontownLocationType.FISHING_GENUS)
        elif fish_checks == fish.FishChecks.Nonne:
            forbidden_location_types.add(locations.ToontownLocationType.FISHING)
            forbidden_location_types.add(locations.ToontownLocationType.FISHING_GENUS)
            forbidden_location_types.add(locations.ToontownLocationType.FISHING_GALLERY)

        tpl = base.localAvatar.slotData.get('treasures_per_location', 4)
        rev_locs = locations.TREASURE_LOCATION_TYPES[::-1]
        for i in range(len(rev_locs) - tpl):
            forbidden_location_types.add(rev_locs[i])

        kkps = base.localAvatar.slotData.get('jokes_per_street', 3)
        rev_locs = locations.KNOCK_KNOCK_LOCATION_TYPES[::-1]
        for i in range(len(rev_locs) - kkps):
            forbidden_location_types.add(rev_locs[i])

        # Differs from the apworld for special implementation here.
        forbidden_location_types.update(locations.BOSS_LOCATION_TYPES)
        wc = base.localAvatar.slotData.get('win_condition', ToontownWinCondition.cog_bosses)
        cpb = base.localAvatar.slotData.get('checks_per_boss', 4)

        if not ToontownWinCondition.cog_bosses in ToontownWinCondition(wc) and cpb <= 0:
            forbidden_location_types.add(locations.ToontownLocationType.BOSS_META)

        racing = base.localAvatar.slotData.get('racing_logic', False)
        if not racing:
            forbidden_location_types.add(locations.ToontownLocationType.RACING)

        golf = base.localAvatar.slotData.get('golfing_logic', False)
        if not golf:
            forbidden_location_types.add(locations.ToontownLocationType.GOLF)

        GAG_LOCATION_TYPES = [
            locations.ToontownLocationType.SUPPORT_GAG_TRAINING,
            locations.ToontownLocationType.TRAP_GAG_TRAINING,
            locations.ToontownLocationType.SOUND_GAG_TRAINING,
            locations.ToontownLocationType.THROW_GAG_TRAINING,
            locations.ToontownLocationType.SQUIRT_GAG_TRAINING,
            locations.ToontownLocationType.DROP_GAG_TRAINING,
        ]

        gags = base.localAvatar.slotData.get('gag_training_check_behavior', 1)
        if gags == options.GagTrainingCheckBehavior.option_disabled:
            for type in GAG_LOCATION_TYPES:
                forbidden_location_types.add(type)

        omitted_track = base.localAvatar.slotData.get('omit_gag', 0)
        if omitted_track != 0:
            forbidden_location_types.add(GAG_LOCATION_TYPES[omitted_track])

        return forbidden_location_types

    def regenerateScrollList(self):
        selectedIndex = 0
        if self.scrollList:
            selectedIndex = self.scrollList.getSelectedIndex()
            self.updateLocationButtons()
            self.scrollList.destroy()
            self.scrollList = None

        hostUi = loader.loadModel('phase_4/models/parties/schtickerbookHostingGUI')
        checkmarkGeom = hostUi.find('**/checkmark')
        self.scrollList = DirectScrolledList(
            parent=self, relief=None, pos=(-0.625, 0, 0),
            # scale=0.75,
            incButton_image=(self.gui.find('**/FndsLst_ScrollUp'),
            self.gui.find('**/FndsLst_ScrollDN'),
            self.gui.find('**/FndsLst_ScrollUp_Rllvr'),
            self.gui.find('**/FndsLst_ScrollUp')), incButton_relief=None,
            incButton_scale=(self.arrowButtonScale * 1.5, self.arrowButtonScale, -self.arrowButtonScale),
            incButton_pos=(self.buttonXstart, 0, self.itemFrameZorigin - 0.999),
            incButton_image3_color=Vec4(1, 1, 1, 0.2), decButton_image=(self.gui.find('**/FndsLst_ScrollUp'),
            self.gui.find('**/FndsLst_ScrollDN'),
            self.gui.find('**/FndsLst_ScrollUp_Rllvr'),
            self.gui.find('**/FndsLst_ScrollUp')), decButton_relief=None,
            decButton_scale=(self.arrowButtonScale * 1.5, self.arrowButtonScale, self.arrowButtonScale),
            decButton_pos=(self.buttonXstart, 0, self.itemFrameZorigin + 0.125),
            decButton_image3_color=Vec4(1, 1, 1, 0.2), itemFrame_pos=(self.itemFrameXorigin, 0, self.itemFrameZorigin),
            itemFrame_scale=1.0, itemFrame_relief=DGG.SUNKEN, itemFrame_frameSize=(self.listXorigin,
            self.listXorigin + self.listFrameSizeX,
            self.listZorigin,
            self.listZorigin + self.listFrameSizeZ), itemFrame_frameColor=(0.85, 0.95, 1, 1),
            itemFrame_borderWidth=(0.01, 0.01), numItemsVisible=15, forceHeight=0.065, items=self.locationButtons #Frames
        )
        make_dsl_scrollable(self.scrollList)
        self.scrollList.scrollTo(selectedIndex)
        return

    def updateLocationButtons(self):
        # Cleanup buttons
        for button in self.locationButtons:
            button.detachNode()
            del button
        self.selectedLocation = False
        self.locationButtons = []

        # Generate new buttons
        for index, location in enumerate(self.locationsPossible.values()):
            button = self.makeLocationButton(index, location)
            self.locationButtons.append(button)

    def makeLocationButton(self, index: int, location: LocationCategory):
        locationName = location.get_display_name()
        command = lambda: self.setLocations(index, location)
        locationButton = DirectButton(relief=None, text=locationName, text_pos=(0.04, 0), text_scale=0.051, text_align=TextNode.ALeft, text1_bg=self.textDownColor, text2_bg=self.textRolloverColor, text3_bg=self.textDisabledColor, textMayChange=0, command=command)
        return locationButton

    def setLocations(self, index, location: LocationCategory):
        self.LocationNode.updateDisplays(location.get_locations())
        self.locationButtons[index]['state'] = DGG.DISABLED
        if not self.selectedLocation is None:
            self.locationButtons[self.selectedLocation]['state'] = DGG.NORMAL
        self.selectedLocation = index

    def showLocationsOnscreen(self):

        # Check if there is currently something already displaying in the hotkey interface slot
        if not base.localAvatar.allowOnscreenInterface():
            return

        # We can now own the slot
        base.localAvatar.setCurrentOnscreenInterface(self)
        messenger.send('wakeup')

        self.enter()
        self.reparentTo(aspect2d)
        self.book.show()
        self.book.setZ(self.book.getZ() - 0.11)
        self.book.hidePageArrows()
        self.book.ignore(ToontownGlobals.StickerBookPageLeft)
        self.book.ignore(ToontownGlobals.StickerBookPageRight)
        self.show()

    def hideLocationsOnscreen(self):

        # If the current onscreen interface is not us, don't do anything
        if base.localAvatar.getCurrentOnscreenInterface() is not self:
            return

        base.localAvatar.setCurrentOnscreenInterface(None)  # Free up the on screen interface slot

        self.reparentTo(self.book)
        self.book.hide()
        self.book.setZ(self.book.getZ() + 0.11)
        self.book.showPageArrows()
        self.book.ignore(ToontownGlobals.StickerBookPageLeft)
        self.book.ignore(ToontownGlobals.StickerBookPageRight)
        self.hide()

    def acceptOnscreenHooks(self):
        self.accept(ToontownGlobals.LocationsHotkeyOn, self.showLocationsOnscreen)
        self.accept(ToontownGlobals.LocationsHotkeyOff, self.hideLocationsOnscreen)

    def ignoreOnscreenHooks(self):
        self.ignore(ToontownGlobals.LocationsHotkeyOn)
        self.ignore(ToontownGlobals.LocationsHotkeyOff)