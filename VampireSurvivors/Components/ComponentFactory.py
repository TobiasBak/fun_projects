from Components.HealthBarComponent import HealthBarComponent
from Components.HealthComponent import HealthComponent
from Entity.EntityInterface import EntityInterface


class ComponentFactory:
    def __init__(self):
        pass

    def create_components(self, owner: EntityInterface) -> None:
        pass


class DefaultLivingEntityComponentFactory(ComponentFactory):
    def __init__(self, health: float = 100):
        super().__init__()
        self.health = health

    def create_components(self, owner: EntityInterface) -> None:
        HealthComponent(owner, self.health)
        HealthBarComponent(owner)
