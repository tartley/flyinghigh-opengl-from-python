
try:
    # Python 2.6 with unittest2 installed
    from unittest2 import TestCase, main
except:
    # Python 2.7
    from unittest import TestCase, main

from collections import Iterable
from itertools import repeat

from ...geometry.geometry import Cube, Geometry, Tetrahedron
from ...geometry.orientation import Orientation
from ...geometry.vec3 import Vec3, YAxis, ZAxis
from ..shapes import MultiShape, Shape



def assert_is_a_shape(test, shape):
    test.assertIsNone(shape.position)
    test.assertIsNone(shape.orientation)
    test.assertTrue(isinstance(shape.vertices, Iterable))
    test.assertTrue(isinstance(shape.faces, Iterable))
    test.assertTrue(isinstance(shape.face_colors, Iterable))
    test.assertEquals(len(list(shape.faces)), len(list(shape.face_colors)))



class testShape(TestCase):

    def testInit(self):
        self.assertRaises(TypeError, Shape)

        geometry = Geometry([], [])

        s = Shape(geometry)
        assert_is_a_shape(self, s)
        self.assertEquals(s.geometry, geometry)
        self.assertEquals(list(s.face_colors), [])

        red = (255, 0, 0, 255)
        p = (1, 2, 3)
        o = Orientation((4, 5, 6))

        s = Shape(geometry, face_colors=repeat(red), position=p, orientation=o)
        self.assertEquals(list(s.face_colors), [])
        self.assertEquals(s.position, p)
        self.assertEquals(s.orientation, o)


    def testAttributes(self):
        verts = [(0, 1, 2), (3, 4, 5), (6, 7, 8)]
        faces = [[1, 2, 3]]
        geom = Geometry(verts, faces)
        color = (11, 22, 33, 44)
        s = Shape(geom, face_colors=repeat(color))
        self.assertTrue(
            all(actual == expected
                for actual, expected in zip(verts, s.vertices)))
        self.assertIs(s.faces, faces)
        self.assertEquals(list(s.face_colors), [color])


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
        YELLOW = (1, 1, 0)
        OFFSET1 = Vec3(100, 200, 300)
        s1 = Shape(Geometry(VERTS1, FACES1),
            face_colors=(RED, YELLOW), position=OFFSET1)

        VERTS2 = [(10, 20, 30), (40, 50, 60), (70, 80, 90), (100, 110, 120)]
        FACES2 = [ [3, 2, 1], [2, 1, 0] ]
        GREEN = (0, 1, 0)
        BLUE = (0, 0, 1)
        OFFSET2 = Vec3(400, 500, 600)
        s2 = Shape(Geometry(VERTS2, FACES2),
            face_colors=(GREEN, BLUE), position=OFFSET2)

        multi = MultiShape()
        multi.add(s1)
        multi.add(s2)

        self.assertEquals(list(multi.vertices),
           [OFFSET1 + v for v in VERTS1] + [OFFSET2 + v for v in VERTS2]
        )
        self.assertEquals(multi.faces,
           [ [0, 1, 2], [1, 2, 3], [7, 6, 5], [6, 5, 4] ]
        )
        self.assertEquals(list(multi.face_colors), [RED, YELLOW, GREEN, BLUE])


    def testMuliShapeCopesWithInfiniteColorIterators(self):
        red = (255, 0, 0, 255)
        blue = (0, 0, 255, 255)
        s1 = Shape(
            geometry=Tetrahedron(1),
            face_colors=repeat(blue),
        )
        s2 = Shape(
            geometry=Cube(1),
            face_colors=repeat(red),
        )
        multi = MultiShape(s1, s2)
        self.assertEquals(
            list(multi.face_colors),
            [blue, blue, blue, blue, red, red, red, red, red, red])


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

