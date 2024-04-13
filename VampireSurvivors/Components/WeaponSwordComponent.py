from pygame import Surface, SurfaceType

from Components.AbstractWeaponComponent import AbstractWeaponComponent
from Events.Events import BulletEvent
from Utils.BulletUtils import BulletConfigSword


class SwordWeaponComponent(AbstractWeaponComponent):
    def __init__(self, owner, damage: float, attack_cooldown: float):
        super().__init__(owner, damage, attack_cooldown)

    def get_damage(self) -> float:
        return self.damage

    def set_damage(self, damage: float) -> None:
        self.damage = damage

    def update_logic_to_run_after_cooldown(self, dt: float) -> bool:
        self.event_manager.dispatch_event(BulletEvent(self, BulletConfigSword()))
        return True

    def render(self, screen: Surface | SurfaceType):
        pass
