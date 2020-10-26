#!/usr/bin/env python

from game import Director, MainScene
from game.levels import Level

if __name__ == '__main__':
    director = Director()
    level = Level("Level0", director)
    for scene in level.get_scenes():
        director.push_scene(scene)
    director.execute()
