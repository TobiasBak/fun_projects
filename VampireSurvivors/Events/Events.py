from Entity.EntityInterface import EntityInterface
from World.CollisionObject import CollisionPair


class Event:
    pass


class CollisionEvent(Event):
    def __init__(self, collision_pair: CollisionPair):
        self.collision_pair = collision_pair


class AttackEvent(Event):
    def __init__(self, source: EntityInterface, target: EntityInterface, damage: float):
        self.source = source
        self.target = target
        self.damage = damage
