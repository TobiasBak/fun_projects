from pygame import Vector2

from Components.CollisionComponent import CollisionComponent
from Components.HealthBarComponent import HealthBarComponent
from Components.HealthComponent import HealthComponent
from Components.WeaponCollisionComponent import CollisionWeaponComponent
from Components.WeaponSwordComponent import SwordWeaponComponent
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
        CollisionComponent(owner, owner.get_radius(), owner.weight)


class DefaultPlayerComponentFactory(DefaultLivingEntityComponentFactory):
    def __init__(self, health: float = 100, damage: float = 2):
        super().__init__(health, damage)

    def create_components(self, owner: AbstractEntity) -> None:
        super().create_components(owner)
        SwordWeaponComponent(owner, self.damage, 1)


class DefaultEnemyComponentFactory(DefaultLivingEntityComponentFactory):
    def __init__(self, health: float = 20, damage: float = 2):
        super().__init__(health, damage)


class DefaultBulletEntityComponentFactory(ComponentFactory):
    def __init__(self):
        super().__init__()

    def create_components(self, owner: AbstractEntity) -> None:
        CollisionComponent(owner, owner.radius, owner.weight)
