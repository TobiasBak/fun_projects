from Components.CollisionComponent import CollisionComponent
from Events.Events import CollisionEvent
from Systems.InitialSystems import world
from Systems.SystemInterface import SystemInterface
from Utils.CollisionUtils import CollisionObject, get_collisions


class CollisionDetectionSystem(SystemInterface):
    def __init__(self):
        super().__init__()

    def update(self, dt: float):
        entities = world.entities

        collisions: set[CollisionObject] = get_collisions(entities)

        for collision_object in collisions:
            self.event_manager.dispatch_event(CollisionEvent(collision_object))

