from Events.EventManager import EventManager
from Events.Events import FindCollisionEvent, CollisionEvent
from Systems.SystemInterface import SystemInterface
from World.CollisionObject import CollisionPair
from World.World import World


class CollisionDetectionSystem(SystemInterface):
    def __init__(self):
        self._event_manager = EventManager.get_instance()
        self._event_manager.add_listener(FindCollisionEvent, self._find_collisions)

    def update(self, dt: float):
        self.update_with_sub_steps(dt, 8)

    def update_with_sub_steps(self, dt: float, sub_steps: int):
        sub_dt = dt / sub_steps
        for _ in range(sub_steps):
            self._event_manager.dispatch_event(FindCollisionEvent(sub_dt, World.get_world().get_collision_objects()))

    def _find_collisions(self, event: FindCollisionEvent):
        dt: float = event.dt
        collision_objects = event.collision_objects

        for collision_object in collision_objects:
            for other in collision_objects:
                if collision_object != other and collision_object.collides_with(other):
                    self._event_manager.dispatch_event(CollisionEvent(dt, CollisionPair(collision_object, other)))



