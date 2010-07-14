
from __future__ import division
from itertools import chain

from .geometry import Geometry
from .face import get_normal


SUBCUBE_BASE = 1/4
SUBCUBE_HEIGHT = 1/2


def add_vertex(vertices, vert):
    vertices.append(vert)
    return len(vertices) - 1


def replace_face(vertices, face, n):
    '''
    Given a list of vertices and a square face described by a list of 4
    indices into the vertex array, append to the vertex list in-place and
    return a new list of faces that describe a replacement geometry which looks
    like the original face, but with a cube sticking out of the middle.
    This replacement is performed recursively on each face of the new cube.
    This is repeated n times.
    '''
    if n <= 0:
        return [face]

    # indices
    i0 = face[0]
    i1 = face[1]
    i2 = face[2]
    i3 = face[3]
    # original verts
    v0 = vertices[i0]
    v1 = vertices[i1]
    v2 = vertices[i2]
    v3 = vertices[i3]
    # base of new cube
    v0inner = v0 + (v2 - v0) * SUBCUBE_BASE
    v1inner = v1 + (v3 - v1) * SUBCUBE_BASE
    v2inner = v2 + (v0 - v2) * SUBCUBE_BASE
    v3inner = v3 + (v1 - v3) * SUBCUBE_BASE
    # peaks of the new cube
    face_normal = get_normal(vertices, face)
    edge = (v0 - v1).length
    height = face_normal * edge * SUBCUBE_HEIGHT
    v0peak = v0inner + height
    v1peak = v1inner + height
    v2peak = v2inner + height
    v3peak = v3inner + height

    # modify vertices in-place. To localise the effect of side-effects,
    # the caller of this function should make a copy of vertices before
    # calling us. (they can then call us many times using a single copy)
    i0i = add_vertex(vertices, v0inner)
    i1i = add_vertex(vertices, v1inner)
    i2i = add_vertex(vertices, v2inner)
    i3i = add_vertex(vertices, v3inner)
    i0p = add_vertex(vertices, v0peak)
    i1p = add_vertex(vertices, v1peak)
    i2p = add_vertex(vertices, v2peak)
    i3p = add_vertex(vertices, v3peak)

    # construct list of new faces which replace 'face'
    faces = [
        # base
        [i0, i1, i1i, i0i],
        [i1, i2, i2i, i1i],
        [i2, i3, i3i, i2i],
        [i3, i0, i0i, i3i],
        # subcube sides
        [i0i, i1i, i1p, i0p],
        [i1i, i2i, i2p, i1p],
        [i2i, i3i, i3p, i2p],
        [i3i, i0i, i0p, i3p],
        # subcube top
        [i0p, i1p, i2p, i3p],
    ]
    return list(chain(
        [ faces[0], faces[1], faces[2], faces[3], ],
        replace_face(vertices, faces[4], n-1),
        replace_face(vertices, faces[5], n-1),
        replace_face(vertices, faces[6], n-1),
        replace_face(vertices, faces[7], n-1),
        replace_face(vertices, faces[8], n-1),
    ))


def KochCube(original, n=1):
    '''
    Performs a 'Koche cube' transformation to the given geometry.
    Return a new geometry, in which each face of the original has been
    replaced by a square with a new cube sticking out of it.
    Assumes the faces of the original are squares.
    '''
    verts = list(original.vertices)
    faces = list(chain.from_iterable(
        replace_face(verts, face, n) for face in original.faces))
    return Geometry(verts, faces)

