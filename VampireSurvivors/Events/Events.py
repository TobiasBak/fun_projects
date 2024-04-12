from Entity.AbstractEntity import AbstractEntity


class Event:
    pass


class CollisionEvent(Event):
    def __init__(self, e1: AbstractEntity, e2: AbstractEntity):
        self.e1 = e1
        self.e2 = e2
