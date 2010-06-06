
from collections import namedtuple
from math import acos, cos, sin, sqrt


EPSILON = 1e-7


class Vec3(namedtuple('Vec3Base', 'x y z')):

    __slots__ = []

    def __repr__(self):
        return 'Vec3(%s, %s, %s)' % (self.x, self.y, self.z)

    def __eq__(self, other):
        return (
            abs(self[0] - other[0]) < EPSILON and
            abs(self[1] - other[1]) < EPSILON and
            abs(self[2] - other[2]) < EPSILON
        )

    # __hash__ is inherited from tuple, and depends on all of x, y, z

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
        '''
        the length
        '''
        return sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    @property
    def length2(self):
        '''
        the length squared
        '''
        return self.x ** 2 + self.y ** 2 + self.z ** 2

    def normalize(self):
        '''
        return a new vector in the same direction, but of length 1
        '''
        length = self.length
        return Vec3(self.x / length, self.y / length, self.z / length)

    def cross(self, other):
        '''
        return a new vector, the cross product
        a x b = (a2b3 - a3b2, a3b1 - a1b3, a1b2 - a2b1)
        http://en.wikipedia.org/wiki/Cross_product
        '''
        return Vec3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x)

    def dot(self, other):
        '''
        return the scalar dot product
        '''
        return self[0] * other[0] + self[1] * other[1] + self[2] * other[2]

    def angle(self, other):
        '''
        return the angle between this vector and the given one
        '''
        return acos(self.dot(other) / (self.length * other.length))

    def rotateX(self, angle):
        '''
        return a new vector, rotated about the X axis
        '''
        sina = sin(angle)
        cosa = cos(angle)
        return Vec3(
            self.x,
            self.y * cosa + self.z * sina,
            -self.y * sina + self.z * cosa)

    def rotateY(self, angle):
        '''
        return a new vector, rotated about the Y axis
        '''
        sina = sin(angle)
        cosa = cos(angle)
        return Vec3(
            self.x * cosa - self.z * sina,
            self.y,
            self.x * sina + self.z * cosa)

    def rotateZ(self, angle):
        '''
        return a new vector, rotated about the Z axis
        '''
        sina = sin(angle)
        cosa = cos(angle)
        return Vec3(
            self.x * cosa + self.y * sina,
            -self.x * sina + self.y * cosa,
            self.z
        )

    def rotate(self, axis, angle):
        '''
        return a new vector, rotated about the given axis
        '''
        c = cos(-angle)
        t = 1 - c
        s = sin(-angle)

        # Matrix 'M' rotates about axis
        d11 = t * axis.x ** 2 + c
        d12 = t * axis.x * axis.y - s * axis.z 
        d13 = t * axis.x * axis.z + s * axis.y
        d21 = t * axis.x * axis.y + s * axis.z 
        d22 = t * axis.y ** 2 + c
        d23 = t * axis.y * axis.z - s * axis.x 
        d31 = t * axis.x * axis.z - s * axis.y
        d32 = t * axis.y * axis.z + s * axis.x 
        d33 = t * axis.z ** 2 + c

        # multiply M * self
        return Vec3(
            d11 * self.x + d12 * self.y + d13 * self.z,
            d21 * self.x + d22 * self.y + d23 * self.z,
            d31 * self.x + d32 * self.y + d33 * self.z,
        )


Origin = Vec3(0, 0, 0)
XAxis = Vec3(1, 0, 0)
YAxis = Vec3(0, 1, 0)
ZAxis = Vec3(0, 0, 1)

