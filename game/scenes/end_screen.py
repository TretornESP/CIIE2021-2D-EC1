from game import ResourceManager
from .abstract_screen import AbstractScreen
from game.gui import PlayButton, ExitButton, RetryButton, TextGUI
from ..audio.rocker import Rocker

class EndScreen(AbstractScreen):
    def __init__(self, menu):
        AbstractScreen.__init__(self, menu, "backgrounds/main_menu.jpg")
        Rocker.action(Rocker.AUD_DEFEAT)
        self._gui_elements.append(RetryButton(self, (self._x_total_half, 270)))
        self._gui_elements.append(ExitButton(self, (self._x_total_half, 340)))

        white = (255, 255, 255)
        font_64 = ResourceManager.load_font_asset("8bit.ttf", 64)
        font_32 = ResourceManager.load_font_asset("8bit.ttf", 32)

        title = TextGUI(self, font_64, white, "Has perdido", (self._x_total_half, 120))
        retry = TextGUI(self, font_32, white, "Reintentar", (self._x_total_half, 270))
        exit = TextGUI(self, font_32, white, "Salir", (self._x_total_half, 340))

        self._gui_elements.append(title)
        self._gui_elements.append(retry)
        self._gui_elements.append(exit)
