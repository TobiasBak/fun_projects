from Components.AbstractWeaponComponent import AbstractWeaponComponent
from Entity.AbstractEntity import AbstractEntity
from Utils.CollisionUtils import entities_collide
from World.World import World
from Events.Events import AttackEvent


class CollisionWeaponComponent(AbstractWeaponComponent):
    def __init__(self, owner, damage: float):
        super().__init__(owner, damage)

    def get_damage(self) -> float:
        return self.damage

    def set_damage(self, damage: float) -> None:
        self.damage = damage

    def update_logic(self, dt: float):
        world: World = World.get_world()
        player: AbstractEntity = world.get_player()
        if entities_collide(self.owner, player):
            self.event_manager.dispatch_event(AttackEvent(self.owner, player, self.damage))
            return True

        return False
