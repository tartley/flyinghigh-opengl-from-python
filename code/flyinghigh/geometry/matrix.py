
from .vec3 import Origin, Vec3
from .orientation import Orientation


class Matrix(object):

    def __init__(self, position, orientation=None):
        if position is None:
            position = Origin
        if orientation is None:
            orientation = Orientation()
        
        self.elements = orientation.get_matrix()
        self.elements[3] = position.x
        self.elements[7] = position.y
        self.elements[11] = position.z


    def transform(self, vert):
        '''
        return the product of the given vertex by self, to give the vertex
        rotated and by our orientation and translated by our position.
        '''
        e = self.elements
        return Vec3(
            vert.x * e[0] + vert.y * e[1] + vert.z * e[2]   + e[3],
            vert.x * e[4] + vert.y * e[5] + vert.z * e[6]   + e[7],
            vert.x * e[8] + vert.y * e[9] + vert.z * e[10]  + e[11],
        )

