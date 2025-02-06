from direct.showbase import PythonUtil
from otp.speedchat.SCMenu import SCMenu
from otp.speedchat.SCMenuHolder import SCMenuHolder
from otp.speedchat.SCStaticTextTerminal import SCStaticTextTerminal
from otp.otpbase import OTPLocalizer

class TTSCBoardingMenu(SCMenu):

    def __init__(self, zoneId):
        SCMenu.__init__(self)
        self.__boardingMessagesChanged(zoneId)

    def destroy(self):
        SCMenu.destroy(self)

    def clearMenu(self):
        SCMenu.clearMenu(self)

    def __boardingMessagesChanged(self, zoneId):
        self.clearMenu()
