
from __future__ import division

from .engine.gameitem import GameItem
from .component.glyph import Glyph
from .component.position import Position
from .component.shapes import Cube, CubeCluster


def populate(world):
    shape = CubeCluster(1.0, 80, 9000)
    item = GameItem(
        position=Position(0, 0, 0),
        shape=shape,
        glyph=Glyph(),
    )
    world.add(item)


def populate_two_squares(world):
    white = (1, 1, 1, 1)
    red = (1, 0, 0, 1)

    item = GameItem(
        position=Position(0, 0, 0),
        shape=Cube(2, white),
        glyph=Glyph(),
    )
    world.add(item)

    item = GameItem(
        position=Position(1, 1, 0),
        shape=Cube(1, red),
        glyph=Glyph(),
    )
    world.add(item)


