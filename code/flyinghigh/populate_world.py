
from __future__ import division
from math import sqrt

from .engine.gameitem import GameItem
from .geometry.vec3 import Vec3, Origin
from .geometry.orientation import Orientation
from .geometry.serpinski import Serpinski
from .component.slowmo import SlowMo
from .component.spinner import Spinner
from .component.shapes import (
    MultiShape, Cube, CubeCross, CubeLattice, RgbAxes, RgbCubeCluster, Shape,
    Tetrahedron,
)
from .component.wobblyorbit import WobblyOrbit


def populate(world):
    world.camera.move = WobblyOrbit(10, 2)

    red = (255, 0, 0, 255)
    orange = (255, 127, 0, 255)
    yellow = (255, 255, 0, 255)
    green = (0, 255, 0, 255)
    blue = (0, 0, 255, 255)

    world.add( GameItem(
        shape=Shape(Serpinski(Tetrahedron(4), 2), orange),
        spin=Spinner(speed=4),
    ) )

    world.add( GameItem(
        position=Vec3(4, 0, 0),
        shape=CubeCross(),
        orientation=Orientation((1, 2, 3)),
        spin=Spinner(speed=3),
    ) )

    world.add( GameItem(
        position=Origin,
        shape=RgbCubeCluster(1.0, 60, 1150),
    ) )

    edge = 48
    darkgrey = (20, 20, 20, 80)
    shape = MultiShape()
    shape.add(CubeLattice(1.0, edge, 8))
    shape.add(Shape(Cube(edge), color=darkgrey))
    world.add( GameItem(
        position=Origin,
        shape=shape,
        slowmo=SlowMo(edge, 0.2),
    ) )

