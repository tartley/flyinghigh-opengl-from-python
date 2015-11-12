from __future__ import division

from os.path import join

import pyglet
from pyglet.event import EVENT_HANDLED
from pyglet.window import Window

from .gameitem import GameItem
from .projection import Projection
from .render import Render
from .shader import FragmentShader, ShaderProgram, VertexShader
from .world import World

from ..component.wobblyorbit import WobblyOrbit
from ..component.camera import Camera
from ..geometry.vec3 import Origin


class Gameloop(object):

    def __init__(self):
        self.camera = None
        self.projection = None
        self.render = None
        self.window = None
        self.world = None
        self.fpss = []

    def prepare(self, options):
        self.window = Window(
            fullscreen=options.fullscreen,
            vsync=False,
            visible=False,
            resizable=True)
        self.window.on_draw = self.draw
        self.projection = Projection(self.window.width, self.window.height)
        self.window.on_resize = self.projection.resize

        self.world = World()

        self.camera = Camera()
        self.world.add( GameItem(
            camera=self.camera,
            position=Origin,
            move=WobblyOrbit(32, 1, speed=-0.5),

        ) )

        self.render = Render(self.world)
        self.render.init()
        pyglet.clock.schedule(self.update)
        self.clock_display = pyglet.clock.ClockDisplay()

        vs = VertexShader(join('flyinghigh', 'shaders', 'lighting.vert'))
        fs = FragmentShader(join('flyinghigh', 'shaders', 'lighting.frag'))
        shader = ShaderProgram(vs, fs)
        shader.use()


    def update(self, dt):
        # self.fpss.append(1/max(1e-3, dt))
        dt = min(dt, 1 / 30)
        self.world.update(dt)
        self.window.invalid = True


    def draw(self):
        self.window.clear()

        self.projection.set_perspective(45)
        self.camera.look_at(Origin)
        self.render.draw()

        self.projection.set_screen()
        self.camera.reset()
        self.render.draw_hud(self.clock_display)

        return EVENT_HANDLED


    def stop(self):
        if self.window:
            self.window.close()
        # print '  '.join("%6.1f" % (dt, ) for dt in self.fpss)

