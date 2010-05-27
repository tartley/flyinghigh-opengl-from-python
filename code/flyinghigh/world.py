from gameitem import Bat, Ball, Wall
from glyph import Glyph
from shapes import Rect, Circle

class World(object):

    _next_id = 0

    def __init__(self):
        self.items = {}

    def init(self):
        pass

    def add(self, item, position):
        item.itemid = World._next_id
        self.items[World._next_id] = item
        World._next_id += 1

        item.glyph = Glyph.from_item(item)
        

    def update(self):
        for item in self.items.itervalues():
            item.update()


def populate(world):

    white = (1, 1, 1, 1)
    grey = (0.5, 0.5, 0.5, 1)

    wall = Wall(Rect(30, 4), grey)
    world.add(wall, (0, 11.5))

    wall = Wall(Rect(4, 25), grey)
    world.add(wall, (-16, 0))

    wall = Wall(Rect(4, 25), grey)
    world.add(wall, (+16, 0))

    world.bat = Bat(Rect(3, 0.67), white)
    world.add(world.bat, (0, -8))

    ball = Ball(Circle(0.33), white)
    world.add(ball, (0, 8))

