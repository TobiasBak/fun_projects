from Entity.Enemy import Enemy
from Entity.Player import Player
from Entity.Bullet import Bullet
from Events.Events import CollisionEvent, AttackEvent
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

        # If one of the entities have died and the collision is still being processed
        if cc1 is None or cc2 is None:
            return

        co1_owner = cc1.owner
        co2_owner = cc2.owner


        match co1_owner, co2_owner:
            # If the owners are a Player and an Enemy
            case (Player(), Enemy()):
                move_distance = get_move_distance_on_collision(co1, co2)
                co1_owner.move(move_distance)
                co2_owner.move(-move_distance)
            # If the owners are both Enemies
            case (Enemy(), Enemy()):
                move_distance = get_move_distance_on_collision(co1, co2)
                co1_owner.move(move_distance)
                co2_owner.move(-move_distance)
            # If The owners are enemy and bullet
            case (Enemy(), Bullet()):
                # print(f"{co1_owner} collided with {co2_owner}")
                enemy = co1_owner
                bullet: Bullet = co2_owner
                if bullet.get_if_entity_should_be_attacked(enemy):
                    self.event_manager.dispatch_event(AttackEvent(enemy, bullet.damage))












