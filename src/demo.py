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


class TransitionSceneLoader(SceneLoader):
    def __init__(self, shader_program: ShaderProgram):
        super().__init__(shader_program)

    @typing.override
    def get_node(self, x, y):
        centre_x = config.RESOLUTION[0] // 2
        centre_y = config.RESOLUTION[1] // 2
        r = min(config.RESOLUTION) / 5

        if (x - centre_x) ** 2 + (y - centre_y)**2 <= r**2:
            return Node(5.0, 0.0, 0.0, False)

        return Node(1.0, 10.0 if x == 0 else 0, 0.0, False)
