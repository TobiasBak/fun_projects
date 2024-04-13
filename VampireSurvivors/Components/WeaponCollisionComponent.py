from Components.AbstractWeaponComponent import AbstractWeaponComponent
from Entity.EntityInterface import EntityInterface
from Utils.CollisionUtils import entities_collide
from World.World import World
from Events.Events import AttackEvent


class CollisionWeaponComponent(AbstractWeaponComponent):
    def __init__(self, owner, damage: float, attack_cooldown: float = 0.5):
        super().__init__(owner, damage, attack_cooldown)

    def get_damage(self) -> float:
        return self.damage

    def set_damage(self, damage: float) -> None:
        self.damage = damage

    def update_logic_to_run_after_cooldown(self, dt: float):
        world: World = World.get_world()
        player: EntityInterface = world.get_player()
        if entities_collide(self.owner, player):
            self.event_manager.dispatch_event(AttackEvent(player, self.damage))
            return True

        return False
