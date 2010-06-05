
from collections import namedtuple
from math import sqrt


class Vec3(namedtuple('Vec3Base', 'x y z')):

    __slots__ = []

    def __repr__(self):
        return 'Vec3(%s, %s, %s)' % (self.x, self.y, self.z)

    def __add__(self, other):
        ox, oy, oz = other
        return Vec3(
            self.x + ox,
            self.y + oy,
            self.z + oz,
        )

    def __neg__(self):
        return Vec3(-self.x, -self.y, -self.z)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        return Vec3(
            self.x - other[0],
            self.y - other[1],
            self.z - other[2],
        )

    def __rsub__(self, other):
        return Vec3(*other).__sub__(self)

    @property
    def length(self):
        return sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    @property
    def length2(self):
        '''
        length squared
        '''
        return self.x * self.x + self.y * self.y + self.z * self.z

    def cross(self, other):
        '''
        http://en.wikipedia.org/wiki/Cross_product
        a x b = (a2b3 - a3b2, a3b1 - a1b3, a1b2 - a2b1)
        '''
        return Vec3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x)

