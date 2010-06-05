
Aims
----

Background
----------

OpenGL has long had two modes of operation:

* Immediate mode, in which client code calls one or more OpenGL API functions
  for every vertex in a model

* Batched mode, in which arrays of vertices can be sent in a single API call.

Immediate mode has long been known to be slower, and as of OpenGL3 is now
being deprecated.

Batch mode's arrays can be loaded into graphics card RAM, so that
subsequent frames can be rendered without them needing to be touched by the
CPU, nor sent over the bus.

From Python, each function call to the OpenGL API incurs a ctypes overhead,
which makes the immediate mode slower still, and migration to batched mode
even more attractive.

Conclusion: Always use batched mode, no matter what.

A previous talk showed how to create and send such arrays of vertices to
OpenGL, using pyglet's Batch API, which is layered on top of pyglet's built-in
OpenGL bindings. (link to talk)

Alternatively, this batching can be done manually using ctypes and the OpenGL
API. This is a relatively common technique and is documented elsewhere, so
this talk doesn't describe how to do this, but instead covers some of the
interesting things that can be done on top of that:

* Use Python to algorithmically generate interesting geometry.
* Create vertex and fragment shaders for special effects and for performance.
* Create a very small compiled C inner-loop, for performance.
* Program design: Prefer composition over inheritance, great benefits result.

---

Generating geometry

DO USE indexed vertices when vertices are re-used in
multiple triangles with the exact same attributes (eg. same color, same
normal. This is normally the case in a mesh of vertices
which are used to model a curving surface. (eg. surface of a sphere.)
Alternatively, when every edge represents a seam (eg. on a cube or
similarly blocky shape) then every use of a vertex uses different normals.
If ever vertex attributes such as normals or colors differ from one use
of the position to the next, then unique vertices must be sent to GL.
Hence using indexed arrays is not appropriate.

Similarly, perfer interleaved arrays by default for performance.
However, if one array is changing but they others aren't (eg. the vertex
array, because the model is changing shape) then separate that data into
its own array. There is a second reason why you'd want to separate one of
the arrays out, but I can't recall what it is.

---

I made a good start on the code for the talk over the long weekend. Got a suitably 'Tron' looking 3D OpenGL demo running. Screenshot attached.

I made a simple Shape class which models the vertices and faces of an arbitrary 3D polygonal shape, and factory functions to produce instances of that such as 'cube', 'tetrahedron', etc. Then a 'Glyph' class converts a Shape into the ctypes arrays needed to be passed to OpenGL. Then I created a CompoundShape which just aggregates many Shapes, and used that to create a randomised cluster of cubes (9,000 at 60fps on my lappy) colored by their position in RGB space, which the camera zooms around and amongst.

Later, I'm hoping to expand on this by using CompoundShape to create a variety of algorithmically generated geometry, such as 3d Serpinski gaskets (only using extrusions instead of holes, since they are a simple aggregation of shapes.) Hopefully this will make a pleasing tetrahedral 'fractal snowflake'. I hope it will be relatively simple to create algorithms to decorate an existing Shape, such as adding bevels to the edges.

I added some very basic vertex and fragment shaders to it - so the pain of integrating those is done. Right now I am getting the shaders to perform lighting calculations on the geometry, which will require that my Glyph class start to generate surface normals for each vertex, too. Later on, a variety of snazzy shader effects would be nice to have, such as shaders for 'plastic shiny surface' or generated wood/stone/fuzz textures.

I'm excited to be using a 'composition instead of inheritance' technique for the visible objects in the game. Each entity in the world is a very bare-bones 'GameItem' instance, to which attributes like Position, Orientation, Shape, etc are added at runtime. Even aspects such as 'being the camera' is just another attribute which is attached at runtime to an otherwise anonymous gameitem instance, as is the 'wobblyorbit' movement aspect which is attached to the same instance. I'm extremely pleased with how neatly this has turned out. I hadn't planned on this being part of the talk, but it's worked out so well that I'm tempted to include it. Future 'sinister ducks'-like projects should definitely try this.

