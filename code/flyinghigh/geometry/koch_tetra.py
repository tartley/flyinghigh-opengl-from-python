
from __future__ import division
from itertools import chain
from math import sqrt

from ..component.shapes import Geometry
from .face import get_normal


SUBTETRA_BASE = 0.5
SUBTETRA_HEIGHT = 0.5


def replace_face(vertices, face, n):
    '''
    Given a list of vertices and a triangular face described by a list of 3
    indices into the vertex array, append to the vertex list in-place and
    return a new list of faces that describe a replacement geometry which looks
    like the original face, but with a tetrahedron sticking out of the middle.
    This replacement is performed recursively on each face of the tetrahedron.
    This is repeated n times.
    '''
    if n <= 0:
        return [face]

    # indices
    i0 = face[0]
    i1 = face[1]
    i2 = face[2]
    # original verts
    v0 = vertices[i0]
    v1 = vertices[i1]
    v2 = vertices[i2]
    # midpoints of edges, which form vertices of the new tetrahedron
    v3mid = (v0 + v1) * SUBTETRA_BASE
    v4mid = (v1 + v2) * SUBTETRA_BASE
    v5mid = (v2 + v0) * SUBTETRA_BASE
    # location of the peak of the new tetrahedron
    face_centroid = (v0 + v1 + v2) / 3
    face_normal = get_normal(vertices, face)
    edge = (v0 - v1).length
    v6peak = face_centroid + face_normal * sqrt(2/3) * edge * SUBTETRA_HEIGHT

    def add_vertex(vert):
        vertices.append(vert)
        return len(vertices) - 1

    # modify vertices in-place. To localise the effect of side-effects,
    # the caller of this function should make a copy of vertices before
    # calling us. (they can then call us many times using a single copy)
    i3 = add_vertex(v3mid)
    i4 = add_vertex(v4mid)
    i5 = add_vertex(v5mid)
    i6 = add_vertex(v6peak)

    # construct list of new faces which replace 'face'
    faces = [ [i0, i3, i5], [i3, i1, i4], [i4, i2, i5],
              [i5, i3, i6], [i3, i4, i6], [i4, i5, i6], ]
    return list(chain(
        [ faces[0], faces[1], faces[2] ],
        replace_face(vertices, faces[3], n-1),
        replace_face(vertices, faces[4], n-1),
        replace_face(vertices, faces[5], n-1),
    ))


def KochTetra(original, n=1):
    '''
    Performs a 'Koche tetrahedron' transformation to the given geometry.
    Return a new geometry, in which each face of the original has been
    replaced by a triangle with a tetrahedron sticking out of it.
    Assumes the faces of the original are triangles.
    '''
    verts = list(original.vertices)
    faces = list(chain.from_iterable(
        replace_face(verts, face, n) for face in original.faces))
    return Geometry(verts, faces)

