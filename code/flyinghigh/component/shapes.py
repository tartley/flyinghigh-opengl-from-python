
from __future__ import division

from itertools import repeat
from math import cos, pi, sin, sqrt
from random import randint

from ..engine.shape import Shape, MultiShape
from ..geometry.vec3 import (
    NegXAxis, NegYAxis, NegZAxis, Origin, Vec3, XAxis, YAxis, ZAxis,
)



def Cube(edge, face_colors=None):
    e2 = edge/2
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
    
