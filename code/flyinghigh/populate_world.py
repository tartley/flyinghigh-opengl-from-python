
from __future__ import division

from .engine.gameitem import GameItem
from .geometry.vec3 import Vec3, Origin, XAxis
from .geometry.orientation import Orientation
from .component.spinner import Spinner
from .component.shapes import CompositeShape, Cube, CubeCross, CubeLattice, RgbCubeCluster


def populate(world):
    darkgrey = (20, 20, 20, 80)
    shape = CompositeShape()
    shape.add(RgbCubeCluster(1.0, 60, 11500))
    shape.add(CubeLattice(1.0, 40, 10))
    shape.add(Cube(40, darkgrey))
    world.add( GameItem(
        position=Origin,
        shape=shape,
    ) )
    world.add( GameItem(
        position=Origin,
        shape=CubeCross(),
        orientation=Orientation(XAxis),
        spin=Spinner(),
    ) )
    shape.add(CubeCross())

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

