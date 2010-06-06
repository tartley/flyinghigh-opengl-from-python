
from ..component.glyph import Glyph


class World(object):

    clearColor = (0.3, 0.3, 0.3, 1)

    def __init__(self):
        self.items = {}

    def add(self, item):
        self.items[item.id] = item

        if hasattr(item, 'shape'):
            item.glyph = Glyph()
            item.glyph.from_shape(item.shape)


    def update(self, dt):
        for item in self.items.itervalues():
            if hasattr(item, 'move'):
                item.position = item.move(dt)

