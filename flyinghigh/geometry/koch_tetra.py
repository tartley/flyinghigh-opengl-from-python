
from __future__ import division
from itertools import repeat
from math import sqrt

from ..engine.shape import Shape, face_normal
from .koch_cube import koch_outer, get_new_color


SUBTETRA_BASE = 0.5
SUBTETRA_HEIGHT = 0.5


def add_vertex(vertices, vert):
    vertices.append(vert)
    return len(vertices) - 1


def koch_tetra_next(original, tip_color):
    '''
    return a new shape, consisting of one small tetrahedron sticking out of
    each face of the original shape. The new shape has a colors copied from
    the faces of the original, but tinted towards 'tip_color'
    '''
    verts = []
    faces = []
    face_colors = []
    orig_verts = original.vertices

    for orig_face, orig_color in zip(original.faces, original.face_colors):
        # indices
        i0 = orig_face[0]
        i1 = orig_face[1]
        i2 = orig_face[2]
        # original verts
        v0 = orig_verts[i0]
        v1 = orig_verts[i1]
        v2 = orig_verts[i2]
        # midpoints of edges, which form vertices of the new tetrahedron
        v3mid = (v0 + v1) * SUBTETRA_BASE
        v4mid = (v1 + v2) * SUBTETRA_BASE
        v5mid = (v2 + v0) * SUBTETRA_BASE
        # location of the peak of the new tetrahedron
        face_centroid = (v0 + v1 + v2) / 3
        edge = (v0 - v1).length
        v6peak = (face_centroid + face_normal(orig_verts, orig_face) *
            sqrt(2/3) * edge * SUBTETRA_HEIGHT)

        # create new shape's vertices & indices
        i3 = add_vertex(verts, v3mid)
        i4 = add_vertex(verts, v4mid)
        i5 = add_vertex(verts, v5mid)
        i6 = add_vertex(verts, v6peak)

        # create new shape's faces
        faces.append( [i5, i3, i6] )
        faces.append( [i3, i4, i6] )
        faces.append( [i4, i5, i6] )

        # new shape's color
        color = get_new_color(orig_color, tip_color)
        face_colors.extend(list(repeat(color, 3)))

    return Shape(verts, faces, face_colors)


def KochTetra(shape, n, tip_color):
    return koch_outer(koch_tetra_next, shape, n, tip_color)

