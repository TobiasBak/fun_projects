
from Events.Events import CollisionEvent
from Systems.SystemInterface import SystemInterface
from Utils.CollisionUtils import get_collision_component, get_move_distance_on_collision


class CollisionHandlerSystem(SystemInterface):
    def __init__(self):
        super().__init__()
        self.event_manager.add_listener(CollisionEvent, self._handle_collision)

    def update(self, dt: float):
        pass

    def _handle_collision(self, collision_event: CollisionEvent):
        co1 = collision_event.collision_pair.co1
        co2 = collision_event.collision_pair.co2

        cc1 = get_collision_component(co1)
        cc2 = get_collision_component(co2)

        co1_owner = cc1.owner
        co2_owner = cc2.owner

        match co1_owner, co2_owner:
            # If the owners are a Player and an Enemy
            case (Player, Enemy):
                Player.move(get_move_distance_on_collision(co1, co2))
                Enemy.move(get_move_distance_on_collision(co2, co1))




