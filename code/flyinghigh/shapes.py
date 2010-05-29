from __future__ import division

from math import cos, pi, sin


class Rect(object):

    dimension = 3

    def __init__(self, width, height):
        self.width = width
        self.height = height

    @property
    def verts(self):
        return [
            (-self.width/2, -self.height/2, 0),
            (+self.width/2, -self.height/2, 0),
            (+self.width/2, +self.height/2, 0),
            (-self.width/2, +self.height/2, 0),
        ]
        
    @property
    def indices(self):
        return [(0, 2, 1), (2, 0, 3)]


class Circle(object):

    dimension = 2
    _NUM_POINTS = 16

    def __init__(self, radius):
        self.radius = radius

    @property
    def verts(self):
        verts = []
        for n in xrange(0, self._NUM_POINTS):
            a = n * 2 * pi / self._NUM_POINTS
            verts.append( (self.radius * cos(a), self.radius * sin(a)) )
        return verts

    @property
    def indices(self):
        return [
            (0, n, n+1)
            for n in xrange(1, self._NUM_POINTS-1)
        ]

