from Components.AbstractComponent import AbstractComponent
from Entity.AbstractEntity import AbstractEntity
from Events.Events import AttackEvent


class HealthComponent(AbstractComponent):
    def __init__(self, entity: AbstractEntity, health):
        super().__init__(entity)
        self.event_manager.add_listener(AttackEvent, self.handle_attack_event)
        self.health = health

    def get_health(self) -> float:
        return self.health

    def set_health(self, health: float) -> None:
        self.health = health

    def handle_attack_event(self, event: AttackEvent) -> None:
        if event.target == self.owner:
            self.health -= event.damage

        if self.health <= 0:
            self.owner.clean_up()
