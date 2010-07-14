
from itertools import chain, repeat

from OpenGL import GL as gl

from ..geometry.face import get_normal



def _glarray(gltype, seq, length):
    '''
    Convert nested sequences of values into a single contiguous ctypes array
    of the given GLtype.
    '''
    arraytype = gltype * length
    return arraytype(*seq)


def _triangulate(face):
    '''
    If 'face' defines the indices of each vertices in a flat, convex polyon,
    output is that surface broken into triangles, wound in the same direction
    as the original poly.
    e.g. [0, 1, 2, 3, 4] -> [[0, 1, 2], [0, 2, 3], [0, 3, 4]]
    '''
    tris = []
    for index in xrange(1, len(face) - 1):
        triangle = [face[0], face[index], face[index+1]]
        tris.append(triangle)
    return tris


class Glyph(object):

    dimension = 3

    def __init__(self):
        self.num_glvertices = None
        self.glvertices = None
        self.index_type = None
        self.glindices = None
        self.glcolors = None
        self.glnormals = None


    def _get_num_glvertices(_, faces):
        return len(list(chain(*faces)))


    def _get_glvertices(self, shape):
        vertices = []
        for face in shape.faces:
            for vertexnum in face:
                vertices.append(shape.vertices[vertexnum])
        return _glarray(gl.GLfloat, chain(*vertices), self.num_glvertices * 3) 


    def _get_index_type(_, num_indices):
        '''
        return the numeric GL type needed to store the given number of values
        '''
        if num_indices < 256:
            index_type = gl.GLubyte
        elif num_indices < 65536:
            index_type = gl.GLushort
        else:
            index_type = gl.GLuint
        return index_type


    def _get_glindices(self, faces):
        indices = []
        face_offset = 0
        for face in faces:
            face_indices = xrange(face_offset, face_offset + len(face))
            indices.extend(chain(*_triangulate(face_indices)))
            face_offset += len(face)
        return _glarray(self.index_type, indices, len(indices))


    def _get_glcolors(self, shape):
        face_colors = iter(shape.face_colors)
        colors = []
        for face in shape.faces:
            colors.extend(repeat(face_colors.next(), len(face)))
        return _glarray(gl.GLubyte, chain(*colors), self.num_glvertices * 4) 


    def _get_glnormals(self, shape):
        faces = list(shape.faces)
        normals = (
            get_normal(shape.vertices, face)
            for face in faces
        )
        face_normals = zip(faces, normals)
        vert_normals = chain.from_iterable(
            repeat(normal, len(face))
            for face, normal in face_normals
        )
        return _glarray(
            gl.GLfloat, chain(*vert_normals), self.num_glvertices * 3) 


    def from_shape(self, shape):
        self.num_glvertices = self._get_num_glvertices(shape.faces)
        self.glvertices = self._get_glvertices(shape)
        self.index_type = self._get_index_type(self.num_glvertices)
        self.glindices = self._get_glindices(shape.faces)
        self.glcolors = self._get_glcolors(shape)
        self.glnormals = self._get_glnormals(shape)

