
from __future__ import division

from .engine.gameitem import GameItem
from .geometry.vec3 import Vec3
from .geometry.orientation import Orientation
from .component.shapes import CompositeShape, Cube, CubeCross, CubeLattice, RgbCubeCluster


def populate(world):
    shape = CompositeShape()
    shape.add(RgbCubeCluster(1.0, 60, 11500))
    shape.add(CubeLattice(1.0, 40, 10))
    darkgrey = (20, 20, 20, 80)
    shape.add(Cube(40, darkgrey), Vec3(0, 0, 0))
    shape.add(CubeCross())
    world.add( GameItem(
        position=Vec3(0, 0, 0),
        shape=shape,
        orientation=Orientation((1, 1, 0)),
    ) )

def populate2(world):
    red = (255, 0, 0, 127)
    world.add( GameItem(
        position=Vec3(0, 0, 0),
        shape=Cube(2, red),
        orientation=Orientation((1, 1, 0)),
    ) )
    white = (255, 255, 255, 127)
    world.add ( GameItem(
        position=Vec3(1, 1, 0),
        shape=Cube(1, white),
        orientation=Orientation((0, 1, 1)),
    ) )

