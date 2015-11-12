from __future__ import division

from .. import gl, glu


class Projection(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height


    def resize(self, width, height):
        self.width = width
        self.height = height
        gl.glViewport(0, 0, width, height)


    def _ortho_bounds(self, zoom, aspect):
        left = bottom = -zoom
        right = top = zoom
        if self.width > self.height:
            # landscape mode window
            bottom /= aspect
            top /= aspect
        elif self.width < self.height:
            # portrait mode window
            left *= aspect
            right *= aspect
        return left, right, bottom, top


    def set_ortho(self, zoom):
        '''
        Screen's shortest dimension (usually height) will show exactly
        self.zoom of the world from the center of the screen to each edge,
        regardless of screen resolution, window size.
        '''
        aspect = self.width / self.height
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        glu.gluOrtho2D(*self._ortho_bounds(zoom, aspect))


    def set_perspective(self, fovy):
        aspect = self.width / self.height
        zNear = 0.1
        zFar = 1000.0
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        glu.gluPerspective(fovy, aspect, zNear, zFar);


    def set_screen(self):
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        glu.gluOrtho2D(0, self.width - 1, 0, self.height - 1)

