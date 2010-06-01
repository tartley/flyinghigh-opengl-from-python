
from math import degrees

from OpenGL import GL as gl


type_to_enum = {
    gl.GLubyte: gl.GL_UNSIGNED_BYTE,
    gl.GLushort: gl.GL_UNSIGNED_SHORT,
    gl.GLuint: gl.GL_UNSIGNED_INT,
}

class Render(object):

    def __init__(self, world):
        self.world = world

    def init(self):
        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        gl.glEnableClientState(gl.GL_COLOR_ARRAY)
        gl.glEnableClientState(gl.GL_NORMAL_ARRAY)
        gl.glEnable(gl.GL_DEPTH_TEST)        
        gl.glEnable(gl.GL_POLYGON_SMOOTH)
        gl.glEnable(gl.GL_BLEND)
        gl.glHint(gl.GL_POLYGON_SMOOTH_HINT, gl.GL_NICEST) 

        gl.glCullFace(gl.GL_BACK)
        gl.glEnable(gl.GL_CULL_FACE)

        gl.glClearColor(*self.world.clearColor)


    def draw(self, world):
        for item in world.items.itervalues():
            if not hasattr(item, 'glyph'):
                continue

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
            gl.glNormalPointer(gl.GL_FLOAT, 0, glyph.glNormals)
            gl.glDrawElements(
                gl.GL_TRIANGLES,
                len(glyph.glIndices),
                type_to_enum[glyph.index_type],
                glyph.glIndices)

            gl.glPopMatrix()

