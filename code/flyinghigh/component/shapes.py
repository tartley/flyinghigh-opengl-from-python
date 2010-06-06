from __future__ import division

from itertools import chain
from math import cos, pi, sin
from random import randint

from ..geometry.vec3 import Vec3


class Shape(object):

    def __init__(self, vertices, faces, color):
        self.vertices = [Vec3(*v) for v in vertices]
        self.faces = faces
        self.color = color

    @property
    def colors(self):
        return [self.color for _ in xrange(len(self.vertices))]

class CompositeShape(object):

    def __init__(self):
        self.children = []
        self._vertices = None
        self._colors = None
        self._faces = None

    def add(self, child, offset=None):
        if offset is None:
            offset = Vec3(0, 0, 0)
        self.children.append((child, offset))

    @property
    def vertices(self):
        if self._vertices is None:
            self._vertices = [
                vert + offset
                for shape, offset in self.children
                for vert in shape.vertices]
        return self._vertices

    @property
    def faces(self):
        if self._faces is None:
            newfaces = []
            index_offset = 0
            for shape, _ in self.children:
                for face in shape.faces:
                    newface = []
                    for index in face:
                        newface.append(index + index_offset)
                    newfaces.append(newface)
                index_offset += len(shape.vertices)
            self._faces = newfaces
        return self._faces

    @property
    def colors(self):
        if self._colors is None:
            self._colors = list(
                chain.from_iterable(shape.colors for shape, _ in self.children))
        return self._colors


def Rectangle(width, height, color):
    vertices = [
        (-width/2, -height/2),
        (+width/2, -height/2),
        (+width/2, +height/2),
        (-width/2, +height/2),
    ]
    face = [0, 1, 2, 3]
    return Shape(vertices, [face], color)


def Circle(radius, color):
    NUM_POINTS = 32
    verts = []
    for n in xrange(0, NUM_POINTS):
        a = n * 2 * pi / NUM_POINTS
        verts.append( (radius * cos(a), radius * sin(a)) )
    face = [n for n in xrange(0, NUM_POINTS)]
    return Shape(verts, [face], color)


def Cube(edge, color):
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
    return Shape(verts, faces, color)


def RgbCubeCluster(edge, cluster_edge, cube_count):
    shape = CompositeShape()
    for i in xrange(cube_count):
        r = randint(1, cluster_edge-1)
        g = randint(1, cluster_edge-1)
        b = randint(1, cluster_edge-1)
        color = (r / cluster_edge, g / cluster_edge, b / cluster_edge, 1)
        pos = [
            r - cluster_edge / 2,
            g - cluster_edge / 2,
            b - cluster_edge / 2,
        ]
        shape.add(Cube(edge, color), Vec3(*pos))
    return shape


def CubeLattice(edge, cluster_edge, freq):
    shape = CompositeShape()
    black = (0, 0, 0, 1)
    for i in xrange(int(-cluster_edge/2), int(+cluster_edge/2+1), freq):
        for j in xrange(int(-cluster_edge/2), int(+cluster_edge/2+1), freq):
            shape.add(Cube(edge, black), Vec3(i, j, -cluster_edge/2))
            shape.add(Cube(edge, black), Vec3(i, j, +cluster_edge/2))
            shape.add(Cube(edge, black), Vec3(i, -cluster_edge/2, j))
            shape.add(Cube(edge, black), Vec3(i, +cluster_edge/2, j))
            shape.add(Cube(edge, black), Vec3(-cluster_edge/2, i, j))
            shape.add(Cube(edge, black), Vec3(+cluster_edge/2, i, j))
    return shape


def CubeCross():
    shape = CompositeShape()
    shape.add(Cube(2, (0.55, 0.55, 0.55, 1)), Vec3(0, 0, 0))
    shape.add(Cube(1, (0.6, 0.6, 0.6, 1)), Vec3(1, 0, 0))
    shape.add(Cube(1, (0.6, 0.6, 0.6, 1)), Vec3(0, 1, 0))
    shape.add(Cube(1, (0.6, 0.6, 0.6, 1)), Vec3(0, 0, 1))
    shape.add(Cube(1, (0.6, 0.6, 0.6, 1)), Vec3(-1, 0, 0))
    shape.add(Cube(1, (0.6, 0.6, 0.6, 1)), Vec3(0, -1, 0))
    shape.add(Cube(1, (0.6, 0.6, 0.6, 1)), Vec3(0, 0, -1))
    return shape

