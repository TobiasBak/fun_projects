from typing import Self
from pygame import Vector2

from Components.ComponentInterface import ComponentInterface
from Components.PosComponent import PosComponent
from World.CollisionObject import CollisionObject
from World.World import World


class CollisionComponent(ComponentInterface):
    """ Weight: 1 is default"""

    def __init__(self, owner_id: int, pos_component: PosComponent, weight: float, amount_of_collision_objects: int = 1,
                 offset: list[Vector2] = [Vector2(0, 0)]):
        # Properties
        self._owner_id: int = owner_id
        self._pos_component: PosComponent = pos_component
        self.amount_of_collision_objects: int = amount_of_collision_objects
        self.offset: list[Vector2] = offset
        self.weight: float = weight

        # Collision Objects
        self.collision_objects: list[CollisionObject] = []
        self._create_collision_objects()
        self._add_collision_objects_to_world()

    def update(self, dt: float):
        for collision_object in self.collision_objects:
            collision_object.update(self._pos_component.get_pos())

    def _create_collision_objects(self):
        for i in range(self.amount_of_collision_objects):
            self.collision_objects.append(
                CollisionObject(self._owner_id, self._pos_component.get_pos(), self.offset[i],
                                self._pos_component.get_size(), self.weight))

    def _add_collision_objects_to_world(self):
        for collision_object in self.collision_objects:
            World.get_world().add_collision_object(collision_object)

    def _get_colliding_distance(self, other_pos: Vector2, combined_radius: float) -> float:
        return self._pos_component.get_pos().distance_to(other_pos) - combined_radius

    def collides_with(self, other: Self) -> bool:
        if self == other:
            return False
        elif self is None or other is None:
            return False
        elif (self._pos_component.get_pos().distance_to(other.owner.get_position())) < (
                self._pos_component.get_size() + other.owner.get_radius()):
            return True
        return False
