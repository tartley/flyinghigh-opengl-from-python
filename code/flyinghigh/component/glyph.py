from itertools import chain

from OpenGL import GL as gl


VALID_VERT_LENS = (2, 3)
VALID_COLOR_LEN = 4


def gl_array(seq, gltype):
    '''
    Convert nested sequences of values into a single contiguous ctypes array
    of the given GLtype.
    '''
    assert all(len(seq[0]) == len(seq[i]) for i in xrange(1, len(seq)))
    values = list(chain(*seq))
    arraytype = gltype * len(values)
    return arraytype(*values)


def triangulate(face):
    '''
    If 'face' defines the indices of each vertices in a flat, convex polyon,
    output is that surface broken into triangles.
    e.g. [0, 1, 2, 3, 4] -> [[0, 1, 2], [0, 2, 3], [0, 3, 4]]
    '''
    assert len(face) > 2
    tris = []
    for index in xrange(1, len(face) - 1):
        triangle = [face[0], face[index], face[index+1]]
        tris.append(triangle)
    return tris


class Glyph(object):

    # todo: generalise this to 2d as well
    dimension = 3

    def __init__(self):
        self.glVerts = None
        self.glColors = None
        self.glIndices = None
        self.index_type = None


    def _get_glverts(self, shape):
        verts = tuple(shape.vertices)
        num_verts = len(verts)
        assert len(verts[0]) in VALID_VERT_LENS
        x = gl_array(verts, gl.GLfloat)
        return x


    def _get_glcolors(self, shape):
        colors = tuple(shape.colors)
        assert len(colors) == len(self.glVerts) / self.dimension
        assert len(colors[0]) == VALID_COLOR_LEN
        return gl_array(colors, gl.GLfloat)


    def _get_index_type(self, num_indices):
        index_type = gl.GLubyte
        if num_indices > 65535:
            index_type = gl.GLuint
        elif num_indices > 255:
            index_type = gl.GLushort
        return index_type


    def _get_glindices(self, shape):
        indices = tuple(chain.from_iterable(
            triangulate(face) for face in shape.faces))
        assert len(indices[0]) == 3
        self.index_type = self._get_index_type(len(indices))
        return gl_array(indices, self.index_type)


    def _get_glnormals(self, shape):
        normals = []
        
        return gl_array(normals, gl.GLfloat)


    def from_shape(self, shape):
        self.glVerts = self._get_glverts(shape)
        self.glColors = self._get_glcolors(shape)
        self.glIndices = self._get_glindices(shape)
        self.glNormals = self._get_glnormals(shape)

