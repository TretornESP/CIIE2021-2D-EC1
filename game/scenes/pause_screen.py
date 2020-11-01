from game import ResourceManager
from .abstract_screen import AbstractScreen
from game.gui import PlayButton, ExitButton, TextGUI

class PauseScreen(AbstractScreen):
    def __init__(self, menu):
        AbstractScreen.__init__(self, menu, "backgrounds/main_menu.jpg")

        self._gui_elements.append(PlayButton(self, (400, 270)))
        self._gui_elements.append(ExitButton(self, (400, 340)))

        white = (255, 255, 255)
        font_32 = ResourceManager.load_font_asset("8bit.ttf", 32)

        play = TextGUI(self, font_32, white, "Reanudar", (400, 270))
        exit = TextGUI(self, font_32, white, "Salir", (400, 340))

        self._gui_elements.append(play)
        self._gui_elements.append(exit)
