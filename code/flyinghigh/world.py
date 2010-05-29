from random import randint, uniform

from .gameitem import GameItem
from .glyph import Glyph
from .shapes import Rect, Circle


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

    wall = GameItem(Rect(30, 2), grey)
    wall.position = (0, 11.5, 0)
    world.add(wall)

    wall = GameItem(Rect(2, 25), grey)
    wall.position = (-15, 0, 0)
    world.add(wall)

    wall = GameItem(Rect(2, 25), grey)
    wall.position = (+15, 0, 0)
    world.add(wall)

    for i in xrange(1, 20):
        rect = GameItem(Rect(randint(1, 20), 2), rand_color())
        rect.position = (randint(-20, 20), randint(-10, 10), i * 3)
        world.add(rect)

        rect = GameItem(Rect(2, randint(1, 20)), rand_color())
        rect.position = (randint(-20, 20), randint(-10, 10), i * 3 + 1)
        world.add(rect)

    ball = GameItem(Circle(3), (1, 1, 1, 1))
    ball.position = (0, 0, +20)
    world.add(ball)

