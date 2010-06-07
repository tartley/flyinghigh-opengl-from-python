
from math import sqrt

from ..component.shapes import Shape
from .face import get_normal


def BaselessTetrahedron(edge):
    '''
    Return a shape, 3 sides of a tetrahedron. One vertex points up the Y axis.
    The opposite face is the missing one.
    '''
    # equilateral triangle centroid to mid-point of edge
    c2e = edge * sqrt(3) / 6
    # regular tetrahedron centroid to mid-point of face
    c2f = edge / sqrt(24)
    return Shape(
        verts = [
            (      0, 3*c2f,          0),
            (-edge/2,  -c2f,       -c2e),
            (+edge/2,  -c2f,       -c2e),
            (      0,  -c2f, edge*c2e*2),
        ],
        faces = [ [0, 1, 2], [0, 2, 3], [0, 1, 3] ],
    )


def Serpinski(original):
    '''
    return a new shape, which is like the given one but with a tetrahedron 
    stuck into the middle of each face.
    Assumes the faces of the given original are equilateral triangles.
    '''
    retval = Shape()
    for face in original.faces:
        # original verts
        v0 = original.vertices[face[0]]
        v1 = original.vertices[face[1]]
        v2 = original.vertices[face[2]]
        # # midpoints of edges
        # midpoints = [
            # (v0 + v1) / 2,
            # (v1 + v2) / 2,
            # (v2 + v0) / 2 ]
        face_centroid = (v0 + v1 + v2) / 3
        face_normal = get_normal(original.vertices, face)
        edge = (v0 - v1).length
        retval.add( Shape(
            geometry=BaselessTetrahedron(edge/2),
            offset=face_centroid,
            orientation=face_normal,
            color=original.color))

