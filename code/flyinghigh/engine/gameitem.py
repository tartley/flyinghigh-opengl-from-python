
from ..component.position import Position


class GameItem(object):

    _next_id = 0

    def __init__(self, geometry, color):
        self.id = GameItem._next_id
        GameItem._next_id += 1

        self.position = Position(0, 0, 0)
        self.angle = 0.0
        self.geometry = geometry
        self.color = color
        self.glyph = None


    def update(self):
        pass

