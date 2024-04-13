from pygame import Vector2

from Components.AbstractComponent import AbstractComponent
from Entity.EntityInterface import EntityInterface
from World.World import World


class AbstractEntity(EntityInterface):
    def __init__(self, color: str, position: Vector2, radius: float, speed: float, weight: float = 1.0):
        super().__init__()
        self.components = {}
        self.color: str = color
        self.position: Vector2 = position
        self.radius: float = radius
        self.speed: float = speed
        self.weight: float = weight

    def __eq__(self, other):
        position_threshold = 0.01  # Adjust this threshold as needed
        return self.id == other.id and \
            self.color == other.color and \
            abs(self.position.x - other.position.x) < position_threshold and \
            abs(self.position.y - other.position.y) < position_threshold and \
            self.radius == other.radius and self.speed == other.speed

    def __hash__(self):
        return hash((self.id, self.color, self.position.x, self.position.y, self.radius, self.speed))

    def update(self, dt: float) -> None:
        for component in self.components.values():
            component.update(dt)

    def render(self, screen) -> None:
        for component in self.components.values():
            component.render(screen)

    def get_component(self, component_name: AbstractComponent.__class__) -> AbstractComponent:
        return self.components.get(component_name, None)

    def add_component(self, component: AbstractComponent) -> None:
        self.components[component.__class__] = component

    def remove_component(self, component_name: AbstractComponent.__class__) -> None:
        self.components.pop(component_name, None)

    def get_position(self) -> Vector2:
        return self.position

    def set_position(self, position: Vector2) -> None:
        self.position = position

    def get_radius(self) -> float:
        return self.radius

    def set_radius(self, size: float) -> None:
        self.radius = size

    def get_speed(self) -> float:
        return self.speed

    def set_speed(self, speed: float) -> None:
        self.speed = speed

    def move(self, distance: Vector2):
        self.position += distance

    def clean_up(self):
        for component in self.components.values():
            component.clean_up()
        World.get_world().remove_entity(self)

    def __str__(self):
        return f"Entity with id {self.id} at {self.position} | type {type(self).__name__}"

    def __repr__(self):
        return self.__str__()
