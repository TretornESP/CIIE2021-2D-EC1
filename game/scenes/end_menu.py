from .abstract_menu import AbstractMenu
from .end_screen import EndScreen

class EndMenu(AbstractMenu):
    def __init__(self):
        AbstractMenu.__init__(self)

        self._screen_list.append(EndScreen(self))
        self._show_first_screen()

    def update(self, *args):
        pass

    def events(self, events):
        AbstractMenu.events(self, events)

    def quit_game(self):
        self._director.flush_scene()

    def retry(self):
        self._director.run_checkpoint()
