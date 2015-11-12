from itertools import repeat
from unittest import TestCase, main

from ...component.shapes import Cube, Tetrahedron
from ...geometry.orientation import Orientation
from ...geometry.vec3 import Vec3, XAxis, YAxis, ZAxis
from ..shape import MultiShape, Shape



class testShape(TestCase):

    def testInit(self):
        verts = [Vec3(1, 2, 3), Vec3(4, 5, 6), Vec3(7, 8, 9)]
        faces = [[0, 1, 2], [0, 1, 2]]
        red = (255, 0, 0, 255)
        shape = Shape(verts, faces, repeat(red))
        self.assertEqual(shape.vertices, verts)
        self.assertEqual(shape.faces, faces)
        self.assertEqual(list(shape.face_colors), [red, red])

    def testInitEmpty(self):
        verts = []
        faces = []
        shape = Shape(verts, faces)
        self.assertEqual(shape.vertices, verts)
        self.assertEqual(shape.faces, faces)
        self.assertEqual(list(shape.face_colors), [])

    def testInitConvertsTupleVerts(self):
        verts = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
        shape = Shape(verts, [])
        for actual, expected in zip(shape.vertices, verts):
            self.assertTrue(isinstance(actual, Vec3))
            self.assertEqual(actual, expected)

    def testInitRaisesOnBadFaces(self):
        verts = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
        for faces in [
            [[0]],                  # face needs 3 verts
            [[0, 1]],               # face needs 3 verts
            [[0, 1, 2], [0]],       # face needs 3 verts
            [[0, 1, 2], [0, 1]],    # face needs 3 verts
            [[0, 1, -1], [0, 1, 2]], # negative index
            [[0, 1, 2], [0, 1, -1]], # negative index
            [[0, 1, 3], [0, 1, 2]], # index bigger than num verts
            [[0, 1, 2], [0, 1, 3]], # index bigger than num verts
        ]:
            self.assertRaises(AssertionError, lambda: Shape(verts, faces))

    def testInitDefaultsMissingColorsToWhite(self):
        verts = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
        faces = [[0, 1, 2]]
        white = (255, 255, 255, 255)
        shape = Shape(verts, faces)
        self.assertEqual(list(shape.face_colors), [white])

    def testInitCreatesColorSequenceOfCorrectLength(self):
        verts = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
        faces = [[0, 0, 0], [1, 1, 1], [2, 2, 2]]
        red = (255, 0, 0, 255)
        blue = (0, 0, 255, 255)

        # short color sequences are cycled
        shape = Shape(verts, faces, repeat(red, 1))
        self.assertEqual(list(shape.face_colors), [red, red, red])

        # short color lists are cycled
        shape = Shape(verts, faces, [red, blue])
        self.assertEqual(list(shape.face_colors), [red, blue, red])

        # normal case
        shape = Shape(verts, faces, repeat(red, 3))
        self.assertEqual(list(shape.face_colors), [red, red, red])

        # long color sequences truncated
        shape = Shape(verts, faces, repeat(red, 4)) 
        self.assertEqual(list(shape.face_colors), [red, red, red])

        # infinite color sequences truncated
        shape = Shape(verts, faces, repeat(red)) 
        self.assertEqual(list(shape.face_colors), [red, red, red])

    def testBadInit(self):
        self.assertRaises(TypeError, lambda: Shape())
        self.assertRaises(TypeError, lambda: Shape([]))


class testMultiShape(TestCase):

    def testInitEmpty(self):
        shape = MultiShape()
        self.assertEqual(list(shape.vertices), [])
        self.assertEqual(list(shape.faces), [])
        self.assertEqual(list(shape.face_colors), [])

    def testAdd(self):
        verts = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
        faces = [[0, 1, 2]]
        red = (255, 0, 0, 255)
        shape = Shape(verts, faces, [red])
        multi = MultiShape()
        multi.add(shape)
        self.assertEqual(list(multi.vertices), verts)
        self.assertEqual(list(multi.faces), faces)
        self.assertEqual(list(multi.face_colors), [red])

    def testAddWithPosition(self):
        verts = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
        faces = [[0, 1, 2]]
        shape = Shape(verts, faces)
        multi = MultiShape()
        multi.add(shape, Vec3(10, 20, 30))
        self.assertEqual(list(multi.vertices),
            [(11, 22, 33), (14, 25, 36), (17, 28, 39)])
        self.assertEqual(list(multi.faces), faces)

    def testAddWithOrientation(self):
        verts = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
        faces = [[0, 1, 2]]
        shape = Shape(verts, faces)
        multi = MultiShape()
        multi.add(shape, orientation=Orientation(XAxis))
        self.assertEqual(list(multi.vertices),
            [(3, 2, -1), (6, 5, -4), (9, 8, -7)])
        self.assertEqual(list(multi.faces), faces)

    def testMultiShapeCombinesChildrensVertsFacesColors(self):
        VERTS1 = [(1, 2, 3), (4, 5, 6), (7, 8, 9), (10, 11, 12)]
        FACES1 = [ [0, 1, 2], [1, 2, 3] ]
        RED = (1, 0, 0)
        YELLOW = (1, 1, 0)
        OFFSET1 = Vec3(100, 200, 300)
        s1 = Shape(VERTS1, FACES1, face_colors=(RED, YELLOW))

        VERTS2 = [(10, 20, 30), (40, 50, 60), (70, 80, 90), (100, 110, 120)]
        FACES2 = [ [3, 2, 1], [2, 1, 0] ]
        GREEN = (0, 1, 0)
        BLUE = (0, 0, 1)
        OFFSET2 = Vec3(400, 500, 600)
        s2 = Shape(VERTS2, FACES2, face_colors=(GREEN, BLUE))

        multi = MultiShape()
        multi.add(s1, OFFSET1)
        multi.add(s2, OFFSET2)

        self.assertEqual(list(multi.vertices),
           [OFFSET1 + v for v in VERTS1] + [OFFSET2 + v for v in VERTS2]
        )
        self.assertEqual(list(multi.faces),
           [ [0, 1, 2], [1, 2, 3], [7, 6, 5], [6, 5, 4] ]
        )
        self.assertEqual(list(multi.face_colors), [RED, YELLOW, GREEN, BLUE])

    def testMuliShapeCopesWithInfiniteColorIterators(self):
        red = (255, 0, 0, 255)
        blue = (0, 0, 255, 255)
        s1 = Tetrahedron(1, repeat(blue))
        s2 = Cube(1, repeat(red))
        multi = MultiShape()
        multi.add(s1)
        multi.add(s2)
        self.assertEqual(
            list(multi.face_colors),
            [blue, blue, blue, blue, red, red, red, red, red, red])

    def testMultiShapeVerticesAccumulateNestedChildrensOffsets(self):
        shape = Shape([(1, 2, 3)], [])

        mInner = MultiShape()
        mInner.add(shape, position=Vec3(10, 20, 30))
        self.assertEqual(list(mInner.vertices), [Vec3(11, 22, 33)])
                
        mOuter = MultiShape()
        mOuter.add(mInner, position=Vec3(100, 200, 300))
        self.assertEqual(list(mOuter.vertices), [Vec3(111, 222, 333)])
        

if __name__ == '__main__':
    main()

