import pygame
from pygame import Vector2, Surface, transform

from Entity.EntityInterface import EntityInterface
from World.World import World


class Bullet(EntityInterface):
    def __init__(self, color: str, pos: Vector2, damage: float, speed: float, radius: float, lifetime: float):
        super().__init__(color, pos, radius, speed)
        self.damage = damage
        self.lifetime = lifetime
        self.attacked_entities: list[EntityInterface] = []

        self._create_and_add_to_world()

    def get_if_entity_should_be_attacked(self, entity: EntityInterface) -> bool:
        if entity not in self.attacked_entities:
            self.attacked_entities.append(entity)
            return True
        return False

    def update(self, dt: float) -> None:
        super().update(dt)
        self.lifetime -= dt
        copy_of_components = self.components.copy()
        if self.lifetime <= 0:
            for component in copy_of_components.values():
                component.clean_up()
            self.clean_up()

    def render(self, screen: Surface) -> None:
        super().render(screen)
        img = pygame.image.load("assets/default_bullet.png")
        img2 = transform.scale(img, (int(self.radius), int(self.radius)))
        screen.blit(img2, self.position - Vector2(self.radius/2, self.radius/2))
        # pygame.draw.circle(screen, self.color, self.position, self.radius)

    def _create_and_add_to_world(self):
        World.get_world().add_entity(self)

    def clean_up(self):
        World.get_world().remove_entity(self)
