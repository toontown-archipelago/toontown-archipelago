from direct.showbase import DConfig
from direct.showbase.Loader import Loader
from direct.showbase.Messenger import Messenger
from direct.task.Task import TaskManager
from panda3d.core import Camera, ClockObject, NodePath

from otp.launcher.LauncherBase import LauncherBase
from toontown.distributed.ToontownClientRepository import ToontownClientRepository
from toontown.toon.LocalToon import LocalToon
from toontown.toonbase.ToonBase import ToonBase

base: ToonBase
config: DConfig
loader: Loader
camera: Camera
localAvatar: LocalToon
launcher: LauncherBase
globalClock: ClockObject
taskMgr: TaskManager
messenger: Messenger

cr: ToontownClientRepository

render: NodePath
hidden: NodePath
aspect2d: NodePath
render2d: NodePath
