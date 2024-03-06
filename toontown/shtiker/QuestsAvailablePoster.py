from direct.gui.DirectGui import *
from panda3d.core import *

from toontown.toonbase import ToontownGlobals


class QuestsAvailablePoster(DirectFrame):
    def __init__(self, hoodId, **kw):

        self.hoodId = hoodId

        bookModel = loader.loadModel('phase_3.5/models/gui/stickerbook_gui')
        questCard = bookModel.find('**/questCard')
        optiondefs = (
            ('parent', kw['parent'], None),
            ('relief', None, None),
            ('image', questCard, None),
            ('image_scale', (0.8, 1.0, 0.58), None),
            ('state', DGG.NORMAL, None)
        )
        self.defineoptions(kw, optiondefs)

        DirectFrame.__init__(self, relief=None, **kw)
        self.initialiseoptions(QuestsAvailablePoster)

        self.numQuestsAvailableLabel = DirectLabel(self, relief=None, text=f"0", text_scale=.9,
                                                   text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1),
                                                   text_font=ToontownGlobals.getSignFont(), pos=(-0.3, 0, 0))

        bookModel.removeNode()

    def getHoodId(self):
        return self.hoodId

    def showLocked(self):
        self.numQuestsAvailableLabel['text'] = 'X'
        self.numQuestsAvailableLabel['text_fg'] = (1, 0, 0, 1)

    def showNumAvailable(self, number):

        color = (.9, .9, .9, 1)
        if number <= 0:
            number = 0
            color = (.1, .9, .1, 1)

        self.numQuestsAvailableLabel['text'] = str(number)
        self.numQuestsAvailableLabel['text_fg'] = color

    def destroy(self):
        super().destroy()
        self.numQuestsAvailableLabel.destroy()
