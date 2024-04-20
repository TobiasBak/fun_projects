
from pygame import Vector2

from Components.ComponentFactory import DefaultBulletEntityComponentFactory, \
    DefaultPlayerComponentFactory, DefaultEnemyComponentFactory

from Entity.Bullet import Bullet
from Entity.Enemy import Enemy
from Entity.EnemyTypes import DefaultEnemyType, EnemyType
from Entity.Entity import Entity
from Entity.EntityInterface import EntityInterface
from GameConfig import GameConfig
from Utils.BulletUtils import DefaultBulletConfig
from settings import GAME_WIDTH, GAME_HEIGHT


class EntityFactory:
    def create_entity(self, pos: Vector2) -> EntityInterface:
        pass


class DefaultPlayerFactory(EntityFactory):
    game_config = GameConfig.get_gameconfig()

    def create_entity(self, pos: Vector2 = Vector2(GAME_WIDTH / 2, GAME_HEIGHT / 2)) -> EntityInterface:
        player = Entity()
        list_of_components = DefaultPlayerComponentFactory().create_components()
        player.add_list_of_components(list_of_components)
        return player


class DefaultEnemyFactory(EntityFactory):
    def __init__(self, enemy_config: EnemyType):
        super().__init__()

    def create_entity(self, pos: Vector2) -> EntityInterface:
        enemy_type = DefaultEnemyType
        enemy = Enemy(enemy_type.color, pos, enemy_type.radius, enemy_type.speed)
        DefaultEnemyComponentFactory(20).create_components(enemy)
        return enemy


class BulletFactory(EntityFactory):
    def __init__(self, bullet_config: DefaultBulletConfig):
        super().__init__()
        self.bullet_config = bullet_config

    def create_entity(self, position: Vector2) -> EntityInterface:
        bullet = Bullet(self.bullet_config.color, position, self.bullet_config.damage, self.bullet_config.speed,
                        self.bullet_config.radius, self.bullet_config.lifetime)
        DefaultBulletEntityComponentFactory().create_components(bullet)
        return bullet
