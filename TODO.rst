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

3d orientation of shapes relative to their containing Multishape

Try using same Cube instance in populate world, to help startup performance

`CURRENT--------------------------------------------------------------------`

TIDY
Convert orientation.matrix back to a property
Split geometry and shape out into separate modules
Make baseless-tetrahedron a geometry factory function

Create serpinski gasket (tetra)
Create serpinski gasket (cube)

GEOMETRY
Processing of shapes:
    Add border to faces
    Bevel edges

User-controlled camera

Fake skybox geometry:
    tiny triangular stars
    a ground
    a spherical moon with rings

PRESENTATION PHASE 1
Write first draft essay about procedural geometry
Find way to automate conversion of essays into slides (rst2s5?)
Write first draft essay about shaders
Write first draft essay about compiled inner loops
Section about 'composition instead of inheritance'?
Section about choosing to use indexed arrays of GL_TRIANGLES

PERFORMANCE
If Vec3 creation is still bulk of startup time, try making Vec3 not inherit
from tuple, giving it plain attributes x, y & z. Adding slots. Give it an
indexor to still allow access to v[0], v[1], v[2].

Are we currently sending all geometry across bus every frame?
try VBOs. but fall back to current method (vertex arrays) if hardware is crap

SHADERS:
attach lighsource to an in-world object, pass position in to vertex shader

GEOMETRY
Cube cluster generated from pixels of small bitmaps. Invader! Mario! etc.

INNER LOOP PHASE 1
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
  * CompositeShapes should be nestable. Perhaps they are already.
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
Automatically triangulate *concave* faces (needs glu triangulate code)
Add to the geometry while it is being displayed

REFACTOR
Review Mike's 'canonical opengl3 application', from his old pycon talk.

SHADERS PHASE 2
Allow each entity (entity's shape?) to specify its own shaders.
Attach and detach shaders from entities at runtime, using keyboard?

GEOMETRY PHASE 3
Create clump of radial sphere segments
Several different clumps of radial sphere segments, all co-centered,
    with differing rates (axes?) of rotation
City buildings
One of each, in the same scene.

SHADERS PHASE 3
Add single texture

SKYBOX
Add a real one

