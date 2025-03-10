#version 460 core
out vec4 color;

uniform ivec2 resolution;
uniform samplerCube skybox;

vec2 fragCoord = gl_FragCoord.xy;

#define INFTY 1E9
#define EPS   1E-3

#define COLOR_RED   0
#define COLOR_GREEN 1
#define COLOR_BLUE  2

#define LAYOUT std430

struct Node {
    float weight;
    float height;
};

layout (LAYOUT, binding = 0) buffer NodeBuffer {
    Node nodes[];
};

int index1d(ivec2 coords) {
    return coords.y * resolution.x + coords.x;
}

ivec2 index2d(int i) {
    return ivec2(i % resolution.x, i / resolution.x);
}

float getColor(ivec2 coords) {
    return abs(nodes[index1d(coords)].height);
}

void step(float delta_t) {
    return;
}

void main() {
    fragCoord -= resolution / 2;
    float d = max(resolution.x, resolution.y);
    vec2 uv = fragCoord / d;
    float tempColor = getColor(ivec2(uv * resolution));
    color = vec4(tempColor, tempColor, tempColor, 1);
}
