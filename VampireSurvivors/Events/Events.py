from Components.ComponentInterface import ComponentInterface
from Entity.EntityInterface import EntityInterface
from Utils.BulletUtils import DefaultBulletConfig
from World.CollisionObject import CollisionPair


class Event:
    pass


class CollisionEvent(Event):
    def __init__(self, collision_pair: CollisionPair):
        self.collision_pair = collision_pair


class AttackEvent(Event):
    def __init__(self, target: EntityInterface, damage: float):
        self.target = target
        self.damage = damage


class BulletEvent(Event):
    def __init__(self, source: ComponentInterface, bullet_config: DefaultBulletConfig):
        print("BulletEvent")
        self.source = source
        self.bullet_config = bullet_config
