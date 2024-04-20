from typing import Self

from pygame import SurfaceType, Surface

from Entity.EntityInterface import EntityInterface
from Systems.SystemInterface import SystemInterface
from World.CollisionObject import CollisionObject


class World(object):
    _instance: Self | None = None

    def __init__(self):
        self.entities: list[EntityInterface] = []
        self.collision_objects: dict[int, set[CollisionObject]] = {}
        self.systems: list[SystemInterface] = []
        self.player = None

    def add_entity(self, entity: EntityInterface) -> None:
        if entity is not None:
            self.entities.append(entity)

    def remove_entity(self, entity: EntityInterface) -> None:
        if entity in self.entities:
            self.entities.remove(entity)

    def get_collision_objects(self) -> list[CollisionObject]:
        collision_objects: list[CollisionObject] = []
        for collision_object_set in self.collision_objects.values():
            collision_objects.extend(collision_object_set)
        return collision_objects

    def get_collision_objects_by_owner_id(self, owner_id: int) -> set[CollisionObject]:
        return self.collision_objects[owner_id]

    def add_collision_object(self, collision_object: CollisionObject) -> None:
        if collision_object.owner_id not in self.collision_objects:
            self.collision_objects[collision_object.owner_id] = set()

        self.collision_objects[collision_object.owner_id].add(collision_object)

    def remove_all_collision_objects_for_entity(self, id: int) -> None:
        self.collision_objects.pop(id)

    def add_player(self, player: EntityInterface) -> None:
        self.player = player
        self.entities.append(player)

    def get_player(self) -> EntityInterface | None:
        return self.player

    def add_system(self, system) -> None:
        self.systems.append(system)

    def update_entities(self, dt: float) -> None:
        for entity in self.entities:
            entity.update(dt)

    def update_systems(self, dt: float) -> None:
        for system in self.systems:
            system.update(dt)

    def update(self, dt: float) -> None:
        self.update_entities(dt)
        self.update_systems(dt)

    def __str__(self):
        return (f"---------- : World : ----------\n"
                f"Player: {str(self.player)}\n"
                f"Entities: {str(self.entities)}\n"
                f"Collision Objects: {str(self.collision_objects)}\n"
                f"Systems: {str(self.systems)}\n"
                f"-------------------------------")

    def __repr__(self):
        return self.__str__()

    @classmethod
    def get_world(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
