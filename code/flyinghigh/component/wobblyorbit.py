from math import cos, sin, pi

from ..geometry.vec3 import Vec3


class WobblyOrbit(object):

    def __init__(self):
        self.age = 0.0
        self.position = None

    def __call__(self, dt):
        # time moves slower when camera is near the origin
        if (
            self.position and
            abs(self.position.x) < 20 and
            abs(self.position.y) < 20 and
            abs(self.position.z) < 20
        ):
            self.age += dt / 4
        else:
            self.age += dt

        # camera position at distance, bearing
        bearing = cos(self.age / 5 - pi/2) * 10
        distance = 80 + sin(self.age / 3) * 75
        x1 = distance * sin(bearing)
        z1 = distance * cos(bearing)

        # then elevate above the x = z = 0 plane
        elevation = sin(self.age) * cos(self.age / 3) * pi / 2
        x2 = x1 * cos(elevation)
        z2 = z1 * cos(elevation)
        y2 = distance * sin(elevation)

        self.position = Vec3(x2, y2, z2)
        return self.position
        
