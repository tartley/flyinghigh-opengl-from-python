
from pyglet.window import key 

from .component.wobblyorbit import WobblyOrbit


class KeyHandler(object):

    def __init__(self, world, bestiary):
        self.world = world
        self.bestiary = bestiary

    def on_key_press(self, symbol, modifiers):

        if symbol in (key.PAGEUP, key.PAGEDOWN):
            zoom = 2 if symbol == key.PAGEUP else 0.5
            if modifiers & key.MOD_SHIFT:
                self.world.camera.move.desired_variance *= zoom
            else:
                self.world.camera.move.desired_mean *= zoom

        elif symbol in self.bestiary:
            item = self.bestiary[symbol]
            if item in self.world:
                self.world.remove( self.bestiary[symbol] )
            else:

                if modifiers & key.MOD_SHIFT:
                    item.move = WobblyOrbit(3, 1)
                else:
                    item.move = None

                self.world.add( self.bestiary[symbol] )

