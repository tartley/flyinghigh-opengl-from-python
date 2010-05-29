
from math import degrees

from OpenGL import GL as gl


class Render(object):

    def init(self):
        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        gl.glEnableClientState(gl.GL_COLOR_ARRAY)
        gl.glDisable(gl.GL_DEPTH_TEST)        
        gl.glEnable(gl.GL_POLYGON_SMOOTH)
        gl.glEnable(gl.GL_BLEND)
        gl.glHint(gl.GL_POLYGON_SMOOTH_HINT, gl.GL_NICEST) 


    def draw(self, world):
        for item in world.items.itervalues():
            gl.glPushMatrix()
            gl.glTranslatef(item.position[0], item.position[1], 0)
            gl.glRotatef(degrees(item.angle), 0, 0, 1)
            gl.glVertexPointer(2, gl.GL_FLOAT, 0, item.glyph.glVerts)
            gl.glColorPointer(4, gl.GL_FLOAT, 0, item.glyph.glColors)
            gl.glDrawElements(
                gl.GL_TRIANGLES,
                len(item.glyph.glIndices),
                gl.GL_UNSIGNED_BYTE,
                item.glyph.glIndices)
            gl.glPopMatrix()

