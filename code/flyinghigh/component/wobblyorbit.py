from math import cos, sin, pi

from ..geometry.vec3 import Vec3


class WobblyOrbit(object):

    def __init__(self, mean, variance):
        self.mean = mean
        self.variance = variance

    def __call__(self, time, dt):
        # camera position at distance, bearing
        bearing = cos(time / 5 - pi/2) * 10
        distance = self.mean + sin(time / 1) * self.variance
        x1 = distance * sin(bearing)
        z1 = distance * cos(bearing)

        # then elevate above the y=0 plane
        elevation = sin(time) * cos(time / 3) * pi / 2
        x2 = x1 * cos(elevation)
        z2 = z1 * cos(elevation)
        y2 = distance * sin(elevation)

        return Vec3(x2, y2, z2)
        
