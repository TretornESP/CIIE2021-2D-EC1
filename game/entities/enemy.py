from .character import Character

class Enemy(Character):
    def __init__(self, level, kind, data, coord, speedx = 25, speedy = 40, invert = False):
        Character.__init__(self, level, data, coord, invert, speedx, speedy)
        self._kind = kind

    def act(self):
            pass
