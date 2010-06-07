

class SlowMo(object):
    '''
    Defines a region of space, if the position of the given item is within it,
    then time passes more slowly
    '''
    def __init__(self, edge, rate):
        self.edge = edge
        self.rate = rate
        self.spread = 10

    def __call__(self, position):
        '''
        return 1.0 for positions well outside the cube shaped region of size
        'edge'. Return self.rate for positions well inside it. Linearly
        interpolate between the two at the boundary.
        '''
        dist = max(abs(position.x), abs(position.y), abs(position.z))
        offset = dist - self.edge / 2 + self.spread / 2
        retval = offset * (1.0 - self.rate) / self.spread
        return min(1.0, max(self.rate, retval))

