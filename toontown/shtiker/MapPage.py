from typing import List

from apworld.toontown.fish import can_av_fish_at_zone
from apworld.toontown import locations
from toontown.quest import Quests
from . import ShtikerPage
from toontown.toonbase import ToontownGlobals
from otp.otpbase import PythonUtil
from toontown.hood import ZoneUtil
from direct.gui.DirectGui import *
from panda3d.core import *
from toontown.toonbase import TTLocalizer
from .QuestsAvailablePoster import QuestsAvailablePoster, FishAvailablePoster, TreasureAvailablePoster, PetsAvailablePoster, CanRacePoster, CanGolfPoster
from ..building import FADoorCodes


class MapPage(ShtikerPage.ShtikerPage):

    def __init__(self):
        ShtikerPage.ShtikerPage.__init__(self)

    def load(self):
        ShtikerPage.ShtikerPage.load(self)
        mapModel = loader.loadModel('phase_3.5/models/gui/toontown_map')
        self.map = DirectFrame(parent=self, relief=None, image=mapModel.find('**/toontown_map'), image_scale=(1.8, 1, 1.35), scale=0.97, pos=(0, 0, 0.0775))
        mapModel.removeNode()
        self.allZones = []
        for hood in ToontownGlobals.Hoods:
            if hood not in [ToontownGlobals.GolfZone, ToontownGlobals.FunnyFarm]:
                self.allZones.append(hood)

        self.cloudScaleList = (((0.55, 0, 0.4), (0.35, 0, 0.25)),
         (),
         ((0.45, 0, 0.45), (0.5, 0, 0.4)),
         ((0.7, 0, 0.45),),
         ((0.55, 0, 0.4),),
         ((0.6, 0, 0.4), (0.5332, 0, 0.32)),
         ((0.7, 0, 0.45), (0.7, 0, 0.45)),
         ((0.7998, 0, 0.39),),
         ((0.5, 0, 0.4),),
         ((-0.45, 0, 0.4),),
         ((-0.45, 0, 0.35),),
         ((0.5, 0, 0.35),),
         ((0.5, 0, 0.35),))
        self.cloudPosList = (((0.575, 0.0, -0.04), (0.45, 0.0, -0.25)),
         (),
         ((0.375, 0.0, 0.4), (0.5625, 0.0, 0.2)),
         ((-0.02, 0.0, 0.23),),
         ((-0.3, 0.0, -0.4),),
         ((0.25, 0.0, -0.425), (0.125, 0.0, -0.36)),
         ((-0.5625, 0.0, -0.07), (-0.45, 0.0, 0.2125)),
         ((-0.125, 0.0, 0.5),),
         ((0.66, 0.0, -0.4),),
         ((-0.68, 0.0, -0.444),),
         ((-0.6, 0.0, 0.45),),
         ((0.66, 0.0, 0.5),),
         ((0.4, 0.0, -0.35),))
        self.labelPosList = ((0.594, 0.0, -0.075),
         (0.0, 0.0, -0.1),
         (0.475, 0.0, 0.25),
         (0.1, 0.0, 0.15),
         (-0.3, 0.0, -0.375),
         (0.2, 0.0, -0.45),
         (-0.55, 0.0, 0.0),
         (-0.088, 0.0, 0.47),
         (0.7, 0.0, -0.5),
         (-0.7, 0.0, -0.5),
         (-0.7, 0.0, 0.5),
         (0.7, 0.0, 0.5),
         (0.45, 0.0, -0.45))
        self.labels = []
        self.clouds = []
        self.cloudAlphas = []

        self.questsAvailableIcons: List[QuestsAvailablePoster] = []
        self.fishAvailableIcons: List[FishAvailablePoster] = []
        self.treasureAvailableIcons: List[TreasureAvailablePoster] = []
        self.petsAvailableIcons: List[PetsAvailablePoster] = []
        self.raceIcons: List[CanRacePoster] = []
        self.golfIcons: List[CanGolfPoster] = []

        guiButton = loader.loadModel('phase_3/models/gui/quit_button')
        buttonLoc = (0.45, 0, - 0.74)
        if base.housingEnabled:
            buttonLoc = (0.55, 0, -0.74)
        self.safeZoneButton = DirectButton(
            parent=self.map,
            relief=None,
            image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')),
            image_scale=(1.3, 1.1, 1.1),
            pos=buttonLoc,
            text=TTLocalizer.MapPageBackToPlayground,
            text_scale=TTLocalizer.MPsafeZoneButton,
            text_pos=(0, -0.02),
            command=self.backToSafeZone)
        self.goHomeButton = DirectButton(
            parent=self.map,
            relief=None,
            image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR'), guiButton.find('**/QuitBtn_UP')),
            image_scale=(0.66, 1.1, 1.1),
            pos=(0.15, 0, -.74),
            text=TTLocalizer.MapPageGoHome,
            text_scale=TTLocalizer.MPgoHomeButton,
            text_pos=(0, -0.02),
            command=self.goHome)

        # todo fix estates
        self.goHomeButton.setColorScale(Vec4(0.6, 0.6, 0.6, 1))
        self.goHomeButton['state'] = DGG.DISABLED

        self.goHomeButton.hide()
        guiButton.removeNode()
        self.hoodLabel = DirectLabel(
            parent=self.map,
            relief=None,
            pos=(-0.43, 0, -0.726),
            text='',
            text_scale=TTLocalizer.MPhoodLabel,
            text_pos=(0, 0),
            text_wordwrap=TTLocalizer.MPhoodLabelWordwrap)
        self.hoodLabel.hide()
        cloudModel = loader.loadModel('phase_3.5/models/gui/cloud')
        cloudImage = cloudModel.find('**/cloud')

        for hood in self.allZones:
            abbrev = base.cr.hoodMgr.getNameFromId(hood)
            fullname = base.cr.hoodMgr.getFullnameFromId(hood)
            hoodIndex = self.allZones.index(hood)
            label = DirectButton(
                parent=self.map,
                relief=None,
                pos=self.labelPosList[hoodIndex],
                pad=(0.2, 0.16),
                text=('', fullname, fullname),
                text_bg=Vec4(1, 1, 1, 0.4),
                text_scale=0.055,
                text_wordwrap=8,
                rolloverSound=None,
                clickSound=None,
                pressEffect=0,
                command=self.__buttonCallback,
                extraArgs=[hood],
                sortOrder=5)
            label.resetFrameSize()
            self.questsAvailableIcons.append(QuestsAvailablePoster(hood, parent=label, pos=(0.06, 0, 0.08), scale=.1, sortOrder=1))
            self.fishAvailableIcons.append(FishAvailablePoster(hood, parent=label, pos=(0.19, 0, 0.08), scale=.1, sortOrder=1))
            self.treasureAvailableIcons.append(TreasureAvailablePoster(hood, parent=label, pos=(-0.06, 0, 0.09), scale=.1, sortOrder=1))
            self.petsAvailableIcons.append(PetsAvailablePoster(hood, parent=label, pos=(-0.16, 0, 0.09), scale=.1, sortOrder=1))
            self.raceIcons.append(CanRacePoster(hood, parent=label, pos=(0.06, 0, 0.09), scale=.1, sortOrder=1))
            self.golfIcons.append(CanGolfPoster(hood, parent=label, pos=(0.06, 0, 0.09), scale=.1, sortOrder=1))
            label.bind(DGG.WITHIN, self.showTasksAvailableFrame, extraArgs=[hood, hoodIndex])
            label.bind(DGG.WITHOUT, self.hideTasksAvailableFrame, extraArgs=[hood, hoodIndex])
            self.labels.append(label)
            hoodClouds = []
            for cloudScale, cloudPos in zip(self.cloudScaleList[hoodIndex], self.cloudPosList[hoodIndex]):
                cloud = DirectFrame(
                    parent=self.map,
                    relief=None,
                    state=DGG.DISABLED,
                    image=cloudImage,
                    scale=(cloudScale[0], cloudScale[1], cloudScale[2]),
                    pos=(cloudPos[0], cloudPos[1], cloudPos[2]))
                cloud.hide()
                hoodClouds.append(cloud)

            self.clouds.append(hoodClouds)
            self.cloudAlphas.append(1)

        cloudModel.removeNode()
        self.resetFrameSize()
        return

    def showTasksAvailableFrame(self, hood, hoodIndex, pos):
        self.__hoverCallback(1, hoodIndex, pos)
        for questPoster, fishPoster, treasurePoster, petPoster, racePoster, golfPoster in zip(self.questsAvailableIcons, self.fishAvailableIcons, self.treasureAvailableIcons, self.petsAvailableIcons, self.raceIcons, self.golfIcons):
            if hood == questPoster.getHoodId():
                treasurePoster.show()
                # Only show if we need to.
                if hood == ToontownGlobals.OutdoorZone and base.localAvatar.slotData.get("golfing_logic"):
                    golfPoster.show()
                if hood == ToontownGlobals.GoofySpeedway and base.localAvatar.slotData.get("racing_logic"):
                    racePoster.show()
                if hood in FADoorCodes.PLAYGROUND_ZONES:
                    questPoster.show()
                    fishPoster.show()
                    petPoster.show()
            else:
                continue

    def hideTasksAvailableFrame(self, hood, hoodIndex, pos):
        self.__hoverCallback(0, hoodIndex, pos)
        for questPoster, fishPoster, treasurePoster, petPoster, racePoster, golfPoster in zip(self.questsAvailableIcons, self.fishAvailableIcons, self.treasureAvailableIcons, self.petsAvailableIcons, self.raceIcons, self.golfIcons):
            if hood == questPoster.getHoodId():
                treasurePoster.hide()
                # Only hide if we need to.
                if hood == ToontownGlobals.OutdoorZone and base.localAvatar.slotData.get("golfing_logic"):
                    golfPoster.hide()
                if hood == ToontownGlobals.GoofySpeedway and base.localAvatar.slotData.get("racing_logic"):
                    racePoster.hide()
                if hood in FADoorCodes.PLAYGROUND_ZONES:
                    questPoster.hide()
                    fishPoster.hide()
                    petPoster.hide()
            else:
                continue

    def updateTasksAvailableFrames(self):

        # Loop through all the posters
        for questPoster, fishPoster, treasurePoster, petPoster, racePoster, golfPoster in zip(self.questsAvailableIcons, self.fishAvailableIcons, self.treasureAvailableIcons, self.petsAvailableIcons, self.raceIcons, self.golfIcons):
            treasurePoster.hide()
            questPoster.hide()
            fishPoster.hide()
            petPoster.hide()
            racePoster.hide()
            golfPoster.hide()
            hoodId = questPoster.getHoodId()

            treasurePoster.update(base.localAvatar)
            golfPoster.update(base.localAvatar)
            racePoster.update(base.localAvatar)

            # Are there pets here?
            if petPoster.hoodId in ToontownGlobals.ZONE_TO_ID_TO_CHECK.keys():
                petPoster.update(base.localAvatar)

            # Can we fish here?
            if not fishPoster.isVisible(base.localAvatar):
                fishPoster.hide()
            elif not can_av_fish_at_zone(base.localAvatar, hoodId):
                fishPoster.showLocked()
            else:
                fishPoster.update(base.localAvatar)

            # Do we not have access to this hood?
            if hoodId in FADoorCodes.PLAYGROUND_ZONES:
                if FADoorCodes.ZONE_TO_ACCESS_CODE[hoodId] not in base.localAvatar.getAccessKeys():
                    questPoster.showLocked()
                else:
                    # Get the reward IDs from this playground
                    rewardIds = Quests.getRewardIdsFromHood(hoodId)
                    rewardIdCopy = rewardIds.copy()

                    # Filter out the rewards we can't get bc we already earned them
                    for reward in rewardIds:
                        apLocation = Quests.RewardDict.get(reward)[1]
                        if apLocation is not None:
                            if locations.LOCATION_NAME_TO_ID[apLocation] in base.localAvatar.getCheckedLocations():
                                rewardIdCopy.remove(reward)

                    # Now filter out the rewards we are working on
                    for quest in base.localAvatar.quests:
                        questId, fromNpcId, toNpcId, rewardId, toonProgress = quest
                        if rewardId in rewardIdCopy:
                            rewardIdCopy.remove(rewardId)

                    # Now we have a number that tells us how many quests this person can learn here
                    questPoster.showNumAvailable(len(rewardIdCopy))

    def unload(self):
        for labelButton in self.labels:
            labelButton.destroy()

        for questPoster, fishPoster, treasurePoster, petPoster in zip(self.questsAvailableIcons, self.fishAvailableIcons, self.treasureAvailableIcons, self.petsAvailableIcons):
            questPoster.destroy()
            fishPoster.destroy()
            treasurePoster.destroy()
            petPoster.destroy()
        self.questsAvailableIcons.clear()
        self.fishAvailableIcons.clear()
        self.treasureAvailableIcons.clear()
        self.petsAvailableIcons.clear()

        del self.labels
        del self.clouds
        self.safeZoneButton.destroy()
        self.goHomeButton.destroy()
        ShtikerPage.ShtikerPage.unload(self)

    def enter(self):
        ShtikerPage.ShtikerPage.enter(self)
        try:
            zone = base.cr.playGame.getPlace().getZoneId()
        except:
            zone = 0

        self.updateTasksAvailableFrames()

        if base.localAvatar.lastHood >= ToontownGlobals.BossbotHQ:
            self.safeZoneButton['text'] = TTLocalizer.MapPageBackToCogHQ
        else:
            self.safeZoneButton['text'] = TTLocalizer.MapPageBackToPlayground
        if zone and ZoneUtil.isPlayground(zone) or self.book.safeMode:
            self.safeZoneButton.hide()
        else:
            self.safeZoneButton.show()
        if base.cr.playGame.getPlaceId() == ToontownGlobals.MyEstate and base.cr.playGame.hood.loader.atMyEstate() or self.book.safeMode:
            self.goHomeButton.hide()
        elif base.housingEnabled:
            self.goHomeButton.show()
        if base.cr.playGame.getPlaceId() == ToontownGlobals.MyEstate:
            if base.cr.playGame.hood.loader.atMyEstate():
                self.hoodLabel['text'] = TTLocalizer.MapPageYouAreAtHome
                self.hoodLabel.show()
            else:
                avatar = base.cr.identifyAvatar(base.cr.playGame.hood.loader.estateOwnerId)
                if avatar:
                    avName = avatar.getName()
                    self.hoodLabel['text'] = TTLocalizer.MapPageYouAreAtSomeonesHome % TTLocalizer.GetPossesive(avName)
                    self.hoodLabel.show()
        elif zone:
            hoodName = ToontownGlobals.hoodNameMap.get(ZoneUtil.getCanonicalHoodId(zone), ('',))[-1]
            streetName = ToontownGlobals.StreetNames.get(ZoneUtil.getCanonicalBranchZone(zone), ('',))[-1]
            if hoodName:
                self.hoodLabel['text'] = TTLocalizer.MapPageYouAreHere % (hoodName, streetName)
                self.hoodLabel.show()
            else:
                self.hoodLabel.hide()
        else:
            self.hoodLabel.hide()
        safeZonesVisited = base.localAvatar.hoodsVisited
        hoodTeleportList = base.localAvatar.getTeleportAccess()
        for hood in self.allZones:
            idx = self.allZones.index(hood)
            label = self.labels[idx]
            clouds = self.clouds[idx]

            # Set cloud visibility.
            if hood in safeZonesVisited:
                label['text_fg'] = (0, 0, 0, 1)
                for cloud in clouds:
                    cloud.hide()
            else:
                label['text_fg'] = (0, 0, 0, 0.65)
                for cloud in clouds:
                    cloud.show()

            # Set label text.
            label.show()
            fullname = base.cr.hoodMgr.getFullnameFromId(hood)
            if hood in hoodTeleportList:
                text = TTLocalizer.MapPageGoTo % fullname
                label['text'] = ('', text, text)
            else:
                label['text'] = ('', fullname, fullname)

            # Set cloud opacity.
            if hood in hoodTeleportList:
                self.cloudAlphas[idx] = 0.5
            else:
                self.cloudAlphas[idx] = 1.0
            cloudAlpha = self.cloudAlphas[idx]
            for cloud in clouds:
                cloud.setColor(1, 1, 1, cloudAlpha)

    def exit(self):
        ShtikerPage.ShtikerPage.exit(self)

    def backToSafeZone(self):
        self.doneStatus = {'mode': 'teleport',
         'hood': base.localAvatar.lastHood}
        messenger.send(self.doneEvent)

    def goHome(self):
        return  # todo fix estates
        if base.config.GetBool('want-qa-regression', 0):
            self.notify.info('QA-REGRESSION: VISITESTATE: Visit estate')
        self.doneStatus = {'mode': 'gohome',
         'hood': base.localAvatar.lastHood}
        messenger.send(self.doneEvent)

    def __buttonCallback(self, hood):
        if hood in base.localAvatar.getTeleportAccess() and hood in base.cr.hoodMgr.getAvailableZones():
            base.localAvatar.sendUpdate('checkTeleportAccess', [hood])
            self.doneStatus = {'mode': 'teleport',
             'hood': hood}
            messenger.send(self.doneEvent)

    def __hoverCallback(self, inside, hoodIndex, pos):
        try:
            alpha = PythonUtil.choice(inside, 0.25, self.cloudAlphas[hoodIndex])
            clouds = self.clouds[hoodIndex]
        except ValueError:
            alpha = 1.0
            clouds = []

        for cloud in clouds:
            cloud.setColor((1,
             1,
             1,
             alpha))
