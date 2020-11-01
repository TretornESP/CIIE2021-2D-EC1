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
                print(f"Cannot load resource with name {name} at {fullname}")
                raise SystemExit
        return cls._resources[name]


    @classmethod
    def load_sheet(cls, level, folder, name="sheet.png", colorkey=None):
        if not name in cls._resources:
            path = os.path.abspath(__package__)
            fullname = os.path.join(path, "levels", level, "data", folder, name)
            try:
                image = pygame.image.load(fullname)
            except Exception:
                print(f"Cannot load resource with name {name} at {fullname}")
                raise SystemExit
            image.convert()
            if colorkey is not None:
                if colorkey == -1:
                    colorkey = image.get_at((0, 0))
                image.set_colorkey(colorkey, RLEACCEL)
            cls._resources[name] = image
        return cls._resources[name]

    @classmethod
    def load_sprite(cls, level, name, colorkey=None):
        if not name in cls._resources:
            path = os.path.abspath(__package__)
            fullname = os.path.join(path, "levels", level, "sprites", name)
            try:
                image = pygame.image.load(fullname)
            except Exception:
                print(f"Cannot load resource with name {name} at {fullname}")
                raise SystemExit
            image.convert()
            if colorkey is not None:
                if colorkey == -1:
                    colorkey = image.get_at((0, 0))
                image.set_colorkey(colorkey, RLEACCEL)
            cls._resources[name] = image
        return cls._resources[name]

    @classmethod
    def load_image_asset(cls, name):
        if not name in cls._resources:
            path = os.path.abspath(__package__)
            fullname = os.path.join(path, "assets", "images", name)
            try:
                image = pygame.image.load(fullname)
            except Exception:
                print(f"Cannot load resource with name {name} at {fullname}")
                raise SystemExit
            cls._resources[name] = image
        return cls._resources[name]

    @classmethod
    def load_music_asset(cls, name):
        if not name in cls._resources:
            path = os.path.abspath(__package__)
            fullname = os.path.join(path, "assets", "music", name)
            try:
                sound = pygame.mixer.Sound(fullname)
            except Exception:
                print(f"Cannot load resource with name {name} at {fullname}")
                raise SystemExit
            cls._resources[name] = sound
        return cls._resources[name]

    @classmethod
    def load_font_asset(cls, name, size):
        res_name = name + "_" + str(size)
        if not res_name in cls._resources:
            path = os.path.abspath(__package__)
            fullname = os.path.join(path, "assets", "fonts", name)
            try:
                font = pygame.font.Font(fullname, size)
            except Exception:
                print(f"Cannot load resource with name {name} at {fullname}")
                raise SystemExit
            cls._resources[res_name] = font
        return cls._resources[res_name]

    @classmethod
    def load_music_channel(cls):
        name = "music_channel"
        if not name in cls._resources:
            channel = pygame.mixer.Channel(0)
            cls._resources[name] = channel
        return cls._resources[name]

    @classmethod
    def load_coords(cls, level, folder, name="coords.json"):
        if not name in cls._resources:
            path = os.path.abspath(__package__)
            fullname = os.path.join(path, "levels", level, "data", folder, name)
            try:
                with open(fullname, "r") as f:
                    coords = json.load(f)
                    cls._resources[name] = coords
            except Exception:
                print(f"Cannot load resource with name {name} at folder: {fullname}")
                raise SystemExit
        return cls._resources[name]
