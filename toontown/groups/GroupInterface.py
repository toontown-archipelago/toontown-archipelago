from direct.gui.DirectGui import *
from panda3d.core import TextNode

from libotp import CFSpeech, CFTimeout


class GroupInterface(DirectFrame):

    GUI_MODEL_PATH = 'phase_14/models/gui/boarding-gui'

    OPTS = {
        'pos': (.38, 0, -.05),
        'scale': 1.3,
        'image_scale': (.5, 1, 1),
        'frameSize': (-.24, .24, -.49, .49),
        'frameColor': (1, 1, 1, 0)
    }

    GAME_OPTIONS_BUTTON_STRETCH_FACTOR = 3.8
    GAME_OPTIONS_BUTTON_TEXT_SCALE = .5

    START_BUTTON_STRETCH_FACTOR = 2.7826
    START_BUTTON_TEXT_SCALE = .6

    MEMBER_ROWS = 16

    def __init__(self, **kw):

        # Load in the elements we need.
        model = loader.loadModel(GroupInterface.GUI_MODEL_PATH)

        # Find the textures we need.
        frameTexture = model.find('**/group-frame')

        selectGameTexture = model.find('**/button-selectgame')
        playGameTexture = model.find('**/button-start')
        leaveTexture = model.find('**/button-leavedisband')

        promoteTexture = model.find('**/button-promote')
        switchTeamTexture = model.find('**/button-switch')
        kickTexture = model.find('**/button-kick')

        leaderTexture = model.find('**/status-leader')
        notReadyStatusTexture = model.find('**/status-notready')
        readyStatusTexture = model.find('**/status-ready')

        # Apply any keywords that our highest level frame needs.
        kw.update(GroupInterface.OPTS)
        kw['image'] = frameTexture
        kw['parent'] = base.a2dLeftCenter

        # Initialize the underlying frame.
        super().__init__(**kw)
        self.initialiseoptions(GroupInterface)

        # Create any other elements that should be on this frame immediately when it is created.
        self.gameSettingsButton = DirectButton(parent=self, text='Crane Game', text_pos=(0, -.12), text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1), text_scale=(GroupInterface.GAME_OPTIONS_BUTTON_TEXT_SCALE / GroupInterface.GAME_OPTIONS_BUTTON_STRETCH_FACTOR, GroupInterface.GAME_OPTIONS_BUTTON_TEXT_SCALE), text_align=TextNode.ABoxedCenter, scale=(.115*GroupInterface.GAME_OPTIONS_BUTTON_STRETCH_FACTOR, .115, .115), relief=None, pos=(0, 0, -.294),image=selectGameTexture, command=self.__onGameSettingsClicked)
        self.leaveButton = DirectButton(parent=self, scale=.115, relief=None, pos=(.16, 0, -.413), image=leaveTexture, command=self.__onLeaveClicked)
        self.startButton = DirectButton(parent=self, text='Start!', text_pos=(0, -.15), text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1), text_scale=(GroupInterface.START_BUTTON_TEXT_SCALE / GroupInterface.START_BUTTON_STRETCH_FACTOR, GroupInterface.START_BUTTON_TEXT_SCALE), text_align=TextNode.ABoxedCenter, scale=(.115 * GroupInterface.START_BUTTON_STRETCH_FACTOR, .115, .115), relief=None, pos=(-.06, 0, -.413), image=playGameTexture, command=self.__onPlayClicked)
        self.rows: list[GroupInterfaceMemberButton] = []
        for i in range(GroupInterface.MEMBER_ROWS):
            pos = (GroupInterfaceMemberButton.X_ORIGIN, 0, GroupInterfaceMemberButton.Y_ORIGIN + GroupInterfaceMemberButton.Y_PADDING * i)
            textures = (promoteTexture, switchTeamTexture, kickTexture,
                        leaderTexture, readyStatusTexture, notReadyStatusTexture)
            button = GroupInterfaceMemberButton(textures, parent=self, pos=pos)
            self.rows.append(button)

        # Cleanup.
        model.removeNode()

    def updateMembers(self, members: list):
        for index, member in enumerate(members):
            if index >= GroupInterface.MEMBER_ROWS:
                return
            self.rows[index].setAvatar(member)

    def clearMembers(self):
        for row in self.rows:
            row.clearAvatar()

    """
    Button Handlers
    """

    def __onGameSettingsClicked(self):
        base.localAvatar.setChatAbsolute("I WANT TO CHANGE THE GAME!!!", CFSpeech | CFTimeout)

    def __onLeaveClicked(self):
        """
        Called via a button press when the leave group button is pressed.
        """
        base.localAvatar.setChatAbsolute('I WANT TO LEAVE MY GROUP!!!', CFSpeech | CFTimeout)

    def __onPlayClicked(self):
        """
        Called via a button press when the start game button is pressed.
        """
        base.localAvatar.setChatAbsolute('I WANT TO PLAY THE VIDEO GAME!!!', CFSpeech | CFTimeout)

    """
    Boilerplate
    """

    def destroy(self):
        super().destroy()
        self.gameSettingsButton.destroy()
        self.leaveButton.destroy()
        self.startButton.destroy()
        for button in self.rows:
            button.destroy()
        self.rows.clear()


class GroupInterfaceMemberButton(DirectButton):
    """
    Represents a player row to be displayed in the group interface.
    There should be 16 of these rows that can fit into the entire frame.
    """

    DEFAULT_TEXT = "Waiting for toon...."

    BUTTON_SCALE = 1
    TEXT_SCALE = .025

    OPTS = {
        'relief': None,
        'scale': BUTTON_SCALE,
        'text': "Waiting for toon...",
        'text_align': TextNode.ALeft,
        'text_scale': TEXT_SCALE,
        'text_pos': (0, -.005),
        'textMayChange': 1,
        'frameSize': (0, .3, -.015, .015)
    }

    X_ORIGIN = -0.18
    Y_ORIGIN = .31
    Y_PADDING = -.035

    SUBOPTION_BUTTON_SCALE = .035

    STATUS_EMPTY = 0
    STATUS_LEADER = 1
    STATUS_READY = 2
    STATUS_UNREADY = 3

    def __init__(self, textures: tuple, **kw):

        # Apply any keywords that our highest level button needs.
        kw.update(GroupInterfaceMemberButton.OPTS)
        kw['command'] = self.__onAvatarClicked

        # Initialize the underlying button.
        super().__init__(**kw)
        self.initialiseoptions(GroupInterfaceMemberButton)

        # Create the 3 buttons that interact with this button and the status label.
        promoteTexture, switchTexture, kickTexture, leaderTexture, readyTexture, notReadyTexture = textures
        # We need to hang on to the status textures so we can switch to and from them.
        self._leaderTexture = leaderTexture
        self._readyTexture = readyTexture
        self._notReadyTexture = notReadyTexture
        self.promoteButton = DirectButton(parent=self, relief=None, scale=GroupInterfaceMemberButton.SUBOPTION_BUTTON_SCALE, pos=(.305, 0, 0), image=promoteTexture, command=self.__onPromoteClicked)
        self.switchButton = DirectButton(parent=self, relief=None, scale=GroupInterfaceMemberButton.SUBOPTION_BUTTON_SCALE, pos=(.34, 0, 0), image=switchTexture, command=self.__onSwitchClicked)
        self.kickButton = DirectButton(parent=self, relief=None, scale=GroupInterfaceMemberButton.SUBOPTION_BUTTON_SCALE, pos=(.375, 0, 0), image=kickTexture, command=self.__onKickClicked)
        self.statusLabel = DirectButton(parent=self, relief=None, scale=GroupInterfaceMemberButton.SUBOPTION_BUTTON_SCALE * .65, pos=(-.02, 0, 0), image=self._notReadyTexture)

        # Initialize state. (The toon that is bound to this button)
        self.avatar = None
        self.avatarID = None
        self['state'] = DGG.DISABLED

    def setAvatar(self, avatar):
        self.avatar = avatar
        self.avatarID = avatar.getDoId()
        self['state'] = DGG.NORMAL
        self['text'] = avatar.getName()

    def clearAvatar(self):
        self.avatar = None
        self.avatarID = None
        self['state'] = DGG.DISABLED
        self['text'] = GroupInterfaceMemberButton.DEFAULT_TEXT

    def updateStatus(self, code):
        self.statusLabel.setColorScale(1, 1, 1, 1)
        match code:
            case GroupInterfaceMemberButton.STATUS_READY:
                self.statusLabel['image'] = self._readyTexture
            case GroupInterfaceMemberButton.STATUS_UNREADY:
                self.statusLabel['image'] = self._notReadyTexture
            case GroupInterfaceMemberButton.STATUS_LEADER:
                self.statusLabel['image'] = self._leaderTexture
            case GroupInterfaceMemberButton.STATUS_EMPTY:
                self.statusLabel['image'] = self._notReadyTexture
                self.statusLabel.setColorScale(.25, .25, .25, .75)

    """
    Button Handlers
    """

    def __onAvatarClicked(self):
        base.localAvatar.setChatAbsolute(f"I want to view {self.avatarID}'s toon.", CFSpeech | CFTimeout)

    def __onPromoteClicked(self):
        base.localAvatar.setChatAbsolute(f"I want to promote {self.avatarID}.", CFSpeech | CFTimeout)

    def __onSwitchClicked(self):
        base.localAvatar.setChatAbsolute(f"I want to switch {self.avatarID}'s team.", CFSpeech | CFTimeout)

    def __onKickClicked(self):
        base.localAvatar.setChatAbsolute(f"I want to kick {self.avatarID}.", CFSpeech | CFTimeout)

    """
    Boilerplate
    """

    def destroy(self):
        self.avatar = None
        self.avatarID = None
        self.promoteButton.destroy()
        self.switchButton.destroy()
        self.kickButton.destroy()
        self.statusLabel.destroy()
        super().destroy()
