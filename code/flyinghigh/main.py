
from sys import argv

from .engine import startup
startup

import pyglet

from .engine.gameloop import Gameloop
from .bestiary import get_bestiary
from .keyhandler import KeyHandler


class Options(object):

    def __init__(self, argv):
        self.fullscreen = '--fullscreen' in argv or '-f' in argv


def run_game():
    try:
        options = Options(argv)
        gameloop = Gameloop()
        gameloop.prepare(options)

        bestiary = get_bestiary(gameloop.world)
        keyhandler = KeyHandler(gameloop.world, bestiary)
        keyhandler.world = gameloop.world

        gameloop.window.push_handlers(keyhandler.on_key_press)
        gameloop.world.update(1/60.0)
        gameloop.window.set_visible()
        pyglet.app.run()
    finally:
        gameloop.stop()


def main():
    run_game()

