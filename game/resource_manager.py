import os
import json
import pygame
from pygame.locals import *
from game.player_repository import PlayerRepository
from game.text_repository import TextRepository


class ResourceManager(object):
    PLAYER_REPOSITORY_NAME = "player.repository"
    TEXT_REPO_NAME = "text.repository"

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
            fullname = os.path.join(path, level, "data", folder, name)
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
    def load_sprite(cls, name, level="assets", colorkey=None, scale=1):
        if not (level+name) in cls._resources:
            path = os.path.abspath(__package__)
            fullname = os.path.join(path, level, "sprites", name)
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
    def get_song_path(cls, name):
        if not name in cls._resources:
            path = os.path.abspath(__package__)
            fullname = os.path.join(path, "assets", "music", name)
            cls._resources[name] = fullname
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
    def load_coords(cls, level, folder, name="coords.json"):
        if not (level+folder+name) in cls._resources:
            path = os.path.abspath(__package__)
            fullname = os.path.join(path, level, "data", folder, name)
            try:
                with open(fullname, "r") as f:
                    coords = json.load(f)
                    cls._resources[(level+folder+name)] = coords
            except Exception as e:
                print(f"Cannot load coords resource with name {name} at folder: {fullname}")
                print("Check JSON sanity!!!")
                raise SystemExit
        return cls._resources[(level+folder+name)]

    @classmethod
    def get_player_repository(cls):
        if cls.PLAYER_REPOSITORY_NAME not in cls._resources:
            cls._resources[cls.PLAYER_REPOSITORY_NAME] = PlayerRepository()
        return cls._resources[cls.PLAYER_REPOSITORY_NAME]

    @classmethod
    def get_text_repository(cls):
        if cls.TEXT_REPO_NAME not in cls._resources:
            cls._resources[cls.TEXT_REPO_NAME] = TextRepository()
        return cls._resources[cls.TEXT_REPO_NAME]
