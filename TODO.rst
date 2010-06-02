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

--CURRENT--

SHADERS
combine fragment color and texture, see:
    http://www.lighthouse3d.com/opengl/glsl/index.php?textureComb

Automatically calculate normals
    Faces of a shape come in two flavours. A flat shape, composed of a
    coplanar ring of vertices describing its edge. Or curved surfaces,
    in which vertices with fixed normals, colors, etc, are re-used by more
    than one triangle. A single shape may be a composite of both such faces
    (eg. a ring with a curved outer and inner surface, but flat top and
    bottom.)

    The glyph should take note of this
    flag when generating arrays. The decision affects both whether indices
    are generated, and the state of other arrays. Vertex positions need to be
    duplicated, with different normals. Length of color array will change
    similarly. Might be two different glyph classes.

    Also, the Render system should take note of this. For flat faces, use
    glDrawArrays (contiguous arrays), and for curved surfaces, use
    glDrawElements (indexed arrays).

REFACTOR
    color should not be part of a shape. Should be passed to composite.add()?
    then we can re-use the same Cube instance within a CubeCluster
    CompositeShapes should be nestable
    use generators for compositeShape properties
    use generators when creating glyph


GEOMETRY
generate normals. This implies expanding number of vertices (one copy per
face it participates in) and ditching indices

SHADERS: multiple colored lights

INNER LOOP PHASE 1
Compile it in C.
Measure performance.

PRESENTATION PHASE 1
Write first draft essay about procedural geometry
Find way to automate conversion of essays into slides (rst2s5?)
Write first draft essay about shaders
Write first draft essay about compiled inner loops
Section about 'composition instead of inheritance'?

REFACTOR
    color generators. SolidColor, Gradient.
    try glBlendFunc(GL_ONE_MINUS_SRC_ALPHA)

REFACTOR: opengl3
    Convert to using vertex buffer objects, if they are available, but do
    not rely on them. Then we should get improved performance on newer hardware
    but fall back to client side arrays on older hardware.

    Review Mike's 'canonical opengl3 application', from his old pycon talk.

GEOMETRY PHASE 2
Cube cluster generated from pixels of small bitmaps. Invader! Mario! etc.
Cube cluster with borders on the cubes: general method to add borders 2 shapes
Automatically triangulate *concave* faces (needs glu triangulate code)
Add to the geometry while it is being displayed
Generic 'modify geometry' while it is being displayed.

REFACTOR
Consider sharing cube geometry between many gameitems (check out huge startup
cost of creating all those cube glyphs. Oh, they can't share color arrays.
But can they share vertex and index arrays and normals?

SHADERS PHASE 2
Allow each entity to specify its own shaders.
Attach and detach shader programs during the render.

INNER LOOP PHASE 2
?

PRESENTATION PHASE 2
Refine

--OPTIONAL--

GEOMETRY PHASE 3
Create clump of radial sphere segments
Several different clumps of radial sphere segments, all co-centered,
    with differing rates (axes?) of rotation
Create serpinski gasket (dodec)
Create serpinski gasket (cube)
City buildings
One of each, in the same scene.

SHADERS PHASE 3
Add single texture

SKYBOX
Add a real one

