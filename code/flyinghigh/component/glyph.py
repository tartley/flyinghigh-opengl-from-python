from collections import Iterable
from itertools import repeat

from OpenGL import GL as gl


VALID_VERT_LENS = (2, 3)
VALID_COLOR_LENS = (3, 4)


def flatten(seq):
    '''
    convert nested sequences into a single flat contiguous stream of values
    eg. ((1, 2, 3), (4, (5, 6))) becomes (1, 2, 3, 4, 5, 6).
    '''
    for item in seq:
        if isinstance(item, Iterable):
            for i in flatten(item):
                yield i
        else:
            yield item


def gl_array(seq, gltype):
    '''
    Convert possibly nested sequences of values into a single contiguous
    ctypes array of the given GLtype.
    '''
    assert all(len(seq[0]) == len(seq[i]) for i in xrange(1, len(seq)))
    values = tuple(flatten(seq))
    arraytype = gltype * len(values)
    return arraytype(*values)


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

        indices = item.geometry.faces
        # assert len(indices[0]) == 3
        self.glIndices = gl_array(indices, gl.GLubyte)

        self.dimension = len(verts[0])

