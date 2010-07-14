
from __future__ import division

from .component.shapes import (
    MultiShape, Cube, CubeCorners, CubeCross, CubeLattice, RgbCubeCluster,
    Shape
)
from .component.slowmo import SlowMo
from .component.spinner import Spinner
from .component.wobblyorbit import WobblyOrbit
from .engine.gameitem import GameItem
from .geometry.geometry import Tetrahedron
from .geometry.koch_cube import KochCube
from .geometry.koch_tetra import KochTetra
from .geometry.orientation import Orientation
from .geometry.sierpinski_tetra import SierpinskiTetra
from .geometry.vec3 import Origin, Vec3, ZAxis



def populate(world, camera):
    camitem = GameItem(
        position=Origin,
        camera=camera,
        move=WobblyOrbit(80, 75, speed=0.5),
    )
    world.add(camitem)

    red = (255, 0, 0, 255)
    orange = (255, 127, 0, 255)
    yellow = (255, 255, 0, 255)
    green = (0, 255, 0, 255)
    blue = (0, 0, 255, 255)
    purple = (255, 0, 255, 255)

    # world.add( GameItem(
        # shape=Shape(SierpinskiTetra(Tetrahedron(40), 7)),
        # spin=Spinner(speed=4),
        # position=Vec3(0, 0, 0),
    # ) )

    world.add( GameItem(
        shape=Shape(SierpinskiTetra(Tetrahedron(40), 7, scale=0.52),
                    color=(0xff, 0xff, 0, 0xff)),
        position=Vec3(0, 0, 0),
        orientation=Orientation(ZAxis),
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
        shape=CubeCorners(),
        spin=Spinner(speed=3),
    ) )

    for color in (orange, green, red, blue, yellow, purple):
        world.add( GameItem(
            shape=Shape(Cube(1), color=color),
            spin=Spinner(speed=20),
            move=WobblyOrbit(3, speed=10),
        ) )

    world.add( GameItem(
        shape=RgbCubeCluster(1.0, 60, 1150),
    ) )

    edge = 48

    def is_inside():
        '''True if camera is inside cube of the given edge at the origin'''
        position = camitem.position
        dist = max(abs(position.x), abs(position.y), abs(position.z))
        return dist < edge / 2

    darkgrey = (20, 20, 20, 80)
    shape = MultiShape()
    shape.add(CubeLattice(1.0, edge, 8))
    shape.add(Shape(Cube(edge), color=darkgrey))
    world.add( GameItem(
        shape=shape,
        slowmo=SlowMo(is_inside, 0.2),
    ) )

