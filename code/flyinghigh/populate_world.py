
from __future__ import division

from .engine.gameitem import GameItem
from .geometry.vec3 import Vec3, ZAxis
from .geometry.orientation import Orientation
from .geometry.koch_cube import KochCube
from .geometry.koch_tetra import KochTetra
from .geometry.sierpinski_tetra import SierpinskiTetra
from .component.slowmo import SlowMo
from .component.spinner import Spinner
from .component.shapes import (
    MultiShape, Cube, CubeCross, CubeLattice, RgbCubeCluster, Shape,
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

    # world.add( GameItem(
        # shape=Shape(SierpinskiTetra(Tetrahedron(40), 7)),
        # spin=Spinner(speed=4),
        # position=Vec3(0, 0, 0),
    # ) )

    world.add( GameItem(
        shape=Shape(SierpinskiTetra(Tetrahedron(40), 7, scale=0.52),
                    color=(0xff, 0xff, 0, 0xff)),
        spin=Spinner(speed=4),
        position=Vec3(0, 0, 0),
    ) )

    # world.add( GameItem(
        # shape=Shape(SierpinskiTetra(Cube(20), 3, scale=0.4),
                    # color=(0x80, 0, 0x80, 0xff)),
        # spin=Spinner(speed=4),
        # position=Vec3(0, 15, 0),
    # ) )

    # world.add( GameItem(
        # shape=Shape(KochCube(Cube(2), 5), color=yellow),
        # spin=Spinner(speed=2),
    # ) )

    # world.add( GameItem(
        # shape=Shape(KochTetra(Tetrahedron(4), 5)),
        # spin=Spinner(speed=4),
        # position=Vec3(0, -4, 4),
    # ) )

    world.add( GameItem(
        position=Vec3(-4, 4, 0),
        shape=CubeCross(),
        spin=Spinner(speed=3),
        move=WobblyOrbit(5, 4),
    ) )

    world.add( GameItem(
        shape=RgbCubeCluster(1.0, 60, 1150),
    ) )

    edge = 48
    darkgrey = (20, 20, 20, 80)
    shape = MultiShape()
    shape.add(CubeLattice(1.0, edge, 8))
    shape.add(Shape(Cube(edge), color=darkgrey))
    world.add( GameItem(
        shape=shape,
        slowmo=SlowMo(edge, 0.2),
    ) )

