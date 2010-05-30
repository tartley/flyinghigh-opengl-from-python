
from random import randint, uniform

from .gameitem import GameItem
from ..component.glyph import Glyph
from ..component.position import Position
from ..component.shapes import Cube


class World(object):

    def __init__(self):
        self.items = {}

    def init(self):
        pass

    def add(self, item):
        self.items[item.id] = item

    def update(self, dt):
        for item in self.items.itervalues():
            if hasattr(item, 'mover'):
                item.mover.update(dt)



def rand_color():
    return (
        uniform(0, 1),
        uniform(0, 1),
        uniform(0, 1),
        1,
    )


def populate(world):

    for i in xrange(1, 150):
        item = GameItem(
            geometry=Cube(1),
            color=rand_color(),
            position=Position(
                randint(-4, +4),
                randint(-4, +4),
                randint(-4, +4),
            ),
            glyph=Glyph(),
        )
        item.glyph.from_geometry(item)

        world.add(item)

