
from random import choice, randint, uniform

from .engine.gameitem import GameItem
from .component.glyph import Glyph
from .component.position import Position
from .component.shapes import CompositeShape, Cube


def rand_color():
    return (
        uniform(0, 1),
        uniform(0, 1),
        uniform(0, 1),
        1,
    )

def populate(world):

    shape = CompositeShape()
    unitcube = Cube(1)
    for i in xrange(200):
        pos = [
            randint(-4, +4),
            randint(-4, +4),
            randint(-4, +4),
        ]
        shape.add(unitcube, Position(*pos))      

    item = GameItem(
        position=Position(0, 0, 0),
        geometry=shape,
        color=rand_color(),
        glyph=Glyph(),
    )
    item.glyph.from_geometry(item)
    world.add(item)

