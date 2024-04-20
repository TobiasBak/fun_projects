import settings
from Components.ComponentInterface import ComponentInterface
from Components.PosComponent import PosComponent


class WASDComponent(ComponentInterface):
    """ Handles user input wanting to move"""

    def __init__(self, pos_component: PosComponent, move_speed: float):
        self._pos_component: PosComponent = pos_component
        self._move_speed: float = move_speed

    def update(self, dt: float) -> None:
        self._move_pos(dt)

    def _move_pos(self, dt: float) -> None:
        keys = pygame.key.get_pressed() #Todo: This might not work
        if settings.FORWARD_KEYS in keys:
            self._pos_component.y -= self._move_speed * dt
        if settings.BACKWARDS_KEYS in keys:
            self._pos_component.y += self._move_speed * dt
        if settings.LEFT_KEYS in keys:
            self._pos_component.x -= self._move_speed * dt
        if settings.RIGHT_KEYS in keys:
            self._pos_component.x += self._move_speed * dt
