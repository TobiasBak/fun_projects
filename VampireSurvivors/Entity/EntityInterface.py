from pygame import Vector2

from Components.ComponentInterface import ComponentInterface
from Utils.RandomUtils import get_new_id


class EntityInterface:
    def __init__(self):
        self.id: int = get_new_id()

    def update(self, dt: float) -> None:
        pass

    def render(self, screen) -> None:
        pass

    def get_component(self, component_name: ComponentInterface.__class__):
        pass

    def add_component(self, component: ComponentInterface) -> None:
        pass

    def remove_component(self, component_name: ComponentInterface.__class__) -> None:
        pass

    def get_position(self) -> Vector2:
        pass

    def set_position(self, position: Vector2) -> None:
        pass

    def get_radius(self) -> float:
        pass

    def set_radius(self, size: float) -> None:
        pass

    def get_speed(self) -> float:
        pass

    def set_speed(self, speed: float) -> None:
        pass

    def move(self, distance: Vector2):
        pass

    def __str__(self):
        pass

    def __repr__(self):
        pass
