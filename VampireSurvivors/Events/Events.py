from Components.ComponentInterface import ComponentInterface
from Entity.EntityInterface import EntityInterface
from Utils.BulletUtils import DefaultBulletConfig
from World.CollisionObject import CollisionPair, CollisionObject


class Event:
    pass


class FindCollisionEvent(Event):
    def __init__(self, dt: float):
        self.dt: float = dt


class CollisionEvent(Event):
    def __init__(self, collision_pair: CollisionPair):
        self.collision_pairs: CollisionPair = collision_pair


class AttackEvent(Event):
    def __init__(self, target: EntityInterface, damage: float):
        self.target = target
        self.damage = damage


class BulletEvent(Event):
    def __init__(self, source: ComponentInterface, bullet_config: DefaultBulletConfig):
        self.source = source
        self.bullet_config = bullet_config
