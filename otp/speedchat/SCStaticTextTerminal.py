from .SCTerminal import SCTerminal
from toontown.chat.SpeedChatLocalizer import SpeedChatPhrases
SCStaticTextMsgEvent = 'SCStaticTextMsg'

def decodeSCStaticTextMsg(textId):
    return SpeedChatPhrases.get(textId, None)


class SCStaticTextTerminal(SCTerminal):

    def __init__(self, textId):
        SCTerminal.__init__(self)
        self.textId = textId
        self.text = SpeedChatPhrases[self.textId]

    def handleSelect(self, displayType=0):
        SCTerminal.handleSelect(self, displayType)
        messenger.send(self.getEventName(SCStaticTextMsgEvent), [self.textId, displayType])
