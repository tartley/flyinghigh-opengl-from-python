
from __future__ import division

from itertools import repeat
from random import uniform

from .component.shapes import (
    MultiShape, Cube, CubeCorners, CubeCross, CubeLattice, RgbCubeCluster,
    Tetrahedron,
)
from .component.slowmo import SlowMo
from .component.spinner import Spinner
from .component.wobblyorbit import WobblyOrbit
from .engine.gameitem import GameItem
from .geometry.koch_cube import KochCube
from .geometry.koch_tetra import KochTetra
from .geometry.sierpinski_tetra import SierpinskiTetra
from .geometry.orientation import Orientation
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
    white = (255, 255, 255, 255)

    world.add( GameItem(
        shape=SierpinskiTetra(
            Tetrahedron(40), 6, scale=0.52,
            face_colors=repeat(yellow),
        ),
        position=Vec3(0, 0, 0),
        orientation=Orientation(ZAxis),
        spin=Spinner(speed=0.5),
    ) )

    world.add( GameItem(
        shape=KochCube(
            Cube(5, face_colors=repeat(red)),
            5,
            tip_color=yellow,
        ),
        spin=Spinner(speed=0.2),
        position=(-10, 0, 0),
    ) )

    world.add( GameItem(
        shape=KochTetra(
            Tetrahedron(20, face_colors=repeat(purple)),
            6,
            tip_color=white,
        ),
        position=(10, 0, 0),
    ) )

    world.add( GameItem(
        shape=CubeCross(),
        spin=Spinner(speed=3),
    ) )

    for color in (orange, green, red, blue, yellow, purple):
        world.add( GameItem(
            shape=Cube(
                1,
                face_colors=repeat(color),
            ),
            spin=Spinner(speed=10),
            move=WobblyOrbit(3, speed=uniform(4, 5)),
        ) )

    world.add( GameItem(
        shape=RgbCubeCluster(1.0, 60, 5000),
    ) )

    edge = 38

    def is_inside():
        '''True if camera is inside cube of the given edge at the origin'''
        position = camitem.position
        dist = max(abs(position.x), abs(position.y), abs(position.z))
        return dist < edge / 2

    darkgrey = (20, 20, 20, 80)
    shape = MultiShape()
    shape.add(CubeLattice(1.0, edge, 8, white))
    shape.add(Cube(edge, face_colors=repeat(darkgrey)))
    world.add( GameItem(
        shape=shape,
        slowmo=SlowMo(is_inside, 0.2),
    ) )

