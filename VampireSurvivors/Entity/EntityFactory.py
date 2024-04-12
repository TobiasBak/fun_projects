from enum import Enum, auto

from pygame import Vector2

from Components.ComponentFactory import DefaultLivingEntityComponentFactory
from Components.HealthBarComponent import HealthBarComponent
from Components.HealthComponent import HealthComponent
from Entity.Enemy import Enemy
from Entity.EnemyTypes import DefaultEnemyType
from Entity.EntityInterface import EntityInterface
from Entity.Player import Player
from consts import GAME_WIDTH, GAME_HEIGHT

_default_entity_factory = DefaultLivingEntityComponentFactory()


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
    speed: float = 300

    def create_entity(self, pos: Vector2 = Vector2(GAME_WIDTH / 2, GAME_HEIGHT / 2)) -> EntityInterface:
        player = Player(self.color, pos, self.size, self.speed)
        _default_entity_factory.create_components(player)
        return player


class DefaultEnemyFactory(EntityFactory):
    def __init__(self):
        super().__init__()

    def create_entity(self, pos: Vector2) -> EntityInterface | None:
        enemy_type = DefaultEnemyType
        enemy = Enemy(enemy_type.color, pos, enemy_type.size, enemy_type.speed)
        _default_entity_factory.create_components(enemy)
        return enemy
