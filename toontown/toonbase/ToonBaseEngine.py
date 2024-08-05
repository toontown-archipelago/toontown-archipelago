import typing

from direct.showbase.MessengerGlobal import messenger

from otp.otpbase import OTPBase
from otp.otpbase import OTPLauncherGlobals
from otp.otpbase import OTPGlobals
from direct.showbase.PythonUtil import *
from direct.showbase.InputStateGlobal import inputState
from . import ToontownGlobals
from direct.directnotify import DirectNotifyGlobal
from . import ToontownLoader
from direct.gui import DirectGuiGlobals
from direct.gui.DirectGui import *
from panda3d.core import *
from libotp import *
import sys
import os
import math
from toontown.discord.DiscordRPC import DiscordRPC
from toontown.toonbase import ToontownAccess
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownBattleGlobals
from toontown.launcher import ToontownDownloadWatcher
import tempfile
import atexit
import shutil
import time

import toontown.archipelago.util.global_text_properties as global_text_properties
from .ErrorTrackingService import ErrorTrackingService, SentryErrorTrackingService, ServiceType
from ..settings.Settings import Settings, ControlSettings

if typing.TYPE_CHECKING:
    from toontown.toonbase.ToonBaseGlobals import *


class ToonBaseEngine(OTPBase.OTPBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('ToonBaseEngine')

    def __init__(self):

        version = self.config.GetString('version', 'v???')
        self.errorReportingService: ErrorTrackingService = SentryErrorTrackingService(ServiceType.CLIENT, version)

        self.global_text_properties = global_text_properties

        self.settings = Settings()
        self.setMultiThreading()

        os.environ['WANT_ERROR_REPORTING'] = 'true' if self.settings.get('report-errors') else 'false'

        antialias = self.settings.get("anti-aliasing")
        mode = self.settings.get("borderless")
        music = self.settings.get("music")
        sfx = self.settings.get("sfx")
        toonChatSounds = self.settings.get("toon-chat-sounds")
        musicVol = self.settings.get("music-volume")
        sfxVol = self.settings.get("sfx-volume")
        res = self.settings.get("resolution")
        fpsMeter = self.settings.get("frame-rate-meter")  # or __debug__
        fpsLimit = self.settings.get("fps-limit")

        loadPrcFileData("toonBase Settings Window Res", f"win-size {res[0]} {res[1]}")
        loadPrcFileData("toonBase Settings Window Borderless", f"undecorated {mode}")
        loadPrcFileData("toonBase Settings Music Active", f"audio-music-active {music}")
        loadPrcFileData("toonBase Settings Sound Active", f"audio-sfx-active {sfx}")
        loadPrcFileData("toonBase Settings Music Volume", f"audio-master-music-volume {musicVol}")
        loadPrcFileData("toonBase Settings Sfx Volume", f"audio-master-sfx-volume {sfxVol}")
        loadPrcFileData("toonBase Settings Toon Chat Sounds", f"toon-chat-sounds {toonChatSounds}")
        loadPrcFileData("toonBase Settings Frame Rate Meter", f"show-frame-rate-meter {fpsMeter}")
        if antialias:
            loadPrcFileData("toonBase Settings Framebuffer MSAA", "framebuffer-multisample 1")
            loadPrcFileData("toonBase Settings MSAA Level", f"multisamples {antialias}")
        else:
            loadPrcFileData("toonBase Settings Framebuffer MSAA", "framebuffer-multisample 0")

        OTPBase.OTPBase.__init__(self)
        if not self.isMainWindowOpen():
            try:
                launcher.setPandaErrorCode(7)
            except:
                pass

            sys.exit(1)
        #self.disableShowbaseMouse()
        self.addCullBins()
        base.debugRunningMultiplier /= OTPGlobals.ToonSpeedFactor
        self.toonChatSounds = self.config.GetBool('toon-chat-sounds', 1)
        self.placeBeforeObjects = config.GetBool('place-before-objects', 0)
        self.endlessQuietZone = False
        self.wantDynamicShadows = 0
        self.exitErrorCode = 0
        camera.setPosHpr(0, 0, 0, 0, 0, 0)
        self.camLens.setMinFov(ToontownGlobals.DefaultCameraFov / (4. / 3.))
        self.camLens.setNearFar(ToontownGlobals.DefaultCameraNear, ToontownGlobals.DefaultCameraFar)
        self.musicManager.setVolume(musicVol ** 2)
        for sfm in self.sfxManagerList:
            sfm.setVolume(sfxVol ** 2)
        self.setBackgroundColor(ToontownGlobals.DefaultBackgroundColor)
        tpm = TextPropertiesManager.getGlobalPtr()
        candidateActive = TextProperties()
        candidateActive.setTextColor(0, 0, 1, 1)
        tpm.setProperties('candidate_active', candidateActive)
        candidateInactive = TextProperties()
        candidateInactive.setTextColor(0.3, 0.3, 0.7, 1)
        tpm.setProperties('candidate_inactive', candidateInactive)
        self.transitions.IrisModelName = 'phase_3/models/misc/iris'
        self.transitions.FadeModelName = 'phase_3/models/misc/fade'
        self.exitFunc = self.userExit
        if 'launcher' in __builtins__ and launcher:
            launcher.setPandaErrorCode(11)
        globalClock.setMaxDt(0.2)
        if fpsLimit != 0:
            globalClock.setMode(ClockObject.MLimited)
            globalClock.setFrameRate(fpsLimit)
        else:
            globalClock.setMode(ClockObject.MNormal)
        if self.config.GetBool('want-particles', 1) == 1:
            self.notify.debug('Enabling particles')
            self.enableParticles()
        self.accept(ToontownGlobals.ScreenshotHotkey, self.takeScreenShot)
        self.accept('f4', self.toggleNameTags)
        self.accept('f3', self.toggleGui)
        self.accept('panda3d-render-error', self.panda3dRenderError)
        oldLoader = self.loader
        self.loader = ToontownLoader.ToontownLoader(self)
        __builtins__['loader'] = self.loader
        oldLoader.destroy()
        self.accept('PandaPaused', self.disableAllAudio)
        self.accept('PandaRestarted', self.enableAllAudio)
        self.friendMode = self.config.GetBool('switchboard-friends', 0)
        self.wantPets = self.config.GetBool('want-pets', 1)
        self.wantBingo = self.config.GetBool('want-fish-bingo', 1)
        self.wantKarts = self.config.GetBool('want-karts', 1)
        self.wantNewSpecies = self.config.GetBool('want-new-species', 0)
        self.inactivityTimeout = self.config.GetFloat('inactivity-timeout', ToontownGlobals.KeyboardTimeout)
        if self.inactivityTimeout:
            self.notify.debug('Enabling Panda timeout: %s' % self.inactivityTimeout)
            self.mouseWatcherNode.setInactivityTimeout(self.inactivityTimeout)
        self.randomMinigameAbort = self.config.GetBool('random-minigame-abort', 0)
        self.randomMinigameDisconnect = self.config.GetBool('random-minigame-disconnect', 0)
        self.randomMinigameNetworkPlugPull = self.config.GetBool('random-minigame-netplugpull', 0)
        self.autoPlayAgain = self.config.GetBool('auto-play-again', 0)
        self.skipMinigameReward = self.config.GetBool('skip-minigame-reward', 0)
        self.wantMinigameDifficulty = self.config.GetBool('want-minigame-difficulty', 0)
        self.minigameDifficulty = self.config.GetFloat('minigame-difficulty', -1.0)
        if self.minigameDifficulty == -1.0:
            del self.minigameDifficulty
        self.minigameSafezoneId = self.config.GetInt('minigame-safezone-id', -1)
        if self.minigameSafezoneId == -1:
            del self.minigameSafezoneId
        cogdoGameSafezoneId = self.config.GetInt('cogdo-game-safezone-id', -1)
        cogdoGameDifficulty = self.config.GetFloat('cogdo-game-difficulty', -1)
        if cogdoGameDifficulty != -1:
            self.cogdoGameDifficulty = cogdoGameDifficulty
        if cogdoGameSafezoneId != -1:
            self.cogdoGameSafezoneId = cogdoGameSafezoneId
        ToontownBattleGlobals.SkipMovie = self.config.GetBool('skip-battle-movies', 0)
        self.creditCardUpFront = self.config.GetInt('credit-card-up-front', -1)
        if self.creditCardUpFront == -1:
            del self.creditCardUpFront
        else:
            self.creditCardUpFront = self.creditCardUpFront != 0
        self.housingEnabled = self.config.GetBool('want-housing', 1)
        self.cannonsEnabled = self.config.GetBool('estate-cannons', 0)
        self.fireworksEnabled = self.config.GetBool('estate-fireworks', 0)
        self.dayNightEnabled = self.config.GetBool('estate-day-night', 0)
        self.cloudPlatformsEnabled = self.config.GetBool('estate-clouds', 0)
        self.greySpacing = self.config.GetBool('allow-greyspacing', 0)
        self.goonsEnabled = self.config.GetBool('estate-goon', 0)
        self.restrictTrialers = self.config.GetBool('restrict-trialers', 1)
        self.roamingTrialers = self.config.GetBool('roaming-trialers', 1)
        self.slowQuietZone = self.config.GetBool('slow-quiet-zone', 0)
        self.slowQuietZoneDelay = self.config.GetFloat('slow-quiet-zone-delay', 5)
        self.killInterestResponse = self.config.GetBool('kill-interest-response', 0)
        tpMgr = TextPropertiesManager.getGlobalPtr()
        WLDisplay = TextProperties()
        WLDisplay.setSlant(0.3)
        WLEnter = TextProperties()
        WLEnter.setTextColor(1.0, 0.0, 0.0, 1)
        tpMgr.setProperties('WLDisplay', WLDisplay)
        tpMgr.setProperties('WLEnter', WLEnter)
        del tpMgr
        self.lastScreenShotTime = globalClock.getRealTime()
        self.accept('InputState-forward', self.__walking)
        self.canScreenShot = 1
        self.glitchCount = 0
        self.walking = 0
        self.oldX = max(1, base.win.getXSize())
        self.oldY = max(1, base.win.getYSize())
        self.aspectRatio = float(self.oldX) / self.oldY
        self.aspect2d.setAntialias(AntialiasAttrib.MMultisample)

        self.WANT_FOV_EFFECTS = self.settings.get('fovEffects')
        self.CAM_TOGGLE_LOCK = self.settings.get('cam-toggle-lock')
        self.WANT_LEGACY_MODELS = self.settings.get('want-legacy-models')
        self.wantRichPresence = self.settings.get('discord-rich-presence')
        self.colorBlindMode = self.settings.get('color-blind-mode')
        self.discord = DiscordRPC()
        self.discord.launching()
        self.ap_version_text = OnscreenText(text=f"Toontown: Archipelago {version}", parent=self.a2dBottomLeft, pos=(.3, .05), mayChange=False, sort=-100, scale=.04, fg=(1, 1, 1, .3), shadow=(0, 0, 0, .3), align=TextNode.ALeft)

        self.enableHotkeys()

        self.setAntiAliasing()
        self.setAnisotropicFilter()
        self.setVerticalSync()
        self.setRichPresence()

        if base.config.GetBool('want-injector', False):
            from ..util.dev.Injector import DeveloperInjector
            DeveloperInjector().start()

    def openMainWindow(self, *args, **kw):
        result = OTPBase.OTPBase.openMainWindow(self, *args, **kw)
        self.setCursorAndIcon()
        return result

    def setCursorAndIcon(self):
        tempdir = tempfile.mkdtemp()
        atexit.register(shutil.rmtree, tempdir)
        vfs = VirtualFileSystem.getGlobalPtr()

        searchPath = DSearchPath()
        searchPath.appendDirectory(Filename('/phase_3/models/gui'))

        for filename in ['toonmono.cur', 'icon.ico']:
            p3filename = Filename(filename)
            found = vfs.resolveFilename(p3filename, searchPath)
            if not found:
                return # Can't do anything past this point.

            with open(os.path.join(tempdir, filename), 'wb') as f:
                f.write(vfs.readFile(p3filename, False))

        wp = WindowProperties()
        wp.setCursorFilename(Filename.fromOsSpecific(os.path.join(tempdir, 'toonmono.cur')))
        wp.setIconFilename(Filename.fromOsSpecific(os.path.join(tempdir, 'icon.ico')))
        self.win.requestProperties(wp)

    def windowEvent(self, win):
        OTPBase.OTPBase.windowEvent(self, win)
        if not config.GetInt('keep-aspect-ratio', 0):
            return
        x = max(1, win.getXSize())
        y = max(1, win.getYSize())
        maxX = base.pipe.getDisplayWidth()
        maxY = base.pipe.getDisplayHeight()
        cwp = win.getProperties()
        originX = 0
        originY = 0
        if cwp.hasOrigin():
            originX = cwp.getXOrigin()
            originY = cwp.getYOrigin()
            if originX > maxX:
                originX = originX - maxX
            if originY > maxY:
                oringY = originY - maxY
        maxX -= originX
        maxY -= originY
        if math.fabs(x - self.oldX) > math.fabs(y - self.oldY):
            newY = x / self.aspectRatio
            newX = x
            if newY > maxY:
                newY = maxY
                newX = self.aspectRatio * maxY
        else:
            newX = self.aspectRatio * y
            newY = y
            if newX > maxX:
                newX = maxX
                newY = maxX / self.aspectRatio
        wp = WindowProperties()
        wp.setSize(newX, newY)
        base.win.requestProperties(wp)
        base.cam.node().getLens().setFilmSize(newX, newY)
        self.oldX = newX
        self.oldY = newY

    def disableShowbaseMouse(self):
        self.useDrive()
        self.disableMouse()
        if self.mouseInterface:
            self.mouseInterface.detachNode()
        if base.mouse2cam:
            self.mouse2cam.detachNode()

    def addCullBins(self):
        cullBinMgr = CullBinManager.getGlobalPtr()
        cullBinMgr.addBin('gui-popup', CullBinManager.BTUnsorted, 60)
        cullBinMgr.addBin('shadow', CullBinManager.BTFixed, 15)
        cullBinMgr.addBin('ground', CullBinManager.BTFixed, 14)

    def __walking(self, pressed):
        self.walking = pressed

    def toggleNameTags(self):
        nametags3d = render.findAllMatches('**/nametag3d')
        nametags2d = render2d.findAllMatches('**/Nametag2d')
        hide = False
        # Check if anything we're supposed to hide is visible
        for nametag in nametags2d:
            if not nametag.isHidden():
                hide = True
        for nametag in nametags3d:
            if not nametag.isHidden():
                hide = True

        # If anything is visible, hide, else we will show everything
        for nametag in nametags3d:
            if hide:
                nametag.hide()
            else:
                nametag.show()
        for nametag in nametags2d:
            if hide:
                nametag.hide()
            else:
                nametag.show()

    def toggleGui(self):
        if aspect2d.isHidden():
            base.transitions.noFade()
            aspect2d.show()
        else:
            aspect2d.hide()
            base.transitions.fadeScreen(alpha=0.01)

    def takeScreenShot(self):
        if not os.path.exists('screenshots/'):
            os.mkdir('screenshots/')

        namePrefix = 'screenshots/' + launcher.logPrefix + 'screenshot-%i.png' % time.time()
        timedif = globalClock.getRealTime() - self.lastScreenShotTime
        if self.glitchCount > 10 and self.walking:
            return
        if timedif < 1.0 and self.walking:
            self.glitchCount += 1
            return
        if not hasattr(self, 'localAvatar'):
            self.screenshot(namePrefix=namePrefix, defaultFilename=0)
            self.lastScreenShotTime = globalClock.getRealTime()
            return
        coordOnScreen = self.config.GetBool('screenshot-coords', 0)
        self.localAvatar.stopThisFrame = 1
        ctext = self.localAvatar.getAvPosStr()
        self.screenshotStr = ''
        messenger.send('takingScreenshot')
        if coordOnScreen:
            coordTextLabel = DirectLabel(pos=(-0.81, 0.001, -0.87), text=ctext, text_scale=0.05, text_fg=VBase4(1.0, 1.0, 1.0, 1.0), text_bg=(0, 0, 0, 0), text_shadow=(0, 0, 0, 1), relief=None)
            coordTextLabel.setBin('gui-popup', 0)
            strTextLabel = None
            if len(self.screenshotStr):
                strTextLabel = DirectLabel(pos=(0.0, 0.001, 0.9), text=self.screenshotStr, text_scale=0.05, text_fg=VBase4(1.0, 1.0, 1.0, 1.0), text_bg=(0, 0, 0, 0), text_shadow=(0, 0, 0, 1), relief=None)
                strTextLabel.setBin('gui-popup', 0)
        self.graphicsEngine.renderFrame()
        self.screenshot(namePrefix=namePrefix, defaultFilename=0, imageComment=ctext + ' ' + self.screenshotStr)
        self.lastScreenShotTime = globalClock.getRealTime()
        if coordOnScreen:
            if strTextLabel is not None:
                strTextLabel.destroy()
            coordTextLabel.destroy()
        return

    def addScreenshotString(self, str):
        if len(self.screenshotStr):
            self.screenshotStr += '\n'
        self.screenshotStr += str

    def initNametagGlobals(self):
        arrow = loader.loadModel('phase_3/models/props/arrow')
        card = loader.loadModel('phase_3/models/props/panel')
        speech3d = ChatBalloon(loader.loadModel('phase_3/models/props/chatbox').node())
        thought3d = ChatBalloon(loader.loadModel('phase_3/models/props/chatbox_thought_cutout').node())
        speech2d = ChatBalloon(loader.loadModel('phase_3/models/props/chatbox_noarrow').node())
        chatButtonGui = loader.loadModel('phase_3/models/gui/chat_button_gui')
        NametagGlobals.setCamera(self.cam)
        NametagGlobals.setArrowModel(arrow)
        NametagGlobals.setNametagCard(card, VBase4(-0.5, 0.5, -0.5, 0.5))
        if self.mouseWatcherNode:
            NametagGlobals.setMouseWatcher(self.mouseWatcherNode)
        NametagGlobals.setSpeechBalloon3d(speech3d)
        NametagGlobals.setThoughtBalloon3d(thought3d)
        NametagGlobals.setSpeechBalloon2d(speech2d)
        NametagGlobals.setThoughtBalloon2d(thought3d)
        NametagGlobals.setPageButton(PGButton.SReady, chatButtonGui.find('**/Horiz_Arrow_UP'))
        NametagGlobals.setPageButton(PGButton.SDepressed, chatButtonGui.find('**/Horiz_Arrow_DN'))
        NametagGlobals.setPageButton(PGButton.SRollover, chatButtonGui.find('**/Horiz_Arrow_Rllvr'))
        NametagGlobals.setQuitButton(PGButton.SReady, chatButtonGui.find('**/CloseBtn_UP'))
        NametagGlobals.setQuitButton(PGButton.SDepressed, chatButtonGui.find('**/CloseBtn_DN'))
        NametagGlobals.setQuitButton(PGButton.SRollover, chatButtonGui.find('**/CloseBtn_Rllvr'))
        rolloverSound = DirectGuiGlobals.getDefaultRolloverSound()
        if rolloverSound:
            NametagGlobals.setRolloverSound(rolloverSound)
        clickSound = DirectGuiGlobals.getDefaultClickSound()
        if clickSound:
            NametagGlobals.setClickSound(clickSound)
        NametagGlobals.setToon(self.cam)
        self.marginManager = MarginManager()
        self.margins = self.aspect2d.attachNewNode(self.marginManager, DirectGuiGlobals.MIDGROUND_SORT_INDEX + 1)
        mm = self.marginManager
        self.leftCells = [mm.addGridCell(0, 1, -1.33333333333, 1.33333333333, -1.0, 1.0, base.a2dTopLeft, (0.222222, 0, -1.5)), mm.addGridCell(0, 2, -1.33333333333, 1.33333333333, -1.0, 1.0, base.a2dTopLeft, (0.222222, 0, -1.16667)), mm.addGridCell(0, 3, -1.33333333333, 1.33333333333, -1.0, 1.0, base.a2dTopLeft, (0.222222, 0, -0.833333))]
        self.bottomCells = [mm.addGridCell(0.5, 0, -1.33333333333, 1.33333333333, -1.0, 1.0, base.a2dBottomCenter, (-0.888889, 0, 0.166667)),
         mm.addGridCell(1.5, 0, -1.33333333333, 1.33333333333, -1.0, 1.0, base.a2dBottomCenter, (-0.444444, 0, 0.166667)),
         mm.addGridCell(2.5, 0, -1.33333333333, 1.33333333333, -1.0, 1.0, base.a2dBottomCenter, (0, 0, 0.166667)),
         mm.addGridCell(3.5, 0, -1.33333333333, 1.33333333333, -1.0, 1.0, base.a2dBottomCenter, (0.444444, 0, 0.166667)),
         mm.addGridCell(4.5, 0, -1.33333333333, 1.33333333333, -1.0, 1.0, base.a2dBottomCenter, (0.888889, 0, 0.166667))]
        self.rightCells = [mm.addGridCell(5, 2, -1.33333333333, 1.33333333333, -1.0, 1.0, base.a2dTopRight, (-0.222222, 0, -1.16667)), mm.addGridCell(5, 1, -1.33333333333, 1.33333333333, -1.0, 1.0, base.a2dTopRight, (-0.222222, 0, -1.5))]
        self.marginManager.setCellAvailable(self.leftCells[0], 0)

    def setCellsAvailable(self, cell_list, available):
        for cell in cell_list:
            if cell is self.leftCells[0]:
                continue
            self.marginManager.setCellAvailable(cell, available)

    def cleanupDownloadWatcher(self):
        self.downloadWatcher.cleanup()
        self.downloadWatcher = None
        return

    def startShow(self, cr, launcherServer = None):
        self.cr = cr
        if base.config.GetBool('framebuffer-multisample', False):
            render.setAntialias(AntialiasAttrib.MAuto)
        base.graphicsEngine.renderFrame()
        self.downloadWatcher = ToontownDownloadWatcher.ToontownDownloadWatcher(TTLocalizer.LauncherPhaseNames)
        if launcher.isDownloadComplete():
            self.cleanupDownloadWatcher()
        else:
            self.acceptOnce('launcherAllPhasesComplete', self.cleanupDownloadWatcher)
        gameServer = base.config.GetString('game-server', '')
        if gameServer:
            self.notify.info('Using game-server from Configrc: %s ' % gameServer)
        elif launcherServer:
            gameServer = launcherServer
            self.notify.info('Using gameServer from launcher: %s ' % gameServer)
        else:
            gameServer = '127.0.0.1'
        serverPort = base.config.GetInt('server-port', 7198)
        serverList = []
        for name in gameServer.split(';'):
            url = URLSpec(name, 1)
            if config.GetBool('want-ssl', False):
                url.setScheme('s')
            if not url.hasPort():
                url.setPort(serverPort)
            serverList.append(url)

        if len(serverList) == 1:
            failover = base.config.GetString('server-failover', '')
            serverURL = serverList[0]
            for arg in failover.split():
                try:
                    port = int(arg)
                    url = URLSpec(serverURL)
                    url.setPort(port)
                except:
                    url = URLSpec(arg, 1)

                if url != serverURL:
                    serverList.append(url)

        cr.loginFSM.request('connect', [serverList])
        self.ttAccess = ToontownAccess.ToontownAccess()
        self.ttAccess.initModuleInfo()

    def removeGlitchMessage(self):
        self.ignore('InputState-forward')
        print('ignoring InputState-forward')

    def exitShow(self, errorCode = None):
        self.notify.info('Exiting Toontown: errorCode = %s' % errorCode)
        if errorCode:
            launcher.setPandaErrorCode(errorCode)
        else:
            launcher.setPandaErrorCode(0)
        sys.exit()

    def setExitErrorCode(self, code):
        self.exitErrorCode = code
        if os.name == 'nt':
            exitCode2exitPage = {OTPLauncherGlobals.ExitEnableChat: 'chat',
             OTPLauncherGlobals.ExitSetParentPassword: 'setparentpassword',
             OTPLauncherGlobals.ExitPurchase: 'purchase'}
            if code in exitCode2exitPage:
                launcher.setRegistry('EXIT_PAGE', exitCode2exitPage[code])

    def getExitErrorCode(self):
        return self.exitErrorCode

    def userExit(self):
        try:
            self.localAvatar.d_setAnimState('TeleportOut', 1)
        except:
            pass

        if hasattr(self, 'ttAccess'):
            self.ttAccess.delete()
        if self.cr.timeManager:
            self.cr.timeManager.setDisconnectReason(ToontownGlobals.DisconnectCloseWindow)
        base.cr._userLoggingOut = False
        try:
            localAvatar
        except:
            pass
        else:
            messenger.send('clientLogout')
            self.cr.dumpAllSubShardObjects()

        self.cr.loginFSM.request('shutdown')
        self.notify.warning('Could not request shutdown; exiting anyway.')
        self.exitShow()

    def panda3dRenderError(self):
        launcher.setPandaErrorCode(14)
        if self.cr.timeManager:
            self.cr.timeManager.setDisconnectReason(ToontownGlobals.DisconnectGraphicsError)
        self.cr.sendDisconnect()
        sys.exit()

    def getShardPopLimits(self):
        if self.cr.productName == 'JP':
            return (config.GetInt('shard-low-pop', ToontownGlobals.LOW_POP_JP), config.GetInt('shard-mid-pop', ToontownGlobals.MID_POP_JP), config.GetInt('shard-high-pop', ToontownGlobals.HIGH_POP_JP))
        elif self.cr.productName in ['BR', 'FR']:
            return (config.GetInt('shard-low-pop', ToontownGlobals.LOW_POP_INTL), config.GetInt('shard-mid-pop', ToontownGlobals.MID_POP_INTL), config.GetInt('shard-high-pop', ToontownGlobals.HIGH_POP_INTL))
        else:
            return (config.GetInt('shard-low-pop', ToontownGlobals.LOW_POP), config.GetInt('shard-mid-pop', ToontownGlobals.MID_POP), config.GetInt('shard-high-pop', ToontownGlobals.HIGH_POP))

    def playMusic(self, music, looping = 0, interrupt = 1, volume = None, time = 0.0):
        OTPBase.OTPBase.playMusic(self, music, looping, interrupt, volume, time)

    @property
    def controls(self) -> ControlSettings:
        return self.settings.controls

    def acceptHotkeys(self) -> None:
        # Accept the screenshot key
        self.accept(self.controls.SCREENSHOT, self.takeScreenShot)
        self.accept(
            self.controls.MAP_PAGE_HOTKEY,
            messenger.send,
            extraArgs=[ToontownGlobals.StickerBookHotkey]
        )
        self.accept(
            self.controls.FRIENDS_LIST_HOTKEY,
            messenger.send,
            extraArgs=[ToontownGlobals.FriendsListHotkey]
        )
        self.accept(
            self.controls.STREET_MAP_HOTKEY,
            messenger.send,
            extraArgs=[ToontownGlobals.MapHotkey]
        )
        self.accept(
            self.controls.INVENTORY_HOTKEY,
            messenger.send,
            extraArgs=[ToontownGlobals.InventoryHotkeyOn]
        )
        self.accept(
            f"{self.controls.INVENTORY_HOTKEY}-up",
            messenger.send,
            extraArgs=[ToontownGlobals.InventoryHotkeyOff]
        )
        self.accept(
            self.controls.QUEST_HOTKEY,
            messenger.send,
            extraArgs=[ToontownGlobals.QuestsHotkeyOn]
        )
        self.accept(
            f"{self.controls.QUEST_HOTKEY}-up",
            messenger.send,
            extraArgs=[ToontownGlobals.QuestsHotkeyOff]
        )
        self.accept(
            self.controls.GALLERY_HOTKEY,
            messenger.send,
            extraArgs=[ToontownGlobals.GalleryHotkeyOn]
        )
        self.accept(
            f"{self.controls.GALLERY_HOTKEY}-up",
            messenger.send,
            extraArgs=[ToontownGlobals.GalleryHotkeyOff]
        )
        self.accept(
            self.controls.CHAT_HOTKEY,
            messenger.send,
            extraArgs=["enterNormalChat"]
        )
        self.accept(
            self.controls.MOVE_LEFT,
            messenger.send,
            extraArgs=[ToontownGlobals.StickerBookPageLeft]
        )
        self.accept(
            self.controls.MOVE_RIGHT,
            messenger.send,
            extraArgs=[ToontownGlobals.StickerBookPageRight]
        )

    def ignoreHotkeys(self) -> None:
        # Ignore the screenshot key
        self.ignore(self.controls.SCREENSHOT)
        self.ignore(self.controls.MAP_PAGE_HOTKEY)
        self.ignore(self.controls.FRIENDS_LIST_HOTKEY)
        self.ignore(self.controls.STREET_MAP_HOTKEY)
        self.ignore(self.controls.INVENTORY_HOTKEY)
        self.ignore(f"{self.controls.INVENTORY_HOTKEY}-up")
        self.ignore(self.controls.QUEST_HOTKEY)
        self.ignore(f"{self.controls.QUEST_HOTKEY}-up")
        self.ignore(self.controls.GALLERY_HOTKEY)
        self.ignore(f"{self.controls.GALLERY_HOTKEY}-up")
        self.ignore(self.controls.CHAT_HOTKEY)
        self.ignore(self.controls.MOVE_LEFT)
        self.ignore(self.controls.MOVE_RIGHT)

    def enableHotkeys(self) -> None:
        self.ignore("enable-hotkeys")
        self.acceptHotkeys()
        self.accept("disable-hotkeys", self.disableHotkeys)

    def disableHotkeys(self) -> None:
        self.ignore("disable-hotkeys")
        self.ignoreHotkeys()
        self.accept("enable-hotkeys", self.enableHotkeys)

    def setRichPresence(self) -> None:
        if self.wantRichPresence:
            self.discord.enable()
        else:
            self.discord.disable()

    def setAntiAliasing(self) -> None:
        antialias = self.settings.get("anti-aliasing")
        if antialias != 0:
            loadPrcFileData("", "framebuffer-multisample 1")
            loadPrcFileData("", f"multisamples {antialias}")
            self.render.setAntialias(AntialiasAttrib.MMultisample, antialias)
            self.aspect2d.setAntialias(AntialiasAttrib.MMultisample, antialias)
        else:
            loadPrcFileData("", "framebuffer-multisample 0")
            loadPrcFileData("", "multisamples 0")
            self.render.setAntialias(AntialiasAttrib.MNone)
            self.aspect2d.setAntialias(AntialiasAttrib.MNone)

    def setAnisotropicFilter(self) -> None:
        level = self.settings.get("anisotropic-filter")
        loadPrcFileData('', f'texture-anisotropic-degree {level}')

    def setVerticalSync(self) -> None:
        vsync = self.settings.get("vertical-sync")
        loadPrcFileData('', f'sync-video {vsync}')

    def setMultiThreading(self) -> None:
        # It is current year, and multithreading has improved stability wise
        # Still experimental, but for documentation's sake, let's add this in
        multithread = self.settings.get("experimental-multithreading")
        if multithread == True:
            loadPrcFileData('', 'threading-model Cull/Draw')
            print('===============================================================')
            print('Warning! You are running this game with multithreading enabled.')
            print('While this option yields performance gains, it can be unstable.')
            print('Please do not report any issues that may be')
            print('caused exclusively from using this setting.')
            print('===============================================================')

    def updateDisplay(self) -> None:
        self.setAntiAliasing()
        self.setAnisotropicFilter()
        self.setVerticalSync()

        xSize, ySize = self.settings.get("resolution")
        borderless = self.settings.get("borderless")

        properties = WindowProperties()
        properties.setSize(xSize, ySize)
        properties.set_undecorated(borderless)

        # Force all the textures to reload.
        gsg = self.win.getGsg()
        if gsg:
            self.render.prepareScene(gsg)
            render2d.prepareScene(gsg)
            aspect2d.prepareScene(gsg)

        if not self.openMainWindow(props=properties, gsg=gsg, keepCamera=True):
            self.notify.error(f"Failed to update display in self.updateDisplay()")
            return

        #self.disableShowbaseMouse()
        NametagGlobals.setCamera(self.cam)
        NametagGlobals.setMouseWatcher(self.mouseWatcherNode)

        # Force a frame to render for good measure.  This should
        # force the window open right now, which helps us avoid
        # starting the countdown timer before the window is open.
        # Also, we can check to see if the window actually opened
        # or not.
        self.graphicsEngine.renderFrame()
        self.graphicsEngine.renderFrame()
        self.graphicsEngine.openWindows()

    @property
    def possibleScreenSizes(self) -> list[list[int]]:
        screenSizes = []

        displayInfo = self.pipe.getDisplayInformation()

        for i in range(displayInfo.getTotalDisplayModes()):
            width = displayInfo.getDisplayModeWidth(i)
            height = displayInfo.getDisplayModeHeight(i)
            size = [width, height]
            if size not in screenSizes:
                screenSizes.append(size)

        return sorted(screenSizes)
