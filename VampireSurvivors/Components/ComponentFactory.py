from Components.HealthBarComponent import HealthBarComponent
from Components.HealthComponent import HealthComponent
from Entity.AbstractEntity import AbstractEntity


class ComponentFactory:
    def __init__(self):
        pass

    def create_components(self, owner: AbstractEntity) -> None:
        pass


class DefaultLivingEntityComponentFactory(ComponentFactory):
    def __init__(self, health: float = 100):
        super().__init__()
        self.health = health

    def create_components(self, owner: AbstractEntity) -> None:
        HealthComponent(owner, self.health)
        HealthBarComponent(owner)
