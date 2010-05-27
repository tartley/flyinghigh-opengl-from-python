

class World(object):

    _next_id = 0    

    def __init__(self):
        self.ents = {}

    def add(self, entity):
        entity.itemid = World._next_id
        self.ents[World._next_id] = entity
        World._next_id += 1

    def update(self):
        pass

