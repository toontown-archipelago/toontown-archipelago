from direct.gui import DirectGuiGlobals
from direct.gui.DirectButton import DirectButton
from direct.gui.OnscreenImage import OnscreenImage, TransparencyAttrib
from direct.showbase.ShowBase import ShowBase

class ButtonTest(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        ready = 'Neutral.png'
		# if you don't want to test out the rollover effect just uncomment below and comment the other pair
		#set = ready
        set = 'Hover.png'
		#set = ready
        go = 'Click.png'
       
        hidden = self.hidden
        ready1 = OnscreenImage(image=ready, parent=hidden)
        ready1.setTransparency(TransparencyAttrib.MAlpha)

        set1 = OnscreenImage(image=set, parent=hidden)
        set1.setTransparency(TransparencyAttrib.MAlpha)
        go1 = OnscreenImage(image=go, parent=hidden)
        go1.setTransparency(TransparencyAttrib.MAlpha)

        self.loadButton = DirectButton(frameSize=None, image=(ready1,
                                                              set1,
                                                              go1),
                                       relief=None,
                                       geom=None, pad=(0.01, 0.01), suppressKeys=0,
                                       borderWidth=(0.015, 0.01), scale=1)






bt = ButtonTest()
bt.run()