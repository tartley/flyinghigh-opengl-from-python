
from .engine import startup
startup

import pyglet

from .engine.gameloop import Gameloop
from .populate_world import populate
from .keyhandler import KeyHandler


def run_game():
    try:
        gameloop = Gameloop()
        gameloop.prepare()
        populate(gameloop.world, gameloop.camera)

        keyhandler = KeyHandler()
        keyhandler.world = gameloop.world

        gameloop.window.push_handler(on_key_press)
        gameloop.world.update(0)
        gameloop.window.set_visible()
        pyglet.app.run()
    finally:
        gameloop.stop()


def main():
    run_game()

