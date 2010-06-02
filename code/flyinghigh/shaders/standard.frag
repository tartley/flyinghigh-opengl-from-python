
uniform sampler2D texture;

void main()
{
    vec4 texel;

    texel = texture2D(texture, gl_TexCoord[0].st);

    gl_FragColor = gl_Color;
}

