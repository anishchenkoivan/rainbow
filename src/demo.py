from scene import *
import config


class ExampleSceneLoader(SceneLoader):
    def __init__(self, shader_program: ShaderProgram):
        super().__init__(shader_program)

    @typing.override
    def spawn_nodes(self):
        amount = config.RESOLUTION[0] * config.RESOLUTION[1]
        nodes = []
        for i in range(amount):
            x = i % config.RESOLUTION[0]
            y = i // config.RESOLUTION[0]
            border = x * y == 0 or x == config.RESOLUTION[0] - 1 or y == config.RESOLUTION[1] - 1
            nodes.append(Node(1.0, 0 if border else 0.5, 0.0, border))
        return nodes
