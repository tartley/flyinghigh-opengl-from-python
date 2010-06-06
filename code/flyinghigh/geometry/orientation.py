
from math import pi, degrees

from .vec3 import Vec3, YAxis

EPSILON = 1e-15

class Orientation(object):
    '''
    Maintains a forward and up vector (and a derived 'right' vector orthogonal
    to these) which define an orientation.
    '''
    def __init__(self, forward, up=None):
        if type(forward) is tuple:
            forward = Vec3(*forward)
        self.forward = forward.normalize()

        if up is None:
            up = self._default_up()
        elif type(up) is tuple:
            up = Vec3(*up)
        self.up = up.normalize()

        angle_between = forward.angle(up)
        assert abs(angle_between - pi/2) < EPSILON, \
            "up (%s) must be orthogonal to forward (%s), actually %f deg" % \
            (up, forward, degrees(angle_between))

        self.right = self._get_right()


    def _default_up(self):
        '''
        returns a sensible default up vector
        '''
        # special case for forward is y-axis or negative y-axis
        angle = self.forward.angle(YAxis)
        if angle < EPSILON:
            return Vec3(0, 0, -1)
        elif angle > pi - EPSILON:
            return Vec3(0, 0, 1)

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
        return self.up.cross(self.forward)


    def __repr__(self):
        return 'Orientation(%s, up=%s)' % (self.forward, self.up)


    def __eq__(self, other):
        return (
            self.forward == other.forward and
            self.up == other.up)


    def __ne__(self, other):
        return (self.forward != other.forward or
                self.up != other.up)


    # Orientations are mutable, so do not allow hashing
    __hash__ = None


    def roll(self, angle):
        '''
        rotate about the 'forward' axis
        '''
        self.up = self.up.rotate(self.forward, angle)
        self.right = self._get_right()


    def yaw(self, angle):
        '''
        rotate about the *down* axis (so that +ve angle yaws to the right)
        '''
        self.forward = self.forward.rotate(self.up, -angle)
        self.right = self._get_right()


    def pitch(self, angle):
        '''
        rotate about the 'right' axis
        '''
        self.forward = self.forward.rotate(self.right, angle)
        self.up = self.up.rotate(self.right, angle)


    def get_matrix(self):
        return 

