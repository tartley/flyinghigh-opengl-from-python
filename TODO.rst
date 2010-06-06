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

--CURRENT--

Colors should be unsigned bytes, not floats. Is it faster? Turn off vsync to measure.

3d orientation of shapes

Create serpinski gasket (tetra)
Create serpinski gasket (cube)

REFACTOR
Color should perhaps not be part of a shape. Should be passed to
composite.add()? Then we could re-use same instance of Cube geometry
for every entry in a CubeCluster. Is that useful?
Simlarly, (Shape, color, offset, orientation) form some sort of quad
in regards to children of composite shapes. How should this be treated?

GEOMETRY
Processing of shapes:
    Add border to faces
    Bevel edges

User-controlled camera

Fake skybox geometry:
    tiny triangular stars
    a ground
    a spherical moon with rings

PERFORMANCE
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

PRESENTATION PHASE 1
Write first draft essay about procedural geometry
Find way to automate conversion of essays into slides (rst2s5?)
Write first draft essay about shaders
Write first draft essay about compiled inner loops
Section about 'composition instead of inheritance'?
Section about choosing to use indexed arrays of GL_TRIANGLES

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

