from math import cos, sin, pi
from random import uniform

from ..geometry.vec3 import Vec3, YAxis


class WobblyOrbit(object):

    def __init__(self, mean, variance=0.0, speed=1.0):
        self.mean = mean
        self.variance = variance
        self.speed = speed
        self.phase = uniform(0, 2 * pi)

    def __call__(self, time, dt):
        # camera position at distance, bearing
        distance = self.mean + sin(time * self.speed) * self.variance
        bearing = sin(time * self.speed / 4.0 + self.phase + 3 * pi / 4.0) * 10
        x1 = distance * sin(bearing)
        z1 = distance * cos(bearing)

        # then elevate above/below the y=0 plane
        elevation = sin(time * self.speed + self.phase) * cos(time / 3) * pi / 2
        x2 = x1 * cos(elevation)
        z2 = z1 * cos(elevation)
        y2 = distance * sin(elevation)

        return Vec3(x2, y2, z2)

