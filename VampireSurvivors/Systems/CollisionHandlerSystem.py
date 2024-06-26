from Components.CollisionComponent import CollisionComponent
from Components.PosComponent import PosComponent
from Entity.EntityInterface import EntityType
from Entity.Bullet import Bullet
from Events.EventManager import EventManager
from Events.Events import CollisionEvent, AttackEvent
from Systems.SystemInterface import SystemInterface
from World.CollisionObject import CollisionObject
from World.World import World


class CollisionHandlerSystem(SystemInterface):
    def __init__(self):
        EventManager.get_instance().add_listener(CollisionEvent, self._handle_collision)
        self.world = World.get_world()

    def update(self, dt: float):
        pass

    def _handle_collision(self, collision_event: CollisionEvent):
        collision_pair = collision_event.collision_pairs
        self._handle_collision_pair(collision_pair)

    def _handle_collision_pair(self, collision_pair):
        co1 = collision_pair.co1
        co2 = collision_pair.co2
        co1_owner = World.get_world().get_entity_by_id(co1.owner_id)
        co2_owner = World.get_world().get_entity_by_id(co2.owner_id)

        match (co1_owner.get_type(), co2_owner.get_type()):
            # If the owners are a Player and an Enemy
            case (EntityType.PLAYER, EntityType.ENEMY):
                self.handle_movement_circles(co1, co2, co1_owner, co2_owner)
            # If the owners are both Enemies
            case (EntityType.ENEMY, EntityType.ENEMY):
                self.handle_movement_circles(co1, co2, co1_owner, co2_owner)
            # If The owners are enemy and bullet
            case (EntityType.ENEMY, EntityType.BULLET):
                # print(f"{co1_owner} collided with {co2_owner}")
                enemy = co1_owner
                bullet: Bullet = co2_owner
                if bullet.get_if_entity_should_be_attacked(enemy):
                    self.event_manager.dispatch_event(AttackEvent(enemy, bullet.damage))

    def handle_movement_circles(self, co1: CollisionObject, co2: CollisionObject, co1_owner, co2_owner):
        o2_o1 = co1.pos - co2.pos
        dist2 = o2_o1.x ** 2 + o2_o1.y ** 2
        dist = dist2 ** 0.5
        summed_radius = co1.radius + co2.radius

        delta = 1.0 * 0.5 * (summed_radius - dist)  # I got no clue what this does
        move_vector = (o2_o1 / dist) * delta

        # Calculate weight ratios
        total_weight = co1.weight + co2.weight
        weight_ratio1 = co2.weight / total_weight
        weight_ratio2 = co1.weight / total_weight

        co1_pos_component: PosComponent = co1_owner.get_component(PosComponent)
        co2_pos_component: PosComponent = co2_owner.get_component(PosComponent)

        co1_pos_component.move(move_vector * weight_ratio1)
        co2_pos_component.move(-move_vector * weight_ratio2)

        co1_collision_component = co1_owner.get_component(CollisionComponent)
        co2_collision_component = co2_owner.get_component(CollisionComponent)

        co1_collision_component.update(0.0)
        co2_collision_component.update(0.0)
