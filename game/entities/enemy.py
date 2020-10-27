from .character import Character

class Enemy(Character):
    def __init__(self, level, data, coord, speedx = 25, speedy = 40, invert = False):
        Character.__init__(self, level, data, coord, invert, speedx, speedy)
        self._kind = data

    def act(self):
            pass
