from Components.AbstractComponent import AbstractComponent
from World.World import World


class CollisionWeaponComponent(AbstractComponent):
    def __init__(self, owner, damage: float):
        super().__init__(owner)
        self.damage = damage

    def get_damage(self) -> float:
        return self.damage

    def set_damage(self, damage: float) -> None:
        self.damage = damage

    def update(self, dt: float):
        world = World.get_world()
        player = world.get_player()
