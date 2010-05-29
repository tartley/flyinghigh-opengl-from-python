from __future__ import division

from math import sin, cos

from OpenGL import GL as gl, GLU as glu

class Camera(object):

    def __init__(self, position):
        self.position = position
        self.lookAt = (0, 0, 0)
        self.angle = 0.0


    def look_at_ortho(self):
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        glu.gluLookAt(
            self.position[0], self.position[1], +1.0,
            self.position[0], self.position[1], -1.0,
            sin(self.angle), cos(self.angle), 0.0)


    def look_at(self):
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        glu.gluLookAt(
            self.position[0], self.position[1], self.position[2],
            self.lookAt[0], self.lookAt[1], self.lookAt[2],
            0, 1, 0)


    def reset(self):
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()


