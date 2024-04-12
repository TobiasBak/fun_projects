import math

from pygame import Vector2

from Components.CollisionComponent import CollisionComponent
from Entity.AbstractEntity import AbstractEntity


class CollisionObject:
    def __init__(self, co1: CollisionComponent, co2: CollisionComponent):
        if co1.id < co2.id:
            self.co1 = co1
            self.co2 = co2
        else:
            self.co1 = co2
            self.co2 = co1

    def __eq__(self, other):
        out = False
        if self.co1 == other.co1 and self.co2 == other.co2:
            out = True
        if self.co1 == other.co2 and self.co2 == other.co1:
            out = True
        return out

    def __hash__(self):
        return hash((self.co1, self.co2))

    def __str__(self):
        return f"CollisionObject between {self.co1} and {self.co2}"

    def __repr__(self):
        return self.__str__()


def entities_collide(e1: AbstractEntity, e2: AbstractEntity) -> bool:
    if e1 == e2:
        return False
    elif e1 is None or e2 is None:
        return False
    elif (e1.get_position().distance_to(e2.get_position())) < (e1.get_radius() + e2.get_radius()):
        return True

    return False


def get_collisions(entities: list[AbstractEntity]) -> set[CollisionObject]:
    """Returns a set of tuples containing colliding entities. (Currently n^2 runtime)"""
    collisions: set[CollisionObject] = set()
    collision_components: list[CollisionComponent] = get_collision_components(entities)

    for component in collision_components:
        if component is None:
            continue
        for o_component in collision_components:
            if o_component is None:
                continue
            if o_component.id == component.id:
                continue
            if component.collides_with(o_component):
                collisions.add(CollisionObject(component, o_component))

    return collisions


def get_collision_components(entities) -> list[CollisionComponent]:
    collision_components: list[CollisionComponent] = []
    for entity in entities:
        if entity is None:
            continue
        collision_component = entity.get_component(CollisionComponent)
        if collision_component is not None:
            collision_components.append(collision_component)
    return collision_components


def get_move_distance_on_collision(co1: CollisionComponent, co2: CollisionComponent) -> Vector2:
    # Calculate direction vector between the centers of the two objects
    direction_x = co2.x - co1.x
    direction_y = co2.y - co1.y

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
    separation_distance = get_colliding_distance(co1, co2)

    # Calculate displacement vectors for each object
    displacement_x = direction_x * separation_distance
    displacement_y = direction_y * separation_distance

    move_distance_co1: Vector2 = Vector2(displacement_x * weight_ratio1, displacement_y * weight_ratio1)
    return move_distance_co1
