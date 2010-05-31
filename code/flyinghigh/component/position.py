
from collections import Iterable, namedtuple


class Position(namedtuple('Position', 'x y z')):

    __slots__ = ()

    def __add__(self, other):
        assert isinstance(other, Iterable)
        assert len(other) == 3
        return Position(
            self.x + other[0],
            self.y + other[1],
            self.z + other[2],
        )

    def __repr__(self):
        return 'Position(%d, %d, %d)' % (self.x, self.y, self.z)

