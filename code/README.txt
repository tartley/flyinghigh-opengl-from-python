
The source code in this directory is an exploration of the ideas for a talk
about using OpenGL from Python.

From the 'code' directory::

    python -O run.py [--profile]


DEPENDENCIES
------------

    Python 2.6 or 2.7
    Pyglet 1.1.4
    PyOpenGL 3.0.1
    numpy 1.5.0.dev8477 (just used for sierpinski generation)

I can't install numpy from source for Python2.7 (configuring distutils to use
the mingw32 compiler instead of Visual Studio doesn't work for me.) and there
are not yet numpy binaries published for Python2.7, so I'm using an unofficial
numpy binary from here:
http://www.lfd.uci.edu/~gohlke/pythonlibs/


DEVELOPMENT
-----------

For development, I'm also using:

    unittest2 (not reqd for Python2.7)
    nose

running tests using 'nosetests' (unittest2 discovery has some wrinkles)

Also I have some simple commands stored in a Makefile, which run under Linux or
under Windows with Cygwin binaries on the PATH. If you're on Windows but don't
have make or Cygwin, open up the Makefile and examine the targets. The commands
they run are generally dead simple and you can easily figure out how to do the
same thing on your system.


PROFILING
---------

For profiling, I'm using the standard library cProfile, with 3rd party tool
'RunSnakeRun' to render the output graphically.

    make profile

will run the script under the profiler, then run RunSnakeRun on the output.

RunSnakeRun is a graphical visualiser for the output of cProfile, very useful.
Installed using: ``easy_install RunSnakeRun`` (or pip) or download from:

 * http://www.vrplumber.com/programming/runsnakerun/

RunSnakeRun also needs:

 * SquareMap: ``easy_install SquareMap`` (or pip)
 * wxPython: from http://www.wxpython.org/download.php#binaries


DESIGN NOTES
------------

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
-----------

As with all pyglet projects, it's important to run with -O. Makes a big
difference to performance.

Biggest problem is converting Shapes to Glyphs, which causes a twenty
second pause on startup. Presumably numpy could fix this?

'make profile' runs the program with profiling turned on. On exit, it then
fires up RunSnakeRun on the resulting output, to view the profiling info
graphically.

Currently runs under Windows at 60fps on my modest 2005-era Thinkpad laptop
(with ATI Radeon X1400). I just fired it up under Linux and got disappointing
20fps. Haven't looked at why, but in the past similar code has tended to run
faster under Linux on my hardware, so hopefully this is something easily
fixable. 

