from typing import Self

from pygame import Surface, SurfaceType

from Entity.EntityInterface import EntityInterface
from Systems.SystemInterface import SystemInterface


class World(object):
    _instance: Self | None = None

    def __init__(self):
        self.entities: list[EntityInterface] = []
        self.systems: list[SystemInterface] = []
        self.player = None

    def add_entity(self, entity: EntityInterface):
        if entity is not None:
            self.entities.append(entity)

    def add_player(self, player: EntityInterface):
        self.player = player
        self.entities.append(player)

    def remove_entity(self, entity: EntityInterface):
        self.entities.remove(entity)

    def get_player(self):
        return self.player

    def add_system(self, system):
        self.systems.append(system)

    def update_entities(self, dt: float):
        for entity in self.entities:
            entity.update(dt)

    def update_systems(self, dt: float):
        for system in self.systems:
            system.update(dt)

    def update(self, dt: float):
        self.update_entities(dt)
        self.update_systems(dt)

    def render(self, screen: Surface | SurfaceType):
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
