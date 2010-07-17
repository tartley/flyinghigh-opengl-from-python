
from itertools import chain, repeat

from OpenGL import GL as gl

from ..engine.shape import face_normal


def glarray(gltype, seq, length):
    '''
    Convert a list of lists into a flattened ctypes array, eg:
    [ (1, 2, 3), (4, 5, 6) ] -> (GLfloat*6)(1, 2, 3, 4, 5, 6)
    '''
    arraytype = gltype * length
    return arraytype(*seq)


def triangulate(face):
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

    def __init__(self):
        self.num_glvertices = None
        self.glvertices = None
        self.index_type = None
        self.glindices = None
        self.glcolors = None
        self.glnormals = None


    def _get_num_glvertices(_, faces):
        return len(list(chain(*faces)))


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


    def _get_glvertices(self, vertices, faces):
        glverts = chain.from_iterable(
            vertices[index]
            for face in faces
            for index in face
        )
        return glarray(gl.GLfloat, glverts, self.num_glvertices * 3)


    def _get_glindices(self, faces):
        indices = []
        face_offset = 0
        for face in faces:
            face_indices = xrange(face_offset, face_offset + len(face))
            indices.extend(chain(*triangulate(face_indices)))
            face_offset += len(face)
        return glarray(self.index_type, indices, len(indices))


    def _get_glcolors(self, faces, face_colors):
        glcolors = []
        for face, color in zip(faces, face_colors):
            glcolors.extend(repeat(color, len(face)))
        return glarray(gl.GLubyte, chain(*glcolors), self.num_glvertices * 4) 


    def _get_glnormals(self, vertices, faces):
        normals = (
            face_normal(vertices, face)
            for face in faces
        )
        glnormals = chain.from_iterable(
            repeat(normal, len(face))
            for face, normal in zip(faces, normals)
        )
        return glarray(
            gl.GLfloat, chain(*glnormals), self.num_glvertices * 3) 


    def from_shape(self, shape):
        vertices = list(shape.vertices)
        faces = list(shape.faces)

        self.num_glvertices = self._get_num_glvertices(faces)
        self.glvertices = self._get_glvertices(vertices, faces)
        self.index_type = self._get_index_type(self.num_glvertices)
        self.glindices = self._get_glindices(faces)
        self.glcolors = self._get_glcolors(faces, shape.face_colors)
        self.glnormals = self._get_glnormals(vertices, faces)

