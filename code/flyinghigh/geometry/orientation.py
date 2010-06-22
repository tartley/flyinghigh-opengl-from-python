
from math import pi, degrees

from OpenGL import GL as gl

from .vec3 import NegYAxis, NegZAxis, Vec3, YAxis, ZAxis


EPSILON = 1e-15
matrix_type = gl.GLfloat * 16

class Orientation(object):
    '''
    Maintains a forward and up vector (and a derived 'right' vector, orthogonal
    to these) which define an orientation.
    When an Orientation is used to rotate a point, the null orientation, which
    results in zero rotation, is with forward pointing along the negative Z
    axis, up along the positive Y axis, and hence right along thepositive X
    axis.
    '''
    def __init__(self, forward=None, up=None):
        '''
        'forward' and 'up' should be Vec3 or 3-part tuple.
        If 'up' is omitted, a sensible default up vector is chosen.
        '''
        if forward is None:
            forward = NegZAxis
        elif not isinstance(forward, Vec3):
            forward = Vec3(*forward)
        self.forward = forward.normalize()

        if up is None:
            up = self._default_up()
        elif not isinstance(up, Vec3):
            up = Vec3(*up)
            angle_between = forward.angle(up)
            assert abs(angle_between - pi/2) < EPSILON, \
                "up (%s) must be 90deg to forward (%s), actually %f deg" % \
                (up, forward, degrees(angle_between))
        self.up = up.normalize()

        self.right = self._get_right()

        self._matrix = None


    def _default_up(self):
        '''
        returns a sensible default up vector (ie. orthogonal to forward,
        but pointed as near to the YAxis as possible)
        '''
        # special case for forward is y-axis or negative y-axis
        if self.forward == YAxis:
            return ZAxis
        elif self.forward == NegYAxis:
            return NegZAxis

        # project 'forward' onto y=0 plane
        flat = Vec3(self.forward.x, 0, self.forward.z)
        # find vector in the y=0 plane at right angles to 'flat'
        axis = flat.cross(YAxis)
        # rotate 'forward' by 90 deg about 'axis'
        up = self.forward.rotate(axis, -pi/2)
        return up.normalize()


    def _get_right(self):
        '''
        value of self.right is always derived from self.forward and self.up
        '''
        return self.forward.cross(self.up)


    def __repr__(self):
        return 'Orientation(%s, up=%s)' % (self.forward, self.up)

    def __eq__(self, other):
        return (
            isinstance(other, Orientation) and
            self.forward == other.forward and
            self.up == other.up)

    def __ne__(self, other):
        return not self.__eq__(other)

    __hash__ = None # Orientations are mutable, so do not allow hashing


    def roll(self, angle):
        '''
        rotate about the 'backward' axis (ie. +ve angle rolls to the right)
        '''
        self.up = self.up.rotate(self.forward, -angle).normalize()
        self.right = self._get_right()


    def yaw(self, angle):
        '''
        rotate about the 'up' axis (ie. +ve angle yaws to the right)
        '''
        self.forward = self.forward.rotate(self.up, angle).normalize()
        self.right = self._get_right()


    def pitch(self, angle):
        '''
        rotate about the 'left' axis (ie. +ve angle pitches up)
        '''
        self.forward = self.forward.rotate(self.right, -angle).normalize()
        self.up = self.up.rotate(self.right, -angle).normalize()


    @property
    def matrix(self):
        '''
        The matrix that the OpenGL modelview matrix should be multiplied by
        to represent this orientation. If a Vec3 offset is supplied, then
        the returned matrix also incorporates that translation offset.
        '''
        if self._matrix is None:
            self._matrix = matrix_type(
                self.right.x,    self.right.y,    self.right.z,   0,
                self.up.x,       self.up.y,       self.up.z,      0,
               -self.forward.x, -self.forward.y, -self.forward.z, 0,
                0,               0,               0,              1,
            )
        return self._matrix

