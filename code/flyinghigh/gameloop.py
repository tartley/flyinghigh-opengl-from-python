
import pyglet
from pyglet.event import EVENT_HANDLED

from .camera import Camera
from .render import Render
from .world import World


class Gameloop(object):

    def __init__(self):
        self.world = None
        self.window = None
        self.camera = None


    def launch(self):
        self.world = World()
        # self.world.init()
        self.camera = Camera()
        self.render = Render()
        self.render.init()

        self.window = pyglet.window.Window(fullscreen=False, visible=False)
        self.window.set_exclusive_mouse(True)
        self.window.on_draw = self.draw
        self.window.on_resize = self.render.resize

        pyglet.clock.schedule(self.update)
        self.clockdisplay = pyglet.clock.ClockDisplay()

        self.window.set_visible()
        pyglet.app.run()


    def update(self, dt):
        # scale dt such that the 'standard' framerate of 60fps gives dt=1.0
        dt *= 60
        # prevent explosion when game is paused then restarted ffor any reason
        dt = min(dt, 2)
        self.world.update()
        self.window.invalid = True


    def draw(self):
        self.window.clear()
        self.camera.world_projection(self.window.width, self.window.height)
        self.camera.look_at()
        self.render.draw(self.world)
        self.clockdisplay.draw()
        return EVENT_HANDLED


    def shutdown(self):
        if self.window:
            self.window.close()        

