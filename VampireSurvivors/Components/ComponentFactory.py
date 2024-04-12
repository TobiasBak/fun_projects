from Components.HealthBarComponent import HealthBarComponent
from Components.HealthComponent import HealthComponent
from Entity.EntityInterface import EntityInterface


class ComponentFactory:
    def __init__(self):
        pass

    def create_components(self, owner: EntityInterface) -> None:
        pass


class DefaultLivingEntityComponentFactory(ComponentFactory):
    def __init__(self):
        super().__init__()

    def create_components(self, owner: EntityInterface) -> None:
        print("Creating default living entity components for entity", owner)
        HealthComponent(owner)
        HealthBarComponent(owner)
