from Components.AbstractComponent import AbstractComponent


class AbstractWeaponComponent(AbstractComponent):
    def __init__(self, owner, damage: float, cooldown: float = 0.2):
        super().__init__(owner)
        self.damage = damage
        self.cooldown = cooldown
        self.time_since_last_attack = 0

    def get_damage(self) -> float:
        return self.damage

    def set_damage(self, damage: float) -> None:
        self.damage = damage

    def get_cooldown(self) -> float:
        return self.cooldown

    def set_cooldown(self, cooldown: float) -> None:
        self.cooldown = cooldown

    def update(self, dt: float):
        if self.time_since_last_attack < self.cooldown:
            self.time_since_last_attack += dt
            return

        did_run = self.update_logic(dt)
        self.time_since_last_attack = 0 if did_run else self.time_since_last_attack + dt

    def update_logic(self, dt: float) -> bool:
        """ Override this method tom implement the logic of the weapon"""
        pass

    def attack(self):
        pass
