
Aims
----

Background
----------

DO USE indexed vertices when vertices are re-used in
multiple triangles with the exact same attributes (eg. same color, same
normal. This is normally the case in a mesh of vertices
which are used to model a curving surface. (eg. surface of a sphere.)
Alternatively, when every edge represents a seam (eg. on a cube or
similarly blocky shape) then every use of a vertex uses different normals.
If ever vertex attributes such as normals or colors differ from one use
of the position to the next, then unique vertices must be sent to GL.
Hence using indexed arrays is less appropriate. But still worthwhile: Even
the most 'seamy' geometry, eg, a bunch of cubes, still re-uses some verts,
because each face needs drawing in two triangles, re-using two of the four
verts. Indices give 33% win in this case.

Similarly, perfer interleaved arrays by default for performance.
However, if one array is changing but they others aren't (eg. the vertex
array, because the model is changing shape) then separate that data into
its own array. There is a second reason why you'd want to separate one of
the arrays out, but I can't recall what it is.

