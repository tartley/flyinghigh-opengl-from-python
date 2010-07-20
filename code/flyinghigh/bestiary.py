
from __future__ import division

from pyglet.window import key

from .component.shapes import (
    MultiShape, Cube, CubeCorners, CubeCross, CubeLattice, CubeRing,
    DualTetrahedron, TriRing,
    RgbCubeCluster, Tetrahedron, TriangleSquare, TruncatedCube, SpaceStation,
)
from .component.slowmo import SlowMo
from .component.spinner import Spinner
from .component.wobblyorbit import WobblyOrbit
from .component.color import (
    Color, red, orange, yellow, green, cyan, blue, purple, white, grey, black,
)
from .engine.gameitem import GameItem
from .geometry.koch_cube import KochCube
from .geometry.koch_tetra import KochTetra
from .geometry.sierpinski_tetra import SierpinskiTetra
from .geometry.orientation import Orientation
from .geometry.vec3 import Origin, Vec3, XAxis, ZAxis, NegZAxis


def get_bestiary(world):
    bestiary = {}

    bestiary[key._0] = GameItem(
        shape=TriangleSquare(),
        position=Origin,
    )

    bestiary[key._1] = GameItem(
        shape=Tetrahedron(1.8, blue.variations(cyan)),
        position=Origin,
    )

    bestiary[key._2] = GameItem(
        shape=Cube(0.9, green.variations(yellow)),
        position=Origin,
    )

    bestiary[key._3] = GameItem(
        shape=TruncatedCube(1, colors=[orange, orange.tinted(red, 0.5)]),
        position=Origin,
    )

    bestiary[key._4] = GameItem(
        shape=SpaceStation(1.1),
        position=Origin,
    )

    bestiary[key.Q] = GameItem(
        shape=DualTetrahedron(1.8),
        spin=Spinner(speed=3),
        position=Origin,
    )

    bestiary[key.W] = GameItem(
        shape=CubeCross(1, red, red.tinted(yellow)),
        spin=Spinner(speed=3),
        position=Origin,
    )

    bestiary[key.E] = GameItem(
        shape=CubeCorners(1, yellow.tinted(white), yellow),
        spin=Spinner(speed=3),
        position=Origin,
    )

    bestiary[key.R] = GameItem(
        shape=CubeRing(1, 2, 7, white.variations()),
        position=Origin,
    )

    bestiary[key.T] = GameItem(
        shape=CubeRing(1, 3, 23, green.tinted(black).variations()),
        position=Origin,
    )

    bestiary[key.Y] = GameItem(
        shape=CubeRing(1, 4, 24, green.tinted(white).variations()),
        position=Origin,
        orientation=XAxis,
    )

    bestiary[key.U] = GameItem(
        shape=TriRing(1, 6, 32, orange.tinted(white).variations()),
        position=Origin,
        orientation=XAxis,
        spinner=Spinner(),
    )

    # world.add( GameItem(
        # shape=SierpinskiTetra(
            # Tetrahedron(4), 6, scale=0.52,
            # face_colors=repeat(yellow),
        # ),
        # position=Vec3(0, 0, 5),
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

    # for color in (orange, green, red, blue, yellow, purple, white):
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
        # position = world.camera.position
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

    return bestiary


