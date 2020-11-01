#!/usr/bin/env python

from game import Director
from game.scenes import MainMenu

if __name__ == '__main__':
    director = Director()
    director.push_scene(MainMenu(director))
    director.execute()
