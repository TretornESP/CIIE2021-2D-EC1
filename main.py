#!/usr/bin/env python

from game import Director, MainScene

if __name__ == '__main__':
    director = Director()
    director.push_scene(MainScene(director))
    director.execute()
