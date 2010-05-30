from __future__ import division

from math import sin, cos

from OpenGL import GL as gl, GLU as glu

from .position import Position


class CameraBase(object):

    def __init__(self, item):
        self.item = item

    def reset(self):
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()


class Camera(CameraBase):

    def __init__(self, item):
        super(Camera, self).__init__(item)
        self.lookAt = Position(0, 0, 0)

    def look_at(self):
        position = self.item.position
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        glu.gluLookAt(
            position.x, position.y, position.z,
            self.lookAt.x, self.lookAt.y, self.lookAt.z,
            0, 1, 0)


class CameraOrtho(CameraBase):

    def __init__(self, item):
        super(CameraOrtho, self).__init__(item)
        self.angle = 0.0

    def look_at(self):
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        glu.gluLookAt(
            self.position.x, self.position.y, +1.0,
            self.position.x, self.position.y, -1.0,
            sin(self.angle), cos(self.angle), 0.0)

