
from collections import Iterable
from unittest2 import TestCase, main


from ...geometry.orientation import Orientation
from ...geometry.vec3 import Origin, Vec3, YAxis, ZAxis
from ..shapes import Geometry, MultiShape, Shape


class testGeometry(TestCase):

    def testInitBad(self):
        self.assertRaises(TypeError, Geometry)
        self.assertRaises(TypeError, lambda: Geometry([]))

    def testInit(self):
        verts = []
        faces = []
        geometry = Geometry(verts, faces)
        self.assertEquals(geometry.vertices, verts)
        self.assertEquals(geometry.faces, faces)


def assert_is_a_shape(test, shape):
    test.assertIsNone(shape.position)
    test.assertIsNone(shape.orientation)
    test.assertTrue(isinstance(shape.vertices, Iterable))
    test.assertTrue(isinstance(shape.faces, Iterable))
    test.assertTrue(isinstance(shape.colors, Iterable))


class testShape(TestCase):

    def testInit(self):
        self.assertRaises(TypeError, Shape)

        geometry = Geometry([], [])

        s = Shape(geometry)
        assert_is_a_shape(self, s)
        self.assertEquals(s.geometry, geometry)
        self.assertEquals(s.color, (255, 255, 255, 255))

        red = (255, 0, 0, 255)
        position = (1, 2, 3)
        orientation = Orientation((4, 5, 6))

        s = Shape(geometry, red, position, orientation)
        self.assertEquals(s.color, red)
        self.assertEquals(s.position, position)
        self.assertEquals(s.orientation, orientation)

    def testAttributes(self):
        verts = [(0, 1, 2), (3, 4, 5), (6, 7, 8)]
        faces = [[1, 2, 3]]
        geom = Geometry(verts, faces)
        color = (11, 22, 33, 44)
        s = Shape(geom, color)
        self.assertTrue(
            all(actual == expected
                for actual, expected in zip(verts, s.vertices)))
        self.assertIs(s.faces, faces)
        self.assertEquals(len(s.colors), len(verts))
        self.assertTrue(all(c == color for c in s.colors))


class testMultiShape(TestCase):

    def testInit(self):
        m = MultiShape()
        assert_is_a_shape(self, m)
        self.assertEquals(m.children, [])

        geometry = Geometry([], [])
        child1 = Shape(geometry)
        child2 = Shape(geometry)
        position = ZAxis
        orientation = Orientation(YAxis)

        m = MultiShape(
            child1, child2, position=position, orientation=orientation)
        self.assertEqual(m.children, [child1, child2])
        self.assertEquals(m.position, position)
        self.assertEquals(m.orientation, orientation)

        self.assertRaises(AssertionError,
            lambda: MultiShape(child1, child2, other_kwargs=None))

        
    def testMultiShapeCombinesChildrensVertsFacesColors(self):
        VERTS1 = [(1, 2, 3), (4, 5, 6), (7, 8, 9), (10, 11, 12)]
        FACES1 = [ [0, 1, 2], [1, 2, 3] ]
        RED = (1, 0, 0)
        OFFSET1 = Vec3(100, 200, 300)
        s1 = Shape(Geometry(VERTS1, FACES1), RED, OFFSET1)

        VERTS2 = [(10, 20, 30), (40, 50, 60), (70, 80, 90), (100, 110, 120)]
        FACES2 = [ [3, 2, 1], [2, 1, 0] ]
        BLUE = (0, 0, 1)
        OFFSET2 = Vec3(400, 500, 600)
        s2 = Shape(Geometry(VERTS2, FACES2), BLUE, OFFSET2)

        multi = MultiShape()
        multi.add(s1)
        multi.add(s2)

        self.assertEquals(list(multi.vertices),
           [OFFSET1 + v for v in VERTS1] + [OFFSET2 + v for v in VERTS2]
        )

        self.assertEquals(multi.faces,
           [ [0, 1, 2], [1, 2, 3], [7, 6, 5], [6, 5, 4] ]
        )

        self.assertEquals(list(multi.colors), [RED] * 4 + [BLUE] * 4)


    def testMultiShapeVerticesAccumulateNestedChildrensOffsets(self):
        geom = Geometry([(1, 2, 3)], [])
        shape = Shape(geom, position=Vec3(10, 20, 30))
        self.assertEquals(shape.vertices, [Vec3(11, 22, 33)])

        mInner = MultiShape(shape, position=Vec3(100, 200, 300))
        self.assertEquals(mInner.vertices, [Vec3(111, 222, 333)])

        mMiddle = MultiShape(mInner, position=Vec3(1000, 2000, 3000))
        self.assertEquals(mMiddle.vertices, [Vec3(1111, 2222, 3333)])
        

if __name__ == '__main__':
    main()

