
from ..geometry.orientation import Orientation
from ..geometry.vec3 import Vec3

class GameItem(object):

    _next_id = 0

    def __init__(self, **kwargs):
        self.id = GameItem._next_id
        GameItem._next_id += 1

        # store the given components on our attributes
        self.__dict__.update(**kwargs)

        # TODO: this should be in some event handler for world.add_item
        # so that GameItem doesn't need to frig with its attached components
        for name, value in kwargs.items():
            if hasattr(value, 'item'):
                setattr(value, 'item', self)

        # if position is a plain old tuple, convert it to Vec3
        if hasattr(self, 'position') and not isinstance(self.position, Vec3):
            self.position = Vec3(*self.position)
        # if orientation is a plain old tuple, convert it to Orientation
        if (
            hasattr(self, 'orientation') and
            not isinstance(self.orientation, Orientation)
        ):
            self.orientation = Orientation(self.orientation)


    def _attributes(self):
        return ' '.join(
            '%s=%s' % (name, getattr(self, name))
            for name in dir(self)
            if not name.startswith('_')
        )


    def __repr__(self):
        return '<GameItem %x %s>' % (id(self), self._attributes())

