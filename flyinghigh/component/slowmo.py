
RATE = 0.1

class SlowMo(object):
    '''
    If condition is False, __call__ returns 1.0, otherwise it returns
    'slowdown'. Transition smoothly from one value to the other,
    '''
    def __init__(self, condition, slowdown):
        self.condition = condition
        self.slowdown = slowdown
        self.current = slowdown if condition() else 1.0

    def __call__(self):
        if self.condition():
            desired = self.slowdown
        else:
            desired = 1.0
        self.current += (desired - self.current) * RATE
        return self.current

