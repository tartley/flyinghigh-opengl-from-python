
from collections import namedtuple
from random import randint, uniform


class Color(namedtuple('_ColorBase', 'r g b a')):

    __slots__ = []

    def __repr__(self):
        return 'Color(%d, %d, %d, %d)' %  (self.r, self.g, self.b, self.a)

    @staticmethod
    def Random():
        return Color(
            randint(0, 255),
            randint(0, 255),
            randint(0, 255),
            255)

    def inverted(self):
        return Color(
            255 - self.r,
            255 - self.g,
            255 - self.b,
            255
        )

    def tinted(self, other=None, proportion=0.5):
        if other is None:
            other = white
        return Color(
            int(self.r * (1 - proportion) + other.r * proportion),
            int(self.g * (1 - proportion) + other.g * proportion),
            int(self.b * (1 - proportion) + other.b * proportion),
            int(self.a * (1 - proportion) + other.a * proportion),
        )

    def variations(self, other=None):
        while True:
            yield self.tinted(other, uniform(0, 1))


red = Color(255, 0, 0, 255)
orange = Color(255, 127, 0, 255)
yellow = Color(255, 255, 0, 255)
green = Color(0, 255, 0, 255)
cyan = Color(0, 255, 255, 255)
blue = Color(0, 0, 255, 255)
purple = Color(255, 0, 255, 255)
white = Color(255, 255, 255, 255)
grey = Color(128, 128, 128, 255)
black = Color(0, 0, 0, 255)

all_colors = [
    red, orange, yellow, green, cyan, blue, purple, white, grey, black]

