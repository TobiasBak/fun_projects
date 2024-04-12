from Entity.EntityInterface import EntityInterface


class Event:
    pass


class CollisionEvent(Event):
    def __init__(self, e1: EntityInterface, e2: EntityInterface):
        self.e1 = e1
        self.e2 = e2
