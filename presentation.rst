
Flying High: Hobbyist OpenGL from Python
========================================

Jonathan Hartley


Inspiratons
-----------

As the field of computer graphics advances, there is an understandable tendency
to strive for photorealism, This is laudable and inevitable, but I also feel
that the effort expended on achieving this technical goal is often undertaken
without considering whether photorealism is the best aesthetic choice for a
particular project.

In the past, games and other applications were non-photorealistic by neccesity.
This resulted in a set of distinctive visual styles.

TODO, get images.

* Rez
* Tron (with 'bit')

Modern projects which pro-actively choose a designed aesthetic style, whether
in emulation of a retro look, or striking out in a new direction of their own,
are often more distinctive, artistically succesful and memorable than any
project which merely strives for photorealism. Programs like these are my
inspiration.

* Love
* AAAaaaAAAaaAAAA
* RunJesusRun
* that FPS that is black and white with red bits
* Demoscene

The demoscene in particular is relevant to this talk, because one of my other
inspirations has been to create pretty geometry just for the sake of it. As a
sculptor might put it, exploring the nature of space.


Performance
-----------

Python might be considered to be the antithesis of the demoscene, which has a
reputation for requiring hardcore C skills and tortured micro-optimisations.
Python generally runs about 100x slower than C.

This isn't as crippling as you might expect, especially if you stick to jobs
for which you can hand a lot of the grunt work off to the GPU. Additionally,
I'm a big believer in the idea that algorithm choice is far moe important for
performance than language choice. Even for problems as trivial as finding
primes, the optimal algorithm is far from obvious. My resultant belief is that
for non-trivial problems (i.e. real-world problems, as opposed to
straightforward number crunching benchmarks), given the same amount of
development time, Python can hold its own against C. Only when everyone is
using an optimal algorithm, i.e. when *much* effort has been expended
refining the algorithm for a well-understood problem, does C's runtime
performance start to nose ahead.

All of the examples we'll see in this talk run at 60fps on my 2005-era laptop
with rubbish graphics hardware (ATI Radeon X1400.)


Starting Point
--------------

I'm assuming we're starting with a simple, vanilla OpenGL application, that
will:

* open a window
* provide an OpenGL context
* set an appropriate 3D projection matrix
* call our 'World.update()' every frame
* call our 'Render.draw(world)' after that

I'm using pyglet for this, but this would work equally well from pygame, or
simply with PyOpenGL along with some utility library to create the window and
context.

Whichever framework or library you use, this minimal application takes about
100 lines or so. This results in a blank screen, redrawn at 60fps.

The idea of this talk is that I will show (or at least mention) *all* of the
code you need to add on top of this minimal canonical OpenGL loop. I want to
demonstrate that producing pretty graphis like this can be done with a
surprisingly small amount of code, and is quite easy. I want you to leave here
enthused to generate your own virtual sculptures and animations, or graphics
engines for games.


Modelling Polyhedra
-------------------

Where a Polyhedron is a 3D shape with flat faces and straight edges.

We can model this using a simple class::

    class Shape(object):
        '''
        model a polyhedron
        '''
        def __init__(self, vertices, faces, face_colors):
            self.vertices = vertices
            self.faces = faces
            self.face_colors = face_colors

Vertices is a list of (x, y, z) named tuples.
Each face is a list of indices into the vertex list.
Each face has a corresponding color, as (r, g, b, a) tuples.

A simple example is a geometry consisting of a triangle joined to a square::

        RED = (255, 0, 0, 255)
        YELLOW = (255, 255, 0, 255)
        shape = Shape(
            vertices=[
                ( 1,  1,   0), # v0
                ( 1, -1,   0), # v1
                (-1, -1,   0), # v2
                (-1   1,   0), # v3
                ( 1,  0.5, 1), # v4
            ],
            faces=[ [0, 1, 4], [0, 1, 2, 3], ],
            face_colors=[RED, YELLOW],
        )

TODO: diagram of wireframe


OpenGL Arrays
-------------

A Shape can be converted into the ctype arrays that OpenGL needs.

I'm going to use indexed arrays of GL_TRIANGLES throughout, which is a good
default choice for all-round performance, and keeps things simple.

Firstly, we need to generate the array of vertex positions.

* TODO Diagram of our tetrahedron and opengl arrays: vertices, colors

    wireframe, showing vertices but not faces

    vertices = [ v0, v1, v2, v3, v4, ]
    faces = [ [0, 1, 4], [0, 1, 2, 3], ]
    ->
    verttype = GLfloat * 12
    glvertices = verttype( v0, v1, v4, v0, v1, v2, v3, )

This array contains GLfloats, and here we see a common ctypes idiom for
creating the type of this array: The actual type is obtained by multiplying
GLfloat by the length of the array.

For the contents of this array, the glvertices have been recreated by
dereferencing the indices in the shape's faces, to produce the sequence of
vertices in the order in which OpenGL should draw them. Note that this
introduces redundant vertex positions - for example v0 now occurs twice in
glvertices. This is necessary whenever a vertex attribute differs from one use
of a vertex to the next. In this case, the color of v0 differs depending on
whether it is used in the square or the triangle.

Later we will see that even if the colors were the same, the redundant vertex
position is still necessary, because other attributes of the vertex, such as
the vertex normal, will still differ.

In short, don't worry about these redundant vertex positions, they are required
and there is nothing you can do about them.

That was a lot of talk, but the code is really small::

    def glarray(datatype, data, length):
        gltype = datatype * length
        return gltype(*data)

    class Glyph(object):

        def get_glvertices(self, shape, num_glverts):
            glverts = chain.from_iterable(
                shape.vertices[index]
                for face in shape.faces
                for index in face
            )
            return glarray(GLfloat, chain(*glverts), num_glverts * 4)

        def from_shape(self, shape):
            num_glverts = sum(len(face) for face in shape.faces)
            self.glverts = self.get_glverts(shape, num_glverts)

So a Glyph class converts our Shape instance into some arrays that OpenGL can
draw.

For performance, we send our vertex array to OpenGL as an *indexed* array.

    TODO: opengl api diagram:
        draw contiguous vertex array
        vs
        draw indexed vertex array
    
This reduces the number of vertices needed in the vertex array, and can help
help the GPU cache the results of vertex processing, speeding things up
when the same vertex is re-used for adjacent triangles (which will happen
about often, as we are about to see).

So we need to generate the array of indices.

(Or glindices will need to be GLushort or GLuint for longer vertex arrays.)


    wireframe, showing vertices and faces

    vertices = [ v0, v1, v2, v3, v4, ]
    faces = [ [0, 1, 4], [0, 1, 2, 3], ]
    ->
    indextype = GLubyte
    glindices = indextype( 0, 1, 4,  0, 1, 2,  2, 0, 3 )
                           -------   -----------------
                          triangle    square, triangulated




Shape Factories
---------------

Factory functions can return instances of Shape. e.g. Tetrahedron::

    def Tetrahedron(edge, face_colors):
        size = edge / sqrt(2)/2
        vertices = [
            (+size, +size, +size), # v0
            (-size, -size, +size), # v1
            (-size, +size, -size), # v2
            (+size, -size, -size), # v3
        ]
        faces = [ [0, 2, 1], [1, 3, 0], [2, 3, 1], [0, 3, 2] ]
        return Shape(vertices, faces, face_colors)

TODO: diagram of wireframe tetra
    
TODO: a bunch of different shapes: cube, platonic solids, elite ships

Using Shaders
--------------



Compiled inner loops
--------------------



