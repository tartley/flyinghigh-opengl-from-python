from math import pi
from unittest import TestCase, main

from ... import gl

from ..vec3 import NegXAxis, NegYAxis, NegZAxis, Vec3, XAxis, YAxis, ZAxis
from ..orientation import Orientation


class testOrientation(TestCase):

    def testConstructionDefaults(self):
        o = Orientation()
        self.assertEqual(o.forward, NegZAxis)
        self.assertEqual(o.up, YAxis)
        self.assertEqual(o.right, XAxis)

    def testConstructionConvertsBareTuples(self):
        o = Orientation(XAxis, ZAxis)
        self.assertEqual(o.forward, XAxis)
        self.assertTrue(isinstance(o.forward, Vec3))
        self.assertEqual(o.up, ZAxis)
        self.assertTrue(isinstance(o.up, Vec3))
        self.assertEqual(o.right, NegYAxis)
        self.assertTrue(isinstance(o.right, Vec3))

    def testConstructionNormalises(self):
        o = Orientation((1, 2, 3))
        self.assertAlmostEqual(o.forward.length, 1, places=15)
        self.assertAlmostEqual(o.up.length, 1, places=15)
        self.assertAlmostEqual(o.right.length, 1, places=15)

    def testConstructionBarfsOnNonOrthogonalVectors(self):
        self.assertRaises(AssertionError,
            lambda: Orientation((1, 2, 3), (3, -2, 1)))

    def testConstructionProvidesDefaultUp(self):
        self.assertEqual(Orientation(XAxis).up, YAxis)
        self.assertEqual(Orientation(YAxis).up, ZAxis)
        self.assertEqual(Orientation(NegYAxis).up, NegZAxis)

    def testStr(self):
        self.assertEqual(str(Orientation(XAxis, up=YAxis)),
            'Orientation(Vec3(1, 0, 0), up=Vec3(0, 1, 0))')

    def testEqual(self):
        a = Orientation((0, 2, 3))
        self.assertTrue(a == Orientation((0, 2, 3)))
        self.assertFalse(a == Orientation((11, 2, 3)))
        self.assertFalse(a == Orientation((0, 2, 3), up=(0, -3, 2)))
        self.assertFalse(a == 123)

    def testNotEqual(self):
        a = Orientation((0, 2, 3))
        self.assertFalse(a != Orientation((0, 2, 3)))
        self.assertTrue(a != Orientation((11, 2, 3)))
        self.assertTrue(a != Orientation((0, 2, 3), up=(0, -3, 2)))
        self.assertTrue(a != 123)

    def testHash(self):
        a = Orientation((0, 2, 3))
        self.assertRaises(TypeError, lambda: hash(a))

    def testRoll(self):
        o = Orientation(ZAxis)
        o.roll(pi/2)
        self.assertEqual(o, Orientation(ZAxis, up=NegXAxis))

    def testYaw(self):
        o = Orientation(ZAxis)
        o.yaw(pi/2)
        self.assertEqual(o, Orientation(NegXAxis))

    def testPitch(self):
        o = Orientation(ZAxis)
        o.pitch(pi/2)
        self.assertEqual(o, Orientation(YAxis, up=NegZAxis))

    def testMatrix(self):
        o = Orientation((1, 2, 3))
        self.assertEqual(type(o.matrix), gl.GLfloat * 16)
        expected = [
            o.right.x,    o.right.y,    o.right.z,   0,
            o.up.x,       o.up.y,       o.up.z,      0,
           -o.forward.x, -o.forward.y, -o.forward.z, 0,
            0,            0,            0,           1,
        ]
        for a, e in zip(o.matrix, expected):
            self.assertAlmostEqual(a, e)


if __name__ == '__main__':
    main()

