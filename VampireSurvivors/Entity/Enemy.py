import math

import pygame
from pygame import Vector2

from Entity.EntityInterface import EntityInterface
from Utils.PositionUtils import get_angle_to_pos, get_pos_to_move_towards_angle, get_distance_to_move
from World.World import World


class Enemy(EntityInterface):
    def __init__(self, health: float, color: str, position: Vector2, radius: float, speed: float):
        super().__init__(health, color, position, radius, speed)

    def update(self, dt: float):
        self._move_towards_player(dt)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.position, self.radius)

    def _move_towards_player(self, dt: float):
        world = World.get_world()
        player = world.get_player()
        player_pos = player.get_position()

        angle = get_angle_to_pos(self.position, player_pos)
        new_pos = get_pos_to_move_towards_angle(self.position, get_distance_to_move(self.speed, dt), angle)
        self.set_position(new_pos)

        self.position.x += self.speed * dt * math.cos(angle)
        self.position.y += self.speed * dt * math.sin(angle)
