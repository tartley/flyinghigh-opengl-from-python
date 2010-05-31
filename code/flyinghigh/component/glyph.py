from itertools import chain, repeat

from OpenGL import GL as gl


VALID_VERT_LENS = (2, 3)
VALID_COLOR_LENS = (3, 4)


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

    def __init__(self):
        self.glVerts = None
        self.glColors = None
        self.glIndices = None
        self.index_type = None
        self.dimensions = None


    def from_shape(self, item):
        verts = tuple(item.shape.vertices)
        num_verts = len(verts)
        assert len(verts[0]) in VALID_VERT_LENS
        self.glVerts = gl_array(verts, gl.GLfloat)

        colors = tuple(item.shape.colors)
        assert len(colors) == len(verts)
        assert len(colors[0]) in VALID_COLOR_LENS
        self.glColors = gl_array(colors, gl.GLfloat)

        indices = tuple(chain.from_iterable(
            triangulate(face) for face in item.shape.faces))
        assert len(indices[0]) == 3
        self.index_type = gl.GLubyte
        if len(indices) > 65536:
            self.index_type = gl.GLuint
        elif len(indices) > 256:
            self.index_type = gl.GLushort
        self.glIndices = gl_array(indices, self.index_type)

        self.dimension = len(verts[0])

