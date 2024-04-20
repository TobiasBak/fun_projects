
from pygame import Vector2

from Components.ComponentFactory import BulletEntityComponentFactory, EnemyComponentFactory, \
    PlayerComponentFactory
from Entity.Bullet import Bullet
from Entity.EnemyTypes import EnemyType
from Entity.Entity import Entity
from Entity.EntityInterface import EntityInterface
from GameConfig import GameConfig
from Utils.BulletUtils import DefaultBulletConfig
from settings import GAME_WIDTH, GAME_HEIGHT


class EntityFactory:
    def create_entity(self, pos: Vector2) -> EntityInterface:
        pass


class PlayerFactory(EntityFactory):
    game_config = GameConfig.get_gameconfig()

    def create_entity(self, pos: Vector2 = Vector2(GAME_WIDTH / 2, GAME_HEIGHT / 2)) -> EntityInterface:
        player = Entity()
        list_of_components = PlayerComponentFactory().create_components()
        player.add_list_of_components(list_of_components)
        return player


class EnemyFactory(EntityFactory):
    def __init__(self, enemy_config: EnemyType, pos: Vector2):
        self.enemy_config = enemy_config
        self.pos = pos

    def create_entity(self, pos: Vector2) -> EntityInterface:
        enemy = Entity()
        list_of_components = EnemyComponentFactory(self.enemy_config, pos).create_components()
        enemy.add_list_of_components(list_of_components)
        return enemy


class BulletFactory(EntityFactory):
    def __init__(self, bullet_config: DefaultBulletConfig):
        super().__init__()
        self.bullet_config = bullet_config

    def create_entity(self, position: Vector2) -> EntityInterface:
        bullet = Bullet(self.bullet_config.color, position, self.bullet_config.damage, self.bullet_config.speed,
                        self.bullet_config.radius, self.bullet_config.lifetime)
        BulletEntityComponentFactory().create_components(bullet)
        return bullet
