from itertools import chain

from OpenGL import GL as gl


def _print_array(name, array):
    print name
    print '\n'.join(
        '%s %s' % (i, element)
        for i, element in enumerate(array))


def _get_index_type(num_indices):
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


def _glarray(gltype, seq, length):
    '''
    Convert nested sequences of values into a single contiguous ctypes array
    of the given GLtype.
    '''
    arraytype = gltype * length
    return arraytype(*seq)


def _get_normal(vertices, face):
    '''
    Given a face, takes the first three vertices, calculates the cross-product
    of the two vectors defined by them. This is a vector at right angles to the
    face - the normal. Note that the direction of the normal will be reversed
    if the face's winding is reversed.
    '''
    v0 = vertices[face[0]]
    v1 = vertices[face[1]]
    v2 = vertices[face[2]]
    a = v0 - v1
    b = v2 - v1
    return b.cross(a)


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


    def _get_num_glvertices(self, faces):
        return len(list(chain(*faces)))


    def _get_glvertices(self, shape):
        vertices = []
        for face in shape.faces:
            for index, vertexnum in enumerate(face):
                vertices.append(shape.vertices[vertexnum])
        return _glarray(gl.GLfloat, chain(*vertices), self.num_glvertices * 3) 


    def _get_glnormals(self, shape):
        face_normals = (_get_normal(shape.vertices, face)
                        for face in shape.faces)
        normals = (normal
                   for face, normal in zip(shape.faces, face_normals)
                   for index in face)
        return _glarray(gl.GLfloat, chain(*normals), self.num_glvertices * 3) 


    def _get_glcolors(self, shape):
        colors = []
        for face in shape.faces:
            for index, vertexnum in enumerate(face):
                colors.append(shape.colors[vertexnum])
        return _glarray(gl.GLfloat, chain(*colors), self.num_glvertices * 4) 


    def _get_glindices(self, shape):
        indices = []
        face_offset = 0
        for face in shape.faces:
            face_indices = []
            for index, vertexnum in enumerate(face):
                face_indices.append(index + face_offset)
            indices.extend(chain(*_triangulate(face_indices)))
            face_offset += len(face)
        return _glarray(self.index_type, indices, len(indices))


    def from_shape(self, shape):
        self.num_glvertices = self._get_num_glvertices(shape.faces)
        self.glvertices = self._get_glvertices(shape)
        self.index_type = _get_index_type(self.num_glvertices)
        self.glindices = self._get_glindices(shape)
        self.glcolors = self._get_glcolors(shape)
        self.glnormals = self._get_glnormals(shape)

