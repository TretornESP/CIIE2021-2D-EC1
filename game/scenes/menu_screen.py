from game import ResourceManager
from .abstract_screen import AbstractScreen
from game.gui import PlayButton, ExitButton, TextGUI

class MenuScreen(AbstractScreen):
    def __init__(self, menu):
        AbstractScreen.__init__(self, menu, "backgrounds/main_menu.jpg", song="schrodinger.ogg")

        (_x_total, _y_total) = ResourceManager.load_config().get_resolution()
        (_x_total_half, _y_total_half) = (_x_total>>1, _y_total>>1)

        self._gui_elements.append(PlayButton(self, (_x_total_half, 270)))
        self._gui_elements.append(ExitButton(self, (_x_total_half, 340)))
        self._gui_elements.append(ExitButton(self, (_x_total_half, 410)))

        white = (255, 255, 255)
        font_64 = ResourceManager.load_font_asset("8bit.ttf", 64)
        font_32 = ResourceManager.load_font_asset("8bit.ttf", 32)
        font_24 = ResourceManager.load_font_asset("8bit.ttf", 24)
        font_16 = ResourceManager.load_font_asset("8bit.ttf", 16)

        title = TextGUI(self, font_64, white, "COVIDeogame", (_x_total_half, 120))
        play = TextGUI(self, font_32, white, "Jugar", (_x_total_half, 270))
        highscores = TextGUI(self, font_32, white, "Highscores", (_x_total_half, 340))
        exit = TextGUI(self, font_32, white, "Salir", (_x_total_half, 410))
        group = TextGUI(self, font_24, white, "Universidade da Coruña", (_x_total_half, 560))
        now_playing = TextGUI(self, font_16, white, "Now playing: BOHR - Schrödinger", (_x_total_half, 585))

        self._gui_elements.append(title)
        self._gui_elements.append(play)
        self._gui_elements.append(exit)
        self._gui_elements.append(highscores)
        self._gui_elements.append(group)
        self._gui_elements.append(now_playing)
