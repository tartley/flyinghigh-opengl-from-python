Create minimal 3d gameloop application, with cube

REFACTOR
camera needs splitting into two things:
    setter of projections, knows width, height, gets told zoom
    maintainer of camera x, y, zoom, setter of modelview

GEOMETRY PHASE 1
Create a cube.
Create a quick clump of interpenetrating cubes.

Have camera move

Automatically triangulate convex faces

construct composite geometry (eg. many cubes in a single glyph)

SHADERS PHASE 1
Integrate shaders:
    std vertex
    pixel shader uses vertex colors, with per-pixel lighting using normals

SHADERS
combine fragment color and texture, see:
    http://www.lighthouse3d.com/opengl/glsl/index.php?textureComb

GEOMETRY
generate normals. This implies expanding number of vertices (one copy per
face it participates in) and ditching indices

Automatically calculate normals for flat faces

Colors should be unsigned bytes, not floats.
Turn off vsync to measure, is it faster?
YES, 20fps faster.

3d orientation of GameItem's

Separate out new class Geometry, leaving Shape to manage geometry, color,
position and orientation (the latter two relative to its containing
MultiShape.) So now we can re-use same geometry instance (eg. Cube(1)) many
times in the same MultiShape.
CompositeShapes should be nestable.

3d orientation of shapes relative to their containing Multishape

Try using same Cube instance in populate world, to help startup performance
Convert orientation.matrix back to a property

Create serpinski gasket (tetra)

PERFORMANCE
try making Vec3 not inherit from tuple, giving it plain attributes x, y & z.
Adding slots. Give it an indexor to still allow access to v[0], v[1], v[2].
- Tried and reverted. This was 20% slower.

rename 'serpinski gasket' to 'koche tetrahedron'

Create koch cube

`CURRENT--------------------------------------------------------------------`

Why does spinner or orientation not work for sierpinskis?

print some useful info to the console, to show users some progress during
startup

Consider python 2.5 and 3.1 compatibility.

vec3 operations like add should work in-place, to remove overhead of
construction This implies vec3 is mutable, and shouldn't hash
Consider:
    'normalise()' (functional, returns new instance)
    'normalized()' (in-place, returns self)
Consider equivalent for other methods.

Try vec3d and matrix from:
    -euclid (looks ok, stolent one or two ideas)
    -planar (will need augmenting to make 3d)
    -numpy

GEOMETRIES
* Koch branch
* Comprise Koch iterations from different Shapes so each one can use
  separate color?
* Tetris shapes (unoptimised)
* Random symmetries of close-packed cube patterns
* regular solids
* Elite ships

Split geometry and shape out into separate modules

GEOMETRY
Processing of shapes:
    Add border to faces (requires face shrinking. um.)
    Bevel edges

User-controlled camera

Slomo should take a lambda as predicate to evaluate whether to activate
or not. Could then slow down on arbitrary conditions, such as two gameitems
colliding, rather than just on camera moving within region.

Fake skybox geometry:
    tiny triangular stars
    a ground
    - with mountains!
    a spherical moon
    - with rings!

PRESENTATION PHASE 1
Write first draft essay
    - like blog post, but with diagrams
Find way to automate conversion of essays into slides (rst2s5?)
    - include number of lines reqd for minimal funky app
    - section on composition instead of inheritance
    - section on shaders
    - section on algorithmic geometry

Are we currently sending all geometry across bus every frame?
try VBOs. but fall back to current method (vertex arrays) if hardware is crap

PRESENTATION
Write first draft essay about compiled inner loops

SHADERS:
attach lighsource to an in-world object, pass position in to vertex shader

GEOMETRY
Cube cluster generated from pixels of small bitmaps. Invader! Mario! etc.
Cube cluster presenting different images when viewed from different angles
    - really needs set of icons re-using same color pallette to work well

INNER LOOP PHASE 1
try out numpy vec3 and matrix classes. compare performance.
try psycho
try pyrex
try cython
try compiled C.
Measure performances.

GEOMETRY
Shape and Glyph should also handle curved surfaces. In these, vertices
will be re-used more often than in our current flat surfaces, because
all triangles adjacent to a vertex can re-use the exact same position,
normal, color, etc. Still used indexed arrays of GL_TRIANGLES though.

REFACTOR
  * use generators when creating glyph (if it is faster. Because it is a pain
    to debug them, hence not worth it if same speed)

SHADERS
    specular highlight
    colored lights
    multiple lights

REFACTOR
    color generators. SolidColor, Gradient.
    try glBlendFunc(GL_ONE_MINUS_SRC_ALPHA)

GEOMETRY
Add to the geometry while it is being displayed
    create big array up front. Just update final few verts in it as the
    shape grows.
'Squaresnake', as square extrudes, curve it left-right or up-down.

GEOMETRY
Automatically triangulate *concave* faces (needs glu triangulate code from
svgbatch)

REFACTOR
Review Mike's 'canonical opengl3 application', from his old pycon talk.

SHADERS PHASE 2
Allow each entity (entity's shape?) to specify its own shaders.
Attach and detach shaders from entities at runtime, using keyboard?

GEOMETRY PHASE 3
Create clump of radial sphere segments
Several different clumps of radial sphere segments, all co-centered,
    with differing rates (axes?) of rotation
One of each, in the same scene.

Create & move geometries with keyboard
Add spinners, movers with keyboard
Change shaders with keyboard

SHADERS PHASE 3
Add single texture

`Out of scope-----------------------------------------------------------------`

SKYBOX
Add a real one

Numpy integration
    possibly can generate geometry and glarrays really quickly with this?

