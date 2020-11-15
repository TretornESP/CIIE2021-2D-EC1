from game import ResourceManager
from ..abstract_screen import AbstractScreen
from game.gui import PlayButton, ExitButton, OptionButton, EmptyButton, TextGUI
from itertools import islice
import os
import pygame

class DialogScreen(AbstractScreen):
    TEXT_AREA_TOP_GAP = 150
    TITLE_TEXT_AREA_GAP = 50
    TEXT_TITLE_GAP = 50
    TEXT_AREA_WIDTH = 800
    TEXT_AREA_HEIGHT = 200
    TEXT_AREA_COLOR = (255, 255, 255)

    OPTIONS_AREA_TEXT_AREA_GAP = 200
    OPTIONS_AREA_WIDTH = 800
    OPTIONS_AREA_HEIGHT = 100
    OPTIONS_AREA_COLOR = (255, 255, 255)

    HEAD_LEFT_GAP = 75
    HEAD_TOP_GAP = 0

    TITLE_COLOR = (0,0,0)
    TEXT_COLOR = (0,0,0)
    TITLE_FONT_SIZE = 32
    TEXT_FONT_SIZE = 16

    def __init__(self, menu, background, title, text, options):
        AbstractScreen.__init__(self, menu, "backgrounds/dialog.jpg", transform = True)

        self._text_area = pygame.Rect(self.rect.centerx-int(DialogScreen.TEXT_AREA_WIDTH/2), self.rect.top+DialogScreen.TEXT_AREA_TOP_GAP, DialogScreen.TEXT_AREA_WIDTH, DialogScreen.TEXT_AREA_HEIGHT)
        self.round_rect(self.image, self._text_area, 50, DialogScreen.TEXT_AREA_COLOR)

        self._options_area = pygame.Rect(self.rect.centerx-int(DialogScreen.OPTIONS_AREA_WIDTH/2), self._text_area.centery-int(DialogScreen.OPTIONS_AREA_HEIGHT/2)+DialogScreen.OPTIONS_AREA_TEXT_AREA_GAP, DialogScreen.OPTIONS_AREA_WIDTH, DialogScreen.OPTIONS_AREA_HEIGHT)
        self.round_rect(self.image, self._options_area, 50, DialogScreen.OPTIONS_AREA_COLOR)

        title_font = ResourceManager.load_font_asset("8bit.ttf", DialogScreen.TITLE_FONT_SIZE)
        text_font = ResourceManager.load_font_asset("8bit.ttf", DialogScreen.TEXT_FONT_SIZE)

        index = 0
        for option in options:
            x_offset, y_offset = text_font.size(option.get_text())
            bpos = (self._options_area.left+x_offset, self._options_area.centery)
            tpos = (self._options_area.left+x_offset, self._options_area.centery)
            otext = TextGUI(self, text_font, DialogScreen.TEXT_COLOR, option.get_text(), tpos)
            self._gui_elements.append(OptionButton(self, bpos, x_offset, y_offset, option.is_valid()))
            self._gui_elements.append(otext)


            index = index + 1

        lines = self.split_text_to_fit(text, DialogScreen.TEXT_FONT_SIZE, DialogScreen.TEXT_AREA_WIDTH)
        title = TextGUI(self, title_font, DialogScreen.TITLE_COLOR, title, (self._text_area.centerx, self._text_area.top+DialogScreen.TITLE_TEXT_AREA_GAP))
        self._gui_elements.append(title)

        background = os.path.join("heads", background)
        self._gui_elements.append(EmptyButton(self, (self._text_area.left+DialogScreen.HEAD_LEFT_GAP, self._text_area.centery+DialogScreen.HEAD_TOP_GAP), 100, 100, background))

        index = 0
        for line in lines:
            ltext = TextGUI(self, text_font, DialogScreen.TEXT_COLOR, "".join(line), (self._text_area.centerx, self._text_area.top+DialogScreen.TITLE_TEXT_AREA_GAP+DialogScreen.TEXT_TITLE_GAP+(DialogScreen.TEXT_FONT_SIZE*index)))
            self._gui_elements.append(ltext)
            index = index + 1

    def split_text_to_fit(self, text, font_size, width, padding = 5, corrector = 100):
        characters_in_line = int(float(width-padding+corrector)/float(font_size))
        return self.split_every(characters_in_line, list(text))

    def split_every(self, n, iterable):
        i = iter(iterable)
        piece = list(islice(i, n))
        while piece:
            yield piece
            piece = list(islice(i, n))

    def round_rect(self, surf, rect, rad, color, thick=0):
        trans = (255,255,1)
        if not rad:
            pygame.draw.rect(surf, color, rect, thick)
            return
        elif rad > rect.width / 2 or rad > rect.height / 2:
            rad = min(rect.width/2, rect.height/2)

        if thick > 0:
            r = rect.copy()
            x, r.x = r.x, 0
            y, r.y = r.y, 0
            buf = pygame.surface.Surface((rect.width, rect.height)).convert()
            buf.set_colorkey(trans)
            buf.fill(trans)
            self.round_rect(buf, r, rad, color, 0)
            r = r.inflate(-thick*2, -thick*2)
            self.round_rect(buf, r, rad, trans, 0)
            surf.blit(buf, (x,y))
        else:
            r  = rect.inflate(-rad * 2, -rad * 2)
            for corn in (r.topleft, r.topright, r.bottomleft, r.bottomright):
                pygame.draw.circle(surf, color, corn, rad)
            pygame.draw.rect(surf, color, r.inflate(rad*2, 0))
            pygame.draw.rect(surf, color, r.inflate(0, rad*2))
