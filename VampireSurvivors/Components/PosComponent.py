import math

from pygame import Vector2

from Components.ComponentInterface import ComponentInterface


class PosComponent(ComponentInterface):
    def __init__(self, pos: Vector2, size: float, offset: Vector2 = Vector2(0, 0)):
        self._pos: Vector2 = pos + offset
        self._offset: Vector2 = offset
        self._size: float = size

    def update(self, dt):
        pass

    def move_towards_angle(self, angle: float, distance: float) -> None:
        self._pos.x += distance * math.cos(angle)
        self._pos.y += distance * math.sin(angle)

    def get_angle_to_pos(self, to_pos: Vector2):
        delta_y = to_pos.y - self._pos.y
        delta_x = to_pos.x - self._pos.x
        return math.atan2(delta_y, delta_x)

    def get_pos(self) -> Vector2:
        return self._pos

    def set_pos(self, pos: Vector2) -> None:
        self._pos = pos

    def get_offset(self) -> Vector2:
        return self._pos

    def set_offset(self, offset: Vector2) -> None:
        self._offset = offset

    def get_size(self) -> float:
        return self._size

    def set_size(self, size: float) -> None:
        self._size = size
