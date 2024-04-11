import pygame
from pygame import Vector2

from Entity.EntityInterface import EntityInterface
from World.World import World
from consts import GAME_HEIGHT, GAME_WIDTH


class Player(EntityInterface):
    def __init__(self, health: float, color: str, pos: Vector2, size: float, speed: float):
        super().__init__(health, color, pos, size, speed)
        self.gold: int = 0
        self.attack_range: float = 400
        self.attack_damage: float = 10
        self.cooldown_before_attack: float = 0.2

    def update(self, dt: float) -> None:
        self._move_player(dt)
        self._teleport_player_if_out_of_bounds()

    def draw(self, screen) -> None:
        pygame.draw.circle(screen, self.color, self.position, self.size)

    def _teleport_player_if_out_of_bounds(self) -> None:
        if self.position.x < 0:
            self.position.x = GAME_WIDTH
        if self.position.x > GAME_WIDTH:
            self.position.x = 0
        if self.position.y < 0:
            self.position.y = GAME_HEIGHT
        if self.position.y > GAME_HEIGHT:
            self.position.y = 0

    def _move_player(self, dt) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.position.y -= self.speed * dt
        if keys[pygame.K_s]:
            self.position.y += self.speed * dt
        if keys[pygame.K_a]:
            self.position.x -= self.speed * dt
        if keys[pygame.K_d]:
            self.position.x += self.speed * dt

    def _attack_nearest_enemy(self, dt) -> None:
        if self.cooldown_before_attack > 0:
            self.cooldown_before_attack -= dt
            return
        world = World.get_world()
        for entity in world.entities:
            if entity == self:
                continue
            if self.position.distance_to(entity.get_position()) < self.attack_range:
                entity.health -= self.attack_damage
                return
