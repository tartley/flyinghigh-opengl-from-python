
from __future__ import division

from .engine.gameitem import GameItem
from .component.glyph import Glyph
from .geometry.vec3 import Vec3
from .component.shapes import Cube, CubeCluster


def populate(world):
    shape = CubeCluster(1.0, 80, 90)
    item = GameItem(
        position=Vec3(0, 0, 0),
        shape=shape,
        glyph=Glyph(),
    )
    world.add(item)


def populate_twocubes(world):
    red = (1, 0, 0, 1)
    world.add( GameItem(
        position=Vec3(0, 0, 0),
        shape=Cube(2, red),
        glyph=Glyph(),
    ) )
    white = (1, 1, 1, 1)
    world.add ( GameItem(
        position=Vec3(1, 1, 0),
        shape=Cube(1, white),
        glyph=Glyph(),
    ) )


