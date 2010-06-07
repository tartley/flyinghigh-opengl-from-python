
from math import sqrt, pi
from unittest2 import TestCase, main

from ..vec3 import EPSILON, Origin, Vec3


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
        self.assertTrue(Vec3(1, 2, 3) == Vec3(1, 2, 3))
        self.assertTrue(Vec3(1, 2, 3) == (1, 2, 3))
        self.assertFalse(Vec3(1, 2, 3) == Vec3(11, 2, 3))
        self.assertFalse(Vec3(1, 2, 3) == Vec3(1, 22, 3))
        self.assertFalse(Vec3(1, 2, 3) == Vec3(1, 2, 33))

    def testNotEq(self):
        self.assertFalse(Vec3(1, 2, 3) != Vec3(1, 2, 3))
        self.assertFalse(Vec3(1, 2, 3) != (1, 2, 3))
        self.assertTrue(Vec3(1, 2, 3) != Vec3(11, 2, 3))
        self.assertTrue(Vec3(1, 2, 3) != Vec3(1, 22, 3))
        self.assertTrue(Vec3(1, 2, 3) != Vec3(1, 2, 33))

    def testHash(self):
        self.assertEqual(hash(Vec3(1, 2, 3)), hash(Vec3(1, 2, 3)))
        self.assertNotEqual(hash(Vec3(1, 2, 3)), hash(Vec3(11, 2, 3)))
        self.assertNotEqual(hash(Vec3(1, 2, 3)), hash(Vec3(1, 22, 3)))
        self.assertNotEqual(hash(Vec3(1, 2, 3)), hash(Vec3(1, 2, 33)))

    def testAlmostEqual(self):
        error = EPSILON * 0.9
        self.assertEqual(Vec3(1, 2, 3), Vec3(1 + error, 2, 3))
        self.assertEqual(Vec3(1, 2, 3), Vec3(1, 2 + error, 3))
        self.assertEqual(Vec3(1, 2, 3), Vec3(1, 2, 3 + error))
        error = EPSILON * 1.1
        self.assertNotEqual(Vec3(1, 2, 3), Vec3(1 + error, 2, 3))
        self.assertNotEqual(Vec3(1, 2, 3), Vec3(1, 2 + error, 3))
        self.assertNotEqual(Vec3(1, 2, 3), Vec3(1, 2, 3 + error))

    def testLength(self):
        self.assertEquals(Vec3(2, 3, 4).length, sqrt(4 + 9 + 16))

    def testLength2(self):
        self.assertEquals(Vec3(2, 3, 4).length2, 4 + 9 + 16)

    def testNormalize(self):
        v = Vec3(3, 4, 5)
        self.assertEquals(
            v.normalize(),
            Vec3(3/v.length, 4/v.length, 5/v.length) )

    def testNeg(self):
        v = -Vec3(1, 2, 3)
        self.assertEqual(v.x, -1)
        self.assertEqual(v.y, -2)
        self.assertEqual(v.z, -3)

    def testAdd(self):
        self.assertEqual(Vec3(1, 2, 3) + Vec3(10, 20, 30), (11, 22, 33))
        self.assertEqual(Vec3(1, 2, 3) +     (10, 20, 30), (11, 22, 33))
        self.assertEqual(    (1, 2, 3) + Vec3(10, 20, 30), (11, 22, 33))
        self.assertRaises(TypeError, lambda: Vec3(1, 2, 3) + 4)
        self.assertRaises(TypeError, lambda: 4 + Vec3(1, 2, 3))

    def testSub(self):
        self.assertEquals(Vec3(11, 22, 33) - Vec3(10, 20, 30), (1, 2, 3))
        self.assertEquals(Vec3(11, 22, 33) -     (10, 20, 30), (1, 2, 3))
        self.assertEquals(    (11, 22, 33) - Vec3(10, 20, 30), (1, 2, 3))
        self.assertRaises(TypeError, lambda: Vec3(1, 2, 3) - 4)
        self.assertRaises(TypeError, lambda: 4 - Vec3(1, 2, 3))

    def testMul(self):
        self.assertEquals(Vec3(1, 2, 3) * 10, Vec3(10, 20, 30))
        self.assertEquals(10 * Vec3(1, 2, 3), Vec3(10, 20, 30))

    def testDiv(self):
        self.assertEquals(Vec3(10, 20, 30) / 10, Vec3(1, 2, 3))
        self.assertEquals(Vec3(2, 0, 0) / 3, Vec3(0.6666666666666667, 0, 0))
        self.assertRaises(ZeroDivisionError, lambda: Vec3(1, 2, 3) / 0)
        self.assertRaises(TypeError, lambda: 3 / Vec3(1, 2, 3))

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

    def testDotProduct(self):
        a = Vec3(2, 3, 5)
        b = Vec3(7, 11, 13)
        self.assertEquals(a.dot(b), 2 * 7 + 3 * 11 + 5 * 13)

    def testAngle(self):
        a = Vec3(1, 0, 0)
        b = Vec3(1, 1, 0)
        self.assertAlmostEqual(a.angle(b), pi/4, places=15)
        self.assertAlmostEqual(a.angle(a), 0, places=7)
        self.assertAlmostEqual(b.angle(b), 0, places=7)

    def testRotateX(self):
        x = Vec3(1, 0, 0)
        y = Vec3(0, 1, 0)
        z = Vec3(0, 0, 1)
        self.assertEquals(x.rotateX(pi/2), x)
        self.assertEquals(y.rotateX(pi/2), -z)
        self.assertEquals(z.rotateX(pi/2), y)

    def testRotateY(self):
        x = Vec3(1, 0, 0)
        y = Vec3(0, 1, 0)
        z = Vec3(0, 0, 1)
        self.assertEquals(x.rotateY(pi/2), z)
        self.assertEquals(y.rotateY(pi/2), y)
        self.assertEquals(z.rotateY(pi/2), -x)

    def testRotateZ(self):
        x = Vec3(1, 0, 0)
        y = Vec3(0, 1, 0)
        z = Vec3(0, 0, 1)
        self.assertEquals(x.rotateZ(pi/2), -y)
        self.assertEquals(y.rotateZ(pi/2), x)
        self.assertEquals(z.rotateZ(pi/2), z)

    def testRotate(self):
        x = Vec3(1, 0, 0)
        y = Vec3(0, 1, 0)
        z = Vec3(0, 0, 1)
        self.assertEquals(x.rotate(x, pi/2), x)
        self.assertEquals(y.rotate(x, pi/2), -z)
        self.assertEquals(z.rotate(x, pi/2), y)

        self.assertEquals(x.rotate(y, pi/2), z)
        self.assertEquals(y.rotate(y, pi/2), y)
        self.assertEquals(z.rotate(y, pi/2), -x)

        self.assertEquals(x.rotate(z, pi/2), -y)
        self.assertEquals(y.rotate(z, pi/2), x)
        self.assertEquals(z.rotate(z, pi/2), z)


if __name__ == '__main__':
    main()

