import sys

from panda3d.core import *

if __debug__:
    if len(sys.argv) == 2 and sys.argv[1] == '--dummy':
        loadPrcFile('config/common.prc')
        loadPrcFile('config/development.prc')

        # The VirtualFileSystem, which has already initialized, doesn't see the mount
        # directives in the config(s) yet. We have to force it to load those manually:
        vfs = VirtualFileSystem.getGlobalPtr()
        mounts = ConfigVariableList('vfs-mount')
        for mount in mounts:
            mountFile, mountPoint = (mount.split(' ', 2) + [None, None, None])[:2]
            vfs.mount(Filename(mountFile), Filename(mountPoint), 0)

import builtins

class game:
    name = 'toontown'
    process = 'client'


builtins.game = game()
import time
import os
import random
import builtins
try:
    launcher
except:
    from toontown.launcher.TTOffDummyLauncher import TTOffDummyLauncher
    launcher = TTOffDummyLauncher()
    builtins.launcher = launcher

launcher.setRegistry('EXIT_PAGE', 'normal')
pollingDelay = 0.5
print('ToontownStart: Polling for game2 to finish...')
while not launcher.getGame2Done():
    time.sleep(pollingDelay)

print('ToontownStart: Game2 is finished.')
print('ToontownStart: Starting the game.')
if launcher.isDummy():
    http = HTTPClient()
else:
    http = launcher.http
tempLoader = Loader()
from direct.gui import DirectGuiGlobals
print('ToontownStart: setting default font')
from . import ToontownGlobals
DirectGuiGlobals.setDefaultFontFunc(ToontownGlobals.getInterfaceFont)
launcher.setPandaErrorCode(7)
from . import ToonBaseEngine
ToonBaseEngine.ToonBaseEngine()
if base.win == None:
    print('Unable to open window; aborting.')
    sys.exit()
launcher.setPandaErrorCode(0)
launcher.setPandaWindowOpen()
ConfigVariableDouble('decompressor-step-time').setValue(0.01)
ConfigVariableDouble('extractor-step-time').setValue(0.01)
base.graphicsEngine.renderFrame()
DirectGuiGlobals.setDefaultRolloverSound(base.loader.loadSfx('phase_3/audio/sfx/GUI_rollover.ogg'))
DirectGuiGlobals.setDefaultClickSound(base.loader.loadSfx('phase_3/audio/sfx/GUI_create_toon_fwd.ogg'))
DirectGuiGlobals.setDefaultDialogGeom(loader.loadModel('phase_3/models/gui/dialog_box_gui'))
from . import TTLocalizer
from otp.otpbase import OTPGlobals
OTPGlobals.setDefaultProductPrefix(TTLocalizer.ProductPrefix)
if base.musicManagerIsValid:
    music = base.musicManager.getSound('phase_3/audio/bgm/tt_theme.ogg')
    print('ToontownStart: Loading default gui sounds')
    DirectGuiGlobals.setDefaultRolloverSound(base.loader.loadSfx('phase_3/audio/sfx/GUI_rollover.ogg'))
    DirectGuiGlobals.setDefaultClickSound(base.loader.loadSfx('phase_3/audio/sfx/GUI_create_toon_fwd.ogg'))
else:
    music = None
from panda3d.core import TextNode
font = loader.loadFont('phase_3/models/fonts/ImpressBT.ttf')
TextNode.setDefaultFont(font)
from . import ToontownLoader
from direct.gui.DirectGui import *
serverVersion = base.config.GetString('server-version', 'no_version_set')
print('ToontownStart: serverVersion: ', serverVersion)
version = OnscreenText(serverVersion, parent=base.a2dBottomLeft, pos=(0.033, 0.025), scale=0.06, fg=Vec4(0, 0, 1, 0.6), align=TextNode.ALeft)
from .ToonBaseGlobal import *
from direct.showbase.MessengerGlobal import *
from toontown.distributed import ToontownClientRepository
cr = ToontownClientRepository.ToontownClientRepository(serverVersion, launcher)
cr.music = music
del music
base.initNametagGlobals()
base.cr = cr
from otp.friends import FriendManager
from otp.distributed.OtpDoGlobals import *
cr.generateGlobalObject(OTP_DO_ID_FRIEND_MANAGER, 'FriendManager')
del tempLoader
version.cleanup()
del version
base.loader = base.loader
builtins.loader = base.loader
autoRun = ConfigVariableBool('toontown-auto-run', 1)
base.discord.startTasks()

from toontown.suit import SuitDNA, DistributedSuitBase

demotedCeo = DistributedSuitBase.DistributedSuitBase(base.cr)
demotedCeo.dna = SuitDNA.SuitDNA()
demotedCeo.dna.newSuit('bgh')
demotedCeo.setDNA(demotedCeo.dna)
demotedCeo.reparentTo(render)
demotedCeo.loop('neutral')
demotedCeo.setPos(-6, 0, 0)
demotedCeo.addActive()
demotedCeo.setDisplayName('Stock Holder\nBossbot\nBoss')
demotedCeo.setH(180)
demotedCeo.doId = 1

demotedCeo2 = DistributedSuitBase.DistributedSuitBase(base.cr)
demotedCeo2.dna = SuitDNA.SuitDNA()
demotedCeo2.dna.newSuit('def')
demotedCeo2.setDNA(demotedCeo2.dna)
demotedCeo2.reparentTo(render)
demotedCeo2.loop('neutral')
demotedCeo2.setPos(-2, 0, 0)
demotedCeo2.addActive()
demotedCeo2.setDisplayName('Head Attorney\nLawbot\nBoss')
demotedCeo2.setH(180)
demotedCeo2.doId = 2

demotedCeo3 = DistributedSuitBase.DistributedSuitBase(base.cr)
demotedCeo3.dna = SuitDNA.SuitDNA()
demotedCeo3.dna.newSuit('ski')
demotedCeo3.setDNA(demotedCeo3.dna)
demotedCeo3.reparentTo(render)
demotedCeo3.loop('neutral')
demotedCeo3.setPos(2, 0, 0)
demotedCeo3.addActive()
demotedCeo3.setDisplayName('Skin Flint\nCashbot\nBoss')
demotedCeo3.setH(180)
demotedCeo3.doId = 3

demotedCeo4 = DistributedSuitBase.DistributedSuitBase(base.cr)
demotedCeo4.dna = SuitDNA.SuitDNA()
demotedCeo4.dna.newSuit('trf')
demotedCeo4.setDNA(demotedCeo4.dna)
demotedCeo4.reparentTo(render)
demotedCeo4.loop('neutral')
demotedCeo4.setPos(6, 0, 0)
demotedCeo4.setH(180)
demotedCeo4.addActive()
demotedCeo4.setDisplayName('Traffic Manager\nSellbot\nBoss')
demotedCeo4.doId = 4

bbhq = loader.loadModel('phase_12/models/bossbotHQ/CogGolfHub')
bbhq.reparentTo(render)
bbhq.setPos(-50, 0, 0)

fog = Fog('BBHQ')

base.camLens.setNearFar(1, 30000)
fog.setColor(0.0, 0.0, 0.0)
fog.setExpDensity(0.004)
render.clearFog()
render.setFog(fog)

#set the camera fov
base.camLens.setFov(100)

if autoRun and launcher.isDummy() and (not Thread.isTrueThreads() or __name__ == '__main__'):
    try:
        base.run()
        base.enableMouse()
    except SystemExit:
        raise
    except:
        from otp.otpbase import PythonUtil
        print(PythonUtil.describeException())
        raise