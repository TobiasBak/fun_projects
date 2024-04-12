import weakref

from pygame import Surface, SurfaceType


class ComponentInterface:
    def __init__(self, owner):
        self.owner_ref = weakref.ref(owner)
        self.owner.add_component(self)

    @property
    def owner(self):
        return self.owner_ref()

    def update(self, dt: float):
        pass

    def render(self, screen: Surface | SurfaceType):
        pass

    def remove(self):
        if self.owner is not None:
            self.owner.remove_component(self.__class__)

    def __str__(self):
        return self.__class__.__name__
