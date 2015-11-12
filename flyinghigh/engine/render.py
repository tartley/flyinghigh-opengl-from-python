
from ..component.glyph import Glyph

from .. import gl


vertex_components = 3
color_components = 4

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
        gl.glEnable(gl.GL_DEPTH_TEST)        
        gl.glEnable(gl.GL_POLYGON_SMOOTH)
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glHint(gl.GL_POLYGON_SMOOTH_HINT, gl.GL_NICEST) 

        gl.glCullFace(gl.GL_BACK)
        gl.glEnable(gl.GL_CULL_FACE)

        gl.glClearColor(*self.world.clearColor)

        self.world.add_item += self.on_world_add_item


    def on_world_add_item(self, item):
        if hasattr(item, 'shape'):
            item.glyph = Glyph()
            item.glyph.from_shape(item.shape)


    def draw(self):
        gl.glEnableClientState(gl.GL_NORMAL_ARRAY)
        for item in self.world:
            if not hasattr(item, 'glyph'):
                continue

            gl.glPushMatrix()

            if hasattr(item, 'position'):
                gl.glTranslatef(*item.position)
            if hasattr(item, 'orientation'):
                gl.glMultMatrixf(item.orientation.matrix)

            glyph = item.glyph
            gl.glVertexPointer(
                vertex_components, gl.GL_FLOAT, 0, glyph.glvertices)
            gl.glColorPointer(
                color_components, gl.GL_UNSIGNED_BYTE, 0, glyph.glcolors)
            gl.glNormalPointer(gl.GL_FLOAT, 0, glyph.glnormals)
            gl.glDrawElements(
                gl.GL_TRIANGLES,
                len(glyph.glindices),
                type_to_enum[glyph.glindex_type],
                glyph.glindices)

            gl.glPopMatrix()


    def draw_hud(self, clock_display):
        gl.glDisableClientState(gl.GL_NORMAL_ARRAY)
        clock_display.draw()

