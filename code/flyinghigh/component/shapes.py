from __future__ import division

from math import cos, pi, sin


class Rect(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height

    @property
    def verts(self):
        return [
            (-self.width/2, -self.height/2),
            (+self.width/2, -self.height/2),
            (+self.width/2, +self.height/2),
            (-self.width/2, +self.height/2),
        ]
        
    @property
    def indices(self):
        return [(0, 1, 2), (2, 3, 0)]



class Cube(object):

    def __init__(self, edge):
        self.edge = edge

    @property
    def verts(self):
        return [
            (-self.edge/2, -self.edge/2, -self.edge/2),
            (-self.edge/2, -self.edge/2, +self.edge/2),
            (-self.edge/2, +self.edge/2, -self.edge/2),
            (-self.edge/2, +self.edge/2, +self.edge/2),
            (+self.edge/2, -self.edge/2, -self.edge/2),
            (+self.edge/2, -self.edge/2, +self.edge/2),
            (+self.edge/2, +self.edge/2, -self.edge/2),
            (+self.edge/2, +self.edge/2, +self.edge/2),
        ]

    @property
    def indices(self):
        return [
            (0, 1, 2), (2, 1, 3), # left
            (4, 6, 5), (6, 7, 5), # right
            (7, 3, 1), (1, 5, 7), # front
            (0, 2, 6), (6, 4, 0), # back
            (3, 7, 6), (6, 2, 3), # top
            (1, 0, 4), (4, 5, 1), # bottom
        ]


class Circle(object):

    _NUM_POINTS = 32

    def __init__(self, radius):
        self.radius = radius

    @property
    def verts(self):
        verts = []
        for n in xrange(0, self._NUM_POINTS):
            a = n * 2 * pi / self._NUM_POINTS
            verts.append(
                (self.radius * cos(a),
                self.radius * sin(a))
            )
        return verts

    @property
    def indices(self):
        return [
            (0, n, n+1)
            for n in xrange(1, self._NUM_POINTS-1)
        ]

