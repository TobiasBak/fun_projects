import math

import pygame
from pygame import Vector2

from Entity.EntityInterface import EntityInterface
from World.World import World


class Enemy(EntityInterface):
    def __init__(self, health: float, color: str, position: Vector2, size: float, speed: float):
        super().__init__(health, color, position, size, speed)

    def update(self, dt: float):
        self._move_towards_player(dt)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.position, self.size)

    def get_position(self):
        pass

    def set_position(self, position):
        pass

    def _move_towards_player(self, dt: float):
        world = World.get_world()
        player = world.get_player()
        player_pos = player.get_position()
        if self.position.distance_to(player_pos) < player.get_size() + self.size:
            return

        angle = self._get_angle_to_pos(player_pos)
        new_pos = self._get_pos_to_move_towards_angle(self.position, angle, self.speed, dt)
        self.set_position(new_pos)

        self.position.x += self.speed * dt * math.cos(angle)
        self.position.y += self.speed * dt * math.sin(angle)

    def _get_angle_to_pos(self, pos: Vector2):
        delta_y = pos.y - self.position.y
        delta_x = pos.x - self.position.x
        return math.atan2(delta_y, delta_x)

    def _get_pos_to_move_towards_angle(self, pos: Vector2, angle: float, speed: float, dt: float):
        return Vector2(pos.x + (speed * math.cos(angle) * dt), pos.y + (speed * math.sin(angle) * dt))
