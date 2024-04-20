import pygame

from settings import GAME_WIDTH, GAME_HEIGHT

_screen = None


def get_screen():
    global _screen

    if _screen is None:
        _screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))

    return _screen
