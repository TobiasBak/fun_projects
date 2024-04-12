from Components.ComponentInterface import ComponentInterface
from Entity.EntityInterface import EntityInterface


class HealthComponent(ComponentInterface):
    def __init__(self, entity: EntityInterface, health):
        super().__init__(entity)
        self.health = health

    def get_health(self) -> float:
        return self.health

    def set_health(self, health: float) -> None:
        self.health = health

