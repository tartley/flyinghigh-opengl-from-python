
class Time(object):

    def __init__(self, world):
        self.world = world
        self.current = 0.0
        self.dt = None

    def tick(self, dt):
        self.dt = dt * self.get_rate()
        self.current += self.dt

    def get_rate(self):
        '''
        ask all the items in the world with a 'slowmo' attribute whether time
        should be running slow right now
        '''
        rate = 1.0
        for item in self.world:
            if hasattr(item, 'slowmo'):
                rate = min(rate, item.slowmo())
        return rate

