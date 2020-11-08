from game.entities.abstract_sprite import AbstractSprite


class AbstractAttached(AbstractSprite):
    def __init__(self, level, data, position, invert, velocity_x = 0, velocity_y = 0):
        AbstractSprite.__init__(self)
