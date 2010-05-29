
from math import cos, sin

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
        self.camera = Camera(position=(0, 0, -10))

        self.window = Window(fullscreen=True, visible=False, resizable=True)
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
        self.camera.position = (
            sin(self.time * 2) * 20,
            0,
            -40 + cos(self.time * 3) * 20)
        self.window.invalid = True


    def draw(self):
        self.window.clear()
        self.projection.set_perspective(45)
        self.camera.look_at()
        self.render.draw(self.world)
        self.projection.set_screen()
        self.camera.reset()
        self.clock_display.draw()
        return EVENT_HANDLED


    def stop(self):
        if self.window:
            self.window.close()

