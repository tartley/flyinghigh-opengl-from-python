
from __future__ import division

from .engine.gameitem import GameItem
from .geometry.vec3 import Vec3
from .component.shapes import CompositeShape, Cube, CubeCross, CubeLattice, RgbCubeCluster


def populate(world):
    shape = CompositeShape()
    shape.add(RgbCubeCluster(1.0, 60, 8000))
    shape.add(CubeLattice(1.0, 40, 10))
    shape.add(Cube(40, (0.1, 0.1, 0.1, 0.4)), Vec3(0, 0, 0))
    shape.add(CubeCross())
    world.add( GameItem(
        position=Vec3(0, 0, 0),
        shape=shape,
    ) )


def populate2(world):
    red = (1, 0, 0, 0.5)
    world.add( GameItem(
        position=Vec3(0, 0, 0),
        shape=Cube(2, red),
    ) )
    white = (1, 1, 1, 0.5)
    world.add ( GameItem(
        position=Vec3(1, 1, 0),
        shape=Cube(1, white),
    ) )


