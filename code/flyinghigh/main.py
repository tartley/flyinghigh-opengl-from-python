
from . import startup
startup

import subprocess
import sys

import pyglet

from .gameloop import Gameloop


def run_game():
    try:
        gameloop = Gameloop()
        gameloop.init()
        pyglet.app.run()
    finally:
        gameloop.stop()


def profile(command):
    import cProfile
    filename = 'profile.out'
    cProfile.runctx( command, globals(), locals(), filename=filename )

    # runsnake must be installed either using:
    #   easy_install RunSnakeRun SquareMap
    # or download from here:
    #   http://www.vrplumber.com/programming/runsnakerun/
    # also needs wxPython, from here:
    #   http://www.wxpython.org/download.php#binaries
    subprocess.call( ['runsnake', filename] )


def main():
    if '--profile' in sys.argv:
        profile('run_game()')
    else:
        run_game()


if __name__ == '__main__':
    main()

