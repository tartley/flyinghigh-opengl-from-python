
from .engine import startup
startup

import pyglet

from .engine.gameloop import Gameloop
from .populate_world import populate


def run_game():
    try:
        gameloop = Gameloop()
        gameloop.prepare()
        populate(gameloop.world)
        gameloop.world.update(0)
        gameloop.window.set_visible()
        pyglet.app.run()
    finally:
        gameloop.stop()


def main():
    run_game()

