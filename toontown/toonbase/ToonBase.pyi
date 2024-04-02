from panda3d.core import NodePath

from otp.otpbase.OTPBase import OTPBase
from toontown.distributed.ToontownClientRepository import ToontownClientRepository
from toontown.toon.LocalToon import LocalToon


class ToonBase(OTPBase):

    localAvatar: LocalToon
    aspect2d: NodePath
    cr: ToontownClientRepository
