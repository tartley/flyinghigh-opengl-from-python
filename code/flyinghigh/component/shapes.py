from __future__ import division

from itertools import islice, repeat
from random import randint

from ..geometry.geometry import Cube
from ..math.matrix import Matrix
from ..math.orientation import Orientation
from ..math.vec3 import Origin, Vec3, XAxis, YAxis, ZAxis


white=(255, 255, 255, 255)


class Shape(object):

    def __init__(self, geometry,
        color=None, face_colors=None, position=None, orientation=None):

        self.geometry = geometry

        assert color is None or face_colors is None
        if face_colors is None:
            if color is None:
                color = white
            face_colors = islice(repeat(color), len(geometry.faces))
        self.face_colors = face_colors

        if type(position) is tuple:
            position = Vec3(*position)
        self.position = position

        if type(orientation) is tuple:
            orientation = Orientation(orientation)
        self.orientation = orientation

        self._vertices = None


    @property
    def vertices(self):
        if self._vertices is None:
            matrix = Matrix(self.position, self.orientation)
            self._vertices = [
                matrix.transform(vert)
                for vert in self.geometry.vertices]
        return self._vertices


    @property
    def faces(self):
        return self.geometry.faces


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


def RgbCubeCluster(edge, cluster_edge, cube_count):
    shape = MultiShape()
    for i in xrange(cube_count):
        while True:
            r = randint(1, cluster_edge-1)
            g = randint(1, cluster_edge-1)
            b = randint(1, cluster_edge-1)
            color = (
                int(r / cluster_edge * 255),
                int(g / cluster_edge * 255),
                int(b / cluster_edge * 255),
                255)
            pos = Vec3(
                r - cluster_edge / 2,
                g - cluster_edge / 2,
                b - cluster_edge / 2,
            )
            if pos.length > 8:
                break
        shape.add(Shape(Cube(edge), color=color, position=Vec3(*pos)))
    return shape


def CubeLattice(edge, cluster_edge, freq, color):
    shape = MultiShape()
    for i in xrange(int(-cluster_edge/2), int(+cluster_edge/2+1), freq):
        for j in xrange(int(-cluster_edge/2), int(+cluster_edge/2+1), freq):
            for pos in [
                Vec3(i, j, -cluster_edge/2),
                Vec3(i, j, +cluster_edge/2),
                Vec3(i, -cluster_edge/2, j),
                Vec3(i, +cluster_edge/2, j),
                Vec3(-cluster_edge/2, i, j),
                Vec3(+cluster_edge/2, i, j),
            ]:
                shape.add(Shape(Cube(edge), color=color, position=pos))
    return shape


def CubeCross():
    multi = MultiShape()
    center_color = (150, 150, 150, 255)
    multi.add(Shape(Cube(2), center_color, Origin))

    outer_color = (170, 170, 170, 255)
    multi.add(Shape(Cube(1), color=outer_color, position=XAxis))
    multi.add(Shape(Cube(1), color=outer_color, position=YAxis))
    multi.add(Shape(Cube(1), color=outer_color, position=ZAxis))
    multi.add(Shape(Cube(1), color=outer_color, position=-XAxis))
    multi.add(Shape(Cube(1), color=outer_color, position=-YAxis))
    multi.add(Shape(Cube(1), color=outer_color, position=-ZAxis))
    return multi


def CubeCorners():
    multi = MultiShape()
    center_color = (150, 150, 150, 255)
    multi.add(Shape(Cube(2), color=center_color, position=Origin))

    outer_color = (170, 170, 170, 255)
    multi.add(Shape(Cube(1), color=outer_color, position=(+1, +1, +1)))
    multi.add(Shape(Cube(1), color=outer_color, position=(+1, +1, -1)))
    multi.add(Shape(Cube(1), color=outer_color, position=(+1, -1, +1)))
    multi.add(Shape(Cube(1), color=outer_color, position=(+1, -1, -1)))
    multi.add(Shape(Cube(1), color=outer_color, position=(-1, +1, +1)))
    multi.add(Shape(Cube(1), color=outer_color, position=(-1, +1, -1)))
    multi.add(Shape(Cube(1), color=outer_color, position=(-1, -1, +1)))
    multi.add(Shape(Cube(1), color=outer_color, position=(-1, -1, -1)))
    return multi
    

def RgbAxes():
    red = (255, 0, 0, 255)
    green = (0, 255, 0, 255)
    blue = (0, 0, 255, 255)
    cube1 = Cube(1)
    multi = MultiShape(
        Shape(
            geometry=cube1,
        ),
        Shape(
            geometry=cube1,
            color=red,
            position=XAxis,
        ),
        Shape(
            geometry=cube1,
            color=green,
            position=YAxis,
        ),
        Shape(
            geometry=Cube(1),
            color=blue,
            position=ZAxis,
        ),
    )
    return multi

