from enum import Enum, auto

from pygame import Vector2

from Components.ComponentFactory import DefaultLivingEntityComponentFactory
from Components.HealthBarComponent import HealthBarComponent
from Components.HealthComponent import HealthComponent
from Entity.Enemy import Enemy
from Entity.EnemyTypes import DefaultEnemyType
from Entity.AbstractEntity import AbstractEntity
from Entity.Player import Player
from consts import GAME_WIDTH, GAME_HEIGHT




class EntityFactory:
    def __init__(self):
        pass

    def create_entity(self, pos: Vector2) -> AbstractEntity | None:
        pass


class DefaultPlayerFactory(EntityFactory):
    def __init__(self):
        super().__init__()

    health: float = 100
    color: str = "black"
    size: float = 30
    speed: float = 300

    def create_entity(self, pos: Vector2 = Vector2(GAME_WIDTH / 2, GAME_HEIGHT / 2)) -> AbstractEntity:
        player = Player(self.color, pos, self.size, self.speed)
        DefaultLivingEntityComponentFactory().create_components(player)
        return player


class DefaultEnemyFactory(EntityFactory):
    def __init__(self):
        super().__init__()

    def create_entity(self, pos: Vector2) -> AbstractEntity | None:
        enemy_type = DefaultEnemyType
        enemy = Enemy(enemy_type.color, pos, enemy_type.radius, enemy_type.speed)
        DefaultLivingEntityComponentFactory(20).create_components(enemy)
        return enemy
