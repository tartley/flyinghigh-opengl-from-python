from __future__ import division

from itertools import chain
from math import cos, pi, sin

from .position import Position


class Shape(object):

    def __init__(self, vertices, faces):
        self.vertices = [Position(*v) for v in vertices]
        self.faces = faces


class CompositeShape(object):

    def __init__(self):
        self.children = set()

    def add(self, child, offset=None):
        if offset is None:
            offset = Position(0, 0, 0)
        self.children.add((child, offset))

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


def Rectangle(width, height):
    vertices = [
        (-width/2, -height/2),
        (+width/2, -height/2),
        (+width/2, +height/2),
        (-width/2, +height/2),
    ]
    faces = [[0, 1, 2, 3]]
    return Shape(vertices, faces)


def Circle(radius):
    NUM_POINTS = 32
    verts = []
    for n in xrange(0, NUM_POINTS):
        a = n * 2 * pi / NUM_POINTS
        verts.append( (radius * cos(a), radius * sin(a)) )
    faces = [[n for n in xrange(0, NUM_POINTS)]]
    return Shape(verts, faces)


def Cube(edge):
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
    return Shape(verts, faces)

