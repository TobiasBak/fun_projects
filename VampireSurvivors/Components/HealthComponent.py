from Components.AbstractComponent import AbstractComponent
from Entity.AbstractEntity import AbstractEntity


class HealthComponent(AbstractComponent):
    def __init__(self, entity: AbstractEntity, health):
        super().__init__(entity)
        self.health = health

    def get_health(self) -> float:
        return self.health

    def set_health(self, health: float) -> None:
        self.health = health

