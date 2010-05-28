from itertools import chain, repeat

from OpenGL import GL as gl


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


    def from_geometry(self, item):
        verts = item.geometry.verts
        assert all(len(vert)==2 for vert in verts)
        self.glVerts = flatten(verts, gl.GLfloat)

        colors = tuple(repeat(item.color, len(item.geometry.verts)))
        assert len(colors[0]) in (3, 4)
        self.glColors = flatten(colors, gl.GLfloat)

        indices = item.geometry.indices
        assert all(len(color)==len(colors[0]) for color in colors)
        self.glIndices = flatten(indices, gl.GLubyte)

