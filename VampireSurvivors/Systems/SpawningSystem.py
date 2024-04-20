import random

from pygame import Vector2

from Entity.EnemyTypes import DefaultEnemyType
from Entity.EntityFactory import EnemyFactory
from Systems.SystemInterface import SystemInterface
from World.World import World
from settings import GAME_WIDTH, GAME_HEIGHT, ENEMIES_TO_SPAWN

world = World.get_world()


class SpawningSystem(SystemInterface):
    def __init__(self):
        super().__init__()

    def update(self, dt: float):
        enemy_x = random.randint(0, GAME_WIDTH)
        enemy_y = random.randint(0, GAME_HEIGHT)
        if len(world.entities) <= ENEMIES_TO_SPAWN:
            enemy_factory = EnemyFactory(DefaultEnemyType, Vector2(enemy_x, enemy_y))
            enemy = enemy_factory.create_entity(Vector2(enemy_x, enemy_y))
            world.add_entity(enemy)
