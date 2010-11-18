
Replace the (* seq) operator on initialising gl_array in Glyph.
instead use::
    array = arraytype()
    array[:] = seq # eg. [11, 22, 33... ]
Test the speed.

Shift from vertex arrays to vertex buffer objects::

    # Generate Buffers (inside Init method)
    circle = array(circle, dtype=float32)
    vertex_vbo = GL.GLuint(0)
    glGenBuffers(1, vertex_vbo)
    glBindBuffer(GL_ARRAY_BUFFER, circle)
    # wtc is 'ADT'? Array data type!
    glBufferData(GL_ARRAY_BUFFER, ADT.arrayByteCount(circle),
        ADT.voidDataPointer(circle), GL_STATIC_DRAW_ARB)

    # Draw buffers (inside Render method)
    glBindBuffer(GL_ARRAY_BUFFER, vertex_vbo)
    glVertexPointer(3, GL_FLOAT, 0, None)
    glDrawArrays(GL_LINE_STRIP, 0, circle.shape[0])

plus see this:
http://www.siafoo.net/snippet/185

Shift to interleaved VBO things.

* Do multiple gameitems with the same Shape all generate their own Glyph?

Review Mike's 'canonical opengl3 application', from his old pycon talk.
try OpenGL.FORWARD_COMPATIBLE_ONLY = True
see http://pyopengl.sourceforge.net/documentation/deprecations.html

* Cython: how much can we improve current?
  (450 independent position and oriented cubes at 60fps)
    - Cython glyph, vec3, orientation, etc, and their uses in Render.draw

 * I'm pretty sure I'm transforming every vertex for every child shape, at
   every step along the branches of each tree of MultiShapes. Can't we just
   transform the transforms, then do each vertex once?

GEOMETRIES
* the regular solids
* Tetris shapes (unoptimised)
* Random symmetries of close-packed cube patterns
* random combos of regular solids
* maze and pipe-like
* Cube cluster generated from pixels of small bitmaps. Invader! Mario! etc.

SHADERS, see
    http://swiftcoder.wordpress.com/2008/12/19/simple-glsl-wrapper-for-pyglet/

SHADERS, fancy
    * Add bitmaps to fragment shader, see:
        http://www.lighthouse3d.com/opengl/glsl/index.php?textureComb
    * noise
    * Allow each entity (entity's shape?) to specify its own shaders.

SHADERS, lighting:
    * Add mobile light source within world space
    * per-pixel lighting, calc normal for each pixel in fragment shader
    * pass in light position
    * attach light sources to a gameitem
    * colored light
    * pass in light color
    * pass in ambient light color
    * multiple light sources
    * specular highlights

GEOMETRY
Shape and Glyph should also handle curved surfaces. In these, vertices
will be re-used more often than in our current flat surfaces, because
all triangles adjacent to a vertex can re-use the exact same position,
normal, color, etc. Still used indexed arrays of GL_TRIANGLES though.
* Cylinder
* sphere
* Ring (hollow cylinder)
* donut
* ring with crosses in it
* multi-axis ring, with multi-axis cross

Startup performance:
    Look in profiler.
    Are we calling anything too often?
    Why all those str.__new__ calls?
    What if we modify vec3's in place?
    Try explicit loops rather than generators
    Can we pre-allocate storage in the output lists?
    Try generating gl arrays all in one loop
    TAKE startup code to Code Clinic! (* seq) on creating glarrays was 20% time

Add to geometry while it is being displayed
    * recreate it from scratch
    * colors too
    * modify or add to an existing geometry 'Squaresnake'

print some useful info to the console, to show users some progress during
startup

Refactorings:
 * multishape just stores matrices, rather than positions and orientations.
   Matrix generator near line 55/59 then becomes simple iteration over
   existing list.
 * multishape "child_offset += len(list(child.vertices))"
   is apparently faster than the quicker-looking current line
   Maybe this and other instances of counting verts could be skipped if a
   shape remembered it's num_verts?
 * Face object, which knows indices, color, normal.
 * cache normals, genreating them takes ages. Put in cache keyed by vertices
   and orientation, then subsequent calls for a different child shape, with
   different position, but same verts list and same orientation, will retrieve
   cache value
 * perform Glyph.from_verts using numpy

User-controlled camera

Fake skybox geometry:
    tiny triangular stars
    a ground
    with mountains!
    a spherical moon
    sky changes color, moon moves
    A sun!
    moon has rings!
    a real bitmap skybox thing
    a real bitmap with vectors overlaid

INNER LOOP PHASE 1
try out numpy vec3 and matrix classes. compare performance.
try psycho
try pyrex
try cython
try compiled C.
Measure performances.

Consider python 2.5 and 3.1 compatibility.

Try augmenting euclid to cython the types, as planar does

Try using numpy for vector / matrix math
    possibly can generate geometry and glarrays really quickly with this?

Automatically triangulate convex faces

`--DONE----------------------------------------------------------------------`

Create a quick clump of interpenetrating cubes.

Have camera move

construct composite geometry (eg. many cubes in a single glyph)

GEOMETRY
generate normals. This implies expanding number of vertices (one copy per
face it participates in) and ditching indices

Automatically calculate normals for flat faces

Colors should be unsigned bytes, not floats.
Turn off vsync to measure, is it faster?
YES, 20fps faster.

3d orientation of GameItems

Separate out new class Geometry, leaving Shape to manage geometry, color,
position and orientation (the latter two relative to its containing
MultiShape.) So now we can re-use same geometry instance (eg. Cube(1)) many
times in the same MultiShape.
CompositeShapes should be nestable.

3d orientation of shapes relative to their containing Multishape

Try using same Cube instance in populate world, to help startup performance
Convert orientation.matrix back to a property

SHADERS PHASE 1
Integrate shaders:
    std vertex
    pixel shader uses vertex colors, with directional lighting using normals

PERFORMANCE
try making Vec3 not inherit from tuple, giving it plain attributes x, y & z.
Adding slots. Give it an indexor to still allow access to v[0], v[1], v[2].
- Tried and reverted. This was 20% slower.

rename 'serpinski gasket' to 'koche tetrahedron'

Create koch cube

Integrate Oscar's sierpinski gaskets

Slomo should take a lambda as predicate to evaluate whether to activate
or not. Could then slow down on arbitrary conditions, such as two gameitems
colliding, rather than just on camera moving within region.

Separate colors for each face.

* Comprise Koch iterations from different Shapes so each one can use separate
  color?

upload refined description to site. Add content (images!) to wiki.

Write the first half of presentation.
    - plan on 1024x768 resolution
    - like blog post, but with diagrams
    - Find way to automate conversion of essays into slides (rst2s5?)
    - include number of lines reqd for minimal funky app
    - section on composition instead of inheritance
    - section on shaders
    - section on algorithmic geometry
    - section on shaders
    - put screenshots on the wiki

