from math import cos, sin, pi

from .position import Position


class WobblyOrbit(object):

    def __init__(self):
        self.age = 0.0

    def __call__(self, dt):
        self.age += dt

        bearing = cos(self.age / 5 - pi/2) * 10
        distance = 80 + sin(self.age / 3) * 75
        elevation = sin(self.age) * cos(self.age / 3) * pi / 2

        x1 = distance * sin(bearing)
        z1 = distance * cos(bearing)

        x2 = x1 * cos(elevation)
        z2 = z1 * cos(elevation)
        y2 = distance * sin(elevation)

        return Position(x2, y2, z2)
        
