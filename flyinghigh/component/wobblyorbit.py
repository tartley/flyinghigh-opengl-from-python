from __future__ import division

from math import cos, sin, pi
from random import uniform

from ..geometry.vec3 import Vec3


class Orbit(object):

    def __init__(self, distance, speed, phase=None):
        self.distance = distance
        self.speed = speed
        if phase is None:
            phase = uniform(0, 2 * pi)
        self.phase = phase

    def __call__(self, time, dt):
        time = time.current
        bearing = time * self.speed + self.phase
        x = self.distance * sin(bearing)
        z = self.distance * cos(bearing)
        return Vec3(x, 0, z)



class WobblyOrbit(object):

    def __init__(self, mean, variance=0.0, speed=1.0):
        self.mean = mean
        self.variance = variance
        self.speed = speed
        self.phase = uniform(0, 2 * pi)

        self.desired_mean = mean
        self.desired_variance = variance

    def __call__(self, time, dt):
        time = time.current

        # move smoothly between transitions
        self.mean += (self.desired_mean - self.mean) * dt * 10
        self.variance = min (
            self.mean - 2,
            self.variance + (self.desired_variance - self.variance) * dt * 10
        )

        # camera position at distance, bearing
        distance = self.mean + sin(time * self.speed) * self.variance
        bearing = sin(time * self.speed / 4 + self.phase + 3 * pi / 4) * 10
        x1 = distance * sin(bearing)
        z1 = distance * cos(bearing)

        # then elevate above/below the y=0 plane
        elevation = sin(time * self.speed + self.phase) * cos(time / 3) * pi / 2
        x2 = x1 * cos(elevation)
        z2 = z1 * cos(elevation)
        y2 = distance * sin(elevation)

        return Vec3(x2, y2, z2)

