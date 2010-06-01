
varying vec3 normal;
varying vec3 light_direction;

void main()
{
	gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;

    
	// normal = gl_NormalMatrix * gl_Normal; 
    normal = vec3(1, 0, 0)

	// direction to light source
	vec4 vertex_in_modelview = gl_ModelViewMatrx * gl_Vertex;
	light_direction = vec3(gl_LightSource[0].position – vertex_in_modelview);
}

