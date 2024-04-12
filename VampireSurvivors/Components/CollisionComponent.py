import math
from typing import Self

from pygame import Vector2

from Components.AbstractComponent import AbstractComponent


class CollisionComponent(AbstractComponent):
    def __init__(self, owner, pos, radius, weight, move_able: bool = True, entities_should_move: bool = True):
        super().__init__(owner)
        self.id = owner.id
        self.pos: Vector2 = pos
        self.radius = radius
        self.weight = weight
        self.move_able = move_able
        self.entities_should_move = entities_should_move

    def update(self, dt: float):
        self.pos = self.owner.get_position()

    def render(self, screen):
        pass

    def handle_collision(self, other: Self) -> None:
        self._move_on_collision(other)

    def _move_on_collision(self, other: Self) -> None:
        if not self.move_able:
            return
        # Calculate direction vector between the centers of the two objects
        direction_x = self.pos.x - other.pos.x
        direction_y = self.pos.y - other.pos.y

        # Calculate distance between centers of the two objects
        distance = math.sqrt(direction_x ** 2 + direction_y ** 2)

        # Normalize direction vector
        if distance != 0:
            direction_x /= distance
            direction_y /= distance

        # Calculate the total weight of the entities
        total_weight = self.weight + other.weight

        # Calculate the ratio of weights
        weight_ratio1 = other.weight / total_weight
        separation_distance = self._get_colliding_distance(other.pos, self.radius + other.radius)

        # Calculate displacement vectors for each object
        displacement_x = direction_x * separation_distance
        displacement_y = direction_y * separation_distance

        move_distance: Vector2 = -Vector2(displacement_x * weight_ratio1, displacement_y * weight_ratio1)
        print(f"Moving {self.owner.id} by {move_distance}")
        self.owner.move(move_distance)

    def _get_colliding_distance(self, other_pos: Vector2, combined_radius: float) -> float:
        return self.pos.distance_to(other_pos) - combined_radius

    def collides_with(self, other: Self) -> bool:
        if self == other:
            return False
        elif self is None or other is None:
            return False
        elif (self.owner.get_position().distance_to(other.owner.get_position())) < (self.owner.get_radius() + other.owner.get_radius()):
            return True
        return False
