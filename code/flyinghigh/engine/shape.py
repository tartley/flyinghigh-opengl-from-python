
from itertools import islice, repeat

from ..geometry.matrix import Matrix
from ..geometry.orientation import Orientation
from ..geometry.vec3 import Vec3


white=(255, 255, 255, 255)


class Shape(object):
    '''
    Defines a polyhedron, a 3D shape with flat faces and straight edges.
    Each vertex defines a point in 3d space. Each face is a list of indices
    into the vertex array, forming a coplanar convex ring defining the face's
    edges. Each face has its own color.
    '''
    def __init__(self, vertices, faces,
        face_colors=None, position=None, orientation=None):

        if len(vertices) > 0 and not isinstance(vertices[0], Vec3):
            vertices = [Vec3(*v) for v in vertices]
        self._vertices = vertices
        self._transformed_vertices = None

        self.faces = faces

        if face_colors is None:
            face_colors = repeat(white)
        else:
            assert (
                hasattr(face_colors, 'next') or
                len(face_colors) == len(faces)
            )
        self.face_colors = islice(face_colors, len(self.faces))

        if type(position) is tuple:
            position = Vec3(*position)
        self.position = position

        if type(orientation) is tuple:
            orientation = Orientation(orientation)
        self.orientation = orientation


    @property
    def vertices(self):
        if self._transformed_vertices is None:
            matrix = Matrix(self.position, self.orientation)
            self._transformed_vertices = [
                matrix.transform(vert)
                for vert in self._vertices]

        return self._transformed_vertices



class MultiShape(object):

    def __init__(self, *args, **kwargs):
        self.children = list(args)
        self.position = kwargs.pop('position', None)
        self.orientation = kwargs.pop('orientation', None)
        assert kwargs == {}, 'unrecognized kwargs, %s' % (kwargs,)
        self._vertices = None
        self._faces = None

    def add(self, child):
        self.children.append(child)

    @property
    def vertices(self):
        if self._vertices is None:
            matrix = Matrix(self.position, self.orientation)
            self._vertices = [
                matrix.transform(vert)
                for shape in self.children
                for vert in shape.vertices]
        return self._vertices

    @property
    def faces(self):
        if self._faces is None:
            newfaces = []
            index_offset = 0
            for shape in self.children:
                for face in shape.faces:
                    newface = []
                    for index in face:
                        newface.append(index + index_offset)
                    newfaces.append(newface)
                index_offset += len(shape.vertices)
            self._faces = newfaces
        return self._faces

    @property
    def face_colors(self):
        face_colors = []
        for shape in self.children:
            face_colors.extend(islice(shape.face_colors, len(shape.faces)))
        return face_colors

