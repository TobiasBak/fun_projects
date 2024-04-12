import math

from pygame import Vector2

from Events.Events import CollisionEvent
from Systems.SystemInterface import SystemInterface
from Utils.CollisionUtils import get_colliding_distance


class CollisionHandlerSystem(SystemInterface):
    def __init__(self):
        super().__init__()
        self.event_manager.add_listener(CollisionEvent, self._handle_collision)

    def update(self, dt: float):
        pass

    def _handle_collision(self, collision_event: CollisionEvent):
        e1 = collision_event.e1
        e2 = collision_event.e2

        # Calculate direction vector between the centers of the two objects
        direction_x = e2.position.x - e1.position.x
        direction_y = e2.position.y - e1.position.y

        # Calculate distance between centers of the two objects
        distance = math.sqrt(direction_x ** 2 + direction_y ** 2)

        # Normalize direction vector
        if distance != 0:
            direction_x /= distance
            direction_y /= distance

        # Calculate the total weight of the entities
        total_weight = e1.weight + e2.weight

        # Calculate the ratio of weights
        weight_ratio1 = e2.weight / total_weight
        weight_ratio2 = e1.weight / total_weight

        separation_distance = get_colliding_distance(e1, e2)

        # Calculate displacement vectors for each object
        displacement_x = direction_x * separation_distance
        displacement_y = direction_y * separation_distance

        e1.move(Vector2(displacement_x * weight_ratio1, displacement_y * weight_ratio1))
        e2.move(Vector2(-displacement_x * weight_ratio2, -displacement_y * weight_ratio2))

    def __str__(self):
        return "CollisionHandlerSystem"
