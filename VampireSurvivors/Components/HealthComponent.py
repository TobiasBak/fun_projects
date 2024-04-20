from Components.ComponentInterface import ComponentInterface
from Events.EventManager import EventManager
from Events.Events import AttackEvent


class HealthComponent(ComponentInterface):
    def __init__(self, health: float):
        self._health = health
        EventManager.get_instance().add_listener(AttackEvent, self.handle_attack_event)

    def update(self, dt: float) -> None:
        pass

    def get_health(self) -> float:
        return self._health

    def set_health(self, health: float) -> None:
        self._health = health

    # ToDo: fix below
    def handle_attack_event(self, event: AttackEvent) -> None:
        # if event.target == self.owner:
        #     self._health -= event.damage
        #
        # if self._health <= 0:
        #     self.owner.clean_up()
        pass
