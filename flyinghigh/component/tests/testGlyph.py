from itertools import chain, repeat
from unittest import TestCase, main

from ... import gl
from ...engine.shape import Shape
from ..glyph import Glyph, tessellate


class testGlyph(TestCase):

    def test_tessellate(self):
        data = [
            ([11, 22, 33], [[11, 22, 33]]),
            ([11, 22, 33, 44], [[11, 22, 33], [11, 33, 44]]),
        ]
        for datum, expected in data:
            self.assertEqual(list(tessellate(datum)), expected)


    def get_shape(self):
        # two orthogonal squares share one common edge
        # create shape using generators, to make sure that works
        return Shape(
            vertices = [
                (0, 0, 0), # v0
                (1, 0, 0), # v1
                (1, 1, 0), # v2
                (0, 1, 0), # v3
                (1, 0, 1), # v4
                (0, 0, 1), # v5
            ],
            faces = [
                [0, 1, 2, 3],
                [0, 1, 4, 5],
            ],
            face_colors = [(11, 22, 33, 44), (55, 66, 77, 88)]
        )

    def test_get_num_glvertices(self):
        shape = self.get_shape()
        glyph = Glyph()
        self.assertEqual(glyph.get_num_glvertices(shape.faces), 8)

    def test_get_glindices(self):
        shape = self.get_shape()
        glyph = Glyph()

        glyph.from_shape(shape)

        actual = glyph.glindices
        expected_values = [0, 1, 2,  0, 2, 3,  4, 5, 6,  4, 6, 7]
        self.assertEqual(type(actual), gl.GLubyte * 12)
        self.assertEqual(list(actual), expected_values)

    def assert_lists_almost_equal(self, l1, l2, places=15):
        for a, e in zip(l1, l2):
            self.assertAlmostEqual(a, e, places=places)

    def test_get_glvertices(self):
        shape = self.get_shape()
        glyph = Glyph()

        glyph.from_shape(shape)

        actual = glyph.glvertices
        self.assertEqual(type(actual), gl.GLfloat * (8 * 3))
        expected_values = [
            (0, 0, 0), #v0 0
            (1, 0, 0), #v1 1 
            (1, 1, 0), #v2 2
            (0, 1, 0), #v3 3
            (0, 0, 0), #v0 4
            (1, 0, 0), #v1 5
            (1, 0, 1), #v4 6
            (0, 0, 1), #v5 7
        ]
        self.assert_lists_almost_equal(
            list(actual), list(chain(*expected_values)))

    def test_get_glnormals(self):
        shape = self.get_shape()
        glyph = Glyph()

        glyph.from_shape(shape)

        actual = glyph.glnormals
        n0 = (0, 0, 1)
        n1 = (0, -1, 0)
        expected_values = [n0, n0, n0, n0, n1, n1, n1, n1]
        self.assertEqual(type(actual), gl.GLfloat * (8 * 3))
        self.assert_lists_almost_equal(
            list(actual), list(chain(*expected_values)))

    def test_get_glcolors(self):
        shape = self.get_shape()
        glyph = Glyph()

        glyph.from_shape(shape)

        actual = glyph.glcolors
        self.assertTrue(isinstance(actual, gl.GLubyte * (8 * 4)))
        self.assertEqual(type(actual), gl.GLubyte * (8 * 4))
        expected_values = list(chain.from_iterable(chain(
            repeat([11, 22, 33, 44], 4),
            repeat([55, 66, 77, 88], 4),
        )))
        self.assert_lists_almost_equal(actual, expected_values, places=7)


if __name__ == '__main__':
    main()

