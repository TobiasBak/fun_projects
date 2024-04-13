
from pygame import Surface, SurfaceType

from Components.ComponentInterface import ComponentInterface
from Entity.EntityInterface import EntityInterface
from Events.EventManager import EventManager


class AbstractComponent(ComponentInterface):
    def __init__(self, owner):
        self.event_manager: EventManager = EventManager().get_instance()
        self.owner: EntityInterface = owner
        self.owner.add_component(self)

    def update(self, dt: float):
        pass

    def render(self, screen: Surface | SurfaceType):
        pass

    def clean_up(self):
        if self.owner is not None:
            self.owner.remove_component(self.__class__)

    def get_owner_id(self) -> id:
        return self.owner.id

    def get_pos(self):
        return self.owner.get_position()

    def __str__(self):
        return self.__class__.__name__
