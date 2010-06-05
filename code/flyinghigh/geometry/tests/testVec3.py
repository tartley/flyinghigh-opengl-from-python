
from math import sqrt
from unittest2 import TestCase, main

from ..vec3 import Vec3


class testVec3(TestCase):

    def testConstructor(self):
        v = Vec3(1, 2, 3)
        self.assertRaises(TypeError, lambda: Vec3())
        self.assertRaises(TypeError, lambda: Vec3(1))
        self.assertRaises(TypeError, lambda: Vec3(1, 2))
        self.assertRaises(TypeError, lambda: Vec3(1, 2, 3, 4))

    def testAccess(self):
        v = Vec3(1, 2, 3)
        self.assertEqual(v.x, 1)
        self.assertEqual(v.y, 2)
        self.assertEqual(v.z, 3)

    def testRepr(self):
        v = Vec3(1, 2, 3)
        self.assertEqual(str(v), 'Vec3(1, 2, 3)')

        v = Vec3(1.1, 2.2, 3.3)
        self.assertEqual(str(v), 'Vec3(1.1, 2.2, 3.3)')

    def testEq(self):
        self.assertEqual(Vec3(1, 2, 3), Vec3(1, 2, 3))
        self.assertEqual(Vec3(1, 2, 3),     (1, 2, 3))

    def testLength(self):
        self.assertEquals(Vec3(2, 3, 4).length, sqrt(4 + 9 + 16))

    def testLength2(self):
        self.assertEquals(Vec3(2, 3, 4).length2, 4 + 9 + 16)

    def testNeg(self):
        v = -Vec3(1, 2, 3)
        self.assertEqual(v.x, -1)
        self.assertEqual(v.y, -2)
        self.assertEqual(v.z, -3)

    def testAdd(self):
        self.assertEqual(Vec3(1, 2, 3) + Vec3(10, 20, 30), (11, 22, 33))
        self.assertEqual(Vec3(1, 2, 3) +     (10, 20, 30), (11, 22, 33))
        self.assertEqual(    (1, 2, 3) + Vec3(10, 20, 30), (11, 22, 33))

    def testSub(self):
        self.assertEquals(Vec3(11, 22, 33) - Vec3(10, 20, 30), (1, 2, 3))
        self.assertEquals(Vec3(11, 22, 33) -     (10, 20, 30), (1, 2, 3))
        self.assertEquals(    (11, 22, 33) - Vec3(10, 20, 30), (1, 2, 3))

    def testCrossProduct(self):
        a = Vec3(1, 0, 0)
        b = Vec3(0, 2, 0)
        c = Vec3(0, 0, 3)
        self.assertEquals(a.cross(b), (0, 0, 2))
        self.assertEquals(b.cross(a), (0, 0, -2))
        self.assertEquals(a.cross(c), (0, -3, 0))
        self.assertEquals(c.cross(a), (0, 3, 0))
        self.assertEquals(b.cross(c), (6, 0, 0))
        self.assertEquals(c.cross(b), (-6, 0, 0))

if __name__ == '__main__':
    main()

