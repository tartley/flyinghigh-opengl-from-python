try:
    # Python 2.6 with unittest2 installed
    from unittest2 import TestCase, main
except:
    # Python 2.7
    from unittest import TestCase, main


from ...geometry.geometry import Geometry


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

