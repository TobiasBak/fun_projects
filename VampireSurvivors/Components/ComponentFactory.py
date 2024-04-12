from Components.HealthBarComponent import HealthBarComponent
from Components.HealthComponent import HealthComponent
from Components.WeaponCollisionComponent import CollisionWeaponComponent
from Entity.AbstractEntity import AbstractEntity


class ComponentFactory:
    def __init__(self):
        pass

    def create_components(self, owner: AbstractEntity) -> None:
        pass


class DefaultLivingEntityComponentFactory(ComponentFactory):
    def __init__(self, health: float = 100, damage: float = 2):
        super().__init__()
        self.health = health
        self.damage = damage

    def create_components(self, owner: AbstractEntity) -> None:
        HealthComponent(owner, self.health)
        HealthBarComponent(owner)
        CollisionWeaponComponent(owner, self.damage)
