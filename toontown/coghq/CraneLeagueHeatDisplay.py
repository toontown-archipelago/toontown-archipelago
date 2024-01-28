from otp.speedchat import ColorSpace

from direct.gui.DirectGui import *
from panda3d.core import *

from toontown.coghq import CraneLeagueGlobals
from toontown.toonbase import ToontownGlobals

LOWEST_HEAT_H_VALUE = 80
HIGHEST_HEAT_H_VALUE = 0

LOWEST_HEAT_S_VALUE = .41
HIGHEST_HEAT_S_VALUE = .70

V_HEAT_VALUE = .83

LOWEST_HEAT = 150
HIGHEST_HEAT = 1000

TITLE_FONT_SIZE = 1.05
DESCRIPTION_TITLE_FONT_SIZE = 0.85
DESCRIPTION_BODY_FONT_SIZE = 0.65
DESCRIPTION_WORD_WRAP = 20


class CraneLeagueHeatDisplay:

    FLAME_POS = (-.53, 0, .74)
    HEAT_NUM_POS = (-.48, .72)
    MODIFIERS_TEXT_POS = (-.64, 0, .6)

    # TextProperties shit to make life easier
    text_properties_manager = TextPropertiesManager.getGlobalPtr()
    text_properties_default_color = TextProperties()
    text_properties_default_color.setTextColor(1, 1, 1, 1)
    text_properties_default_color.setTextScale(TITLE_FONT_SIZE)
    text_properties_manager.setProperties("default_mod_color", text_properties_default_color)

    def __init__(self):
        self.heat = 500
        self.frame = DirectFrame(parent=base.a2dRightCenter)
        self.flame_image = OnscreenImage(parent=self.frame, image='phase_10/maps/heat.png', pos=self.FLAME_POS, scale=.05)
        self.flame_image.setTransparency(TransparencyAttrib.MAlpha)

        self.heat_number = OnscreenText(parent=self.frame, text='500', style=3, fg=self.calculate_color(), align=TextNode.ALeft, scale=.1, pos=self.HEAT_NUM_POS, font=ToontownGlobals.getSuitFont())

        self.hover_button = DirectButton(parent=self.frame, pos=(-.43, 0, .74), scale=(1.5, 1, .5))
        self.hover_button.setTransparency(TransparencyAttrib.MAlpha)
        self.hover_button.setColorScale(1, 1, 1, 0)

        # Bind the heat button to show the modifiers when we hover over it
        self.hover_button.bind(DGG.ENTER, self.__show_modifiers)  # Bind hover on event to show the information
        self.hover_button.bind(DGG.EXIT, self.__hide_modifiers)  # Bind hover off event to clear the information

        # The text that describes modifiers
        self.modifiers_desc = TextNode('modifiers-desc')
        self.modifiers_desc.setText(self.generateText())
        self.modifiers_desc.setAlign(TextNode.ACenter)
        self.modifiers_desc.setFrameColor(self.calculate_color())
        self.modifiers_desc.setFrameAsMargin(0.4, 0.4, 0.2, 0.2)
        self.modifiers_desc.setCardColor(.2, .2, .2, .75)
        self.modifiers_desc.setCardAsMargin(0.38, 0.38, 0.19, 0.19)
        self.modifiers_desc.setCardDecal(True)
        self.modifiers_desc.setWordwrap(DESCRIPTION_WORD_WRAP)
        self.modifiers_desc.setShadow(0.05, 0.05)
        self.modifiers_desc.setShadowColor(0, 0, 0, 1)
        self.modifiers_desc.setTextColor(.7, .7, .7, 1)
        self.modifiers_desc.setTextScale(DESCRIPTION_BODY_FONT_SIZE)
        self.modifiers_desc.setFont(ToontownGlobals.getCompetitionFont())
        self.modifiers_desc_path = base.a2dRightCenter.attachNewNode(self.modifiers_desc)
        self.modifiers_desc_path.setScale(.055)
        self.modifiers_desc_path.setPos(self.MODIFIERS_TEXT_POS)
        self.modifiers_desc_path.hide()

    def __show_modifiers(self, event=None):
        self.modifiers_desc_path.show()

    def __hide_modifiers(self, event=None):
        self.modifiers_desc_path.hide()

    # Taking a list of modifier objects, generate a text string to put inside the box thingy
    def generateText(self, modifiers=None):
        if not modifiers or len(modifiers) <= 0:
            return "\1default_mod_color\1No modifiers :(\2"

        # First the title of the box
        s = '\1default_mod_color\1Active Modifiers\2'

        # Now loop through all the modifiers, and add the required text
        for mod in modifiers:
            # We have a title and a description, first add some space from above
            s += '\n\n'
            title = mod.getName()
            desc = mod.getDescription()
            # Define text prop objs
            title_text_properties = TextProperties()
            title_text_properties.setTextColor(mod.TITLE_COLOR)
            title_text_properties.setTextScale(DESCRIPTION_TITLE_FONT_SIZE)
            desc_text_properties = TextProperties()
            desc_text_properties.setTextColor(mod.DESCRIPTION_COLOR)
            desc_text_properties.setTextScale(DESCRIPTION_BODY_FONT_SIZE)

            title_key = 'mod-title-' + str(title)
            desc_key = 'mod-desc-' + str(title)
            self.text_properties_manager.setProperties(title_key, title_text_properties)
            self.text_properties_manager.setProperties(desc_key, desc_text_properties)

            # Now add the text with the special chars in it
            s += '\1' + title_key + '\1' + title + '\2\n'
            # Now add the desc, replacing color_start and color_end with color codes
            s += desc % {'color_start': '\1' + desc_key + '\1', 'color_end': '\2'}

        # The entire string should now be built, return it
        return s

    # What color should the number be based on the heat?
    def calculate_color(self):
        heat_factor = float(self.heat-LOWEST_HEAT) / (HIGHEST_HEAT-LOWEST_HEAT)
        h = (1-heat_factor) * (LOWEST_HEAT_H_VALUE+HIGHEST_HEAT_H_VALUE)
        h = int(h)

        s = LOWEST_HEAT_S_VALUE + ((HIGHEST_HEAT_S_VALUE-LOWEST_HEAT_S_VALUE)*heat_factor)
        r, g, b = ColorSpace.hsv2rgb(h, s, V_HEAT_VALUE)
        print(('setting to %s %s %s (%s %s %s)' % (r, g, b, h, s, V_HEAT_VALUE)))
        return r, g, b, 1

    # Take in an integer and set the heat to display, update the color
    def set_heat(self, num):
        self.heat = num
        self.heat_number.setText(str(num))
        self.heat_number['fg'] = self.calculate_color()

    def hide(self):
        self.heat_number.hide()
        self.flame_image.hide()
        self.modifiers_desc_path.hide()

    def show(self):
        self.heat_number.show()
        self.flame_image.show()
        # self.modifiers_desc_path.show()

    # Updates all elements on the gui
    def update(self, heat, modifiers):
        self.set_heat(heat)
        self.modifiers_desc.setText(self.generateText(modifiers))
        self.modifiers_desc.setFrameColor(self.calculate_color())

    def cleanup(self):
        self.frame.destroy()
        self.modifiers_desc_path.removeNode()
