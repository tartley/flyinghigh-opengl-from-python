
from __future__ import division

from .engine.gameitem import GameItem
from .geometry.vec3 import Vec3, Origin
from .geometry.serpinski import Serpinski
from .component.slowmo import SlowMo
from .component.spinner import Spinner
from .component.shapes import (
    CompositeShape, Cube, CubeCross, CubeLattice, RgbCubeCluster, Tetrahedron,
)
from .component.wobblyorbit import WobblyOrbit


def populate(world):
    world.camera.move = WobblyOrbit()

    world.add( GameItem(
        position=Vec3(4, 0, 0),
        shape=CubeCross(),
        spin=Spinner(speed=3),
    ) )

    world.add( GameItem(
        position=Origin,
        shape=RgbCubeCluster(1.0, 60, 1150),
    ) )

    # orange = (255, 127, 0, 255)
    # shape = Serpinski(Tetrahedron(80, orange))
    # world.add( GameItem(
        # position=Origin,
        # shape=shape,
        # spin=Spinner(speed=2),
    # ) )

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

