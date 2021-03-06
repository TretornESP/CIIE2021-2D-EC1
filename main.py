#!/usr/bin/env python

from game import ResourceManager
from game.scenes import MainMenu
import sys, getopt, os

if __name__ == '__main__':
    sys.path.append(os.getcwd())
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:v", ["help", "invulnerable"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(str(err))  # will print something like "option -a not recognized"
        sys.exit(2)
    invulnerable = False
    verbose = False
    for o, a in opts:
        if o in ("-h", "--help"):
            print("Options: --invulnerable --debug_scene=name")
            sys.exit()
        if o in ("-i", "--invulnerable"):
            invulnerable = True
        if o in ("-d", "--debug"):
            ResourceManager.enable_debug(a)

    director = ResourceManager.load_director()
    director.push_scene(MainMenu(invulnerable))
    director.execute()
