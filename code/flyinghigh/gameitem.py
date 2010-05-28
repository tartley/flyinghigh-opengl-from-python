
class GameItem(object):

    def __init__(self, geometry, color):
        self.position = (0, 0)
        self.angle = 0.0
        self.geometry = geometry
        self.color = color
        self.itemid = None
        self.glyph = None

    def update(self):
        pass

