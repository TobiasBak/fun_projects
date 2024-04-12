from Components.AbstractWeaponComponent import AbstractWeaponComponent
from Components.HealthComponent import HealthComponent
from Entity.EntityInterface import EntityInterface
from Utils.CollisionUtils import entities_collide
from World.World import World


class CollisionWeaponComponent(AbstractWeaponComponent):
    def __init__(self, owner, damage: float):
        super().__init__(owner, damage)

    def get_damage(self) -> float:
        return self.damage

    def set_damage(self, damage: float) -> None:
        self.damage = damage

    def update_logic(self, dt: float):
        world: World = World.get_world()
        player: EntityInterface = world.get_player()
        if entities_collide(self.owner, player):
            player.get_component(HealthComponent).set_health(
                player.get_component(HealthComponent).get_health() - self.damage
            )
            return True

        return False
