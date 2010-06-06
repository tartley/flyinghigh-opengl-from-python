
from math import pi
from unittest2 import TestCase, main

from ..vec3 import Vec3, XAxis, YAxis, ZAxis
from ..orientation import Orientation


class testOrientation(TestCase):

    def testConstructionRightIsGenerated(self):
        o = Orientation(ZAxis)
        self.assertEqual(o.forward, (0, 0, 1))
        self.assertEqual(o.up, (0, 1, 0))
        self.assertEqual(o.right, (1, 0, 0))

    def testConstructionConvertsBareTuples(self):
        o = Orientation((1, 0, 0), (0, 0, 1))
        self.assertEquals(o.forward, (1, 0, 0))
        self.assertTrue(isinstance(o.forward, Vec3))
        self.assertEquals(o.up, (0, 0, 1))
        self.assertTrue(isinstance(o.up, Vec3))
        self.assertEquals(o.right, (0, 1, 0))
        self.assertTrue(isinstance(o.right, Vec3))

    def testConstructionNormalises(self):
        o = Orientation((1, 2, 3))
        self.assertAlmostEquals(o.forward.length, 1, places=15)
        self.assertAlmostEquals(o.up.length, 1, places=15)
        self.assertAlmostEquals(o.right.length, 1, places=15)

    def testConstructionBarfsOnNonOrthogonalVectors(self):
        self.assertRaises(AssertionError,
            lambda: Orientation((1, 2, 3), (3, -2, 1)))

    def testConstructionProvidesDefaultUp(self):
        self.assertEqual(Orientation((1, 0, 0)).up, (0, 1, 0))
        self.assertEqual(Orientation((0, 2, 0)).up, (0, 0, -1))
        self.assertEqual(Orientation((0, -2, 0)).up, (0, 0, 1))

    def testStr(self):
        self.assertEqual(str(Orientation(XAxis, up=YAxis)),
            'Orientation(Vec3(1.0, 0.0, 0.0), up=Vec3(0.0, 1.0, 0.0))')

    def testEqual(self):
        a = Orientation((0, 2, 3))
        self.assertTrue(a == Orientation((0, 2, 3)))
        self.assertFalse(a == Orientation((11, 2, 3)))
        self.assertFalse(a == Orientation((0, 2, 3), up=(0, -3, 2)))

    def testNotEqual(self):
        a = Orientation((0, 2, 3))
        self.assertFalse(a != Orientation((0, 2, 3)))
        self.assertTrue(a != Orientation((11, 2, 3)))
        self.assertTrue(a != Orientation((0, 2, 3), up=(0, -3, 2)))

    def testHash(self):
        a = Orientation((0, 2, 3))
        self.assertRaises(TypeError, lambda: hash(a))

    def testRoll(self):
        o = Orientation(ZAxis)
        o.roll(pi/2)
        self.assertEqual(o, Orientation(ZAxis, up=XAxis))

    def testYaw(self):
        o = Orientation(ZAxis)
        o.yaw(pi/2)
        self.assertEqual(o, Orientation(XAxis))

    def testPitch(self):
        o = Orientation(ZAxis)
        o.pitch(pi/2)
        self.assertEqual(o, Orientation(YAxis))

    def testMatrix(self):
        o = Orientation((1, 2, 3))
        expected = [
            o.right.x,   o.right.y,   o.right.z,   0,
            o.up.x,      o.up.y,      o.up.z,      0,
            o.forward.x, o.forward.y, o.forward.z, 0,
            0,           0,           0,           1,
        ]
        self.assertEqual(o.matrix, expected)

if __name__ == '__main__':
    main()

