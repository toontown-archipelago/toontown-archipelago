import typing

from direct.gui.DirectGui import *
from panda3d.core import TextNode

from libotp import CFSpeech, CFTimeout
from toontown.friends.OnlineToon import OnlineToon
from toontown.groups.GroupMemberStruct import GroupMemberStruct

if typing.TYPE_CHECKING:
    from toontown.groups.DistributedGroup import DistributedGroup


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

    def __init__(self, group: "DistributedGroup", **kw):

        self.group: "DistributedGroup" = group

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
        readyStatusTexture = model.find('**/ready-final')

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
            # Bind a special hover event to this button to handle the sub option hiding/showing.
            button.bind(DGG.ENTER, self.__onHoverRow, extraArgs=[button])
            self.rows.append(button)

        # Cleanup.
        model.removeNode()

    def updateMembers(self, members: list[GroupMemberStruct]):
        self.clearMembers()
        for index, member in enumerate(members):
            if index >= GroupInterface.MEMBER_ROWS:
                return
            row = self.rows[index]
            row.setAvatar(member)
            row.updateStatus(member.status)
            row.updateStateFromGroup(self.group)

    def clearMembers(self):
        for row in self.rows:
            row.clearAvatar()
            row.updateStateFromGroup(self.group)

    """
    Button Handlers
    """

    def __onGameSettingsClicked(self):
        base.localAvatar.setChatAbsolute("I WANT TO CHANGE THE GAME!!!", CFSpeech | CFTimeout)

    def __onLeaveClicked(self):
        """
        Called via a button press when the leave group button is pressed.
        When this button is clicked, we are essentially trying to kick ourselves from the group.
        """
        base.localAvatar.getGroupManager().attemptKick(base.localAvatar.getDoId())

    def __onPlayClicked(self):
        """
        Called via a button press when the start game button is pressed.
        """
        base.localAvatar.getGroupManager().attemptStart()

    def __onHoverRow(self, row, event=None):
        # Hide every single row.
        for other in self.rows:
            other.hideOptions()
        # Show this one.
        row.showOptions()

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
        'relief': DGG.FLAT,
        'scale': BUTTON_SCALE,
        'text': "Waiting for toon...",
        'text_align': TextNode.ALeft,
        'text_scale': TEXT_SCALE,
        'text_pos': (0, -.005),
        'textMayChange': 1,
        'frameSize': (0, .391, -.015, .015),
        'frameColor': (1, 1, 1, 0)
    }

    HOVER_FRAME_COLOR = (.6, .8, 1, .2)

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
        self.promoteButton = DirectButton(parent=self, relief=None, scale=GroupInterfaceMemberButton.SUBOPTION_BUTTON_SCALE, pos=(.34, 0, 0), image=promoteTexture, command=self.__onPromoteClicked)
        self.switchButton = DirectButton(parent=self, relief=None, scale=GroupInterfaceMemberButton.SUBOPTION_BUTTON_SCALE, pos=(.305, 0, 0), image=switchTexture, command=self.__onSwitchClicked)
        self.kickButton = DirectButton(parent=self, relief=None, scale=GroupInterfaceMemberButton.SUBOPTION_BUTTON_SCALE, pos=(.375, 0, 0), image=kickTexture, command=self.__onKickClicked)
        self.statusLabel = DirectButton(parent=self, relief=None, scale=GroupInterfaceMemberButton.SUBOPTION_BUTTON_SCALE * .65, pos=(-.02, 0, 0), image=self._notReadyTexture)
        self.hideOptions()

        # Now bind hover events to the buttons so the user knows what they do.
        self.__addTooltip(self.promoteButton, HoverableTooltip(self.promoteButton, 'promote-node', "Promote", (.8, .6, .1, 1)))
        self.__addTooltip(self.switchButton, HoverableTooltip(self.switchButton, 'promote-node', "Switch", (.1, .9, .9, 1)))
        self.__addTooltip(self.kickButton, HoverableTooltip(self.kickButton, 'kick-node', "Kick", (.9, .3, .3, 1)))

        # Initialize state. (The toon that is bound to this button)
        self.avatar: OnlineToon | None = None
        self.avatarID = None
        self['state'] = DGG.DISABLED
        self.updateStatus(GroupInterfaceMemberButton.STATUS_EMPTY)

    def setAvatar(self, member: GroupMemberStruct):
        onlineToon = base.cr.onlinePlayerManager.getOnlineToon(member.avId)
        name = f"??? - {member.avId}"
        if onlineToon is not None:
            name = onlineToon.name
        self.avatar = onlineToon
        self.avatarID = member.avId
        self['text_fg'] = (.25, .25, .6, 1)
        self['state'] = DGG.NORMAL
        self['text'] = name

    def clearAvatar(self):
        self.avatar = None
        self.avatarID = None
        self['state'] = DGG.DISABLED
        self['text'] = GroupInterfaceMemberButton.DEFAULT_TEXT
        self.updateStatus(GroupInterfaceMemberButton.STATUS_EMPTY)
        self['text_fg'] = (.6, .6, .6, .6)

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

    def updateStateFromGroup(self, group):

        if self.avatarID is None:
            self.hideOptions()
            self.updateStatus(GroupInterfaceMemberButton.STATUS_EMPTY)
            return

        if group.getLeader() == self.avatarID:
            self.updateStatus(GroupInterfaceMemberButton.STATUS_LEADER)

        # Are we the leader of the group? we have full control over everything except promoting ourselves.
        if group.getLeader() == base.localAvatar.getDoId():
            self.promoteButton['state'] = DGG.DISABLED if self.avatarID == group.getLeader() else DGG.NORMAL
            self.promoteButton.setColorScale((.5, .5, .5, 1) if self.avatarID == group.getLeader() else (1, 1, 1, 1))
            self.switchButton['state'] = DGG.NORMAL
            self.switchButton.setColorScale(1, 1, 1, 1)
            self.kickButton['state'] = DGG.NORMAL
            self.kickButton.setColorScale(1, 1, 1, 1)
            return

        # We are a normal member of the group. Only allow the switch button and kick button ourselves.
        self.promoteButton['state'] = DGG.DISABLED
        self.promoteButton.setColorScale(.5, .5, .5, 1)
        self.switchButton['state'] = DGG.DISABLED if self.avatarID != base.localAvatar.getDoId() else DGG.NORMAL
        self.switchButton.setColorScale((.5, .5, .5, 1) if self.avatarID != base.localAvatar.getDoId() else (1, 1, 1, 1))
        self.kickButton['state'] = DGG.DISABLED if self.avatarID != base.localAvatar.getDoId() else DGG.NORMAL
        self.kickButton.setColorScale((.5, .5, .5, 1) if self.avatarID != base.localAvatar.getDoId() else (1, 1, 1, 1))

    def hideOptions(self):
        self.promoteButton.hide()
        self.kickButton.hide()
        self.switchButton.hide()
        self['frameColor'] = (1, 1, 1, 0)

    def showOptions(self):
        self.promoteButton.show()
        self.kickButton.show()
        self.switchButton.show()
        self['frameColor'] = GroupInterfaceMemberButton.HOVER_FRAME_COLOR

    """
    Button Handlers
    """

    def __onAvatarClicked(self):
        # We need to resolve a handler to dispatch over the messenger. This either needs to be a DisToon or a friend handle.
        if None in (self.avatar, self.avatarID):
            return

        handle = base.cr.getDo(self.avatarID)
        if handle is None:
            handle = self.avatar.handle()

        messenger.send('clickedNametag', [handle])

    def __onPromoteClicked(self):
        if self.avatar is not None:
            base.localAvatar.getGroupManager().attemptPromote(self.avatarID)

    def __onSwitchClicked(self):
        pass

    def __onKickClicked(self):
        if self.avatar is not None:
            base.localAvatar.getGroupManager().attemptKick(self.avatarID)

    def __addTooltip(self, button, tooltip):
        def __show(_):
            tooltip.show()

        def __hide(_):
            tooltip.hide()

        button.bind(DGG.ENTER, __show)
        button.bind(DGG.EXIT, __hide)

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


class HoverableTooltip:
    def __init__(self, parent, name: str, text: str, border: tuple = (1, 1, 1, 1)):

        # The text that describes modifiers
        self.modifiers_desc = TextNode(name)
        self.modifiers_desc.setText(text)
        self.modifiers_desc.setAlign(TextNode.ACenter)
        self.modifiers_desc.setFrameColor(border)
        self.modifiers_desc.setFrameAsMargin(0.3, 0.3, 0.15, 0.15)
        self.modifiers_desc.setCardColor(.2, .2, .2, .75)
        self.modifiers_desc.setCardAsMargin(0.28, 0.28, 0.14, 0.14)
        self.modifiers_desc.setCardDecal(True)
        self.modifiers_desc.setShadow(0.05, 0.05)
        self.modifiers_desc.setShadowColor(0, 0, 0, 1)
        self.modifiers_desc.setTextColor(1, 1, 1, 1)
        self.modifiers_desc.setTextScale(1)
        self.modifiers_desc_path = parent.attachNewNode(self.modifiers_desc)
        self.modifiers_desc_path.setScale(1)
        self.modifiers_desc_path.setPos(0, 0, 1)
        self.modifiers_desc_path.hide()

    def hide(self):
        self.modifiers_desc_path.hide()

    def show(self):
        self.modifiers_desc_path.show()
