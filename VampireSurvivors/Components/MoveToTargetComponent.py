from Components.ComponentInterface import ComponentInterface
from Components.PosComponent import PosComponent


class MoveToTargetComponent(ComponentInterface):
    def __init__(self, pos_component: PosComponent, target_pos_component: PosComponent, move_speed: float):
        self._pos_component: PosComponent = pos_component
        self._target_pos_component: PosComponent = target_pos_component
        self._move_speed: float = move_speed

    def update(self, dt: float) -> None:
        self._move_towards_target_pos(dt)

    def _move_towards_target_pos(self, dt: float):
        angle = self._pos_component.get_angle_to_pos(self._target_pos_component.get_pos())
        # new_pos = get_pos_to_move_towards_angle(self.position, get_distance_to_move(self.speed, dt), angle)
        # self.set_position(new_pos)

        self._pos_component.move_towards_angle(angle, self._move_speed * dt)
