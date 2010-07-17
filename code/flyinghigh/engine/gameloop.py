from os.path import join

import pyglet
from pyglet.event import EVENT_HANDLED
from pyglet.window import Window

from .projection import Projection
from .render import Render
from .shader import FragmentShader, ShaderProgram, VertexShader
from .world import World
from ..component.camera import Camera


class Gameloop(object):

    def __init__(self):
        self.camera = None
        self.projection = None
        self.render = None
        self.window = None
        self.world = None


    def prepare(self):
        self.window = Window(
            vsync=True, fullscreen=True, visible=False, resizable=True)
        self.window.set_exclusive_mouse(True)
        self.window.on_draw = self.draw
        self.projection = Projection(self.window.width, self.window.height)
        self.window.on_resize = self.projection.resize

        self.camera = Camera()
        self.world = World()

        self.render = Render(self.world)
        self.render.init()
        pyglet.clock.schedule(self.update)
        self.clock_display = pyglet.clock.ClockDisplay()

        vs = VertexShader(join('flyinghigh', 'shaders', 'lighting.vert'))
        fs = FragmentShader(join('flyinghigh', 'shaders', 'lighting.frag'))
        shader = ShaderProgram(vs, fs)
        shader.use()


    def update(self, dt):
        dt = min(dt, 1/30.0)
        self.world.update(dt)
        self.window.invalid = True


    def draw(self):
        self.window.clear()
        self.projection.set_perspective(45)
        self.camera.look_at()
        self.render.draw()
        self.projection.set_screen()
        self.camera.reset()
        self.clock_display.draw()
        return EVENT_HANDLED


    def stop(self):
        if self.window:
            self.window.close()

