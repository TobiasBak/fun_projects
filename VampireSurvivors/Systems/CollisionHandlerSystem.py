
from Events.Events import CollisionEvent
from Systems.SystemInterface import SystemInterface


class CollisionHandlerSystem(SystemInterface):
    def __init__(self):
        super().__init__()
        self.event_manager.add_listener(CollisionEvent, self._handle_collision)

    def update(self, dt: float):
        pass

    def _handle_collision(self, collision_event: CollisionEvent):
        co1 = collision_event.collision_object.co1
        co2 = collision_event.collision_object.co2

        # Ensure that the collision objects should move
        if co1.entities_should_move is False or co2.entities_should_move is False:
            return
        print(f"Handling collision between {co1.id} and {co2.id}")
        co1.handle_collision(co2)
        co2.handle_collision(co1)


