from Events.Events import CollisionEvent
from Systems.SpawningSystem import world
from Systems.SystemInterface import SystemInterface
from Utils.CollisionUtils import get_collisions
from World.CollisionObject import CollisionPair


class CollisionDetectionSystem(SystemInterface):
    def __init__(self):
        super().__init__()

    def update(self, dt: float):
        collision_objects = world.get_collision_objects()

        collisions: set[CollisionPair] = get_collisions(collision_objects)

        for pair in collisions:
            self.event_manager.dispatch_event(CollisionEvent(pair))
