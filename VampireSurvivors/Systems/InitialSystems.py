import random

from pygame import Vector2

from Entity.EntityFactory import DefaultEnemyFactory, Enemies
from Systems.SystemInterface import SystemInterface
from World.World import World
from consts import GAME_WIDTH, GAME_HEIGHT

world = World.get_world()


class SpawningSystem(SystemInterface):
    def __init__(self):
        super().__init__()

    def update(self, dt: float):
        enemy_x = random.randint(0, GAME_WIDTH)
        enemy_y = random.randint(0, GAME_HEIGHT)
        if len(world.entities) < 2:
            enemy_factory = DefaultEnemyFactory()
            enemy = enemy_factory.create_entity(Vector2(enemy_x, enemy_y))
            world.add_entity(enemy)

    def __str__(self):
        return "SpawningSystem"


class CleanEntitiesSystem(SystemInterface):
    def __init__(self):
        super().__init__()

    def update(self, dt: float):
        _world = World.get_world()
        for entity in _world.entities:
            if entity.get_health() <= 0:
                world.remove_entity(entity)

    def __str__(self):
        return "CleanEntitiesSystem"


class CollisionSystem(SystemInterface):
    def __init__(self):
        super().__init__()

    def update(self, dt: float):
        pass
        player = world.get_player()
        for entity in world.entities:
            if entity == player:
                continue

    def __str__(self):
        return "CollisionSystem"
