from itertools import chain, repeat

from OpenGL import GL as gl


VALID_VERT_LENS = (2, 3)
VALID_COLOR_LENS = (3, 4)


def flatten(seq, gltype):
    '''
    Convert a sequence of the form ((a, b, c), (d, e, f)...) into a flat
    contiguous ctypes array (a, b, c, d, e, f...) of the given GLtype.
    '''
    assert all(len(seq[0]) == len(seq[i]) for i in xrange(1, len(seq)))
    return (gltype * (len(seq) * len(seq[0])))(*tuple(chain(*seq)))


class Glyph(object):

    def __init__(self):
        self.glVerts = None
        self.glColors = None
        self.glIndices = None
        self.dimensions = None


    def from_geometry(self, item):
        verts = item.geometry.verts
        assert len(verts[0]) in VALID_VERT_LENS
        self.glVerts = flatten(verts, gl.GLfloat)

        colors = tuple(repeat(item.color, len(item.geometry.verts)))
        assert len(colors) == len(verts)
        assert len(colors[0]) in VALID_COLOR_LENS
        self.glColors = flatten(colors, gl.GLfloat)

        indices = item.geometry.indices
        assert len(indices[0]) == 3
        self.glIndices = flatten(indices, gl.GLubyte)

        self.dimension = len(verts[0])

