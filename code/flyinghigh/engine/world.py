
class World(object):

    clearColor = (0.3, 0.7, 0.4, 1)

    def __init__(self):
        self.items = {}

    def add(self, item):
        self.items[item.id] = item

    def update(self, dt):
        for item in self.items.itervalues():
            if hasattr(item, 'mover'):
                item.mover.update(dt)

