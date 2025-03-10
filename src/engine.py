import sys

import pygame
from pygame.locals import *
from graphics import Renderer
import config
import platform
import os


class Engine:
    def __init__(self):
        if platform.system() == "Linux":
            os.environ["SDL_VIDEO_X11_FORCE_EGL"] = "1"
        pygame.init()
        pygame.display.set_mode(config.RESOLUTION, DOUBLEBUF | OPENGL)
        pygame.display.set_caption('Real Engine')

    def run(self, renderer: Renderer):
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            renderer.render()
            pygame.display.flip()
            clock.tick(config.FPS)
