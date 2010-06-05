
from __future__ import division

from .engine.gameitem import GameItem
from .component.glyph import Glyph
from .geometry.vec3 import Vec3
from .component.shapes import CompositeShape, Cube, CubeCross, CubeCluster, Shape


def populate(world):
    shape = CompositeShape()
    shape = CubeCluster(1.0, 80, 1600)
    shape.add(CubeCross())
    #shape.add(Cube(80, (0.1, 0.1, 0.1, 0.4)), Vec3(0, 0, 0))

    item = GameItem(
        position=Vec3(0, 0, 0),
        shape=shape,
        glyph=Glyph(),
    )
    world.add(item)


def populate2(world):
    red = (1, 0, 0, 0.5)
    world.add( GameItem(
        position=Vec3(0, 0, 0),
        shape=Cube(2, red),
        glyph=Glyph(),
    ) )
    white = (1, 1, 1, 0.5)
    world.add ( GameItem(
        position=Vec3(1, 1, 0),
        shape=Cube(1, white),
        glyph=Glyph(),
    ) )


