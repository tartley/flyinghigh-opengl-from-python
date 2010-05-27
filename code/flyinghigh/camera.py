from __future__ import division

from math import sin, cos

from OpenGL import GL as gl, GLU as glu


class Camera(object):

    def __init__(self, x=0.0, y=0.0, zoom=10.0):
        self.x = x
        self.y = y
        self.zoom = zoom
        self.angle = 0.0


    def _get_ortho2d_bounds(self, width, height):
        aspect = width / height
        left = bottom = -self.zoom
        right = top = self.zoom
        if width > height: # landscape
            left *= aspect
            right *= aspect
        elif width < height: # portrait
            bottom /= aspect
            top /= aspect
        return left, right, bottom, top


    def world_projection_ortho(self, width, height):
        '''
        Screen's shortest dimension (usually height) will show exactly
        self.zoom of the world in each direction from the center of the screen,
        regardless of screen resolution
        '''
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        glu.gluOrtho2D(*self._get_ortho2d_bounds(width, height))
        gl.glMatrixMode(gl.GL_MODELVIEW)


    def look_at(self):
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        glu.gluLookAt(
            self.x, self.y, +1.0,
            self.x, self.y, -1.0,
            sin(self.angle), cos(self.angle), 0.0)

