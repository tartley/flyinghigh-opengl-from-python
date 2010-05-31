from __future__ import division

from itertools import chain
from math import cos, pi, sin
from random import randint, uniform

from .position import Position


class Shape(object):

    def __init__(self, vertices, faces, color):
        self.vertices = [Position(*v) for v in vertices]
        self.faces = faces
        self.color = color


class CompositeShape(object):

    def __init__(self):
        self.children = []

    def add(self, child, offset=None):
        if offset is None:
            offset = Position(0, 0, 0)
        self.children.append((child, offset))

    @property
    def vertices(self):
        newverts = []
        for shape, offset in self.children:
            for vert in shape.vertices:
                newverts.append(
                    Position(
                        vert.x + offset.x,
                        vert.y + offset.y,
                        vert.z + offset.z,
                    )
                )
        return newverts
        #return chain(
        #    add_offset(child.vertices, offset) for child, offset in self.children)

    @property
    def faces(self):
        newfaces = []
        index_offset = 0
        for shape, _ in self.children:
            for face in shape.faces:
                newface = []
                for index in face:
                    newface.append(index + index_offset)
                newfaces.append(newface)
            index_offset += len(shape.vertices)
        return newfaces
        # return chain.from_iterable(shape.faces for shape, _ in self.children)

    @property
    def colors(self):
        for shape, _ in self.children:
            for vertex in shape.vertices:
                yield shape.color


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
    verts = [
        (-edge/2, -edge/2, -edge/2),
        (-edge/2, -edge/2, +edge/2),
        (-edge/2, +edge/2, -edge/2),
        (-edge/2, +edge/2, +edge/2),
        (+edge/2, -edge/2, -edge/2),
        (+edge/2, -edge/2, +edge/2),
        (+edge/2, +edge/2, -edge/2),
        (+edge/2, +edge/2, +edge/2),
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


def CubeCluster(edge, cluster_edge, cube_count):
    shape = CompositeShape()
    for i in xrange(cube_count):
        r = randint(0, cluster_edge)
        g = randint(0, cluster_edge)
        b = randint(0, cluster_edge)
        pos = [
            r - cluster_edge / 2,
            g - cluster_edge / 2,
            b - cluster_edge / 2,
        ]

        color = (r / cluster_edge, g / cluster_edge, b / cluster_edge, 1)
        if any(x in [0, cluster_edge] for x in [r, g, b]):
            color = (0, 0, 0, 0)

        shape.add(Cube(edge, color), Position(*pos))
        # TODO: shouldn't need to construct a new Cube every time, geom is same
    return shape

