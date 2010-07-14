
from math import cos, sin

from ..math.orientation import Orientation
from ..math.vec3 import XAxis


class Spinner(object):

    def __init__(self, speed):
        self.speed = speed
        self.orientation = Orientation(XAxis)

    def __call__(self, time):
        self.orientation.pitch(sin(time.current) * time.dt * self.speed)
        self.orientation.roll(cos(time.current * 1.5) * time.dt * self.speed)
        return self.orientation

