
* print some useful info to the console, to show users some progress during
  startup

* figure out how to keep bestiary behaviour same as now (press a key to
  toggle items in and out of world) but also include more complex groups
  of multiple shapes, such as the cluster of independent cube shapes that
  is currently added into world at startup as a performance test.

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


--DONE----------------------------------------------------------------------

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

