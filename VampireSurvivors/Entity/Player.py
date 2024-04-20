import pygame
from pygame import Vector2

from Entity.EntityInterface import EntityInterface
from settings import GAME_HEIGHT, GAME_WIDTH


class Player(EntityInterface):
    def __init__(self, radius: float, speed: float, weight: float = 2.0):
        super().__init__()
        self.gold: int = 0
        self.attack_range: float = 400
        self.attack_damage: float = 10
        self.cooldown_before_attack: float = 0.2

    def update(self, dt: float) -> None:
        super().update(dt)
        self._move_player(dt)
        self._teleport_player_if_out_of_bounds()

    def render(self, screen) -> None:
        super().render(screen)
        pygame.draw.circle(screen, self.color, self.position, self.radius)

    def _teleport_player_if_out_of_bounds(self) -> None:
        if self.position.x < 0:
            self.position.x = GAME_WIDTH
        if self.position.x > GAME_WIDTH:
            self.position.x = 0
        if self.position.y < 0:
            self.position.y = GAME_HEIGHT
        if self.position.y > GAME_HEIGHT:
            self.position.y = 0

