#!/usr/bin/env python

from game import ResourceManager
from game.scenes import MainMenu
import sys, getopt

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:v", ["help", "invulnerable"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(str(err))  # will print something like "option -a not recognized"
        sys.exit(2)
    invulnerable = False
    verbose = False
    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            print("Options: --invulnerable")
            sys.exit()
        elif o in ("-i", "--invulnerable"):
            invulnerable = True
        else:
            assert False, "unhandled option"

    director = ResourceManager.load_director()
    director.push_scene(MainMenu(invulnerable))
    director.execute()
