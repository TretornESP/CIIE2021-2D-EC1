import pygame
from game import ResourceManager
from ..entities.spikes import Spikes
from ..scenes import AbstractHorizontalScene
from ..scenes.skies import AbstractSky
from game.entities import Platform, Player, Covid, Torreta, Corredor
from ..scenes.backgrounds import MainBackground
from ..scenes import Scene
from ..util import Clog
from ..entities import Object
from ..entities import Trigger
from ..farm_factory import FarmFactory
from ..scenes.dialogs import DialogOption
from ..scenes.dialogs import DialogMenu
from pygame.locals import *
import os
import json

class Level():
    def __init__(self, filename, hacks=False):
        self._clog = Clog(__name__)
        self.id = None
        self.name = None
        self.scenes = []
        self.dialogs = []
        self._hacks = hacks
        self._clog.info("Loading level")
        self.construct_file_path(filename)
        self.load_json_file()
        self.parse_json(self._json_data)
        self._clog.info("Level loading finished")

    def get_scenes(self):
        return self.scenes

    def construct_file_path(self, filename):
        path = os.path.dirname(os.path.realpath(__file__))
        self._level_file = os.path.join(path, filename, "level.json")

    def load_json_file(self):
        with open(self._level_file) as f:
            self._json_data = json.loads(f.read())

    def parse_coords(self, json):
        return (json['pos_x'], json['pos_y'])

    def parse_player(self, json):
        coords = self.parse_coords(json['coords'])
        invert = json['coords']['inverted']
        speedx = 25 #REPLACE ME
        speedy = 40 #REPLACE ME
        datafn = json['data']
        return Player(self.name, datafn, coords, speedx, speedy, invert, self._hacks)

    def parse_platform(self, json):
        sprite = json['sprite']
        collid = json['collides']
        coords = self.parse_coords(json['coords'])
        invert = json['coords']['inverted']

        if 'scale' in json:
            scale = json['scale']
        else:
            scale = None

        return Platform(self.name, sprite, collid, coords, invert, scale=scale)

    def parse_object(self, json):
        kind   = json['kind']
        sprite = json['sprite']
        collid = json['collides']
        coords = self.parse_coords(json['coords'])
        invert = json['coords']['inverted']
        return Object(self.name, kind, sprite, collid, coords, invert)

    def parse_size(self, json):
        return (json['width'], json['height'])

    def parse_enemy(self, j):
        # el comportamiento depende de codigo
        # el sprite es generico pero no su comportamiento
        # necesaria especificacion en clases
        #
        # @author: iñaki

        collid = j['collides']
        datafn = j['data']
        speedx = j['speedx']
        speedy = j['speedy']
        coords = self.parse_coords(j['coords'])
        invert = j['coords']['inverted']
        shot = j.get('shot')

        if datafn == 'covid':
            return Covid(self.name, datafn, coords, speedx, speedy, invert)
        elif datafn == 'torreta':
            if shot == None:
                raise NotImplemented("You must specify shot data folder!")
            return Torreta(self.name, datafn, shot, coords, speedx, speedy, invert)
        elif datafn == 'corredor':
            return Corredor(self.name, datafn, coords, speedx, speedy, invert)
        elif datafn == 'spikes':
            return Spikes(self.name, datafn, coords, speedx, speedy, invert)
        else:
            raise NotImplemented("No existe este enemigo")

    def parse_trigger(self, json):
        event     = json['event']
        id        = json.get('id')
        indica    = json['indicator']
        once      = json.get('once')
        if once == None: #Once by default is true bro
            once = True  #Once by default aint shit as it is not required by json schema!
        locking   = json.get('locking')
        if locking == None:
            locking = True
        if locking == True:
            once = True # This prevents getting locked inside the dialog!
        coords = self.parse_coords(json['coords'])
        invert = json['coords']['inverted']
        size   = self.parse_size(json['size'])
        if event == 2 and id != None:
            extra = self.dialogs[id]
        if event == 3:
            extra = json['next_scene']
        else:
            extra = None
        return Trigger(self.name, event, indica, once, coords, size, invert, extra, locking)

    def parse_json(self, json):
        self.id = json['id']
        self.name =  os.path.join("levels", json['name'])

        for d in json['dialogs']:
            index = d['index']
            title = d['title']
            text = d['text']
            data = d['data']
            options = []
            for o in d['options']:
                options.append(DialogOption(o['text'], o['valid']))
            dia = DialogMenu(data, title, text, options)
            self.dialogs.append(dia)
        self._clog.info("dialog added")

        self._clog.info("populating level")
        for scene in json['scenes']:
            f = FarmFactory()
            f.set_player(self.parse_player(scene['player']))
            for object in scene['objects']:
                f.add_object(self.parse_object(object))
            for enemy in scene['enemies']:
                f.add_enemy(self.parse_enemy(enemy))
            for trigger in scene['triggers']:
                f.add_trigger(self.parse_trigger(trigger))
            for platform in scene['platforms']:
                f.add_platform(self.parse_platform(platform))
            s = Scene(self.name, f, scene['id'], scene['background'], scene['scroll'], scene['sky'])

            self.scenes.append(s)
            self._clog.info("scene added")
