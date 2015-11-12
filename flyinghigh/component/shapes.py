
from __future__ import division

from itertools import chain, islice, product, repeat
from math import sqrt, pi, sin, cos
from random import randint

from .color import (
    Color, red, orange, yellow, green, cyan, blue, purple, white, grey, black,
)
from ..engine.shape import Shape, MultiShape
from ..geometry.vec3 import (
    NegXAxis, NegYAxis, NegZAxis, Origin, Vec3, XAxis, YAxis, ZAxis,
)
from ..geometry.orientation import Orientation


def TriangleSquare():
    return Shape(
        vertices=[
            ( 1, -1,  1), # v0
            ( 1, -1, -1), # v1
            (-1, -1, -1), # v2
            (-1, -1,  1), # v3
            ( 1,  1,  0), # v4
        ],
        faces=[ [0, 4, 1], [0, 1, 2, 3], ],
        face_colors=[red, yellow],
    )


def Tetrahedron(edge, face_colors=None):
    size = edge / sqrt(2)/2
    vertices = [
        (+size, +size, +size),
        (-size, -size, +size),
        (-size, +size, -size),
        (+size, -size, -size), 
    ]
    faces = [ [0, 2, 1], [1, 3, 0], [2, 3, 1], [0, 3, 2] ]
    return Shape(vertices, faces, face_colors)


def DualTetrahedron(edge, color1=None, color2=None):
    if color1 is None:
        color1 = Color.Random()
        color2 = Color.Random()
    m = MultiShape()
    m.add( Tetrahedron(edge, color1.variations()) )
    m.add( Tetrahedron(edge, color2.variations()), orientation=Orientation(XAxis) )
    return m


def Cube(edge, face_colors=None):
    e2 = edge / 2
    verts = list(product(*repeat([-e2, +e2], 3)))
    faces = [
        [0, 1, 3, 2], # left
        [4, 6, 7, 5], # right
        [7, 3, 1, 5], # front
        [0, 2, 6, 4], # back
        [3, 7, 6, 2], # top
        [1, 0, 4, 5], # bottom
    ]
    return Shape(verts, faces, face_colors)


def Cuboid(x, y, z, face_colors=None):
    x = x/2
    y = y/2
    z = z/2
    verts = list(product((-x, +x), (-y, +y), (-z, +z)))
    faces = [
        [0, 1, 3, 2], # left
        [4, 6, 7, 5], # right
        [7, 3, 1, 5], # front
        [0, 2, 6, 4], # back
        [3, 7, 6, 2], # top
        [1, 0, 4, 5], # bottom
    ]
    return Shape(verts, faces, face_colors)
    

def TruncatedCube(edge, truncation=0.67, colors=None):
    e2 = edge / 2
    verts = [
        (-e2 + e2 * truncation, -e2, -e2),
        (-e2, -e2 + e2 * truncation, -e2),
        (-e2, -e2, -e2 + e2 * truncation),

        (-e2 + e2 * truncation, -e2, +e2),
        (-e2, -e2 + e2 * truncation, +e2),
        (-e2, -e2, +e2 - e2 * truncation),

        (-e2 + e2 * truncation, +e2, -e2),
        (-e2, +e2 - e2 * truncation, -e2),
        (-e2, +e2, -e2 + e2 * truncation),

        (-e2 + e2 * truncation, +e2, +e2),
        (-e2, +e2 - e2 * truncation, +e2),
        (-e2, +e2, +e2 - e2 * truncation),

        (+e2 - e2 * truncation, -e2, -e2),
        (+e2, -e2 + e2 * truncation, -e2),
        (+e2, -e2, -e2 + e2 * truncation),

        (+e2 - e2 * truncation, -e2, +e2),
        (+e2, -e2 + e2 * truncation, +e2),
        (+e2, -e2, +e2 - e2 * truncation),

        (+e2 - e2 * truncation, +e2, -e2),
        (+e2, +e2 - e2 * truncation, -e2),
        (+e2, +e2, -e2 + e2 * truncation),

        (+e2 - e2 * truncation, +e2, +e2),
        (+e2, +e2 - e2 * truncation, +e2),
        (+e2, +e2, +e2 - e2 * truncation),
    ]
    faces = [
        [ 1,  2,  5,  4, 10, 11,  8,  7], # left
        [14, 13, 19, 20, 23, 22, 16, 17], # right
        [22, 21,  9, 10,  4,  3, 15, 16], # front
        [ 0,  1,  7,  6, 18, 19, 13, 12], # back
        [11,  9, 21, 23, 20, 18, 6,  8], # top
        [ 3,  5,  2,  0, 12, 14, 17, 15], # bottom

        [0, 2, 1],
        [3, 4, 5],
        [6, 7, 8],
        [9, 11, 10],
        [12, 13, 14],
        [15, 17, 16],
        [18, 20, 19],
        [21, 22, 23],
    ]
    face_colors = chain(
        repeat(colors[0], 6),
        repeat(colors[1], 8),
    )
    return Shape(verts, faces, face_colors)


def SpaceStation(edge):

    colors = [grey.tinted(white, 0.5), grey]
    shape = TruncatedCube(edge, truncation=0.999, colors=colors)

    # add the door
    e2 = edge / 2
    HEIGHT = 0.075
    WIDTH = 0.25
    shape.vertices.extend( [
        Vec3(+e2 * 1.001, +e2 * HEIGHT, +e2 * WIDTH),
        Vec3(+e2 * 1.001, +e2 * HEIGHT, -e2 * WIDTH),
        Vec3(+e2 * 1.001, -e2 * HEIGHT, -e2 * WIDTH),
        Vec3(+e2 * 1.001, -e2 * HEIGHT, +e2 * WIDTH),
    ] )
    shape.faces.append( [27, 26, 25, 24] )
    shape.face_colors.append( black )

    return shape


def CubeCross(edge, color1, color2):
    multi = MultiShape()

    multi.add(Cube(edge, face_colors=repeat(color1)))

    for pos in [XAxis, YAxis, ZAxis, NegXAxis, NegYAxis, NegZAxis]:
        center = pos * (edge / 2)
        multi.add(
            Cube(1/2, repeat(color2)),
            position=center,
        )
    return multi


def CubeCorners(edge, color1, color2):
    multi = MultiShape()
    multi.add(
        Cube(edge, repeat(color1)),
        position=Origin,
    )
    for pos in list(product(*repeat([-1, +1], 3))):
        multi.add(
            Cube(edge/2, repeat(color2)),
            position=Vec3(*pos) * (edge / 2),
        )
    return multi


def Ring(basic_shape, radius, number):
    multi = MultiShape()

    angle = 0
    orientation = Orientation()
    delta_angle = 2 * pi / number
    while angle < 2 * pi:
        angle += delta_angle
        pos = Vec3(
            0,
            radius * sin(angle),
            radius * cos(angle),
        )
        orientation.pitch(delta_angle)
        multi.add(basic_shape, pos, orientation)
    return multi


def CubeRing(edge, radius, number, face_colors):
    return Ring(Cube(edge, face_colors), radius, number)


def TriRing(edge, radius, number, colors):
    multi = MultiShape()
    c1 = CubeRing(edge, radius, number, colors)
    multi.add(c1, orientation=Orientation(XAxis))
    multi.add(c1, orientation=Orientation(YAxis))
    multi.add(c1, orientation=Orientation(ZAxis, XAxis))
    return multi


def CubeFrame(edge, colors):

    timbers = (
        ((edge + 1, 1, 1), (0, +edge/2, +edge/2)),
        ((edge + 1, 1, 1), (0, +edge/2, -edge/2)),
        ((edge + 1, 1, 1), (0, -edge/2, +edge/2)),
        ((edge + 1, 1, 1), (0, -edge/2, -edge/2)),

        ((1, edge + 1, 1), (+edge/2, 0, +edge/2)),
        ((1, edge + 1, 1), (+edge/2, 0, -edge/2)),
        ((1, edge + 1, 1), (-edge/2, 0, +edge/2)),
        ((1, edge + 1, 1), (-edge/2, 0, -edge/2)),

        ((1, 1, edge + 1), (+edge/2, +edge/2, 0)),
        ((1, 1, edge + 1), (+edge/2, -edge/2, 0)),
        ((1, 1, edge + 1), (-edge/2, +edge/2, 0)),
        ((1, 1, edge + 1), (-edge/2, -edge/2, 0)),
    )

    face_colors = list(islice(colors, 0, 6))
    multi = MultiShape()
    for dims, posn in timbers:
        timber = Cuboid(dims[0], dims[1], dims[2], face_colors)
        multi.add(timber, Vec3(*posn))
    return multi


def CubeGlob(radius, number, colors):
    GAP = 20
    multi = MultiShape()
    cube = Cube(1, colors)
    for _ in range(number):
        pos = Vec3.Random(radius - GAP)
        gap = pos.normalized() * GAP
        pos = pos + gap
        multi.add(
            cube,
            position=pos,
            orientation=Orientation.Random() )
    return multi


def CubeCluster(edge, positions):
    multi = MultiShape()
    cube = Cube(1, Color.Random().variations())
    for pos in positions:
        multi.add(cube, pos)
    return multi


def RgbCubeCluster(edge, cluster_edge, cube_count, hole=0):
    cluster = MultiShape()
    for _ in range(cube_count):
        while True:
            pos = Vec3(
                randint(-cluster_edge, +cluster_edge),
                randint(-cluster_edge, +cluster_edge),
                randint(-cluster_edge, +cluster_edge),
            )
            color = Color(
                int((pos.x + cluster_edge) / cluster_edge / 2 * 255),
                int((pos.y + cluster_edge) / cluster_edge / 2 * 255),
                int((pos.z + cluster_edge) / cluster_edge / 2 * 255),
                255
            )
            # make a hole in the center
            if pos.length > hole:
                break
        cluster.add(
            Cube(edge, repeat(color)),
            position=Vec3(*pos)
        )
    return cluster


def CubeLattice(edge, cluster_edge, freq, color):
    shape = MultiShape()
    for i in range(int(-cluster_edge/2), int(+cluster_edge/2+1), freq):
        for j in range(int(-cluster_edge/2), int(+cluster_edge/2+1), freq):
            for pos in [
                Vec3(i, j, -cluster_edge/2),
                Vec3(i, j, +cluster_edge/2),
                Vec3(i, -cluster_edge/2, j),
                Vec3(i, +cluster_edge/2, j),
                Vec3(-cluster_edge/2, i, j),
                Vec3(+cluster_edge/2, i, j),
            ]:
                shape.add(
                    Cube(edge, repeat(color)),
                    position=pos,
                )
    return shape

