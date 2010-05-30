
class GameItem(object):

    _next_id = 0

    def __init__(self, *_, **kwargs):
        self.id = GameItem._next_id
        GameItem._next_id += 1

        # store the components of this gameitem on our attributes
        for name, value in kwargs.iteritems():
            self.attach(name, value)


    def attach(self, name, component):
        '''
        attach a new component to this game item
        '''
        if hasattr(component, 'item'):
            setattr(component, 'item', self)
        
        setattr(self, name, component)


    def detach(self, name):
        delattr(self, name)

