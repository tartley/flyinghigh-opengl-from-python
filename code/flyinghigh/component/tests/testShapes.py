
from itertools import chain
from unittest2 import TestCase, main

from ..shapes import CompositeShape, Shape



class testCompositeShape(TestCase):

    def testVerts(self):
        VERTS1 = [(1, 2, 3), (4, 5, 6), (7, 8, 9), (10, 11, 12)]
        FACES1 = [ [0, 1, 2], [1, 2, 3] ]
        RED = (1, 0, 0)
        s1 = Shape(VERTS1, FACES1, RED)

        VERTS2 = [(10, 20, 30), (40, 50, 60), (70, 80, 90), (100, 110, 120)]
        FACES2 = [ [3, 2, 1], [2, 1, 0] ]
        BLUE = (0, 0, 1)
        s2 = Shape(VERTS2, FACES2, BLUE)

        composite = CompositeShape()
        composite.add(s1)
        composite.add(s2)

        self.assertEquals(composite.vertices, VERTS1 + VERTS2)

        self.assertEquals(composite.faces,
           [ [0, 1, 2], [1, 2, 3], [7, 6, 5], [6, 5, 4] ]
        )

        self.assertEquals(list(composite.colors), [RED] * 4 + [BLUE] * 4)

if __name__ == '__main__':
    main()

