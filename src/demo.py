from scene import *
import config


class ExampleSceneLoader(SceneLoader):
    def __init__(self, shader_program: ShaderProgram):
        super().__init__(shader_program)

    @typing.override
    def spawn_nodes(self):
        amount = config.PHYSICAL_RESOLUTION[0] * config.PHYSICAL_RESOLUTION[1]
        return [Node(1, i / amount) for i in range(amount)]
