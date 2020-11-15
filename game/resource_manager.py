import os
import json
import pygame
from .checkpoint_repository import CheckpointRepository
from .player_repository import PlayerRepository
from .text_repository import TextRepository
from .configuration import Configuration
from .director import Director
from pygame.locals import *

if __name__ != "__main__":
    pygame.mixer.init()

class ResourceManager(object):
    CONFIGURATION_NAME = "config.json"
    TEXT_REPO_NAME = "text.repository"
    DIRECTOR_NAME = "director.director"
    PLAYER_REPOSITORY_NAME = "player.repository"
    CHECKPOINT_REPO_NAME = "checkpoint.repository"

    _resources = {}
    _debug = None
    _sound = {}

    _channels = [
            pygame.mixer.Channel(0),
            pygame.mixer.Channel(1),
            pygame.mixer.Channel(2),
            pygame.mixer.Channel(3)
    ]
    _channel_idx = 0

    @classmethod
    def enable_debug(cls, debug):
        cls._debug = debug

    @classmethod
    def play_sound(cls, name):
        path = os.path.abspath(__package__)
        path = os.path.join(path, "assets/music/", name)
        sound = cls._sound.get(path)
        if sound == None:
            try:
                sound = pygame.mixer.Sound(path)
            except Exception as e:
                raise SystemExit("End")
            cls._sound[path] = sound
        cls._channel_idx = (cls._channel_idx + 1) % len(cls._channels)
        cls._channels[cls._channel_idx].play(sound)

    @classmethod
    def get_debug_name(cls):
        return cls._debug

    @classmethod
    def load_director(cls):
        if not ResourceManager.DIRECTOR_NAME in cls._resources:
            cls._resources[ResourceManager.DIRECTOR_NAME] = Director()
        return cls._resources[ResourceManager.DIRECTOR_NAME]

    @classmethod
    def load_config(cls):
        name = ResourceManager.CONFIGURATION_NAME
        if not name in cls._resources:
            path = os.path.abspath(__package__)
            fullname = os.path.join(path, name)
            try:
                with open(fullname, "r") as f:
                    config = json.load(f)
                    cls._resources[name] = Configuration(config)
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
                print(e)
                raise SystemExit
        return cls._resources[(level+folder+name)]

    @classmethod
    def load_hs(cls):
        path = os.path.abspath(__package__)
        fullname = os.path.join(path, "highscores.json")
        with open(fullname, "r") as f:
            hs = json.load(f)
            hs = sorted(hs, key=lambda h: h[1])
            return hs[:5]

    @classmethod
    def append_hs(cls, highscore_sec):
        path = os.path.abspath(__package__)
        fullname = os.path.join(path, "highscores.json")
        hs = None
        with open(fullname, "r") as f:
            hs = json.load(f)
            from datetime import date
            hs.append([date.today().strftime("%d-%m-%Y"), highscore_sec])
        with open(fullname, "w") as f:
            json.dump(hs, f)

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

    @classmethod
    def get_checkpoint_repository(cls):
        if cls.CHECKPOINT_REPO_NAME not in cls._resources:
            cls._resources[cls.CHECKPOINT_REPO_NAME] = CheckpointRepository()
        return cls._resources[cls.CHECKPOINT_REPO_NAME]
