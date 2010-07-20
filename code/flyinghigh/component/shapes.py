
from __future__ import division

from itertools import chain, repeat
from math import sqrt
from random import randint

from ..engine.shape import Shape, MultiShape
from ..geometry.vec3 import (
    NegXAxis, NegYAxis, NegZAxis, Origin, Vec3, XAxis, YAxis, ZAxis,
)


def TriangleSquare():
    RED = (255, 0, 0, 255)
    YELLOW = (255, 255, 0, 255)
    return Shape(
        vertices=[
            ( 1, -1,  1), # v0
            ( 1, -1, -1), # v1
            (-1, -1, -1), # v2
            (-1, -1,  1), # v3
            ( 1,  1,  0), # v4
        ],
        faces=[ [0, 4, 1], [0, 1, 2, 3], ],
        face_colors=[RED, YELLOW],
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


def Cube(edge, face_colors=None):
    e2 = edge / 2
    verts = [
        (-e2, -e2, -e2),
        (-e2, -e2, +e2),
        (-e2, +e2, -e2),
        (-e2, +e2, +e2),
        (+e2, -e2, -e2),
        (+e2, -e2, +e2),
        (+e2, +e2, -e2),
        (+e2, +e2, +e2),
    ]
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
    face_colors = None
    return Shape(verts, faces, face_colors)



# def SpaceStation(edge):
    # face_colors = chain(
        # repeat(lightGrey, 6),
        # repeat(grey, 8),
        # [black])
    # shape = TruncatedCube(edge, truncation=0.9)
        # (+e2, +e2 * DOORH, +e2 * DOORW),
        # (+e2, 0, 0),
        # (+e2, 0, 0),
        # (+e2, 0, 0),
    # return shape

def RgbCubeCluster(edge, cluster_edge, cube_count):
    shape = MultiShape()
    for i in xrange(cube_count):
        while True:
            r = randint(1, cluster_edge-1)
            g = randint(1, cluster_edge-1)
            b = randint(1, cluster_edge-1)
            color = (
                int(r / cluster_edge * 255),
                int(g / cluster_edge * 255),
                int(b / cluster_edge * 255),
                255)
            pos = Vec3(
                r - cluster_edge / 2,
                g - cluster_edge / 2,
                b - cluster_edge / 2,
            )
            if pos.length > 8:
                break
        shape.add(
            Cube(edge, repeat(color)),
            position=Vec3(*pos)
        )
    return shape


def CubeLattice(edge, cluster_edge, freq, color):
    shape = MultiShape()
    for i in xrange(int(-cluster_edge/2), int(+cluster_edge/2+1), freq):
        for j in xrange(int(-cluster_edge/2), int(+cluster_edge/2+1), freq):
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


def CubeCross():
    multi = MultiShape()

    center_color = (150, 150, 150, 255)
    multi.add(Cube(2, face_colors=repeat(center_color)))

    outer_color = (170, 170, 170, 255)
    for pos in [XAxis, YAxis, ZAxis, NegXAxis, NegYAxis, NegZAxis]:
        multi.add(
            Cube(1, repeat(outer_color)),
            position=pos,
        )
    return multi


def CubeCorners():
    multi = MultiShape()
    center_color = (150, 150, 150, 255)
    multi.add(
        Cube(2, repeat(center_color)),
        position=Origin,
    )
    outer_color = (170, 170, 170, 255)

    for pos in [
        (+1, +1, +1),
        (+1, +1, -1),
        (+1, -1, +1),
        (+1, -1, -1),
        (-1, +1, +1),
        (-1, +1, -1),
        (-1, -1, +1),
        (-1, -1, -1),
    ]:
        multi.add(
            Cube(1, repeat(outer_color)),
            position=pos,
        )
    return multi
    
