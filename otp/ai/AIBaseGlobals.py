from direct.showbase import DConfig
from direct.showbase.Loader import Loader
from panda3d.core import Camera, ClockObject

from otp.ai.AIBase import AIBase
from toontown.distributed.ToontownInternalRepository import ToontownInternalRepository

simbase: AIBase
config: DConfig
loader: Loader
camera: Camera
globalClock: ClockObject
