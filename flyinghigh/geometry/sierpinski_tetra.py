"""
Brilliant Sierpinski gasket generator submitted by Oscar Lindberg
"""
from __future__ import division

import numpy as np

from ..engine.shape import Shape
from .vec3 import Vec3


def SierpinskiTetra(original, n, scale=0.5, **kwargs):
    verts = list(original.vertices)
    faces = list(original.faces)

    CORNERS = len(verts)

    # Convert geometry to ndarrays
    vs = np.zeros((1, len(verts), 3), dtype=np.float32)
    for i, vert in enumerate(verts):
        vs[0, i] = vert.x, vert.y, vert.z
    fs = np.array(faces).reshape(1, len(faces), len(faces[0]))

    # Split tetras n times
    for _ in range(n):
        # Create new arrays with room for 4 child tetras for each tetra
        vs_next = np.zeros((vs.shape[0], CORNERS, vs.shape[-2], vs.shape[-1]))
        fs_next = np.zeros((fs.shape[0], CORNERS, fs.shape[-2], fs.shape[-1]), 
                           dtype=np.int32)
        # For each tetra
        for i, tetra_vs in enumerate(vs):
          # Create a new tetra at each corner
          for j, corner in enumerate(tetra_vs):
            vs_next[i, j] = scale * (tetra_vs - corner) + corner
            fs_next[i, j] = CORNERS*(CORNERS*i+j) + fs[0]
        # We don't care any longer that the tetras are children. 
        # Now we just have a list of tetras again
        vs_next.shape = (-1, vs_next.shape[-2], vs_next.shape[-1])
        fs_next.shape = (-1, fs_next.shape[-2], fs_next.shape[-1])

        vs = vs_next
        fs = fs_next

    vs.shape = (-1, vs.shape[-1])
    fs.shape = (-1, fs.shape[-1])

    # Convert ndarrays back to Geometry
    verts = [Vec3(x, y, z) for x, y, z in vs]
    faces = fs.tolist()

    return Shape(verts, faces, **kwargs)

