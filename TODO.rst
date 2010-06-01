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

REFACTOR
    color should not be part of a shape. Should be passed in to composite.add()?
    then we can re-use the same Cube instance within a CubeCluster
    Must CompositeShapes be nestable?
    use generators for compositeShape properties
    use generators when creating glyph

REFACTOR
    color generators. SolidColor, Gradient.
    try glBlendFunc(GL_ONE_MINUS_SRC_ALPHA)

GEOMETRY PHASE 1
generate normals. This implies expanding number of vertices (one copy per
face it participates in) and ditching indices (resulting indices would be
simply `xrange(num_verts)`.)

SHADERS: multiple colored lights

INNER LOOP PHASE 1
Compile it in C.
Measure performance.

PRESENTATION PHASE 1
Write first draft essay about procedural geometry
Write first draft essay about shaders
Write first draft essay about compiled inner loops
Find way to automate conversion of essays into slides (rst2s5?)

GEOMETRY PHASE 2
Automatically calculate normals
Cube cluster generated from pixels of small bitmaps. Invader! Mario! etc.
Cube cluster with borders on the cubes: general method to add borders 2 shapes
Automatically triangulate concave faces (needs glu triangulate code)
Add to the geometry while it is being displayed

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
Add one

