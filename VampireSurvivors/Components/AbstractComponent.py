
from pygame import Surface, SurfaceType

from Entity.EntityInterface import EntityInterface


class AbstractComponent:
    def __init__(self, owner):
        self.owner: EntityInterface = owner
        self.owner.add_component(self)

    def update(self, dt: float):
        pass

    def render(self, screen: Surface | SurfaceType):
        pass

    def remove(self):
        if self.owner is not None:
            self.owner.remove_component(self.__class__)

    def __str__(self):
        return self.__class__.__name__
