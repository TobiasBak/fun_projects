
from pygame import Vector2

from Components.ComponentFactory import DefaultBulletEntityComponentFactory, \
    DefaultPlayerComponentFactory, DefaultEnemyComponentFactory

from Entity.Bullet import Bullet
from Entity.Enemy import Enemy
from Entity.EnemyTypes import DefaultEnemyType
from Entity.AbstractEntity import AbstractEntity
from Entity.Player import Player
from Utils.BulletUtils import DefaultBulletConfig
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
        DefaultPlayerComponentFactory().create_components(player)
        return player


class DefaultEnemyFactory(EntityFactory):
    def __init__(self):
        super().__init__()

    def create_entity(self, pos: Vector2) -> AbstractEntity | None:
        enemy_type = DefaultEnemyType
        enemy = Enemy(enemy_type.color, pos, enemy_type.radius, enemy_type.speed)
        DefaultEnemyComponentFactory(20).create_components(enemy)
        return enemy


class BulletFactory(EntityFactory):
    def __init__(self, bullet_config: DefaultBulletConfig):
        super().__init__()
        self.bullet_config = bullet_config

    def create_entity(self, position: Vector2) -> AbstractEntity:
        bullet = Bullet(self.bullet_config.color, position, self.bullet_config.damage, self.bullet_config.speed,
                        self.bullet_config.radius, self.bullet_config.lifetime)
        DefaultBulletEntityComponentFactory().create_components(bullet)
        return bullet
