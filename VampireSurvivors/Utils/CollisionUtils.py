import math

from pygame import Vector2

from Components.CollisionComponent import CollisionComponent
from Entity.AbstractEntity import AbstractEntity
from World.CollisionObject import CollisionPair, CollisionObject
from World.World import World


def get_collision_component(collision_object: CollisionObject) -> CollisionComponent:
    world = World.get_world()
    for entity in world.entities:
        if entity.id == collision_object.owner_id:
            return entity.get_component(CollisionComponent)
    return None


def entities_collide(e1: AbstractEntity, e2: AbstractEntity) -> bool:
    if e1 is None or e2 is None:
        return False

    if e1 == e2:
        return False

    e1_collision_objects = World.get_world().get_collision_objects_by_owner_id(e1.id)
    e2_collision_objects = World.get_world().get_collision_objects_by_owner_id(e2.id)

    for co1 in e1_collision_objects:
        for co2 in e2_collision_objects:
            if co1.check_collision(co2):
                return True

    return False


def get_collisions(collision_objects: list[CollisionObject]) -> set[CollisionPair]:
    """Returns a set of tuples containing colliding entities. (Currently n^2 runtime)"""
    collisions: set[CollisionPair] = set()
    collision_objects: list[CollisionObject]

    for collision_object in collision_objects:
        if collision_object is None:
            continue
        for collision_object_2 in collision_objects:
            if collision_object_2 is None:
                continue
            if collision_object.owner_id == collision_object_2.owner_id:
                continue
            if collision_object.check_collision(collision_object_2):
                collisions.add(CollisionPair(collision_object, collision_object_2))

    return collisions


def get_move_distance_on_collision(co1: CollisionObject, co2: CollisionObject) -> Vector2:
    # Calculate direction vector between the centers of the two objects
    direction_x = co2.pos.x - co1.pos.x
    direction_y = co2.pos.y - co1.pos.y

    # Calculate distance between centers of the two objects
    distance = math.sqrt(direction_x ** 2 + direction_y ** 2)

    # Normalize direction vector
    if distance != 0:
        direction_x /= distance
        direction_y /= distance

    # Calculate the total weight of the entities
    total_weight = co1.weight + co2.weight

    # Calculate the ratio of weights
    weight_ratio1 = co2.weight / total_weight
    separation_distance = co1.get_colliding_distance(co2.pos, co1.radius + co2.radius)

    # Calculate displacement vectors for each object
    displacement_x = direction_x * separation_distance
    displacement_y = direction_y * separation_distance

    move_distance_co1: Vector2 = Vector2(displacement_x * weight_ratio1, displacement_y * weight_ratio1)
    return move_distance_co1
