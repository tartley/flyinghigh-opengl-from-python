

class SlowMo(object):
    '''
    Defines a region of space, if the position of the given item is within it,
    then time passes more slowly
    '''
    def __init__(self, edge, rate):
        self.edge = edge
        self.rate = rate

    def __call__(self, position):
        if (
            abs(position.x) < self.edge/2 and
            abs(position.y) < self.edge/2 and
            abs(position.z) < self.edge/2
        ):
            return self.rate
        else:
            return 1.0

