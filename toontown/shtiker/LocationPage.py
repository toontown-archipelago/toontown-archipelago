from collections import Counter
from . import ShtikerPage
from apworld.toontown import locations, options, fish, test_location, ToontownWinCondition
from BaseClasses import MultiWorld
from toontown.toonbase import TTLocalizer
from direct.gui.DirectGui import *
from panda3d.core import *
from toontown.archipelago.definitions import util
from ..util.ui import make_dsl_scrollable


class LocationPage(ShtikerPage.ShtikerPage):

    def __init__(self):
        ShtikerPage.ShtikerPage.__init__(self)
        self.locationsPossible = []
        self.scrollList = None
        self.textRolloverColor = Vec4(1, 1, 0, 1)
        self.textDownColor = Vec4(0.5, 0.9, 1, 1)
        self.textDisabledColor = Vec4(0.4, 0.8, 0.4, 1)
        self.locationButtons = []

    def load(self):
        title_text_scale = 0.12
        self.title = DirectLabel(parent=self, relief=None, text=TTLocalizer.LocationPageTitle, text_scale=title_text_scale, textMayChange=0, pos=(0, 0, 0.6))
        self.gui = loader.loadModel('phase_3.5/models/gui/friendslist_gui')
        self.listXorigin = 0.02
        self.listFrameSizeX = 0.9
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

    def getLocations(self):
        # Get our checked locations
        checkedLocationIds = base.localAvatar.getCheckedLocations()
        # Get our remaining locations
        missingLocations = []
        # Remaining locations that should be combined
        missingLocationsCounter = Counter()
        # Locations to force to the top of the list.
        priorityMissingLocations = []
        # Determine forbidden location types.
        forbidden_location_types: set[locations.ToontownLocationType] = self.get_disabled_location_types()

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
                priorityMissingLocations.append(location_data.name.value + f" ({base.localAvatar.slotData.get('checks_per_boss', 4)}x)")
                continue
            # Locations that are identical with only a number appended.
            if location_data.type in locations.TREASURE_LOCATION_TYPES + locations.TASK_LOCATION_TYPES:
                without_number = location_data.name.value.rsplit(" ", 1)[0]
                missingLocationsCounter.update([without_number])
                continue
            #Other locations to combine.
            # if location_data.region == locations.ToontownRegionName.GALLERY:
            #     missingLocationsCounter.update(['Cog ' + location_data.type.name.replace('_', ' ').title()])
            #     continue
            if location_data.region == locations.ToontownRegionName.FISHING:
                missingLocationsCounter.update([location_data.type.name.title()])
                continue
            if location_data.type == locations.ToontownLocationType.PET_SHOP:
                missingLocationsCounter.update([location_data.region.name + " Pet Shop"])
                continue
            missingLocations.append(location_data.name.value)
        
        countedMissingLocations = [location +f" ({count}x)" for location, count in missingLocationsCounter.items()]

        self.locationsPossible =  priorityMissingLocations + countedMissingLocations + missingLocations

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

        gags = base.localAvatar.slotData.get('gag_training_check_behavior', 1)
        if gags == options.GagTrainingCheckBehavior.option_disabled:
            forbidden_location_types.add(locations.ToontownLocationType.GAG_TRAINING)

        return forbidden_location_types

    def exit(self):
        super().exit()

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
            itemFrame_borderWidth=(0.01, 0.01), numItemsVisible=15, forceHeight=0.065, items=self.locationButtons
        )
        make_dsl_scrollable(self.scrollList)
        self.scrollList.scrollTo(selectedIndex)
        return

    def updateLocationButtons(self):
        # Cleanup buttons
        for button in self.locationButtons:
            button.detachNode()
            del button
        self.locationButtons = []

        # Generate new buttons
        for location in self.locationsPossible:
            button = self.makeLocationButton(location)
            self.locationButtons.append(button[0])

    def makeLocationButton(self, location):
        locationName = location
        locationButtonParent = DirectFrame()
        locationButton = DirectButton(parent=locationButtonParent, relief=None, text=locationName, text_pos=(0.04, 0), text_scale=0.051, text_align=TextNode.ALeft, text1_bg=self.textDownColor, text2_bg=self.textRolloverColor, text3_fg=self.textDisabledColor, textMayChange=0)
        return (locationButtonParent, locationButton)
