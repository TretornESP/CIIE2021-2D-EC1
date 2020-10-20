import pygame, os

class ResourceManager(object):
    _resources = {}

    @classmethod
    def load_image(cls, name, colorkey=None):
        if not name in cls._resources:
            path = os.path.abspath(__package__)
            fullname = os.path.join(path, "images", name)
            try:
                image = pygame.image.load(fullname)
            except Exception:
                print(f"Cannot load resource with name {name}")
                raise SystemExit
            image.convert()
            if colorkey is not None:
                if colorkey == -1:
                    colorkey = image.get_at((0, 0))
                image.set_colorkey(colorkey, RLEACCEL)
            cls._resources[name] = image
        return cls._resources[name]
