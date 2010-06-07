
from __future__ import division

from .engine.gameitem import GameItem
from .geometry.vec3 import Vec3, Origin
from .geometry.orientation import Orientation
from .component.slowmo import SlowMo
from .component.spinner import Spinner
from .component.shapes import (
    CompositeShape, Cube, CubeCross, CubeLattice, RgbCubeCluster, Tetrahedron,
)


def populate(world):
    world.add( GameItem(
        position=Origin,
        shape=CubeCross(),
        spin=Spinner(speed=3),
    ) )

    world.add( GameItem(
        position=Origin,
        shape=RgbCubeCluster(1.0, 60, 11500),
        spin=Spinner(speed=1),
    ) )

    orange = (255, 255, 0, 255)
    world.add( GameItem(
        position=Origin,
        shape=Tetrahedron(80, orange),
    ) )

    edge = 48
    darkgrey = (20, 20, 20, 80)
    shape = CompositeShape()
    shape.add(CubeLattice(1.0, edge, 8))
    shape.add(Cube(edge, darkgrey))
    world.add( GameItem(
        position=Origin,
        shape=shape,
        slowmo=SlowMo(edge, 0.2),
    ) )

def populate2(world):
    red = (255, 0, 0, 127)
    world.add( GameItem(
        position=Origin,
        shape=Cube(2, red),
        orientation=Orientation((1, 1, 0)),
    ) )
    white = (255, 255, 255, 127)
    world.add ( GameItem(
        position=Vec3(1, 1, 0),
        shape=Cube(1, white),
        orientation=Orientation((0, 1, 1)),
    ) )

