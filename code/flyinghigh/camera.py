from __future__ import division

from math import sin, cos

from OpenGL import GL as gl, GLU as glu

from .component.position import Position


class Camera(object):

    def __init__(self, position):
        self.position = position
        self.lookAt = Position(0, 0, 0)
        self.angle = 0.0


    def look_at_ortho(self):
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        glu.gluLookAt(
            self.position.x, self.position.y, +1.0,
            self.position.x, self.position.y, -1.0,
            sin(self.angle), cos(self.angle), 0.0)


    def look_at(self):
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        glu.gluLookAt(
            self.position.x, self.position.y, self.position.z,
            self.lookAt.x, self.lookAt.y, self.lookAt.z,
            0, 1, 0)


    def reset(self):
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()


