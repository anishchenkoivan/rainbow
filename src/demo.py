from scene import *
import config


class ExampleSceneLoader(SceneLoader):
    def __init__(self, shader_program: ShaderProgram):
        super().__init__(shader_program)

    @typing.override
    def spawn_nodes(self):
        amount = config.RESOLUTION[0] * config.RESOLUTION[1]
        return [Node(1.0, i / amount, 0.0) for i in range(amount)]
