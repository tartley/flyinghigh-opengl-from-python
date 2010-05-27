
from math import degrees

from OpenGL import GL as gl


class Render(object):

    def init(self):
        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        gl.glEnableClientState(gl.GL_COLOR_ARRAY)
        gl.glEnable(gl.GL_DEPTH_TEST)        
        gl.glEnable(gl.GL_POLYGON_SMOOTH)
        gl.glEnable(gl.GL_BLEND)
        gl.glHint(gl.GL_POLYGON_SMOOTH_HINT, gl.GL_NICEST) 


    def resize(self, width, height):
        print 'resize', width, height
        gl.glViewport(0, 0, width, height)

        # projection.screen()
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(-width/2, width/2, -height/2, height/2, -1, 1)

        gl.glMatrixMode(gl.GL_MODELVIEW)


    def draw(self, world):
        for item in world.ents.itervalues():
            gl.glPushMatrix()
            pos = item.position
            gl.glTranslatef(*pos)
            #gl.glRotatef(degrees(item.angle), 0, 0, 1)
            gl.glVertexPointer(2, gl.GL_FLOAT, 0, item.glyph.glVerts)
            gl.glColorPointer(4, gl.GL_FLOAT, 0, item.glyph.glColors)

            gl.glDrawElements(
                gl.GL_TRIANGLES,
                len(item.glyph.glIndices),
                gl.GL_UNSIGNED_BYTE,
                item.glyph.glIndices)

            gl.glBegin(gl.GL_TRIANGLES)
            gl.glColor(0.5, 0.25, 0.1, 1.0)

            gl.glVertex2f(-4.0, -4.0)
            gl.glVertex2f(4.0, 4.0)
            gl.glVertex2f(4.0, -4.0)

            # gl.glVertex2f(-5, -5)
            # gl.glVertex2f(-5, +5)
            # gl.glVertex2f(+5, +5)

            gl.glEnd()

            gl.glPopMatrix()

