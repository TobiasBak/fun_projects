from Systems.CollisionDetectionSystem import CollisionDetectionSystem
from Systems.CollisionHandlerSystem import CollisionHandlerSystem
from Systems.InitialSystems import SpawningSystem
from Systems.SystemInterface import SystemInterface

from World.World import World


class SystemFactory:
    def __init__(self):
        self.systems: list[SystemInterface] = []

    def create_and_add_systems(self) -> None:
        self._populate_systems()
        world = World.get_world()
        for system in self.systems:
            world.add_system(system)

    def _populate_systems(self) -> None:
        pass


class InitialSystems(SystemFactory):
    def __init__(self):
        super().__init__()

    def _populate_systems(self) -> None:
        self.systems.append(SpawningSystem())
        self.systems.append(CollisionDetectionSystem())
        self.systems.append(CollisionHandlerSystem())
