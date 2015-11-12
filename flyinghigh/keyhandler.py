
from __future__ import division

from pyglet import image
from pyglet.window import key 

from .component.wobblyorbit import WobblyOrbit


ZOOM_SPEED = 2.0

image_no = 0


class KeyHandler(object):

    def __init__(self, world, bestiary):
        self.world = world
        self.bestiary = bestiary

    def on_key_press(self, symbol, modifiers):
        global image_no

        if symbol in self.bestiary:
            item = self.bestiary[symbol]
            if item in self.world:
                self.world.remove( self.bestiary[symbol] )
            else:
                self.world.add( item )

        elif symbol in (key.PAGEUP, key.PAGEDOWN):

            zoom = ZOOM_SPEED
            if symbol == key.PAGEDOWN:
                zoom = 1 / ZOOM_SPEED

            if modifiers & key.MOD_SHIFT:
                self.world.camera.move.desired_variance *= zoom
            else:
                self.world.camera.move.desired_mean *= zoom

        elif symbol == key.BACKSPACE:
            itemid = max(i for i in self.world.items.keys())
            self.world.items.pop(itemid)

        elif symbol == key.SPACE:
            itemid = max(i for i in self.world.items.keys())
            item = self.world.items[itemid]
            if hasattr(item, 'old_move'):
                item.move = item.old_move
                del item.old_move
            else:
                item.old_move = getattr(item, 'move', None)
                item.move = WobblyOrbit(4, 3)

        elif symbol == key.F12:
            image.get_buffer_manager().get_color_buffer().save(
                'screenshot%02d.png' % (image_no,))
            image_no += 1


