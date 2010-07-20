
from .engine import startup
startup

import pyglet

from .engine.gameloop import Gameloop
from .bestiary import get_bestiary
from .keyhandler import KeyHandler


def run_game():
    try:
        gameloop = Gameloop()
        gameloop.prepare()

        bestiary = get_bestiary(gameloop.world)
        keyhandler = KeyHandler(gameloop.world, bestiary)
        keyhandler.world = gameloop.world

        gameloop.window.push_handlers(keyhandler.on_key_press)
        gameloop.world.update(0)
        gameloop.window.set_visible()
        pyglet.app.run()
    finally:
        gameloop.stop()


def main():
    run_game()

