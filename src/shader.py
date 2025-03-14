from graphics import *
import config
import engine
from scene import *


def main(scene_loader):
    engine_instance = engine.Engine()
    vertex_shader = Shader("../shaders/render.vert")
    fragment_shader = Shader("../shaders/render.frag")
    shader = ShaderProgram(vertex_shader, fragment_shader)
    logic_provider = DefaultLogicProvider(shader, scene_loader)

    # Cube vertices (positions + colors)
    vertices = np.array([
        -1.0, -1.0,
        1.0, -1.0,
        1.0, 1.0,

        1.0, 1.0,
        -1.0, 1.0,
        -1.0, -1.0,
    ], dtype=np.float32)

    mesh = VerticesMesh(vertices)
    renderer = Renderer(shader, MeshGroup(mesh), logic_provider)
    engine_instance.run(renderer)


class DefaultLogicProvider(LogicProvider):
    def __init__(self, shader: ShaderProgram, scene_loader):
        super().__init__()
        self.shader = shader
        self.scene_loader = scene_loader(shader)

    def render(self):
        self.scene_loader.render()
        glUniform2i(glGetUniformLocation(self.shader.program, "resolution"), config.RESOLUTION[0], config.RESOLUTION[1])


class VerticesMesh(Mesh):
    def __init__(self, attribute: np.array):
        super().__init__(attribute)

    def setup_vao(self):
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, self.attribute, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 2 * 4, None)
        glEnableVertexAttribArray(0)

    def draw(self):
        glDrawArrays(GL_TRIANGLES, 0, 6)
