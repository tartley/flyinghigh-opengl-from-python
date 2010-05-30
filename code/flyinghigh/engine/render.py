
from math import degrees

from OpenGL import GL as gl


class Render(object):

    def init(self):
        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        gl.glEnableClientState(gl.GL_COLOR_ARRAY)
        gl.glEnable(gl.GL_DEPTH_TEST)        
        gl.glEnable(gl.GL_POLYGON_SMOOTH)
        gl.glDisable(gl.GL_BLEND)
        gl.glHint(gl.GL_POLYGON_SMOOTH_HINT, gl.GL_NICEST) 

        gl.glCullFace(gl.GL_BACK)
        gl.glEnable(gl.GL_CULL_FACE)

        gl.glClearColor(0.4, 0.2, 0.1, 1)


    def draw(self, world):
        for item in world.items.itervalues():
            gl.glPushMatrix()

            position = item.position
            if len(position) == 2:
                gl.glTranslatef(position[0]. position[1], 0)
                gl.glRotatef(degrees(item.angle), 0, 0, 1)
            else:
                gl.glTranslatef(*position)
                # TODO: 3D orientation

            glyph = item.glyph
            gl.glVertexPointer(
                glyph.dimension, gl.GL_FLOAT, 0, glyph.glVerts)
            gl.glColorPointer(4, gl.GL_FLOAT, 0, glyph.glColors)
            gl.glDrawElements(
                gl.GL_TRIANGLES,
                len(glyph.glIndices),
                gl.GL_UNSIGNED_BYTE,
                glyph.glIndices)

            gl.glPopMatrix()

