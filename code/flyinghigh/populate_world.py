
from __future__ import division

from .engine.gameitem import GameItem
from .geometry.vec3 import Vec3, Origin
from .geometry.orientation import Orientation
from .component.slowmo import SlowMo
from .component.spinner import Spinner
from .component.shapes import (
    MultiShape, Cube, CubeCross, CubeLattice, RgbAxes, RgbCubeCluster, Shape,
    Tetrahedron,
)
from .component.wobblyorbit import WobblyOrbit


def populate(world):
    world.camera.move = WobblyOrbit(80, 75)

    red = (255, 0, 0, 255)
    orange = (255, 127, 0, 255)
    yellow = (255, 255, 0, 255)
    green = (0, 255, 0, 255)
    blue = (0, 0, 255, 255)

    world.add( GameItem(
        shape=RgbAxes(),
    ) )

    shape=MultiShape(
        Shape(
            geometry=Cube(2),
            color=orange,
            position=(0, 2, 2),
            orientation=(0.2, 0, -1),
        ),
        Shape(
            geometry=Cube(2),
            color=red,
            position=(1, 1, -1),
            orientation=(1, 1, 0),
        )
    )
    shape.add( Shape(
        geometry=Cube(1),
        color=yellow,
        position=(-1, -1, -1),
    ) )
    world.add(
        GameItem(
            shape=shape,
            spin=Spinner(speed=1),
        )
    )

    world.add( GameItem(
        position=Vec3(4, 0, 0),
        shape=CubeCross(),
        orientation=Orientation((1, 2, 3)),
        spin=Spinner(speed=3),
    ) )

    world.add( GameItem(
        position=Origin,
        shape=RgbCubeCluster(1.0, 60, 11500),
    ) )

    world.add( GameItem(
        position=(0, 0, 3),
        shape=Shape(Tetrahedron(1), orange),
        spin=Spinner(speed=2),
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

