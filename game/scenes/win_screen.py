from game import ResourceManager
from .abstract_screen import AbstractScreen
from game.gui import ExitButton, TextGUI
from game.player_repository import PlayerRepository

class WinScreen(AbstractScreen):
    def __init__(self, menu):
        AbstractScreen.__init__(self, menu, "backgrounds/main_menu.jpg")
        self._gui_elements.append(ExitButton(self, (self._x_total_half, 480)))

        repo = ResourceManager.get_player_repository()
        score = int(repo.get_parameter(PlayerRepository.ATTR_TOTAL_TIME))
        ResourceManager.append_hs(score)

        white = (255, 255, 255)
        font_64 = ResourceManager.load_font_asset("8bit.ttf", 64)
        font_32 = ResourceManager.load_font_asset("8bit.ttf", 32)
        font_24 = ResourceManager.load_font_asset("8bit.ttf", 24)

        title = TextGUI(self, font_64, white, "Has ganado", (self._x_total_half, 120))
        score = TextGUI(self, font_24, white, f"Score: {score} sec", (self._x_total_half, 300))
        exit = TextGUI(self, font_32, white, "Salir", (self._x_total_half, 480))

        self._gui_elements.append(title)
        self._gui_elements.append(score)
        self._gui_elements.append(exit)
