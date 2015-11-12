
uniform sampler2D texture;

void main()
{
    vec4 texel;
    vec3 rgb;

    texel = texture2D(texture, gl_TexCoord[0].st);
    rgb = mix(gl_Color.rgb, texel.rgb, texel.a);
    gl_FragColor = vec4(rgb, gl_Color.a);
}

