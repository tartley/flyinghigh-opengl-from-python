
cdef extern from "GL/gl.h":
    ctypedef unsigned int GLenum
    ctypedef int GLint
    ctypedef void GLvoid
    ctypedef int GLsizei
    ctypedef float GLfloat

    int GL_TRIANGLES
    int GL_FLOAT
    int GL_UNSIGNED_BYTE

    cdef void glPushMatrix()
    cdef void glPopMatrix()
    cdef void glTranslatef(GLfloat x, GLfloat y, GLfloat z)

    cdef void glVertexPointer(
        GLint size, GLenum type, GLsizei stride, GLvoid *ptr)
    cdef void glColorPointer(
        GLint size, GLenum type, GLsizei stride, GLvoid *ptr)
    cdef void glIndexPointer(
        GLenum type, GLsizei stride, GLvoid *ptr)
    cdef void glNormalPointer(
        GLenum type, GLsizei stride, GLvoid *ptr)

    cdef void  glDrawElements(GLenum, GLsizei, GLenum, GLvoid*)


cdef extern from "Python.h":
    ctypedef void PyTypeObject

cdef struct CDataObject:
    Py_ssize_t ob_refcnt
    PyTypeObject *ob_type
    char *b_ptr

cdef int vertex_components
cdef int color_components


from flyinghigh.component.glyph import Glyph

from pyglet import gl

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
        gl.glEnableClientState(gl.GL_NORMAL_ARRAY)
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
        cdef object b
        cdef CDataObject *a
        cdef char *x

        gl.glEnableClientState(gl.GL_NORMAL_ARRAY)
        for item in self.world:
            if not hasattr(item, 'glyph'):
                continue

            glPushMatrix()

            if hasattr(item, 'position'):
                glTranslatef(
                    <GLfloat>item.position.x,
                    <GLfloat>item.position.y,
                    <GLfloat>item.position.z)
            if hasattr(item, 'orientation'):
                gl.glMultMatrixf(
                    item.orientation.matrix)

            glyph = item.glyph

            b = glyph.glvertices
            a = <CDataObject *>b
            x = a.b_ptr
            glVertexPointer(
                vertex_components,
                GL_FLOAT,
                0,
                <GLvoid *>x)

            b = glyph.glcolors
            a = <CDataObject *>b
            x = a.b_ptr
            glColorPointer(
                color_components,
                GL_UNSIGNED_BYTE,
                0,
                <GLvoid *>x)

            b = glyph.glnormals
            a = <CDataObject *>b
            x = a.b_ptr
            glNormalPointer(
                GL_FLOAT,
                0,
                <GLvoid *>x)

            b = glyph.glindices
            a = <CDataObject *>b
            x = a.b_ptr
            glDrawElements(
                GL_TRIANGLES,
                len(glyph.glindices),
                type_to_enum[glyph.glindex_type],
                <GLvoid *>x)

            glPopMatrix()
        gl.glDisableClientState(gl.GL_NORMAL_ARRAY)


    def draw_hud(self, clock_display):
        clock_display.draw()

