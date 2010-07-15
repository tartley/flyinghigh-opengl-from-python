from __future__ import division

from math import cos, pi, sin, sqrt

from .vec3 import Vec3


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


