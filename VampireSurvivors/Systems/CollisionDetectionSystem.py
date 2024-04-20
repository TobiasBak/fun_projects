from Events.EventManager import EventManager
from Events.Events import CollisionEvent, FindCollisionEvent
from Systems.SystemInterface import SystemInterface
from World.CollisionObject import CollisionPair
from World.World import World


class CollisionDetectionSystem(SystemInterface):
    def __init__(self):
        EventManager.get_instance().add_listener(FindCollisionEvent, self._find_collisions)

    def update(self, dt: float):
        EventManager.get_instance().dispatch_event(FindCollisionEvent(World.get_world().get_collision_objects()))

    def _find_collisions(self, event: FindCollisionEvent):
        collisions: set[CollisionPair] = set()
        collision_objects = event.collision_objects

        for collision_object in collision_objects:
            for other in collision_objects:
                if collision_object != other and collision_object.collides_with(other):
                    collisions.add(CollisionPair(collision_object, other))

        if collisions:
            print(f"Collisions: {collisions}")
            EventManager.get_instance().dispatch_event(CollisionEvent(collisions))
