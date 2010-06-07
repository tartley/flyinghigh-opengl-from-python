
from math import cos, sin

from ..geometry.orientation import Orientation
from ..geometry.vec3 import XAxis


class Spinner(object):

    def __init__(self, speed):
        self.speed = speed
        self.orientation = Orientation(XAxis)

    def __call__(self, time, dt):
        self.orientation.pitch(sin(time) * dt * self.speed)
        self.orientation.roll(cos(time * 1.5) * dt * self.speed)
        return self.orientation

