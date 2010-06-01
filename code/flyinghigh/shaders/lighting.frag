varying vec3 normal;
varying vec3 light_direction;

void main()
{
	// Defining The Material Colors
	const vec4 ambient = vec4(0.1, 0.0, 0.0, 1.0);
	const vec4 diffuse = vec4(1.0, 0.0, 0.0, 1.0);

	// Scaling The Input Vector To Length 1
	vec3 norm_normal = normalize(normal);
	vec3 norm_light_direction = normalize(light_direction);

	// Calculating The Diffuse Term And Clamping It To [0;1]
	float diffuse = clamp(dot(norm_normal, norm_light_direction), 0.0, 1.0);

	// Calculating The Final Color
	gl_FragColor = ambient + diffuse_color * diffuse;
}

