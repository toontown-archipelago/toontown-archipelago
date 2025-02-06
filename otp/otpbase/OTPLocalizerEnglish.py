import string
from otp.otpbase.OTPLocalizerEnglishProperty import *
from .OTPGlobals import *

lTheBrrrgh = 'The Brrrgh'
lDaisyGardens = 'Daisy Gardens'
lDonaldsDock = "Donald's Dock"
lDonaldsDreamland = "Donald's Dreamland"
lMinniesMelodyland = "Minnie's Melodyland"
lToontownCentral = 'Toontown Central'
lGoofySpeedway = 'Goofy Speedway'
lOutdoorZone = "Chip 'n Dale's Acorn Acres"
lGolfZone = "Chip 'n Dale's MiniGolf"
lCancel = 'Cancel'
lClose = 'Close'
lOK = 'OK'
lNext = 'Next'
lNo = 'No'
lQuit = 'Quit'
lYes = 'Yes'
Cog = 'Cog'
Cogs = 'Cogs'
DialogOK = lOK
DialogCancel = lCancel
DialogYes = lYes
DialogNo = lNo
DialogDoNotShowAgain = 'Do Not\nShow Again'
WhisperNoLongerFriend = '%s left your friends list.'
WhisperNowSpecialFriend = '%s is now your True Friend!'
WhisperComingToVisit = '%s is coming to visit you.'
WhisperFailedVisit = '%s tried to visit you.'
WhisperTargetLeftVisit = '%s has gone somewhere else. Try again!'
WhisperGiveupVisit = "%s couldn't find you because you're moving around!"
WhisperIgnored = '%s is ignoring you!'
TeleportGreeting = 'Hi, %s.'
WhisperFriendComingOnline = '%s is coming online!'
WhisperFriendLoggedOut = '%s has logged out.'
WhisperPlayerOnline = '%s logged into %s'
WhisperPlayerOffline = '%s is offline.'
WhisperUnavailable = 'That player is no longer available for whispers.'
DialogSpecial = 'ooo'
DialogExclamation = '!'
DialogQuestion = '?'
ChatInputNormalSayIt = 'Say It'
ChatInputNormalCancel = lCancel
ChatInputNormalWhisper = 'Whisper'
ChatInputWhisperLabel = 'To %s'
SCEmoteNoAccessMsg = 'You do not have access\nto this emotion yet.'
SCEmoteNoAccessOK = lOK
ParentLogin = 'Parent Login'
ParentPassword = 'Parent Account Password'
ChatGarblerDefault = ['blah']
ChatManagerChat = 'Chat'
ChatManagerWhisperTo = 'Whisper to:'
ChatManagerWhisperToName = 'Whisper To:\n%s'
ChatManagerCancel = lCancel
ChatManagerWhisperOffline = '%s is offline.'
OpenChatWarning = 'To become True Friends with somebody, click on them, and select "True Friends" from the detail panel.\n\nSpeedChat Plus can also be enabled, which allow users to chat by typing words found in the SpeedChat Plus dictionary.\n\nTo activate these features or to learn more, exit Toontown and then click on Membership and select Manage Account.  Log in to edit your "Community Settings."\n\nIf you are under 18, you need a Parent Account to manage these settings.'
OpenChatWarningOK = lOK
UnpaidChatWarning = 'Once you have subscribed, you can use this button to chat with your friends using the keyboard.  Until then, you should chat with other Toons using SpeedChat.'
UnpaidChatWarningPay = 'Subscribe'
UnpaidChatWarningContinue = 'Continue Free Trial'
PaidNoParentPasswordWarning = 'Use this button to chat with your friends by using the keyboard, enable it through your Account Manager on the Toontown Web site. Until then, you can chat by using SpeedChat.'
UnpaidNoParentPasswordWarning = 'This is for SpeedChat Plus, which allows users to chat by typing words found in the SpeedChat Plus dictionary. To activate this feature, exit Toontown and click on Membership. Select Manage Account and log in to edit your "Community Settings." If you are under 18, you need a Parent Account to manage these settings.'
PaidNoParentPasswordWarningSet = 'Update Chat Settings'
PaidNoParentPasswordWarningContinue = 'Continue Playing Game'
PaidParentPasswordUKWarning = 'Once you have Enabled Chat, you can enable this button to chat with your friends using the keyboard. Until then, you should chat with other Toons using SpeedChat.'
PaidParentPasswordUKWarningSet = 'Enable Chat Now!'
PaidParentPasswordUKWarningContinue = 'Continue Playing Game'
NoSecretChatWarningTitle = 'Parental Controls'
NoSecretChatWarning = 'To chat with a friend, the True Friends feature must first be enabled.  Kids, have your parent visit the Toontown Web site to learn about True Friends.'
RestrictedSecretChatWarning = 'To get or enter a True Friend Code, log in with the Parent Account. You can disable this prompt by changing your True Friends options.'
NoSecretChatWarningOK = lOK
NoSecretChatWarningCancel = lCancel
NoSecretChatWarningWrongPassword = "That's not the correct Parent Account.  Please log in with the Parent Account that is linked to this account."
NoSecretChatAtAllTitle = 'Open Chat With True Friends'
NoSecretChatAtAll = 'Open Chat with True Friends allows real-life friends to chat openly with each other by means of a True Friend Code that must be shared outside of the game.\n\nTo activate these features or to learn more, exit Toontown and then click on Membership and select Manage Account. Log in to edit your "Community Settings." If you are under 18, you need a Parent Account to manage these settings.'
NoSecretChatAtAllAndNoWhitelistTitle = 'Chat button'
NoSecretChatAtAllAndNoWhitelist = 'You can use the blue Chat button to communicate with other Toons by using Speechat Plus or Open Chat with True Friends.\n\nSpeedchat Plus is a form of type chat that allows users to communicate by using the SpeedChat Plus dictionary.\n\nOpen Chat with True Friends allows real-life friends to chat openly with each other by means of a True Friend Code that must be shared outside of the game.\n\nTo activate these features or to learn more, exit Toontown and then click on Membership and select Manage Account.  Log in to edit your "Community Settings." If you are under 18, you need a Parent Account to manage these settings.'
NoSecretChatAtAllOK = lOK
ChangeSecretFriendsOptions = 'Change True Friends Options'
ChangeSecretFriendsOptionsWarning = '\nPlease enter the Parent Account Password to change your True Friends options.'
ActivateChatTitle = 'True Friends Options'
WhisperToFormat = 'To %s %s'
WhisperToFormatName = 'To %s'
WhisperFromFormatName = '%s whispers'
ThoughtOtherFormatName = '%s thinks'
ThoughtSelfFormatName = 'You think'
from panda3d.core import TextProperties, TextPropertiesManager

shadow = TextProperties()
shadow.setShadow(-0.025, -0.025)
shadow.setShadowColor(0, 0, 0, 1)
TextPropertiesManager.getGlobalPtr().setProperties('shadow', shadow)
red = TextProperties()
red.setTextColor(1, 0, 0, 1)
TextPropertiesManager.getGlobalPtr().setProperties('red', red)
green = TextProperties()
green.setTextColor(0, 1, 0, 1)
TextPropertiesManager.getGlobalPtr().setProperties('green', green)
yellow = TextProperties()
yellow.setTextColor(1, 1, 0, 1)
TextPropertiesManager.getGlobalPtr().setProperties('yellow', yellow)
measly_brown = TextProperties()
measly_brown.setTextColor(0.373, 0.31, 0.161, 1.0)
TextPropertiesManager.getGlobalPtr().setProperties('measly_brown', measly_brown)
freaky_orange = TextProperties()
freaky_orange.setTextColor(0.886, 0.467, 0.267, 1.0)
TextPropertiesManager.getGlobalPtr().setProperties('freaky_orange', freaky_orange)
midgreen = TextProperties()
midgreen.setTextColor(0.2, 1, 0.2, 1)
TextPropertiesManager.getGlobalPtr().setProperties('midgreen', midgreen)
blue = TextProperties()
blue.setTextColor(0, 0, 1, 1)
TextPropertiesManager.getGlobalPtr().setProperties('blue', blue)
white = TextProperties()
white.setTextColor(1, 1, 1, 1)
TextPropertiesManager.getGlobalPtr().setProperties('white', white)
black = TextProperties()
black.setTextColor(0, 0, 0, 1)
TextPropertiesManager.getGlobalPtr().setProperties('black', black)
grey = TextProperties()
grey.setTextColor(0.5, 0.5, 0.5, 1)
TextPropertiesManager.getGlobalPtr().setProperties('grey', grey)
ActivateChat = "True Friends allows one member to chat with another member only by means of a True Friend Code that must be communicated outside of the game. True Friends is not moderated or supervised.\n\nPlease choose one of Toontown's True Friends options:\n\n      \x01shadow\x01No True Friends\x02 - Ability to make True Friends is disabled.\n      This offers the highest level of control.\n\n      \x01shadow\x01Restricted True Friends\x02 - Requires the Parent Account Password to make\n      each new True Friend.\n\n      \x01shadow\x01Unrestricted True Friends\x02 - Once enabled with the Parent Account Password,\n      it is not required to supply the Parent Account Password to make each new\n      True Friend. \x01red\x01This option is not recommended for children under 13.\x02\n\n\n\n\n\n\nBy enabling the True Friends feature, you acknowledge that there are some risks inherent in the True Friends feature and that you have been informed of, and agree to accept, any such risks."
ActivateChatYes = 'Update'
ActivateChatNo = lCancel
ActivateChatMoreInfo = 'More Info'
ActivateChatPrivacyPolicy = 'Privacy Policy'
ActivateChatPrivacyPolicy_Button1A = 'Version 1'
ActivateChatPrivacyPolicy_Button1K = 'Version 1'
ActivateChatPrivacyPolicy_Button2A = 'Version 2'
ActivateChatPrivacyPolicy_Button2K = 'Version 2'
PrivacyPolicyText_1A = [' ']
PrivacyPolicyText_1K = [' ']
PrivacyPolicyText_2A = [' ']
PrivacyPolicyText_2K = [' ']
PrivacyPolicyText_Intro = [' ']
PrivacyPolicyClose = lClose
SecretFriendsInfoPanelOk = lOK
SecretFriendsInfoPanelClose = lClose
SecretFriendsInfoPanelText = [
    '\nThe Open Chat with True Friends Feature\n\nThe Open Chat with True Friends feature enables a member to chat directly with another member within Toontown Online (the "Service") once the members establish a True Friends connection. Here is a detailed description of the process of creating an Open Chat with True Friends connection between members whom we will call "John" and "Little Cat."\n1. First, John requests a True Friend Code (described below) from within the Service.\n',
    "\nThen, John's True Friend Code is given to Little Cat outside of the Service. (John's True Friend Code may be communicated to Little Cat either directly by John, or indirectly through John's disclosure of the True Friend Code to another person.)\nLittle Cat submits John's True Friend Code to the Service within 48 hours of the time that John requested the True Friend Code from the Service.\n5. The Service then notifies Little Cat that John has become Little Cat's True Friend.  The Service similarly notifies John that Little Cat has become John's True Friend.\nJohn and Little Cat can now open chat directly with each other until either one chooses to terminate the other as a True Friend.",
    "\nTrue Friends feature by going to the Account Options area within the Service and following the steps set forth there.\n\nA True Friend Code is a computer-generated random code assigned to a particular member. The True Friend Code must be used to activate a True Friend connection within 48 hours of the time that the member requests the True Friend Code; otherwise, the True Friend Code expires and cannot be used.  Moreover, a single True Friend Code can only be used to establish one True Friend connection.  To make additional True Friend connections, a member must request an additional True Friend Code for each additional True Friend.\n\nTrue Friendships do not transfer.  For example, if Little Cat becomes a True Friend of John, and John becomes a True Friend of Jesse, Little Cat does not automatically become Jesse's True Friend.  In order for Little Cat and Jesse to\n",
    '\nbecome True Friends, one of them must request a new True Friend Code from the Service and communicate it to the other.\n\nTrue Friends communicate with one another in a free-form interactive open chat.  The content of this chat is directly entered by the participating member and is processed through the Service, which is operated by independent server hosters.  While we advise members not to exchange personal information such as first and last names, e-mail addresses, postal addresses, or phone numbers while using Open Chat with True Friends, we cannot guarantee that such exchanges of personal information will not happen. Although the True Friends chat is automatically filtered for most bad words, Open Chat with True Friends may be moderated, and server operators reserve the right to moderate any part of the Service that they,\n',
    "\nin their sole and absolute discretion, deem necessary. However, because Open Chat with True Friends will not always be moderated, we strongly encourage parents to supervise their child or children while they play in the Service. By enabling the Open Chat with True Friends feature, the user acknowledges that there are some risks inherent in the Open Chat with True Friends feature and that they have been informed of, and agree to accept, any such risks, whether foreseeable or otherwise. \n\nToontown Online does not use the content of True Friends chat for any purpose other than communicating that content to the member's True Friend, and does not disclose that content to any third party except: (1) if required by law, for example, to comply with a court order or subpoena;\n",
    "\nor, (2) to protect the safety and security of Members of the Service and the Service itself. In accordance with the Children's Online Privacy Protection Act, we are prohibited from conditioning, and do not condition, a child's participation in any activity (including Open Chat with True Friends) on the child's disclosing more personal information than is reasonably necessary to participate in such activity. By enabling the Open Chat with True Friends feature, you acknowledge that there are some risks inherent in the ability of members to open chat with one another through the Open Chat with True Friends feature, and that you have been informed of, and agree to accept, any such risks, whether foreseeable or otherwise.\n"]
LeaveToPay = 'Click Purchase to exit the game and buy a Membership'
LeaveToPayYes = 'Purchase'
LeaveToPayNo = lCancel
LeaveToSetParentPassword = 'In order to set parent account password, the game will exit to the Toontown website.'
LeaveToSetParentPasswordYes = 'Set Password'
LeaveToSetParentPasswordNo = lCancel
LeaveToEnableChatUK = 'In order to enable chat, the game will exit to the Toontown website.'
LeaveToEnableChatUKYes = 'Enable Chat'
LeaveToEnableChatUKNo = lCancel
ChatMoreInfoOK = lOK
SecretChatDeactivated = 'The "True Friends" feature has been disabled.'
RestrictedSecretChatActivated = 'The "Restricted True Friends" feature has been enabled!'
SecretChatActivated = 'The "Unrestricted True Friends" feature has been enabled!'
SecretChatActivatedOK = lOK
SecretChatActivatedChange = 'Change Options'
ProblemActivatingChat = 'Oops!  We were unable to activate the "True Friends" chat feature.\n\n%s\n\nPlease try again later.'
ProblemActivatingChatOK = lOK
MultiPageTextFrameNext = lNext
MultiPageTextFramePrev = 'Previous'
MultiPageTextFramePage = 'Page %s/%s'
GuiScreenToontownUnavailable = 'The server appears to be temporarily unavailable, still trying...'
GuiScreenCancel = lCancel
CreateAccountScreenUserName = 'Account Name'
CreateAccountScreenPassword = 'Password'
CreateAccountScreenConfirmPassword = 'Confirm Password'
CreateAccountScreenCancel = lCancel
CreateAccountScreenSubmit = 'Submit'
CreateAccountScreenConnectionErrorSuffix = '.\n\nPlease try again later.'
CreateAccountScreenNoAccountName = 'Please enter an account name.'
CreateAccountScreenAccountNameTooShort = 'Your account name must be at least %s characters long. Please try again.'
CreateAccountScreenPasswordTooShort = 'Your password must be at least %s characters long. Please try again.'
CreateAccountScreenPasswordMismatch = 'The passwords you typed did not match. Please try again.'
CreateAccountScreenUserNameTaken = 'That user name is already taken. Please try again.'
CreateAccountScreenInvalidUserName = 'Invalid user name.\nPlease try again.'
CreateAccountScreenUserNameNotFound = 'User name not found.\nPlease try again or create a new account.'
CRConnecting = 'Connecting...'
CRNoConnectTryAgain = 'Could not connect to %s:%s. Try again?'
CRNoConnectProxyNoPort = 'Could not connect to %s:%s.\n\nYou are communicating to the internet via a proxy, but your proxy does not permit connections on port %s.\n\nYou must open up this port, or disable your proxy, in order to play.  If your proxy has been provided by your ISP, you must contact your ISP to request them to open up this port.'
CRMissingGameRootObject = 'Missing some root game objects.  (May be a failed network connection).\n\nTry again?'
CRNoDistrictsTryAgain = 'No Districts are available. Try again?'
CRRejectRemoveAvatar = 'The avatar was not able to be deleted, try again another time.'
CRLostConnection = 'Your internet connection to the servers has been unexpectedly broken.'
CRBootedReasons = {
    BootedUnexpectedProblem: 'An unexpected problem has occurred.  Your connection has been lost, but you should be able to connect again and go right back into the game.',
    BootedLoggedInElsewhere: 'You have been disconnected because someone else just logged in using your account on another computer.',
    BootedKeyboardChatAuth: 'You have been disconnected because of a problem with your authorization to use keyboard chat.',
    BootedConnectionKilled: 'There has been an unexpected problem logging you in. If this issue persists, please contact the contributors in the Toontown Ranked Discord.',
    BootedVersionMismatch: 'You are running a different version of the game than the server host. If you have just updated your game, please ask the server host to update and restart their server.',
    BootedFileMismatch: 'Your installed files appear to be invalid.  If you are getting this error repeatedly, the server host is likely running a different version of the game.',
    BootedNoAdminPrivileges: 'You are not authorized to use administrator privileges.',
    BootedToonIssue: 'A problem has occurred with your Toon.  If this issue persists, please contact one of the contributors in the Toontown Ranked Discord.',
    BootedKickedForMaintenance: 'You have been logged out by an administrator working on the servers.',
    BootedBanned: "There has been a reported violation of this server's rules connected to '%(name)s'. You have been banned.",
    BootedDistrictReset: 'The district you were playing on has been reset.  Everyone who was playing on that district has been disconnected.  However, you should be able to connect again and go right back into the game.',
    BootedOutOfTime: 'Sorry, you have run out of time to play.'
}
CRBootedReasonUnknownCode = 'An unexpected problem has occurred (error code %s).  Your connection has been lost, but you should be able to connect again and go right back into the game.'
CRBootedAdditionalInfo = '\n\nAdditional information:\n{}'
CRTryConnectAgain = '\n\nTry to connect again?'
CRToontownUnavailable = 'The server appears to be temporarily unavailable, still trying...'
CRToontownUnavailableCancel = lCancel
CRNameCongratulations = 'CONGRATULATIONS!!'
CRNameAccepted = 'Your name has been\napproved by the Toon Council.\n\nFrom this day forth\nyou will be named\n"%s"'
CRServerConstantsProxyNoPort = 'Unable to contact %s.\n\nYou are communicating to the internet via a proxy, but your proxy does not permit connections on port %s.\n\nYou must open up this port, or disable your proxy, in order to play.  If your proxy has been provided by your ISP, you must contact your ISP to request them to open up this port.'
CRServerConstantsProxyNoCONNECT = 'Unable to contact %s.\n\nYou are communicating to the internet via a proxy, but your proxy does not support the CONNECT method.\n\nYou must enable this capability, or disable your proxy, in order to play.  If your proxy has been provided by your ISP, you must contact your ISP to request them to enable this capability.'
CRServerConstantsTryAgain = 'Unable to contact %s.\n\nThe account server might be temporarily down, or there might be some problem with your internet connection.\n\nTry again?'
CRServerDateTryAgain = 'Could not get server date from %s. Try again?'
AfkForceAcknowledgeMessage = 'Your toon got sleepy and went to bed.'
PeriodTimerWarning = 'Your available time is almost over!'
PeriodForceAcknowledgeMessage = 'Sorry, you have used up all of your available time. Please exit to purchase more.'
CREnteringToontown = 'Entering...'
DownloadWatcherUpdate = 'Downloading %s'
DownloadWatcherInitializing = 'Download Initializing...'
LoginScreenUserName = 'Account Name'
LoginScreenPassword = 'Password'
LoginScreenLogin = 'Login'
LoginScreenCreateAccount = 'Create Account'
LoginScreenQuit = lQuit
LoginScreenLoginPrompt = 'Please enter a user name and password.'
LoginScreenBadPassword = 'Bad password.\nPlease try again.'
LoginScreenInvalidUserName = 'Invalid user name.\nPlease try again.'
LoginScreenUserNameNotFound = 'User name not found.\nPlease try again or create a new account.'
LoginScreenPeriodTimeExpired = 'Sorry, you have used up all of your available time.'
LoginScreenNoNewAccounts = 'Sorry, we are not accepting new accounts at this time.'
LoginScreenTryAgain = 'Try Again'
DialogSpecial = 'ooo'
DialogExclamation = '!'
DialogQuestion = '?'
DialogLength1 = 6
DialogLength2 = 12
DialogLength3 = 20
GlobalSpeedChatName = 'SpeedChat'
SCMenuPromotion = 'PROMOTIONAL'
SCMenuElection = 'ELECTION'
SCMenuEmotions = 'EMOTIONS'
SCMenuCustom = 'MY PHRASES'
SCMenuResistance = 'UNITE!'
SCMenuPets = 'PETS'
SCMenuPetTricks = 'TRICKS'
SCMenuCog = 'COG SPEAK'
SCMenuHello = 'HELLO'
SCMenuBye = 'GOODBYE'
SCMenuHappy = 'HAPPY'
SCMenuSad = 'SAD'
SCMenuFriendly = 'FRIENDLY'
SCMenuSorry = 'SORRY'
SCMenuStinky = 'STINKY'
SCMenuPlaces = 'PLACES'
SCMenuToontasks = 'TOONTASKS'
SCMenuBattle = 'BATTLE'
SCMenuGagShop = 'GAG SHOP'
SCMenuFactory = 'FACTORY'
SCMenuKartRacing = 'RACING'
SCMenuFactoryMeet = 'MEET'
SCMenuCFOBattle = 'C.F.O.'
SCMenuCFOBattleCranes = 'CRANES'
SCMenuCFOBattleGoons = 'GOONS'
SCMenuCJBattle = 'CHIEF JUSTICE'
SCMenuCEOBattle = 'C.E.O.'
SCMenuGolf = 'GOLF'
SCMenuWhiteList = 'WHITELIST'
SCMenuPlacesPlayground = 'PLAYGROUND'
SCMenuPlacesEstate = 'ESTATE'
SCMenuPlacesCogs = 'COGS'
SCMenuPlacesWait = 'WAIT'
SCMenuPlacesMinigames = 'MINIGAMES'
SCMenuFriendlyYou = 'You...'
SCMenuFriendlyILike = 'I like...'
SCMenuPlacesLetsGo = "Let's go..."
SCMenuToontasksMyTasks = 'MY TASKS'
SCMenuToontasksYouShouldChoose = 'I think you should choose...'
SCMenuToontasksINeedMore = 'I need more...'
SCMenuBattleGags = 'GAGS'
SCMenuBattleTaunts = 'TAUNTS'
SCMenuBattleStrategy = 'STRATEGY'
SCMenuBoardingGroup = 'BOARDING'
SCMenuParties = 'PARTIES'
SCMenuAprilToons = "APRIL TOONS'"
SCMenuSingingGroup = 'SINGING'
SCMenuCarol = 'CAROLING'
SCMenuSillyHoliday = 'SILLY METER'
SCMenuVictoryParties = 'VICTORY PARTIES'
SCMenuSellbotNerf = 'STORM SELLBOT'
SCMenuJellybeanJam = 'JELLYBEAN WEEK'
SCMenuHalloween = 'HALLOWEEN'
SCMenuWinter = 'WINTER'
SCMenuSellbotInvasion = 'SELLBOT INVASION'
SCMenuFieldOffice = 'FIELD OFFICES'
SCMenuIdesOfMarch = 'GREEN'
FriendSecretNeedsPasswordWarningTitle = 'Parental Controls'
FriendSecretNeedsParentLoginWarning = 'To get or enter a True Friend Code, log in with the Parent Account.  You can disable this prompt by changing your True Friend options.'
FriendSecretNeedsPasswordWarning = 'To get or enter a True Friend Code, you must enter the Parent Account Password.  You can disable this prompt by changing your True Friends options.'
FriendSecretNeedsPasswordWarningOK = lOK
FriendSecretNeedsPasswordWarningCancel = lCancel
FriendSecretNeedsPasswordWarningWrongUsername = "That's not the correct username.  Please enter the username of the parental account.  This is not the same username used to play the game."
FriendSecretNeedsPasswordWarningWrongPassword = "That's not the correct password.  Please enter the password of the parental account.  This is not the same password used to play the game."
FriendSecretIntro = "If you are playing Toontown Online with someone you know in the real world, you can become True Friends.  You can chat using the keyboard with your True Friends.  Other Toons won't understand what you're saying.\n\nYou do this by getting a True Friend Code.  Tell the True Friend Code to your friend, but not to anyone else.  When your friend types in your True Friend Code on their screen, you'll be True Friends in Toontown!"
FriendSecretGetSecret = 'Get a True Friend Code'
FriendSecretEnterSecret = 'If you have a True Friend Code from someone you know, type it here.'
FriendSecretOK = lOK
FriendSecretEnter = 'Enter True Friend Code'
FriendSecretCancel = lCancel
FriendSecretGettingSecret = 'Getting True Friend Code. . .'
FriendSecretGotSecret = "Here is your new True Friend Code.  Be sure to write it down!\n\nYou may give this True Friend Code to one person only.  Once someone types in your True Friend Code, it will not work for anyone else.  If you want to give a True Friend Code to more than one person, get another True Friend Code.\n\nThe True Friend Code will only work for the next two days.  Your friend will have to type it in before it goes away, or it won't work.\n\nYour True Friend Code is:"
FriendSecretTooMany = "Sorry, you can't have any more True Friend Codes today.  You've already had more than your fair share!\n\nTry again tomorrow."
FriendSecretTryingSecret = 'Trying True Friend Code. . .'
FriendSecretEnteredSecretSuccess = 'You are now True Friends with %s!'
FriendSecretTimeOut = 'Sorry, True Friend Codes are not working right now.'
FriendSecretTimeOutRetro = 'Sorry, secrets are not working right now.'
FriendSecretEnteredSecretUnknown = "That's not anyone's True Friend Code.  Are you sure you spelled it correctly?\n\nIf you did type it correctly, it may have expired.  Ask your friend to get a new True Friend Code for you (or get a new one yourself and give it to your friend)."
FriendSecretEnteredSecretFull = "You can't be friends with %s because one of you has too many friends on your friends list."
FriendSecretEnteredSecretFullNoName = "You can't be friends because one of you has too many friends on your friends list."
FriendSecretEnteredSecretSelf = 'You just typed in your own True Friend Code!  Now no one else can use that True Friend Code.'
FriendSecretEnteredSecretWrongProduct = "You have entered the wrong type of True Friend Code.\nThis game uses codes that begin with '%s'."
FriendSecretNowFriends = 'You are now True Friends with %s!'
FriendSecretNowFriendsNoName = 'You are now True Friends!'
FriendSecretDetermineSecret = 'What type of True Friend would you like to make?'
FriendSecretDetermineSecretAvatar = 'Avatar'
FriendSecretDetermineSecretAvatarRollover = 'A friend only in this game'
FriendSecretDetermineSecretAccount = 'Account'
FriendSecretDetermineSecretAccountRollover = 'A friend in another game'  # across the DigiPulse network? :thinking:
GuildMemberTitle = 'Member Options'
GuildMemberPromote = 'Make Officer'
GuildMemberPromoteInvite = 'Make Veteran'
GuildMemberDemoteInvite = 'Demote to Veteran'
GuildMemberGM = 'Make Guildmaster'
GuildMemberGMConfirm = 'Confirm'
GuildMemberDemote = 'Demote to Member'
GuildMemberKick = 'Remove Member'
GuildMemberCancel = lCancel
GuildMemberOnline = 'has come online.'
GuildMemberOffline = 'has gone offline.'
GuildPrefix = '(G):'
GuildNewMember = 'New Guild Member'
GuildMemberUnknown = 'Unknown'
GuildMemberGMMessage = 'Warning! Would you like to give up leadership of your guild and make %s your guild master?\n\nYou will become an officer'
GuildInviteeOK = lOK
GuildInviteeNo = lNo
GuildInviteeInvitation = '%s is inviting you to join %s.'
GuildRedeemErrorInvalidToken = 'Sorry, that code is invalid. Please try again.'
GuildRedeemErrorGuildFull = 'Sorry, this guild has too many members already.'
FriendInviteeTooManyFriends = '%s would like to be your friend, but you already have too many friends on your list!'
FriendInviteeInvitation = '%s would like to be your friend.'
FriendInviteeInvitationPlayer = "%s's player would like to be your friend."
FriendNotifictation = '%s is now your friend.'
FriendInviteeOK = lOK
FriendInviteeNo = lNo
GuildInviterWentAway = '%s is no longer present.'
GuildInviterAlready = '%s is already in a guild.'
GuildInviterBusy = '%s is busy right now.'
GuildInviterNotYet = 'Invite %s to join your guild?'
GuildInviterCheckAvailability = 'Inviting %s to join your guild.'
GuildInviterOK = lOK
GuildInviterNo = lNo
GuildInviterCancel = lCancel
GuildInviterYes = lYes
GuildInviterTooFull = 'Guild has reached maximum size.'
GuildInviterClickToon = 'Click on the pirate you would like to invite.'
GuildInviterTooMany = 'This is a bug'
GuildInviterNotAvailable = '%s is busy right now; try again later.'
GuildInviterGuildSaidNo = '%s has declined your guild invitation.'
GuildInviterAlreadyInvited = '%s has already been invited.'
GuildInviterEndGuildship = 'Remove %s from the guild?'
GuildInviterFriendsNoMore = '%s has left the guild.'
GuildInviterSelf = 'You are already in the guild!'
GuildInviterIgnored = '%s is ignoring you.'
GuildInviterAsking = 'Asking %s to join the guild.'
GuildInviterGuildSaidYes = '%s has joined the guild!'
GuildInviterFriendKickedOut = '%s has kicked out %s from the Guild.'
GuildInviterFriendKickedOutP = '%s have kicked out %s from the Guild.'
GuildInviterFriendInvited = '%s has invited %s to the Guild.'
GuildInviterFriendInvitedP = '%s have invited %s to the Guild.'
GuildInviterFriendPromoted = '%s has promoted %s to the rank of %s.'
GuildInviterFriendPromotedP = '%s have promoted %s to the rank of %s.'
GuildInviterFriendDemoted = '%s has demoted %s to the rank of %s.'
GuildInviterFriendDemotedP = '%s have demoted %s to the rank of %s.'
GuildInviterFriendPromotedGM = '%s has named %s as the new %s'
GuildInviterFriendPromotedGMP = '%s have named %s as the new %s'
GuildInviterFriendDemotedGM = '%s has been named by %s as the new GuildMaster who became the rank of %s'
GuildInviterFriendDemotedGMP = '%s have been named by %s as the new GuildMaster who beaome the rank of %s'
FriendOnline = 'has come online.'
FriendOffline = 'has gone offline.'
FriendInviterOK = lOK
FriendInviterCancel = lCancel
FriendInviterStopBeingFriends = 'Stop being friends'
FriendInviterConfirmRemove = 'Remove'
FriendInviterYes = lYes
FriendInviterNo = lNo
FriendInviterClickToon = 'Click on the toon you would like to make friends with.'
FriendInviterTooMany = 'You have too many friends on your list to add another one now. You will have to remove some friends if you want to make friends with %s.'
FriendInviterToonTooMany = 'You have too many toon friends on your list to add another one now. You will have to remove some toon friends if you want to make friends with %s.'
FriendInviterPlayerTooMany = 'You have too many player friends on your list to add another one now. You will have to remove some player friends if you want to make friends with %s.'
FriendInviterNotYet = 'Would you like to make friends with %s?'
FriendInviterCheckAvailability = 'Seeing if %s is available.'
FriendInviterNotAvailable = '%s is busy right now; try again later.'
FriendInviterCantSee = 'This only works if you can see %s.'
FriendInviterNotOnline = 'This only works if %s is online'
FriendInviterNotOpen = '%s does not have open chat, use secrets to make friends'
FriendInviterWentAway = '%s went away.'
FriendInviterAlready = '%s is already your friend.'
FriendInviterAlreadyInvited = '%s has already been invited.'
FriendInviterAskingCog = 'Asking %s to be your friend.'
FriendInviterAskingPet = '%s jumps around, runs in circles and licks your face.'
FriendInviterAskingMyPet = '%s is already your BEST friend.'
FriendInviterEndFriendship = 'Are you sure you want to stop being friends with %s?'
FriendInviterFriendsNoMore = '%s is no longer your friend.'
FriendInviterSelf = "You are already 'friends' with yourself!"
FriendInviterIgnored = '%s is ignoring you.'
FriendInviterAsking = 'Asking %s to be your friend.'
FriendInviterFriendSaidYes = 'You are now friends with %s!'
FriendInviterPlayerFriendSaidYes = "You are now friends with %s's player, %s!"
FriendInviterFriendSaidNo = '%s said no, thank you.'
FriendInviterFriendSaidNoNewFriends = "%s isn't looking for new friends right now."
FriendInviterOtherTooMany = '%s has too many friends already!'
FriendInviterMaybe = '%s was unable to answer.'
FriendInviterDown = 'Cannot make friends now.'
TalkGuild = 'G'
TalkParty = 'P'
TalkPVP = 'PVP'
AntiSpamInChat = '***Spamming***'
IgnoreConfirmOK = lOK
IgnoreConfirmCancel = lCancel
IgnoreConfirmYes = lYes
IgnoreConfirmNo = lNo
IgnoreConfirmNotYet = 'Would you like to Ignore %s?'
IgnoreConfirmAlready = 'You are already ignoring %s.'
IgnoreConfirmSelf = 'You cannot ignore yourself!'
IgnoreConfirmNewIgnore = 'You are ignoring %s.'
IgnoreConfirmEndIgnore = 'You are no longer ignoring %s.'
IgnoreConfirmRemoveIgnore = 'Stop ignoring %s?'
EmoteList = ['Wave',
             'Happy',
             'Sad',
             'Angry',
             'Sleepy',
             'Shrug',
             'Dance',
             'Think',
             'Bored',
             'Applause',
             'Cringe',
             'Confused',
             'Belly Flop',
             'Bow',
             'Banana Peel',
             'Resistance Salute',
             'Laugh',
             lYes,
             lNo,
             lOK,
             'Surprise',
             'Cry',
             'Delighted',
             'Furious',
             'Laugh',
             'Taunt']
EmoteWhispers = ['%s waves.',
                 '%s is happy.',
                 '%s is sad.',
                 '%s is angry.',
                 '%s is sleepy.',
                 '%s shrugs.',
                 '%s dances.',
                 '%s thinks.',
                 '%s is bored.',
                 '%s applauds.',
                 '%s cringes.',
                 '%s is confused.',
                 '%s does a belly flop.',
                 '%s bows to you.',
                 '%s slips on a banana peel.',
                 '%s gives the resistance salute.',
                 '%s laughs.',
                 "%s says '" + lYes + "'.",
                 "%s says '" + lNo + "'.",
                 "%s says '" + lOK + "'.",
                 '%s is surprised.',
                 '%s is crying.',
                 '%s is delighted.',
                 '%s is furious.',
                 '%s is laughing.',
                 '%s taunts you.']
EmoteFuncDict = {'Wave': 0,
                 'Happy': 1,
                 'Sad': 2,
                 'Angry': 3,
                 'Sleepy': 4,
                 'Shrug': 5,
                 'Dance': 6,
                 'Think': 7,
                 'Bored': 8,
                 'Applause': 9,
                 'Cringe': 10,
                 'Confused': 11,
                 'Belly Flop': 12,
                 'Bow': 13,
                 'Banana Peel': 14,
                 'Resistance Salute': 15,
                 'Laugh': 16,
                 lYes: 17,
                 lNo: 18,
                 lOK: 19,
                 'Surprise': 20,
                 'Cry': 21,
                 'Delighted': 22,
                 'Furious': 23,
                 'Laugh': 24,
                 'Taunt': 25}
# 'Sing Note G1': 25,
# 'Sing Note A': 26,
# 'Sing Note B': 27,
# 'Sing Note C': 28,
# 'Sing Note D': 29,
# 'Sing Note E': 30,
# 'Sing Note F': 31,
# 'Sing Note G2': 32}
SuitBrushOffs = {'f': ["I'm late for a meeting."],
                 'p': ['Push off.'],
                 'ym': ['Yes Man says NO.'],
                 None: ["It's my day off.",
                        "I believe you're in the wrong office.",
                        'Have your people call my people.',
                        "You're in no position to meet with me.",
                        'Talk to my assistant.']}
SuitFaceoffTaunts = {'b': ['Do you have a donation for me?',
                           "I'm going to make you a sore loser.",
                           "I'm going to leave you high and dry.",
                           'I\'m "A Positive" I\'m going to win.',
                           '"O" don\'t be so "Negative".',
                           "I'm surprised you found me, I'm very mobile.",
                           "I'm going to need to do a quick count on you.",
                           "You're soon going to need a cookie and some juice.",
                           "When I'm through you'll need to lie down.",
                           'This will only hurt for a second.',
                           "I'm going to make you dizzy.",
                           "Good timing, I'm a pint low."],
                     'm': ["You don't know who you're mingling with.",
                           'Ever mingle with the likes of me?',
                           'Good, it takes two to mingle.',
                           "Let's mingle.",
                           'This looks like a good place to mingle.',
                           "Well,isn't this cozy?",
                           "You're mingling with defeat.",
                           "I'm going to mingle in your business.",
                           "Are you sure you're ready to mingle?"],
                     'ms': ['Get ready for a shake down.',
                            'You had better move out of the way.',
                            'Move it or lose it.',
                            "I believe it's my move.",
                            'This should shake you up.',
                            'Prepare to be moved.',
                            "I'm ready to make my move.",
                            "Watch out toon, you're on shaky ground.",
                            'This should be a moving moment.',
                            'I feel moved to defeat you.',
                            'Are you shaking yet?'],
                     'hh': ["I'm way ahead of you.",
                            "You're headed for big trouble.",
                            "You'll wish this was all in your head.",
                            "Oh good, I've been hunting for you.",
                            "I'll have your head for this.",
                            'Heads up!',
                            "Looks like you've got a head for trouble.",
                            'Headed my way?',
                            'A perfect trophy for my collection.',
                            'You are going to have such a headache.',
                            "Don't lose your head over me."],
                     'tbc': ["Watch out, I'm gouda getcha.",
                             'You can call me Jack.',
                             'Are you sure?  I can be such a Muenster at times.',
                             'Well finally, I was afraid you were stringing me along.',
                             "I'm going to cream you.",
                             "Don't you think I've aged well?",
                             "I'm going to make mozzarella outta ya.",
                             "I've been told I'm very strong.",
                             'Careful, I know your expiration date.',
                             "Watch out, I'm a whiz at this game.",
                             'Beating you will be a brieeze.'],
                     'cr': ['RAID!',
                            "You don't fit in my corporation.",
                            'Prepare to be raided.',
                            "Looks like you're primed for a take-over.",
                            'That is not proper corporate attire.',
                            "You're looking rather vulnerable.",
                            'Time to sign over your assets.',
                            "I'm on a toon removal crusade.",
                            'You are defenseless against my ideas.',
                            "Relax, you'll find this is for the best."],
                     'mh': ['Are you ready for my take?',
                            'Lights, camera, action!',
                            "Let's start rolling.",
                            'Today the role of defeated toon, will be played by - YOU!',
                            'This scene will go on the cutting room floor.',
                            'I already know my motivation for this scene.',
                            'Are you ready for your final scene?',
                            "I'm ready to roll your end credits.",
                            'I told you not to call me.',
                            "Let's get on with the show.",
                            "There's no business like it!",
                            "I hope you don't forget your lines."],
                     'nc': ['Looks like your number is up.',
                            'I hope you prefer extra crunchy.',
                            "Now you're really in a crunch.",
                            'Is it time for crunch already?',
                            "Let's do crunch.",
                            'Where would you like to have your crunch today?',
                            "You've given me something to crunch on.",
                            'This will not be smooth.',
                            'Go ahead, try and take a number.',
                            'I could do with a nice crunch about now.'],
                     'ls': ["It's time to collect on your loan.",
                            "You've been on borrowed time.",
                            'Your loan is now due.',
                            'Time to pay up.',
                            'Well you asked for an advance and you got it.',
                            "You're going to pay for this.",
                            "It's pay back time.",
                            'Can you lend me an ear?',
                            "Good thing you're here,  I'm in a frenzy.",
                            'Shall we have a quick bite?',
                            'Let me take a bite at it.'],
                     'mb': ['Time to bring in the big bags.',
                            'I can bag this.',
                            'Paper or plastic?',
                            'Do you have your baggage claim?',
                            "Remember, money won't make you happy.",
                            'Careful, I have some serious baggage.',
                            "You're about to have money trouble.",
                            'Money will make your world go around.',
                            "I'm too rich for your blood.",
                            'You can never have too much money!'],
                     'ski': ['Lets get this almost to the bone, toon.',
                             'My wealth is my life.',
                             "I depend on my money.",
                             "You'll need to force this money out of me.",
                             "No deal, toon."],
                     'rb': ["You've been robbed.",
                            "I'll rob you of this victory.",
                            "I'm a royal pain!",
                            'Hope you can grin and baron.',
                            "You'll need to report this robbery.",
                            "Stick 'em up.",
                            "I'm a noble adversary.",
                            "I'm going to take everything you have.",
                            'You could call this neighborhood robbery.',
                            'You should know not to talk to strangers.'],
                     'bs': ['Never turn your back on me.',
                            "You won't be coming back.",
                            'Take that back or else!',
                            "I'm good at cutting costs.",
                            'I have lots of back up.',
                            "There's no backing down now.",
                            "I'm the best and I can back that up.",
                            'Whoa, back up there toon.',
                            'Let me get your back.',
                            "You're going to have a stabbing headache soon.",
                            'I have perfect puncture.'],
                     'bw': ["Don't brush me aside.",
                            'You make my hair curl.',
                            'I can make this permanent if you want.',
                            "It looks like you're going to have some split ends.",
                            "You can't handle the truth.",
                            "I think it's your turn to be dyed.",
                            "I'm so glad you're on time for your cut.",
                            "You're in big trouble.",
                            "I'm going to wig out on you.",
                            "I'm a big deal little toon."],
                     'le': ["Careful, my legal isn't very tender.",
                            'I soar, then I score.',
                            "I'm bringing down the law on you.",
                            'You should know, I have some killer instincts.',
                            "I'm going to give you legal nightmares.",
                            "You won't win this battle.",
                            'This is so much fun it should be illegal.',
                            "Legally, you're too small to fight me.",
                            'There is no limit to my talons.',
                            "I call this a citizen's arrest."],
                     'sd': ["You'll never know when I'll stop.",
                            'Let me take you for a spin.',
                            'The doctor will see you now.',
                            "I'm going to put you into a spin.",
                            'You look like you need a doctor.',
                            'The doctor is in, the Toon is out.',
                            "You won't like my spin on this.",
                            'You are going to spin out of control.',
                            'Care to take a few turns with me?',
                            'I have my own special spin on the subject.'],
                     'f': ["I'm gonna tell the boss about you!",
                           "I may be just a flunky - But I'm real spunky.",
                           "I'm using you to step up the corporate ladder.",
                           "You're not going to like the way I work.",
                           'The boss is counting on me to stop you.',
                           "You're going to look good on my resume.",
                           "You'll have to go through me first.",
                           "Let's see how you rate my job performance.",
                           'I excel at Toon disposal.',
                           "You're never going to meet my boss.",
                           "I'm sending you back to the Playground."],
                     'bgh': ["You seem to be struggling, want a hand, toon?",
                             "You'll make a easy bag for the ladder.",
                             'Hold it. I have to bag you in.',
                             "The boss will be pleased at this sacked victory.",
                             "Parden me, I have to bag this one."],
                     'p': ["I'm gonna rub you out!",
                           "Hey, you can't push me around.",
                           "I'm No.2!",
                           "I'm going to scratch you out.",
                           "I'll have to make my point more clear.",
                           'Let me get right to the point.',
                           "Let's hurry, I bore easily.",
                           'I hate it when things get dull.',
                           'So you want to push your luck?',
                           'Did you pencil me in?',
                           'Careful, I may leave a mark.'],
                     'ym': ["I'm positive you're not going to like this.",
                            "I don't know the meaning of no.",
                            'Want to meet?  I say yes, anytime.',
                            'You need some positive enforcement.',
                            "I'm going to make a positive impression.",
                            "I haven't been wrong yet.",
                            "Yes, I'm ready for you.",
                            'Are you positive you want to do this?',
                            "I'll be sure to end this on a positive note.",
                            "I'm confirming our meeting time.",
                            "I won't take no for an answer."],
                     'mm': ["I'm going to get into your business!",
                            'Sometimes big hurts come in small packages.',
                            'No job is too small for me.',
                            "I want the job done right, so I'll do it myself.",
                            'You need someone to manage your assets.',
                            'Oh good, a project.',
                            "Well, you've managed to find me.",
                            'I think you need some managing.',
                            "I'll take care of you in no time.",
                            "I'm watching every move you make.",
                            'Are you sure you want to do this?',
                            "We're going to do this my way.",
                            "I'm going to be breathing down your neck.",
                            'I can be very intimidating.'],
                     'ds': ["You're going down!",
                            'Your options are shrinking.',
                            'Expect diminishing returns.',
                            "You've just become expendable.",
                            "Don't ask me to lay off.",
                            'I might have to make a few cutbacks.',
                            'Things are looking down for you.',
                            'Why do you look so down?'],
                     'cc': ['Surprised to hear from me?',
                            'You rang?',
                            'Are you ready to accept my charges?',
                            'This caller always collects.',
                            "I'm one smooth operator.",
                            "Hold the phone -- I'm here.",
                            'Have you been waiting for my call?',
                            "I was hoping you'd answer my call.",
                            "I'm going to cause a ringing sensation.",
                            'I always make my calls direct.',
                            'Boy, did you get your wires crossed.',
                            'This call is going to cost you.',
                            "You've got big trouble on the line."],
                     'tm': ['I plan on making this inconvenient for you.',
                            'Can I interest you in an insurance plan?',
                            'You should have missed my call.',
                            "You won't be able to get rid of me now.",
                            'This a bad time?  Good.',
                            'I was planning on running into you.',
                            'I will be reversing the charges for this call.',
                            'I have some costly items for you today.',
                            'Too bad for you - I make house calls.',
                            "I'm prepared to close this deal quickly.",
                            "I'm going to use up a lot of your resources."],
                     'nd': ['In my opinion, your name is mud.',
                            "I hope you don't mind if I drop your name.",
                            "Haven't we met before?",
                            "Let's hurry, I'm having lunch with 'Mr. Hollywood.'",
                            "Have I mentioned I know 'The Mingler?'",
                            "You'll never forget me.",
                            'I know all the right people to bring you down.',
                            "I think I'll just drop in.",
                            "I'm in the mood to drop some Toons.",
                            "You name it, I've dropped it."],
                     'gh': ['Put it there, Toon.',
                            "Let's shake on it.",
                            "I'm going to enjoy this.",
                            "You'll notice I have a very firm grip.",
                            "Let's seal the deal.",
                            "Let's get right to the business at hand.",
                            "Off handedly I'd say, you're in trouble.",
                            "You'll find I'm a handful.",
                            'I can be quite handy.',
                            "I'm a very hands-on kinda guy.",
                            'Would you like some hand-me-downs?',
                            'Let me show you some of my handiwork.',
                            'I think the handwriting is on the wall.'],
                     'sc': ['I will make short work of you.',
                            "You're about to have money trouble.",
                            "You're about to be overcharged.",
                            'This will be a short-term assignment.',
                            "I'll be done with you in short order.",
                            "You'll soon experience a shortfall.",
                            "Let's make this a short stop.",
                            "I think you've come up short.",
                            'I have a short temper for Toons.',
                            "I'll be with you shortly.",
                            "You're about to be shorted."],
                     'pp': ['This is going to sting a little.',
                            "I'm going to give you a pinch for luck.",
                            "You don't want to press your luck with me.",
                            "I'm going to put a crimp in your smile.",
                            'Perfect, I have an opening for you.',
                            'Let me add my two cents.',
                            "I've been asked to pinch-hit.",
                            "I'll prove you're not dreaming.",
                            'Heads you lose, tails I win.',
                            'A Penny for your gags.'],
                     'tw': ['Things are about to get very tight.',
                            "That's Mr. Tightwad to you.",
                            "I'm going to cut off your funding.",
                            'Is this the best deal you can offer?',
                            "Let's get going - time is money.",
                            "You'll find I'm very tightfisted.",
                            "You're in a tight spot.",
                            'Prepare to walk a tight rope.',
                            'I hope you can afford this.',
                            "I'm going to make this a tight squeeze.",
                            "I'm going to make a big dent in your budget."],
                     'bc': ['I enjoy subtracting Toons.',
                            'You can count on me to make you pay.',
                            'Bean there, done that.',
                            'I can hurt you where it counts.',
                            'I make every bean count.',
                            'Your expense report is overdue.',
                            'Time for an audit.',
                            "Let's step into my office.",
                            'Where have you bean?',
                            "I've bean waiting for you.",
                            "I'm going to bean you."],
                     'bf': ["Looks like you've hit rock bottom.",
                            "I'm ready to feast.",
                            "I'm a sucker for Toons.",
                            'Oh goody, lunch time.',
                            'Perfect timing, I need a quick bite.',
                            "I'd like some feedback on my performance.",
                            "Let's talk about the bottom line.",
                            "You'll find my talents are bottomless.",
                            'Good, I need a little pick-me-up.',
                            "I'd love to have you for lunch."],
                     'tf': ["It's time to face-off!",
                            'You had better face up to defeat.',
                            'Prepare to face your worst nightmare!',
                            "Face it, I'm better than you.",
                            'Two heads are better than one.',
                            'It takes two to tango, you wanna tango?',
                            "You're in for two times the trouble.",
                            'Which face would you like to defeat you?',
                            "I'm 'two' much for you.",
                            "You don't know who you're facing.",
                            'Are you ready to face your doom?'],
                     'trf': ["HALT!",
                             'STEP BACK.',
                             "I'll make the GO call, toon.",
                             "The Vice President counts on me.",
                             "I'm a royal heading-ache.",
                             'On the count of three...'],
                     'dt': ["I'm gonna give you double the trouble.",
                            'See if you can stop my double cross.',
                            'I serve a mean double-\x04DECKER.',
                            "It's time to do some double-dealing.",
                            'I plan to do some double DIPPING.',
                            "You're not going to like my double play.",
                            'You may want to double think this.',
                            'Get ready for a double TAKE.',
                            'You may want to double up against me.',
                            'Doubles anyone??'],
                     'ac': ["I'm going to chase you out of town!",
                            'Do you hear a siren?',
                            "I'm going to enjoy this.",
                            'I love the thrill of the chase.',
                            'Let me give you the run down.',
                            'Do you have insurance?',
                            'I hope you brought a stretcher with you.',
                            'I doubt you can keep up with me.',
                            "It's all uphill from here.",
                            "You're going to need some urgent care soon.",
                            'This is no laughing matter.',
                            "I'm going to give you the business."],
                     'def': ["All of my clients have protection.",
                             "I hope you brought a shield, Toon.",
                             "Your claim better break diamond.",
                             "I have this case locked 'n sealed."]}
Emotes_Root = 'EMOTES'
Emotes_Dances = 'Dances'
Emotes_General = 'General'
Emotes_Music = 'Music'
Emotes_Expressions = 'Emotions'
Emote_ShipDenied = 'Cannot emote while sailing.'
Emote_MoveDenied = 'Cannot emote while moving.'
Emote_CombatDenied = 'Cannot emote while in combat.'
Emote_CannonDenied = 'Cannot emote while using a cannon.'
Emote_SwimDenied = 'Cannot emote while swimming.'
Emote_ParlorGameDenied = 'Cannot emote while playing a parlor game.'
Emotes = (60505,
          60506,
          60509,
          60510,
          60511,
          60516,
          60519,
          60520,
          60521,
          60522,
          60523,
          60524,
          60525,
          60526,
          60527,
          60528,
          60529,
          60530,
          60602,
          60607,
          60611,
          60614,
          60615,
          60622,
          60627,
          60629,
          60632,
          60636,
          60638,
          60640,
          60644,
          60652,
          60654,
          60657,
          60658,
          60663,
          60664,
          60665,
          60666,
          60668,
          60669,
          60612,
          60661,
          60645,
          60629,
          60641,
          60654,
          60630,
          60670,
          60633,
          60676,
          60677,
          65000,
          65001,
          60517,
          60678,
          60909)
SCFactoryMeetMenuIndexes = (1903,
                            1904,
                            1906,
                            1907,
                            1908,
                            1910,
                            1913,
                            1915,
                            1916,
                            1917,
                            1919,
                            1922,
                            1923,
                            1924,
                            1932,
                            1940,
                            1941)
CustomSCStrings = {10: 'Oh, well.',
                   20: 'Why not?',
                   30: 'Naturally!',
                   40: "That's the way to do it.",
                   50: 'Right on!',
                   60: 'What up?',
                   70: 'But of course!',
                   80: 'Bingo!',
                   90: "You've got to be kidding...",
                   100: 'Sounds good to me.',
                   110: "That's kooky!",
                   120: 'Awesome!',
                   130: 'For crying out loud!',
                   140: "Don't worry.",
                   150: 'Grrrr!',
                   160: "What's new?",
                   170: 'Hey, hey, hey!',
                   180: 'See you tomorrow.',
                   190: 'See you next time.',
                   200: 'See ya later, alligator.',
                   210: 'After a while, crocodile.',
                   220: 'I need to go soon.',
                   230: "I don't know about this!",
                   240: "You're outta here!",
                   250: 'Ouch, that really smarts!',
                   260: 'Gotcha!',
                   270: 'Please!',
                   280: 'Thanks a million!',
                   290: "You are stylin'!",
                   300: 'Excuse me!',
                   310: 'Can I help you?',
                   320: "That's what I'm talking about!",
                   330: "If you can't take the heat, stay out of the kitchen.",
                   340: 'Well shiver me timbers!',
                   350: "Well isn't that special!",
                   360: 'Quit horsing around!',
                   370: 'Cat got your tongue?',
                   380: "You're in the dog house now!",
                   390: 'Look what the cat dragged in.',
                   400: 'I need to go see a Toon.',
                   410: "Don't have a cow!",
                   420: "Don't chicken out!",
                   430: "You're a sitting duck.",
                   440: 'Whatever!',
                   450: 'Totally!',
                   460: 'Sweet!',
                   470: 'That rules!',
                   480: 'Yeah, baby!',
                   490: 'Catch me if you can!',
                   500: 'You need to heal first.',
                   510: 'You need more Laff Points.',
                   520: "I'll be back in a minute.",
                   530: "I'm hungry.",
                   540: 'Yeah, right!',
                   550: "I'm sleepy.",
                   560: "I'm ready!",
                   570: "I'm bored.",
                   580: 'I love it!',
                   590: 'That was exciting!',
                   600: 'Jump!',
                   610: 'Got gags?',
                   620: "What's wrong?",
                   630: 'Easy does it.',
                   640: 'Slow and steady wins the race.',
                   650: 'Touchdown!',
                   660: 'Ready?',
                   670: 'Set!',
                   680: 'Go!',
                   690: "Let's go this way!",
                   700: 'You won!',
                   710: 'I vote yes.',
                   720: 'I vote no.',
                   730: 'Count me in.',
                   740: 'Count me out.',
                   750: "Stay here, I'll be back.",
                   760: 'That was quick!',
                   770: 'Did you see that?',
                   780: "What's that smell?",
                   790: 'That stinks!',
                   800: "I don't care.",
                   810: 'Just what the doctor ordered.',
                   820: "Let's get this party started!",
                   830: 'This way everybody!',
                   840: 'What in the world?',
                   850: "The check's in the mail.",
                   860: 'I heard that!',
                   870: 'Are you talking to me?',
                   880: "Thank you, I'll be here all week.",
                   890: 'Hmm.',
                   900: "I'll get this one.",
                   910: 'I got it!',
                   920: "It's mine!",
                   930: 'Please, take it.',
                   940: 'Stand back, this could be dangerous.',
                   950: 'No worries!',
                   960: 'Oh, my!',
                   970: 'Whew!',
                   980: 'Owoooo!',
                   990: 'All Aboard!',
                   1000: 'Hot Diggity Dog!',
                   1010: 'Curiosity killed the cat.',
                   2000: 'Act your age!',
                   2010: 'Am I glad to see you!',
                   2020: 'Be my guest.',
                   2030: 'Been keeping out of trouble?',
                   2040: 'Better late than never!',
                   2050: 'Bravo!',
                   2060: 'But seriously, folks...',
                   2070: 'Care to join us?',
                   2080: 'Catch you later!',
                   2090: 'Changed your mind?',
                   2100: 'Come and get it!',
                   2110: 'Dear me!',
                   2120: 'Delighted to make your acquaintance.',
                   2130: "Don't do anything I wouldn't do!",
                   2140: "Don't even think about it!",
                   2150: "Don't give up the ship!",
                   2160: "Don't hold your breath.",
                   2170: "Don't ask.",
                   2180: 'Easy for you to say.',
                   2190: 'Enough is enough!',
                   2200: 'Excellent!',
                   2210: 'Fancy meeting you here!',
                   2220: 'Give me a break.',
                   2230: 'Glad to hear it.',
                   2240: 'Go ahead, make my day!',
                   2250: 'Go for it!',
                   2260: 'Good job!',
                   2270: 'Good to see you!',
                   2280: 'Got to get moving.',
                   2290: 'Got to hit the road.',
                   2300: 'Hang in there.',
                   2310: 'Hang on a second.',
                   2320: 'Have a ball!',
                   2330: 'Have fun!',
                   2340: "Haven't got all day!",
                   2350: 'Hold your horses!',
                   2360: 'Horsefeathers!',
                   2370: "I don't believe this!",
                   2380: 'I doubt it.',
                   2390: 'I owe you one.',
                   2400: 'I read you loud and clear.',
                   2410: 'I think so.',
                   2420: 'I think you should pass.',
                   2430: "I wish I'd said that.",
                   2440: "I wouldn't if I were you.",
                   2450: "I'd be happy to!",
                   2460: "I'm helping my friend.",
                   2470: "I'm here all week.",
                   2480: 'Imagine that!',
                   2490: 'In the nick of time...',
                   2500: "It's not over 'til it's over.",
                   2510: 'Just thinking out loud.',
                   2520: 'Keep in touch.',
                   2530: 'Lovely weather for ducks!',
                   2540: 'Make it snappy!',
                   2550: 'Make yourself at home.',
                   2560: 'Maybe some other time.',
                   2570: 'Mind if I join you?',
                   2580: 'Nice place you have here.',
                   2590: 'Nice talking to you.',
                   2600: 'No doubt about it.',
                   2610: 'No kidding!',
                   2620: 'Not by a long shot.',
                   2630: 'Of all the nerve!',
                   2640: 'Okay by me.',
                   2650: 'Righto.',
                   2660: 'Say cheese!',
                   2670: 'Say what?',
                   2680: 'Tah-dah!',
                   2690: 'Take it easy.',
                   2700: 'Ta-ta for now!',
                   2710: 'Thanks, but no thanks.',
                   2720: 'That takes the cake!',
                   2730: "That's funny.",
                   2740: "That's the ticket!",
                   2750: "There's a Cog invasion!",
                   2760: 'Toodles.',
                   2770: 'Watch out!',
                   2780: 'Well done!',
                   2790: "What's cooking?",
                   2800: "What's happening?",
                   2810: 'Works for me.',
                   2820: 'Yes sirree.',
                   2830: 'You betcha.',
                   2840: 'You do the math.',
                   2850: 'You leaving so soon?',
                   2860: 'You make me laugh!',
                   2870: 'You take right.',
                   2880: "You're going down!",
                   3000: 'Anything you say.',
                   3010: 'Care if I join you?',
                   3020: 'Check, please.',
                   3030: "Don't be too sure.",
                   3040: "Don't mind if I do.",
                   3050: "Don't sweat it!",
                   3060: "Don't you know it!",
                   3070: "Don't mind me.",
                   3080: 'Eureka!',
                   3090: 'Fancy that!',
                   3100: 'Forget about it!',
                   3110: 'Going my way?',
                   3120: 'Good for you!',
                   3130: 'Good grief.',
                   3140: 'Have a good one!',
                   3150: 'Heads up!',
                   3160: 'Here we go again.',
                   3170: 'How about that!',
                   3180: 'How do you like that?',
                   3190: 'I believe so.',
                   3200: 'I think not.',
                   3210: "I'll get back to you.",
                   3220: "I'm all ears.",
                   3230: "I'm busy.",
                   3240: "I'm not kidding!",
                   3250: "I'm speechless.",
                   3260: 'Keep smiling.',
                   3270: 'Let me know!',
                   3280: 'Let the pie fly!',
                   3290: "Likewise, I'm sure.",
                   3300: 'Look alive!',
                   3310: 'My, how time flies.',
                   3320: 'No comment.',
                   3330: "Now you're talking!",
                   3340: 'Okay by me.',
                   3350: 'Pleased to meet you.',
                   3360: 'Righto.',
                   3370: 'Sure thing.',
                   3380: 'Thanks a million.',
                   3390: "That's more like it.",
                   3400: "That's the stuff!",
                   3410: 'Time for me to hit the hay.',
                   3420: 'Trust me!',
                   3430: 'Until next time.',
                   3440: 'Wait up!',
                   3450: 'Way to go!',
                   3460: 'What brings you here?',
                   3470: 'What happened?',
                   3480: 'What now?',
                   3490: 'You first.',
                   3500: 'You take left.',
                   3510: 'You wish!',
                   3520: "You're toast!",
                   3530: "You're too much!",
                   4000: 'Toons rule!',
                   4010: 'Cogs drool!',
                   4020: 'Toons of the world unite!',
                   4030: 'Howdy, partner!',
                   4040: 'Much obliged.',
                   4050: 'Get along, little doggie.',
                   4060: "I'm going to hit the hay.",
                   4070: "I'm chomping at the bit!",
                   4080: "This town isn't big enough for the two of us!",
                   4090: 'Saddle up!',
                   4100: 'Draw!!!',
                   4110: "There's gold in them there hills!",
                   4120: 'Happy trails!',
                   4130: 'This is where I ride off into the sunset...',
                   4140: "Let's skedaddle!",
                   4150: 'You got a bee in your bonnet?',
                   4160: 'Lands sake!',
                   4170: 'Right as rain.',
                   4180: 'I reckon so.',
                   4190: "Let's ride!",
                   4200: 'Well, go figure!',
                   4210: "I'm back in the saddle again!",
                   4220: 'Round up the usual suspects.',
                   4230: 'Giddyup!',
                   4240: 'Reach for the sky.',
                   4250: "I'm fixing to.",
                   4260: 'Hold your horses!',
                   4270: "I can't hit the broad side of a barn.",
                   4280: "Y'all come back now.",
                   4290: "It's a real barn burner!",
                   4300: "Don't be a yellow belly.",
                   4310: 'Feeling lucky?',
                   4320: "What in Sam Hill's goin' on here?",
                   4330: 'Shake your tail feathers!',
                   4340: "Well, don't that take all.",
                   4350: "That's a sight for sore eyes!",
                   4360: 'Pickins is mighty slim around here.',
                   4370: 'Take a load off.',
                   4380: "Aren't you a sight!",
                   4390: "That'll learn ya!",
                   6000: 'I want candy!',
                   6010: "I've got a sweet tooth.",
                   6020: "That's half-baked.",
                   6030: 'Just like taking candy from a baby!',
                   6040: "They're cheaper by the dozen.",
                   6050: 'Let them eat cake!',
                   6060: "That's the icing on the cake.",
                   6070: "You can't have your cake and eat it too.",
                   6080: 'I feel like a kid in a candy store.',
                   6090: 'Six of one, half a dozen of the other...',
                   6100: "Let's keep it short and sweet.",
                   6110: 'Keep your eye on the doughnut not the hole.',
                   6120: "That's pie in the sky.",
                   6130: "But it's wafer thin.",
                   6140: "Let's gum up the works!",
                   6150: "You're one tough cookie!",
                   6160: "That's the way the cookie crumbles.",
                   6170: 'Like water for chocolate.',
                   6180: 'Are you trying to sweet talk me?',
                   6190: 'A spoonful of sugar helps the medicine go down.',
                   6200: 'You are what you eat!',
                   6210: 'Easy as pie!',
                   6220: "Don't be a sucker!",
                   6230: 'Sugar and spice and everything nice.',
                   6240: "It's like butter!",
                   6250: 'The candyman can!',
                   6260: 'We all scream for ice cream!',
                   6270: "Let's not sugar coat it.",
                   6280: 'Knock knock...',
                   6290: "Who's there?",
                   7000: 'Quit monkeying around!',
                   7010: 'That really throws a monkey-wrench in things.',
                   7020: 'Monkey see, monkey do.',
                   7030: 'They made a monkey out of you.',
                   7040: 'That sounds like monkey business.',
                   7050: "I'm just monkeying with you.",
                   7060: "Who's gonna be monkey in the middle?",
                   7070: "That's a monkey off my back...",
                   7080: 'This is more fun than a barrel of monkeys!',
                   7090: "Well I'll be a monkey's uncle.",
                   7100: "I've got monkeys on the brain.",
                   7110: "What's with the monkey suit?",
                   7120: 'Hear no evil.',
                   7130: 'See no evil.',
                   7140: 'Speak no evil.',
                   7150: "Let's make like a banana and split.",
                   7160: "It's a jungle out there.",
                   7170: "You're the top banana.",
                   7180: 'Cool bananas!',
                   7190: "I'm going bananas!",
                   7200: "Let's get into the swing of things!",
                   7210: 'This place is swinging!',
                   7220: "I'm dying on the vine.",
                   7230: 'This whole affair has me up a tree.',
                   7230: "Let's make like a tree and leave.",
                   7240: "Jellybeans don't grow on trees!",
                   10000: 'This place is a ghost town.',
                   10001: 'Nice costume!',
                   10002: 'I think this place is haunted.',
                   10003: 'Trick or Treat!',
                   10004: 'Boo!',
                   10005: 'Happy Haunting!',
                   10006: 'Happy Halloween!',
                   10007: "It's time for me to turn into a pumpkin.",
                   10008: 'Spooktastic!',
                   10009: 'Spooky!',
                   10010: "That's creepy!",
                   10011: 'I hate spiders!',
                   10012: 'Did you hear that?',
                   10013: "You don't have a ghost of a chance!",
                   10014: 'You scared me!',
                   10015: "That's spooky!",
                   10016: "That's freaky!",
                   10017: 'That was strange....',
                   10018: 'Skeletons in your closet?',
                   10019: 'Did I scare you?',
                   11000: 'Bah! Humbug!',
                   11001: 'Better not pout!',
                   11002: 'Brrr!',
                   11003: 'Chill out!',
                   11004: 'Come and get it!',
                   11005: "Don't be a turkey.",
                   11006: 'Gobble gobble!',
                   11007: 'Happy holidays!',
                   11008: 'Happy New Year!',
                   11009: 'Happy Thanksgiving!',
                   11010: 'Happy Turkey Day!',
                   11011: 'Ho! Ho! Ho!',
                   11012: 'It\'s "snow" problem.',
                   11013: 'It\'s "snow" wonder.',
                   11014: 'Let it snow!',
                   11015: "Rake 'em in.",
                   11016: "Season's greetings!",
                   11017: 'Snow doubt about it!',
                   11018: 'Snow far, snow good!',
                   11019: 'Yule be sorry!',
                   11020: 'Have a Wonderful Winter!',
                   11021: 'The Holiday Party decorations are Toontastic!',
                   11022: 'Toon Troopers are hosting Holiday Parties!',
                   12000: 'Be mine!',
                   12001: 'Be my sweetie!',
                   12002: "Happy ValenToon's Day!",
                   12003: 'Aww, how cute.',
                   12004: "I'm sweet on you.",
                   12005: "It's puppy love.",
                   12006: 'Love ya!',
                   12007: 'Will you be my ValenToon?',
                   12008: 'You are a sweetheart.',
                   12009: 'You are as sweet as pie.',
                   12010: 'You are cute.',
                   12011: 'You need a hug.',
                   12012: 'Lovely!',
                   12013: "That's darling!",
                   12014: 'Roses are red...',
                   12015: 'Violets are blue...',
                   12016: "That's sweet!",
                   12050: 'I LOVE busting Cogs!',
                   12051: "You're dynamite!",
                   12052: 'I only have hypno-eyes for you!',
                   12053: "You're sweeter than a jellybean!",
                   12054: "I'd LOVE for you to come to my ValenToon's party!",
                   13000: "Top o' the mornin' to you!",
                   13001: "Happy St. Patrick's Day!",
                   13002: "You're not wearing green!",
                   13003: "It's the luck of the Irish.",
                   13004: "I'm green with envy.",
                   13005: 'You lucky dog!',
                   13006: "You're my four leaf clover!",
                   13007: "You're my lucky charm!",
                   14000: "Let's have a summer Estate party!",
                   14001: "It's party time!",
                   14002: 'Last one in the pond is a rotten Cog!',
                   14003: 'Group Doodle training time!',
                   14004: 'Doodle training time!',
                   14005: 'Your Doodle is cool!',
                   14006: 'What tricks can your Doodle do?',
                   14007: 'Time for Cannon Pinball!',
                   14008: 'Cannon Pinball rocks!',
                   14009: 'Your Estate rocks!',
                   14010: 'Your Garden is cool!',
                   14011: 'Your Estate is cool!'}
SCMenuCommonCogIndices = (20000, 20004)
SCMenuCustomCogIndices = {'bf': (20005, 20014),
                          'nc': (20015, 20024),
                          'ym': (20025, 20035),
                          'ms': (20036, 20046),
                          'bc': (20047, 20057),
                          'cc': (20058, 20070),
                          'nd': (20071, 20080),
                          'ac': (20081, 20092),
                          'tf': (20093, 20103),
                          'hh': (20104, 20114),
                          'le': (20115, 20124),
                          'bs': (20125, 20135),
                          'cr': (20136, 20145),
                          'tbc': (20146, 20156),
                          'ds': (20157, 20164),
                          'gh': (20165, 20177),
                          'pp': (20178, 20187),
                          'b': (20188, 20199),
                          'f': (20200, 20210),
                          'mm': (20211, 20224),
                          'tw': (20225, 20235),
                          'mb': (20236, 20245),
                          'm': (20246, 20254),
                          'mh': (20255, 20266),
                          'dt': (20267, 20276),
                          'p': (20277, 20287),
                          'tm': (20288, 20298),
                          'bw': (20299, 20308),
                          'ls': (20309, 20319),
                          'rb': (20320, 20329),
                          'sc': (20330, 20331),
                          'sd': (20341, 20350)}
PSCMenuExpressions = 'EXPRESSIONS'
PSCMenuGreetings = 'GREETINGS'
PSCMenuGoodbyes = 'GOODBYES'
PSCMenuFriendly = 'FRIENDLY'
PSCMenuHappy = 'HAPPY'
PSCMenuSad = 'SAD'
PSCMenuSorry = 'SORRY'
PSCMenuCombat = 'COMBAT'
PSCMenuSeaCombat = 'SEA COMBAT'
PSCMenuPlaces = 'PLACES'
PSCMenuLetsSail = "LET'S SAIL..."
PSCMenuLetsHeadTo = "LET'S HEAD TO..."
PSCMenuHeadToPortRoyal = 'PORT ROYAL'
PSCMenuWhereIs = 'WHERE IS ..?'
PSCMenuWhereIsPortRoyal = 'PORT ROYAL'
PSCMenuWhereIsTortuga = 'TORTUGA'
PSCMenuWhereIsPadresDelFuego = 'PADRES DEL FUEGO'
PSCMenuWhereIsLasPulgas = 'LAS PULGAS'
PSCMenuWhereIsLosPadres = 'LOS PADRES'
PSCMenuDirections = 'DIRECTIONS'
PSCMenuInsults = 'INSULTS'
PSCMenuCompliments = 'COMPLIMENTS'
PSCMenuCardGames = 'CARD GAMES'
PSCMenuPoker = 'POKER'
PSCMenuBlackjack = 'BLACKJACK'
PSCMenuMinigames = 'MINIGAMES'
PSCMenuFishing = 'FISHING'
PSCMenuCannonDefense = 'CANNON DEFENSE'
PSCMenuPotions = 'POTION BREWING'
PSCMenuRepair = 'REPAIR'
PSCMenuInvitations = 'INVITATIONS'
PSCMenuVersusPlayer = 'VERSUS'
PSCMenuHunting = 'HUNTING'
PSCMenuQuests = 'QUESTS'
PSCMenuGM = 'GM'
PSCMenuShips = 'SHIPS'
PSCMenuAdventures = 'ADVENTURE'
GWSCMenuHello = 'GREETINGS'
GWSCMenuBye = 'GOODBYES'
GWSCMenuHappy = 'HAPPY'
GWSCMenuSad = 'SAD'
GWSCMenuPlaces = 'PLACES'
RandomButton = 'Randomize'
TypeANameButton = 'Type Name'
PickANameButton = 'Pick-A-Name'
NameShopSubmitButton = 'Submit'
RejectNameText = 'That name is not allowed. Please try again.'
WaitingForNameSubmission = 'Submitting your name...'
NameShopNameMaster = 'NameMasterEnglish.txt'
NameShopPay = 'Subscribe'
NameShopPlay = 'Free Trial'
NameShopOnlyPaid = 'Only paid users\nmay name their Toons.\nUntil you subscribe\nyour name will be\n'
NameShopContinueSubmission = 'Continue Submission'
NameShopChooseAnother = 'Choose Another Name'
NameShopToonCouncil = 'Your name\nwill be accepted\non next login.  \n' + 'Please re-log to\nget access to\nyour new name\nafter toon creation.'
PleaseTypeName = 'Please type your name:'
ToonAlreadyExists = '%s already exists'
AllNewNames = 'All new names\nmust be approved\nby the Name Council.'
NameShopNameRejected = 'The name you\nsubmitted has\nbeen rejected.'
NameShopNameAccepted = 'Congratulations!\nThe name you\nsubmitted has\nbeen accepted!'
NoPunctuation = "You can't use punctuation marks in your name!"
PeriodOnlyAfterLetter = 'You can use a period in your name, but only after a letter.'
ApostropheOnlyAfterLetter = 'You can use an apostrophe in your name, but only after a letter.'
NoNumbersInTheMiddle = 'Numeric digits may not appear in the middle of a word.'
ThreeWordsOrLess = 'Your name must be three words or fewer.'
CopyrightedNames = ('mickey',
                    'mickey mouse',
                    'mickeymouse',
                    'minnie',
                    'minnie mouse',
                    'minniemouse',
                    'donald',
                    'donald duck',
                    'donaldduck',
                    'pluto',
                    'goofy')
NCTooShort = 'That name is too short.'
NCNoDigits = 'Your name cannot contain numbers.'
NCNeedLetters = 'Each word in your name must contain some letters.'
NCNeedVowels = 'Each word in your name must contain some vowels.'
NCAllCaps = 'Your name cannot be all capital letters.'
NCMixedCase = 'That name has too many capital letters.'
NCBadCharacter = "Your name cannot contain the character '%s'"
NCRepeatedChar = "Your name has too many of the character '%s'"
NCGeneric = 'Sorry, that name will not work.'
NCTooManyWords = 'Your name cannot be more than four words long.'
NCDashUsage = "Dashes may only be used to connect two words together (like in 'Boo-Boo')."
NCCommaEdge = 'Your name may not begin or end with a comma.'
NCCommaAfterWord = 'You may not begin a word with a comma.'
NCCommaUsage = 'That name does not use commas properly. Commas must join two words together, like in the name "Dr. Quack, MD". Commas must also be followed by a space.'
NCPeriodUsage = 'That name does not use periods properly. Periods are only allowed in words like "Mr.", "Mrs.", "J.T.", etc.'
NCApostrophes = 'That name has too many apostrophes.'
AvatarDetailPanelOK = lOK
AvatarDetailPanelCancel = lCancel
AvatarDetailPanelClose = lClose
AvatarDetailPanelLookup = 'Looking up details for %s.'
AvatarDetailPanelFailedLookup = 'Unable to get details for %s.'
AvatarDetailPanelPlayer = 'Player: %(player)s\nWorld: %(world)s\nLocation: %(location)s'
AvatarDetailPanelOnline = 'District: %(district)s\nLocation: %(location)s'
AvatarDetailPanelOffline = 'District: offline\nLocation: offline'
AvatarPanelFriends = 'Friends'
AvatarPanelWhisper = 'Whisper'
AvatarPanelSecrets = 'True Friends'
AvatarPanelGoTo = 'Go To'
AvatarPanelIgnore = 'Ignore'
AvatarPanelStopIgnore = 'Stop Ignoring'
AvatarPanelEndIgnore = 'End Ignore'
AvatarPanelTrade = 'Trade'
AvatarPanelCogLevel = 'Level: %s'
AvatarPanelCogDetailClose = lClose
TeleportPanelOK = lOK
TeleportPanelCancel = lCancel
TeleportPanelYes = lYes
TeleportPanelNo = lNo
TeleportPanelCheckAvailability = 'Trying to go to %s.'
TeleportPanelNotAvailable = '%s is busy right now; try again later.'
TeleportPanelIgnored = '%s is ignoring you.'
TeleportPanelNotOnline = "%s isn't online right now."
TeleportPanelWentAway = '%s went away.'
TeleportPanelUnknownHood = "You don't know how to get to %s!"
TeleportPanelUnavailableHood = '%s is not available right now; try again later.'
TeleportPanelDenySelf = "You can't go to yourself!"
TeleportPanelOtherShard = "%(avName)s is in district %(shardName)s, and you're in district %(myShardName)s.  Do you want to switch to %(shardName)s?"
KartRacingMenuSections = [-1,
                          'PLACES',
                          'RACES',
                          'TRACKS',
                          'COMPLIMENTS',
                          'TAUNTS']
AprilToonsMenuSections = [-1,
                          'GREETINGS',
                          'PLAYGROUNDS',
                          'CHARACTERS',
                          'ESTATES']
SillyHolidayMenuSections = [-1, 'WORLD', 'BATTLE']
CarolMenuSections = [-1]
VictoryPartiesMenuSections = [-1, 'PARTY', 'ITEMS']
GolfMenuSections = [-1,
                    'COURSES',
                    'TIPS',
                    'COMMENTS']
BoardingMenuSections = ['GROUP',
                        "Let's go to...",
                        "We're going to...",
                        -1]
SellbotNerfMenuSections = [-1, 'GROUPING', 'SELLBOT TOWERS/VP']
JellybeanJamMenuSections = ['GET JELLYBEANS', 'SPEND JELLYBEANS']
WinterMenuSections = ['CAROLING', -1]
HalloweenMenuSections = [-1]
SingingMenuSections = [-1]
WhiteListMenu = [-1, 'WHITELIST']
SellbotInvasionMenuSections = [-1]
SellbotFieldOfficeMenuSections = [-1, 'STRATEGY']
IdesOfMarchMenuSections = [-1]
TTAccountCallCustomerService = 'Please call Customer Service at %s.'
TTAccountCustomerServiceHelp = '\nIf you need help, please call Customer Service at %s.'
TTAccountIntractibleError = 'An error occurred.'


def timeElapsedString(timeDelta):
    timeDelta = abs(timeDelta)
    if timeDelta.days > 0:
        if timeDelta.days == 1:
            return '1 day ago'
        else:
            return '%s days ago' % timeDelta.days
    elif timeDelta.seconds / 3600 > 0:
        if timeDelta.seconds / 3600 == 1:
            return '1 hour ago'
        else:
            return '%s hours ago' % (timeDelta.seconds / 3600)
    elif timeDelta.seconds / 60 < 2:
        return '1 minute ago'
    else:
        return '%s minutes ago' % (timeDelta.seconds / 60)
