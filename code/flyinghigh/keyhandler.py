

class KeyHandler(object):

    def __init__(self, world, bestiary):
        self.world = world
        self.bestiary = bestiary

    def on_key_press(self, symbol, modifers):
        if symbol in self.bestiary:
            item = self.bestiary[symbol]
            if item in self.world:
                self.world.remove( self.bestiary[symbol] )
            else:
                self.world.add( self.bestiary[symbol] )

