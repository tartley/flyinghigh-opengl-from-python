from __future__ import division

from itertools import chain
from math import cos, pi, sin, sqrt
from random import randint

from ..geometry.matrix import Matrix
from ..geometry.orientation import Orientation
from ..geometry.vec3 import Origin, Vec3, XAxis, YAxis, ZAxis


white=(255, 255, 255, 255)


class Geometry(object):
    '''
    Defines a 3d object as a list of vertices, and a list of faces.
    Each face is a list of indices into the vertex array, forming a
    coplanar convex ring defining the face's boundary.
    '''
    def __init__(self, vertices, faces):
        if len(vertices) > 0 and not isinstance(vertices[0], Vec3):
            vertices = [Vec3(*v) for v in vertices]
        self.vertices = vertices
        self.faces = faces


class Shape(object):

    def __init__(self, geometry, color=white, position=None, orientation=None):
        self.geometry = geometry
        self.color = color
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

    @property
    def colors(self):
        return [self.color for _ in xrange(len(self.vertices))]


class MultiShape(object):

    def __init__(self, *args, **kwargs):
        self.children = list(args)
        self.position = kwargs.pop('position', None)
        self.orientation = kwargs.pop('orientation', None)
        assert kwargs == {}, 'unrecognized kwargs, %s' % (kwargs,)
        self._vertices = None
        self._colors = None
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
    def colors(self):
        if self._colors is None:
            self._colors = list(
                chain.from_iterable(shape.colors for shape in self.children))
        return self._colors


def Rectangle(width, height):
    vertices = [
        (-width/2, -height/2),
        (+width/2, -height/2),
        (+width/2, +height/2),
        (-width/2, +height/2),
    ]
    face = [0, 1, 2, 3]
    return Geometry(vertices, [face])


def Circle(radius):
    NUM_POINTS = 32
    verts = []
    for n in xrange(0, NUM_POINTS):
        a = n * 2 * pi / NUM_POINTS
        verts.append( (radius * cos(a), radius * sin(a)) )
    face = [n for n in xrange(0, NUM_POINTS)]
    return Geometry(verts, [face])


def Cube(edge):
    e2 = edge/2
    verts = [
        (-e2, -e2, -e2),
        (-e2, -e2, +e2),
        (-e2, +e2, -e2),
        (-e2, +e2, +e2),
        (+e2, -e2, -e2),
        (+e2, -e2, +e2),
        (+e2, +e2, -e2),
        (+e2, +e2, +e2),
    ]
    faces = [
        [0, 1, 3, 2], # left
        [4, 6, 7, 5], # right
        [7, 3, 1, 5], # front
        [0, 2, 6, 4], # back
        [3, 7, 6, 2], # top
        [1, 0, 4, 5], # bottom
    ]
    return Geometry(verts, faces)


def Tetrahedron(edge):
    size = edge / sqrt(2)/2
    vertices = [
        (+size, +size, +size),
        (-size, -size, +size),
        (-size, +size, -size),
        (+size, -size, -size), 
    ]
    faces = [ [0, 2, 1], [1, 3, 0], [2, 3, 1], [0, 3, 2] ]
    return Geometry(vertices, faces)


def Tetrahedron2(edge):
    '''
    same geometry as Tetrahedron, but at a differetn orientation
    '''
    # equilateral triangle centroid to mid-point of edge
    c2e = edge * sqrt(3) / 6
    # regular tetrahedron centroid to mid-point of face
    c2f = edge / sqrt(24)
    vertices = [
        (      0, 3*c2f,          0),
        (-edge/2,  -c2f,       -c2e),
        (+edge/2,  -c2f,       -c2e),
        (      0,  -c2f, edge*c2e*2),
    ]
    faces = [ [0, 1, 2], [0, 2, 3], [0, 1, 3] ]
    return Geometry(vertices, faces)


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


def CubeLattice(edge, cluster_edge, freq):
    shape = MultiShape()
    black = (0, 0, 0, 255)
    for i in xrange(int(-cluster_edge/2), int(+cluster_edge/2+1), freq):
        for j in xrange(int(-cluster_edge/2), int(+cluster_edge/2+1), freq):
            shape.add(Shape(Cube(edge), black, Vec3(i, j, -cluster_edge/2)))
            shape.add(Shape(Cube(edge), black, Vec3(i, j, +cluster_edge/2)))
            shape.add(Shape(Cube(edge), black, Vec3(i, -cluster_edge/2, j)))
            shape.add(Shape(Cube(edge), black, Vec3(i, +cluster_edge/2, j)))
            shape.add(Shape(Cube(edge), black, Vec3(-cluster_edge/2, i, j)))
            shape.add(Shape(Cube(edge), black, Vec3(+cluster_edge/2, i, j)))
    return shape


def CubeCross():
    multi = MultiShape()
    center_color = (150, 150, 150, 255)
    multi.add(Shape(Cube(2), center_color, Origin))

    outer_color = (170, 170, 170, 255)
    multi.add(Shape(Cube(1), outer_color, XAxis))
    multi.add(Shape(Cube(1), outer_color, YAxis))
    multi.add(Shape(Cube(1), outer_color, ZAxis))
    multi.add(Shape(Cube(1), outer_color, -XAxis))
    multi.add(Shape(Cube(1), outer_color, -YAxis))
    multi.add(Shape(Cube(1), outer_color, -ZAxis))
    return multi


def CubeCorners():
    multi = MultiShape()
    center_color = (150, 150, 150, 255)
    multi.add(Shape(Cube(2), center_color, Origin))

    outer_color = (170, 170, 170, 255)
    multi.add(Shape(Cube(1), outer_color, (+1, +1, +1)))
    multi.add(Shape(Cube(1), outer_color, (+1, +1, -1)))
    multi.add(Shape(Cube(1), outer_color, (+1, -1, +1)))
    multi.add(Shape(Cube(1), outer_color, (+1, -1, -1)))
    multi.add(Shape(Cube(1), outer_color, (-1, +1, +1)))
    multi.add(Shape(Cube(1), outer_color, (-1, +1, -1)))
    multi.add(Shape(Cube(1), outer_color, (-1, -1, +1)))
    multi.add(Shape(Cube(1), outer_color, (-1, -1, -1)))
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

