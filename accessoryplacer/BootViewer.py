from panda3d.core import TextNode, Texture, LoaderOptions, TexturePool
from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from direct.gui.DirectGui import *

LegDict = {
    's': 'phase_3/models/char/tt_a_chr_dgs_shorts_legs_',
    'm': 'phase_3/models/char/tt_a_chr_dgm_shorts_legs_',
    'l': 'phase_3/models/char/tt_a_chr_dgl_shorts_legs_'
}
LegNames = ['Short Legs', 'Medium Legs', 'Long Legs']
ShoeNames = ['Shoes', 'Long Boots', 'Short Boots']

class BootViewer(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        self.legOptions = ['s', 'm', 'l']
        self.shoesOptions = ['shoes', 'boots_long', 'boots_short']
        self.legChoice = 0
        self.shoesChoice = 0
        self.legs = None

        self.legLabel = DirectLabel(self.a2dBottomLeft, relief=None, text='', text_align=TextNode.ALeft, text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1), text_scale=0.08, pos=(0.05, 0, 0.15))
        self.shoeLabel = DirectLabel(self.a2dBottomLeft, relief=None, text='', text_align=TextNode.ALeft, text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1), text_scale=0.08, pos=(0.05, 0, 0.05))

        self.loadLegs()

        self.accept('arrow_left', self.addLegChoice, [-1])
        self.accept('arrow_right', self.addLegChoice, [1])
        self.accept('arrow_down', self.addShoeChoice, [-1])
        self.accept('arrow_up', self.addShoeChoice, [1])
        self.accept('r', self.reloadTexture)

    def addLegChoice(self, offset):
        self.legChoice = (self.legChoice + offset) % len(self.legOptions)
        self.loadLegs()

    def addShoeChoice(self, offset):
        self.shoesChoice = (self.shoesChoice + offset) % len(self.shoesOptions)
        self.loadShoes()

    def loadShoes(self):
        for i, shoe in enumerate(self.shoesOptions):
            node = self.legs.find('**/' + shoe)

            if self.shoesChoice == i:
                node.show()
            else:
                node.hide()

        self.shoeLabel['text'] = ShoeNames[self.shoesChoice]
        self.reloadTexture()

    def reloadTexture(self):
        TexturePool.releaseAllTextures()

        tex = loader.loadTexture('custom.png')
        tex.setMinfilter(Texture.FTLinearMipmapLinear)
        tex.setMagfilter(Texture.FTLinear)
        self.legs.find('**/' + self.shoesOptions[self.shoesChoice]).setTexture(tex, 1)

    def unloadLegs(self):
        if self.legs:
            self.legs.delete()

        self.legs = None

    def loadLegs(self):
        self.unloadLegs()

        legPrefix = LegDict[self.legOptions[self.legChoice]]
        self.legs = Actor(legPrefix + '1000.bam', {'neutral': legPrefix + 'neutral.bam', 'run': legPrefix + 'run.bam'})
        self.legs.reparentTo(render)
        self.legs.setPosHpr(0, 10, -2, 180, 0, 0)
        self.legs.loop('neutral')
        self.legs.find('**/feet').hide()
        self.legs.find('**/legs').setColor(1, 1, 1, 1)

        self.legLabel['text'] = LegNames[self.legChoice]
        self.loadShoes()

if __name__ == '__main__':
    base = BootViewer()
    base.run()