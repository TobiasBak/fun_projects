from Components.ComponentInterface import ComponentInterface


class PosComponent(ComponentInterface):
    def __init__(self, pos: Vector2, offset: Vector2, size: float):
        self._pos: Vector2 = pos + offset
        self._offset: Vector2 = offset
        self._size: float = size

    def update(self, dt):
        pass

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

    def set_size(self, size: float) -> float:
        self._size = size