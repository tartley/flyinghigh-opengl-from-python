
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

    clearColor = (0.3, 0.3, 0.3, 1)

    def __init__(self):
        self.time = Time(self)
        self.items = {}
        self.add_item = Event()


    def add(self, item):
        self.items[item.id] = item
        self.add_item.fire(item)


    def update(self, dt):
        self.time.tick(dt)
        for item in self.items.itervalues():
            if hasattr(item, 'move'):
                item.position = item.move(self.time)
            if hasattr(item, 'spin'):
                item.orientation = item.spin(self.time)

