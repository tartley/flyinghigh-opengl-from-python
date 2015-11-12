
from .time import Time


class Event(object):

    def __init__(self):
        self.listeners = []

    def __iadd__(self, listener):
        self.listeners.append(listener)
        return self

    def fire(self, *args, **kwargs):
        for listener in self.listeners:
            listener(*args, **kwargs)


class World(object):

    clearColor = (0.1, 0.4, 0.2, 1)

    def __init__(self):
        self.time = Time(self)
        self.items = {}
        self.add_item = Event()
        self.remove_item = Event()
        self.camera = None

    def __iter__(self):
        return iter(self.items.values())

    def add(self, item):
        self.items[item.id] = item
        self.add_item.fire(item)
        if hasattr(item, 'camera'):
            self.camera = item

    def remove(self, item):
        del self.items[item.id]
        self.remove_item.fire(item)

    def update(self, dt):
        self.time.tick(dt)
        for item in self:
            if hasattr(item, 'move') and item.move:
                item.position = item.move(self.time, dt)
            if hasattr(item, 'spin') and item.spin:
                item.orientation = item.spin(self.time, dt)

