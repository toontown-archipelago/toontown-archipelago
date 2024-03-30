from direct.gui import DirectGuiGlobals

from otp.speedchat.SCTerminal import SCTerminal
from toontown.chat import ResistanceChat
TTSCResistanceMsgEvent = 'TTSCResistanceMsg'


def decodeTTSCResistanceMsg(textId):
    return ResistanceChat.getChatText(textId)


class TTSCResistanceTerminal(SCTerminal):

    def __init__(self, textId, charges):
        SCTerminal.__init__(self)
        self.setCharges(charges)
        self.textId = textId
        self.text = ResistanceChat.getItemText(self.textId)

        self.accept(ResistanceChat.RESISTANCE_TOGGLE_EVENT, self.__toggle_event)

    def isWhisperable(self):
        return False

    def handleSelect(self, displayType=0):
        SCTerminal.handleSelect(self)
        messenger.send(self.getEventName(TTSCResistanceMsgEvent), [self.textId])

    def __toggle_event(self, state: bool):
        self.setDisabled(state)
        self.invalidate()
        self.finalizeAll()

    def destroy(self):
        self.ignore(ResistanceChat.RESISTANCE_TOGGLE_EVENT)
