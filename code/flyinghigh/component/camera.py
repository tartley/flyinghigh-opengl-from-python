from __future__ import division

from math import sin, cos

from OpenGL import GL as gl, GLU as glu

from ..geometry.vec3 import Origin


class CameraBase(object):

    def __init__(self):
        self.item = None

    def reset(self):
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()


class Camera(CameraBase):

    def __init__(self):
        super(Camera, self).__init__()
        self.lookAt = Origin

    def look_at(self):
        position = self.item.position
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        glu.gluLookAt(
            position.x, position.y, position.z,
            self.lookAt.x, self.lookAt.y, self.lookAt.z,
            0, 1, 0)


class CameraOrtho(CameraBase):

    def __init__(self):
        super(CameraOrtho, self).__init__()
        self.angle = 0.0

    def look_at(self):
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        glu.gluLookAt(
            self.position.x, self.position.y, +1.0,
            self.position.x, self.position.y, -1.0,
            sin(self.angle), cos(self.angle), 0.0)

