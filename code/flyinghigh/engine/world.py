
import operator

from ..component.glyph import Glyph


class World(object):

    clearColor = (0.3, 0.3, 0.3, 1)

    def __init__(self):
        self.items = {}
        self.time = 0.0

    def add(self, item):
        self.items[item.id] = item

        if hasattr(item, 'shape'):
            item.glyph = Glyph()
            item.glyph.from_shape(item.shape)

        if hasattr(item, 'camera'):
            self.camera = item

    def product(self, *args):
        return reduce(operator.mul, list(*args), 1)

    def _get_rate(self):
        rate = self.product(
            item.slowmo(self.camera.position)
            for item in self.items.itervalues()
            if hasattr(item, 'slowmo'))
        return rate

    def update(self, dt):
        dt *= self._get_rate()
        self.time += dt
        for item in self.items.itervalues():
            if hasattr(item, 'move'):
                item.position = item.move(self.time, dt)
            if hasattr(item, 'spin'):
                item.orientation = item.spin(self.time, dt)

