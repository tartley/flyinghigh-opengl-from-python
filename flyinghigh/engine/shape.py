
from itertools import chain, cycle, islice, repeat

from ..geometry.matrix import Matrix
from ..geometry.vec3 import Vec3
from ..component.color import Color, white


def face_normal(vertices, face):
    '''
    Return the unit normal vector (at right angles to) this face.
    Note that the direction of the normal will be reversed if the
    face's winding is reversed.
    '''
    v0 = vertices[face[0]]
    v1 = vertices[face[1]]
    v2 = vertices[face[2]]
    a = v0 - v1
    b = v2 - v1
    return b.cross(a).normalized()


class Shape(object):
    '''
    Defines a polyhedron, a 3D shape with flat faces and straight edges.
    Each vertex defines a point in 3d space. Each face is a list of indices
    into the vertex array, forming a coplanar convex ring defining the face's
    edges. Each face has its own color.
    '''
    def __init__(self, vertices, faces, face_colors=None):
        
        if len(vertices) > 0 and not isinstance(vertices[0], Vec3):
            vertices = [Vec3(*v) for v in vertices]
        self.vertices = vertices

        for face in faces:
            assert len(face) >= 3
            for index in face:
                assert 0 <= index < len(vertices)
        self.faces = faces

        if face_colors is None:
            face_colors = white
        if isinstance(face_colors, Color):
            face_colors = repeat(face_colors)

        # TODO: colors of koch_cube/tetra break if we remove this 'list'
        # and set face_colors to return the 'islice'. Don't know why.
        self.face_colors = list(islice(cycle(face_colors), len(self.faces)))


class MultiShape(object):

    def __init__(self, *args):
        self.children = []
        self.matrices = []

        self._vertices = None
        self._faces = None


    def add(self, child, position=None, orientation=None):
        self.children.append(child)
        self.matrices.append(Matrix(position, orientation))


    @property
    def vertices(self):
        return (
            matrix.transform(vertex)
            for child, matrix in zip(self.children, self.matrices)
            for vertex in child.vertices
        )


    @property
    def faces(self):
        if self._faces is None:
            self._faces = []

            child_offset = 0
            for child in self.children:
                for face in child.faces:
                    newface = []
                    for index in face:
                        newface.append(index + child_offset)
                    self._faces.append(newface)
                child_offset += len(list(child.vertices))

        return self._faces


    @property
    def face_colors(self):
        return chain.from_iterable(
            child.face_colors for child in self.children)

