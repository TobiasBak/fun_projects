from settings import GAME_HEIGHT, GAME_WIDTH


class GameConfig:
    """ Singleton class. Use get_game_config"""
    _instance = None

    def __init__(self):
        # Player settings
        self.PLAYER_SPEED = 200
        self.PLAYER_START_POS = Vector2(GAME_WIDTH / 2, GAME_HEIGHT / 2)

    @classmethod
    def get_gameconfig(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

