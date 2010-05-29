
from random import randint, uniform

from .gameitem import GameItem
from .glyph import Glyph
from .shapes import Rect, Circle, Cube


class World(object):

    def __init__(self):
        self.items = {}

    def init(self):
        pass

    def add(self, item):
        self.items[item.id] = item

        item.glyph = Glyph()
        item.glyph.from_geometry(item)
        

    def update(self, _):
        for item in self.items.itervalues():
            item.update()



def rand_color():
    return (
        uniform(0, 1),
        uniform(0, 1),
        uniform(0, 1),
        uniform(0, 1),
    )

def populate(world):

    grey = (0.5, 0.5, 0.5, 1)

    for i in xrange(1, 150):
        rect = GameItem(Cube(1), rand_color())
        arena = 4
        rect.position = (
            randint(-arena, +arena),
            randint(-arena, +arena),
            randint(-arena, +arena),
        )
        world.add(rect)

