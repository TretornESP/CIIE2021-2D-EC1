from ..abstract_sprite  import AbstractSprite
from ...resource_manager import ResourceManager

class HudElement(AbstractSprite):
    def __init__(self, level, sprite, coord):
        AbstractSprite.__init__(self)

        self.image = ResourceManager.load_sprite(level, sprite)
        self.rect = self.image.get_rect()
        self.set_static_position(coord) # TODO Esto es un bug y debería eliminarse.
                                        # wip: set_static_position
