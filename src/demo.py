from scene import *
import config


class ExampleSceneLoader(SceneLoader):
    def __init__(self, shader_program: ShaderProgram):
        super().__init__(shader_program)

    @typing.override
    def get_node(self, x, y):
        border = x * \
            y == 0 or x == config.RESOLUTION[0] - \
            1 or y == config.RESOLUTION[1] - 1
        return Node(1.0, 0 if border else 0.5, 0.0, border)
