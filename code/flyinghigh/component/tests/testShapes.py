
from unittest2 import TestCase, main

from ..shapes import CompositeShape, Shape


class testCompositeShape(TestCase):

    def testVerts(self):
        s1 = Shape(
            [(1, 2, 3), (4, 5, 6), (7, 8, 9), (10, 11, 12)],
            [ [0, 1, 2], [1, 2, 3] ]
        )
        s2 = Shape(
            [(10, 20, 30), (40, 50, 60), (70, 80, 90), (100, 110, 120)],
            [ [3, 2, 1], [2, 1, 0] ]
        )
        composite = CompositeShape()
        composite.add(s1)
        composite.add(s2)

        self.assertEquals( composite.vertices,
            [(1, 2, 3), (4, 5, 6), (7, 8, 9), (10, 11, 12),
             (10, 20, 30), (40, 50, 60), (70, 80, 90), (100, 110, 120)]
        )

        self.assertEquals( composite.faces,
            [ [0, 1, 2], [1, 2, 3], [7, 6, 5], [6, 5, 4] ])


if __name__ == '__main__':
    main()

