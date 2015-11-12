
from __future__ import division

from math import pi
from random import choice, uniform

from pyglet.window import key

from .component.shapes import (
    MultiShape, Cube, CubeGlob, Cuboid, CubeCorners, CubeCross, CubeFrame,
    CubeLattice, CubeRing, DualTetrahedron, Ring, TriRing, RgbCubeCluster,
    Tetrahedron, TriangleSquare, TruncatedCube, SpaceStation,
)
from .component.slowmo import SlowMo
from .component.spinner import Spinner
from .component.wobblyorbit import Orbit
from .component.color import (
    Color, red, orange, yellow, green, cyan, blue, purple, white,
    grey, black,
)
from .engine.gameitem import GameItem
from .geometry.koch_cube import KochCube
from .geometry.koch_tetra import KochTetra
#from .geometry.sierpinski_tetra import SierpinskiTetra
from .geometry.orientation import Orientation
from .geometry.vec3 import Origin, Vec3, XAxis


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

    bestiary[key._5] = GameItem(
        shape=DualTetrahedron(1.8),
        position=Origin,
    )

    bestiary[key._6] = GameItem(
        shape=CubeCross(1, red, red.tinted(yellow)),
        position=Origin,
    )

    bestiary[key._7] = GameItem(
        shape=CubeCorners(1, yellow.tinted(white), yellow),
        position=Origin,
    )

    bestiary[key.Q] = GameItem(
        shape=Ring(Cube(1, cyan.tinted(white).variations()), 2, 13),
        position=Origin,
    )

    bestiary[key.W] = GameItem(
        shape=Ring(
            TruncatedCube(1, 0.67, [orange.tinted(grey), orange.tinted(yellow)]),
            3,
            22),
        position=Origin,
        spin=Spinner(speed=-0.5),
    )

    bestiary[key.E] = GameItem(
        shape=Ring(
            DualTetrahedron(1, orange.tinted(black, 0.5), orange.tinted(black)),
            4,
            54,
        ),
        position=Origin,
        orientation=XAxis,
        spin=Spinner(speed=1),
    )

    bestiary[key.R] = GameItem(
        shape=TriRing(1, 6, 32, orange.tinted(white).variations()),
        position=Origin,
        orientation=XAxis,
        spin=Spinner(speed=1.5),
    )

    bestiary[key.T] = GameItem(
        shape=CubeFrame(10, [grey.tinted(white)]),
        position=Origin,
    )

    bestiary[key.Y] = GameItem(
        shape=CubeFrame(13, [grey]),
        position=Origin,
        spin=Spinner(),
    )

    bestiary[key.U] = GameItem(
        shape=CubeGlob(50, 12000, [red]),
        position=Origin,
    )

    bestiary[key.I] = GameItem(
        shape=RgbCubeCluster(1.0, 20, 4000),
        position=Origin,
    )

    bestiary[key.A] = GameItem(
        shape=KochCube(
            Cube(3, face_colors=[red]),
            5,
            tip_color=yellow,
        ),
        spin=Spinner(speed=0.2),
        move=Orbit(10, speed=0.1, phase=0),
    )

    bestiary[key.S] = GameItem(
        shape=KochTetra(
            Tetrahedron(10, face_colors=[purple]),
            5,
            tip_color=white,
        ),
        move=Orbit(10, speed=0.1, phase=pi),
        spin=Spinner(speed=0.2),
    )

    #bestiary[key.D] = GameItem(
        #shape=SierpinskiTetra(
            #Tetrahedron(240), 6, scale=0.52,
            #face_colors=[yellow],
        #),
        #position=Origin,
    #)

    edge = 40

    def camera_inside():
        return all(abs(dist) < edge/2 for dist in world.camera.position)

    bestiary[key.F] = GameItem(
        slowmo=SlowMo(camera_inside, 0.2),
        position=Origin,
        shape=CubeLattice(1, edge, 2, white),
    )

    # code to test performance with many indpendantly positioned and oriented
    # cubes in the world
    if 0:
        NUM_CUBES = 873
        SIZE = 16
        for _ in range(NUM_CUBES):
            world.add( GameItem(
                shape=Cube(
                    uniform(1, 1.2) ** 4,
                    red.tinted(black, uniform(0, 0.5)),
                ),
                position=Vec3(
                    uniform(-SIZE, SIZE),
                    uniform(-SIZE, SIZE),
                    uniform(-SIZE, SIZE),
                ),
                orientation=Orientation.Random(),
            ) )

    return bestiary

