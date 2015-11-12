
from __future__ import division
from itertools import repeat

from ..engine.shape import Shape, MultiShape, face_normal


SUBCUBE_BASE = 1/4
SUBCUBE_HEIGHT = 1/2


def add_vertex(vertices, vert):
    vertices.append(vert)
    return len(vertices) - 1


def get_new_color(orig, tip):
    RATE = 0.25
    r, g, b, _ = orig
    tr, tg, tb, _ = tip
    rdiff = tr - r
    gdiff = tg - g
    bdiff = tb - b
    return (
        int(r + rdiff * RATE),
        int(g + gdiff * RATE),
        int(b + bdiff * RATE),
        255)


def koch_cube_next(original, tip_color):
    verts = []
    faces = []
    face_colors = []
    original_verts = original.vertices
    for orig_face, orig_color in zip(original.faces, original.face_colors):
        # indices
        i0 = orig_face[0]
        i1 = orig_face[1]
        i2 = orig_face[2]
        i3 = orig_face[3]
        # original verts
        v0 = original_verts[i0]
        v1 = original_verts[i1]
        v2 = original_verts[i2]
        v3 = original_verts[i3]
        # base of new cube
        v0inner = v0 + (v2 - v0) * SUBCUBE_BASE
        v1inner = v1 + (v3 - v1) * SUBCUBE_BASE
        v2inner = v2 + (v0 - v2) * SUBCUBE_BASE
        v3inner = v3 + (v1 - v3) * SUBCUBE_BASE
        # peaks of the new cube
        edge = (v0 - v1).length
        height = face_normal(original_verts, orig_face) * edge * SUBCUBE_HEIGHT
        v0peak = v0inner + height
        v1peak = v1inner + height
        v2peak = v2inner + height
        v3peak = v3inner + height

        # create new shape's vertices & indices
        i0i = add_vertex(verts, v0inner)
        i1i = add_vertex(verts, v1inner)
        i2i = add_vertex(verts, v2inner)
        i3i = add_vertex(verts, v3inner)
        i0p = add_vertex(verts, v0peak)
        i1p = add_vertex(verts, v1peak)
        i2p = add_vertex(verts, v2peak)
        i3p = add_vertex(verts, v3peak)

        # create new shape's faces
        faces.append( [i0i, i1i, i1p, i0p] )
        faces.append( [i1i, i2i, i2p, i1p] )
        faces.append( [i2i, i3i, i3p, i2p] )
        faces.append( [i3i, i0i, i0p, i3p] )
        faces.append( [i0p, i1p, i2p, i3p] )

        # new shape's color
        color = get_new_color(orig_color, tip_color)
        face_colors.extend(list(repeat(color, 5)))

    return Shape(verts, faces, face_colors)


def koch_outer(transform, shape, n, tip_color):
    multi = MultiShape()
    multi.add(shape)
    for _ in range(n):
        shape = transform(shape, tip_color)
        multi.add(shape)
    return multi


def KochCube(shape, n, tip_color):
    return koch_outer(koch_cube_next, shape, n, tip_color)

