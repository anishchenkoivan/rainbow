#version 460 core
out vec4 color;

uniform ivec2 resolution;
uniform samplerCube skybox;

vec2 fragCoord = gl_FragCoord.xy;

#define SPRING_COEFFICIENT 0.1
#define ENERGY_SAVING 0.99

#define INFTY 1E9
#define EPS   1E-3

#define COLOR_RED   0
#define COLOR_GREEN 1
#define COLOR_BLUE  2

#define LAYOUT std430

struct Node {
    float weight;
    float height;
    float velocity;
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

void step(float delta_t, ivec2 coords) {
    int i = index1d(coords);
    float sumHeight = 0;
    int counter = 0;
    if (coords.x > 0) {
        sumHeight += nodes[index1d(coords + ivec2(-1, 0))].height;
        counter++;
    }
    if (coords.x < resolution.x - 1) {
        sumHeight += nodes[index1d(coords + ivec2(1, 0))].height;
        counter++;
    }
    if (coords.y > 0) {
        sumHeight += nodes[index1d(coords + ivec2(0, -1))].height;
        counter++;
    }
    if (coords.y < resolution.y - 1) {
        sumHeight += nodes[index1d(coords + ivec2(0, 1))].height;
        counter++;
    }

    float averageHeight = sumHeight / counter;
    float acceleration = (averageHeight - nodes[i].height) * SPRING_COEFFICIENT;

    nodes[i].velocity = acceleration * (1 / nodes[i].weight) * delta_t;

    nodes[i].velocity *= ENERGY_SAVING;

    nodes[i].height += nodes[i].velocity * delta_t;
}

void main() {
    fragCoord -= resolution / 2;
    float d = max(resolution.x, resolution.y);
    vec2 uv = fragCoord / d;
    step(1/60, ivec2(uv * resolution));
    float tempColor = getColor(ivec2(uv * resolution));
    color = vec4(tempColor, tempColor, tempColor, 1);
}
