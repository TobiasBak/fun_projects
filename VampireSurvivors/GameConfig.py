from pygame import Vector2

from settings import GAME_HEIGHT, GAME_WIDTH


class GameConfig:
    """ Singleton class. Use get_game_config"""
    _instance = None

    def __init__(self):
        # Player settings
        self.PLAYER_START_POS = Vector2(GAME_WIDTH / 2, GAME_HEIGHT / 2)
        self.PLAYER_START_HEALTH = 100
        self.PLAYER_SPEED = 800
        self.PLAYER_SIZE = 30
        self.PLAYER_WEIGHT = 100


    @classmethod
    def get_gameconfig(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

