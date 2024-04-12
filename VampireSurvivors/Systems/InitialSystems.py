import math
import random

from pygame import Vector2

from Entity.EntityFactory import DefaultEnemyFactory
from Systems.SystemInterface import SystemInterface
from Utils.CollisionUtils import get_collisions, get_colliding_distance, CollisionObject
from World.World import World
from consts import GAME_WIDTH, GAME_HEIGHT, ENEMIES_TO_SPAWN

world = World.get_world()


class SpawningSystem(SystemInterface):
    def __init__(self):
        super().__init__()

    def update(self, dt: float):
        enemy_x = random.randint(0, GAME_WIDTH)
        enemy_y = random.randint(0, GAME_HEIGHT)
        if len(world.entities) <= ENEMIES_TO_SPAWN:
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
        entities = world.entities

        collisions: set[CollisionObject] = get_collisions(entities)

        for collision_object in collisions:
            e1 = collision_object.e1
            e2 = collision_object.e2

            # Calculate direction vector between the centers of the two objects
            direction_x = e2.position.x - e1.position.x
            direction_y = e2.position.y - e1.position.y

            # Calculate distance between centers of the two objects
            distance = math.sqrt(direction_x ** 2 + direction_y ** 2)

            # Normalize direction vector
            if distance != 0:
                direction_x /= distance
                direction_y /= distance

            # Calculate the total weight of the entities
            total_weight = e1.weight + e2.weight

            # Calculate the ratio of weights
            weight_ratio1 = e2.weight / total_weight
            weight_ratio2 = e1.weight / total_weight

            separation_distance = get_colliding_distance(e1, e2)

            # Calculate displacement vectors for each object
            displacement_x = direction_x * separation_distance
            displacement_y = direction_y * separation_distance

            e1.move(Vector2(displacement_x * weight_ratio1, displacement_y * weight_ratio1))
            e2.move(Vector2(-displacement_x * weight_ratio2, -displacement_y * weight_ratio2))

    def __str__(self):
        return "CollisionSystem"
