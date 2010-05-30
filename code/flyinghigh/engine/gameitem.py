
class GameItem(object):

    _next_id = 0

    def __init__(self, *_, **kwargs):
        self.id = GameItem._next_id
        GameItem._next_id += 1

        for name, value in kwargs.iteritems():
            setattr(self, name, value)

    def update(self):
        pass

