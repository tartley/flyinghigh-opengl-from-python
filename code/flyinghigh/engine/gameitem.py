
from ..geometry.orientation import Orientation

class GameItem(object):

    _next_id = 0

    def __init__(self, **kwargs):
        self.id = GameItem._next_id
        GameItem._next_id += 1

        # store the given components on our attributes
        self.__dict__.update(**kwargs)

        # TODO: this should be in some event handler for world.add_item
        # so that GameItem doesn't need to frig with its attached components
        for name, value in kwargs.iteritems():
            if hasattr(value, 'item'):
                setattr(value, 'item', self)

        # TODO: this should be in some event handler for world.add_item
        # so that GameItem doesn't need to frig with its attached components
        if hasattr(self, 'orientation') and isinstance(self.orientation, tuple):
            self.orientation = Orientation(self.orientation)


    def _attributes(self):
        return ' '.join('%s' % (name,) for name in dir(self))


    def __repr__(self):
        return '<GameItem %x %s>' % (id(self), self._attributes())

