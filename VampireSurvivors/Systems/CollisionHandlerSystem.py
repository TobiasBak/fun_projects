from pygame import Vector2

from Components.PosComponent import PosComponent
from Entity.EntityInterface import EntityType
from Entity.Bullet import Bullet
from Events.EventManager import EventManager
from Events.Events import CollisionEvent, AttackEvent, FindCollisionEvent
from Systems.SystemInterface import SystemInterface
from Utils.CollisionUtils import get_move_distance_on_collision
from World.World import World


class CollisionHandlerSystem(SystemInterface):
    def __init__(self):
        EventManager.get_instance().add_listener(CollisionEvent, self._handle_collision)

    def update(self, dt: float):
        pass

    def _handle_collision(self, collision_event: CollisionEvent):
        collision_pairs = collision_event.collision_pairs

        for collision_pair in collision_pairs:
            self._handle_collision_pair(collision_pair)

        # EventManager.get_instance().dispatch_event(FindCollisionEvent(World.get_world().get_collision_objects()))

    def _handle_collision_pair(self, collision_pair):
        co1 = collision_pair.co1
        co2 = collision_pair.co2
        co1_owner = World.get_world().get_entity_by_id(co1.owner_id)
        co2_owner = World.get_world().get_entity_by_id(co2.owner_id)
        co1_pos_component: PosComponent = co1_owner.get_component(PosComponent)
        co2_pos_component: PosComponent = co2_owner.get_component(PosComponent)

        match co1_owner.get_type(), co2_owner.get_type():
            # If the owners are a Player and an Enemy
            case (EntityType.PLAYER, EntityType.ENEMY):
                move_distance = get_move_distance_on_collision(co1, co2)
                actual_move_distance = self.adjust_move_distance_based_on_min_distance(move_distance)
                print(f"Moving entities: {actual_move_distance}")
                co1_pos_component.move(actual_move_distance[0])
                co2_pos_component.move(-actual_move_distance[1])
                print(f"Entities collided: {co1_owner} and {co2_owner}")
            # If the owners are both Enemies
            case (EntityType.ENEMY, EntityType.ENEMY):
                move_distance = get_move_distance_on_collision(co1, co2)
                actual_move_distance = self.adjust_move_distance_based_on_min_distance(move_distance)
                co1_pos_component.move(actual_move_distance[0])
                co2_pos_component.move(-actual_move_distance[1])
            # If The owners are enemy and bullet
            case (EntityType.ENEMY, EntityType.BULLET):
                # print(f"{co1_owner} collided with {co2_owner}")
                enemy = co1_owner
                bullet: Bullet = co2_owner
                if bullet.get_if_entity_should_be_attacked(enemy):
                    self.event_manager.dispatch_event(AttackEvent(enemy, bullet.damage))

    def adjust_move_distance_based_on_min_distance(self, move_distance: [Vector2, Vector2]) -> [Vector2, Vector2]:
        minimum_positive_move_distance = 0.2
        minimum_negative_move_distance = -0.2
        if move_distance[0].x < 0 and move_distance[0].x > minimum_negative_move_distance:
            move_distance[0].x = minimum_negative_move_distance
        if move_distance[0].y < 0 and move_distance[0].y > minimum_negative_move_distance:
            move_distance[0].y = minimum_negative_move_distance
        if move_distance[0].x > 0 and move_distance[0].x < minimum_positive_move_distance:
            move_distance[0].x = minimum_positive_move_distance
        if move_distance[0].y > 0 and move_distance[0].y < minimum_positive_move_distance:
            move_distance[0].y = minimum_positive_move_distance

        if move_distance[1].x > 0 and move_distance[1].x < minimum_positive_move_distance:
            move_distance[1].x = minimum_positive_move_distance
        if move_distance[1].y > 0 and move_distance[1].y < minimum_positive_move_distance:
            move_distance[1].y = minimum_positive_move_distance
        if move_distance[1].x < 0 and move_distance[1].x > minimum_negative_move_distance:
            move_distance[1].x = minimum_negative_move_distance
        if move_distance[1].y < 0 and move_distance[1].y > minimum_negative_move_distance:
            move_distance[1].y = minimum_negative_move_distance
        return move_distance
