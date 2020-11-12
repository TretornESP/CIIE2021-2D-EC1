#!/usr/bin/env python

from game import ResourceManager
from game.scenes import MainMenu

if __name__ == '__main__':
    director = ResourceManager.load_director()
    director.push_scene(MainMenu())
    director.execute()
