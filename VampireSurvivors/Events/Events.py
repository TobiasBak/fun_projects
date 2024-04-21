from Components.ComponentInterface import ComponentInterface
from Entity.EntityInterface import EntityInterface
from Utils.BulletUtils import DefaultBulletConfig
from World.CollisionObject import CollisionPair, CollisionObject


class Event:
    pass


class FindCollisionEvent(Event):
    def __init__(self, dt: float, collision_objects: list[CollisionObject]):
        self.dt: float = dt
        self.collision_objects = collision_objects


class CollisionEvent(Event):
    def __init__(self, dt:float, collision_pair: CollisionPair):
        self.dt: float = dt
        self.collision_pairs: CollisionPair = collision_pair


class AttackEvent(Event):
    def __init__(self, target: EntityInterface, damage: float):
        self.target = target
        self.damage = damage


class BulletEvent(Event):
    def __init__(self, source: ComponentInterface, bullet_config: DefaultBulletConfig):
        self.source = source
        self.bullet_config = bullet_config
