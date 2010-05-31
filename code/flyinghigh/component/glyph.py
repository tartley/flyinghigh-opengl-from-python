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
        self.dimensions = None


    def from_geometry(self, item):
        verts = item.geometry.vertices
        num_verts = len(verts)
        assert len(verts[0]) in VALID_VERT_LENS
        self.glVerts = gl_array(verts, gl.GLfloat)

        colors = tuple(repeat(item.color, num_verts))
        assert len(colors) == len(verts)
        assert len(colors[0]) in VALID_COLOR_LENS
        self.glColors = gl_array(colors, gl.GLfloat)

        indices = chain.from_iterable(
            triangulate(face) for face in item.geometry.faces)
        # assert len(indices[0]) == 3
        self.glIndices = gl_array(indices, gl.GLubyte)

        self.dimension = len(verts[0])

