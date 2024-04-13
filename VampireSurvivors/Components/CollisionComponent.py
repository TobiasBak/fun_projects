from typing import Self
from pygame import Vector2
from Components.AbstractComponent import AbstractComponent
from Entity.EntityInterface import EntityInterface
from World.CollisionObject import CollisionObject
from World.World import World


class CollisionComponent(AbstractComponent):
    def __init__(self, owner: EntityInterface, radius, weight, amount_of_collision_objects: int = 1,
                 offset=None):
        super().__init__(owner)

        # Properties
        if offset is None:
            offset = [Vector2(0, 0)]
        if offset is None:
            offset = list(Vector2(0, 0))
        self.id: int = owner.id
        self.amount_of_collision_objects: int = amount_of_collision_objects
        self.offset: list[Vector2] = offset
        self.radius: float = radius
        self.weight: float = weight

        # Collision Objects
        self.collision_objects: list[CollisionObject] = []
        self._create_collision_objects()
        self._add_collision_objects_to_world()


    def update(self, dt: float):
        for collision_object in self.collision_objects:
            collision_object.update(self.owner.get_position())

    def render(self, screen):
        pass

    def clean_up(self):
        super().clean_up()
        World.get_world().remove_all_collision_objects_for_entity(self.owner.id)

    def _create_collision_objects(self):
        for i in range(self.amount_of_collision_objects):
            self.collision_objects.append(
                CollisionObject(self.owner.id, self.owner.get_position(), self.offset[i], self.radius, self.weight))

    def _add_collision_objects_to_world(self):
        for collision_object in self.collision_objects:
            World.get_world().add_collision_object(collision_object)

    def _get_colliding_distance(self, other_pos: Vector2, combined_radius: float) -> float:
        return self.owner.get_position().distance_to(other_pos) - combined_radius

    def collides_with(self, other: Self) -> bool:
        if self == other:
            return False
        elif self is None or other is None:
            return False
        elif (self.owner.get_position().distance_to(other.owner.get_position())) < (
                self.owner.get_radius() + other.owner.get_radius()):
            return True
        return False
