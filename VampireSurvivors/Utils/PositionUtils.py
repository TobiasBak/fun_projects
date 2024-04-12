import math

from pygame import Vector2


def get_angle_to_pos(from_pos: Vector2, to_pos: Vector2):
    delta_y = to_pos.y - from_pos.y
    delta_x = to_pos.x - from_pos.x
    return math.atan2(delta_y, delta_x)


def get_pos_to_move_towards_angle(pos: Vector2, distance: Vector2, angle_to_target: float):
    return Vector2(pos.x + distance.x * math.cos(angle_to_target), pos.y + distance.y * math.sin(angle_to_target))


def get_distance_to_move(speed: float, dt: float):
    return Vector2(speed * dt, speed * dt)
