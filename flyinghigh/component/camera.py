from __future__ import division

from math import sin, cos

from .. import gl, glu


class CameraBase(object):

    def __init__(self):
        self.item = None

    def reset(self):
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()


class Camera(CameraBase):

    def __init__(self):
        super(Camera, self).__init__()

    def look_at(self, lookat):
        '''
        lookat is a tuple (x, y, z), towards which the camera should point
        '''
        position = self.item.position
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        glu.gluLookAt(
            position.x, position.y, position.z,
            lookat.x, lookat.y, lookat.z,
            0, 1, 0)


class CameraOrtho(CameraBase):

    def __init__(self):
        super(CameraOrtho, self).__init__()
        self.angle = 0.0

    def look_at(self, lookat):
        '''
        lookat is a tuple (x, y), towards which the camera should point
        '''
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        glu.gluLookAt(
            self.position.x, self.position.y, +1.0,
            lookat.x, lookat.y, -1.0,
            sin(self.angle), cos(self.angle), 0.0)

