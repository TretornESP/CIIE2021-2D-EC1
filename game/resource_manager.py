import os
import json
import pygame
from pygame.locals import *


class ResourceManager(object):
    _resources = {}

    @classmethod
    def load_config(cls, name="config.json"):
        if not name in cls._resources:
            path = os.path.abspath(__package__)
            fullname = os.path.join(path, name)
            try:
                with open(fullname, "r") as f:
                    config = json.load(f)
                    cls._resources[name] = config
            except Exception:
                print(f"Cannot load config resource with name {name} at {fullname}")
                raise SystemExit
        return cls._resources[name]


    @classmethod
    def load_sheet(cls, level, folder, name="sheet.png", colorkey=None):
        if not (level+folder+name) in cls._resources:
            path = os.path.abspath(__package__)
            fullname = os.path.join(path, "levels", level, "data", folder, name)
            try:
                image = pygame.image.load(fullname)
            except Exception:
                print(f"Cannot load sheet resource with name {name} at {fullname}")
                raise SystemExit
            image.convert()
            if colorkey is not None:
                if colorkey == -1:
                    colorkey = image.get_at((0, 0))
                image.set_colorkey(colorkey, RLEACCEL)
            cls._resources[(level+folder+name)] = image
        return cls._resources[(level+folder+name)]

    @classmethod
    def load_sprite(cls, level, name, colorkey=None):
        if not (level+name) in cls._resources:
            path = os.path.abspath(__package__)
            fullname = os.path.join(path, "levels", level, "sprites", name)
            try:
                print(f"loading sprite at {fullname}")
                image = pygame.image.load(fullname)
            except Exception:
                print(f"Cannot load sprite resource with name {name} at {fullname}")
                raise SystemExit
            image.convert()
            if colorkey is not None:
                if colorkey == -1:
                    colorkey = image.get_at((0, 0))
                image.set_colorkey(colorkey, RLEACCEL)
            cls._resources[(level+name)] = image
        return cls._resources[(level+name)]

    @classmethod
    def load_coords(cls, level, folder, name="coords.json"):
        if not (level+folder+name) in cls._resources:
            path = os.path.abspath(__package__)
            fullname = os.path.join(path, "levels", level, "data", folder, name)
            try:
                with open(fullname, "r") as f:
                    coords = json.load(f)
                    cls._resources[(level+folder+name)] = coords
            except Exception as e:
                print(f"Cannot load coords resource with name {name} at folder: {fullname}")
                print("Check JSON sanity!!!")
                raise SystemExit
        return cls._resources[(level+folder+name)]
