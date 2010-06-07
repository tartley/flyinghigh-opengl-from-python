
def get_normal(vertices, face):
    '''
    Vertices is a sequence of 3d vertices, face is a sequence of indices into
    the vertex array that defines the coplanar vetices of a flat polygon.
    Return the unit normal vector (at right angles to) this polygon. Note that
    the direction of the normal will be reversed if the face's winding is
    reversed.
    '''
    v0 = vertices[face[0]]
    v1 = vertices[face[1]]
    v2 = vertices[face[2]]
    a = v0 - v1
    b = v2 - v1
    return b.cross(a).normalize()

