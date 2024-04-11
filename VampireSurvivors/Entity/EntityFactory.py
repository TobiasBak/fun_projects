from enum import Enum, auto

from pygame import Vector2

from Entity.Enemy import Enemy
from Entity.EnemyTypes import DefaultEnemyType
from Entity.EntityInterface import EntityInterface
from Entity.Player import Player
from consts import GAME_WIDTH, GAME_HEIGHT


class Enemies(Enum):
    ENEMY = auto()


class EntityFactory:
    def __init__(self):
        pass

    def create_entity(self, pos: Vector2) -> EntityInterface | None:
        pass


class DefaultPlayerFactory(EntityFactory):
    def __init__(self):
        super().__init__()

    health: float = 100
    color: str = "black"
    size: float = 30
    speed: float = 200

    def create_entity(self, pos: Vector2 = Vector2(GAME_WIDTH / 2, GAME_HEIGHT / 2)) -> EntityInterface:
        player = Player(self.health, self.color, pos, self.size, self.speed)
        return player


class DefaultEnemyFactory(EntityFactory):
    def __init__(self):
        super().__init__()

    def create_entity(self, pos: Vector2) -> EntityInterface | None:
        enemy_type = DefaultEnemyType
        return Enemy(enemy_type.health, enemy_type.color, pos, enemy_type.size, enemy_type.speed)

