from game import ResourceManager
from .abstract_screen import AbstractScreen
from game.gui import PlayButton, ExitButton, TextGUI, MainMenuButton


class HighscoresScreen(AbstractScreen):
    def __init__(self, menu):
        AbstractScreen.__init__(self, menu, "backgrounds/main_menu.jpg")

        self._gui_elements.append(MainMenuButton(self, (self._x_total_half, self._y_total * 14 / 16)))

        white = (255, 255, 255)
        font_64 = ResourceManager.load_font_asset("8bit.ttf", 64)
        # font_32 = ResourceManager.load_font_asset("8bit.ttf", 32)
        font_24 = ResourceManager.load_font_asset("8bit.ttf", 24)
        # font_16 = ResourceManager.load_font_asset("8bit.ttf", 16)

        title = TextGUI(self, font_64, white, "Highscores", (self._x_total_half, self._y_total * 2 / 16))

        hs_rect = HSBackground(self, (self._x_total_half, self._y_total>>1), 500, 325)

        self.hs1 = TextGUI(self, font_24, white, "None", (self._x_total_half, self._y_total * 5 / 16))
        self.hs2 = TextGUI(self, font_24, white, "None", (self._x_total_half, self._y_total * 6.5 / 16))
        self.hs3 = TextGUI(self, font_24, white, "None", (self._x_total_half, self._y_total * 8 / 16))
        self.hs4 = TextGUI(self, font_24, white, "None", (self._x_total_half, self._y_total * 9.5 / 16))
        self.hs5 = TextGUI(self, font_24, white, "None", (self._x_total_half, self._y_total * 11 / 16))

        back_button = TextGUI(self, font_24, white, "Menú Principal", (self._x_total_half, self._y_total * 14 / 16))

        self._gui_elements.append(title)
        self._gui_elements.append(hs_rect)
        self._gui_elements.append(self.hs1)
        self._gui_elements.append(self.hs2)
        self._gui_elements.append(self.hs3)
        self._gui_elements.append(self.hs4)
        self._gui_elements.append(self.hs5)
        self._gui_elements.append(back_button)

    def populate_hs_list(self, list):
        font_24 = ResourceManager.load_font_asset("8bit.ttf", 24)
        white = (255, 255, 255)
        self._gui_elements.remove(self.hs1)
        self._gui_elements.remove(self.hs2)
        self._gui_elements.remove(self.hs3)
        self._gui_elements.remove(self.hs4)
        self._gui_elements.remove(self.hs5)

        self.hs1 = TextGUI(self, font_24, white, f"{list[0][0]}    -    {list[0][1]} sec", (self._x_total_half, self._y_total * 5 / 16))
        self.hs2 = TextGUI(self, font_24, white, f"{list[1][0]}    -    {list[1][1]} sec", (self._x_total_half, self._y_total * 6.5 / 16))
        self.hs3 = TextGUI(self, font_24, white, f"{list[2][0]}    -    {list[2][1]} sec", (self._x_total_half, self._y_total * 8 / 16))
        self.hs4 = TextGUI(self, font_24, white, f"{list[3][0]}    -    {list[3][1]} sec", (self._x_total_half, self._y_total * 9.5 / 16))
        self.hs5 = TextGUI(self, font_24, white, f"{list[4][0]}    -    {list[4][1]} sec", (self._x_total_half, self._y_total * 11 / 16))

        self._gui_elements.append(self.hs1)
        self._gui_elements.append(self.hs2)
        self._gui_elements.append(self.hs3)
        self._gui_elements.append(self.hs4)
        self._gui_elements.append(self.hs5)

from ..gui.gui_element import GUIElement
class HSBackground(GUIElement):
    def __init__(self, screen, pos, x_size, y_size):
        import pygame
        self.image = pygame.Surface((x_size, y_size))
        self.image.fill((160, 160, 160))

        self.rect = self.image.get_rect()
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]

        GUIElement.__init__(self, screen, self.rect)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def callback(self):
        pass