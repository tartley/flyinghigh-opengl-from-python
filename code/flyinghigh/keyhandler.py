

class KeyHandler(object):

    def __init__(self, world, bestiary):
        self.world = world
        self.bestiary = bestiary

    def on_key_press(self, symbol, modifers):
        print symbol, type(symbol)

