--CURRENT--
Create minimal 3d gameloop application, with cube

REFACTOR
camera needs splitting into two things:
    setter of projections, knows width, height, gets told zoom
    maintainer of camera x, y, zoom, setter of modelview

GEOMETRY PHASE 1
Create a cube.
Create a quick clump of interpenetrating cubes.

Have object rotate

SHADERS PHASE 1
Integrate shaders:
    std vertex
    pixel shader uses vertex colors, with per-pixel lighting.

INNER LOOP PHASE 1
Compile it in C.
Measure performance.

PRESENTATION PHASE 1
Write first draft essay about procedural geometry
Write first draft essay about shaders
Write first draft essay about compiled inner loops
Find way to automate conversion of essays into slides (rst2s5?)

GEOMETRY PHASE 2
clump of cuboids: Remove faces that are totally embedded.
Add to the geometry while it is being displayed

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

