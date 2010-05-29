
from math import sin

import pyglet
from pyglet.event import EVENT_HANDLED
from pyglet.window import Window

from .camera import Camera
from .projection import Projection
from .render import Render
from .world import World, populate

class Gameloop(object):

    def __init__(self):
        self.camera = None
        self.projection = None
        self.render = None
        self.time = 0.0
        self.window = None
        self.world = None


    def start(self):
        self.world = World()
        self.world.init()
        populate(self.world)

        self.render = Render()
        self.camera = Camera(position=(0, 0, 0), zoom=15.0)

        self.window = Window(fullscreen=False, visible=False, resizable=True)
        # self.window.set_exclusive_mouse(True)
        self.window.on_draw = self.draw

        self.projection = Projection(self.window.width, self.window.height)
        self.window.on_resize = self.projection.resize
        self.render.init()
        pyglet.clock.schedule(self.update)
        self.clock_display = pyglet.clock.ClockDisplay()

        self.window.set_visible()
        pyglet.app.run()


    def update(self, dt):
        dt = min(dt, 1/30.0)
        self.time += dt
        self.world.update(dt)
        self.camera.position = (sin(self.time) * 5, 0, 0)
        self.window.invalid = True


    def draw(self):
        self.window.clear()
        self.projection.world_ortho(self.camera.zoom)
        self.camera.look_at_ortho()
        self.render.draw(self.world)
        self.projection.screen()
        self.camera.reset()
        self.clock_display.draw()
        return EVENT_HANDLED


    def stop(self):
        if self.window:
            self.window.close()

