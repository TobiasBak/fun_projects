from pygame import key

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
        keys_pressed = key.get_pressed()  # Todo: This might not work
        if self._one_of_keys_pressed(settings.FORWARD_KEYS, keys_pressed):
            self._pos_component.get_pos().y -= self._move_speed * dt
        if self._one_of_keys_pressed(settings.BACKWARDS_KEYS, keys_pressed):
            self._pos_component.get_pos().y += self._move_speed * dt
        if self._one_of_keys_pressed(settings.LEFT_KEYS, keys_pressed):
            self._pos_component.get_pos().x -= self._move_speed * dt
        if self._one_of_keys_pressed(settings.RIGHT_KEYS, keys_pressed):
            self._pos_component.get_pos().x += self._move_speed * dt

    def _one_of_keys_pressed(self, keys: list[int], keys_pressed) -> bool:
        for _key in keys:
            if keys_pressed[_key]:
                return True
        return False
