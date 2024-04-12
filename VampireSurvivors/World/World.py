from typing import Self

from pygame import Surface, SurfaceType

from Entity.AbstractEntity import AbstractEntity
from Systems.SystemInterface import SystemInterface
from Utils.CollisionUtils import CollisionObject


class World(object):
    _instance: Self | None = None

    def __init__(self):
        self.entities: list[AbstractEntity] = []
        self.collision_objects: list[CollisionObject] = []
        self.systems: list[SystemInterface] = []
        self.player = None

    def add_entity(self, entity: AbstractEntity) -> None:
        if entity is not None:
            self.entities.append(entity)

    def remove_entity(self, entity: AbstractEntity) -> None:
        self.entities.remove(entity)

    def get_collision_objects(self) -> list[CollisionObject]:
        return self.collision_objects

    def add_collision_object(self, collision_object: CollisionObject) -> None:
        self.collision_objects.append(collision_object)

    def remove_collision_object(self, collision_object: CollisionObject) -> None:
        self.collision_objects.remove(collision_object)

    def add_player(self, player: AbstractEntity) -> None:
        self.player = player
        self.entities.append(player)

    def get_player(self) -> AbstractEntity | None:
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

    def render(self, screen: Surface | SurfaceType) -> None:
        for entity in self.entities:
            entity.render(screen)

    def __str__(self):
        return (f"---------- : World : ----------\n"
                f"Entities: {str(self.entities)}\n"
                f"Systems: {str(self.systems)}\n"
                f"-------------------------------")

    def __repr__(self):
        return self.__str__()

    @classmethod
    def get_world(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
