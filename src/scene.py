import typing
from graphics import LogicProvider, ShaderProgram

from OpenGL.GL import *
from pyglm import glm
from struct import pack, unpack

from buffers import Buffers
import config


class Converter:
    @staticmethod
    def to_int(data):
        if data is None:
            return 0
        if isinstance(data, int):
            return data
        if isinstance(data, float):
            data = pack('f', data)
            return unpack('i', data)[0]
        if isinstance(data, bool):
            return float(data)

        raise NotImplementedError()

    @staticmethod
    def to_glm_array(arr):
        arr = [Converter.to_int(item) for item in arr]
        return glm.array(glm.int32, *arr)


class LoadableObject:
    def __init__(self):
        pass

    def as_array(self):
        raise NotImplementedError()


class Vector(LoadableObject):
    def __init__(self, x, y, z):
        super().__init__()
        self.x = x
        self.y = y
        self.z = z

    @typing.override
    def as_array(self):
        return [self.x, self.y, self.z, None]


class Color(Vector):
    def __init__(self, red, green, blue):
        super().__init__(red, green, blue)

    @property
    def red(self):
        return self.x

    @property
    def green(self):
        return self.y

    @property
    def blue(self):
        return self.z


class GraphicalPrimitive(LoadableObject):
    def __init__(self):
        super().__init__()


class Node(GraphicalPrimitive):
    def __init__(self, weight: float, height: float, velocity: float, blocked: bool):
        super().__init__()
        self.weight = weight
        self.height = height
        self.velocity = velocity
        self.blocked = blocked

    @typing.override
    def as_array(self):
        return [self.weight, self.height, self.velocity, self.blocked]


class SceneLoader(LogicProvider):
    def __init__(self, shader_program: ShaderProgram):
        super().__init__()
        self.shader = shader_program
        self.__initialized = False

    @typing.final
    def render(self):
        if not self.__initialized:
            self.__initialize()
            self.__initialized = True

        super().render()

    def __initialize(self):
        nodes = self.spawn_nodes()
        self.__load_SSBO(nodes, Buffers.NODES.value)

    def __load_SSBO(self, data, index):
        if len(data) == 0:
            return

        data = SceneLoader.to_glm_array(data)
        size = len(data) * 4
        ssbo = glGenBuffers(1)
        glBindBuffer(GL_SHADER_STORAGE_BUFFER, ssbo)
        glBufferData(GL_SHADER_STORAGE_BUFFER, size, None, GL_STATIC_DRAW)
        glBufferSubData(GL_SHADER_STORAGE_BUFFER, 0, size, data.ptr)
        glBindBufferBase(GL_SHADER_STORAGE_BUFFER, index, ssbo)

    def spawn_nodes(self):
       amount = config.RESOLUTION[0] * config.RESOLUTION[1]
       nodes = []
       for i in range(amount):
            x = i % config.RESOLUTION[0]
            y = i // config.RESOLUTION[0]
            nodes.append(self.get_node(x, y))
       return nodes

    def get_node(self, x, y):
        raise NotImplementedError()

    @staticmethod
    def to_glm_array(data: list[LoadableObject]):
        if len(data) == 0:
            return None

        arr = []

        for i in data:
            arr += i.as_array()

        return Converter.to_glm_array(arr)
