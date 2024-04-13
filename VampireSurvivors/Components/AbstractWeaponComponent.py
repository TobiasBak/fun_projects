from Components.AbstractComponent import AbstractComponent


class AbstractWeaponComponent(AbstractComponent):
    def __init__(self, owner, damage: float, attack_cooldown: float = 0.5):
        super().__init__(owner)
        self.damage = damage
        self.attack_cooldown = attack_cooldown
        self.time_since_last_attack = 0
        self.bullet_speed = 0
        self.bullet_radius = 0

    def get_damage(self) -> float:
        return self.damage

    def set_damage(self, damage: float) -> None:
        self.damage = damage

    def get_cooldown(self) -> float:
        return self.attack_cooldown

    def set_cooldown(self, cooldown: float) -> None:
        self.attack_cooldown = cooldown

    def update(self, dt: float):
        if self.time_since_last_attack < self.attack_cooldown:
            self.time_since_last_attack += dt
            return

        did_run = self.update_logic_to_run_after_cooldown(dt)
        self.time_since_last_attack = 0 if did_run else self.time_since_last_attack + dt

    def update_logic_to_run_after_cooldown(self, dt: float) -> bool:
        """ Override this method tom implement the logic of the weapon"""
        pass

    def attack(self):
        pass
