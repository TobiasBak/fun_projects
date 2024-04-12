from Utils.CollisionUtils import CollisionObject


class Event:
    pass


class CollisionEvent(Event):
    def __init__(self, collision_object: CollisionObject):
        self.collision_object = collision_object
