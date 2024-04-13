from typing import Self, Callable

from pygame import Vector2


class CollisionObject:
    """ All entities and components can create CollisionObjects to check for collisions."""

    def __init__(self, owner_id: int, pos: Vector2, pos_offset: Vector2, radius: float, weight: float = 1):
        self.owner_id: int = owner_id
        self.pos: Vector2 = pos
        self.pos_offset: Vector2 = pos_offset
        self.radius: float = radius
        self.weight: float = weight
        print(f"CollisionObject: {self.owner_id} created at {self.pos} and offset {self.pos_offset}")

    def set_pos(self, pos):
        self.pos = pos

    def update(self, pos):
        self.pos = pos + self.pos_offset

    def draw(self, screen):
        pass

    def check_collision(self, other):
        if self.owner_id == other.owner_id:
            return True
        if self.pos.distance_to(other.pos) < self.radius + other.radius:
            return True
        return False

    def get_colliding_distance(self, other_pos, combined_radius):
        return self.pos.distance_to(other_pos) - combined_radius

    def __eq__(self, other: Self):
        return self.owner_id == other.owner_id and self.pos.x == other.pos.x and self.pos.y == other.pos.y and self.radius == other.radius

    def __hash__(self):
        return hash((self.owner_id, self.pos.x, self.pos.y, self.radius))

    def __str__(self):
        return f"CollisionObject: with owner {self.owner_id} at {self.pos}"

    def __repr__(self):
        return self.__str__()


class CollisionPair:
    def __init__(self, co1: CollisionObject, co2: CollisionObject):
        if co1.owner_id < co2.owner_id:
            self.co1 = co1
            self.co2 = co2
        else:
            self.co1 = co2
            self.co2 = co1

    def __eq__(self, other: Self):
        return self.co1 == other.co1 and self.co2 == other.co2

    def __hash__(self):
        return hash((self.co1, self.co2))
