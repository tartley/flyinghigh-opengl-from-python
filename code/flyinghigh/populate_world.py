
from __future__ import division

from itertools import repeat
from random import uniform

from .component.shapes import (
    MultiShape, Cube, CubeCorners, CubeCross, CubeLattice, RgbCubeCluster,
    Tetrahedron, TriangleSquare
)
from .component.slowmo import SlowMo
from .component.spinner import Spinner
from .component.wobblyorbit import WobblyOrbit
from .engine.gameitem import GameItem
from .geometry.koch_cube import KochCube
from .geometry.koch_tetra import KochTetra
from .geometry.sierpinski_tetra import SierpinskiTetra
from .geometry.orientation import Orientation
from .geometry.vec3 import Origin, Vec3, XAxis, ZAxis, NegZAxis


def color_invert(color):
    r, g, b, _ = color
    return (
        255 - r,
        255 - g,
        255 - b,
        255
    )


def populate(world, camera):
    camitem = GameItem(
        position=(-5, 0, 0),
        camera=camera,
        # move=WobblyOrbit(80, 75, speed=0.5),
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
        shape=TriangleSquare(),
    ) )

    # world.add( GameItem(
        # shape=SierpinskiTetra(
            # Tetrahedron(4), 6, scale=0.52,
            # face_colors=repeat(yellow),
        # ),
        # position=Vec3(0, 0, 5),
        # orientation=Orientation(ZAxis),
        # spin=Spinner(speed=0.75),
    # ) )

    # world.add( GameItem(
        # shape=KochCube(
            # Cube(3, face_colors=repeat(red)),
            # 5,
            # tip_color=yellow,
        # ),
        # spin=Spinner(speed=0.2),
        # position=(5, 5, 0),
    # ) )

    # world.add( GameItem(
        # shape=KochTetra(
            # Tetrahedron(10, face_colors=repeat(purple)),
            # 5,
            # tip_color=white,
        # ),
        # position=(-5, 0, 0),
    # ) )

    # world.add( GameItem(
        # shape=CubeCross(),
        # spin=Spinner(speed=3),
    # ) )

    # for color in (orange, green, red, blue, yellow, purple, white):
        # shape = MultiShape()
        # shape.add(
            # Tetrahedron(
                # 1,
                # face_colors=repeat(color),
            # )
        # )
        # shape.add(
            # Tetrahedron(
                # 1,
                # face_colors=repeat(color_invert(color)),
            # ),
            # orientation=Orientation(XAxis),
        # )
        # world.add( GameItem(
            # shape=shape,
            # spin=Spinner(speed=uniform(8, 12)),
            # move=WobblyOrbit(2, speed=uniform(4, 5)),
        # ) )

    # world.add( GameItem(
        # shape=RgbCubeCluster(1.0, 60, 5000),
    # ) )

    # edge = 38

    # def is_inside():
        # '''True if camera is inside cube of the given edge at the origin'''
        # position = camitem.position
        # dist = max(abs(position.x), abs(position.y), abs(position.z))
        # return dist < edge / 2

    # darkgrey = (20, 20, 20, 80)
    # shape = MultiShape()
    # shape.add(CubeLattice(1.0, edge, 8, white))
    # shape.add(Cube(edge, face_colors=repeat(darkgrey)))
    # world.add( GameItem(
        # shape=shape,
        # slowmo=SlowMo(is_inside, 0.2),
    # ) )

