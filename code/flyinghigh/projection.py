from __future__ import division

from OpenGL import GL as gl, GLU as glu

class Projection(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height


    def resize(self, width, height):
        self.width = width
        self.height = height
        gl.glViewport(0, 0, width, height)


    def _ortho_zoom_to_longest(self, zoom, aspect):
        left = bottom = -zoom
        right = top = zoom
        if self.width > self.height: # landscape
            bottom /= aspect
            top /= aspect
        elif self.width < self.height: # portrait
            left *= aspect
            right *= aspect
        return left, right, bottom, top


    def _ortho_zoom_to_shortest(self, zoom, aspect):
        left = bottom = -zoom
        right = top = zoom
        if self.width > self.height: # landscape
            left *= aspect
            right *= aspect
        elif self.width < self.height: # portrait
            bottom /= aspect
            top /= aspect
        return left, right, bottom, top


    def world_ortho(self, zoom):
        '''
        Screen's shortest dimension (usually height) will show exactly
        self.zoom of the world from the center of the screen to each edge,
        regardless of screen resolution, window size.
        '''
        aspect = self.width / self.height

        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        glu.gluOrtho2D(*self._ortho_zoom_to_longest(zoom, aspect))


    def world_3d(self):
        fovy = 90.0
        aspect = self.width / self.height
        zNear = 1.0
        zFar = 100.0
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        glu.gluPerspective(fovy, aspect, zNear, zFar);


    def screen(self):
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        glu.gluOrtho2D(0, self.width - 1, 0, self.height - 1)

