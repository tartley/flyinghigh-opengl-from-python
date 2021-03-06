from unittest import TestCase, main

from ..orientation import Orientation
from ..matrix import Matrix
from ..vec3 import Vec3, XAxis, YAxis


class testMatrix(TestCase):

    def testConstructor(self):
        position = Vec3(1, 2, 3)
        orientation = Orientation((4, 5, 6))

        matrix = Matrix(position, orientation)

        forward = orientation.forward
        up = orientation.up
        right = orientation.right
        expected = orientation.matrix
        expected[3] = position.x
        expected[7] = position.y
        expected[11] = position.z
        self.assertEqual(matrix.elements, expected)

    def testTransform(self):
        position = Vec3(10, 20, 30)
        vert = Vec3(1, 2, 3)

        # default orientation, this should translate only, zero rotation
        orientation = Orientation()
        matrix = Matrix(position, orientation)
        self.assertEqual(matrix.transform(vert) - position, vert)

        # now try a couple of transforms which do involve a rotation
        orientation = Orientation(YAxis)
        matrix = Matrix(position, orientation)
        self.assertEqual(matrix.transform(vert) - position, (1, 3, -2))

        orientation = Orientation(XAxis)
        matrix = Matrix(position, orientation)
        self.assertEqual(matrix.transform(vert) - position, (3, 2, -1))


if __name__ == '__main__':
    main()

