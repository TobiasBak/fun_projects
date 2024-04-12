from pygame import Surface, SurfaceType

from Components.AbstractWeaponComponent import AbstractWeaponComponent
from Components.CollisionComponent import CollisionComponent


class SwordWeaponComponent(AbstractWeaponComponent):
    def __init__(self, owner, damage: float):
        super().__init__(owner, damage)

    def get_damage(self) -> float:
        return self.damage

    def set_damage(self, damage: float) -> None:
        self.damage = damage

    def update_logic(self, dt: float) -> bool:
        return False

    def create_sword_collision_components(self):
        CollisionComponent(self, self.get_position(), self.get_radius(), self.weight)

    def render(self, screen: Surface | SurfaceType):
        pass