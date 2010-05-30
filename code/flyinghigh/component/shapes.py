from __future__ import division

from math import cos, pi, sin


class Shape(object):

    def __init__(self, vertices, indices):
        self.vertices = vertices
        self.indices = indices


def Rectangle(width, height):
    vertices = [
        (-width/2, -height/2),
        (+width/2, -height/2),
        (+width/2, +height/2),
        (-width/2, +height/2),
    ]
    indices = [(0, 1, 2), (2, 3, 0)]
    return Shape(vertices, indices)


def Circle(radius):
    NUM_POINTS = 32
    verts = []
    for n in xrange(0, NUM_POINTS):
        a = n * 2 * pi / NUM_POINTS
        verts.append( (radius * cos(a), radius * sin(a)) )
    indices = [
        (0, n, n+1)
        for n in xrange(1, NUM_POINTS-1)
    ]
    return Shape(verts, indices)


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
    indices = [
        (0, 1, 2), (2, 1, 3), # left
        (4, 6, 5), (6, 7, 5), # right
        (7, 3, 1), (1, 5, 7), # front
        (0, 2, 6), (6, 4, 0), # back
        (3, 7, 6), (6, 2, 3), # top
        (1, 0, 4), (4, 5, 1), # bottom
    ]
    return Shape(verts, indices)

