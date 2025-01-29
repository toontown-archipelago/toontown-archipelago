from otp.speedchat.SCTerminal import *
from toontown.chat.SpeedChatLocalizer import SpeedChatPhrases
TTSCIndexedMsgEvent = 'SCIndexedMsg'

def decodeTTSCIndexedMsg(msgIndex):
    return SpeedChatPhrases.get(msgIndex, None)


class TTSCIndexedTerminal(SCTerminal):

    def __init__(self, msg, msgIndex):
        SCTerminal.__init__(self)
        self.text = msg
        self.msgIndex = msgIndex

    def handleSelect(self, displayType=0):
        SCTerminal.handleSelect(self)
        messenger.send(self.getEventName(TTSCIndexedMsgEvent), [self.msgIndex])
