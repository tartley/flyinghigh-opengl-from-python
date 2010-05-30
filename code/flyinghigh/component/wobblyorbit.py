from math import cos, sin

from .position import Position


class WobblyOrbit(object):

    def __init__(self):
        self.item = None
        self.age = 0.0

    def update(self, dt):
        self.age += dt

        bearing = self.age + cos(self.age / 5 + 0.5) * 10
        distance = 20 + cos(self.age) * 10
        elevation = sin(self.age)

        x1 = distance * sin(bearing)
        z1 = distance * cos(bearing)

        x2 = x1 * cos(elevation)
        z2 = z1 * cos(elevation)
        y2 = distance * sin(elevation)

        self.item.position = Position(x2, y2, z2)
        
