
from unittest2 import TestCase, main

from ..glyph import triangulate


class testGlyph(TestCase):

    def testTriangulate(self):
        data = [
            ([11, 22, 33], [[11, 22, 33]]),
            ([11, 22, 33, 44], [[11, 22, 33], [11, 33, 44]]),
        ]
        for datum, expected in data:
            self.assertEquals(list(triangulate(datum)), expected)


    def testTriangulateFails(self):
        data = [ [], [11], [11, 22], ]
        for datum in data:
            self.assertRaises(AssertionError, lambda: list(triangulate(datum)))


if __name__ == '__main__':
    main()

