
The source code in this directory is an exploration of the ideas for a talk
about using OpenGL from Python.

From the 'code' directory::

    python -O run.py [--profile]


DEPENDENCIES:

    Python 2.6
    Pyglet
    PyOpenGL

For development, I'm also using:

    unittest2
    nose

running tests using 'nosetests' (unittest2 discovery has some wrinkles)

For profiling, I'm using the standard library cProfile, with this to render
the output graphically:

    RunSnakeRun
    # runsnake must be installed either using:
    #   easy_install RunSnakeRun SquareMap
    # or download from here:
    #   http://www.vrplumber.com/programming/runsnakerun/
    # also needs wxPython, from here:
    #   http://www.wxpython.org/download.php#binaries


DESIGN NOTES

The hub of the design is the 'engine.GameLoop' class, which contains the
main game loop and responds to pyglet window events such as update and
draw.

Every item that exists in the 3D space (visible objects, and the
camera) is represented by an instance of the minimal 'engine.GameItem' class.

The engine.World class maintains a collection of these GameItem instances.

The top-level 'populate_world.py' module creates all the intances of GameItem,
and passes them to world.add().

The engine.Render class is used by the window draw handler, to render the
contents of the world. If the GameItem has a 'glyph' attribute, then that
object is expected to provide OpenGL arrays suitable for passing to 
glDrawElements.

The code is organised in a 'prefer composition to inheritance' kind of
design. GameItem itself does little more than assign each instance a unique
ID, used as the key in World's collection if GameItems. Instances of GameItem
are then assigned arbitrary attributes at runtime. Generally the value of these
attributes are instances of the classes defined in the 'components'
sub-package, eg. gameitem.glyph is set to an instance of component.Glyph.
GameItems with this attribute are rendered by engine.Render. Those without it
(eg. the camera) are not rendered.

Currently, all glyph attribute values are derived directly from the gameitem's
'shape' attribute. The Glyph class does this conversion itself. It is
instructed to do so by 'world.add()', which knows that any gameitem with a
shape attribute should have a corresponding 'glyph' attribute added, so that it
can be rendered.

Other components that may be attached to gameitems as attributes include
spinners and movers, that move or reorient their parent gameitem. For
example, the camera gameitem has a 'mover' attribute, which is an instance
of component.WobblyOrbit. This is responsible for the camera movement.

I ended up accidentally creating my own hand-rolled vec3 class, which I
acknowledge is dumb.


PERFORMANCE

As with all pyglet projects, it's important to run with -O. Makes a big
difference to performance.

run.py recognises a '--profile' command line param, which runs the program
with profiling turned on. On exit, it then fires up
RunSnakeRun on the resulting output, to view the profiling info graphically.

Currently runs under Windows at 60fps on my modest 2005-era Thinkpad laptop
(with ATI Radeon X1400). I just fired it up under Linux and got disappointing
20fps. Haven't looked at why, but in the past similar code has tended to run
faster under Linux on my hardware, so hopefully this is something easily
fixable. 

