from gameitem import GameItem
from glyph import Glyph
from shapes import Rect, Circle

class World(object):

    _next_id = 0

    def __init__(self):
        self.items = {}

    def init(self):
        pass

    def add(self, item):
        item.itemid = World._next_id
        self.items[World._next_id] = item
        World._next_id += 1

        item.glyph = Glyph()
        item.glyph.from_geometry(item)
        

    def update(self, _):
        for item in self.items.itervalues():
            item.update()


def populate(world):

    white = (1, 1, 1, 1)
    grey = (0.5, 0.5, 0.5, 1)

    wall = GameItem(Rect(30, 4), grey)
    wall.position = (0, 11.5)
    world.add(wall)

    wall = GameItem(Rect(4, 25), grey)
    wall.position = (-15, 0)
    world.add(wall)

    wall = GameItem(Rect(4, 25), grey)
    wall.position = (+15, 0)
    world.add(wall)

    bat = GameItem(Rect(3, 0.67), white)
    bat.position = (0, -8)
    world.add(bat)

    ball = GameItem(Circle(0.33), white)
    ball.position = (0, 8)
    world.add(ball)

