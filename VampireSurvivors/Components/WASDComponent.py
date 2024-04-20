import math

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
        angle = self._get_angle_to_move()
        if angle is not None:
            self._pos_component.move_towards_angle(angle, self._move_speed * dt)

    def _one_of_keys_pressed(self, keys: list[int], keys_pressed) -> bool:
        for _key in keys:
            if keys_pressed[_key]:
                return True
        return False

    def should_move_forward(self) -> bool:
        return self._one_of_keys_pressed(settings.FORWARD_KEYS, key.get_pressed())

    def should_move_backwards(self) -> bool:
        return self._one_of_keys_pressed(settings.BACKWARDS_KEYS, key.get_pressed())

    def should_move_left(self) -> bool:
        return self._one_of_keys_pressed(settings.LEFT_KEYS, key.get_pressed())

    def should_move_right(self) -> bool:
        return self._one_of_keys_pressed(settings.RIGHT_KEYS, key.get_pressed())

    def _get_angle_to_move(self):
        FORWARD = self.should_move_forward()
        BACKWARDS = self.should_move_backwards()
        LEFT = self.should_move_left()
        RIGHT = self.should_move_right()

        amount_of_keys_pressed = sum([FORWARD, BACKWARDS, LEFT, RIGHT])
        if amount_of_keys_pressed > 2 or amount_of_keys_pressed == 0:
            return

        FORWARD_RIGHT = FORWARD and RIGHT
        if FORWARD_RIGHT:
            return 1.75 * math.pi

        FORWARD_LEFT = FORWARD and LEFT
        if FORWARD_LEFT:
            return 1.25 * math.pi

        BACKWARDS_RIGHT = BACKWARDS and RIGHT
        if BACKWARDS_RIGHT:
            return 0.25 * math.pi

        BACKWARDS_LEFT = BACKWARDS and LEFT
        if BACKWARDS_LEFT:
            return 0.75 * math.pi

        if FORWARD:
            return 1.5 * math.pi
        if BACKWARDS:
            return 0.5 * math.pi
        if LEFT:
            return math.pi
        if RIGHT:
            return 0

